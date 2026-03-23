# ADR Decision Categories — Context Guide

This reference helps Claude ask the right follow-up questions based on the type of architectural decision being documented.

---

## API Design

**Key questions to ask:**
- REST, GraphQL, gRPC, or event-driven? What drove that choice?
- How will the API be versioned? (path prefix `/v1/`, headers, query param)
- What authentication mechanism? (JWT, API key, OAuth2, session)
- Will this be a public API or internal only?
- How are errors communicated? (HTTP status codes + body shape)
- Pagination style? (cursor, offset, keyset)

**Common decisions in this category:**
- API protocol choice (REST vs GraphQL vs gRPC)
- Authentication strategy
- Versioning approach
- Error response format
- Pagination strategy
- Rate limiting policy

---

## Database & Storage

**Key questions to ask:**
- Relational or document store? Why?
- What are the access patterns — read-heavy, write-heavy, mixed?
- Is data consistency critical or is eventual consistency acceptable?
- Any specific query or scale requirements driving the choice?
- ORM or raw queries? Why?
- Migration strategy?

**Common decisions in this category:**
- Database engine choice (PostgreSQL, MySQL, MongoDB, DynamoDB...)
- Schema design approach (normalized vs denormalized)
- ORM vs query builder vs raw SQL
- Indexing strategy
- Caching layer (Redis, Memcached, in-memory)
- Backup and recovery approach

---

## Authentication & Authorization

**Key questions to ask:**
- Who are the users? Internal team, external customers, service-to-service?
- Session-based or token-based?
- Where is authorization enforced — API gateway, service, database row-level?
- What happens when tokens expire?
- Is SSO/SAML/OIDC involved?

**Common decisions in this category:**
- Auth mechanism (JWT, sessions, OAuth2, API keys)
- Token storage approach
- Role-based vs attribute-based access control
- SSO provider choice
- Multi-tenancy isolation model

---

## Architecture & Service Design

**Key questions to ask:**
- Monolith, modular monolith, or microservices? What's the team size and maturity?
- Synchronous or asynchronous communication between services?
- How will services discover each other?
- What's the deployment target (containers, serverless, VMs)?
- What happens when a service is down?

**Common decisions in this category:**
- Service decomposition (monolith vs microservices)
- Communication patterns (REST, message queue, events)
- Event-driven architecture adoption
- Service mesh / API gateway usage
- Deployment model (containers, serverless)

---

## Language, Framework & Libraries

**Key questions to ask:**
- What was already in use? What's the team familiar with?
- What specific capabilities drove the choice (performance, ecosystem, type safety)?
- What are the long-term maintenance implications?
- Was this a pragmatic choice or a principled one?

**Common decisions in this category:**
- Programming language choice
- Web framework selection
- Testing framework
- Dependency management approach
- Logging / observability library

---

## Data & Event Flow

**Key questions to ask:**
- Is this event-driven, request-driven, or batch?
- What's the ordering guarantee requirement?
- How are failures and retries handled?
- Who are the producers and consumers?

**Common decisions in this category:**
- Message broker choice (Kafka, RabbitMQ, SQS)
- Event schema format (JSON, Avro, Protobuf)
- Dead letter queue strategy
- Exactly-once vs at-least-once delivery
- Event sourcing adoption

---

## Security

**Key questions to ask:**
- What is the threat model?
- What data is being protected?
- Is this a compliance requirement (GDPR, SOC2, HIPAA)?
- Where does encryption happen (at rest, in transit, end-to-end)?

**Common decisions in this category:**
- Secret management approach
- Encryption at rest / in transit
- Data anonymization / pseudonymization
- Audit logging
- Dependency vulnerability scanning

---

## General Guidance

When the decision doesn't fit a clear category:
1. Focus on: what problem exists, what was chosen, and why alternatives failed
2. Make consequences concrete and specific — not "better performance" but "reduces p99 latency by ~30% under load"
3. If the decision was made under time pressure or incomplete information, say so — it's honest and helps future readers understand why it was revisited
