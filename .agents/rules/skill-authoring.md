---
paths:
  - "skills/**"
  - "agents/**"
---

# Skill and subagent authoring

Apply [`shared/skill-authoring.md`](../../shared/skill-authoring.md).

Each skill lives at `skills/<name>/SKILL.md`.
Its frontmatter needs a matching `name` and a specific `description` that states capability and trigger.
Preserve supported invocation, effort, and tool fields.

Keep `SKILL.md` focused on shared purpose, workflow, constraints, and reference routing.
Put substantial optional procedures or examples under `references/` and link them where they become relevant.
Add scripts only when deterministic execution or reuse justifies them.
Do not add placeholder directories or auxiliary README files.

The single named subagent is `agents/staff-reviewer.md`.
Its tools remain read-only and minimal.
Do not add another named subagent without an explicit design decision.

Validate names, frontmatter, links, packaging, and meaningful behavior.
Routing descriptions must distinguish nearby skills.
Tests protect outcomes, not exact prose.
