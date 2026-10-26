---
name: link-check
description: Check a list of URLs for broken links and report the status of each one. Use before a release, after a documentation edit, or when a reader reports a dead link on a page you publish.
---

# Link check: an open source skill with its own script

Kortix is open source, and this skill is the example in this repository that ships code an agent runs instead of instructions it reads.

## Run it

```bash
python3 skills/link-check/scripts/check_links.py https://agentskillsguide.dev https://kortix.com
```

For a longer list, write one URL per line into a file and pass the file. Blank lines and lines starting with `#` are skipped.

```bash
python3 skills/link-check/scripts/check_links.py --file urls.txt
```

`--json` prints a report an agent can parse. `--quiet` prints only the failures. `--timeout` and `--workers` change the pace. `--help` lists the rest.

## What the script reports

One line per URL with the status it got and, for a failure, the reason. It sends a `HEAD` request first and asks again with `GET` when a server refuses the method with 400, 403, 405 or 501, because that refusal says nothing about the page. Redirects are followed, so the status is the last one in the chain.

Exit codes are part of the contract:

- `0`: every URL answered with a 2xx or 3xx status;
- `1`: at least one URL failed, with a 4xx, 5xx, timeout, DNS failure or refused connection;
- `2`: the command could not run, for example a missing `--file` or no URLs at all.

A script that exits 0 on a broken link is worse than no script, because a release check that calls it will pass.

## Rules for the agent

- Report every failing URL with its status or reason. A count tells a reader nothing they can act on.
- Retry a timeout once. A page that answers on the second try is slow, not broken; say so.
- Do not edit a page so that the check passes. A dead link is a fact about the page, and the fix is a decision for the person who owns it.
- A redirect to a sign-in page counts as a failure for a public link, even when the status is 200. Say where it landed.

## Stop condition

Stop at the first run that reports failures. Report the list, and do not keep re-running the same list with a longer timeout.

## Exit criterion

Done when every URL in the list answered with a 2xx or 3xx status, or when the failures are listed with their codes and the run is handed back to the person who asked.
