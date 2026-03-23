# Discovery Agent Prompts by Role

Use the prompt matching the source role when spawning Explore agents in Phase 1.
Replace `{path}` with the absolute path of the source directory.

---

## `backend-api`

```
Perform EXHAUSTIVE analysis of REST/GraphQL API code in {path}. For EVERY endpoint, document:

1. IDENTIFICATION: method, path, handler function, file:line, route registration location

2. REQUEST HANDLING:
   - Middleware chain, authentication (what's checked, what fails), authorization, validation rules and error messages, parameter parsing

3. BUSINESS LOGIC (read code line by line):
   - Every conditional branch, every DB query, every external service call, every calculation/transformation, all side effects

4. RESPONSE CONSTRUCTION: what's included/excluded and why, error formats per error type

5. EDGE CASES & ERROR HANDLING: what can go wrong, how each is handled, what the client sees

Goal: documentation detailed enough that a developer could rewrite the endpoint from scratch.
```

---

## `backend-batch`

```
Perform EXHAUSTIVE analysis of batch/ETL scripts in {path}. Document the COMPLETE processing logic:

1. ORCHESTRATION: entry point, step sequencing, trigger mechanism, state maintenance between runs

2. FOR EACH PROCESSING STEP:
   a) PURPOSE: what business problem does this step solve?
   b) INPUTS: exact sources (table names, file paths, API endpoints), query/read logic
   c) PROCESSING LOGIC: explain each significant line — loops, conditions, transformations, validations, business rules
   d) OUTPUTS: destination, write mode (insert/upsert/truncate+insert), output schema
   e) ERROR HANDLING: what can fail, retry logic, alerting
   f) PERFORMANCE: batch sizes, memory considerations, optimizations and rationale

3. DATA FLOW: how data moves through the pipeline, intermediate states, what's persisted vs discarded

4. DEPENDENCIES: what must run before/after, shared resources

Goal: documentation allowing someone to reimplement the ETL in a different technology.
```

---

## `frontend`

```
Perform EXHAUSTIVE analysis of frontend code in {path}. Document the COMPLETE application logic:

1. APPLICATION STRUCTURE: routing (every route, component, guards), layout hierarchy, entry point/bootstrap

2. STATE MANAGEMENT: all stores/contexts/atoms, shape of each, initialization, every action/mutation, derived state

3. FOR EACH SIGNIFICANT COMPONENT: purpose, every prop (type, required, default), internal state, side effects, event handlers

4. DATA FETCHING: every API call (endpoint, trigger, response handling), caching, loading/error states, optimistic updates

5. FORMS: every form — fields, validation rules, submission logic, error display, success behaviour

6. BUSINESS LOGIC IN UI: calculations in frontend, display logic, permission/visibility rules

Goal: documentation allowing someone to rebuild the UI with complete fidelity.
```

---

## `database-ddl`

```
Perform EXHAUSTIVE analysis of database schemas in {path}. Document the COMPLETE data model.

⚠️ CRITICAL TRUTH REQUIREMENT:
- Document EXACT names as found in DDL — do NOT translate (CUSMST stays CUSMST, not 'Customer Master')
- Mark all inferred business meanings explicitly as "(inferred)"
- If a DDL definition is missing, mark the entity as [UNVERIFIED]

FOR EACH TABLE/ENTITY:
a) IDENTIFICATION: exact table name, schema, file:line
b) PURPOSE: business meaning (mark inferred vs documented), when records are created/updated/deleted
c) COLUMNS (every one, EXACT NAMES): name, type, nullable, default, business meaning, valid values, how value is set, constraints. For JSON: document the expected structure. For enum-like: list ALL valid values.
d) KEYS AND INDEXES: primary key (natural or surrogate), foreign keys with cascade behaviour, unique constraints, indexes and what queries they serve
e) RELATIONSHIPS: type (1:1, 1:N, N:M), meaning, orphan behaviour

DATA LIFECYCLE: how data enters, moves, and is archived/deleted

UNCERTAIN ITEMS (MANDATORY): tables/fields referenced in code but not in DDL, inferred meanings, implicit relationships

Goal: documentation allowing someone to recreate the exact schema with full understanding.
```

---

## `database-queries`

```
Perform EXHAUSTIVE analysis of SQL query templates in {path}. Document EVERY query:

1. QUERY INVENTORY: every file/template, naming conventions, organisation by domain/function

2. FOR EACH QUERY:
   a) PURPOSE: what business question does this answer?
   b) LOGIC: plain-language explanation of tables read, join conditions and why, filters and why, aggregations, CTEs, ordering rationale
   c) PARAMETERS: every placeholder — type, valid values, NULL behaviour
   d) PERFORMANCE: expected result size, indexes used, known slow cases
   e) USAGE: where called in codebase, what caller does with results

Goal: documentation allowing someone to understand and recreate every query.
```

---

## `shared`

