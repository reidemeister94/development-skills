# Aggregation and reporting

Invoked from `SKILL.md` Step 5, after all trials complete.

---

## Cross-agent aggregator command

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/ai-agent-bench/scripts/parse_transcript.py" \
    --aggregate "$REPO/eval-results/<task>/*/run-*/" \
    --output "$REPO/eval-results/<task>/comparison.json" \
    --render-report "$REPO/eval-results/<task>/comparison.md"
```

Run once — it walks every `run-*` directory under the task and produces both the machine
form (`comparison.json`) and the human form (`comparison.md`).

---

## Output layout to print

```
✓ All trials complete.

Per-trial reports:
  eval-results/<task>/claude/run-1-<ts>/report.md
  eval-results/<task>/codex/run-1-<ts>/report.md
  ...

Cross-agent comparison:
  eval-results/<task>/comparison.md

Preserved branches (agent's work, ready for inspection):
  eval-claude-run1-<ts>
  eval-codex-run1-<ts>
```

---

## Top-line summary to extract from `comparison.json`

Print three bullets:

- Who passed the gate?
- Lowest cost USD?
- Biggest speedup (if perf was measured)?

Do not paraphrase the numbers — read directly from `comparison.json` and quote them.

---

## Manual-review reminder

> The `report.md` has **manual review sections** (hard-constraint compliance, code
> quality, prompt adherence) that need a human pass. Check out each branch to inspect
> the actual diff:
>
> ```bash
> git checkout eval-<agent>-run<id>-<ts>
> git diff <start_commit>...HEAD
> ```
