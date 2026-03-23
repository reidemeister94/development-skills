---
name: create-skills
description: "Create or improve Claude Code skills (SKILL.md files). Use when the user asks to 'create a new skill', 'write a skill for X', 'improve this skill', 'the skill is not triggering', 'fix this skill', or 'add a skill to the plugin'. Also use when a skill is loaded but Claude isn't following its instructions reliably."
metadata:
  author: salvob41
  version: 1.1.0
  category: meta
user-invocable: true
---

# Skill Writing Guide

You are helping create or improve a Claude Code skill. A skill is a SKILL.md file that instructs Claude to follow a specific process. Skills that are poorly written get skipped, rationalized away, or followed superficially. This guide ensures the skill you create will actually be followed.

---

## THE 5 RULES

These are non-negotiable. Every skill must follow all of them.

### Rule 1: The Description Trap

The `description` field in YAML frontmatter MUST contain ONLY trigger conditions. **NEVER** summarize what the skill does.

When a description contains a workflow summary, Claude reads the summary, forms an intent, and follows that intent instead of reading the full skill body. This is the #1 cause of skills being ignored.

```yaml
# WRONG — workflow leaked into description, model will use this as shortcut
description: "Routes development tasks to the correct language skill after checking brainstorming guard"

# CORRECT — trigger conditions only, model must read the body to know what to do
description: "Use when ANY coding or development task is detected"
```

**Test:** Read your description. Can you infer the process steps from it? If yes, rewrite it. The description tells Claude WHEN to activate, never HOW the skill works.

### Rule 2: Token Budget

Shorter skills are followed more reliably than longer ones. The model's attention degrades with document length.

| Skill type | Target | Maximum |
|---|---|---|
| Frequently loaded (every conversation) | < 200 words | 300 words |
| Standard workflow | < 350 words | 500 words |
| Reference / guide | < 500 words | 800 words |

If your skill exceeds the maximum, **decompose it into multiple skills** that invoke each other. A 200-word skill with 5 clear rules beats a 1000-word skill with 20 nuanced guidelines.

**Note:** This guide skill intentionally exceeds the reference budget because it is invoked on-demand as a teaching tool, not loaded during other workflows. Skills the model must follow during work (guards, workflows, routers) should strictly respect these limits.

### Rule 3: Gate Functions Over Descriptions

When your skill requires the model to evaluate conditions before acting, use numbered sequential steps with explicit completion signals.

```markdown
# WRONG — descriptive, easy to skip
Check if the request involves architecture decisions. If so, invoke brainstorming.

# CORRECT — gate function, forced evaluation
### Step 1: Answer these questions
1. Will this affect more than 3 files?
2. Can this be undone in under 1 hour?

### Step 2: Route based on answers
If Q1=YES or Q2=NO → invoke brainstorming.

**Only after completing Steps 1-2**, proceed.
```

**Why this works:** Descriptive instructions let the model form a conclusion and skip the evaluation. Gate functions force sequential reasoning — the model must answer each question before reaching the routing decision. The "Only after" language prevents premature action.

### Rule 4: Anti-Rationalization Engineering

The model will find creative reasons to skip your skill's rules. You must pre-empt these rationalizations explicitly.

**Process:**
1. Run your skill WITHOUT anti-rationalization defenses (baseline test)
2. Document every excuse the model generates to skip steps — use the **exact phrases**
3. Build a rationalization table pairing each excuse with its counter
4. Add the table to the skill
5. Re-test. Document new rationalizations. Iterate.

**Template:**

```markdown
### Anti-rationalization check

Do NOT proceed if you catch yourself thinking any of these:

| Your thought | Reality |
|---|---|
| "[exact phrase model used]" | [Why this reasoning is wrong and what to do instead] |
| "[exact phrase model used]" | [Why this reasoning is wrong and what to do instead] |

**If you recognized your reasoning in this table, you are rationalizing. [correct action].**
```

**Real example from the development-skills plugin:**