```
Perform EXHAUSTIVE analysis of shared code in {path}. For EVERY shared element:

TYPES/INTERFACES: every field, optionality, valid values, why shared, relationships to other types

UTILITY FUNCTIONS: purpose, every parameter (type, valid values), step-by-step logic, return value, edge cases, where used in codebase

CONSTANTS: value, meaning, why constant, where used

Goal: documentation allowing someone to understand and recreate all shared code.
```

---

## `config`

```
Perform EXHAUSTIVE analysis of configuration in {path}:

ENVIRONMENT VARIABLES: every variable — name, purpose, type, valid values, examples, default, what breaks if missing/wrong

SERVICE DEPENDENCIES: every external service — what, why, connection details, impact if unavailable

CONFIGURATION FILES: every setting — meaning, valid values, impact, how config is loaded and merged

Goal: documentation allowing complete environment setup from scratch.
```

---

## `config-variants`

```
Perform EXHAUSTIVE analysis of variant configurations in {path}:

VARIANT DIMENSION: what varies (plants, tenants, environments), why variants exist, how variant is selected at runtime

FOR EACH VARIANT: name/identifier, every parameter that differs from base/default, business meaning of differences

VARIANT MATRIX: table showing all parameters and their values per variant — which truly differ, which are identical

Goal: documentation allowing someone to understand and recreate the variant system.
```

---

## `tests`

```
Analyze test files in {path}. For each test:
- What behaviour is being tested (specific, concrete)
- Setup: fixtures, mocks, test data
- Assertions: what's verified
- Edge cases covered
- What is NOT tested (gaps)

Goal: test documentation that reveals the full expected system behaviour.
```

---

## `api-specs`

```
Analyze API specifications in {path}. For EVERY endpoint:
- Method, path, purpose
- Every request parameter: type, required, validation
- Every response field: type, when present
- Every error: code, when it occurs
- Authentication/authorization requirements

Goal: complete API contract documentation.
```

---

## `algorithms`

```
Perform EXHAUSTIVE analysis of algorithm/optimization code in {path}:

1. PROBLEM DEFINITION: business problem, why an algorithm is needed, mathematical formulation if applicable

2. ALGORITHM LOGIC: step-by-step explanation, data structures and why, complexity, optimisation techniques

3. INPUTS: every input — format, constraints, validation, sample inputs

4. OUTPUTS: format, how to interpret results

5. CONFIGURATION: tuning parameters, impact of each

6. EDGE CASES: known limitations, problematic inputs, failure handling

Goal: documentation allowing algorithm reimplementation.
```

---

## `legacy-integration`

```
Perform EXHAUSTIVE analysis of legacy system integration in {path}.

⚠️ CRITICAL TRUTH REQUIREMENT:
- NEVER invent or guess legacy system names (tables, fields, programs)
- AS400/SAP/mainframe naming is cryptic and CANNOT be guessed — ORDHDP stays ORDHDP
- If you see integration code but NOT the legacy DDL, mark legacy details as [UNVERIFIED]

1. LEGACY SYSTEM: type (AS400, SAP, etc.), version if known, what it provides, why integration exists

2. DATA FLOW: direction (read/write/bidirectional), what flows each direction, triggers

3. TECHNICAL DETAILS: connection method (API, file, DB link, RPC), auth, protocols, formats

4. TRANSFORMATION (BE EXACT):
   - Field mappings using EXACT names from BOTH systems
   - If legacy field name unknown → [UNVERIFIED]
   - Type conversions

5. ERROR HANDLING: what can fail, retry logic, manual intervention needed

6. CONSTRAINTS: rate limits, timing windows, known issues

7. UNCERTAIN ITEMS (MANDATORY): list ALL legacy details not verified from source — what you know, what you need, where you saw the reference

Goal: documentation allowing someone to maintain/recreate the integration.
```

---

## `docs-technical`

```
Analyze technical documentation in {path}. Extract:
- Document structure and hierarchy
- Code references (file:line, function names)
- API documentation
- Architecture diagrams
- Technical terminology and definitions

Return a summary with cross-references to code elements.
```

---

## `docs-user`

```
Analyze user-facing documentation in {path}. Extract:
- Document structure (folders, navigation)
- Format and framework (MD, MDX, RST / Nextra, Docusaurus, etc.)
- Language and terminology (note if non-English)
- Screenshot/image inventory by section
- Workflow descriptions (user journeys)
- Business terminology and glossary

No code references expected.
Return a terminology glossary and workflow summary.
```

---

## `docs-confluence`

```
Analyze Confluence pages in space {space_key}. Use MCP tools to:
- List all pages in the space hierarchy
- Read page content
- Extract diagrams (draw.io, Gliffy, Lucidchart embeds) and tables
- Identify business rules and domain definitions
- Note page authors and last update dates
- Map page structure to documentation sections

Return structured content with page URLs for reference.
```

Note: ensure Atlassian MCP is configured before spawning this agent:
```bash
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
```

---

## `custom`

```
Analyze {path} as described: {user_description}.
Perform EXHAUSTIVE analysis — understand the code deeply, explain logic step by step,
document all edge cases, note all dependencies.

Goal: documentation allowing complete understanding and reconstruction.
```
