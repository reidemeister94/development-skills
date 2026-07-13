# Project conventions — shared discovery rules

Discover project-local design conventions relative to the project root, using bounded globs rather than searching every Markdown file:

- `ui-guidelines/*.md`, `docs/design/`, `docs/ui/`, `docs/style/`
- `CONVENTIONS.md`, `STYLE.md`
- Design, UI, or styling sections of `AGENTS.md` and `CLAUDE.md`
- `.agents/rules/`, `.claude/rules/`, and `.cursor/rules/`
- `package.json` for the framework, component libraries, notification system, and icon libraries

Project rules win. Cite a discovered convention only when diverging from it, when asked, or when matching an existing file. If none exists, use the relevant skill references and the generic audit contract; do not invent a convention file.
