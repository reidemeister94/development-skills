---
name: brainstorming
description: "Use when multiple valid approaches exist, the wrong choice is costly to reverse, or the WHY behind a request matters."
user-invocable: true
allowed-tools: Glob, Read, Edit, Task, Skill
---

# Brainstorming — Orchestrator

You delegate ALL analysis to an isolated Task agent. You do NOT analyze, research, or read code yourself.

## TASK CONTEXT

**Your task:** $ARGUMENTS

If `$ARGUMENTS` is empty: Display "What would you like me to analyze?" Then STOP.

---

## STEP 1: LAUNCH ANALYSIS SUBAGENT

1. Glob `**/brainstorming/analysis-agent.md` (fallback: `~/.claude/plugins/`)
2. Read it. Note the directory (= skill directory).
3. Replace `{TASK}` with complete task context and `{SKILL_DIR}` with directory path
4. Spawn via Task tool: `subagent_type: general-purpose`, `model: opus`

**Do NOT analyze yourself. Do NOT follow the agent's instructions.**

---

## STEP 2: DISPLAY RESULTS

### `BRAINSTORM_RESULT::PASS_THROUGH`:

> **Brainstorming: PASS THROUGH** — Task does not require analysis.
> **USER CHOICE: PASS_THROUGH**

STOP.

### `BRAINSTORM_RESULT::NEEDS_CLARIFICATION`:

Display questions. STOP. Wait for answers. Re-spawn with original context + answers.

### `BRAINSTORM_RESULT::COMPLETE`:

Extract PLAN_PATH, RESEARCH_PATH, VERDICT, APPROACH, COMPLEXITY, summary.

> **Brainstorming complete.**
> **Plan:** `[PLAN_PATH]` | **Research:** `[RESEARCH_PATH]`
>
> [Summary]

If verdict is **STOP**: **WARNING: Critical evaluation recommends STOP.** [Reason]

**STOP your response. End your turn.** Do NOT proceed to Step 3 in the same response.

### Malformed output:

Display and note "unexpected format."

### Error or timeout:

1. Check `docs/plans/` for partial results
2. Partial plan → present with "agent failed mid-analysis"
3. Nothing → report failure, offer: retry / proceed without / abandon

---

## STEP 3: APPROACH SELECTION — HARD GATE

**Anti-rationalization:** If thinking "analysis is clear, I can proceed" — STOP. User MUST confirm.

### 3a: Clarifying Questions

If genuine uncertainty from analysis, display and STOP. Otherwise skip to 3b.

### 3b: Present Options (MANDATORY)

```
Which approach do you want to go with?

1. [Approach A] (Recommended) — [summary + trade-off]
2. [Approach B] — [summary + trade-off]
N-1. Modify something
N. Just the analysis — don't start implementation
```

**Do NOT use AskUserQuestion. STOP. Wait.**

### 3c: Handle Response

- **Approach selected:** → Step 4
- **Modify:** Ask what. Simple → edit plan, return to 3b. Fundamental → re-launch agent. After 3 cycles, suggest proceeding.
- **Just analysis:** Announce plan saved. STOP.

---

## STEP 4: SAVE AND ROUTE

### 4a: Save

Append to plan file at `[PLAN_PATH]`:

```markdown
## Approach Decision

**Selected:** [name]
**User modifications:** [None / changes]
**Confirmed:** [YYYY-MM-DD]
```

### 4b: Route

> **Approach confirmed: [name].** Starting development workflow.

Invoke `development-skills:core-dev` via Skill tool (no args — Step 1 detects active plan).

### 4c: Abandon

Edit `Status: In Progress` → `Status: Abandoned` in plan file. STOP.
