# {Name of the project}

## Principles to always follow

Think critically from first principles and prefer the smallest clear solution. Preserve the requested result, maintainability, and quality; remove everything that does not help them.

- Use the `development-skills` plugin for project work. If it is unavailable, tell the user how to install it.
- Inspect before deciding. For consequential work, agree on the result and its proof, then record the plan and decision chronicle before implementation.
- Follow this project's established patterns. Add a dependency, abstraction, file, or rule only when removing it would cause a real failure.
- Fix root causes. Never hide a failure with skipped checks, swallowed errors, or unsupported claims.
- Verify with fresh evidence and state what remains unobserved.
- Store durable discoveries in the repository: brief critical facts here, deeper topic rules in `.agents/rules/`, decisions in `docs/chronicles/`, and procedures in `docs/plans/`.
- Keep `AGENTS.md` near 70 lines, shared artifacts in English, and personal machine facts in ignored local files.
- Communicate in simple, precise language. Cut filler, not necessary information.
