---
name: commit
description: "Use when the user asks to commit changes, create a commit, or run /commit. Use when staged changes need a conventional commits message."
user-invocable: true
---

# Commit Skill

Commit staged changes with a conventional commits message.

## Instructions

1. Run `git status` to see staged changes (never use -uall flag)
2. Run `git diff --cached` to see the actual staged changes
3. Run `git log --oneline -5` to see recent commit style for context

4. Analyze the staged changes and create a commit message following the **Conventional Commits** specification:
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, `perf`, `ci`, `build`
   - Scope is optional but recommended (e.g., component name, feature area)
   - Description should be concise, imperative mood, lowercase, no period at end

   **Body rules (most commits need NO body):**
   - Default: subject line only, no body
   - Skip the body if the subject line fully explains the change
   - Only add a body for:
     - Breaking changes (required)
     - Non-obvious reasoning that isn't clear from code/PR
     - Migration steps users must take
   - If you do add a body, keep it to 1-2 short sentences max

5. Create the commit:

   **Default (no body):**
   ```bash
   git commit -m "type(scope): description"
   ```

   **Only when body is needed:**
   ```bash
   git commit -m "$(cat <<'EOF'
   type(scope): description

   Brief explanation of WHY, not WHAT.
   EOF
   )"
   ```

6. Run `git status` to verify the commit succeeded

## Important

- Do NOT add `Co-Authored-By` lines
- **Note:** This overrides the default Claude Code behavior of adding Co-Authored-By. The team prefers clean commit messages without attribution lines.
- Do NOT include emojis in the commit message
- Keep the subject line under 72 characters
- Use imperative mood: "add" not "added", "fix" not "fixed"

## Anti-patterns (do NOT do this)

Bad - body repeats the subject:
```
fix(auth): handle null user in session check

Handle the case where user is null in the session check.
```

Bad - body describes obvious changes:
```
feat(ui): add dark mode toggle

Add a toggle button for dark mode in the settings panel.
```

Good - no body needed:
```
fix(auth): handle null user in session check
```

Good - body adds non-obvious context:
```
feat(api): switch from REST to GraphQL

Breaking: All /api/v1 endpoints removed. See MIGRATION.md.
```

## Examples

- `feat(auth): add logout button to navbar`
- `fix(api): handle timeout errors in fetchPlanning`
- `refactor(campaigns): extract column definitions to separate file`
- `chore(deps): update dependencies`
- `docs(readme): add deployment instructions`
