---
name: best-practices
description: "Use when the user wants state-of-the-art knowledge, best practices, or a comprehensive analysis of a software engineering or technology topic. Use when user says best practices, state of the art, pros and cons, comparison, when to use, how to choose, trade-offs, or /best-practices. Performs deep web research from authoritative sources to deliver high-signal, noise-free analysis."
argument-hint: "<topic>"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList
---

# Best Practices — Deep Research & State-of-the-Art Analysis

ultrathink

**Announce:** "Researching **$ARGUMENTS** — gathering state-of-the-art knowledge from authoritative sources."

Read `references/research-strategy.md` in this skill's directory now. Keep its principles active throughout.

## MANDATORY: Progress Updates

**Output a short status message to the user at each phase transition.** The user must see progress in real-time. Use this exact pattern — output text BEFORE launching tools for each phase:

| When | Message pattern |
|------|----------------|
| Phase 0 start | `Phase 0/4 — Fetching mandatory sources (superpowers, official docs, releases, tips)...` |
| Phase 1 start | `Phase 1/4 — Decomposing topic into research angles...` then list the angles |
| Phase 2 start | `Phase 2/4 — Launching web research ({N} queries across {N} agents)...` |
| Phase 2 complete | `Research complete — {N} sources collected. Filtering by authority...` |
| Phase 3 start | `Phase 3/4 — Deep-fetching top {N} URLs...` |
| Phase 4 start | `Phase 4/4 — Synthesizing report from {N} sources...` |

**Rules:** Messages must be emitted as visible text output, not internal reasoning. Keep each under one line. Skip Phase 0 message if topic is not Claude Code-related.

## Date Awareness — Temporal Calibration

Determine TODAY's date from the system context (e.g., `currentDate` in system-reminder). Set:

- `TODAY` = current date (e.g., 2026-03-27)
- `CURRENT_YEAR` = year from TODAY (e.g., 2026)
- `PREV_YEAR` = CURRENT_YEAR - 1 (e.g., 2025)
- `RECENCY_WINDOW` = PREV_YEAR and CURRENT_YEAR (e.g., "2025 2026")

**Recency calibration for ALL searches and synthesis:**

| Age | Label | Treatment |
|-----|-------|-----------|
| < 12 months old | **Current** | Full weight, cite as current practice |
| 12-24 months old | **Recent** | High weight, note "as of {year}" |
| 2-4 years old | **Established** | Medium weight, only if still consensus — verify not superseded |
| > 4 years old | **Foundational** | Include ONLY if seminal (Fowler, Lamport, GoF, etc.) — explicitly mark as historical |

Use `RECENCY_WINDOW` in ALL search queries instead of hardcoded years. Older content is NOT automatically wrong, but must be verified against current practice.

## Argument Parsing

- **No arguments** (`$ARGUMENTS` is blank): Ask "What topic would you like me to research?" Then STOP.
- **Arguments present**: Treat `$ARGUMENTS` as the research topic.

Set `TOPIC` = `$ARGUMENTS`

---

## PHASE 0: MANDATORY SOURCES (Topic-Specific)

Before general web research, check if `TOPIC` relates to **Claude Code** (skills, SKILL.md, hooks, subagents, agents, CLAUDE.md, plugins, context engineering, agentic coding, Claude Code workflow, Claude Code best practices, slash commands, MCP in Claude Code).

**If Claude Code-related**, you MUST fetch and deeply read ALL of these sources IN ADDITION to the regular search battery. These are Tier S — authoritative, non-negotiable:

