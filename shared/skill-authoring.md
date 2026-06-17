# Skill Authoring — the reduce-gate

The single canonical gate for any skill, reference, or plugin doc. Apply it before writing or editing one; the `staff-reviewer` re-fires it on every `plugins/**` / `SKILL.md` diff (it binds in both review modes, no caller prompt). Other docs reference this file — they do not restate it.

**The best skill is the one you never wrote.** Brevity comes from necessity, not negligence — lazy, not negligent.

Benchmark every line against yourself: **if a capable coding agent would already do it correctly from training, it is noise — delete it, however well written.** A skill body carries ONLY the non-obvious project/company/domain facts and procedures an agent would NOT derive unprompted. That institutional knowledge is the one thing brevity never touches — distill or relocate it, never amputate it. Restating an Iron Rule, a generic best practice, or a framework idiom is itself a Principle 5 violation.

The ladder, before adding anything:
1. Does this skill / file / line need to exist? — no → skip it.
2. Does an existing skill or shared file already cover >50%? — yes → fold in or reject.
3. One fewer file / section / table? — yes → make it so.
4. Only then: the minimal form.

Reference, never duplicate — link to `shared/` / `references/` by path. A reference file needs a live inbound link and must be non-derivable before it exists. The plugin is the source of truth for company/project conventions: encode what you learn HERE, inline and self-contained — never defer to "go read repo X" or a runtime fetch.

Editing an existing artifact: net words added ≤ removed, unless you can name the non-obvious fact each new line carries. This overrides skill-creator's "make it pushy / go longer" bias — descriptions stay terse but discriminating, bodies stay minimal.
