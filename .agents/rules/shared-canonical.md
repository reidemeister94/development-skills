---
paths:
  - "shared/**"
---

# Editing canonical workflow docs

`shared/` is the single source of truth for the workflow engine. Skills, subagents, and phases reference these files by path. Editing here ripples to every consumer — be deliberate.

## Canonical files (DO NOT duplicate elsewhere)

| File | Role |
|------|------|
| `shared/iron-rules.md` | 9 Core Pillars + 4 Process Rules (A · B · C · D). Authoritative behavioral standard. Every skill references it. |
| `shared/workflow.md` | LIGHT (6-step inline) and FULL (4-phase) tiers, plus the triage gate. Authoritative tier definition. |
| `shared/phases/phase-1-research-plan.md` | Phase 1 contract: research, plan file, HOW-level locks, user approval. |
| `shared/phases/phase-2-chronicle.md` | Phase 2 contract: chronicle file or NOT NEEDED annotation. |
| `shared/phases/phase-3-implement-verify.md` | Phase 3 contract: Red/Green TDD, anti-slop check, 5-step verification gate. |
| `shared/phases/phase-4-review-finalize.md` | Phase 4 contract: staff-reviewer two-stage review, finalize, optional commit. |
| `shared/phases/compaction-guide.md` | How to survive `/compact` and `/clear` mid-workflow. |
| `shared/templates/plan-template.md` | Plan file skeleton. NNNN__YYYY-MM-DD__implementation_plan__slug.md naming. |
| `shared/lint-enforcement.md` | JS/TS lint as a blocking gate — union of biome/eslint/oxlint. |
| `shared/package-manager.md` | Package-manager detection contract before any install/run/exec command. |
| `shared/agents/research-agent.md` | Research subagent spec referenced from Phase 1. |

## Editing rules

1. **Never restate iron-rule content elsewhere.** Skills, AGENTS.md, README all reference `shared/iron-rules.md` by path. A copy in two places is a divergence waiting to happen.
2. **Phase contracts are stable interfaces.** A change to `phase-3-implement-verify.md` affects every FULL-tier execution. Change the contract intentionally, not as a side effect of a skill tweak.
3. **Numbering and naming.** Phase files use `phase-N-<slug>.md`. Plan files generated from the template use `NNNN__YYYY-MM-DD__implementation_plan__<slug>.md`. Chronicles use `NNNN__YYYY-MM-DD__<slug>.md`. Do not reformat existing entries.
4. **Markdown style.** No emojis. No flattery. Tables beat prose. Pillar 2 (signal, zero noise) applies to docs.

## What does NOT belong in shared/

- Project-specific examples (those belong in skill `references/`).
- User-facing install instructions (README.md / .codex/INSTALL.md).
- Cross-version changelog narrative (CHANGELOG.md).

If you're about to add a file under `shared/`, ask: would every skill / phase / agent reference it? If not, it belongs elsewhere.