| # | Source | What to extract | How |
|---|--------|----------------|-----|
| 1 | **superpowers** — `@~/Documents/ai/superpowers` | Iron Laws, skill writing patterns (CSO, anti-rationalization tables, baseline testing), TDD enforcement, Two-Stage Review, progressive disclosure, subagent-driven development, whole-plan review, defense-in-depth. Read: `README.md`, `skills/writing-skills/SKILL.md`, `skills/test-driven-development/SKILL.md`, `skills/subagent-driven-development/SKILL.md`, `skills/verification-before-completion/SKILL.md` | Use Read tool on local files. If local copy unavailable, WebFetch `https://github.com/obra/superpowers` |
| 2 | **Claude Code releases** | Latest features, breaking changes, new capabilities, deprecations | WebFetch `https://github.com/anthropics/claude-code/releases` with prompt: "Extract all release notes from the last 3 months. Focus on new features, skill/agent/hook changes, and breaking changes." |
| 3 | **Official Claude Code docs** | Best practices, skill authoring, subagent patterns, hook guide, context management | WebFetch `https://code.claude.com/docs/en/best-practices` AND `https://code.claude.com/docs/en/skills` AND `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` |
| 4 | **claude-code-tips** — `@~/Documents/ai/claude-code-tips` | Community-tested tips, CLAUDE.md examples, workflow patterns, real-world productivity tricks | Use Read tool on local `README.md`. If unavailable, WebFetch `https://github.com/ykdojo/claude-code-tips` |
| 5 | **claude-code-best-practice** — `@~/Documents/ai/claude-code-best-practice` | all claude code best practices and references | Use Read tool on local `README.md`. If unavailable, WebFetch `https://github.com/shanraisshan/claude-code-best-practice` |


**Execution:** Fetch all sources in parallel (use Agent subagents or parallel tool calls). These results feed into Phase 4 synthesis alongside web research results.

**If NOT Claude Code-related**, skip this phase entirely.

---

## PHASE 1: DECOMPOSE THE TOPIC

Before searching, break the topic into 4-6 research angles. Think about what a staff engineer would want to know:

1. **Core concepts** — What is it? Definitions, mental models, fundamental theory
2. **Trade-offs & comparisons** — Pros/cons, when to use what, decision frameworks
3. **Practical patterns** — Real-world implementation, architecture examples, battle-tested approaches
4. **Failure modes** — Common mistakes, anti-patterns, lessons learned at scale
5. **Ecosystem & tooling** — Libraries, frameworks, GitHub projects, official docs
6. **Emerging trends** — What changed recently, where the industry is heading

---

## PHASE 2: SYSTEMATIC WEB RESEARCH

Execute ALL search queries below. Each query targets a different angle to maximize coverage.

### Search Battery (run all 8-10 queries)

Construct and execute these WebSearch queries, adapting keywords to `TOPIC`:

| # | Query Pattern | Purpose |
|---|--------------|---------|
| 1 | `"{TOPIC}" best practices {RECENCY_WINDOW}` | Recent best practices |
| 2 | `"{TOPIC}" trade-offs comparison "when to use"` | Decision frameworks |
| 3 | `"{TOPIC}" architecture real-world production` | Production experience |
| 4 | `"{TOPIC}" mistakes anti-patterns lessons learned` | Failure knowledge |
| 5 | `"{TOPIC}" site:martinfowler.com OR site:blog.pragmaticengineer.com OR site:architecturenotes.co` | Authoritative engineering blogs |
| 6 | `"{TOPIC}" site:github.com awesome OR curated stars` | GitHub ecosystem |
| 7 | `"{TOPIC}" book recommended reading` | Key literature |
| 8 | `"{TOPIC}" engineering blog Netflix OR Uber OR Stripe OR Airbnb OR Google OR Meta` | Big tech engineering |
| 9 | `"{TOPIC}" research paper survey state of the art` | Academic/deep analysis |
| 10 | `"{TOPIC}" official documentation guide` | Official docs |

**Execution:** Run queries in parallel batches of 3-4 using Agent subagents. Each subagent runs 1 WebSearch query and returns the top results.

Alternatively, if Agent parallelism is not available, run them sequentially — but run ALL of them.

### Source Quality Filter

