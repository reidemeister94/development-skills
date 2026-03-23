---
name: java-dev
description: "Java development. Use for Java, Spring Boot, Maven, Gradle, JPA, Hibernate."
user-invocable: true
allowed-tools: Glob, Read, Grep, Bash, Task, Skill, Edit, Write, EnterPlanMode
---

# Java Development

**Announce:** "I'm using the java-dev skill. Following the mandatory 7-phase workflow."

## MANDATORY: Read and Follow the Shared Workflow

**You MUST read [workflow.md](../../shared/workflow.md) NOW** and follow ALL 7 phases defined there. The sections below provide Java-specific inputs for each phase.

Read [patterns.md](patterns.md) during Phase 1.

**If you lost workflow.md from context:** Re-read `../../shared/workflow.md` NOW before continuing.

---

## Java-Specific Configuration

### Verification Commands (Phase 2 + Phase 5)

WORKFLOW STATE Verification line: `mvn test / gradle test, mvn compile / gradle build`

**Phase 5 Tier A commands:**
- `mvn test` or `gradle test` — run tests
- `mvn compile` or `gradle build` — compilation check
- Check for compiler warnings

**Phase 5 Tier B additional MCP verifications:**
- PostgreSQL MCP → Query DB state before/after

### Implementation Rules (Phase 4)

- **Data carrier structure** — Records with CRUD variants per entity (CreateRequest/UpdateRequest/Response), domain-driven packages, composition over deep inheritance
- **Minimize complexity** — efficient streams, HashMap lookups over list scans
- **Preserve compatibility** — Overloaded methods for new params, @JsonProperty for renamed fields, @Deprecated before removal

### Staff Review Configuration (Phase 6)

- **Patterns file path:** Path to this skill's `patterns.md`

---

## Anti-Rationalization (Java-Specific)

Add these to the shared workflow's anti-rationalization check:

| Your thought | Reality |
|---|---|
| "Java's type system catches everything at compile time" | The compiler catches type errors, not logic bugs, concurrency issues, or SQL injection. Verification and review are still mandatory. |
| "Spring Boot auto-configuration handles this" | Auto-configuration can mask issues. Understand what it does before relying on it. |
| "This is just a CRUD endpoint, no need for full workflow" | CRUD endpoints still need proper validation, error handling, and tests. Follow the workflow. |

### Red Flags (Java-Specific)

- Expressing satisfaction before running `mvn test` or `gradle test`

---

## Quality Checklist (Java-Specific)

Add these to the shared workflow's verification checklist:

- [ ] Using Java 21+ features (var, records, switch expressions, pattern matching)
- [ ] Records used for immutable data carriers
- [ ] Constructor injection for all dependencies
- [ ] No raw types — generics used properly
- [ ] Build succeeds without warnings
- [ ] `mvn test` or `gradle test` passes
- [ ] No compiler warnings
