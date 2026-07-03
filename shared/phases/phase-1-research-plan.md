# Phase 1: RESEARCH + PLAN — GATE

Apply [Iron Rules](../iron-rules.md). Knowledge-first: check disk → fill gaps in an isolated subagent (raw results stay there) → write plan to disk → lock HOW-level ambiguities → gate.

## Step 1 — Load existing research
Check the plan's WORKFLOW STATE for `Research:` → read `docs/plans/NNNN__research__{slug}.md` if present; do not repeat covered searches.

## Step 2 — Read patterns + clarify
Read ALL pattern files from the skill's config. Ask focused questions if unclear; for non-trivial tasks, ask which existing patterns NOT to follow and which legacy workarounds to avoid. Record answers under `## Clarifications` (Q / A / Impact).

## Step 3 — Fill research gaps
Identify missing implementation/library/API/codebase knowledge. No gaps → state **"RESEARCH OK — leveraging `[file]`"**. Gaps or multiple possible valid approaches → dispatch an isolated subagent (`model: opus`) per `../agents/research-agent.md` and then read the results.

## Step 4 — Write the plan
Instantiate `../templates/plan-template.md` (canonical schema, including the Global Constraints block and the HOW-locks table). Fill Global Constraints with the project-wide invariants this change must not break, copied verbatim (or `N/A: none`) — Phase 3 scans against them and Phase 4a hands them to the reviewer. Set WORKFLOW STATE: Status, Current Phase, Phases remaining, Research path, Chronicle (TBD — Phase 2), Verification commands.

## Step 5 — HOW-level locks (MANDATORY)
Fill the plan-template HOW-locks table, one row each: **edge cases · data shapes · error semantics · contract boundaries · test scope · rollback.** Lock each or write `N/A: reason` — never blank, never guess, pick the simplest answer. Unknowns → display as plain text and STOP (`AskUserQuestion` for a discrete 2-4 pick).

## Step 6 — Present + gate
Display a 6-10 line summary: scope · approach · files to touch · locks status · verification strategy · key risk. Ask **"Approve the plan and proceed?"** via `AskUserQuestion` — always selectable, never typed approval (`Approve (Recommended)` / `Edit` / `Chat about`). WAIT for explicit approval (non-yes detection per brainstorming Step 8). On approval: WORKFLOW STATE → `Current Phase: 2`. If implementation later reveals the plan won't work, STOP, return here, re-approve.

**Gate:** state **"RESEARCH + PLAN COMPLETE — APPROVED"**. → Read `phase-2-chronicle.md`.