From ALL search results, rank by authority. Prioritize:

| Tier | Source Type | Examples |
|------|-----------|----------|
| **S** | Official docs, RFCs, seminal papers | RFC docs, Martin Fowler, research papers |
| **A** | Major tech engineering blogs | Netflix Tech Blog, Uber Engineering, Stripe Blog, Google AI Blog |
| **B** | Well-known industry authors/blogs | Pragmatic Engineer, Architecture Notes, InfoQ, ThoughtWorks Radar |
| **C** | GitHub projects ≥ 1k stars + actively maintained, curated awesome-lists | awesome-* repos, major OSS projects |
| **D** | High-quality community (HN, Reddit top posts) | Top HN discussions, r/programming top posts |

### HARD QUALITY GATES — Zero Exceptions

These gates are **mandatory filters** applied to every resource before it enters the report. A resource that fails any gate is silently dropped — never mentioned, never linked, never recommended.

| Resource type | Minimum bar | How to verify |
|---------------|-------------|---------------|
| **GitHub repo** | ≥ 1,000 stars AND last commit within 6 months | Check stars AND recent commit activity via search snippet or WebFetch. Both conditions must be met. A repo with 1k stars and active commits beats one with 5k stars abandoned 2 years ago. If either metric is unknown and cannot be verified, drop it. |
| **Article / blog post** | Author or publication has established authority (Tier S/A/B sources, or recognized individual experts with verifiable track record) | Must be from the named Tier S/A/B domains, or from a named author with a known body of work (conference talks, books, major OSS contributions). Anonymous or first-time bloggers on Medium/Dev.to/personal sites: drop. |
| **Engineering blog** | From a company with at-scale production systems | Must be a recognized engineering organization (see `references/research-strategy.md` Tier A list, or comparable). Startup vanity blogs without technical depth: drop. |
| **Book** | Multiple editions OR ≥ 100 citations OR recommended by ≥ 2 independent authoritative sources | Cross-reference against authoritative reading lists, conference recommendations, or citation counts. Self-published books with no external validation: drop. |
| **Conference talk / video** | Major conference (QCon, Strange Loop, KubeCon, GOTO, re:Invent, Google I/O, PyCon, JSConf, etc.) OR speaker with recognized expertise | Random YouTube tutorials or meetup recordings from unknown speakers: drop. |
| **Community discussion** | Top-voted HN/Reddit post with substantive first-hand experience | Low-engagement threads, anecdotal comments without evidence: drop. |

**Rationale:** The user's time is the scarcest resource. Every recommendation carries implicit endorsement. Recommending obscure, unvetted, or low-signal resources wastes time and erodes trust. When in doubt, drop it — a shorter list of excellent resources beats a long list with filler.

Discard: SEO spam, low-effort listicles, outdated content (older than 4 years from TODAY unless foundational/seminal), content farms, AI-generated summaries.

Select the **top 10-15 URLs** across all tiers for deep fetching.

---

## PHASE 3: DEEP CONTENT EXTRACTION

For each selected URL, use WebFetch with a targeted prompt:

```
WebFetch(url, prompt="Extract the key insights, best practices, trade-offs,
and practical recommendations about {TOPIC} from this page. Include specific
data points, benchmarks, architecture decisions, and code patterns if present.
Focus on actionable, expert-level knowledge. Skip promotional content.")
```

**For GitHub repos:** Extract README summary, stars count, key features, and how they relate to `TOPIC`.

**For books/papers:** Extract title, author, key thesis, and most relevant chapter summaries.

**Handle failures gracefully:** If a URL fails to fetch, skip it and note it. Never retry more than once.

Collect all extracted content for synthesis.

---

## PHASE 4: SYNTHESIS — STATE OF THE ART REPORT

Synthesize ALL gathered information into a structured report. Write it as a comprehensive answer — not a link dump.

### Output Format

