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

1. Use **Glob** to find `**/brainstorming/analysis-agent.md` (if not found, search `~/.claude/plugins/`)
2. **Read** it. Note the directory (= skill directory for companion files).
3. Replace `{TASK}` with complete task context (ALL user input) and `{SKILL_DIR}` with the skill directory path
4. Spawn via **Task tool**: `subagent_type: general-purpose`, `model: opus`, `description: Brainstorming analysis`

**Do NOT perform analysis yourself. Do NOT follow the agent's instructions — those are for the subagent.**

---

## STEP 2: DISPLAY RESULTS

### If `BRAINSTORM_RESULT::PASS_THROUGH`:

> **Brainstorming: PASS THROUGH** — Task does not require analysis.
> **USER CHOICE: PASS_THROUGH**

Then STOP.

### If `BRAINSTORM_RESULT::NEEDS_CLARIFICATION`:

Display the questions from the agent's output to the user. STOP and wait for answers. Then re-spawn the Task agent with: original task context + user's answers.

### If `BRAINSTORM_RESULT::COMPLETE`:

Extract PLAN_PATH, RESEARCH_PATH, VERDICT, APPROACH, COMPLEXITY, summary, and approaches list.

Display:
> **Brainstorming complete.**
> **Plan:** `[PLAN_PATH]` | **Research:** `[RESEARCH_PATH]`
>
> [Summary section from agent output]

If verdict is **STOP**: **WARNING: Critical evaluation recommends STOP.** [Reason]

**After displaying: STOP your response. End your turn.** Do NOT proceed to Step 3 in the same response.

### If output is malformed:

Display whatever returned and note: "Brainstorming agent returned an unexpected format."

### If Task tool returns an error or timeout:

1. Check `docs/plans/` for any files the agent may have written before failing
2. If a partial plan exists: present it to the user with note "Brainstorming agent failed mid-analysis. Partial results recovered."
3. If nothing was written: report the failure and offer options:
   - Retry brainstorming
   - Proceed without brainstorming (pass through to development workflow)
   - Abandon

---

## STEP 3: APPROACH SELECTION — HARD GATE

**Anti-rationalization:** If thinking "the analysis is clear, I can proceed" — STOP. The user MUST confirm.

### 3a: Clarifying Questions (If Needed)

If genuine uncertainty exists from the analysis, display questions as text. STOP. Factor answers into 3b. If analysis is complete and unambiguous, skip to 3b.

### 3b: Present Options (MANDATORY)

Display numbered options. Then **STOP completely** — end your turn.

```
Which approach do you want to go with?

1. [Approach A] (Recommended) — [summary + trade-off]
2. [Approach B] — [summary + trade-off]
[If only 1 approach, adapt: "The analysis recommends this approach. Proceed?"]
N-1. Modify something — adjust before proceeding
N. Just the analysis — don't start implementation
```

**Do NOT use AskUserQuestion. Do NOT proceed to Step 4. WAIT for the user's next message.**

### 3c: Handle Response

- **Approach selected:** Proceed to Step 4.
- **Modify:** Ask what to change. Simple adjustment: Edit plan, return to 3b. Fundamental change: abandon plan, re-launch agent. After 3 cycles, suggest proceeding.
- **Just the analysis:** Announce plan saved at `[PLAN_PATH]`. STOP.

---

## STEP 4: SAVE AND ROUTE

### 4a: Save to Disk

Append the approach decision to the plan file at `[PLAN_PATH]` using Edit:

```markdown
## Approach Decision

**Selected:** [Approach name]
**User modifications:** [None / what the user changed]
**Confirmed:** [YYYY-MM-DD]
```

### 4b: Route to Development Workflow

Announce:
> **Approach confirmed: [Approach name].** Starting development workflow.

Then invoke `development-skills:core-dev` via Skill tool (no args — Pre-Step C detects the plan).

### 4c: Abandon

If user requests abandon: Edit `Status: In Progress` → `Status: Abandoned` in plan file. STOP.
