# Development loop

Complete the requested result with the smallest useful change. Keep project knowledge and operational constraints.
Use the [writing contract](writing.md) for natural language and the [engineering contract](engineering.md) for code and design.

## Standards gate

Before editing, read the project's agent instructions, matching scoped rules, and applicable project conventions.
Inspect the affected files and their callers. Load references only when their subject applies.

Apply sources in this order: the current explicit user decision; project rules; standards of record; established local patterns; model defaults.
Read a named reference project only when these sources leave an important choice unresolved.
Record selected standards in a plan when one is needed. Otherwise cite them when they explain a decision or conflict.

## Design authority

Respect the user's outcome, constraints, and chosen approach. Challenge an approach when evidence shows a concrete problem.
Explain the cost and recommend an alternative that preserves the requested result.
Ask when a consequential choice remains unresolved; reuse explicit decisions and existing authorization.
Examples include a published contract, authentication behavior, or a data model holding real records.
Continue independent work while that decision remains open.
Treat a prescribed implementation as an assumption to check against standards and evidence.
If that check exposes a problem, resolve the contested approach through `brainstorming` before editing.
Present the alternative for agreement; do not implement it merely because it appears better.
A reaffirmed user choice governs; record a material deviation and its consequences.

For a disputed tool or library claim, check official documentation for the version actually in use.
Check current documentation when a recommendation depends on what is available today.
Distinguish installed behavior from upgrade advice. Never upgrade a dependency silently.

## Reach agreement

Use `brainstorming` for unresolved goals, business trade-offs, consequential choices, or a contested approach.
On every path, interview until every branch of the open decision is settled. The number of questions follows the ambiguity.
Look up discoverable facts. Choose routine, reversible implementation details only after the design decisions are settled.
A request with nothing open gets no interview questions; the approval question follows Authorization.
Include a recommended answer and its trade-off with each question.
Group only independent questions; resolve dependent questions in order.
The skill owns interview depth, design checks, and the stop before planning while decisions remain open.

Use the platform's available question tool within its limits. Otherwise ask one concise question in chat.
For tool mappings, read [Codex tools](../skills/using-development-skills/references/codex-tools.md).

### Authorization

The approval unit is a presented plan. A plan exists when `brainstorming` settled open decisions or the full path wrote a plan file.
When no plan exists, the explicit request to implement authorizes the in-scope edits and their checks.
When a plan exists, present it in chat before the first implementation edit as a native Plan mode summary.
Give it four sections: context and why, what changes, how it works with exact files, how it is checked.
The checks section names the clean-context reviewer.
Add a section only when it helps the decision, such as decisions taken, risks, or what stays out of scope.
Keep it readable in one pass: concrete facts the user needs to decide, no template filler, no copy of the plan file.
Write the presentation with the [writing contract](writing.md).
Then ask `Approve`, `Edit`, or `Cancel` with the question tool. Without a question tool, ask in chat and wait for the answer.
Interview answers and the original request do not approve the plan. Do not ask for separate approval before presenting it.
`Edit` returns to the interview or the plan. `Cancel` keeps the saved records and makes no edit.
Native Plan mode approval is the same approval, carried by the `plan-approved` hook. Native Plan mode limits still apply.
Never ask twice for the same presented plan.
A request for analysis, review, or planning alone authorizes no implementation.
Approval carries through implementation, checks, required fixes, review, explanation, and document alignment.
Ask again only for new scope, an unauthorized destructive or external action, or a material unresolved decision.
Specific project limits on production, publishing, commits, protected branches, and tags still apply.

## Choose the path

The path decides the work record and review. State the path and reason before editing.

- **Direct**: one clear, reversible change in an existing flow. Its tests belong to the same change.
- **Bounded**: a clear result across several modules, or a change that needs independent review because of its impact.
- **Full**: decisions need a lasting reason, proof needs design, or work must resume across sessions. Read the [full path](full-path.md).

Authentication, data holding real records, a published contract, or a migration requires at least bounded work and independent review.
Choose the smallest sufficient path. Change paths when new evidence changes the work needed.

### Direct path

Inspect, edit, run the relevant check, and report the result and unchecked limits. No plan, chronicle, or separate reviewer.

### Bounded path

State the approach, affected files, and checks in chat. Apply the authorization rule above.
Implement and verify. Use `staff-review` for the impact signals above; otherwise the pull request review supplies independent review.
No plan file or chronicle is required unless a lasting decision makes the work full.

## Working rules

- Change only the requested scope and necessary dependencies. Preserve unrelated user work.
- Bring modified behavior up to standard, not the whole file. Avoid a worse hybrid with consistent surrounding code.
- Report a pre-existing bug or an unrelated improvement as a follow-up. Never start a spontaneous refactor.
- `refactor` owns an explicitly requested repository convergence audit and selected changes.
- Edit a file in place. Rewrite it whole only when most of it changes.
- For behavior changes, observe a relevant regression test fail before the fix and pass after it when practical.
- A refactor's characterization proof starts green on the unchanged code and must stay green. Never break working behavior for a failure demonstration.
- Add one focused test per stated behavior. Scratch checks stay out of the suite.
- Run required project checks. After they pass, repeat only for new changes, failures, or unresolved concerns.
- Never suppress a failure or weaken proof to claim success. Explain any proposed test removal or replacement before applying it.
- For large mechanical changes, verify a small pilot before scaling.
- Clean up only worktrees you created after merge or discard. Never remove a detached-HEAD harness worktree.
- Commit only when explicitly requested.

## Finish

Complete requested implementation, relevant checks, required review fixes, and affected documentation before reporting completion.
If plans, chronicles, rules, or AGENTS files change, invoke `development-skills:align-docs` in normal mode with the current task.
Also invoke it when documents are created, moved, or removed.
An edit to code, tests, or the content of an existing document skips it unless those changes invalidate documentation.
The skill owns archive moves; the [documentation contract](documentation.md) owns lifecycle metadata.

## Resume

Read an active plan's current step, standards, decisions, and verification record. Continue there instead of restarting discovery.
