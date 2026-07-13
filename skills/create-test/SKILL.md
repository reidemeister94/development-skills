---
name: create-test
description: "Define or implement regression proof for a project or business flow. Use for test strategy, black-box or deep-integration tests, business KPIs and thresholds, test audits, missing tests, or test implementation."
argument-hint: "[file-or-directory-or-goal]"
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Edit, Write, AskUserQuestion
---

# Create Test

Start with what must remain true for the user or business, not with files, coverage, or internal calls. Inspect the project for facts; ask only for business decisions that cannot be discovered.

## Define the regression contract

For the whole project or the requested flow, establish:

- actors, goals, and externally observable outcomes;
- business rules and invariants that must never change;
- critical paths plus rejection, timeout, retry, permission, concurrency, and partial-failure cases that matter;
- the current baseline and every intended behavior change;
- KPIs or operational signals, with measurement window, data set, acceptable variance, and a justified pass/fail threshold;
- systems crossed, production-like data needs, and evidence the available environment can actually provide.

Do not invent a metric or threshold to fill a blank. Record it as an open decision or blind spot.

## Choose the proof

Prefer the highest boundary that gives reliable feedback:

1. black-box tests through the public API, UI, job, event, or CLI;
2. deep integration with the real database, queue, connector, or protocol;
3. contract, replay, property, or characterization tests for narrower risks;
4. unit tests for isolated rules where a wider test adds no confidence.

Use mocks only beyond the boundary being verified. For database or migration work, read [integration patterns](references/integration-patterns.md).

When asked only for strategy or an audit, return a concise contract, prioritized scenario map, proof method, and remaining blind spots. Judge existing tests by the outcomes and failures they would catch, not assertion counts or line coverage.

## Implement when asked

Follow the project's test layout and development loop. Add the smallest test that proves the next important scenario, observe RED, make only approved source changes, then observe GREEN. Assert business outcomes, persisted state, emitted events, metrics, and error contracts rather than implementation calls. Run the focused test and the relevant suite; report what is now proven and what remains outside the evidence boundary.
