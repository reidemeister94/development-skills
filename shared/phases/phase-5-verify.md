# Phase 5: VERIFY — GATE

**Spawn the `test-verifier` agent** via the Task tool with the verification commands from your language skill's configuration. Verbose output stays in the subagent's context, not yours.

**Tier A — Projects with tests:** Pass the verification commands specified in your language skill's configuration to the verifier. Add new tests for new/modified code before running. Coverage target: 70-80%.

**Tier B — Legacy projects without tests:** Run verification inline (not via subagent — Tier B requires interactive MCP operations that need user confirmation):
- Execute the code path, capture and show output
- Log inspection, MCP-assisted verification if available
- **PRODUCTION ENVIRONMENT** — ASK user before ANY MCP operation.

**Language skills may define additional tiers** (e.g., Tier C for Xcode projects). Check your language skill's verification configuration.

**Principle:** "Prove to me this works" — the verifier returns pass/fail summary with failure details.

**Persist verification results to disk:** After the verifier returns, append a `## Verification Results` section to the plan file. Write the **full details**, not just a summary — this is the audit trail that Phase 6 (Staff Review) reads from disk. Avoids telephone-game information loss.

```markdown
## Verification Results

### Iteration 1
- **Result:** 45/47 passed
- **Failures:**
  - `test_auth`: [specific error message and root cause]
  - `test_validation`: [specific error message and root cause]
- **Action:** [what was fixed and why]

### Iteration 2
- **Result:** 46/47 passed (net +1)
- **Fixed:** test_auth — [what was done]
- **Remaining:** test_validation — [why still failing]
- **Action:** [next fix applied]

### Final
- **Result:** 47/47 passed ✓
```

## If Verification FAILS

1. Read failure details from verifier's response
2. Code bug → fix it, re-spawn verifier, stay in Phase 5
3. Plan was wrong → return to Phase 2, update plan, get approval, re-implement
4. Environmental issue → document it, ask the user for help

**Regression guard:** Track the total test pass/fail count across iterations in the `## Verification Results` section. If a fix causes net regression (fixes 1 test but breaks 2), STOP and reassess the approach. Two consecutive regressions = return to Phase 2.

**After a fix-verify cycle:** Run `/compact` before re-running verification to keep context clean.

**Gate:** State **"VERIFICATION COMPLETE"** with evidence (verifier's pass/fail summary).

## Expected Artifacts
- `## Verification Results` section appended to plan file (full details, not just summary)
- All tests passing (or failures documented with root cause)
- WORKFLOW STATE updated: `Current Phase: 6 (Staff Review)`

## Verification Checklist — MANDATORY

Complete ALL items before claiming task completion:

**Workflow Gates:**
- [ ] RESEARCH COMPLETE stated
- [ ] Plan approved by user (EnterPlanMode → ExitPlanMode)
- [ ] CHRONICLE INITIATED (or NOT NEEDED with reason)
- [ ] SOLUTION COMPLETE stated
- [ ] VERIFICATION COMPLETE stated with evidence
- [ ] STAFF REVIEW: APPROVED
- [ ] CHRONICLE FINALIZED (or NOT NEEDED confirmed)
- [ ] WORKFLOW COMPLETE stated

**Code Quality:**
- [ ] Simplest working solution
- [ ] No over-engineering or unnecessary abstraction
- [ ] Functions are pure where possible
- [ ] No function exceeds 70 lines (decomposed with single responsibility)
- [ ] Time/space complexity minimized (no O(n²) when O(n) possible)
- [ ] Only non-obvious code commented

**Also check your language skill's quality checklist** for language-specific items.

**→ Proceed immediately to Phase 6. Read `phase-6-review.md`.**
