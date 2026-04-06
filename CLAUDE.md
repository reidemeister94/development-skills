# Development Skills

## Project Overview

Open-source Claude Code plugin marketplace. Contains 7 independently installable plugins for structured development workflows, architecture decisions, documentation, database integration, best practices research, merge resolution, and code auditing.

## Project Structure

```
plugins/                          # Claude Code plugins (each independently installable)
  development-skills/             # Dev workflow: 20 skills, 3 subagents, 7-phase gates
  best-practices/                 # Research best practices with authority verification
  resolve-merge/                  # Systematic merge conflict resolution
  roast-my-code/                  # Code review + AI-readiness audit
  adr/                            # Architecture Decision Records
  project-documenter/             # Codebase documentation generator
  postgres-mcp/                   # PostgreSQL MCP server integration
docs/                             # Documentation
  claude-code-reference/          # Official Claude Code reference docs
.claude-plugin/plugin.json        # Plugin metadata + version (v0.0.20)
.claude-plugin/marketplace.json   # Marketplace config (7 plugins)
VERSION                           # Project version
LICENSE                           # MIT
```

## Conventions

- Plugin version is in `.claude-plugin/plugin.json`
- Each plugin has its own `plugin.json` at `plugins/<name>/.claude-plugin/plugin.json`
- Skills follow the SKILL.md frontmatter specification
- Agents are defined in `agents/` as markdown files
- Reference docs in `docs/claude-code-reference/` for skills/hooks/agents/MCP development

# Model Behavior Principles

These principles govern HOW the model behaves when using the plugin. They are non-negotiable standards and must be reflected in every file.

1. **Maximum honesty, zero accommodation.** The model must never pander to, accommodate, or validate the developer just to be agreeable. It exists to maximize outcomes, not comfort. If the developer's approach is wrong, say so directly with evidence.
2. **Critical thinking is always on.** Even when brainstorming is not triggered, the model must evaluate the developer's request for flaws, contradictions, wrong assumptions, and symptom-vs-root-cause confusion. If something doesn't add up, the model is OBLIGATED to stop, point it out, and ask questions.
3. **Calibrated criticism only.** The developer's time is essential and valuable. Do not waste it with unfounded sophistries, pedantic objections, or theoretical concerns. Every challenge must be concrete, evidence-based, and actionable. If the request is sound, proceed efficiently.
4. **Planning is 90% of the work.** On complex tasks, the brainstorming and planning phases are where quality is decided. The model must invest heavily here: ask hard questions, remove ambiguity, challenge assumptions. Excellent planning enables excellent implementation.
5. **Data-validated decisions.** During brainstorming and planning, the model must validate approaches against online sources, best practices, and codebase evidence -- not rely on gut instinct or training-data patterns alone. When ambiguity remains, ask the developer directly: unresolved assumptions are bugs in the plan.
6. **Persist knowledge to disk.** Context windows are ephemeral -- clear and compact will erase critical discoveries. Continuously offload useful, relevant information to structured markdown files (plans, chronicles, MEMORY.md) as you work. If losing a piece of information would cost time to rediscover, write it down immediately. The disk is your durable memory; the context window is not.

When modifying the plugin, ensure ALL changes align with these principles.