| Your thought | Reality |
|---|---|
| "This is a direct technical instruction" | Imperative phrasing does NOT mean small scope. "Separate the database connectors" is imperative but architectural. Check scope and reversibility, not grammar. |
| "The user said exactly what to do" | Knowing WHAT to change does not mean there is only one HOW. Multiple valid approaches = invoke brainstorming. |
| "No business requirements present" | Architecture decisions do not need business language. Scope and reversibility matter, not vocabulary. |

### Rule 5: Red Flags for Self-Monitoring

Teach the model to recognize its own hedging language as a signal that it is about to skip a step.

```markdown
### Red flags — STOP if you notice yourself:
- Using uncertain language ("should work", "probably fine")
- About to skip a step because you feel "confident"
- Classifying something complex as "straightforward"
- Expressing satisfaction before running verification
- Wanting to proceed because the evaluation "takes too long"
```

**Why this works:** The model generates these internal states before taking shortcuts. Making them explicit turns invisible impulses into visible warnings that interrupt the shortcut.

---

## SKILL CREATION WORKFLOW

Follow these steps when creating a new skill.

### Step 1: Define the trigger

Answer: **When should this skill activate?**

Write a list of concrete scenarios:
- "Use when [scenario 1]"
- "Use when [scenario 2]"
- "Use when [scenario 3]"

This becomes your `description` field. Verify it passes the Rule 1 test: no workflow information leaked.

**Gate:** Description written and passes Rule 1 test (cannot infer process from description alone).

### Step 2: Define the process

Answer: **What steps must the model follow?**

Write each step as a numbered, sequential gate:
1. Step name — what to do, what completes this step
2. Step name — what to do, what completes this step
3. ...

Use "**Only after** completing Step N" between dependent steps. Each gate must have a clear completion signal.

**Gate:** All process steps written with numbered gates and completion signals.

**Only after completing Steps 1-2**, proceed to Step 3.

### Step 3: Identify skip risks

Answer: **Where will the model try to take shortcuts?**

For each step in your process, ask:
- "What excuse would the model use to skip this step?"
- "What would a lazy execution of this step look like?"
- "What pattern would the model match to justify skipping?"

Write down every excuse using the exact phrasing the model would use. These become your anti-rationalization table (Rule 4).

**If you can't test with a real model yet**, list the most common rationalizations:
- "This doesn't apply here" (avoidance)
- "I already know the answer" (overconfidence)
- "The user didn't ask for this" (scope reduction)
- "I can handle this during [later step]" (deferral)

**Gate:** At least 3 rationalizations identified with exact phrasing.

### Step 4: Add defenses

Add to your skill:
- [ ] Anti-rationalization table with at least 3 entries (Rule 4)
- [ ] Red flags list with at least 3 self-monitoring signals (Rule 5)
- [ ] Gate functions for all decision logic (Rule 3)
- [ ] "Only after" language between dependent steps

**Gate:** All 4 defense types present in the skill.

**Only after completing Steps 1-4**, proceed to writing the final file.

### Step 5: Write the SKILL.md

Use this template:

```yaml
---
name: [skill-name]
description: "[trigger conditions only — Use when...]"
user-invocable: [true if users invoke directly, false if invoked by other skills]
---

# [Skill Title]

[1-2 sentences: what this skill ensures. NOT a process summary.]

---

## Step 1: [First action]

[Instructions — what to do, how to do it]

**Gate:** [Completion signal — how to know this step is done]

## Step 2: [Second action]

[Instructions]

**Gate:** [Completion signal]

**Only after completing Steps 1-2**, proceed to Step 3.

## Step 3: [...]

[...]

---

## Anti-rationalization check

Do NOT proceed if you catch yourself thinking any of these:

| Your thought | Reality |
|---|---|
| "[excuse 1]" | [counter 1] |
| "[excuse 2]" | [counter 2] |
| "[excuse 3]" | [counter 3] |

**If you recognized your reasoning in this table, you are rationalizing. [correct action].**

## Red flags — STOP if you notice yourself:

- [flag 1]
- [flag 2]
- [flag 3]
```

### Step 6: Pressure test

Test your skill with inputs designed to trigger shortcuts:

