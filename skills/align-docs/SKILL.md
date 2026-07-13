---
name: align-docs
description: "Align AGENTS.md, rules, README, plans, and chronicles with the codebase; use --clean to archive obsolete task docs into ATLAS.md."
user-invocable: true
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, AskUserQuestion
---

# Align docs

Make the repository the one shared source for Claude Code, Codex, and humans:

```text
CLAUDE.md                 # exactly @AGENTS.md
AGENTS.md                 # concise always-read facts and rules index
.agents/rules/*.md        # topic rules with paths: frontmatter
.claude/rules -> ../.agents/rules
```

Resolve the git root and inspect these files, README, `docs/`, manifests, referenced paths, and any agent memory. Report missing, stale, duplicated, or oversized context before editing.

Preserve an `align-docs:principles-customized` block in AGENTS.md if already present. Otherwise prepend [agents-template.md](references/agents-template.md) at the top of AGENTS.md. Keep AGENTS.md near 70 lines: project scope, only non-obvious domain/infrastructure/company/project facts, then one index row per rule. A rule owns its topic; AGENTS.md links instead of repeating it.

Ensure CLAUDE.md is the one-line import, the rules symlink exists, and `.gitignore` contains `.claude/CLAUDE.md` and `AGENTS.override.md`. Personal machine facts belong in `.claude/CLAUDE.md` or the user's global Codex AGENTS file, not shared docs.

Capture only durable facts learned in the current session and absent from disk. Cold invocation reports `CAPTURE: NONE`. Put always-read facts in AGENTS.md, topic depth in a rule, decisions in chronicles, and procedures in plans. Empty or generic memory is deleted after useful content is moved.

With `--clean`, also follow [clean-mode.md](references/clean-mode.md): update `docs/ATLAS.md` as the decision index and archive obsolete plans/chronicles without deleting decisions.

Finish by checking line budget, rule scopes, symlink target, ignored personal files, README/manifests against disk, and every Markdown link. Apply the [reduce-gate](../../shared/skill-authoring.md) to all changed agent docs.
