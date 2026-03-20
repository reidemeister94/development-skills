Produce a factual chronicle of what happened with the development-skills plugin during this conversation. Pure record of events — zero judgment, zero opinions, zero adjectives like "unnecessary" or "excellent". The reader draws their own conclusions.

Write to `docs/reports/development-skills-feedback-YYYY-MM-DD.md` (today's date). Self-contained — the reader knows nothing about this project.

## Section 1: Project Context (short)

Language, size, test count, framework. What task was performed. Why the plugin was involved.

## Section 2: Full Chain-of-Thought Dump

EXHAUSTIVE chronological dump of every plugin interaction from first message to final result. Every skill trigger, phase file read, gate evaluation, routing decision, agent spawn, tool call, verification run, deviation. Nothing skipped.

Each step:
1. **Plugin instruction:** Quote the specific instruction from the specific plugin file being followed
2. **Agent action:** Tool called, parameters, result
3. **Agent reasoning:** Why it followed or deviated from the instruction
4. **Outcome:** What happened

```
Step 3: core-dev/SKILL.md Step 1: "Run: bash scripts/find-plan.sh active"
  - Action: Glob("**/find-plan.sh") → no results. Glob variant → no results. grep fallback → found plan.
  - Reasoning: Script not found. Used fallback instruction "or check docs/plans/ directly".
  - Outcome: Active plan found. 3 tool calls.

Step 4: core-dev/SKILL.md Step 4: "LIGHTWEIGHT MODE applies if ALL: Scope <= 3 files..."
  - Action: Evaluated scope = 20+ files → FALSE.
  - Reasoning: Task is 20+ files (fails lightweight) but zero logic changes. No mode between lightweight and full.
  - Outcome: Full 7-phase workflow activated.
```

## Section 3: Friction Point Summary

Table indexing Section 2 friction points:

| # | Step | Plugin file + instruction | What happened | Tool calls |
|---|------|--------------------------|---------------|------------|

## Section 4: Proposed Behavioral Evals

One eval per friction point. JSON format:

```json
{
  "name": "kebab-case-name",
  "category": "category",
  "tests_change": "which friction point",
  "prompt": "user prompt triggering the scenario",
  "expected_output": "what the model should do",
  "assertions": [{"name": "x", "type": "behavioral", "check": "what to check", "pass_criteria": "pass/fail criteria"}]
}
```

After writing, verify Section 2 covers every plugin interaction, then tell the user where the report is.
