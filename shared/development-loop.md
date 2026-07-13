# Development loop

Reason from first principles and favor simplicity above all — while preserving every requested capability and state-of-the-art quality. Build the smallest change that reaches an agreed, observable result. Challenge the premise and separate facts from interpretations. A skipped gate, suppressed test, swallowed warning, or hidden failure is a violation regardless of intent, in every skill and subagent. Cut useless words, never necessary information. When two rules conflict, pick the application a critical reader would find less surprising.

## Choose the path

Use the **direct path** only when the result, solution, and proof are already clear, the change is easy to reverse, and no business or design choice remains. Inspect, change, verify, report.

Use the **full path** for everything else. Uncertainty about the path means full.

## Full path

1. **Decide.** Inspect the code and available evidence before asking. State the problem, affected user or system, solved state, constraints, unknowns, and what would disprove the proposed answer. `brainstorming` is the default; skip it only when all three hold: fully reversible with low effort, one obvious forced approach, and the WHY does not affect the HOW. "The user said exactly what to do" fixes the WHAT, not the HOW; a prior spec or guide is input to the plan, never a substitute.
2. **Define the proof.** Agree on the smallest evidence that could expose failure. For business flows, KPIs, deep integrations, or probabilistic behavior, use `create-test` to design the regression contract.
3. **Express.** Research only when current external evidence or a durable unknown can change the decision; durable findings go to `docs/plans/NNNN__research__<slug>.md`. Write a decision-complete plan at `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__<slug>.md` and start a chronicle at `docs/chronicles/NNNN__YYYY-MM-DD__<topic>.md` (`NNNN` = highest existing prefix in that folder + 1). Plans hold the work and checks; chronicles hold intent, discoveries, and decisions. Then present the design — outcome, success check, out of scope, approach, files, risks — and gate implementation on explicit plan approval.
4. **Implement.** Work in small slices. Where a test can prove the behavior, see it fail before the fix and pass after it; production code written before its test is deleted, not adapted. Run the nearest useful check after each slice. Follow the project rules and applicable conventions. Update the chronicle when a discovery changes understanding.
5. **Verify.** Run the agreed outcome checks and repository quality gates with fresh output. A check that can only say yes is confirmation, not verification — pick one that would fail if the claim were false. Read failures and fix their cause; never weaken, skip, or suppress a check to claim success. Raise pre-existing failures instead of ignoring them.
6. **Review.** Give an independent reviewer the request, plan, standards, diff, and verification boundary. Fix every critical/high finding, rerun affected checks, finalize plan/chronicle/docs, and report what remains unobserved. Commit only when explicitly requested.

## Working rules

- Prefer an existing mechanism over a new file, abstraction, hook, or dependency.
- Remove any line or component whose deletion loses no useful behavior.
- Change only what traces to the request; preserve unrelated user work.
- Comments explain non-obvious reasons, not visible code.
- No material claim without evidence that could have proved it false.
- A failed proof or new unknown returns to the earliest step it invalidates.
- High-scale mechanical migrations: pilot a small batch, verify, fix the process, then scale.
- Skipping, deleting, or re-baselining a test needs explicit approval.

## Resume

An in-progress plan is the persistent state. Read its current step, standards, chronicle, and verification record; continue there instead of restarting discovery.
