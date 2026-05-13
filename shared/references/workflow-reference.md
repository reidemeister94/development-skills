# Workflow Reference

## Skills vs Agents — Use the correct tool

| Name | Type | Tool to use |
|------|------|-------------|
| `development-skills:brainstorming` | **Skill** | `Skill` tool |
| `development-skills:debugging` | **Skill** | `Skill` tool |
| Language skills (`python-dev`, `java-dev`, `typescript-dev`, `swift-dev`, `frontend-dev`) | **Skill** | `Skill` tool |
| `development-skills:staff-reviewer` | **Agent** | `Task` tool |

**Do NOT use the Task tool to invoke Skills. Do NOT use the Skill tool to invoke Agents.**

Implementation and verification run in the main thread per `phases/phase-3-implement-verify.md`.

---

## Key Rules

- **Every phase is a gate.** Do NOT skip or combine phases.
- **The plan file IS the plan.** Present plan summary, ask for approval, gate.
- **After Phase 3, continue to Phase 4.** Do NOT stop after verification.
- **No positive claim without evidence.** *"Should work"* is not verification.
- **Iron Rules:** see `shared/iron-rules.md` (single canonical source).
