# Contributing to development-skills

Thanks for your interest in improving the plugin. Here's how to contribute effectively.

## The Golden Rule

**Every change aligns with the Iron Rules.** This plugin enforces discipline on AI agents — we hold ourselves to the same standard. Reason from first principles, favor simplicity, and make each change trace to a clear need.

## Getting Started

1. Fork the repository
2. Clone and test locally:
   ```bash
   claude --plugin-dir ./development-skills
   ```
3. Make your changes following the Iron Rules (see below)
4. Open a PR with a clear description of what changed and why

## What to Contribute

**High-impact contributions:**
- New language skills (Rust, Go, Kotlin, Ruby, C#) — see the issue template
- Improved patterns for existing languages
- Better anti-rationalization tables
- Bug reports with reproduction steps

**Before starting work:** open an issue to discuss the approach. This prevents duplicate effort and ensures alignment with the project's philosophy.

## Skill Structure

Each skill is a directory under `skills/`:
```
skills/
  your-skill/
    SKILL.md          # Required: YAML frontmatter + body
    references/       # Optional: detailed material loaded on demand (subdir)
    patterns.md       # Optional: language-specific patterns (single file convention used by python-dev, java-dev, typescript-dev, swift-dev)
```

The `SKILL.md` must include:
- YAML frontmatter with `name` (matches directory name) and `description` (the trigger contract — lead with "Use when …" and list explicit keyword triggers)
- A markdown body — no mandatory section headings; aim for ≤ 200 lines (push longer material into `references/`)
- For language skills: verification commands (test / lint / build), implementation rules, quality checklist

Look at `skills/python-dev/SKILL.md` for a language-skill reference and `skills/using-development-skills/SKILL.md` for a workflow-skill reference.

## Design Principles

All changes must align with the canonical Iron Rules — **13 principles (0-12) + 1 meta-rule (spirit beats letter)** — in [`shared/iron-rules.md`](shared/iron-rules.md). The principles apply to every skill, agent, and phase. Particularly load-bearing when contributing:

- **Principle 0 (don't pander)** — skills must make the model challenge wrong approaches, not defer to user confirmation as validation
- **Principle 3 (simplicity by default)** — refuse to add a new file / abstraction / config / dependency when an existing mechanism covers >50% of the need
- **Principle 8 (no claim without fresh evidence)** — verify outcomes against actual run output, not assumed behavior
- **Principle 10 (document every discovery)** — non-trivial decisions in PRs go in `docs/chronicles/`, not just in commit messages
- **Principle 7 (TDD: Red → Green → Refactor)** — new behavior is paired with a failing test before the code is written

## Pull Request Checklist

- [ ] Changes align with the Iron Rules
- [ ] One concern per PR
- [ ] Clear description of what changed and why

## Code of Conduct

Be constructive. We're building tools that enforce quality — let's hold ourselves to the same standard.
