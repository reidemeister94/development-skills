# Phase 4: REVIEW + FINALIZE — GATE

Staff review + finalization. The `staff-reviewer` agent is a subagent with independent context, scoped tools, fresh eyes on the diff. Apply [Iron Rules](../iron-rules.md).

## 4a — Staff review (MANDATORY, cannot self-approve)

1. `git diff` — if >500 lines, write to a temp file and pass the path; if >2000 lines, split by component (the `## Task Checklist` file list) into separate reviews, all must pass.
2. Spawn `staff-reviewer` via the Task tool with: task, constraints (from the plan), diff (or path), plan file path, patterns file path(s), Phase 3 verification summary, detected framework.
3. Returns `APPROVED` / `SPEC_ISSUES` / `ISSUES` (file:line). Append `## Review Log` to the plan each cycle; fix → re-verify (Phase 3 Step 4) → re-review until APPROVED.

**Gate:** state **"STAFF REVIEW: APPROVED"**.

## 4b — Chronicle finalization

Created → align with final code, fill "After", set Completed; keep critical user input verbatim (summarize only non-critical input, losslessly). NOT NEEDED → if significant discoveries emerged (check `## Implementation Log`), reconsider a retroactive chronicle. WORKFLOW STATE → `Status: Completed`.

**Gate:** state **"CHRONICLE FINALIZED — [filename]"** (or confirm NOT NEEDED).

## 4c — Capture discoveries + align docs (cannot skip)

Invoke `development-skills:align-docs` and let it run in full — the single discovery-capture + doc-alignment step. It harvests what the session learned (Principle 10) into `AGENTS.md` / `.agents/rules/`, sweeps project facts out of memory into the repo (teammates share only the repo), then cleans and aligns every docs/agents file. Do NOT capture discoveries inline first — that duplicates align-docs.

**Gate:** state **"DISCOVERIES CAPTURED + DOCS ALIGNED — [files] / NONE"**.

## 4d — Integration

Changes on current branch → ask via `AskUserQuestion`: *"Commit now?"* (`Yes, commit now` / `No, I'll handle it (Recommended)`). Commit only on explicit yes, via `development-skills:commit`.

Unmerged worktree branch (rare) → ask how to land: merge locally (checkout base → merge → test → delete branch) · push + `gh pr create` with the plan summary · keep as-is · discard (confirm "discard" first).

State: **"WORKFLOW COMPLETE"**.
