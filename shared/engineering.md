# Engineering

Preserve useful behavior and project constraints. Prefer deleting unnecessary code, then simplifying, then optimizing, then automating.

## Design and data

Check why an existing constraint exists before removing it. An unusual retry or nullable field might preserve a real requirement.
Name domain terms precisely. Resolve conflicting meanings through a concrete case before changing the model.
Use types that prevent invalid states. Normalize data when it prevents a real update error.
Derive values instead of storing duplicate state when the derivation remains correct.

An interface includes invariants, ordering, errors, configuration, and cost, as well as its signature.
Keep behavior behind the smallest useful interface and test through that interface where possible.
Give each behavior one owner. Extract real duplication; do not generalize coincidental similarity or hypothetical future needs.
Before removing a component, inspect its callers. Remove it when its deletion removes complexity without losing needed behavior.

## Cost and dependencies

Choose the lowest practical time and space cost for the real workload while keeping the code clear and correct.
Measure a performance claim with the same workload before and after the change.
Batch database work when possible. Inspect query access paths; add indexes for actual filters or joins.
Add a cache, queue, worker, or service only for an established requirement. State the need it serves.

Before adding a dependency, check existing language, framework, and project capabilities.
Check maintenance, compatibility, security, and ownership. Low popularity or a quiet release history alone does not prove poor quality.

## Functions and explanations

Use one responsibility per function or method, at most 70 lines, and simple descriptive names.
Separate side effects from calculations when that separation makes behavior easier to test and maintain.
Comments state a non-obvious functional, business, or technical reason, rather than repeat the code.
Record decisions that future maintainers need to understand; keep routine implementation details in the code.
