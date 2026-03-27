# Distill Test Fixtures Manifest

20 test files covering all 10 noise categories, edge cases, and difficulty levels.

| # | File | Primary Noise | Difficulty | Key Assertions |
|---|------|--------------|------------|----------------|
| 01 | hedging-heavy | Hedging (cat 1) | Easy | All 10 hedges removed, 3 env vars preserved |
| 02 | transitions-conclusions | Transitions (2) + Conclusions (3) | Easy | 12 transitions removed, 5 migration steps preserved, conclusion paragraph deleted |
| 03 | buzzwords-verbose | Buzzwords (5) + Verbose (6) | Medium | 15+ buzzwords removed, 16 verbose→short subs, 4 architecture facts preserved |
| 04 | noncommittal-hedging | Non-committal (8) + Hedging (1) | Medium | "can potentially" → direct claims, 47 queries/800ms/3 fixes preserved |
| 05 | repetition-redundancy | Repetition (9) | Medium | Each fact stated once (JWT/24h/bcrypt/rate-limit), >50% word reduction |
| 06 | structural-padding | Structural (7) | Easy | Intro/summary/TOC removed, all env vars preserved verbatim |
| 07 | filler-openers-chatbot | Fillers (4) | Easy | All "Certainly!/Great question!" deleted, 2 code blocks preserved |
| 08 | verbosity-compensation | VC (10) | Medium | Direct answer early, SQL commands preserved, 4 isolation levels listed |
| 09 | already-dense | None | Edge case | <10% reduction, marked "already dense", all values/ARNs preserved |
| 10 | mixed-all-patterns | All 10 categories | Hard | All timeline entries preserved, 4 action items intact, noise from all cats removed |
| 11 | code-heavy-preserve | Mixed | Medium | YAML + Python code blocks byte-identical, noise prose compressed |
| 12 | italian-text | Mixed (Italian) | Medium | Output in Italian, YAML config preserved, all 4 alerts preserved |
| 13 | urls-dates-numbers | Mixed | Hard | All URLs/Jira IDs/dates/$ amounts/percentages preserved exactly |
| 14 | nuance-preservation | Minimal noise | Hard | A/B test stats preserved, all 3 strategies preserved with rationale, limitation preserved |
| 15 | adversarial-meaning-change | Minimal noise | Hard | CVSS scores preserved, code examples preserved, severity levels unchanged |
| 16 | linkedin-corporate | Buzzwords (5) + Structural (7) | Medium | 3 roadmap dates preserved, 65%/99.97% stats preserved, hashtags removed |
| 17 | table-heavy | Hedging + Tables | Medium | All 3 comparison tables preserved with exact numbers, decision preserved |
| 18 | adr-decision-record | Transitions | Medium | ADR structure preserved, 4 decision reasons preserved, consequences preserved |
| 19 | extreme-inflation | All categories | Easy | >50% word reduction, all code blocks preserved, command table preserved |
| 20 | minimal-noise-technical | Near-zero noise | Edge case | <10% reduction, YAML preserved, priority range preserved |

## Coverage Matrix

| Noise Category | Primary in | Also appears in |
|---------------|-----------|-----------------|
| 1. Hedging | 01, 04 | 10, 13, 17 |
| 2. Empty transitions | 02 | 03, 10, 11, 13, 18, 19 |
| 3. Empty conclusions | 02 | 10, 12, 19 |
| 4. Filler openers | 07 | 08, 10, 19 |
| 5. Buzzword inflation | 03, 16 | 10, 18, 19 |
| 6. Verbose constructions | 03 | 04, 10, 11, 13, 18, 19 |
| 7. Structural padding | 06, 16 | 10, 19 |
| 8. Non-committal language | 04 | 10, 18 |
| 9. Repetition/redundancy | 05 | 08, 10 |
| 10. Verbosity compensation | 08 | 10, 19 |

## Edge Cases

| Case | Files | Why it matters |
|------|-------|---------------|
| Already dense text | 09, 20 | Must not over-compress; should report "already dense" |
| Code-heavy | 11, 15, 19 | Code blocks must be byte-identical |
| Numbers/URLs/dates | 13, 15, 17 | Hard-gate: NEVER delete facts, numbers, URLs |
| Nuance preservation | 14, 18 | Qualified claims must keep qualifications |
| Non-English | 12 | Must preserve language |
| Meaning change risk | 15 | Security findings must not be softened |
| Tables with data | 17 | Table data must be preserved exactly |
