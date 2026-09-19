---
paths:
  - "shared/**"
---

# Canonical workflow files

`shared/` owns contracts used by several skills or the reviewer.

| File | Role |
|---|---|
| `shared/development-loop.md` | Scope, authorization, path selection, checks, and completion. |
| `shared/full-path.md` | Persistent plan and chronicle workflow. |
| `shared/engineering.md` | Language-agnostic code and design rules. |
| `shared/writing.md` | Plain-language contract for chat and files. |
| `shared/documentation.md` | Knowledge metadata and lifecycle. |
| `shared/review-categories.md` | Review severity definitions. |
| `shared/skill-authoring.md` | Skill instruction reduction and validation. |
| `shared/templates/plan-template.md` | `YYYY-MM-DD__<slug>.md` plan skeleton. |
| `shared/templates/chronicle-template.md` | `YYYY-MM-DD__<slug>.md` decision skeleton. |

Skills, agents, README files, and guides link to these owners instead of copying their instructions.
Treat the development loop as a stable interface because each workflow depends on it.

Preserve legacy plan and chronicle names. New files use date and slug without a sequence number.
Use no emoji. Keep Markdown direct and factual.

Project-specific examples, installation instructions, changelog history, and language conventions do not belong under `shared/`.
