# Research Strategy Reference

## Source Authority Hierarchy

When evaluating sources for best practices research, apply this hierarchy strictly:

### Tier S — Primary Authorities
- **Official documentation** (language/framework/tool docs)
- **RFCs and standards** (IETF, W3C, ECMA, IEEE)
- **Seminal papers** (Lamport, Brewer, Fowler, etc.)
- **Martin Fowler's Bliki** (martinfowler.com)
- **Google SRE Books** (sre.google)
- **AWS Well-Architected Framework**

### Tier A — Major Engineering Blogs
- Netflix Tech Blog (netflixtechblog.com)
- Uber Engineering (eng.uber.com)
- Stripe Engineering (stripe.com/blog/engineering)
- Airbnb Engineering (medium.com/airbnb-engineering)
- Meta Engineering (engineering.fb.com)
- Google AI Blog (blog.google/technology)
- Cloudflare Blog (blog.cloudflare.com)
- LinkedIn Engineering (engineering.linkedin.com)
- Spotify Engineering (engineering.atspotify.com)
- Shopify Engineering (shopify.engineering)
- Discord Engineering (discord.com/blog)

### Tier B — Trusted Industry Voices
- Pragmatic Engineer (blog.pragmaticengineer.com)
- Architecture Notes (architecturenotes.co)
- InfoQ (infoq.com)
- ThoughtWorks Technology Radar (thoughtworks.com/radar)
- ByteByteGo (blog.bytebytego.com)
- The New Stack (thenewstack.io)
- High Scalability (highscalability.com)
- CNCF Blog (cncf.io/blog)
- Increment Magazine (increment.com)
- ACM Queue (queue.acm.org)

### Tier C — Curated Open Source
- GitHub repos with ≥ 1,000 stars AND last commit within 6 months (both required — popularity without activity = abandoned)
- GitHub awesome-* lists (≥ 1k stars, actively maintained)
- Major OSS project documentation
- CNCF graduated/incubating projects
- Curated reading lists from recognized engineers

### Tier D — Community Discussion
- Hacker News top posts (news.ycombinator.com)
- Reddit r/programming, r/softwarearchitecture, r/devops (top posts only)
- Stack Overflow canonical answers (high-vote, community wiki)
- Dev.to posts from verified authors

### Disqualified Sources
- Content farms (medium posts with no author credibility)
- SEO-optimized listicles ("Top 10 ways to...")
- AI-generated summary articles
- Outdated content (>4 years from current date) unless foundational/seminal
- Vendor marketing disguised as technical content
- Tutorial sites recycling official docs
- **GitHub repos with < 1,000 stars OR last commit > 6 months ago** — both conditions must pass. A 1k-star active repo beats a 5k-star repo abandoned 2 years ago
- **Blog posts / articles by unknown authors** — if the author has no verifiable track record (books, conference talks, major OSS contributions, staff+ role at a recognized company), drop the resource
- **Engineering blogs from companies without at-scale production systems** — startup vanity blogs, agency blogs, and consultancy marketing posts are not credible engineering sources
- **Self-published books with no external validation** — must have multiple editions, ≥ 100 citations, or independent recommendations from authoritative sources
- **Random YouTube tutorials and meetup recordings** — only major conference talks (QCon, Strange Loop, KubeCon, GOTO, re:Invent, PyCon, etc.) from recognized speakers qualify

## Search Query Construction

### Principles
1. **Use quotes** for exact phrases: `"event-driven architecture"`
2. **Use site: operator** for authoritative domains: `site:martinfowler.com`
3. **Add year filters** for recency: `2025 OR 2026`
4. **Combine perspectives**: technical + business + operational
5. **Search for failures too**: `"lessons learned" OR "post-mortem" OR "mistakes"`

### Query Templates
For any topic X, use `{RECENCY_WINDOW}` (= PREV_YEAR + CURRENT_YEAR from system date):

```
# Authoritative overview
"X" best practices guide comprehensive

# Decision framework
"X" vs alternative "when to use" comparison trade-offs

# Production experience
"X" production experience scale lessons learned

# Engineering blogs
"X" site:netflixtechblog.com OR site:eng.uber.com OR site:stripe.com/blog

# Failure knowledge
"X" anti-patterns mistakes "lessons learned" post-mortem

# Books and deep content
"X" book recommended reading essential

# GitHub ecosystem
"X" awesome curated github stars

# Academic/research
"X" survey paper state of the art architecture

# Official docs
"X" official documentation getting started guide

# Emerging trends (use dynamic years)
"X" {RECENCY_WINDOW} trends future evolution
```

## Content Extraction Prompts

### For Engineering Blog Posts
```
Extract: key architectural decisions, specific metrics/benchmarks,
trade-offs evaluated, technologies chosen and why, lessons learned.
Skip: author bio, promotional content, job postings.
```

### For Official Documentation
```
Extract: core concepts, recommended patterns, configuration best practices,
performance guidelines, security considerations, migration paths.
Skip: installation steps, basic tutorials, API reference details.
```

### For GitHub READMEs
```
Extract: project purpose, key features, architecture approach,
performance claims with benchmarks, comparison with alternatives,
adoption indicators (stars, contributors, sponsors).
Skip: installation commands, license details, contribution guidelines.
```

### For Books/Papers
```
Extract: central thesis, key frameworks/models introduced,
most cited findings, practical recommendations,
chapter summaries for relevant sections.
Skip: acknowledgments, appendices, methodology details.
```

