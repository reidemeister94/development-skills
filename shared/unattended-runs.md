# Unattended runs

The loop skills follow the [development loop](development-loop.md), with permission to commit their verified changes on their own branch.
Keep unrelated changes out of those commits. Never push, merge, or write to production.

Agree on the result and verification before starting autonomous work. Continue while useful work can advance within that agreement.
Record questions and proposed changes that need the user, and continue independent work.
Ask through the question tool: under a goal, a question written in chat ends the turn and the run continues without the answer.
Reread the plan and invoked skill when resuming so the objective and limits survive context compaction.

A goal keeps the run going: in Claude Code the user starts it with `/goal /<skill> [focus]`; in Codex, create it with the goal tool once done and verification are agreed.
The goal's evaluator reads only the conversation. End each turn with progress against the agreed done items.
Finish with `DONE` and the evidence when the agreed result and checks are satisfied, or `BLOCKED` with what needs the user.
