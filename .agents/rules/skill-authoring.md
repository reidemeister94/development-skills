---
paths:
  - "skills/**"
  - "agents/**"
---

# Skill and subagent authoring

Conventions for editing files under `skills/` and `agents/`. Triggering, structure, and what NOT to duplicate from `shared/`.

## SKILL.md frontmatter

Every skill is a directory under `skills/` with a `SKILL.md` file. Required frontmatter:

```yaml
---
name: <kebab-case-skill-name>
description: Use when <triggering condition>. Use when user says <keyword1>, <keyword2>, or <keyword3>.
---
```

- `name` MUST equal the directory name.
- `description` is the trigger contract — the platform decides whether to invoke the skill from this string alone. Lead with "Use when …" and list explicit keyword triggers the user might type. Specific > generic.
- Body is markdown. No mandatory section headings.

## Agent files

Single subagent today: `agents/staff-reviewer.md`. Implementation and verification run in the main thread per `shared/phases/phase-3-implement-verify.md` — do NOT introduce extra named subagents without explicit design discussion.

Agent frontmatter:

```yaml
---
name: <agent-name>
description: <one-line role description>
tools: Read, Grep, Glob, Bash
---
```

Tool list is the agent's allowlist — keep it minimal.

## What NOT to duplicate

`shared/iron-rules.md` is the canonical Iron Rules. `shared/workflow.md` is the canonical workflow. `shared/phases/*.md` are canonical phase definitions. Skills MUST reference these by path, never restate their content. A skill that copies iron-rule text will drift the moment the canonical version updates.

## References subdirectory

Detailed material that a skill points to but does not load by default goes in `skills/<skill>/references/<topic>.md`. The SKILL.md body references it by relative path. Keeps the SKILL.md body short and the auto-loaded surface small.

## Description triggering — be specific

A vague description ("helps with code") wastes triggering budget. Concrete triggers ("Use when user runs /commit, or asks to commit changes, or staged changes need a conventional commits message") fire reliably. The skill `description` is read on every conversation — treat it as a contract.

## Length budget

SKILL.md body: aim for ≤ 200 lines. Anything longer belongs in `references/`. Pillar 7 (slim docs) applies recursively — every skill obeys it.
