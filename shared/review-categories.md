# Code Review Severity Categories

Canonical severity scale for every code-review surface in this repo (`staff-reviewer`, `staff-review`, `roast-my-code`, `github-pr`, `bitbucket-pr`, FULL Phase 4). Classify every finding by it.

**Comment format (every surface):** `> **[TIER]** {description}` — add `> **Why:** {impact}` for CRITICAL/HIGH, and `> **Suggestion:** {fix}` for all tiers except LOW.

- **CRITICAL** — ships a production incident, security breach, or data loss the moment it merges (reachable exploit, committed secret, data corruption, breaks-on-merge).
- **HIGH** — a serious defect: logic error breaking core functionality, request/job-crashing exception, breaking API change without versioning, resource leak, concurrency bug, not-yet-exploitable security weakness.
- **MEDIUM** — degrades quality/performance/maintainability without immediate failure: missing error handling on external calls, N+1 / missing index, missing boundary validation, test gaps, poor abstraction, duplicated logic.
- **LOW** — style and readability: naming, inconsistency, over-complex expressions, missing docstrings on public APIs.

## Gating

- Must address before merge: CRITICAL + HIGH.
- Auto-fix tiers (`roast-my-code --fix` and default fix sets): CRITICAL + HIGH. MEDIUM + LOW are informational.
- PR inline-comment posting (`github-pr`, `bitbucket-pr`): CRITICAL + HIGH.
