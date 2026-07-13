---
name: brainstorming
description: "Clarify an ambiguous or consequential change before planning or implementation when more than one sound approach exists."
user-invocable: true
allowed-tools: Glob, Grep, Read, Bash, Task, AskUserQuestion, Skill
---

# Brainstorming

If `$ARGUMENTS` is empty, ask what the user wants to explore and stop.

Inspect the repository before asking technical questions. State the current problem hypothesis, the observed facts behind it, and the unknowns that could change the result or proof.

Interview until both sides agree on why the change matters, what is in scope, what solved looks like, and how failure would be exposed. Ask one decision at a time, wait for the answer, and include your recommended answer with its trade-off. Facts come from exploration; decisions belong to the user.

Use `best-practices` when current external evidence can change the choice. Create a research file only when the result will remain useful after this task.

Offer alternatives only when they are genuinely different. Recommend the simplest one that meets the agreed result and company/project constraints.

Do not plan or implement until the shared understanding is explicit. A detailed request or prior spec is a stronger trigger, not an exemption — it fixes the WHAT, not the HOW. For data models and system boundaries, resolve identity, cardinality, lifecycle, ownership, time, and derivation before choosing a schema. Then return it to the full [development loop](../../shared/development-loop.md), which gates implementation on explicit plan approval.
