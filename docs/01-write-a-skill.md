# How to write an open source agent skill: folder, frontmatter, budgets

Kortix is open source. The format below is an open standard too, set out at [agentskills.io/specification](https://agentskills.io/specification), and a skill is a directory containing, at minimum, a `SKILL.md` file. Most of the difficulty does not sit in the format. It sits in the two decisions the format leaves to whoever writes the skill: what the description promises, and where the body stops.

## The folder is the unit

```text
skills/link-check/
├── SKILL.md
└── scripts/
    └── check_links.py
```

The folder name is part of the format, not a filing convention. It is checked against `name` before anything loads, so `link-check` inside a folder called `link_check` is invalid even though both strings read the same to a person. Keep the two identical and the question never comes up.

## Frontmatter: two required fields

Frontmatter comes first, then the Markdown body. `SKILL.md` holds YAML frontmatter followed by Markdown content, and `name` and `description` are both required.

```yaml
---
name: link-check
description: Check a list of URLs for broken links and report the status of each one. Use before a release, after a documentation edit, or when a reader reports a dead link on a page you publish.
---
```

`name` is 1 to 64 characters of lowercase letters, digits and hyphens, and must match the folder name. Three further rules catch most bad names: no hyphen at the start, none at the end, never two in a row.

`description` is 1 to 1024 characters, and should say both what the skill does and when to use it. The second half is the one writers skip. It is also the only half that decides whether the skill ever loads, because it is all an agent has at decision time. Write the situation, in the words a person would use in the request: "before a release", "when a reader reports a dead link".

Four fields are optional: `license`, `compatibility` (1 to 500 characters), `metadata` (a string map) and `allowed-tools` (experimental). Set `compatibility` only when the skill depends on something specific, such as a package or network access. Most skills leave all four out.

## What loads, and when

Every skill costs about 100 tokens of metadata at startup. Its body arrives only once the skill is activated, and the recommendation is to stay under 5,000 tokens. Bundled files arrive only when the agent reads them. The main `SKILL.md` should stay under 500 lines, with detailed material in its own file.

That budget explains the shape of a good skill. The description carries the routing decision, because it is present from the first turn. The body carries the work, because it arrives after the decision. References carry what the agent reads once, kept out of every activation.

## Three support folders

Scripts go in `scripts/`, reference documents in `references/`, and templates or data in `assets/`. A script earns its place when it replaces a judgment the agent is bad at: counting things, fetching a list of URLs, parsing a table. Write it self-contained, with an error message a person can act on, and put the edge cases in code rather than in prose the agent has to remember. [The link checker in this repository](../skills/link-check/scripts/check_links.py) reads top to bottom in a few minutes and documents its exit codes in `--help`.

## The body

The Markdown body has no format restrictions; the specification recommends step-by-step instructions, input and output examples, and common edge cases. Three additions turn a description of a topic into a procedure:

- Steps, numbered, in the order they run, each an action rather than a subject.
- A stop condition: where the procedure ends without finishing, and what to report instead. "Stop at step 5 when the script exits non-zero" is one.
- An exit criterion: how the agent knows the work is done, in terms it can check. "Every URL answered with a 2xx or 3xx status" is one. "The release looks good" is not.

"You are an expert at releases, be thorough" gives an agent nothing to do differently on the next run. A body with those three parts can be re-run by a model that has never seen the repository, and reviewed by a person who did not write it.

## One worked example

[`skills/release-check/SKILL.md`](../skills/release-check/SKILL.md) carries all of it. Read it for the missing parts as much as the present ones: no background section, no glossary, no advice about quality. Step 4 is a command. Step 5 reads the exit code of that command, and the stop condition names the step number where the procedure ends.

## Validate before you commit

The command is `skills-ref validate ./skills/link-check`. That library comes with the specification, and it checks frontmatter and naming. Run it before anyone reads the diff. Name casing, a hyphen in the wrong place and a 1,100-character description are mechanical questions. A reviewer's attention is better spent on whether the steps are right.

## Checklist

- [ ] folder name equals `name`, in lowercase, digits and single hyphens
- [ ] description says what the skill does and when to use it
- [ ] body has numbered steps, a stop condition and an exit criterion
- [ ] any script runs on its own and exits non-zero when it fails
- [ ] `skills-ref validate` passes
- [ ] the agent's `skills:` grant names the skill
