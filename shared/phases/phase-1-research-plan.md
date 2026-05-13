# Phase 1: RESEARCH + PLAN — GATE

**Combined phase.** Research informs planning; planning locks ambiguity. **Planning is 90% of the work** — a flawed plan produces flawed code. Last checkpoint before implementation tokens are spent.

**Knowledge-first:** check what's on disk, fill only gaps in an **isolated subagent** so raw results never bloat your context. Then write a plan to disk, lock the HOW-level ambiguities, gate.

Apply [Iron Rules](../iron-rules.md) — especially #2 (no positive claims without evidence) and #6 (every gate explicit).

---

## Step 1: Load existing research

Check plan file's `WORKFLOW STATE` for a `Research:` field pointing to `docs/plans/NNNN__research__{slug}.md`.

- **Research file exists** (brainstorming wrote one, or a prior phase did): Read it. Do NOT repeat covered searches.
- **No research file:** No prior knowledge — create one in Step 3 if gaps require it.

---

## Step 2: Read patterns + ask clarification questions

1. **Read language/framework patterns** — ALL pattern files from your skill's config.
2. **Ask clarification questions** — focused, if unclear.
3. **Identify legacy patterns** — For non-trivial tasks, ask: *"Are there existing patterns that should NOT be followed? Legacy workarounds to avoid?"*
4. **Persist Q&A to disk** — Append `## Clarifications` to plan file:
   ```markdown
   ## Clarifications
   - **Q:** [question]
     **A:** [answer]
     **Impact:** [how this affects implementation]
   ```
   Skip if no questions needed.

---

## Step 3: Assess and fill research gaps

Review task requirements against existing research. Identify missing implementation-specific knowledge, library/API details, unexplored codebase areas.

**No gaps:** State **"RESEARCH OK — leveraging existing findings from `[file]`"** and proceed to Step 4.

**Gaps exist:** Delegate to **isolated subagent** (Task tool, `general-purpose`, **model: opus**):

1. Receives: task description, specific gaps, existing research file path.
2. Reads existing research to avoid duplication.
3. Performs targeted searches / codebase exploration for gaps ONLY.
4. **Writes to disk:**
   - Research file exists → append under `## Phase 1 Addendum`
   - No research file → create `docs/plans/NNNN__research__{slug}.md` (plan's NNNN prefix, slug = kebab-case task topic)
5. Returns brief summary (max 10 lines) + file path.

**Subagent prompt template:** Read `shared/agents/research-agent.md`. Fill `{TASK}`, `{RESEARCH_TARGETS}` (the gaps), `{CODEBASE_FINDINGS}`, `{EXISTING_RESEARCH_FILE}` (path if any, else `"none"`), `{NNNN}`, `{SLUG}`. Spawn via Task tool.

After return, read summary only (full research stays on disk for later phases).

---

## Step 4: Write the Plan to disk

**The plan file is the single persistent artifact.**

Write or update `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__brief-description.md` with:

```markdown
## WORKFLOW STATE
Status: In Progress
Current Phase: 1 (Research + Plan)
Phases remaining: 2, 3, 4
Research: [docs/plans/NNNN__research__{slug}.md or NOT AVAILABLE]
Chronicle: [TBD — decided in Phase 2]
Verification: [commands from language skill]

**Sections:** WORKFLOW STATE | Clarifications | Plan | Task Checklist | Implementation Log | Verification Results | Review Log

## Plan
- **Assumptions** — about codebase, requirements, environment
- **Risks** — what could go wrong, edge cases, side effects
- **Unknowns** — anything unclear (note explicitly — do NOT guess)
- **Verification strategy** — how to prove it works
- **Files to modify** — specific files and planned changes
- **HOW-level locks** — see Step 5 below (mandatory)
```

Each subsequent phase appends: `## Task Checklist` + `## Implementation Log` + `## Verification Results` (all P3), `## Review Log` (P4).

---

## Step 5: Zero-Ambiguity HOW-Level Q&A — MANDATORY

**No plan survives ambiguity at the HOW level.** For every dimension below, the plan must lock the answer OR state N/A with a one-line reason. The model does not guess.

Apply [Iron Rules](../iron-rules.md) Pillar 1 (simplicity) and Pillar 2 (signal-not-noise) when filling each cell — pick the simplest answer that handles the dimension. If a dimension genuinely doesn't apply, state N/A explicitly; never leave a cell blank.

| Dimension | What to lock |
|---|---|
| **Edge cases** | Empty input, null, max size, concurrent access, partial failure paths |
| **Data shapes** | Exact field types, optional/required, nullable, default values |
| **Error semantics** | Raise vs return, retry policy, idempotency, error propagation |
| **Contract boundaries** | Public API surface, callers to update, schema/migration impact |
| **Test scope** | Unit, integration, regression baseline; what's explicitly deferred |
| **Rollback** | Single-commit revert? Feature flag? Migration reversibility? |

**Format in the plan file:**

```markdown
### HOW-level locks
| Dimension | Answer |
|---|---|
| Edge cases | [decision or N/A: reason] |
| Data shapes | [decision or N/A: reason] |
| Error semantics | [decision or N/A: reason] |
| Contract boundaries | [decision or N/A: reason] |
| Test scope | [decision or N/A: reason] |
| Rollback | [decision or N/A: reason] |
```

A blank cell is a red flag — the model doesn't know yet. Ask the user.

**For unknowns:** Display questions as plain text and STOP. Wait for response. (`AskUserQuestion` fits when the answer is a discrete pick from 2-4 options; use plain text for free-form unknowns.)

---

## Step 6: Critical evaluation

If the user proposed a solution, evaluate against research. If a better approach exists, say so directly. Apply [Iron Rule #1](../iron-rules.md): critical, not agreeable. Keep it brief.

---

## Step 7: Present plan summary, gate on approval

Display a 6-10 line summary in chat: scope, approach, files to touch, HOW-level locks status, verification strategy, key risk.

Ask: **"Approve the plan and proceed to Chronicle/Implementation?"** — on Claude Code use `AskUserQuestion` with options `"Approve and proceed (Recommended)"` / `"Modify"`. On Codex, numbered list + STOP.

**WAIT for explicit user approval.** No "looks good" inferred from silence.

**On approval:** Update WORKFLOW STATE to `Current Phase: 2`. Proceed immediately.

**Re-plan trigger:** If implementation reveals the plan won't work, STOP coding, return here, get new approval.

---

## Expected Artifacts

- Plan file at `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__brief-description.md`
- `## Clarifications` (if questions asked)
- `## Plan` with `### HOW-level locks` table — all 6 dimensions filled or marked N/A
- User has explicitly approved

**Gate:** State **"RESEARCH + PLAN COMPLETE — APPROVED"**

**→ Proceed immediately to Phase 2. Read `phase-2-chronicle.md`.**
