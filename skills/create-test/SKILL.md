---
name: create-test
description: "Design and generate tests: boundary, property, invariant, integration, E2E, characterization, concurrency, contract, visual regression, mutation. Analyzes coverage gaps, audits weak assertions, creates golden fixtures. Trigger: /create-test"
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Agent, Edit, Write
effort: high
---

# Create Test — Intelligent Test Design

<!-- ultrathink: triggers extended reasoning mode -->

**Announce:** "Using the create-test skill. Analyzing code to design tests that find bugs, not just exist."

Read `references/testing-strategies.md` now. Keep its principles active throughout.

## Argument Parsing

- **No arguments** (`$ARGUMENTS` is blank): Explorer mode
- **Arguments present**: Targeted mode — treat `$ARGUMENTS` as file path, module path, or directory

---

## MODE A: Explorer (no arguments)

Spawn an analysis subagent (Agent tool) with this prompt:

```
You are a test coverage analyst. Your job: find the most dangerous untested code in this project.

## Instructions

1. **Detect project type and test infrastructure:**
   - Glob for: pyproject.toml, pom.xml, build.gradle, package.json, Package.swift
   - Read the config to understand: language, framework, test runner, existing test locations
   - Detect DB layer: grep for asyncpg, SQLAlchemy, psycopg, prisma, database URLs, connection pools
   - Detect browser testing: glob for playwright.config.*, cypress.config.*, *.spec.ts, *.e2e.ts
   - Detect containers: glob for docker-compose*.yml, Dockerfile*, testcontainers usage
   - Detect legacy indicators: source files with 0 test coverage, functions >100 lines, no test directory

2. **Map what EXISTS:**
   - Glob for test files: `tests/**`, `test/**`, `src/test/**`, `__tests__/**`, `*Test.*`, `*_test.*`, `*.test.*`, `*.spec.*`
   - For each test file, count: test functions, assertion density (assertions per test), use of randomization
   - Identify: markers/tags, conftest/fixtures, test infrastructure

3. **Map what is UNTESTED:**
   - Glob for source files in: `src/`, `app/`, `lib/`, `api/`, main directories
   - For each source file, identify: public functions/methods, API endpoints, data transformations, state machines
   - Cross-reference: which source functions have NO corresponding test
   - Pay special attention to: error handlers, boundary conditions in if/switch, functions with numeric thresholds

4. **Risk-prioritize untested code:**

   Score each untested area (1-5 per dimension, sum them):

   | Dimension | 1 (low) | 3 (medium) | 5 (high) |
   |-----------|---------|------------|----------|
   | **Blast radius** | Internal helper | Service layer | Public API / data pipeline |
   | **Complexity** | Pure function, no branches | Multiple branches, state | Recursive, concurrent, external deps |
   | **Change frequency** | Untouched 6+ months (`git log --since="6 months ago" -- <file> \| wc -l` = 0) | Monthly changes | Weekly or more |
   | **Data sensitivity** | Display/formatting | Business logic | Financial, auth, data integrity |

   Risk = sum of scores. Rank from highest to lowest.

5. **Audit existing test quality:**
   Read `references/weak-assertion-patterns.md`.
   Use Grep with the regex patterns from that file to scan existing test files for weak assertions.
   Report files with assertion density < 2 or weak assertion ratio > 0.3.

6. **Output format:**

```markdown
# Test Coverage Analysis

## Project: [name] | Language: [X] | Test Runner: [X]
## Existing Tests: [N files, M test functions, avg assertion density: X]

## PRIORITY 1 — Critical Untested Code (risk >= 15)
| # | File:Function | Risk | Why | Recommended Strategy |
|---|--------------|------|-----|---------------------|

## PRIORITY 2 — Important Untested Code (risk 10-14)
| # | File:Function | Risk | Why | Recommended Strategy |

## PRIORITY 3 — Nice to Have (risk < 10)
[brief list]

## Existing Tests — Quality Issues
| File | Issue | Severity |
|------|-------|----------|

## Recommended Test Infrastructure
[conftest patterns, fixtures, markers — only if missing]

## Testing Layers Assessment
| Layer | Status | Gap |
|-------|--------|-----|
| Unit (boundary, property, invariant) | [present/absent] | [what's missing] |
| Integration (real DB, services) | [present/absent] | [what's missing] |
| E2E (browser/API lifecycle) | [present/absent] | [what's missing] |
| Characterization (golden master) | [present/absent] | [needed for refactoring?] |
| Contract (service boundaries) | [present/absent] | [multi-service?] |
| Visual regression | [present/absent] | [UI project?] |
```

Write this analysis to `test-analysis.md` in the project root.
```

After the subagent returns, display the analysis summary to the user:

> **Test Coverage Analysis Complete** — see `docs/test-analysis.md`
>
> [Show PRIORITY 1 table + quality issues table]
>
> Which items should I generate tests for? (numbers, "all priority 1", or "skip")

**On user selection:** For each selected item, run Targeted Mode (Mode B) with the file:function as argument.

---

## MODE B: Targeted (with arguments)

### Step 1: Read and Understand

1. Read the target file completely
2. If a directory, read all source files in it
3. Identify the project language and test framework (from project config files)
4. Read `references/language-templates.md` for the target language

### Step 2: Implementation Analysis

For each public function/method/endpoint in the target:

**Boundary detection:**
- Find numeric comparisons (`<`, `>`, `<=`, `>=`, `==`) — extract threshold values
- Find string length checks, array size limits, enum switches
- Find type coercion points (int/float, string encoding, null handling)
- For each boundary: note the N-1, N, N+1 test values (the "255, 256, 257" pattern)

**State space mapping:**
- Identify state transitions (if/else chains, switch/match, state machines)
- Find the fragile states: error paths, fallback branches, retry logic, timeout handling
- Identify which states are NOT reachable from current tests

**Invariant detection:**
- Functions that transform data: what properties must hold? (round-trip, idempotence, monotonicity, ordering preservation)
- Functions that compute: can a simpler reference implementation verify the result?
- Functions that aggregate: do totals match? Are constraints preserved?

**API surface analysis** (if target is an endpoint/controller):
- Request/response schemas
- Status code branches
- CRUD lifecycle completeness
- Error response formats

### Step 3: Strategy Selection

Refer to `references/testing-strategies.md` to select strategies. Apply this matrix:

| Code characteristic | Primary strategy | Secondary | Reference |
|-------------------|-----------------|-----------|-----------|
| Numeric thresholds | Boundary stress | Property-based | testing-strategies.md §1 |
| Data transformation | Property-based (round-trip, invariant) | Boundary | testing-strategies.md §2 |
| Parser / serializer | Fuzz + property-based | Boundary | testing-strategies.md §2 |
| API endpoint (read) | Golden fixture regression | Boundary | testing-strategies.md §4 |
| API endpoint (write) | CRUD lifecycle | Golden fixture | testing-strategies.md §5 |
| State machine | State transition coverage | Boundary | testing-strategies.md §1 |
| Algorithm / computation | Invariant (reference impl) | Property-based | testing-strategies.md §3 |
| Pure function, few params | Boundary exhaustive | — | testing-strategies.md §1 |
| DB queries / repositories | Real DB integration | Factory fixtures | integration-patterns.md |
| Browser UI / user flows | Playwright E2E | Visual regression | e2e-browser-patterns.md |
| Legacy code, pre-refactoring | Characterization (golden master) | Approval test | testing-strategies.md §9 |
| Concurrent / async operations | Concurrency stress | Property-based | testing-strategies.md §10 |
| Microservice boundary | Contract test (Pact) | CRUD lifecycle | testing-strategies.md §11 |
| DB migrations (Alembic, etc.) | Up/down verification | Rollback test | integration-patterns.md |
| **Migration legacy→new** | Live comparison | Characterization | testing-strategies.md §6 |

### Step 4: Generate Tests

Generate the test file. For each test function:

1. **Descriptive name** — describes the behavior being tested, not the method name
2. **AAA structure** — Arrange, Act, Assert (clearly separated)
3. **Strong assertions** — assert specific values, not just "not null". Check `references/weak-assertion-patterns.md`.
4. **Boundary tests** — at every identified threshold: N-1, N, N+1
5. **Property-based tests** — for data transformations, use the language's property library (hypothesis, jqwik, fast-check)
6. **Random stress tests** — for complex logic: generate random inputs, verify invariants over many iterations
7. **Error path tests** — invalid inputs, null/empty, type mismatches

For golden fixture / e2e patterns, generate BOTH:
- The capture script (to be run once against live system)
- The regression test (replays from captured fixtures)

**For DB integration tests:** Apply patterns from `references/integration-patterns.md` (isolation strategies, factory fixtures, synthetic data).

**For Playwright E2E tests:** Apply patterns from `references/e2e-browser-patterns.md` (POM, locator priority, web-first assertions, visual regression).

**For characterization tests:** Apply patterns from `references/testing-strategies.md` §9 (capture baseline, Printer/normalizer, capture script + regression test).

**For concurrency tests:** Apply patterns from `references/testing-strategies.md` §10 and `references/language-templates.md` concurrency scaffolds.

**For contract tests:** Apply patterns from `references/language-templates.md` Pact scaffolds.

### Step 5: Run and Verify

1. Run the generated tests: use the project's test command
2. Read the output completely
3. If tests fail: fix the test (not the source code), re-run
4. After tests pass, verify each test can actually fail: if the production code had a bug at this boundary, would this assertion catch it? If unsure, temporarily invert an assertion to confirm it fails.

### Step 6: Quality Report

```
## Test Generation Report: [target]

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Tests generated | N | — | — |
| Assertion density | X/test | >= 2 | OK/WARN |
| Boundary tests | N | >= 1 per threshold | OK/WARN |
| Property-based tests | N | >= 1 per transform | OK/WARN |
| Weak assertions | N | 0 | OK/WARN |
| Random/fuzz tests | N | >= 1 for complex logic | OK/WARN |
| Integration tests (real DB) | N | >= 1 per repository/query | OK/WARN/N/A |
| E2E browser tests | N | >= 1 per critical flow | OK/WARN/N/A |
| Characterization tests | N | >= 1 per legacy module | OK/WARN/N/A |
| Concurrency tests | N | >= 1 per shared resource | OK/WARN/N/A |

### Strategies Applied
- Boundary stress: [list of thresholds tested]
- Property-based: [list of properties verified]
- Invariant: [list of invariants checked]
- Golden fixture: [if applicable]
- CRUD lifecycle: [if applicable]
- DB integration: [if applicable — isolation strategy used]
- E2E browser: [if applicable — flows covered]
- Characterization: [if applicable — modules locked]
- Contract: [if applicable — consumer/provider pairs]

### NOT Tested (and why)
[Functions/paths deliberately excluded with justification]
```

---

## Rules

- **Tests must find bugs, not just exist.** Every test must target a specific failure mode.
- **Test through the public API.** Do not test private/internal functions directly. Test them through their public callers.
- **Strong assertions only.** Never generate `assertNotNull(x)` as the sole assertion. Assert specific values, shapes, and invariants.
- **Random data over fixed data.** Prefer property-based tests with random generation over hardcoded test cases. Fixed cases only for specific boundary values.
- **Fast by default.** Property tests: 100 examples default. Fuzz tests: 1000 iterations. Parametrize, don't duplicate.
- **Run every test you write.** Never present tests as done without executing them and reading the output.
- **Never modify source code.** Only create/modify test files, conftest, and fixtures.
- **Match project conventions.** Use the project's existing test directory, naming, markers, and fixture patterns.
