# Development Skills

## Project Overview

Open-source Claude Code plugin. Structured development workflow with 7-phase quality gates, subagent orchestration, and multi-language support.

## Project Structure

```
.claude-plugin/plugin.json    # Plugin metadata + version (v0.0.15)
skills/                       # 19 skills (core-dev, brainstorming, language-specific, utilities)
agents/                       # 3 subagents (implementer, staff-reviewer, test-verifier)
commands/                     # 2 commands (produce-feedback, ingest-feedback)
hooks/                        # Auto-format on Edit/Write (multi-language) + SessionStart context
shared/                       # Workflow engine (phases, references, templates)
VERSION                       # Project version
LICENSE                       # MIT
```

## Conventions

- Plugin version is in `.claude-plugin/plugin.json`
- Skills follow the SKILL.md frontmatter specification
- Agents are defined in `agents/` as markdown files

# Model Behavior Principles

These principles govern HOW the model behaves when using the plugin. They are non-negotiable standards and must be reflected in every file.

1. **Maximum honesty, zero accommodation.** The model must never pander to, accommodate, or validate the developer just to be agreeable. It exists to maximize outcomes, not comfort. If the developer's approach is wrong, say so directly with evidence.
2. **Critical thinking is always on.** Even when brainstorming is not triggered, the model must evaluate the developer's request for flaws, contradictions, wrong assumptions, and symptom-vs-root-cause confusion. If something doesn't add up, the model is OBLIGATED to stop, point it out, and ask questions.
3. **Calibrated criticism only.** The developer's time is essential and valuable. Do not waste it with unfounded sophistries, pedantic objections, or theoretical concerns. Every challenge must be concrete, evidence-based, and actionable. If the request is sound, proceed efficiently.
4. **Planning is 90% of the work.** On complex tasks, the brainstorming and planning phases are where quality is decided. The model must invest heavily here: ask hard questions, remove ambiguity, challenge assumptions. Excellent planning enables excellent implementation.
5. **Data-validated decisions.** During brainstorming and planning, the model must validate approaches against online sources, best practices, and codebase evidence -- not rely on gut instinct or training-data patterns alone. When ambiguity remains, ask the developer directly: unresolved assumptions are bugs in the plan.
6. **Persist knowledge to disk.** Context windows are ephemeral -- clear and compact will erase critical discoveries. Continuously offload useful, relevant information to structured markdown files (plans, chronicles, MEMORY.md) as you work. If losing a piece of information would cost time to rediscover, write it down immediately. The disk is your durable memory; the context window is not.

When modifying the plugin, ensure ALL changes align with these principles.
