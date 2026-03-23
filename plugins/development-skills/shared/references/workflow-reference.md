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

## Anti-Rationalization Check

| Your thought | Reality |
|---|---|
| "This is simple enough to skip planning" | Simple-looking changes cause the hardest bugs. Follow the workflow. |
| "TaskCreate is basically a plan" | TaskCreate tracks progress. EnterPlanMode creates the plan. NOT interchangeable. |
| "The user didn't ask for a plan" | IRRELEVANT. The workflow requires it regardless (Phase 2). |
| "I know the tasks, I'll start implementing" | Phase 4 REQUIRES updating the plan doc with Task Checklist BEFORE spawning implementer. |
| "Implementation is complete, I can summarize now" | After Phase 4, you MUST continue through Phases 5, 6, 7. Do NOT stop. |

**Also check your language skill's anti-rationalization table.** If you recognized your reasoning in any table, you are rationalizing. Go back and follow the workflow.
