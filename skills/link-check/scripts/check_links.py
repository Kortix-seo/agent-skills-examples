#!/usr/bin/env python3
"""Check a list of URLs and exit non-zero when one of them is broken.

Part of the open source agent skills examples for Kortix
(https://agentskillsguide.dev). Standard library only, so it runs on any
machine with python3 and nothing installed.

Each URL gets a HEAD request first. Servers that refuse HEAD (400, 403, 405,
501) are asked again with GET, because a refusal of the method says nothing
about the page. Redirects are followed and the final status is the one
reported.

Exit codes:
  0  every URL answered with a 2xx or 3xx status
  1  at least one URL failed (4xx, 5xx, timeout, DNS, connection refused)
  2  the command could not run (no URLs, unreadable --file, bad argument)
"""

from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict

USER_AGENT = "check-links/1.0 (agent skills examples; +https://agentskillsguide.dev)"
URL_RE = re.compile(r"^https?://\S+$", re.IGNORECASE)
HEAD_REFUSED = {400, 403, 405, 501}


@dataclass
class Result:
    url: str
    status: int | None
    detail: str
    final_url: str | None = None

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 400


def _request(url: str, method: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    )


def _reason(exc: BaseException) -> str:
    reason = getattr(exc, "reason", exc)
    if isinstance(reason, (socket.timeout, TimeoutError)):
        return "timed out"
    text = str(reason) or reason.__class__.__name__
    return " ".join(text.split())


def check_url(url: str, timeout: float) -> Result:
    """Return the status of one URL. Never raises for a network problem."""
    if not URL_RE.match(url):
        return Result(url, None, "not an http or https URL")

    for method in ("HEAD", "GET"):
        try:
            with urllib.request.urlopen(_request(url, method), timeout=timeout) as response:
                return Result(url, response.status, "ok", response.geturl())
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in HEAD_REFUSED:
                continue
            return Result(url, exc.code, "HTTP %d %s" % (exc.code, exc.reason or ""), None)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            # A connection reset or a dropped HEAD is worth one GET attempt;
            # a DNS failure or a refused connection will fail the same way.
            if method == "HEAD":
                continue
            return Result(url, None, _reason(exc), None)
        except TimeoutError:
            if method == "HEAD":
                continue
            return Result(url, None, "timed out", None)

    return Result(url, None, "no response", None)


def read_url_file(path: str) -> list[str]:
    urls: list[str] = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            item = line.strip()
            if item and not item.startswith("#"):
                urls.append(item)
    return urls


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_links.py",
        description="Check URLs and exit non-zero when one of them is broken.",
        epilog=(
            "exit codes: 0 all URLs answered 2xx or 3xx, 1 at least one URL failed, "
            "2 the command could not run. Example: "
            "python3 skills/link-check/scripts/check_links.py --file urls.txt"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("urls", nargs="*", metavar="URL", help="URL to check; repeat for each one")
    parser.add_argument("-f", "--file", metavar="PATH",
                        help="read URLs from a file, one per line; blank lines and # comments are skipped")
    parser.add_argument("-t", "--timeout", type=float, default=10.0, metavar="SECONDS",
                        help="seconds to wait for each request (default: 10)")
    parser.add_argument("-w", "--workers", type=int, default=8, metavar="N",
                        help="URLs checked at the same time (default: 8)")
    parser.add_argument("--json", action="store_true", help="print a JSON report instead of lines")
    parser.add_argument("--quiet", action="store_true", help="print failing URLs only")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    urls = list(args.urls)
    if args.file:
        try:
            urls.extend(read_url_file(args.file))
        except OSError as exc:
            print("check_links.py: cannot read %s: %s" % (args.file, exc), file=sys.stderr)
            return 2

    if not urls:
        parser.error("give at least one URL, or a file with --file")

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.workers < 1:
        parser.error("--workers must be at least 1")

    # Keep the input order in the report, whatever order the answers arrive in.
    seen: dict[str, Result] = {}
    unique = [u for u in dict.fromkeys(urls)]
    with ThreadPoolExecutor(max_workers=min(args.workers, len(unique))) as pool:
        for result in pool.map(lambda u: check_url(u, args.timeout), unique):
            seen[result.url] = result

    results = [seen[u] for u in unique]
    failed = [r for r in results if not r.ok]

    if args.json:
        print(json.dumps(
            {"checked": len(results), "failed": len(failed),
             "results": [asdict(r) | {"ok": r.ok} for r in results]},
            indent=2,
        ))
    else:
        for r in results:
            if r.ok:
                if not args.quiet:
                    print("ok    %-3s %s" % (r.status, r.url))
            else:
                code = r.status if r.status is not None else "---"
                print("FAIL  %-3s %s  (%s)" % (code, r.url, r.detail))
        print("%d checked, %d failed" % (len(results), len(failed)))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
