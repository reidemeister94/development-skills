# Critical Analysis Framework

Reference for the brainstorming evaluation phase.

---

## Complexity Score (0-10)

Score 0-2 per dimension. Sum them.

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Reversibility** | Trivial (rename, format) | Moderate (new feature, refactor) | Costly/impossible (architecture, public API, migration) |
| **Blast radius** | Single file/function | Multiple files, one service | Multiple services/teams/consumers |
| **Ambiguity** | Single correct approach | Multiple valid approaches | Genuinely uncertain, trade-off dependent |
| **Novelty** | Done this exact thing before | Similar but different context | First time, unfamiliar domain/tech |
| **Stakes** | Low (cosmetic, internal) | Moderate (user-facing, performance) | High (security, data integrity, compliance) |

### Decision Threshold

| Score | Action |
|-------|--------|
| 0-3 | SKIP analysis. Low-risk. |
| 4-5 | SKIP. Only analyze if specific, concrete risk visible. |
| 6-7 | LIGHT analysis. Focus on 1-2 highest-risk dimensions. |
| 8-10 | FULL analysis. Complete framework below. |

---

## FULL Analysis (score 8-10)

### The Request
[One-sentence restatement]

### What You're Getting Right
[Solid aspects. Skip if nothing — do not fabricate.]

### Risks & Weaknesses

**[RISK 1: Name]**
- **What:** [Description]
- **Why it matters:** [Impact if materialized]
- **Evidence:** [Citation — URL or source]
- **Severity:** CRITICAL / HIGH / MEDIUM

[2-5 risks. Quality over quantity.]

### Hidden Assumptions
"You are assuming [X]. This breaks if [Y]."
[Only assumptions that could actually break.]

### Alternatives Considered
| Approach | Pros | Cons | Best When |
|----------|------|------|-----------|

### Anti-Patterns to Avoid
"Do NOT [X] because [Y]. Source: [Z]"

### Verdict

**[PROCEED / PROCEED WITH CHANGES / RECONSIDER / STOP]**

- **PROCEED**: Sound. Risks manageable.
- **PROCEED WITH CHANGES**: Direction right, adjustments needed. [List.]
- **RECONSIDER**: Significant risks or better alternatives. [Explain.]
- **STOP**: Fundamental flaw. [Explain.]

[2-3 sentence rationale.]

### Sources
[Numbered list with URLs]

---

## LIGHT Analysis (score 6-7)

### Decision
[One sentence]

### Key Risk
[Biggest risk with evidence]

### Watch Out For
[1-2 anti-patterns]

### Recommendation
[PROCEED / PROCEED WITH CHANGES / RECONSIDER] — [One sentence]

### Source
[1-2 references]

---

## Source Quality

| Tier | Source | Trust |
|------|--------|-------|
| 1 | Official docs, RFCs, specs | Authoritative |
| 2 | Production post-mortems (Stripe, Netflix, Uber) | High |
| 3 | Reputable blogs (Fowler, ThoughtWorks, CNCF) | High |
| 4 | Stack Overflow high-vote accepted | Medium |
| 5 | Random blogs, Medium | Low |
| 6 | AI-generated, undated, no-author | Ignore |

---

## Tone

### Be Direct
| Instead of... | Say... |
|---------------|--------|
| "You might want to consider..." | "This is wrong because..." |
| "It could potentially be an issue..." | "This will fail when..." |
| "Perhaps an alternative..." | "A better approach is..." |

### Be Constructive
Every criticism: (1) what is wrong, (2) why (with evidence), (3) what to do instead.

### Be Calibrated
Match intensity to severity. No crying wolf on minor issues. No downplaying critical ones.
