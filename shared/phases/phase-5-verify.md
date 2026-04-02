# Phase 5: VERIFY — GATE

**Spawn `test-verifier`** via Task tool with verification commands from your language skill. Verbose output stays in the subagent.

**Tier A — Projects with tests:** Pass verification commands. Add new tests for new/modified code first. Coverage target: 70-80%.

**Tier B — Legacy without tests:** Run verification inline (not subagent — requires interactive MCP with user confirmation): execute code path, capture output, log inspection.

**Language skills may define additional tiers** (e.g., Tier C for Xcode).

**Principle:** "Prove it works" — no positive claim without fresh evidence.

**Observation masking:** Verbose output stays in subagent. Only pass/fail summary returns. Write full details to plan file.

**Persist to disk:** Append `## Verification Results` to plan file with full details (audit trail for Phase 6):

```markdown
## Verification Results

### Iteration 1
- **Result:** 45/47 passed
- **Failures:**
  - `test_auth`: [error and root cause]
  - `test_validation`: [error and root cause]
- **Action:** [what was fixed]

### Final
- **Result:** 47/47 passed ✓
```

## If Verification FAILS

1. Read failure details
2. Code bug → fix, re-spawn verifier, stay in Phase 5
3. Plan wrong → return to Phase 2
4. Environmental → document, ask user

**Regression guard:** Track pass/fail across iterations. Net regression → STOP and reassess. Two consecutive regressions → return to Phase 2.

**After fix-verify cycle:** Run `/compact` before re-running.

**Gate:** State **"VERIFICATION COMPLETE"** with evidence.

## Expected Artifacts
- `## Verification Results` in plan file (full details)
- All tests passing (or failures documented with root cause)
- WORKFLOW STATE: `Current Phase: 6 (Staff Review)`

## Verification Checklist — MANDATORY

**Workflow Gates:**
- [ ] RESEARCH COMPLETE
- [ ] Plan approved (EnterPlanMode → ExitPlanMode)
- [ ] CHRONICLE INITIATED (or NOT NEEDED with reason)
- [ ] SOLUTION COMPLETE
- [ ] VERIFICATION COMPLETE with evidence
- [ ] STAFF REVIEW: APPROVED
- [ ] CHRONICLE FINALIZED (or NOT NEEDED confirmed)
- [ ] WORKFLOW COMPLETE

**Code Quality:**
- [ ] Simplest working solution
- [ ] No over-engineering
- [ ] Pure functions where possible
- [ ] No function > 70 lines
- [ ] Complexity minimized (no O(n²) when O(n) works)
- [ ] WHY comments on ambiguous code
- [ ] No restating comments (comments explain WHY, not WHAT the code does)
- [ ] No excessive error handling (try/catch only at boundaries, not on safe internal calls)
- [ ] Schema fields with non-trivial types annotated
- [ ] No useless WHAT comments
- [ ] TDD discipline (RED→GREEN→REFACTOR)

**Also check language skill's quality checklist.**

**→ Proceed immediately to Phase 6. Read `phase-6-review.md`.**
