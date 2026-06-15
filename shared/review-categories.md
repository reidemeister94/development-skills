# Code Review Severity Categories

Canonical severity scale for every code-review surface in this repo (`staff-reviewer` agent in both modes, `staff-review`, `roast-my-code`, `github-pr`, `bitbucket-pr`, FULL Phase 4). Four tiers: **CRITICAL / HIGH / MEDIUM / LOW**.

**Comment format (every surface):** `> **[TIER]** {description}` — add `> **Why:** {impact}` for CRITICAL/HIGH, and `> **Suggestion:** {fix}` for all tiers except LOW.

## CRITICAL — Must Fix Before Merge (catastrophic)

Will cause a production incident, security breach, or data loss the moment it ships.

**What to look for:**
- Exploitable security holes with a reachable sink (RCE, auth/authz bypass, SQL/command injection, SSRF, stored XSS)
- Secrets committed to the repo (keys, tokens, passwords)
- Data loss or corruption (missing transaction boundaries, unsafe bulk deletes, races that drop writes)
- Changes that break production on merge (crash on startup, broken migration, removed-but-still-called API)

---

## HIGH — Should Fix Before Merge (serious)

A real defect or weakness that is serious but not immediately catastrophic.

**What to look for:**
- Logic errors that break core functionality
- Unhandled exceptions that crash a request/job (not the whole app)
- Breaking API contract changes without versioning
- Resource leaks (unclosed connections, file handles, memory)
- Concurrency bugs (deadlocks, lost updates)
- Security weaknesses that are not directly exploitable yet (weak defaults, missing authz on a low-traffic path)

---

## MEDIUM — Should Fix

Degrades quality, performance, or maintainability but won't cause immediate failures.

**What to look for:**
- Missing error handling for external calls (APIs, DB, filesystem)
- Performance issues (N+1 queries, unnecessary allocations, missing indexes)
- Missing input validation at system boundaries
- Test gaps for changed logic paths
- Poor abstraction (god functions, tight coupling)
- Duplicated logic that should be extracted
- Missing logging for error paths
- Incorrect or missing type annotations on public interfaces

---

## LOW — Consider Fixing

Style and readability improvements. Nice to have, not blocking.

**What to look for:**
- Naming (unclear variable/function names, inconsistent conventions)
- Code style inconsistencies with the rest of the codebase
- Overly complex expressions that could be simplified
- Missing or outdated comments/docstrings on public APIs
- Import ordering, unused imports
- Minor readability improvements

---

## Gating

- **Must address before merge:** CRITICAL + HIGH.
- **Auto-fix tiers** (`roast-my-code --fix`, and the default fix set elsewhere): CRITICAL + HIGH. MEDIUM + LOW are informational.
- **PR inline-comment posting** (`github-pr`, `bitbucket-pr`): CRITICAL + HIGH findings.
