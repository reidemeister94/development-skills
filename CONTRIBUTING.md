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

The plugin ships with **25 evals and 94 assertions** covering 10 behavioral dimensions. These are the project's test suite — the equivalent of unit tests for a skill-based system.

### Eval Categories

| Category | Evals | What It Tests |
|----------|-------|--------------|
| `anti-rationalization` | 5 | Resists shortcuts, catches flawed premises, meta-rule (spirit beats letter) adherence |
| `brainstorming-guard` | 5 | Triggers brainstorming when needed, skip-conditions, user-bypass |
| `implementer-discipline` | 3 | TDD vertical slicing, 5-step verification gate, no horizontal slicing |
| `workflow-phases` | 3 | Phase progression, WORKFLOW STATE recovery, chronicle IS/NOT NEEDED, Phase 4 integration |
| `anti-sycophancy` | 2 | Principle 0 — no flattery, evidence over confirmation |
| `brainstorming-internal-runtime` | 2 | Hypothesis + numeric Confidence, Q+GUESS+CONFIDENCE calibration |
| `workflow-tier` | 2 | Triage tiers including 1-file FULL borderline, LIGHT escalation |
| `brainstorming-sota` | 1 | Design-it-twice, 6-line restate, plan-mode-style outline, non-yes detection |
| `create-test` | 1 | Specialized route for test-design tasks |
| `language-detection` | 1 | Frontend > TypeScript routing |

### Running the Full Regression Suite

Use the `/eval-regression` skill or run manually with `skill-creator`:

```
/eval-regression
```

This will:
1. **Snapshot** the current committed version as baseline
2. **Execute** all 25 evals against both baseline and your modified version
3. **Grade** each eval's assertions (pass/fail with evidence)
4. **Compare** results and generate a regression report
5. **Verdict**: `SAFE TO COMMIT` or `REGRESSIONS FOUND`

### Workspace Layout

```
plugins/
├── development-skills/              # Your plugin (modified)
│   └── evals/
│       └── evals.json               # Eval definitions (25 evals, 94 assertions)
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
  "id": 26,
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

All changes must align with the canonical Iron Rules — **14 principles (0-13) + 1 meta-rule (spirit beats letter)** — in [`shared/iron-rules.md`](shared/iron-rules.md). The principles apply to every skill, agent, and phase. Particularly load-bearing when contributing:

- **Principle 0 (don't pander)** — skills must make the model challenge wrong approaches, not defer to user confirmation as validation
- **Principle 3 (simplicity by default)** — refuse to add a new file / abstraction / config / dependency when an existing mechanism covers >50% of the need
- **Principle 8 (no claim without fresh evidence)** — every eval must verify outcomes against actual run output, not assumed behavior
- **Principle 10 (document every discovery)** — non-trivial decisions in PRs go in `docs/chronicles/`, not just in commit messages
- **Principle 7 (TDD: Red → Green → Refactor)** — new skill behavior is paired with a failing eval before the skill is written

## Pull Request Checklist

- [ ] Ran `/eval-regression` — all 25 evals pass (zero regressions)
- [ ] `benchmark.md` pasted in PR description
- [ ] New evals added for any new or modified behavior
- [ ] One concern per PR
- [ ] Clear description of what changed and why

## Code of Conduct

Be constructive. We're building tools that enforce quality — let's hold ourselves to the same standard.
