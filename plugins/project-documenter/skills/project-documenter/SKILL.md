---
name: project-documenter
description: |
  Generate project documentation from code, DDLs, and scripts. Use when asked to "document this project",
  "create documentation from these DDLs", "explain the codebase structure", "generate an ER diagram",
  "document this ETL pipeline", "create a context file for LLMs", or "explain how this system works".
  Handles DDL analysis, ETL scripts, API endpoints, entity relationships, and workflow decomposition.
  Never invents information — asks clarifying questions when uncertain, especially for legacy systems (AS400, SAP).
metadata:
  author: salvob41
  version: 1.0.1
  category: documentation
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - Agent
---

# Project Documenter

Generate documentation that serves as the **written form of the code**: reading the docs must be equivalent to reading the code, in natural language.

## IRON RULE: Truth Before Completeness

**Never write something you haven't read in the source.** Every fact must be traceable to a `file:line` reference. If uncertain → mark as `[UNVERIFIED]` and ask the user. This applies doubly to legacy systems (AS400, SAP, Oracle Forms) where cryptic names cannot be inferred.

---

## Step 1: Ask for Project Structure

```
I need to know your project structure. List ALL relevant source directories:

| # | Path | Role | Description |
|---|------|------|-------------|
| 1 | _____ | _____ | _____ |

Output location (where to write docs): _____
```

### Supported Roles

| Role | What it contains |
|------|-----------------|
| `backend-api` | REST/GraphQL API server code |
| `backend-batch` | ETL scripts, batch jobs, scheduled tasks |
| `frontend` | React, Vue, or other UI frameworks |
| `database-ddl` | DDLs, migrations, schemas |
| `database-queries` | SQL query templates, stored procedures |
| `shared` | Shared libraries, utils, types |
| `config` | Infrastructure, deployment, env configs |
| `config-variants` | Multi-tenant/plant/env configurations |
| `tests` | Test files, fixtures |
| `api-specs` | OpenAPI/Swagger, GraphQL schemas |
| `algorithms` | Optimization, ML, complex business logic |
| `legacy-integration` | Integration with legacy systems (AS400, etc.) |
| `docs-technical` | Technical markdown/MDX docs |
| `docs-user` | User-facing guides |
| `docs-confluence` | Confluence pages (via MCP) |

Add modifiers for context: `backend-api (FastAPI)`, `database-queries (80+ SQL templates)`, etc.

---

## Step 2: Phase 1 — Discovery

Read `references/roles.md` to get the agent prompt for each source role.

For each source directory, spawn a **parallel Explore agent** using the matching prompt from `references/roles.md`. Pass the absolute path and role modifier as context.

Collect all agent outputs before proceeding.

---

## Step 3: Phase 2 — Validation Checkpoint

After discovery, synthesize a summary and surface all uncertain items:

```markdown
## Discovery Summary

### Source N: {path} (role: {role})
- Entities/endpoints/components found: …
- Key dependencies: …
- Uncertain items: …

## Cross-Source Analysis
- Element mappings (e.g. API entity → DB table): …
- Shared dependencies: …
- Gaps: …

## Uncertain Items [REQUIRES CLARIFICATION BEFORE PROCEEDING]
| Item | What we know | What we need | Source |
|------|--------------|--------------|--------|
```

**Stop here** if uncertain items exist. Present them to the user and wait for answers before writing any documentation.

---

## Step 4: Phase 3 — Planning

Propose the documentation file structure. Get user confirmation before writing anything.

Example structure:
```
docs/
  overview.md
  entities/
    user.md
    invoice.md
  api/
    post-invoices.md
    get-invoices-id.md
  workflows/
    billing-pipeline.md
  er-diagram.md
```

---

## Step 5: Phase 4 — Execution

Spawn **parallel implementer agents** — one per documentation file or logical group. Each agent:
1. Reads the relevant source files
2. Uses the appropriate template from `references/` (`api-template.md`, `entity-template.md`, `workflow-template.md`)
3. Includes Mermaid diagrams for flows and ER relationships (see `references/mermaid-patterns.md`)
4. Writes the documentation file

---

## Step 6: Phase 5 — Synthesis

Create:
- `docs/overview.md` — project summary, architecture diagram, navigation index
- Cross-references between files (link entities to API endpoints to workflows)
- Validate all `file:line` references are accurate

---

## Quality Rules

- **Truth first.** Every fact has a `file:line` source. No guessing.
- **Concrete over vague.** Exact table names, field names, SQL, config values — not "probably stores X".
- **Exhaustive on logic.** Document every branch, validation rule, edge case, and business rule.
- **Mermaid for flows.** Every pipeline, data flow, ER relationship, and sequence gets a diagram.
- **Omit empty sections.** Don't write placeholder content.
- **Legacy systems.** Never translate cryptic names. Document `CUSMST` as `CUSMST`, not "Customer Master".

## Examples

### Example 1: Document a codebase
User says: "Document this project so a new developer can understand it"
Actions: Explore structure → read key files → generate overview doc with architecture diagram
Result: Comprehensive documentation file covering structure, flows, and key components

### Example 2: Generate ER diagram from DDLs
User says: "Create an ER diagram from these SQL DDL files"
Actions: Read DDL files → identify entities and relationships → generate Mermaid ER diagram
Result: ER diagram with all tables and relationships documented
