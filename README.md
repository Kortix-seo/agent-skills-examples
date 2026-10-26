# Open source agent skills examples that run

Kortix is open source, and this repository is three Agent Skills you can copy into your own project today: a router, a release procedure, and a link checker that exits non-zero when a URL is broken. Each one is a folder with a `SKILL.md` inside it. All three are written so an agent can follow them rather than read about them.

The repository is also the argument. A skill that only describes a topic gets loaded and then ignored. What survives in a repo is shaped like a procedure. Numbered steps, a stop condition, an exit criterion, and the command the agent actually runs. All of it stays inert until a grant in `kortix.yaml` names the skill for one agent.

## What is in the box

| Path | What it is | What it demonstrates |
| --- | --- | --- |
| `skills/inbox-router/SKILL.md` | Routes one message to one queue | A description written for the trigger, plus one tie-break |
| `skills/release-check/SKILL.md` | Numbered pre-release steps | A stop condition and an exit criterion a reviewer can check |
| `skills/link-check/SKILL.md` | Wraps the bundled script | A real command, with exit codes the agent reads |
| `skills/link-check/scripts/check_links.py` | Standard library link checker | Code the agent runs, not instructions it interprets |
| `agents/triage.md` | Frontmatter and a system prompt | Behavior in a file you can diff |
| `kortix.yaml` | Manifest for the project | A grant that names two skills for one agent |
| `skills-lock.json` | Pins each skill by path and hash | A skill change shows up as a reviewable diff |

## The fastest path

1. Copy a skill folder into your project at `skills/<name>/`, and keep the folder name equal to the `name` in its frontmatter.
2. Add that name to the `skills:` list of the agent that should be able to load it.
3. Run the script once by hand, so you know what a pass looks like before an agent reports one.

```yaml
agents:
  triage:
    file: agents/triage.md
    skills: [inbox-router, release-check]
```

That snippet is the whole grant, and it matches the manifest here. A skill in `skills/` is usable only when that agent's grant allows it. The line your team reviews is the line that says what the agent can do.

## Run the link checker

```bash
python3 skills/link-check/scripts/check_links.py https://agentskillsguide.dev https://kortix.com
```

It prints one line per URL. Exit `0` means every URL answered with a 2xx or 3xx status, `1` means one failed, and `2` means the command could not run. Pass `--file urls.txt` for a list, `--json` for a machine-readable report, or `--help` for the rest. Standard library only: it runs on a machine with nothing installed but `python3`.

## Left out on purpose

`skills/link-check` is in this repository and missing from `triage`'s `skills:` grant. No agent can load it. That is the point: a folder on disk is not access. Add `link-check` to the list and the same agent can load it on its next session. `release-check` still works without that grant. It calls the script by path, and running a script is a tool rule rather than a skill.

The hashes in `skills-lock.json` cover the skill files as they appear in this repository. Nothing here was copied from another repository, so there is no upstream pin to bump.

## Where the guide explains each piece

Each part of this repository has a longer explanation on the site that goes with it:

- What a skill is, and how its description decides whether an agent loads it: <https://agentskillsguide.dev/what-are-agent-skills>
- How a skill differs from an MCP server, and which layer carries the connection rather than the procedure: <https://agentskillsguide.dev/agent-skills-vs-mcp>
- The three skills in this repository, quoted and read line by line: <https://agentskillsguide.dev/agent-skills-examples>
- Grants, review and the lockfile, in a repository your team owns: <https://agentskillsguide.dev/agent-skills-in-your-repo>

## Where the rest is written down

- [How to write a skill](docs/01-write-a-skill.md): the format, the two required fields, the context budgets, and one worked example.
- [Skills and MCP](docs/02-skills-vs-mcp.md): which layer carries the connection and which carries the procedure.
- [Granting and reviewing skills](docs/03-grant-and-review.md): the lookup order, the `skills` grant, the change request, and hash pinning.
- The specification: <https://agentskills.io/specification>
- More examples and the longer argument: <https://agentskillsguide.dev>
- Kortix: <https://kortix.com>, and [Kortix on GitHub](https://github.com/kortix-ai/suna)

## Copying

The three skills and the script are here to be copied, cut down and changed.

Open source. Read it, fork it, audit it.
