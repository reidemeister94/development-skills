# Phase 2: PLAN — GATE

**Planning is 90% of the work.** A flawed plan produces flawed code regardless of implementation quality. Invest heavily here: remove ALL ambiguity, challenge assumptions, question the developer's reasoning if something doesn't add up. This is the LAST checkpoint before tokens are spent on implementation.

**Use `EnterPlanMode` tool.** TaskCreate is NOT a substitute.

**Include a WORKFLOW STATE block at the TOP of the plan:**

```
## WORKFLOW STATE
Status: In Progress
Current Phase: 2 (Plan)
Phases remaining: 3, 4, 5, 6, 7
Research: [docs/plans/NNNN__research.md or NOT AVAILABLE]
Chronicle: [TBD — decided in Phase 3]
Verification: [use commands from your language skill's configuration]
```

The plan file is the **single persistent document** for this workflow. Every phase appends its outputs here. Sections added during the workflow: `## Clarifications` (Phase 1), `## Task Checklist` (Phase 4), `## Implementation Log` (Phase 4), `## Verification Results` (Phase 5), `## Review Log` (Phase 6). You do NOT need to create these sections now — they are added by each phase.

**Add a quick-reference index** after the WORKFLOW STATE block so later phases (especially Phase 6 reviewer) can jump directly to relevant sections without scanning the entire file:
```markdown
**Sections:** WORKFLOW STATE | Clarifications | Task Checklist | Implementation Log | Verification Results | Review Log
```
Update this index as sections are added — it stays at the top for fast navigation.

### Zero-Ambiguity Gate — Clarify Unknowns Before Writing the Plan

**No plan survives ambiguity.** Before writing, eliminate ALL remaining uncertainty. This is the last checkpoint before tokens are spent on implementation — any ambiguity here becomes a wrong assumption in code.

**First-principles check:** Does the plan address the actual problem (not just the requested solution)? If brainstorming identified a framing mismatch, the plan must address the corrected framing — confirm with the developer if not already resolved.

If unknowns or ambiguities remain, display your questions as text and STOP your turn. Wait for the user to respond, then incorporate their answers into the plan. Do NOT use AskUserQuestion — it auto-resolves in skill contexts.

**What to ask about:**
- Implementation choices where two valid options exist: "For [component], should we [option A] or [option B]?"
- Edge cases the user cares about: "How should the system handle [edge case]?"
- Information not in the codebase: "I couldn't determine [X] from research. Can you clarify?"
- Scope boundaries: "Should this also cover [related concern], or keep it out of scope?"
- Assumptions you're making: "I'm assuming [X]. Is that correct, or should I account for [Y]?"

**The questions also serve the developer** — they surface blind spots and force clearer thinking. A question that makes the developer reconsider a requirement is as valuable as one that gives you missing information.

If no genuine unknowns exist — the approach is confirmed, the codebase is clear, and the plan follows naturally — skip straight to writing the plan. Do NOT ask questions for the sake of asking.

### Write the Plan

Include:
- **Assumptions** — What you're assuming about the codebase, requirements, environment
- **Risks** — What could go wrong, edge cases, potential side effects
- **Unknowns** — Anything still unclear (note these explicitly — do NOT guess)
- **Verification strategy** — How you'll prove the solution works
- **Files to modify** — List specific files and planned changes (detailed enough that another developer could follow)

Use `ExitPlanMode` to present plan for user approval. **WAIT for user approval before any code changes.**

**After approval:** Check if brainstorming already wrote a plan file to `docs/plans/` — if so, use that file (update its WORKFLOW STATE). Otherwise, get next number via `bash scripts/find-plan.sh next` (from the development-skills plugin directory) and write to `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__brief-description.md`. This file survives context clearing.

**Keep WORKFLOW STATE current:** After completing each phase, update the plan file: advance `Current Phase`, remove completed phases from `Phases remaining`. Set `Status: Completed` when Phase 7 finishes.

**Do NOT make things up.** Missing detail? Ask or propose alternatives.

**Re-plan trigger:** If implementation reveals the plan won't work:
1. STOP coding immediately
2. Note what failed and why
3. Return to Phase 2 — update the plan, get new user approval
4. Resume Phase 4 with the updated plan

**Gate:** User must explicitly approve the plan.

## Expected Artifacts
- Plan file on disk at `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__brief-description.md`
- WORKFLOW STATE block at top with `Current Phase: 2 (Plan)` → updated to `3` after approval
- Sections index after WORKFLOW STATE
- User has explicitly approved the plan

**→ Proceed immediately to Phase 3. Read `phase-3-chronicle.md`.**