```markdown
# State of the Art: {TOPIC}

> **Research date:** {today's date}
> **Sources analyzed:** {N} articles, {N} engineering blogs, {N} GitHub projects, {N} books/papers

---

## TL;DR

[3-5 bullet points capturing the essential current consensus — what a senior engineer
needs to know in 30 seconds]

---

## 1. Core Concepts & Mental Models

[Foundational theory. Define key terms. Explain the fundamental mental models
that experts use to reason about this topic. Include diagrams/ASCII art if helpful.]

---

## 2. Trade-offs & Decision Framework

[When to use what. Present as a decision matrix or flowchart.
Include specific criteria and thresholds for choosing between alternatives.]

| Criterion | Option A | Option B | When it matters |
|-----------|----------|----------|----------------|
| ...       | ...      | ...      | ...             |

---

## 3. Best Practices (Current Consensus)

[Numbered list of battle-tested practices. Each with:
- The practice itself
- WHY it matters (with evidence from sources)
- Example or pattern]

---

## 4. Anti-Patterns & Failure Modes

[What NOT to do. Real-world failures cited from engineering blogs.
Each anti-pattern with: the mistake, the consequence, the fix.]

---

## 5. Real-World Architecture & Patterns

[How leading companies actually implement this. Cite specific examples
from Netflix, Uber, Stripe, etc. Include architecture patterns,
code patterns, and infrastructure choices.]

---

## 6. Ecosystem & Tooling

### Key Libraries & Frameworks (≥ 1k stars + active within 6 months)
| Name | Stars | Language | Best for | Link |
|------|-------|----------|----------|------|

### Official Documentation
- [links to official docs with brief descriptions]

---

## 7. Emerging Trends ({PREV_YEAR}-{CURRENT_YEAR})

[What's changing. New approaches, evolving consensus, upcoming shifts.
Reference ThoughtWorks Radar, conference talks, recent papers.]

---

## 8. Recommended Reading

### Books
| Title | Author | Year | Key takeaway |
|-------|--------|------|--------------|

### Articles & Blog Posts
| Title | Source | Key insight |
|-------|--------|-------------|

### Talks & Videos
| Title | Speaker/Event | Key point |
|-------|--------------|-----------|

---

## Sources

[Numbered list of ALL sources consulted, with URLs.
Grouped by tier (S/A/B/C/D) to signal authority level.]
```

---

## RULES

1. **Signal over noise.** Every sentence must add information. No filler, no generic advice, no "it depends" without specifying on WHAT.
2. **Cite sources inline.** When stating a fact or practice, reference the source: "Netflix found that... [source]" or "According to Martin Fowler [source]..."
3. **Be opinionated where consensus exists.** If 8 out of 10 authoritative sources agree, state the consensus clearly. Note dissenting views but don't false-balance.
4. **Concrete over abstract.** Prefer specific numbers, benchmarks, code patterns over vague statements.
5. **Date-stamp everything.** Use the recency calibration table. Note when practices are current ({RECENCY_WINDOW}) vs established vs foundational. Mark each source with its age category.
6. **Acknowledge knowledge gaps.** If research couldn't find authoritative answers for a sub-topic, say so rather than speculate.
7. **No AI summaries of AI summaries.** Use primary sources. If a result looks AI-generated, skip it.
8. **Language matching.** Write the report in the SAME LANGUAGE the user used in their prompt. If the user wrote in Italian, respond in Italian. If in English, respond in English. Match the user's language exactly.
9. **Hard quality gates are non-negotiable.** Never recommend GitHub repos with < 1k stars or inactive for > 6 months (both conditions must pass). Never cite articles from unknown/unvetted authors or publications. Never link engineering blogs from companies without at-scale production credibility. Apply the gates from Phase 2 to every single resource in the final report — including the Ecosystem & Tooling table, Recommended Reading, and inline citations. If enforcing these gates leaves a section empty, state "No resources met the quality bar" rather than lowering standards.
