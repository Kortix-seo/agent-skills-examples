---
name: release-check
description: Run the documentation checks that must pass before a release is tagged, and stop at the first one that fails. Use when someone asks whether a release is ready, when a docs change lands on the release branch, or when the test suite is green and nobody has opened the site.
---

# Release check: an open source procedure skill

Kortix is open source, and this procedure is one of the examples in this repository. Copy the folder, keep the steps that match your release, delete the rest.

The script it calls lives in the `link-check` skill, at `skills/link-check/scripts/check_links.py`. Running the script needs no skill grant; only loading a skill does.

## Steps

1. Read `CHANGELOG.md` and write down the version at the top. Every later step refers to it.
2. Compare that version with the version in `package.json`. If they differ, stop and report both strings.
3. Collect the URLs to check: the homepage, every path in `sitemap.xml`, and every link in the changelog section for this version. Write them one per line into `urls.txt`.
4. Run the link check:

   ```bash
   python3 skills/link-check/scripts/check_links.py --file urls.txt
   ```

5. Read the exit code. `0` means every URL answered; `1` means at least one failed; `2` means the command itself could not run. On `1` or `2`, stop and report the failing line the script printed.
6. Open the homepage and one page for each section the release touched. A page that renders without its heading is a failure even when its status was 200.
7. Write `release-report.md`: the version, the commit being checked, the date, and one line per check reading `pass` or `fail` with the command that produced it.
8. Open a change request containing `release-report.md` and the changelog edit. Do not tag the release in the same branch.

## Stop condition

Stop at step 2 when the two versions disagree, at step 5 when the script exits non-zero, and at step 6 when a touched page renders wrong. When you stop, report the step number, the command you ran and its output, and nothing else. Do not tag, and do not edit a page to make a check pass.

## Exit criterion

The check is finished when the script exited `0` on the full URL list, `release-report.md` names the commit and the date, every line in it reads `pass`, and the change request is open with the report in it. A report with one `fail` line is a blocked release, not a finished check.

## What this shape buys you

A procedure that names its steps, its stop condition and its exit criterion can be reviewed by someone who did not write it, and re-run by an agent that has never seen the repository. An instruction to "make sure the release is fine" cannot do either.