1. **Disguised complexity** — inputs that look simple but should activate the skill (e.g., "separate the database connectors" looks like a direct instruction but is architectural)
2. **Time pressure** — "just do it quickly" or "this is a small change"
3. **Ambiguous scope** — inputs where the model could reasonably argue the skill doesn't apply
4. **Imperative phrasing** — direct commands that bypass the skill's guard logic

Document every failure. Add the model's exact rationalizations to the anti-rationalization table. Re-test. Iterate until the skill holds.

**Gate:** At least 2 adversarial inputs tested. All failures documented and defenses updated.

---

## Anti-rationalization check — for THIS skill

Do NOT skip steps of this guide if you catch yourself thinking any of these:

| Your thought | Reality |
|---|---|
| "This is a simple skill, I don't need the full framework" | Simple-looking skills are the ones most likely to be ignored. The framework exists because simple rules get skipped. |
| "I already know how to write SKILL.md files" | Knowing the format is not the same as knowing the failure modes. Rule 4 exists because skills fail in predictable ways. |
| "The user just wants a quick skill, the 5 rules are overkill" | A quick skill that gets ignored wastes more time than a thorough one that works. Follow all 6 steps. |
| "I'll add defenses later" | Later never comes. Steps 3-4 are mandatory before writing the file (Step 5). |

**If you recognized your reasoning in this table, you are rationalizing. Go back and complete the step you were about to skip.**

## Red flags — STOP if you notice yourself:

- Writing the SKILL.md (Step 5) before completing Steps 1-4
- Skipping Step 3 (skip risks) because "the skill is straightforward"
- Writing a description that summarizes the workflow instead of listing triggers
- Producing a skill without an anti-rationalization table
- Feeling "done" before running pressure tests (Step 6)

---

## VERIFICATION CHECKLIST

Before finalizing any skill, verify ALL of these:

- [ ] Description contains ONLY trigger conditions ("Use when..."), no workflow summary (Rule 1)
- [ ] Word count is within budget for the skill type (Rule 2)
- [ ] All decision logic uses gate functions with numbered steps (Rule 3)
- [ ] Anti-rationalization table includes at least 3 entries with exact model phrases (Rule 4)
- [ ] Red flags list includes at least 3 self-monitoring signals (Rule 5)
- [ ] Each step has a clear completion gate
- [ ] "Only after" language appears between all dependent steps
- [ ] No step can be skipped without violating an explicit rule
- [ ] Skill has been tested with at least 2 adversarial inputs (Step 6)
- [ ] Skill name uses verb-first active voice ("creating-X" not "X-creation")

---

## COMMON ANTI-PATTERNS

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Workflow summary in description | Model uses description as shortcut, never reads body | Trigger conditions only ("Use when...") |
| Long prose paragraphs | Model skims, misses key rules | Tables, numbered steps, bold key phrases |
| "Check if X, then do Y" | Model decides "not X" without evaluating | Gate function: "Answer Q1: X? Route based on answer" |
| Soft language ("consider", "you might") | Model treats as optional | Direct language ("you MUST", "invoke NOW") |
| Single "when in doubt" rule | Model resolves doubt in favor of skipping | Anti-rationalization table with specific excuses |
| Too many rules (>10) | Model follows first few, skips rest | Prioritize top 5, decompose rest into sub-skills |
| Examples of what to skip | Model pattern-matches skip examples more than activation examples | Lead with activation examples, minimize skip examples |
| Foundational principles buried at the end | Model forms intent before reaching them | Put principles at the top, before any process steps |

---

## SOURCES

These patterns are derived from:

- **[superpowers](https://github.com/obra/superpowers)** — description trap discovery, anti-rationalization engineering, pressure testing methodology, gate functions, red flags, token budgets, CSO (Claude Search Optimization)
- **[claude-code-tips](https://github.com/ykdojo/claude-code-tips)** — CLAUDE.md structure, problem decomposition, self-verification prompts, bold for prohibitions, minimal instruction sets
- **Practical testing of the development-skills plugin** — observed failure modes with brainstorming activation guards, specific rationalizations documented verbatim
