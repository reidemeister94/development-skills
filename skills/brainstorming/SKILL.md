---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Task, AskUserQuestion, Edit, Write, Skill
---

# Brainstorming — Conversational Design

**Announce:** "Using brainstorming. I'll walk the design tree with you, one branch at a time, before proposing approaches."

You run **in-thread**. The user is reachable. Walk the design tree with the user, then optionally delegate web research to a subagent, then write a plan to disk and gate before handing off to `core-dev`.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY non-trivial task regardless of perceived simplicity.

Truly trivial tasks (single-line typo, format a file, rename a variable, fix a one-line import) may exit early via Step 0 `PASS_THROUGH`. Anything beyond that — including *"translate an existing audit/plan into code"* — goes through the full flow.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

A long, detailed prior artifact (audit, RFC, design doc, plan, ticket) is NOT an exemption — it is a *stronger* trigger. Stale or under-challenged plans are the leading cause of wasted implementation work. The design can be short (a few sentences for genuinely simple cases), but you MUST present it and gate.

If thinking *"this is too simple to need a design"* or *"the audit already decided everything"* or *"this is just execution, not creative work"* — STOP. Display the design and gate.

## YOUR TASK

**Task:** $ARGUMENTS

If `$ARGUMENTS` is empty: ask *"What would you like me to brainstorm?"* and STOP.

---

## STEP 0 — Triage

Classify the task:

- **PASS_THROUGH**: small, bounded, clear (rename a variable, format a file, fix a typo, single-file mechanical change). Announce *"Triage: pass-through — this task does not need brainstorming"* and invoke `development-skills:core-dev` directly.
- **Focused**: a specific technical decision ("X vs Y", choice of library, design pattern, migration strategy). Skip Step 2 Q&A — go to Step 3 Approaches with focused research.
- **Full**: ambiguous, business-driven, architectural, multi-area, high blast radius. Run the full flow below.

If unsure: prefer Full over Focused, Focused over PASS_THROUGH.

---

## STEP 1 — Codebase Scan

Lightweight: Glob + Grep + Read of entry points, similar features, related modules. Build a `CODEBASE_FINDINGS` mental note.

**Do this BEFORE asking any technical question.** Never ask the user something a 60-second look at the codebase would answer.

Skip for PASS_THROUGH (already exited).

---

## STEP 2 — Q&A (Walk the Design Tree)

**Goal:** lock `WHY → scope → WHAT → quality bars → HOW`, in that order. Resolve parent decisions before children.

**Rules:**

1. **One topic at a time.** Resolve one branch before opening another.
2. **Multiple choice when possible**; open-ended only when no good options exist.
3. **Provide a recommended answer** when you are confident; declare uncertainty otherwise.
4. **Hard rule:** WHY / scope / priority / trade-off can never be derived from the codebase. Always ask if missing.
5. **No cap on questions.** Stop only when every branch is resolved or the user says *"enough"* / *"just propose"*.
6. **Anti-pattern:** do not infer, guess, or rationalize *"the user said X so probably means Y"*. When in doubt, ask.

**On Claude Code:** use the `AskUserQuestion` tool. Up to 4 logically-related questions per call (questions whose answers don't reframe each other). Dependent questions (where Q2 depends on Q1's answer) go in separate calls. Recommended answer = first option, label `"[option] (Recommended)"`.

**On Codex:** `AskUserQuestion` does not exist. Use a numbered list with an explicit STOP marker:

```
1. [option A] (Recommended)
2. [option B]
3. Other (describe)

Reply with the number or free text. STOP. Wait.
```

End your turn. Wait for the user's reply. Do not proceed until you have an answer.

---

## STEP 3 — Approach Sketch

Based on locked WHAT/WHY/scope, sketch **2-3 candidate approaches**:

- Each: 1-2 sentence description, complexity LOW/MEDIUM/HIGH, key trade-off.
- Lead with the recommended one.

**If the task is interface / API / module design**, read `references/design-it-twice.md` for the parallel-design technique. Optional but encouraged when the wrong shape is costly to reverse.

---

## STEP 4 — Optional Research

If approaches involve external best practices, official docs, or unfamiliar tech, delegate to the research subagent. Skip if the task is internal-only, the approaches are well-known, or the codebase already shows the pattern.

Pick `NNNN` = highest existing prefix in `docs/plans/` + 1 (or `0001`). Pick `SLUG` = kebab-case task topic. Remember both — they are reused in Step 7.

