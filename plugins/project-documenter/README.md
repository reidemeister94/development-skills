# Project Documenter

Generates exhaustive markdown documentation from codebases for Claude Code. The output serves as the written form of the code: reading the documentation is equivalent to reading the code, in natural language.

## Quick Start

```
/project-documenter
```

## Core Principle: Truth Before Completeness

**Never invents information.** Every fact must be traceable to a specific `file:line` in the source code. Uncertain items are marked as `[UNVERIFIED]` and the user is asked for clarification before proceeding.

## What It Does

1. **Discovery** -- Explores the codebase in parallel, categorized by source role (backend, frontend, database, config, etc.)
2. **Validation** -- Identifies uncertain items and asks the user for clarification
3. **Planning** -- Creates an execution plan with the documentation file structure
4. **Execution** -- Spawns sub-agents for parallel documentation generation
5. **Synthesis** -- Creates overviews, cross-references, and navigation

## Supported Source Roles

`backend-api`, `backend-batch`, `frontend`, `database-ddl`, `database-queries`, `docs-technical`, `docs-user`, `shared`, `config`, `tests`, `api-specs`, `algorithms`, `legacy-integration`, and more.

## Special Handling

- **Legacy systems** (AS400, SAP, Oracle Forms) -- Never guesses cryptic names; requires actual DDL/DDS files
- **Entity relationships** -- Documents with Mermaid ER diagrams
- **API endpoints** -- Structured documentation with request/response schemas
- **ETL workflows** -- Step-by-step pipeline decomposition

## Prerequisites

- A codebase to document
- Source files accessible to Claude Code (local or via MCP)
