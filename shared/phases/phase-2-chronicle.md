# Phase 2: CHRONICLE — GATE

A chronicle is a **project snapshot** — months later, a reader should understand what the user wanted (in their own words), how the conversation got there, why decisions were made, what was discovered, and what changed. Focus: the intent, the conversation that shaped it, and the *whys* behind the choices.

```
Code + Git = WHAT changed (diffs)
Plan docs  = HOW implemented (tasks, approaches)
Chronicles = WHY it happened, USER INPUT (verbatim + Q&A), PROJECT STATE
```

**When in doubt, create the chronicle.** Cost: ~30 seconds. Cost of missing one: losing the WHY forever.

**Chronicle IS NEEDED when ANY apply:**
- New feature or endpoint
- Architectural change or new patterns
- Complex bug fix requiring investigation
- Breaking change or API modification
- Multi-file refactoring with design decisions
- Business logic where WHY isn't obvious
- Significant research or discovery

**Chronicle NOT NEEDED when ALL apply:**
- Single-line or trivial fix
- No new patterns or architectural decisions
- Change is self-evident from the diff
- No business context worth preserving

Apply [Iron Rules](../iron-rules.md) — especially Principle 10 (document every discovery). Workflow gate discipline (every gate explicit) per `../workflow.md`.

---

## If Chronicle IS Needed

### Create the Chronicle File

1. `mkdir -p docs/chronicles/`
2. Find next number: `ls docs/chronicles/*.md 2>/dev/null | sort | tail -1` — increment (start at 0001)
3. Write using template below
4. Fill: User Input & Conversation, Context, Objective (WHY), Project State (before), Affected Areas

**Naming:** `docs/chronicles/NNNN__YYYY-MM-DD__brief-description.md`

### Template

```markdown
# [Brief Title]

> Chronicle: NNNN__YYYY-MM-DD__brief-description.md
> Status: Draft | In Progress | Completed

## User Input & Conversation (Always Captured)

Preserve what the user actually wrote — enough to understand the task **and how the conversation got there**: their prompts, their answers to the agent's questions, and any other message carrying requirements, constraints, preferences, or course corrections.

**Fidelity rule (graduated):**
- **Critical input** (requirements, constraints, explicit decisions, course corrections, the answer that locked a design choice) — keep in the user's **exact words** (verbatim); never condense.
- **Everything else** — may be summarized, but without losing any useful information (remove noise, never signal).

### Prompts & relevant messages (chronological)

> [in order, so the evolution is visible — verbatim if critical, else a faithful lossless summary]

### Q&A (agent ↔ user)

[one bullet per exchange, in order]
- **Q:** [question the agent asked] → **A:** [user's answer — verbatim when it locks a decision]

### How the understanding evolved

[short narrative: initial ask → what was surfaced → how the user refined it → net result]

## Context

[Background from research. Project state, technical context.]

**Key references:**
- `path/to/module/` - [why involved]

## Project State

**Before:** [State before work]
**After:** [Updated during finalization]

## Objective (The WHY)

[WHY this change. Business context, user needs, problems.]

## Affected Areas

| Area | Files/Modules | Impact |
|------|---------------|--------|
| [Component] | `path/` | [Change] |

## Discoveries & Insights

- **[Date]**: [Discovery or insight]

---

## Agent doc updates

### Updates to apply:

- [ ] `AGENTS.md` - [What to add/update]
```

### Lifecycle

- **Phase 3 (Implement-Verify):** Update Discoveries; record design decisions encountered during implementation.
- **Phase 4 (Review-Finalize):** Align with final code; fill "After" state, set Completed, identify AGENTS.md updates. **Fidelity on finalization:** keep **critical user input verbatim** (prompts, decisions, Q&A) — never condense; summarize only *non-critical* input, losslessly.

**Update WORKFLOW STATE in plan file:** `Chronicle: docs/chronicles/NNNN__YYYY-MM-DD__brief-description.md`, `Current Phase: 3`.

**Gate:** State **"CHRONICLE INITIATED — [filename]"**

---

## If Chronicle NOT Needed

1. Update plan file WORKFLOW STATE: `Chronicle: NOT NEEDED — [reason]`, `Current Phase: 3`.
2. **Gate:** State **"CHRONICLE: NOT NEEDED — [reason]"**

---

## Expected Artifacts

- Chronicle file in `docs/chronicles/` (if needed), OR WORKFLOW STATE annotated with `NOT NEEDED + reason`
- WORKFLOW STATE: `Current Phase: 3`

**→ Proceed immediately to Phase 3. Read `phase-3-implement-verify.md`.**
