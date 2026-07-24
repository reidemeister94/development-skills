# Contributing to development-skills

Thanks for your interest in improving the plugin. Here's how to contribute effectively.

## The Golden Rule

**Every change aligns with the development loop.** This plugin enforces discipline on AI agents — we hold ourselves to the same standard. Reason from first principles, favor simplicity, and make each change trace to a clear need.

## Getting Started

1. Fork the repository
2. Clone and test locally:
   ```bash
   claude --plugin-dir ./development-skills
   ```
3. Make your changes following the development loop (see below)
4. Open a PR with a clear description of what changed and why

## What to Contribute

**High-impact contributions:**
- New skills that add a genuinely missing capability — see the issue template
- Sharper workflow steps or clearer gates
- Better anti-rationalization tables and reference material
- Bug reports with reproduction steps

**Before starting work:** open an issue to discuss the approach. This prevents duplicate effort and ensures alignment with the project's philosophy.

## Skill Structure

Each skill is a directory under `skills/`:
```
skills/
  your-skill/
    SKILL.md          # Required: YAML frontmatter + body
    references/       # Optional: detailed material loaded on demand (subdir)
```

The `SKILL.md` must include:
- YAML frontmatter with `name` (matches directory name) and `description` (the trigger contract — lead with "Use when …" and list explicit keyword triggers)
- A markdown body — no mandatory section headings; aim for ≤ 200 lines (push longer material into `references/`)

Look at `skills/using-development-skills/SKILL.md` for a workflow-skill reference, and [`shared/skill-authoring.md`](shared/skill-authoring.md) for the reduce-gate every new or edited skill must pass.

## Design Principles

All changes must align with the development loop and its principles in [`shared/development-loop.md`](shared/development-loop.md). They apply to every skill and agent. Particularly load-bearing when contributing:

- **Don't pander** — skills must make the model challenge wrong approaches, not defer to user confirmation as validation.
- **Simplicity by default** — refuse to add a new file, abstraction, config, or dependency when an existing mechanism covers most of the need.
- **No claim without fresh evidence** — verify outcomes against actual run output, not assumed behavior.
- **Document every discovery** — non-trivial decisions in PRs go in `docs/chronicles/`, not just in commit messages.
- **Test first** — new behavior is paired with a failing test before the code is written.

## Pull Request Checklist

- [ ] Changes align with the development loop
- [ ] One concern per PR
- [ ] Clear description of what changed and why

## Code of Conduct

Be constructive. We're building tools that enforce quality — let's hold ourselves to the same standard.
