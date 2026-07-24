# Review Severity

Use this scale for every review surface:

- **CRITICAL** — merging causes an immediate production incident, reachable security breach, data loss, corruption, or broken build.
- **HIGH** — a serious reachable defect: broken core behavior, request or job crash, unversioned breaking contract, leak, concurrency bug, or security weakness.
- **MEDIUM** — no immediate outage, but reliability, performance, or maintainability is materially worse: missing boundary handling, N+1 query, test gap, poor abstraction, or duplicated logic.
- **LOW** — readability or codified style only.

CRITICAL, HIGH and MEDIUM must be fixed before merge and are the only default auto-fix or inline-PR tiers. LOW can be done but it's a nice to have and should be agreed with the user if fix them or not.

For posted review comments use `> **[TIER]** description`, add `> **Why:** impact` for CRITICAL/HIGH, and `> **Suggestion:** fix` except for LOW.
