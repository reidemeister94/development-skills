---
name: using-development-skills
description: Use when starting any conversation - establishes how the development-skills plugin works and how to invoke its components on each platform (Claude Code, Codex). Read first.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply, you MUST invoke it. Not negotiable. Not optional. You cannot rationalize your way out.
</EXTREMELY-IMPORTANT>

# Using development-skills

## Iron Rules

8 Core Pillars + 3 process rules. Canonical: `shared/iron-rules.md`. Do not duplicate.

## Triage & Flow

**Before reading the user's task content in depth, classify the task:**

1. **PASS_THROUGH** (trivial, 1 file, fully reversible, no design choice) → execute directly.
2. **FULL** (everything else, default) → 4 phases, sequential, mandatory:
   - **Phase 1**: plan file in `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__slug.md` with HOW-level Q&A locks (data shapes / edge cases / error semantics / contract boundaries / test scope / rollback).
   - **Phase 2**: chronicle in `docs/chronicles/NNNN__YYYY-MM-DD__topic.md` capturing initial decisions.
   - **Phase 3**: implement with Red/Green TDD.
   - **Phase 4**: `staff-reviewer` subagent review.

**Rules during FULL:**

- External spec/guide/prior brainstorming exists → skip brainstorming only. Phase 1-4 still run. The spec is INPUT to Phase 1, not a substitute. A guide's own gates and numbered steps STACK with the workflow, they do not replace it.
- Ambiguity ≥1% on any HOW-level dimension → ask the user (`AskUserQuestion` on Claude Code for discrete options; plain text otherwise).
- Phase skipping detected mid-execution → stop, rejoin at the missed phase, produce its artifact, continue.

**Routing:** Bug fixes → `development-skills:debugging`. Test work → `development-skills:create-test`.

## Platform

- **Claude Code**: skills auto-activate. Subagent `staff-reviewer` via `Task`/`Agent` with `subagent_type: development-skills:staff-reviewer`. Hooks fire automatically.
- **Codex**: skills auto-discovered (see `.codex/INSTALL.md`). Subagent via `spawn_agent` (requires `multi_agent = true`). No hooks. Full mapping: `references/codex-tools.md`.

## User Override

User instructions (`CLAUDE.md`, `AGENTS.md`, direct requests) > development-skills > default system prompt.
