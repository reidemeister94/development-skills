# `gate_cmd` recipes

The `gate_cmd` is the single most important field in the task config. It decides whether the
agent's work is "safe to consider" or "broken". Exit code 0 = pass. Anything else = fail.

**The harness runs the gate twice**:
1. **Preflight**: on HEAD (before the worktree is created). Must pass. If it fails, the trial
   aborts: an invalid gate cannot be a valid baseline.
2. **Post-trial**: in the worktree after the agent finishes. Result is recorded in
   `gate_exit_code.txt` and surfaced in the report. A failed post-gate does NOT abort the trial
   — the artifacts stay for audit — but marks the trial as unsuccessful.

---

## Choosing the right gate — principles

- **Broad enough to catch what matters**: the gate should fail if the agent breaks the feature
  you care about. A gate that only runs 3 unit tests won't catch an integration regression.
- **Narrow enough to be reliable**: flaky tests poison the gate. If you know a test is flaky, it's
  better to temporarily exclude it (and flag to the reviewer) than to leave it and get noise.
- **Fast enough for the feedback loop**: a 2-hour gate is worse than a 10-minute one — you want to
  be able to iterate. 5–30 minutes is the sweet spot.
- **Deterministic**: random seeds pinned, time-dependent logic mocked.

---

## Common recipes

### Python

```toml
gate_cmd = "pytest -q"
gate_cmd = "pytest -m 'not e2e' -q"
gate_cmd = "pytest tests/unit tests/integration -q && pytest -m e2e tests/e2e -q"
gate_cmd = "pre-commit run --all-files && pytest -q"
gate_cmd = "ruff check . && mypy . && pytest -q"
```

### Node.js / TypeScript

```toml
gate_cmd = "npm test"
gate_cmd = "npm run test:ci"
gate_cmd = "npm run typecheck && npm run lint && npm test"
gate_cmd = "pnpm -r test"
gate_cmd = "yarn test --ci"
```

### Go

```toml
gate_cmd = "go test ./..."
gate_cmd = "go test -race ./..."
gate_cmd = "go vet ./... && go test -race ./..."
```

### Java / Gradle

```toml
gate_cmd = "./gradlew test"
gate_cmd = "./gradlew check"
```

### Rust

```toml
gate_cmd = "cargo test --all"
gate_cmd = "cargo clippy -- -D warnings && cargo test --all"
```

### Project-specific orchestration

Some projects wrap their gate behind a bespoke script that composes multiple suites (unit +
integration + e2e + parity checks, or similar). The skill cannot know this from the filesystem
alone — during Phase A recon it must read the project's `CLAUDE.md` / `AGENTS.md` / `README` /
CI config (`.github/workflows/`, `.bitbucket-pipelines.yml`, `.gitlab-ci.yml`, etc.) and ask the
developer directly: *is there a canonical "run everything we consider a blocker for merge"
command already defined?*

If yes, use it. If it accepts a flag to preserve logs for downstream analysis, pass `{run_dir}`
so the harness can reference those artifacts:

```toml
gate_cmd = "./scripts/check.sh --fast --preserve-logs {run_dir}/gate_artifacts"
```

If no bespoke orchestrator exists, compose the gate explicitly from the primitives the project
does have (see the recipes above). Do not invent a `scripts/` path — verify it exists first.

### Doc-only tasks

```toml
gate_cmd = "markdownlint '**/*.md' && mkdocs build --strict"
```

### Type-check only (refactor-safe tasks)

```toml
gate_cmd = "mypy --strict src/"
gate_cmd = "tsc --noEmit"
```

---

## Layered gates (fast + slow)

If your primary test suite is slow, you can do a two-phase gate — but remember it's a single
shell command, so chain with `&&`:

```toml
gate_cmd = """\
set -e; \
npm run typecheck && npm run lint && \
npm run test:unit && \
npm run test:integration \
"""
```

The harness only sees the final exit code. If one step fails, the chain stops; the `gate.log`
will show which step died.

---

## Gate is MANDATORY

A trial without a gate is unscientific. The skill will insist on a gate; to override, the
developer must provide a written justification (stored in the report as "NO GATE — <justification>").

Default answers if the wizard can't find obvious test infrastructure:

- Python project with `pyproject.toml` mentioning pytest → suggest `pytest -q`
- `package.json` with `test` script → suggest `npm test`
- `go.mod` → suggest `go test ./...`
- `Makefile` with a `test` target → suggest `make test`
- Nothing obvious → ask the developer; suggest `pre-commit run --all-files` as a last resort
