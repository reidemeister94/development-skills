# Repository documentation format

Use the [writing contract](writing.md) for documentation.
Repository knowledge documents use the [Open Knowledge Format](https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/refs/heads/main/okf/SPEC.md) fields below.
Skill files, agent files, scoped rules, and templates retain their own required formats. `docs/ATLAS.md` has no frontmatter.

## Metadata

- `type`: `entrypoint`, `rule`, `guide`, `explanation`, `reference`, `plan`, `decision`, or `report`.
- `description`: one meaningful line that helps an agent decide whether to read the document.

Optional fields are `title`, `tags` with kebab-case values, `timestamp` for the last meaningful change, and `resource` for a canonical URI.
The H1 supplies the human title. Preserve unknown fields. Add metadata only when it carries useful information.

## Task lifecycle

Plans and chronicles additionally use:

```yaml
status: active        # draft | active | superseded | obsolete
archived: false       # matches the file's location
work_status: draft    # draft | in-progress | completed
```

Use repository-relative paths without `.md` as document IDs.
The optional `plan` and `chronicle` fields link paired task records. Update these paths after an archive move.
`status: superseded` requires `superseded_by`; the successor lists the old ID in `supersedes`.
Use whole-document supersession only when the entire record is replaced. For partial changes, link the affected decision.
`status: obsolete` requires a dated `obsolete_reason`.
Completed chronicle decision prose is immutable; lifecycle metadata and link repairs can change.
A completed plan can move to `docs/plans/archive/` only when every task item is closed.
`align-docs` owns archive moves and inbound link repairs.
