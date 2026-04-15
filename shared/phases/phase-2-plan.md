# Phase 2: PLAN — GATE

**Planning is 90% of the work.** A flawed plan produces flawed code. Remove ALL ambiguity, challenge assumptions, question reasoning. Last checkpoint before implementation tokens are spent.

**Use `EnterPlanMode`.** TaskCreate is NOT a substitute.

**Include WORKFLOW STATE at TOP:**

```
## WORKFLOW STATE
Status: In Progress
Current Phase: 2 (Plan)
Phases remaining: 3, 4, 5, 6, 7
Research: [docs/plans/NNNN__research__{slug}.md or NOT AVAILABLE]
Chronicle: [TBD — decided in Phase 3]
Verification: [commands from language skill]
```

The plan file is the **single persistent document**. Each phase appends: `## Clarifications` (P1), `## Task Checklist` (P4), `## Implementation Log` (P4), `## Verification Results` (P5), `## Review Log` (P6).

**Add quick-reference index** after WORKFLOW STATE:
```markdown
**Sections:** WORKFLOW STATE | Clarifications | Task Checklist | Implementation Log | Verification Results | Review Log
```

### Zero-Ambiguity Gate

**No plan survives ambiguity.** Eliminate ALL uncertainty first.

**First-principles check:** Does the plan address the actual problem? If brainstorming identified a framing mismatch, confirm with developer.

If unknowns remain, display questions as text and STOP. Wait for response. Do NOT use AskUserQuestion.

**Ask about:** implementation choices with two valid options, edge cases, info not in codebase, scope boundaries, assumptions.

If no genuine unknowns — skip to writing the plan.

### Write the Plan

Include:
- **Assumptions** — about codebase, requirements, environment
- **Risks** — what could go wrong, edge cases, side effects
- **Unknowns** — anything unclear (note explicitly — do NOT guess)
- **Verification strategy** — how to prove it works
- **Files to modify** — specific files and planned changes

Use `ExitPlanMode` to present. **WAIT for user approval.**

**After approval:** Check if brainstorming wrote a plan to `docs/plans/` — if so, update its WORKFLOW STATE. Otherwise, find next NNNN (highest + 1, default `0001`), write to `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__brief-description.md`.

**Keep WORKFLOW STATE current** after each phase.

**Re-plan trigger:** If implementation reveals the plan won't work: STOP coding, note what failed, return to Phase 2, get new approval, resume Phase 4.

**Gate:** User must explicitly approve.

## Expected Artifacts
- Plan file at `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__brief-description.md`
- WORKFLOW STATE with `Current Phase: 2` → updated to `3` after approval
- Sections index after WORKFLOW STATE
- User has approved

**→ Proceed immediately to Phase 3. Read `phase-3-chronicle.md`.**
