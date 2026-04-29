## 0.3.0 (2026-04-29)

### Feat

- **brainstorming**: refactored to in-thread conversational design. Walk the design tree with the user one branch at a time (Step 2 Q&A via `AskUserQuestion` on Claude Code, numbered list + STOP on Codex), then optionally delegate web research to a subagent, then write a plan and gate before handing off. Renames `analysis-agent.md` → `research-agent.md` (research-only role; Q&A stays in main thread). Adds `references/design-it-twice.md` for parallel-design technique. New `<HARD-GATE>` and "This Is Too Simple To Need A Design" anti-pattern at the top, plus PASS_THROUGH triage for genuinely trivial tasks.
- **using-development-skills**: strengthens enforcement with `<EXTREMELY-IMPORTANT>` "1% chance" rule, Instruction Priority section, 5-step Skill Flow, expanded Red Flags table (15 rows), Skill Types and User Instructions sections.
- **hooks/session-start**: mirrors `obra/superpowers` approach — injects the full `using-development-skills/SKILL.md` body as `additionalContext` so skill-routing rules and anti-rationalization devices load from token 0 (no auto-discovery dependency).
- **ai-agent-bench**: major simplification — replaces Phase A/Phase B verification design with a single `outer_check` (live e2e correctness + wall time) recorded once before and once after the agent session. Drops `gate_cmd`/`measure_cmd` split, sufficiency check, prompt hygiene gate, and most TOML knobs. Adds `monitor.py` sidecar for 3-min heartbeat; consolidates references into `agents.md` (how to add an agent) + `anomalies.md` (anomaly log format and triggers).
- **create-test**: adds `references/tdd-workflow.md` for vertical-slice red-green-refactor loop and "no horizontal slicing" anti-pattern.
- **roast-my-code**: adds `references/architectural-depth.md` (module / interface / depth / seam / adapter glossary, deletion test, friction signals).

### Fix

- **claude-to-codex**: generic "appropriate test suites" wording replaces project-specific test suite names in the agent context template.

## 0.2.1 (2026-04-23)

### Feat

- ai-agent-bench: add `measure_repetitions` knob — run `measure_cmd` N times per phase (baseline + post) to beat measurement noise on perf benchmarks. Added `--measure-reps` CLI flag on `run_trial.py`, automatic merging of indexed runs in `parse_transcript.py` (fast-cluster min across reps, pooled stddev), and "Two orthogonal axes" methodology section (agent sessions × measurement reps) so users tune the right knob.
- README / CLAUDE.md: reframe plugin as dual-platform (Claude Code + Codex CLI) now that the Codex install path is stable.

### Fix

- python-dev patterns: replace domain-specific service example with a generic `UserService` example so the sample code is universally applicable.

## 0.2.0 (2026-04-23)

### Feat

- **Codex CLI support**: plugin now runs on both Claude Code and Codex CLI. Adds `AGENTS.md` (portable per-agent instructions Codex auto-discovers), `.codex/INSTALL.md` (install + `multi_agent = true` feature flag), and `skills/using-development-skills/` with `references/codex-tools.md` mapping Claude Code tools to Codex equivalents (`spawn_agent`, `wait`, `close_agent`, `update_plan`).
- add `ai-agent-bench` skill: guided comparative benchmarking across AI agents (Claude Code, Codex, OpenCode) on refactoring/perf/code-change tasks in the current repo. Includes `run_trial.py` / `parse_transcript.py` scripts and full methodology references (gate/measure examples, sufficiency checks, prompt hygiene, aggregation, monitoring, anomaly log, report template).
- add `claude-to-codex` skill: convert existing projects so both Claude Code and Codex CLI read the same canonical agent context (`CLAUDE.md` → `@AGENTS.md`, slim `AGENTS.md`, `.agents/rules/` with `.claude/rules` symlink, gitignored per-agent personal-instruction slots).
- add `using-development-skills` skill: bootstrap context for every conversation — explains how to invoke components on Claude Code vs Codex, serves as SessionStart-hook substitute on Codex.
- convert feedback commands to user-invocable skills (`disable-model-invocation: true`): `context-transfer`, `produce-feedback`, `ingest-feedback`. Drops the separate `commands/` directory.

### Fix

- brainstorming: document Codex subagent dispatch path (`spawn_agent` with `multi_agent = true` feature flag) alongside native Claude Code `Task` tool usage.
- roast-my-code: document Codex staff-reviewer dispatch path mirroring the brainstorming change.

## 0.1.1 (2026-04-15)

### Feat

- add 10 best-practices evals covering non-tech domains (fitness, nutrition, finance, design, ergonomics, cooking) to verify skill universalization
- frontend-dev React patterns: add "Watch the state surface area", "Keep the return statement clean", "Avoid unnecessary useEffect" sections
- frontend-dev TypeScript patterns: add Trust Boundary Validation section (API responses, JSON.parse, URL params, persist rehydration)

### Fix

- research file naming now includes descriptive slug: `NNNN__research__{slug}.md` (propagated across phase-1-research, phase-2-plan, brainstorming analysis-agent, plan-template, resolve-merge)

## 0.0.18 (2026-03-31)

### Feat

- add roast-my-code skill (code quality critique + AI-readiness audit)
- add create-test evals (6 evals, 24 assertions covering routing, explorer, DB integration, Playwright, Hypothesis, characterization)
- add e2e-browser-patterns.md reference (Playwright POM, locator priority, visual regression, CI/CD)
- add integration-patterns.md reference (testcontainers, transaction rollback, factory fixtures, migration testing)
- add progress update messages to best-practices skill
- enhance language-templates.md with Hypothesis composites, settings profiles, Pact contract testing, mutation testing setup

### Fix

- remove duplication in create-test SKILL.md (replaced inline blocks with single-line references)
- remove redundant double-read of testing-strategies.md
- add flaky test prevention and migration testing sections to testing-strategies
- add pytest-xdist worker isolation, pytest-factoryboy, IntegreSQL patterns to integration-patterns
- replace hardcoded model:opus with effort:high frontmatter
- standardize reference path phrasing across create-test skill

## 0.0.17 (2026-03-30)

### Feat

- add python performance patterns and evals
- add best practices skill

### Fix

- improvements to best practices and dev skill workflow
- improvements to distill + evals
- adjust readme
- improve distill
- update readme
- improve readme
- improve readme

## 0.0.11 (2026-03-25)

### Fix

- improvements

## 0.0.10 (2026-03-25)

### Feat

- add create-test and eval-regression skills, distill improvements
- add distill skill
- initial release of development-skills

### Fix

- minor improvements
- improve readme
- improve readme
- adjust worktree workflows
- integrate create test
- improvements
- improvements
- improvements
- minor fixes
- improvements
- minor fixes
