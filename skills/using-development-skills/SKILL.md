---
name: using-development-skills
description: Read at session start to route development work through the direct or full development loop on Claude Code and Codex.
---

# Using development-skills

Skip this file when dispatched as a subagent for one bounded task.

Read the shared [development loop](../../shared/development-loop.md). Resume an in-progress plan at its recorded step; otherwise choose:

- **Direct:** the result, forced solution, and proof are clear; the change is reversible and carries no business or design choice.
- **Full:** anything else. Inspect first, run the `brainstorming` gate (default on; skip criteria in the loop), agree on the result and proof, then plan, get explicit plan approval, chronicle, implement, verify, and review.

Use `create-test` when the task is test work or when the proof needs business, integration, KPI, or probabilistic criteria. Use `best-practices` when current external evidence can change a decision.

Load only applicable language and project conventions discovered in the target repository. Project instructions and the user's request take precedence.

Claude Code names are canonical in older skill bodies. On Codex, translate them with [codex-tools.md](references/codex-tools.md).
