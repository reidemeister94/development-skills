# Phase 1: RESEARCH — GATE

Research follows a **knowledge-first** model: check what's already known (on disk), then fill only the gaps — and always in an **isolated subagent** so raw search results never bloat your main context.

## Step 1: Load existing research knowledge

Check the active plan file's `WORKFLOW STATE` for a `Research:` field. If present, that file (in `docs/plans/`) contains structured research from brainstorming — web findings, codebase analysis, alternatives evaluated, sources.

- **If a research file exists:** Read it. This is your knowledge base. Do NOT repeat searches that are already covered.
- **If no research file exists:** No prior knowledge — you will create one in Step 3.

## Step 2: Always do (regardless of prior research)

1. **Read language/framework patterns** — Read ALL pattern files specified in your language skill's configuration. These are implementation-specific and are NOT covered by brainstorming. **In LIGHTWEIGHT MODE:** read only the Quick Reference and anti-patterns sections of patterns.md (skip the full examples).
2. **Ask clarification questions** — If anything is unclear about the task, ask the user. Keep it focused.
3. **Identify legacy patterns** — For non-trivial tasks, ask the user: "Are there existing patterns in this codebase that should NOT be followed? Any legacy workarounds the new implementation should avoid?" This distinguishes essential complexity (keep) from accidental complexity (don't replicate).
4. **Persist Q&A to disk** — After all clarification questions are answered, append a `## Clarifications` section to the plan file with each question, the user's answer, and its impact on implementation. This ensures the implementer (Phase 4) sees user constraints even if context is compacted.
   ```markdown
   ## Clarifications
   - **Q:** [question asked]
     **A:** [user's answer]
     **Impact:** [how this affects the implementation]
   ```
   If no clarification questions were needed, skip this step.

## Step 3: Assess knowledge gaps and fill them

Review the task requirements against the existing research knowledge (Step 1). Identify what's **missing** for implementation:

- Are there implementation-specific technical questions not covered by the research file?
- Does the task require knowledge about libraries, APIs, or patterns not yet researched?
- Are there codebase areas not yet explored that the implementation will touch?

**If no gaps exist** (brainstorming research is sufficient): State **"RESEARCH COMPLETE — leveraging brainstorming findings from `[research file]`"** and proceed.

**If gaps exist**, delegate ALL additional research to an **isolated subagent** via the Task tool (`general-purpose` agent, **model: opus** — use the best model for research to ensure high-quality analysis of complex code relationships and accurate synthesis). The subagent:

1. Receives: the task description, the specific gaps to research, and the path to the existing research file (if any)
2. Reads the existing research file (if any) to avoid duplication
3. Performs targeted web searches and/or codebase exploration for the gaps ONLY
4. **Writes findings to disk** — either appending to the existing research file or creating a new one:
   - **If research file exists:** Append new sections under a `## Phase 1 Addendum` heading in the same file
   - **If no research file exists:** Create `docs/plans/NNNN__research.md` (use the active plan's NNNN prefix — the plan file already exists at this point). Use the same structured format: `## Web Research`, `## Codebase Analysis`, `## Sources`
5. Returns a **brief summary** (bullet points, max 10 lines) of what was found and the path to the research file

**The subagent prompt:** Read the research agent template at `shared/agents/research-agent.md` (use Glob to find `**/research-agent.md` if path is unknown). Replace placeholders with actual values and spawn via Task tool.

After the subagent returns, read its summary (NOT the full research file — that stays on disk for later phases).

## Step 4: Critical evaluation (always in main context)

- If the user proposes a solution, evaluate honestly against the research knowledge. If a better approach exists, say so directly.
- This is a quick judgement call, not a research activity — keep it brief.

**Gate:** State **"RESEARCH COMPLETE"** with:
- Summary of key findings (from existing research + any new research)
- Path to the research file on disk
- Whether additional research was needed beyond brainstorming (and why)

## Expected Artifacts
- Research file on disk (existing from brainstorming, or newly created)
- `## Clarifications` section appended to plan file (if questions were asked)
- WORKFLOW STATE unchanged (Phase 1 doesn't update it — Phase 2 creates it)

**→ Proceed immediately to Phase 2. Read `phase-2-plan.md`.**
