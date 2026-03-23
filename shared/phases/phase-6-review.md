# Phase 6: STAFF ENGINEER REVIEW — GATE

**MANDATORY. Cannot skip.** Do not rationalize "simple changes" or "already verified."

## Before Spawning

1. Run `git diff` — if >500 lines, write to temp file and pass path
2. Collect Phase 5 pass/fail summary (full details in plan file — pass path, not content)
3. **If diff >2000 lines:** Split by component using Task Checklist's file list. Spawn separate reviews. All must pass.

## Spawn `staff-reviewer`

Via Task tool. Pass:
- **Task:** Original requirement
- **Constraints:** From approved plan
- **Git diff:** The changes
- **Plan file path:** FULL path — reviewer reads `## Task Checklist` and `## Verification Results` directly
- **Patterns file path(s):** From language skill config
- **Verification summary:** Phase 5 result
- **Additional context** from language skill (e.g., detected framework)

Two-stage review: spec compliance THEN code quality. Returns APPROVED, SPEC_ISSUES, or ISSUES with file:line.

## Persist Results

Append `## Review Log` to plan file after EACH cycle:

```markdown
## Review Log

### Review 1
- **Stage 1 (Spec):** PASS / SPEC_ISSUES
- **Stage 2 (Quality):** APPROVED / ISSUES
- **Issues:**
  1. [file:line] [SEVERITY] [description] → Fix: [action]
- **Action:** Applied fixes, re-verified, re-submitted

### Review 2
- **Result:** APPROVED
```

## Handling Results

SPEC_ISSUES → fix, re-verify (Phase 5), re-review.
ISSUES → fix, re-verify (Phase 5), re-review. Iterate until APPROVED.

**After fix-review cycle:** Run `/compact` before re-spawning.

**Gate:** State **"STAFF REVIEW: APPROVED"**

## Expected Artifacts
- `## Review Log` in plan file
- Staff reviewer APPROVED
- WORKFLOW STATE: `Current Phase: 7 (Finalize)`

**→ Proceed immediately to Phase 7. Read `phase-7-finalize.md`.**
