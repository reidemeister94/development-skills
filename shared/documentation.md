# Repository documentation format

Always follow the [writing contract](writing.md)

Apply the [Open Knowledge Format (OKF) v0.1](https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/refs/heads/main/okf/SPEC.md) for every documentation file produced in the repository.

Required on every document:

- `type`: `entrypoint`, `rule`, `guide`, `explanation`, `reference`, `plan`, `decision`, or `report`;
- `description`: one meaningful line an agent reads to decide whether to open the file.

Optional anywhere: `title` (the H1 owns the human title), `tags` (kebab-case strings), `timestamp` (date of last meaningful content change), `resource` (canonical URI when the document describes a real external asset).

Plans and chronicles/decisions additionally require lifecycle metadata:

```yaml
---
type: plan
description: One sentence an agent can use to decide whether to open the file.
status: active        # draft | active | superseded | obsolete
archived: false       # matches the file's location
work_status: draft    # draft | in-progress | completed (plans and chronicles)
---
```

- `status: superseded` requires `superseded_by: <document-id>`; the successor lists the prior document in `supersedes: [<document-id>]`;
- `status: obsolete` requires `obsolete_reason: <dated reason>`.

When a lifecycle field refers to another document, use its repository-relative path without `.md` as the document ID. Preserve unknown frontmatter fields. Never add placeholder descriptions or speculative metadata.
