# Skill authoring

Keep guidance that changes a capable agent's decisions: project conventions, operational constraints, fragile procedures, and task-specific knowledge.
For every skill, reference, example, or line:

1. Delete it if no useful capability or fact is lost.
2. Merge duplication into its existing owner.
3. Simplify what remains with the [writing contract](writing.md).

Descriptions state the capability and its specific trigger. Preserve manual invocation policies unless the user changes them.
A short skill can stay self-contained. Split references only when a task can skip substantial detail.
Link each reference where its information becomes relevant. Inspect callers before moving or deleting it.
Use fixed steps for fragile operations; otherwise state the result, constraints, and completion checks.
An existing user authorization remains valid. Skill selection does not authorize external actions.

Stable project conventions belong in project rules or references; skills own workflows and task exceptions.
Validate packaging, links, and relevant behavior. Tests must protect outcomes and real contracts, not incidental wording.
