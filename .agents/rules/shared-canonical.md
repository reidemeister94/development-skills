---
paths:
  - "shared/**"
---

# Editing canonical workflow docs

`shared/` is the single source of truth for the workflow. Skills and the subagent reference these files by path. Editing here ripples to every consumer — be deliberate.

## Canonical files (DO NOT duplicate elsewhere)

| File | Role |
|------|------|
| `shared/development-loop.md` | The authoritative loop: direct/full paths, the full-path steps, the standards gate, and the working-rule principles. Every skill references it. |
| `shared/writing.md` | The writing contract for every piece of natural language — chat, docs, comments, commits. |
| `shared/documentation.md` | The repository documentation format: Open Knowledge Format frontmatter plus plan/chronicle lifecycle metadata. |
| `shared/review-categories.md` | Canonical CRITICAL/HIGH/MEDIUM/LOW severity definitions for every review surface. |
| `shared/skill-authoring.md` | Reduce-gate for authoring/editing any skill, reference, or plugin doc. Referenced from `staff-reviewer`. |
| `shared/templates/plan-template.md` | Plan file skeleton. `NNNN__YYYY-MM-DD__implementation_plan__slug.md` naming. |
| `shared/templates/chronicle-template.md` | Chronicle file skeleton. `NNNN__YYYY-MM-DD__slug.md` naming. |

## Editing rules

1. **Never restate loop content elsewhere.** Skills, AGENTS.md, README all reference `shared/development-loop.md` by path. A copy in two places is a divergence waiting to happen.
2. **The loop is a stable interface.** A change to `development-loop.md` affects every full-path execution. Change it intentionally, not as a side effect of a skill tweak.
3. **Numbering and naming.** Plan files use `NNNN__YYYY-MM-DD__implementation_plan__<slug>.md`. Chronicles use `NNNN__YYYY-MM-DD__<slug>.md`. Do not reformat existing entries.
4. **Markdown style.** No emojis. No flattery. Tables beat prose. The signal-over-noise rule applies to docs.

## What does NOT belong in shared/

- Project-specific examples (those belong in skill `references/`).
- User-facing install instructions (README.md is the single source).
- Cross-version changelog narrative (CHANGELOG.md).
- Language-specific conventions — this plugin is language-agnostic and ships none.

If you're about to add a file under `shared/`, ask: would every skill / agent reference it? If not, it belongs elsewhere.
