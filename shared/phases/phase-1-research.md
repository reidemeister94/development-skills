# Phase 1: RESEARCH — GATE

**Knowledge-first:** check what's on disk, fill only gaps — always in an **isolated subagent** so raw results never bloat your context.

## Step 1: Load existing research

Check plan file's `WORKFLOW STATE` for a `Research:` field pointing to `docs/plans/`.

- **Research file exists:** Read it. Do NOT repeat covered searches.
- **No research file:** No prior knowledge — create one in Step 3.

## Step 2: Always do

1. **Read language/framework patterns** — ALL pattern files from your skill's config. **LIGHTWEIGHT MODE:** read only Quick Reference and anti-patterns sections.
2. **Ask clarification questions** — focused, if unclear.
3. **Identify legacy patterns** — For non-trivial tasks, ask: "Are there existing patterns that should NOT be followed? Legacy workarounds to avoid?"
4. **Persist Q&A to disk** — Append `## Clarifications` to plan file:
   ```markdown
   ## Clarifications
   - **Q:** [question]
     **A:** [answer]
     **Impact:** [how this affects implementation]
   ```
   Skip if no questions needed.

## Step 3: Assess and fill gaps

Review task requirements against existing research. Identify missing implementation-specific knowledge, library/API details, unexplored codebase areas.

**No gaps:** State **"RESEARCH COMPLETE — leveraging brainstorming findings from `[file]`"** and proceed.

**Gaps exist:** Delegate to **isolated subagent** (Task tool, `general-purpose`, **model: opus**):

1. Receives: task description, specific gaps, existing research file path
2. Reads existing research to avoid duplication
3. Performs targeted searches and/or codebase exploration for gaps ONLY
4. **Writes to disk:**
   - Research file exists → append under `## Phase 1 Addendum`
   - No research file → create `docs/plans/NNNN__research__{slug}.md` (plan's NNNN prefix, slug = kebab-case task/topic name)
5. Returns brief summary (max 10 lines) + file path

**Subagent prompt:** Read `shared/agents/research-agent.md` (Glob `**/research-agent.md`). Replace placeholders, spawn via Task tool.

After return, read summary only (full research stays on disk for later phases).

## Step 4: Critical evaluation

If user proposes a solution, evaluate against research. If a better approach exists, say so directly. Keep it brief.

**Gate:** State **"RESEARCH COMPLETE"** with:
- Key findings summary
- Research file path
- Whether additional research was needed (and why)

## Expected Artifacts
- Research file on disk (from brainstorming or newly created)
- `## Clarifications` in plan file (if questions asked)
- WORKFLOW STATE unchanged (Phase 2 creates it)

**→ Proceed immediately to Phase 2. Read `phase-2-plan.md`.**
