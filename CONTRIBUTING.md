# Contributing to development-skills

Thanks for your interest in improving the plugin. Here's how to contribute effectively.

## Getting Started

1. Fork the repository
2. Clone and test locally:
   ```bash
   claude --plugin-dir ./development-skills
   ```
3. Make changes — the plugin is markdown-based, no build step needed
4. Test by running Claude Code with `--plugin-dir` pointing to your fork
5. Open a PR against `main`

## What to Contribute

**High-impact contributions:**
- New language skills (Rust, Go, Kotlin, Ruby, C#) — see the issue template
- Improved patterns for existing languages
- Bug reports with reproduction steps
- Documentation improvements

**Before starting work:** open an issue to discuss the approach. This prevents duplicate effort and ensures alignment with the project's philosophy.

## Skill Structure

Each language skill follows this pattern:
```
skills/
  your-skill/
    SKILL.md          # Frontmatter + instructions
    references/       # Optional reference files
    patterns/         # Optional pattern files
```

The `SKILL.md` must include:
- YAML frontmatter with `name`, `description`, `user-invocable`
- Verification commands (test, lint, build)
- Language-specific implementation rules
- Quality checklist

Look at `skills/python-dev/SKILL.md` as a reference implementation.

## Design Principles

All changes must align with the [Model Behavior Principles](CLAUDE.md):

1. **Maximum honesty, zero accommodation** — skills should make the model challenge wrong approaches
2. **Critical thinking is always on** — never skip evaluation
3. **Planning is 90% of the work** — invest in brainstorming and planning phases
4. **Persist knowledge to disk** — context windows are ephemeral

## Pull Request Guidelines

- One concern per PR
- Include a clear description of what changed and why
- If adding a new skill, include example prompts that trigger it
- Run the plugin locally and verify your changes work

## Code of Conduct

Be constructive. We're building tools that enforce quality — let's hold ourselves to the same standard.