- **Claude Code:** `Task` tool, `subagent_type: general-purpose`, `model: opus`. Read `research-agent.md`, fill `{TOPIC}`, `{APPROACHES_TO_RESEARCH}`, `{CODEBASE_FINDINGS}`, `{NNNN}`, `{SLUG}`, `{SKILL_DIR}`, pass as prompt.
- **Codex:** see `using-development-skills/references/codex-tools.md` — requires `[features] multi_agent = true` in `~/.codex/config.toml`. Read `research-agent.md`, wrap the filled body in the standard agent template, `spawn_agent(agent_type="worker", message=...)`.

The subagent writes `docs/plans/{NNNN}__research__{SLUG}.md` and returns `RESEARCH_PATH::<path>` + a 5-line digest.

**Failure handling:** malformed return → retry once with a stricter format reminder. Second failure → tell the user, offer to proceed without external research.

After the subagent returns, **Read** the research file. Pull the selected approach, anti-patterns, and any reusable codebase patterns into your context.

---

## STEP 5 — Critical Evaluation

Read `critical-analysis.md`. Score complexity (0-10). Apply LIGHT (6-7) or FULL (8-10) framework. Below 6: skip critical evaluation, proceed with the recommended approach.

Produce a verdict: **PROCEED / PROCEED WITH CHANGES / RECONSIDER / STOP**. If `RECONSIDER` or `STOP`, surface the reason to the user and re-enter Step 2 Q&A or end the brainstorming flow.

---

## STEP 6 — Approach Selection

Present the candidate approaches to the user.

- **On Claude Code:** `AskUserQuestion` — 1 question, options = approaches + `"Just analysis"` + `"Modify"`.
- **On Codex:** numbered list + STOP.

Wait for user reply.

- **Approach selected:** continue to Step 7.
- **"Modify":** ask what. Simple edit → re-present. Fundamental → re-enter Step 2.
- **"Just analysis":** if Step 4 ran, the research file is already saved. End the brainstorming flow without writing a plan.

---

## STEP 7 — Write Plan File

Read `templates/plan-template.md`. Write to:

`docs/plans/{NNNN}__YYYY-MM-DD__implementation_plan__{SLUG}.md`

Use the same `NNNN` and `SLUG` from Step 4. Set `Status: In Progress`. The WORKFLOW STATE section MUST reference the research file path (if Step 4 ran) and include a Brainstorming Summary block.

---

## STEP 8 — Hard Gate (Design Approval)

**MANDATORY before invoking `core-dev`. No exceptions.**

Display a concise design summary in chat (5-10 lines: WHAT, WHY, selected approach, key risks). Then gate:

- **On Claude Code:** `AskUserQuestion` — *"Approve the design and proceed to implementation?"* — options: `"Approve and proceed (Recommended)"`, `"Modify"`.
- **On Codex:** numbered list:
  ```
  Design summary above. Approve to proceed to implementation?

  1. Approve and proceed (Recommended)
  2. Modify

  Reply with the number. STOP. Wait.
  ```

**Anti-rationalization line** — read this to yourself before deciding to skip the gate:
> *"If thinking 'this is too simple to need approval' — STOP. Display the gate."*

Do NOT invoke `core-dev` without an explicit approval signal.

If user picks `"Modify"`: ask what, edit the plan file, re-display the summary, re-gate.

---

## STEP 9 — Save Decision and Route

Append to the plan file:

```markdown
## Approach Decision

**Selected:** [name]
**User modifications:** [None / changes]
**Confirmed:** [YYYY-MM-DD]
```

Announce: *"Approach confirmed: [name]. Routing to core-dev."*

Invoke `development-skills:core-dev` via the Skill tool, no arguments. `core-dev`'s Step 1 detects `Status: In Progress` and proceeds without re-triggering brainstorming.

---

## Anti-Patterns

- **"This is too simple to need a design"** — every non-trivial task goes through this. The design can be short, but you MUST present it and gate.
- **Skipping Q&A because the user described HOW in detail** — the WHAT may be clear, but the WHY rarely is. Ask anyway.
- **Inferring scope** — if the user didn't say what's IN and what's OUT, ask. Don't assume.
- **Writing the plan without an approach decision** — Step 6 must happen before Step 7.
- **Routing to core-dev without the hard gate** — Step 8 is mandatory, not optional.
- **Multiple questions in one turn that reframe each other** — split them. Q1's answer must be in hand before Q2 makes sense.
