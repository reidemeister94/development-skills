# Architectural Depth — Shared Lens

For work touching architecture, refactoring, testability, module depth — "many small files doing little", "hard-to-write tests", "one fix changes 8 files". From Ousterhout's *A Philosophy of Software Design* and Feathers' *seam*. Shared by create-test, roast-my-code, and brainstorming. Skip for style/naming/tooling.

## Glossary (use these terms exactly; don't drift)

- **Module** — anything with an interface and an implementation (function, class, package, slice). Scale-agnostic. *Avoid*: unit, component, service.
- **Interface** — everything a caller must know to use the module: types, invariants, ordering, error modes, required config, performance characteristics. *Avoid*: API, signature (type-level only).
- **Implementation** — the body inside. Distinct from *Adapter*: a thing can be a small adapter with a large implementation (Postgres repo) or a large adapter with a small implementation (in-memory fake).
- **Depth** — leverage at the interface: behavior a caller/test can exercise per unit of interface learned. **Deep** = much behavior behind a small interface. **Shallow** = interface ~ as complex as implementation.
- **Seam** *(Feathers)* — a place where you can alter behavior without editing in that place; the location where a module's interface lives. Where to put it is its own decision, distinct from what goes behind it. *Avoid*: boundary (collides with DDD bounded context).
- **Adapter** — a concrete thing satisfying an interface at a seam. Describes *role* (which slot), not substance.
- **Leverage** — what callers get from depth: one implementation pays back across N call sites and M tests.
- **Locality** — what maintainers get: change, bugs, knowledge, verification concentrate in one place. Fix once, fixed everywhere.

## Diagnostics

- **Deletion test** — hypothesize deleting a suspiciously shallow module. If complexity reappears across callers, it earns its keep (a real seam) — leave it. If complexity vanishes, it's a pass-through to inline.
- **Interface is the test surface** — callers and tests cross the same seam. Tests that mock internal deps, inspect private state, or break after a behavior-preserving refactor mean the interface is too narrow or the seam is misplaced.
- **One adapter = hypothetical, two = real** — an interface + 1 implementation with no fake/alt-impl and no concrete second on the roadmap: drop the interface, use the concrete type.
- **Depth is a property of the interface, not the implementation** — a deep module may be internally composed of small swappable parts (internal seams used by its own tests) that aren't part of its interface.

## Output

For each architectural candidate: files involved, the friction (in glossary terms), diagnosis (current depth, where the real seam lives, why it's shallow/misplaced), refactor direction in plain English (leverage and locality gained), tests that would become natural. **Do not propose concrete signatures here** — only flag friction so the owner picks what to explore.

## Rejected framings

- **Depth as implementation-lines / interface-lines ratio** (Ousterhout's original): rewards padding the implementation. Use **depth-as-leverage**.
- **"Interface" = the TS `interface` keyword or a class's public methods**: too narrow; interface includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD bounded context — say **seam** or **interface**.

## Cross-link

- Designing new interfaces: `skills/brainstorming/references/design-it-twice.md`.