### For Community Discussions (HN/Reddit)
```
Extract: points with highest engagement that add original insight,
first-hand experience reports, contrarian views with evidence,
links to resources mentioned by commenters.
Skip: jokes, short agreement comments, off-topic tangents.
```

## Recency Calibration

Apply to every source and every claim in the final report:

| Age | Label | Treatment |
|-----|-------|-----------|
| < 12 months old | **Current** | Full weight, cite as current practice |
| 12-24 months old | **Recent** | High weight, note "as of {year}" |
| 2-4 years old | **Established** | Medium weight, only if still consensus — verify not superseded |
| > 4 years old | **Foundational** | Include ONLY if seminal (Fowler, Lamport, GoF, etc.) — explicitly mark as historical |

Use `RECENCY_WINDOW` (= PREV_YEAR + CURRENT_YEAR from system date) in ALL search queries instead of hardcoded years. Older content is NOT automatically wrong, but must be verified against current practice.

## Search Battery

Run all 8-10 queries per topic. Adapt `{TOPIC}` and `{RECENCY_WINDOW}` to the current topic and date.

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

Run queries in parallel batches of 3-4 using Agent subagents. Each subagent runs 1 WebSearch query and returns the top results. Select the **top 10-15 URLs** across all tiers for deep fetching.

## Hard Quality Gates

Apply to every resource before it enters the report. A resource that fails any gate is silently dropped — never mentioned, never linked, never recommended.

| Resource type | Minimum bar | How to verify |
|---------------|-------------|---------------|
| **GitHub repo** | ≥ 1,000 stars AND last commit within 6 months | Check stars AND recent commit activity via search snippet or WebFetch. Both conditions must be met. If either metric cannot be verified, drop it. |
| **Article / blog post** | Author or publication has established authority (Tier S/A/B, or recognized individual with verifiable track record) | Must be from named Tier S/A/B domains, or from an author with known body of work (conference talks, books, major OSS contributions). Anonymous Medium/Dev.to posts: drop. |
| **Engineering blog** | From a company with at-scale production systems | Must be a recognized engineering organization (see Tier A list above). Startup vanity blogs: drop. |
| **Book** | Multiple editions OR ≥ 100 citations OR recommended by ≥ 2 independent authoritative sources | Cross-reference authoritative reading lists or citation counts. Self-published with no external validation: drop. |
| **Conference talk / video** | Major conference (QCon, Strange Loop, KubeCon, GOTO, re:Invent, Google I/O, PyCon, JSConf, etc.) OR speaker with recognized expertise | Random YouTube tutorials or unknown-speaker meetup recordings: drop. |
| **Community discussion** | Top-voted HN/Reddit post with substantive first-hand experience | Low-engagement threads, anecdotal comments without evidence: drop. |

**Rationale:** Every recommendation carries implicit endorsement. Recommending unvetted or low-signal resources wastes the user's time and erodes trust. When in doubt, drop it — a shorter list of excellent resources beats a long list with filler.

## Phase 4 Output Template

Synthesize all gathered information into this structure. Write a comprehensive answer — not a link dump.

```markdown
# State of the Art: {TOPIC}

> **Research date:** {today's date}
> **Sources analyzed:** {N} articles, {N} engineering blogs, {N} GitHub projects, {N} books/papers

---

## TL;DR

[3-5 bullet points capturing the essential current consensus — what a senior engineer needs to know in 30 seconds]

---

## 1. Core Concepts & Mental Models

[Foundational theory. Define key terms. Explain the fundamental mental models experts use. Include diagrams/ASCII art if helpful.]

---

## 2. Trade-offs & Decision Framework

[When to use what. Present as a decision matrix or flowchart. Include specific criteria and thresholds.]

| Criterion | Option A | Option B | When it matters |
|-----------|----------|----------|----------------|

---

## 3. Best Practices (Current Consensus)

[Numbered list. Each practice with: the practice, WHY it matters (with source evidence), and an example or pattern.]

---

## 4. Anti-Patterns & Failure Modes

[What NOT to do. Real-world failures from engineering blogs. Each: the mistake, the consequence, the fix.]

---

## 5. Real-World Architecture & Patterns

[How leading companies implement this. Cite specific examples from Netflix, Uber, Stripe, etc.]

---

## 6. Ecosystem & Tooling

### Key Libraries & Frameworks (≥ 1k stars + active within 6 months)
| Name | Stars | Language | Best for | Link |
|------|-------|----------|----------|------|

### Official Documentation
- [links with brief descriptions]

---

## 7. Emerging Trends ({PREV_YEAR}-{CURRENT_YEAR})

[What's changing. New approaches, evolving consensus, upcoming shifts. Reference ThoughtWorks Radar, conference talks, recent papers.]

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

[Numbered list of ALL sources consulted, with URLs. Grouped by tier (S/A/B/C/D).]
```

## Synthesis Principles

1. **Triangulate**: A practice is "best practice" if 3+ independent authoritative sources agree
2. **Date-weight**: Apply the recency calibration table above. Current > Recent > Established > Foundational
3. **Scale-contextualize**: What works for Netflix may not work for a 5-person startup — always note scale context
4. **Evidence hierarchy**: Benchmark data > production experience > expert opinion > community consensus
5. **Acknowledge tension**: When authorities disagree, present both sides with their reasoning
6. **Concrete examples**: Every abstract principle should have at least one concrete implementation example
