---
name: eval-regression
description: Use when the user asks to compare a plugin or skill against HEAD, run regression evals, or check behavioral regressions before a commit.
allowed-tools: Glob, Read, Bash, Grep
---

# Eval regression

Compare the working tree with `HEAD` using the same Pydantic Evals cases, runner, agent, and repeat count. Only the plugin version may differ.

Resolve the target plugin from the argument or current directory. Use its `evals/fresh-context.json`; if absent, help define executable cases first, using this plugin's file as the smallest example. Support only installed Claude and Codex CLIs. Run the requested agent, or both when none is named.

For each agent:

1. Stop if the target has no behavioral diff.
2. Create a temporary directory and extract the base with `git archive HEAD` without touching the working tree. Accept an explicit `--base <commit>` instead.
3. Run `../ai-agent-bench/scripts/fresh_context_eval.py` against the archived plugin and the candidate plugin. Use `repeat=3` by default; use `1` only for an explicit smoke run.
4. Compare their JSON reports with the runner's `--compare BASELINE CANDIDATE` mode.
5. Report each `REGRESSION`, `IMPROVEMENT`, `STABLE`, or `INCONCLUSIVE` result and its observed rates. A missing run, timeout, or unequal evidence is inconclusive, never a pass.
6. Remove the temporary directory. Do not edit or commit the target.

The runner sends traces to Logfire only when a token is present. Its assertions are deterministic only (`tool`, `clean_worktree`, `changed_file`, `file_contains`); a genuinely semantic contract means extending the runner with a Pydantic AI judge first, not approximating it with prose.
