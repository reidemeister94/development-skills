---
name: plugin-feedback
description: "Record or apply development-skills plugin feedback; runs on /plugin-feedback. Mode via argument: produce (factual report of plugin interactions this conversation) | ingest <report-path> (apply only evidence-backed simplifications)."
user-invocable: true
argument-hint: "produce | ingest <report-path>"
---

# Plugin feedback

`produce` writes `docs/reports/development-skills-feedback-YYYY-MM-DD.md` with the task context, plugin/skill actions, observed outcomes, friction, and reproducible eval ideas. Record events and evidence, not private reasoning.

`ingest <report-path>` treats the report as a hypothesis. Change the plugin only when an instruction is demonstrably wrong or repeatedly wasteful and the fix is simpler than the current text. Prefer deletion or merging; do not add an exception for one model mistake.

Add an eval only when it can check an observable outcome through the Pydantic fresh-context schema. Report fixes, rejected suggestions, changed files, and verification. Expect most suggestions to be rejected.
