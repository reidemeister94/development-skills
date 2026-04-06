# Contributing to development-skills

Thanks for your interest in improving the plugin. Here's how to contribute effectively.

## The Golden Rule

**No PR is accepted without a regression eval benchmark proving zero regressions.**

This plugin enforces discipline on AI agents — we hold ourselves to the same standard. Every PR must include a `skill-creator` regression report showing that the proposed changes don't degrade any existing behavior. This is non-negotiable.

## Getting Started

1. Fork the repository
2. Install the [`skill-creator`](https://github.com/anthropics/claude-plugins-official) plugin (required):
   ```json
   // ~/.claude/settings.json
   {
     "enabledPlugins": {
       "skill-creator@claude-plugins-official": true
     }
   }
   ```
3. Clone and test locally:
   ```bash
   claude --plugin-dir ./development-skills
   ```
4. Make your changes
5. Run the regression eval suite (see below)
6. Open a PR with the benchmark results

## Regression Testing with skill-creator

The plugin ships with **27 evals and 89 assertions** covering 10 behavioral dimensions. These are the project's test suite — the equivalent of unit tests for a skill-based system.

### Eval Categories

| Category | Evals | What It Tests |
|----------|-------|--------------|
| `brainstorming-guard` | 7 | Triggers brainstorming when needed, skips when appropriate |
| `smart-isolation` | 6 | Parallel vs single agent decisions, worktree safety |
| `anti-rationalization` | 4 | Resists shortcuts, catches flawed premises |
| `workflow-phases` | 3 | Phase progression, resumption, plan discovery |
| `implementer-discipline` | 2 | TDD, caller updates, verification honesty |
| `language-detection` | 1 | Frontend vs TypeScript backend routing |
| `chronicle-quality` | 1 | WHY documentation quality |
| `askuserquestion-avoidance` | 1 | Uses conversational text, not AskUserQuestion tool |
| `turn-boundary` | 1 | Stops at the right moment, doesn't overflow turns |
| `project-directives` | 1 | Respects existing project directives |

### Running the Full Regression Suite

Use the `/eval-regression` skill or run manually with `skill-creator`:

```
/eval-regression
```

This will:
1. **Snapshot** the current committed version as baseline
2. **Execute** all 27 evals against both baseline and your modified version
3. **Grade** each eval's assertions (pass/fail with evidence)
4. **Compare** results and generate a regression report
5. **Verdict**: `SAFE TO COMMIT` or `REGRESSIONS FOUND`

### Workspace Layout

```
plugins/
├── development-skills/              # Your plugin (modified)
│   └── evals/
│       └── evals.json               # Eval definitions (27 evals, 89 assertions)
└── development-skills-workspace/    # Created by skill-creator (gitignored)
    ├── skill-snapshot/              # Baseline snapshot
    └── iteration-N/
        ├── eval-{ID}/
        │   ├── eval_metadata.json   # {eval_id, eval_name, prompt, expectations}
        │   └── with_skill/
        │       ├── outputs/         # transcript.md + generated files
        │       └── grading.json     # {expectations: [{text, passed, evidence}], summary}
        ├── benchmark.json           # Machine-readable results
        └── benchmark.md             # Human-readable report
```

### What the PR Must Include

1. **`benchmark.md`** — paste the human-readable report in the PR description
2. **Pass rate** — must be 100% on all existing assertions (zero regressions)
3. **New evals** — if your change adds a skill or modifies routing, add evals that test the new behavior

### Adding New Evals

If your PR adds a skill or changes behavior, you must add corresponding evals to `evals/evals.json`:

```json
{
  "id": 28,
  "name": "your-eval-name",
  "category": "brainstorming-guard",
  "prompt": "The exact user prompt to test",
  "expected_output": "What should happen (for grader context)",
  "assertions": [
    {
      "description": "What this assertion checks",
      "pass_criteria": "Specific, verifiable condition"
    }
  ],
  "files": []
}
```

**Guidelines for good evals:**
- Test the **routing decision**, not the full implementation (evals stop after first routing)
- Each assertion should check one specific behavior
- `pass_criteria` must be unambiguous — a grader should be able to judge pass/fail without context
- Use `files` array to inject context files the eval needs (plan files, project configs)
- Choose the right `category` from the existing set

## What to Contribute

**High-impact contributions:**
- New language skills (Rust, Go, Kotlin, Ruby, C#) — see the issue template
- Improved patterns for existing languages
- Better anti-rationalization tables
- New evals for uncovered edge cases
- Bug reports with reproduction steps

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

## Pull Request Checklist

- [ ] Ran `/eval-regression` — all 27 evals pass (zero regressions)
- [ ] `benchmark.md` pasted in PR description
- [ ] New evals added for any new or modified behavior
- [ ] One concern per PR
- [ ] Clear description of what changed and why

## Code of Conduct

Be constructive. We're building tools that enforce quality — let's hold ourselves to the same standard.
