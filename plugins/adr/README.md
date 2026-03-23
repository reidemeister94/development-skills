# ADR Plugin

Architecture Decision Records (ADRs) are short documents that capture architectural decisions: what was decided, why, and what alternatives were rejected. They are the institutional memory of a project.

## Why ADRs?

Without ADRs, architectural decisions live only in people's heads or buried in old Slack threads. Six months later, nobody knows:
- Why did we choose PostgreSQL over MongoDB?
- Why is the API versioned in the URL path and not via headers?
- Why did we not use GraphQL?

ADRs answer these questions permanently, for every team member — including future ones.

---

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `adr` | `/adr` | Document a new architectural decision interactively |
| `adr-list` | `/adr-list` | Browse all ADRs with status and summary |
| `adr-update` | `/adr-update` | Change a decision's status (accept, deprecate, supersede) |

---

## Usage

### Create a new ADR

```
/adr Use PostgreSQL as the primary database
```

Claude will ask follow-up questions about context, alternatives considered, and consequences — then generate the ADR for your review before saving.

You can also just say:

```
/adr
```

And Claude will ask you what decision to document.

### List all ADRs

```
/adr-list
```

Shows a table of all ADRs with number, status, date, and title.

```
/adr-list authentication
```

Filters to ADRs related to authentication.

### Update an ADR

```
/adr-update 0003
```

Change the status of ADR-0003 (Proposed → Accepted, or mark as Deprecated/Superseded).

---

## ADR Format

ADRs are saved to `docs/decisions/` in your project, with this filename pattern:

```
docs/decisions/ADR-0001-use-postgresql-as-primary-database.md
```

Each ADR contains:
- **Context** — What problem or situation triggered this decision
- **Decision** — What was decided, stated definitively
- **Alternatives Considered** — What else was evaluated and why it was rejected
- **Consequences** — What becomes easier and what becomes harder

---

## Multi-Project Usage

The ADR plugin works in any project. Each project has its own `docs/decisions/` folder with independent numbering. Simply install the plugin once and use `/adr` in any project directory.

---

## Decision Categories Supported

The plugin knows the right questions to ask for different decision types:
- API design (REST vs GraphQL, versioning, auth, error formats)
- Database & storage (engine choice, ORM, caching)
- Authentication & authorization (JWT, sessions, RBAC, SSO)
- Service architecture (monolith vs microservices, messaging)
- Language & framework choices
- Data and event flow (message brokers, event sourcing)
- Security (secret management, encryption, compliance)

---

## Convention

- **One decision per ADR.** Don't bundle multiple decisions into one file.
- **ADRs are immutable.** Don't edit the content of an accepted ADR — instead create a new ADR that supersedes it.
- **Supersede, don't delete.** Old ADRs stay in the record. Mark them superseded.
- **Be honest about trade-offs.** An ADR with only positives is not an honest ADR.
