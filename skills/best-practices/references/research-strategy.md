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
- GitHub awesome-* lists (>5k stars)
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

## Synthesis Principles

1. **Triangulate**: A practice is "best practice" if 3+ independent authoritative sources agree
2. **Date-weight**: Apply the recency calibration table from SKILL.md. Current > Recent > Established > Foundational
3. **Scale-contextualize**: What works for Netflix may not work for a 5-person startup — always note scale context
4. **Evidence hierarchy**: Benchmark data > production experience > expert opinion > community consensus
5. **Acknowledge tension**: When authorities disagree, present both sides with their reasoning
6. **Concrete examples**: Every abstract principle should have at least one concrete implementation example
