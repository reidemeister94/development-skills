---
name: best-practices
description: "Use when the user wants state-of-the-art knowledge, best practices, or a comprehensive analysis of a software engineering or technology topic. Use when user says best practices, state of the art, pros and cons, comparison, when to use, how to choose, trade-offs, or /best-practices."
argument-hint: "<topic>"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Glob, Grep, Agent, TaskCreate, TaskUpdate, TaskList
---

# Best Practices — Deep Research & State-of-the-Art Analysis

ultrathink

**Announce:** "Researching **$ARGUMENTS** — gathering state-of-the-art knowledge from authoritative sources."

Read `references/research-strategy.md` in this skill's directory now. It contains the source tier hierarchy, search query templates, recency calibration table, hard quality gates, and the Phase 4 output template. Keep all of it active throughout.

## MANDATORY: Progress Updates

Emit a visible status line BEFORE launching tools at each phase transition:

- `Phase 0/4 — Fetching mandatory sources...` (skip if not Claude Code-related)
- `Phase 1/4 — Decomposing topic: [list angles]`
- `Phase 2/4 — Launching web research ({N} queries)...`
- `Research complete — {N} sources. Filtering by authority...`
- `Phase 3/4 — Deep-fetching top {N} URLs...`
- `Phase 4/4 — Synthesizing report from {N} sources...`

## Date Awareness — Temporal Calibration

Determine TODAY's date from the system context (e.g., `currentDate` in system-reminder). Set:

- `TODAY` = current date (e.g., 2026-03-27)
- `CURRENT_YEAR` = year from TODAY (e.g., 2026)
- `PREV_YEAR` = CURRENT_YEAR - 1 (e.g., 2025)
- `RECENCY_WINDOW` = PREV_YEAR and CURRENT_YEAR (e.g., "2025 2026")

See `references/research-strategy.md` for the recency calibration table and how to apply it.

## Argument Parsing

- **No arguments** (`$ARGUMENTS` is blank): Ask "What topic would you like me to research?" Then STOP.
- **Arguments present**: Treat `$ARGUMENTS` as the research topic.

Set `TOPIC` = `$ARGUMENTS`

---

## PHASE 0: MANDATORY SOURCES (Claude Code topics only)

Check if `TOPIC` relates to **Claude Code** (skills, SKILL.md, hooks, subagents, agents, CLAUDE.md, plugins, context engineering, agentic coding, Claude Code workflow, slash commands, MCP).

**If Claude Code-related**, fetch ALL of these in parallel before general web research (Tier S — non-negotiable):

| # | Source | What to extract | How |
|---|--------|----------------|-----|
| 1 | **Official Claude Code docs** | Best practices, skill authoring, subagent patterns, hook guide, context management | WebFetch `https://code.claude.com/docs/en/best-practices` AND `https://code.claude.com/docs/en/skills` AND `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` |
| 2 | **Claude Code releases** | Latest features, breaking changes, new capabilities, deprecations | WebFetch `https://github.com/anthropics/claude-code/releases` — extract all release notes from the last 3 months |
| 3 | **Local documentation** | Project-specific context, team conventions, local best practices | Check for relevant local documentation files if available (e.g. referenced in CLAUDE.md) |

**If NOT Claude Code-related**, skip this phase entirely.

---

## PHASE 1: DECOMPOSE THE TOPIC

Break the topic into 4-6 research angles before searching:

1. **Core concepts** — definitions, mental models, theory
2. **Trade-offs & comparisons** — when to use what, decision frameworks
3. **Practical patterns** — real-world implementation, battle-tested approaches
4. **Failure modes** — anti-patterns, lessons learned at scale
5. **Ecosystem & tooling** — libraries, frameworks, official docs
6. **Emerging trends** — recent shifts, industry direction

---

## PHASE 2: SYSTEMATIC WEB RESEARCH

See `references/research-strategy.md` for the full search battery (10 query patterns) and source tier table. Run all queries in parallel batches of 3-4 using Agent subagents. Apply the hard quality gates from the reference file to filter every result before it enters Phase 3.

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

See `references/research-strategy.md` for content extraction prompts tailored to engineering blogs, official docs, GitHub READMEs, books/papers, and community discussions.

**Handle failures gracefully:** If a URL fails to fetch, skip it and note it. Never retry more than once.

---

## PHASE 4: SYNTHESIS — STATE OF THE ART REPORT

Synthesize all gathered information using the output template in `references/research-strategy.md`. Write a comprehensive answer — not a link dump.

---

## RULES

1. **Signal over noise.** No filler, no generic advice, no "it depends" without specifying on WHAT.
2. **Cite sources inline.** "Netflix found that... [source]"
3. **Be opinionated where consensus exists.** State it clearly. Note dissenting views but don't false-balance.
4. **Concrete over abstract.** Numbers, benchmarks, code patterns over vague statements.
5. **Date-stamp everything.** Apply the recency calibration table from `references/research-strategy.md`.
6. **Acknowledge knowledge gaps.** Say so rather than speculate.
7. **No AI summaries of AI summaries.** Use primary sources.
8. **Language matching.** Write the report in the SAME LANGUAGE the user used.
9. **Hard quality gates are non-negotiable.** Apply gates from `references/research-strategy.md` to every resource in the report. If a section would be empty, state "No resources met the quality bar."
