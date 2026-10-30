# Granting, reviewing, and pinning an open source skill

Kortix is open source. The rules that decide whether a skill ever runs are all files: one names the skill for an agent, one records the change, one holds a hash. A team can read the three together in a single diff.

Authoring is the easy half. The other half is distribution. Which agent is allowed to load this skill? What happens when someone edits it? Which copy does a session end up with? Three questions, three file answers.

## What sits where

```text
kortix.yaml                  the manifest
agents/triage.md             one agent
skills/inbox-router/SKILL.md
skills/release-check/SKILL.md
skills/link-check/SKILL.md
skills/link-check/scripts/check_links.py
```

`kortix.yaml` declares the machine image, connectors and triggers, and secret names and grants. Secret values never appear in the repo. The prompt and the tool rules for one agent live in `agents/<name>.md`: frontmatter for the rules, a body for the system prompt. Skills are folders under `skills/`, each with its `SKILL.md`, and any bundled file sits beside it.

Splitting governance from behavior pays off when a permission question comes up. A wider reach for one agent is a name added to a list, on a line short enough to argue about in a review comment.

## Four places a name is looked up

A session does not read one skills folder. It searches an ordered list, and the first copy of a name wins:

1. the managed `kortix-*` skills;
2. `skills/` in the project;
3. `.kortix/opencode/skills/`, which older projects still use;
4. `harnesses/pi/skills/`, read by pi only.

The managed set is the layer no project can overwrite. Those `kortix-*` skills are copied into every session, and a project folder that reuses one of their names loses the tie. A new project commits `skills/kortix-cli` and nothing else from that set, because git leaves the rest out of the session.

Two consequences follow, and both catch people once. A `skills:` list has to name every `kortix-*` skill the agent needs, since none arrive on their own. And a project skill called `kortix-system` is dead weight.

## The grant, in four shapes

Each agent names the skills it may load in its own `skills:` list. A folder under `skills/` grants nothing on its own.

| `skills:` value | `permission.skill` |
| --- | --- |
| `all` | allow every skill |
| `none` or `[]` | deny every skill |
| a list of names | allow those, deny the rest |
| omitted | grants nothing |

The grant compiles to the agent's `permission.skill` rule. When the key is present it replaces any such rule in the agent file. Left out, the key grants nothing.

This repository shows what a grant is worth. `kortix.yaml` names two skills for `triage`:

```yaml
kortix_version: 3

agents:
  triage:
    prompt_file: agents/triage.md
    skills: [inbox-router, release-check]
```

`skills/link-check` sits in the repo and not in that list, so the agent cannot load it. `release-check` still reaches its script, because the procedure calls `python3 skills/link-check/scripts/check_links.py` and `agents/triage.md` allows that command. Reaching a script and loading instructions are two different permissions.

## The review path

Session work happens on a copy of the repo, on a branch that carries the session's id. The agent commits there. Moving that work onto the default branch takes a change request, and a person holding `project.gitops.merge` reads it and merges it.

A skill diff deserves four readings, and only the first is obvious:

1. the body change, in the skill's own language;
2. new files under `references/` or `scripts/`, which load later and hide in a collapsed diff;
3. the `description` line, when the trigger changed, because that is what the agent reads to decide;
4. the lockfile entry, when the skill came from somewhere else.

## A hash for anything borrowed

`skills-lock.json` pins each skill by source repository, `skillPath` and a `computedHash`, in the same spirit as a dependency lockfile. A `ref` pins a tag as well.

```json
{
  "version": 1,
  "skills": {
    "inbox-router": {
      "source": "agentskillsguide/agent-skills-examples",
      "sourceType": "github",
      "skillPath": "skills/inbox-router/SKILL.md",
      "computedHash": "a6c375b5a9f1114de69de531f8ae5e3cda9d19df00279b1d714761da2c26d39a"
    }
  }
}
```

The hash earns its keep on the day upstream rewrites its skill. Your copy stays the one you read until somebody bumps the hash, and the bump appears in the same change request as the decision to take the new version. Without one, the instructions move under you between two runs, and no diff says so.

## Validate first

```bash
skills-ref validate ./skills/release-check
```

`skills-ref` is the specification's reference library, and it checks frontmatter and naming. Run it in the same change request as the edit, so a reviewer spends their attention on whether the steps are right rather than on whether `name` matches the folder.

## What goes wrong six months later

The failure is rarely a broken skill. It is a folder of skills nobody can account for: instructions pasted in from a blog post, descriptions written as topic labels, no record of who added them or which agent may load them. Six months on, the agent behaves in a way the team cannot explain, and the fix is archaeology.

Three habits prevent it, and each one is a file: a `description` that names the situation, a `skills:` list that names the skills and nothing more, and a lockfile entry with a hash for anything borrowed.
