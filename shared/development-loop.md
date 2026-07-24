# Development loop

Build the smallest change that reaches an agreed result. Start from evidence, question the premise, and keep facts separate from interpretations.

Never hide failure by skipping a gate, suppressing a test, or swallowing a warning. All natural-language text follows the [writing contract](writing.md). When rules conflict, choose the result a critical reader would find less surprising.

On Claude Code, call `AskUserQuestion` whenever the user must choose among stated options. Printing choices in chat does not satisfy this rule. On Codex, ask one concise question in chat; do not depend on an interactive input tool.

## Standards gate

For every codebase task, before the first codebase mutation, read the project's agent instructions and all matching scoped rules. Inspect nearby code for established local patterns, load any conventions the project defines, and state the selected source paths. A Full plan records the same exact paths.

Apply sources in this order: the current explicit user decision; project instructions and scoped rules; shared project conventions and named standards of record; established local patterns; model defaults. Read a named reference project only when the higher sources leave an important choice unresolved. If the target differs from a higher standard, state the effect instead of silently spreading the divergence.

Normal work changes only the task's files and necessary dependencies. A repository-convergence or standards-alignment task is the explicit exception and may audit and refactor the whole target.

## Choose the path

Use the direct path only when the result, solution, and proof are clear, the change is easy to reverse, and no business or design choice remains. Choosing among viable approaches is a design choice. Inspect, change, verify, report.

Use the full path for everything else. Uncertainty about the path means full.

State the path and why before the first mutation. A requested review or audit ends with findings; edit only after explicit approval. If an approval gate is unreachable, stop rather than downgrading full to direct.

## Full path

### 1. Decide

Inspect before asking. State the problem, affected user or system, solved state, constraints, unknowns, and what would show the proposed answer is wrong.

Use `brainstorming` to reach a deep and complete agreement with the user about all the aspects of the work, unless the change is easy to reverse, needs little work, has one forced approach, and its reason cannot affect the implementation. A request, spec, or guide supplies inputs but may not settle the approach.

Ask one decision at a time and recommend an answer.

### 2. Define the proof

Agree on what could expose failure. For non-trivial tasks, business flows, KPIs, deep integrations, or probabilistic behavior, use `create-test` to design the regression proof.

### 3. Express

Research only when external evidence or an unanswered question can change the decision. Record the result in `docs/plans/NNNN__research__<slug>.md` only when it will remain useful after the task.

Before product or plugin edits, write a plan that settles the implementation choices at `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__<slug>.md`. Start `docs/chronicles/NNNN__YYYY-MM-DD__<topic>.md` at the same time.

Use the next folder prefix and the [plan](templates/plan-template.md) and [chronicle](templates/chronicle-template.md) templates. A plan first explains why the work matters and how the solution will work, then records exact tasks and checks. A chronicle explains what was learned, what was decided and why, and what changed. Translate the template headings into the repository's documentation language when needed.

Record user intent faithfully. Follow the writing contract's language rule, and keep valuable or specific company, project, and workflow information verbatim.

Present six short parts in the conversation language: result, checks, what is out of scope, approach, files, and risks. Then offer the conversation-language equivalents of `Approve / Edit / Cancel / Chat about` through the platform behavior above. Only `Approve` after this presentation permits implementation; the original task request does not.

### 4. Implement

Work in small slices and run the nearest useful check after each. When a test can prove behavior, observe it fail before the fix and pass afterward. Delete production code written before its test instead of adapting it.

Follow the recorded standards and quality contract. Record discoveries that change the plan.

### 5. Verify

Run fresh outcome checks and repository gates. Recheck changed code against the recorded standards and quality contract. Use checks that could fail if the claim were false. Fix root causes; never weaken, skip, or suppress a check to claim success.

Report pre-existing failures. After three failed fixes, question the approach. Say what was not checked.

### 6. Explain diff

When the change contains a business, architecture, lifecycle, trade-off, or failure-mode concept worth teaching, run `explain-diff` with the request, plan or chronicle, diff, verification, and what was not checked.

Teach the mental model, then ask free-response questions one at a time; zero is valid. A conscious skip remains unverified but does not block Review. If no concept qualifies, state that and continue.

### 7. Review

Give an independent reviewer the request, plan, standards, diff, and what verification did and did not cover. Do not give them quiz answers or `explain-diff` interpretations.

Fix all CRITICAL/HIGH findings and rerun affected checks. If review changes an essential concept, repeat its verification and the part of the explanation that is now stale. Then finalize the plan and chronicle and invoke `align-docs` in normal mode with the current task context; it captures lasting discoveries, aligns docs, and archives documents made obsolete, superseded or historical by this task. Commit only when explicitly requested.

## Working rules

- Everything you write or say in natural language, follows the [writing contract](writing.md)
- Documentation follows the [repository documentation format](documentation.md).
- Keep code simple, efficient and clear. Functions and methods have one responsibility, no side effects and at most 70 lines. Use simple, descriptive names for files, types, functions, variables, and arguments.
- Give each behavior one owner. Reuse or extract real duplication; do not abstract coincidental similarity.
- Choose the lowest practical time and space complexity for the real workload while preserving correctness and clarity. Measure hot paths before adding complex optimizations.
- For database work, optimize each statement and its access pattern. Profile tables, schemas, queries. Never write single queries inside loop when you can batch them and make them fast and efficient.
- Remove any line or component whose deletion loses no useful behavior.
- When refactoring, the objective is to become clearer, more efficient, reliable, or maintainable.
- Change only what traces to the request; preserve unrelated user work.
- Comments explain non-obvious functional, business, or technical reasons, not what the code already says.
- User approval validates proceeding, not the analysis — a wrong analysis still owes a correction. No flattery openers; demonstrate merit with evidence, not adjectives.
- Say each rule once in its owner. Remove only what the current model already knows or would do unprompted. Keep examples that carry a real requirement and every project- or team-specific fact. Use `simplify-stuff` for deep passes over existing files.
- Explanations include the intuition, how the change works, trade-offs, and evidence.
- No material claim without evidence that could have proved it false.
- A failed proof or new unknown returns to the earliest step it invalidates.
- For large mechanical changes, verify a small pilot before scaling.
- Skipping, deleting, or re-baselining a test needs explicit user approval.
- Clean up only worktrees you created and only after merge or discard. Never remove a detached-HEAD harness worktree.

## Resume

An in-progress plan is the persistent state. Read its current step, standards, chronicle, and verification record; continue there instead of restarting discovery.
