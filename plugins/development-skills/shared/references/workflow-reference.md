# Workflow Reference

## Skills vs Agents — Use the correct tool

| Name | Type | Tool to use |
|------|------|-------------|
| `development-skills:brainstorming` | **Skill** | `Skill` tool |
| `development-skills:debugging` | **Skill** | `Skill` tool |
| Language skills (`python-dev`, `java-dev`, etc.) | **Skill** | `Skill` tool |
| `development-skills:implementer` | **Agent** | `Task` tool |
| `development-skills:test-verifier` | **Agent** | `Task` tool |
| `development-skills:staff-reviewer` | **Agent** | `Task` tool |

**Do NOT use the Task tool to invoke Skills. Do NOT use the Skill tool to invoke Agents.**

---

## Key Rules

- **Every phase is a gate.** Do NOT skip or combine phases.
- **TaskCreate is NOT a plan.** Use EnterPlanMode for plans.
- **After Phase 4, continue through 5, 6, 7.** Do NOT stop after implementation.
- **No positive claim without evidence.** "Should work" is not verification.
