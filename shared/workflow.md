# Mandatory Development Workflow

Two tiers. PASS_THROUGH (trivial, 1-file, no design choice) is triaged in `skills/using-development-skills/SKILL.md` and bypasses both. [Iron Rules](iron-rules.md) apply across tiers and phases — referenced, never duplicated. Every gate must be explicitly passed; the plan file is the persistent record, updated as each phase completes.

## Tier selection

- **LIGHT** — mechanical change: one forced approach, no logic/business/architecture impact, no new pattern, no chronicle-worthy knowledge. 6-step inline (below).
- **FULL** — everything else. 4 gated phases, plan-file-backed.

Default on uncertainty → FULL.

**Formatting (every tier, incl. PASS_THROUGH):** apply the language skill's formatter (`ruff format`, Biome/Prettier, etc.) after editing code, before claiming done.

## LIGHT — inline 6-step

1. **Detect language inline** (`.py`→python, `.java`→java, `.swift`→swift, frontend signals→frontend, `.ts`+`tsconfig.json`→typescript; markdown/config-only → skip step 2).
2. **Read `skills/{lang}-dev/patterns.md`** + its verification commands. Reference only — do NOT invoke the language skill (its chain is FULL).
3. **One-paragraph sketch + single gate:** WHAT changes, WHICH files, VERIFY command, one-line risk-or-N/A. Then `AskUserQuestion`: Proceed (Recommended) / Modify / Escalate to FULL.
4. **Implement + verify inline** with fresh evidence.
5. **Iron-Rules walk against the diff.** Any "no" → fix → re-verify. Diff touches `plugins/**` or any `SKILL.md` → also apply the [`skill-authoring.md`](skill-authoring.md) reduce-gate.
6. **Done** — state "LIGHT WORKFLOW COMPLETE" with evidence.

**Escalate to FULL** the moment any of: a design/business/logic choice surfaces, `AGENTS.md`/`.agents/rules/` needs updating, verification fails twice. Materialize the sketch into `docs/plans/NNNN__YYYY-MM-DD__implementation_plan__<slug>.md` and resume at Phase 1.

## FULL — 4 phases, each a GATE

Read each via `Glob("**/development-skills/shared/phases/phase-*.md")`. Implementation + verification run in the main thread. After each gate, proceed to the next phase — except Phase 1 (plan approval) and Phase 4d (commit choice).

| Phase | Gate statement | File |
|---|---|---|
| 1 Research + Plan | "RESEARCH + PLAN COMPLETE — APPROVED" | `phases/phase-1-research-plan.md` |
| 2 Chronicle | "CHRONICLE INITIATED" / "NOT NEEDED" | `phases/phase-2-chronicle.md` |
| 3 Implement + Verify | "IMPLEMENT + VERIFY COMPLETE" + evidence | `phases/phase-3-implement-verify.md` |
| 4 Review + Finalize | "WORKFLOW COMPLETE" | `phases/phase-4-review-finalize.md` |

No skipping/combining phases, no substituting the plan with another artifact, no coding before plan approval, no commit unless the user explicitly asks.

## Tools

`staff-reviewer` is an **Agent** (`Task` tool). `brainstorming`, `debugging`, and the language skills are **Skills** (`Skill` tool). Never cross them.

## User interaction

Any discrete choice — including approvals and gates → `AskUserQuestion` (auto-resolves inside Task subagents — never call from `staff-reviewer` prompts; Codex → numbered list + STOP per `skills/using-development-skills/references/codex-tools.md`). Plain text + STOP only for genuinely open-ended answers with no options, one at a time.

## Context compaction & handoff

On auto-compression or `/clear`, the plan file is the persistent record (don't prescribe `/compact` — context is the user's prerogative). Auto-recovery: read the plan's `## WORKFLOW STATE` → language skill config → re-read this file + the current phase file. Cross-session handoff to a new chat: `development-skills:handoff`.
