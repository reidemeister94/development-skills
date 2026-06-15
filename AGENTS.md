# Development skills

This repo IS the source of the `development-skills` plugin: a 3-tier workflow (PASS_THROUGH · LIGHT · FULL 4-phase) plus skills, hooks, and a single `staff-reviewer` subagent, distributed to Claude Code and Codex CLI.

0. **Don't pander · be critical.** Challenge assumptions, push back on bad ideas. No flattery openers. User confirmation validates the decision, not the analysis.
1. **Think before coding.** State assumptions explicitly. Ask when unclear. Don't guess, don't hide confusion.
2. **Plan before implementing.** Explore → plan → lock the HOW (edge cases · data shapes · error semantics · contract boundaries · test scope · rollback) → code.
3. **Simplicity by default.** Minimum code that solves the problem. Three filters before adding anything: existing mechanism covers >50%? · can this be one fewer file / abstraction / config / dependency? · would removing it cause a real failure? A refactor must measurably improve one of: clear · descriptive · efficient · performant · reliable · robust · maintainable.
4. **Surgical changes.** Every changed line traces to the request. No refactoring of adjacent code. No error handling for impossible scenarios. Clean up only your own mess.
5. **All signal, zero noise.** No dead branches, no defensive try/catch on safe paths, no wrapper-for-nothing functions, no unused imports. No filler openers, no trailing summaries when the diff is the answer.
6. **Comments explain WHY, not WHAT.** Non-obvious business logic, hidden constraints, workarounds — yes. Restating what the next line does — no.
7. **TDD: Red → Green → Refactor.** No production code without a failing test first. One test = one cycle. Wrote production code before the test? Delete it. Untestable (UI-heavy / infrastructure / config-only) → closest automated check + documented WHY + manual evidence.
8. **No claim without fresh evidence.** IDENTIFY → RUN → READ → VERIFY → CLAIM. *"I'm confident"* is not a step. Skipping any step = lying, not verifying.
9. **Root cause, not symptoms.** Fix the underlying error, never suppress it. `# type: ignore`, swallowed exceptions, disabled tests, `--no-verify` are admissions the bug is winning.
10. **Document every discovery** (anything you lacked at the start — non-obvious, domain·infrastructure·company·project-specific). WHY → `docs/chronicles/`, HOW → `docs/plans/`; a critical always-read fact → one line in the `AGENTS.md` list; a topic with depth → `.agents/rules/<topic>.md` (same convention), indexed from `AGENTS.md`. Fewest words. Pay investigation costs once.
11. **Context is the constraint.** Subagents isolate noise. Compact early. References on demand, not eagerly. Standing instructions, not one-shot steps.
12. **No commits without explicit user request.** Approving a plan, completing phases, passing review — none are permission. Omit AI-attribution trailers when authorized.
13. **Slim docs · English · memory ≈ empty.** `AGENTS.md` ≤ 70 lines: principles → *use development-skills* → single fewest-words list of the most critical, non-trivial domain·infra·company·project facts → index to `.agents/rules/`; no section headings. Each rules file: same convention, vertical per topic. English only across all artifacts. Teammates share only the repo — memory is per-machine and invisible to them: project facts live in `AGENTS.md` / `.agents/rules/`, never in memory; machine-specific facts → gitignored `.claude/CLAUDE.md` / `~/.codex/AGENTS.md`; memory stays ≈ empty.

- Canonical Iron Rules — 14 principles (0-13) + 1 meta-rule (spirit beats letter) — live in `shared/iron-rules.md`; never restate them in skills, AGENTS.md, README, or chronicles — reference by path.
- Canonical workflow tiers (LIGHT / FULL) live in `shared/workflow.md`; phase contracts in `shared/phases/`. A change to a phase file ripples to every FULL execution — edit deliberately.
- Versioning is automated via `make bump-version-{minor,major,patch}` (commitizen): `cz bump` atomically updates `[tool.commitizen] version` in `pyproject.toml`, `VERSION`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `.claude-plugin/marketplace.json`, then creates the annotated git tag `$version`. Never bump version files manually.
- Only one named subagent ships: `staff-reviewer`. Implementation and verification run in the main thread per `shared/phases/phase-3-implement-verify.md` — do not introduce extra subagents without explicit design discussion.
- Hooks in `hooks/` run natively on Claude Code and on Codex 0.131+ (auto-loaded); Codex 0.128–0.130 needs `[features] plugin_hooks = true` in `~/.codex/config.toml`. Document the manual fallback whenever a hook is added.
- `evals/evals.json` is the regression suite — any skill behavior change that moves pass/fail outcomes MUST update the matching eval expectation in the same change.
- `pyproject.toml` exists for plugin-internal scripts (eval runners, lint helpers) — the plugin is markdown-first and not distributed as a PyPI package.
- Personal per-machine context: `.claude/CLAUDE.md` (Claude) or `~/.codex/AGENTS.md` (Codex). Both must stay gitignored; never commit either.

| Rule | Scope (`paths:`) | Topic |
|------|------------------|-------|
| `.agents/rules/skill-authoring.md` | `skills/**`, `agents/**` | SKILL.md / subagent frontmatter, references/ subdirs, what NOT to duplicate from `shared/` |
| `.agents/rules/shared-canonical.md` | `shared/**` | Canonical files inventory; iron-rules / workflow / phases / templates editing rules |
| `.agents/rules/plugin-packaging.md` | `.claude-plugin/**`, `.codex-plugin/**`, `.agents/plugins/**`, `evals/**`, `VERSION`, `CHANGELOG.md`, `pyproject.toml` | Version sync (4 files + pyproject), dual manifest, dual marketplace catalog, marketplace-only install, changelog format, eval suite |
| `.agents/rules/formatting-hooks.md` | `hooks/**` | Auto-format command table, hook authoring conventions, Codex parity |

Local machine instructions: Claude → `.claude/CLAUDE.md` (gitignored). Codex → `~/.codex/AGENTS.md` (user-global) — avoid in-repo `AGENTS.override.md` because Codex loads one file per directory and an override fully replaces this file rather than merging.
