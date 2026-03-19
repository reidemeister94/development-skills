# Phase 6: STAFF ENGINEER REVIEW — GATE

**MANDATORY. You CANNOT skip this.** Do not rationalize: "the changes are simple" or "I already verified."

## Before Spawning the Review Agent

1. Run `git diff` and **write it to a temp file** if it exceeds ~500 lines. Pass the file path to the reviewer instead of inlining the diff — large diffs bloat your context and degrade review quality.
2. Collect the pass/fail summary from Phase 5 (the full details are in the plan file — pass the path, not the content)
3. **If the diff exceeds ~2000 lines:** Split the review. Use the Task Checklist's per-task file list to group changes by component, then spawn separate reviewer invocations per component. Merge the results (all must pass).

## Spawn the `staff-reviewer` Agent

Use the Task tool. Pass:
- **Task:** The original requirement
- **Constraints:** Key constraints from the approved plan
- **Git diff:** The exact code changes
- **Plan file path:** The FULL path to the plan file. The reviewer reads the `## Task Checklist` (artifact trail) and `## Verification Results` sections directly from disk — this eliminates orchestrator paraphrasing.
- **Patterns file path(s):** As specified in your language skill's configuration — the agent reads them dynamically
- **Verification summary:** Pass/fail from Phase 5 (also in plan file, but pass it for convenience)
- **Additional context** from your language skill's staff review configuration (e.g., detected framework)

The agent performs a **two-stage review** (spec compliance THEN code quality):
1. **Stage 1 — Spec compliance:** Did the implementation address ALL requirements? Nothing missing, nothing extra.
2. **Stage 2 — Code quality:** Is it built well? Primary mandate is SIMPLIFICATION.

Returns APPROVED, SPEC_ISSUES, or ISSUES with file:line references.

## Persist Review Results to Disk

After EACH review cycle, append to the plan file's `## Review Log` section. This creates an audit trail of what was reviewed, what was found, and how it was resolved.

```markdown
## Review Log

### Review 1
- **Stage 1 (Spec):** PASS / SPEC_ISSUES
- **Stage 2 (Quality):** APPROVED / ISSUES
- **Issues found:**
  1. [file:line] [SEVERITY] [description] → Fix: [action taken]
  2. [file:line] [SEVERITY] [description] → Fix: [action taken]
- **Action:** Applied fixes, re-verified, re-submitted

### Review 2
- **Result:** APPROVED — Spec complete, no simplification possible.
```

## Handling Review Results

If SPEC_ISSUES found: fix missing/extra requirements, re-verify (Phase 5), re-review.
If ISSUES found: fix them, re-verify (Phase 5), re-review. Iterate until APPROVED.

**After a fix-review cycle:** Run `/compact` before re-spawning the reviewer to keep context clean.

**Gate:** State **"STAFF REVIEW: APPROVED"**

## Expected Artifacts
- `## Review Log` section appended to plan file (per-review iteration results)
- Staff reviewer returned APPROVED
- WORKFLOW STATE updated: `Current Phase: 7 (Finalize)`

**→ Proceed immediately to Phase 7. Read `phase-7-finalize.md`.**
