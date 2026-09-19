# Full path

Use a plan for resumable work and a chronicle for lasting decision reasons.
The [development loop](development-loop.md) owns scope, authorization, standards, and completion.

## 1. Decide

Establish the requested result, constraints, open decisions, and evidence that would disprove the approach.
Resolve material decisions through `brainstorming`; use repository evidence for discoverable facts.

## 2. Define the proof

Define checks for the requested behavior and its important failure cases.
Use `create-test` when business flows, integrations, performance, or probabilistic behavior need a designed proof.

## 3. Express

Before implementation, write paired files at `docs/plans/YYYY-MM-DD__<slug>.md` and `docs/chronicles/YYYY-MM-DD__<slug>.md`.
Use the [plan](templates/plan-template.md) and [chronicle](templates/chronicle-template.md) templates.
Resume existing task files. For distinct tasks, choose distinct slugs; preserve legacy names.
Translate the template headings into the repository's documentation language.

The plan holds result, design, exact paths, work items, checks, and current state.
The chronicle holds the request, decision reasons, rejected alternatives, and useful failed approaches.
Write the chronicle with the [writing contract](writing.md).
Keep evidence beside the decision it supports. Keep execution and verification in the plan or linked reports.
Save useful research at `docs/plans/YYYY-MM-DD__research__<slug>.md`.

Then present the plan and ask for approval. Apply the loop's authorization rule: the plan and chronicle exist before the question.
Include the separate clean-context reviewer in the presentation.
After native Plan mode approval, save or update these records before implementation and continue the approved work.

## 4. Implement

Work in verifiable slices. Keep design facts, checklist state, and `Current step` current after each completed slice.
Keep changed reasons in the chronicle. Include the matching plan update when a commit is requested.

## 5. Verify

Run the agreed proof and required repository checks. Fix failures caused by the change and say what was not checked.
Report pre-existing failures separately. After repeated failed fixes, reassess the cause before trying the same approach again.

## 6. Review

Invoke `development-skills:staff-review` after verification. That skill owns the separate clean-context subagent review.
Wait for its specification and quality verdicts.
Fix every `MISSING` or `EXTRA` specification finding and every CRITICAL or HIGH quality finding.
Use the [severity scale](review-categories.md). Report MEDIUM and LOW findings without changing their ratings.
Run affected checks and re-review the required findings and fix diff.
Ask when a finding conflicts with an approved decision, requires new authority, or remains unresolved after three fix rounds.

## 7. Explain diff

Use `explain-diff` when the final change introduces a useful business, design, lifecycle, or failure concept.
Give it the request, plan, final diff, verification, review verdict, and unchecked limits.
An explanation does not delay completion for a mandatory comprehension interview.
If new evidence invalidates the work, return to the affected step. Changed code repeats verification and review.

Finalize task records, then invoke `development-skills:align-docs` with the task context.
