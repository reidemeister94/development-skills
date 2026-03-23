# Critical Analysis Framework

Reference document for the brainstorming skill's evaluation phase. Read this file when performing critical analysis of a proposed approach.

---

## Complexity Score (0-10)

Evaluate EACH dimension. Score 0-2 per dimension. Sum them.

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Reversibility** | Trivially reversible (rename, format, small fix) | Moderate effort to reverse (new feature, refactor) | Costly or impossible to reverse (architecture, public API, data model, migration) |
| **Blast radius** | Single file or function | Multiple files, one service | Multiple services, teams, or external consumers |
| **Ambiguity** | Clear, single correct approach | Multiple valid approaches | Genuinely uncertain, depends on trade-offs |
| **Novelty** | Team has done this exact thing before | Similar to past work but different context | First time, unfamiliar domain or technology |
| **Stakes** | Low impact if wrong (cosmetic, internal tooling) | Moderate impact (user-facing feature, performance) | High impact (security, data integrity, system stability, compliance) |

### Decision Threshold

| Total Score | Action |
|-------------|--------|
| 0-3 | SKIP critical analysis. Approach is low-risk. |
| 4-5 | SKIP. Borderline — only analyze if you see a specific, concrete risk. |
| 6-7 | LIGHT analysis. Focus on the 1-2 highest-risk dimensions only. |
| 8-10 | FULL analysis. Complete framework below. |

---

## FULL Critical Analysis Template (score 8-10)

### The Request
[One-sentence restatement of what is being decided]

### What You're Getting Right
[Acknowledge solid aspects. Skip if nothing to praise — do not fabricate.]

### Risks & Weaknesses

**[RISK 1: Clear name]**
- **What:** [Specific description]
- **Why it matters:** [Concrete impact if materialized]
- **Evidence:** [Citation from research — URL or source name]
- **Severity:** CRITICAL / HIGH / MEDIUM

[Minimum 2, maximum 5. Quality over quantity.]

### Hidden Assumptions
"You are assuming [X]. This breaks if [Y]."
[Only list assumptions that could actually break.]

### Alternatives Considered
| Approach | Pros | Cons | Best When |
|----------|------|------|-----------|
| [Requested] | ... | ... | ... |
| [Alt 1] | ... | ... | ... |

### Anti-Patterns to Avoid
"Do NOT [X] because [Y]. Source: [Z]"

### Verdict

**[PROCEED / PROCEED WITH CHANGES / RECONSIDER / STOP]**

- **PROCEED**: Sound approach. Risks manageable. Go ahead.
- **PROCEED WITH CHANGES**: Direction right, adjustments needed. [List changes.]
- **RECONSIDER**: Significant risks or better alternatives. [Explain.]
- **STOP**: Fundamental flaw. Must be resolved first. [Explain clearly.]

[2-3 sentence rationale.]

### Sources
[Numbered list with URLs]

---

## LIGHT Analysis Template (score 6-7)

### Decision
[One-sentence restatement]

### Key Risk
[Single biggest risk, with evidence]

### Watch Out For
[1-2 specific anti-patterns or pitfalls]

### Recommendation
[PROCEED / PROCEED WITH CHANGES / RECONSIDER] — [One sentence why]

### Source
[1-2 key references]

---

## Source Quality Hierarchy

| Tier | Source Type | Trust Level |
|------|-----------|-------------|
| 1 | Official docs, RFCs, specs | **Authoritative** — cite directly |
| 2 | Production post-mortems (Stripe, Netflix, Uber, Cloudflare) | **High** — real-world evidence |
| 3 | Reputable technical blogs (Martin Fowler, ThoughtWorks, CNCF) | **High** — expert analysis |
| 4 | Stack Overflow accepted answers with high votes | **Medium** — community consensus |
| 5 | Random blog posts, Medium articles | **Low** — verify independently |
| 6 | AI-generated, undated, no-author | **Ignore** |

---

## Tone Rules

### Be Direct
| Instead of... | Say... |
|---------------|--------|
| "You might want to consider..." | "This is wrong because..." |
| "It could potentially be an issue..." | "This will fail when..." |
| "Perhaps an alternative..." | "A better approach is..." |

### Be Constructive
Every criticism MUST include: (1) What is wrong, (2) Why (with evidence), (3) What to do instead.

### Be Calibrated
Match intensity to severity. Do not cry wolf on minor issues. Do not downplay critical ones.
