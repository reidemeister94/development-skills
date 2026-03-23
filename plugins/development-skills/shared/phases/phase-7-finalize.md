# Phase 7: FINALIZE — GATE

## 7a: Chronicle Finalization

1. **Chronicle created:** Read `## Implementation Log` for discoveries. Align with final code. Update Status to Completed. Identify insights for CLAUDE.md.
2. **Chronicle NOT NEEDED:** Check WORKFLOW STATE reason. If significant discoveries emerged (check Implementation Log), consider retroactive chronicle.
3. **Update CLAUDE.md** with new patterns/rules/knowledge
4. **Update WORKFLOW STATE:** `Status: Completed`, `Current Phase: 7 (Complete)`

**Gate:** State **"CHRONICLE FINALIZED — [filename]"** (or confirm NOT NEEDED)

## 7b: Align Documentation

Invoke `development-skills:align-docs` via Skill tool.

## 7c: Integration

**Default (changes on current branch):**

```
Implementation complete. Would you like me to commit the changes?

1. Yes, commit now
2. No, I'll handle it myself
```

**STOP and wait.** Only commit if user chooses option 1. Use `development-skills:commit` via Skill tool.

**Unmerged worktree branch (rare):**

```
Implementation complete. How would you like to land the changes?

1. Merge to current branch locally
2. Push and create a Pull Request
3. Keep the branch as-is
4. Discard this work
```

| Option | Actions |
|--------|---------|
| 1. Merge | checkout base → merge → test → delete branch → cleanup worktree |
| 2. PR | push → `gh pr create` with plan summary → keep branch |
| 3. Keep | Report branch name and path |
| 4. Discard | Confirm with "discard" → checkout base → delete branch → cleanup |

## Expected Artifacts
- Chronicle finalized or confirmed NOT NEEDED
- CLAUDE.md updated (if applicable)
- Documentation aligned
- Changes integrated per user's choice
- WORKFLOW STATE: `Status: Completed`, `Current Phase: 7 (Complete)`

State: **"WORKFLOW COMPLETE"**
