# Phase 7: FINALIZE — GATE

## 7a: Chronicle Finalization

1. **If chronicle was created:**
   - Read the plan file's `## Implementation Log` for discoveries and design decisions
   - Align chronicle with the final code state
   - Ensure all discoveries and insights are captured
   - Update chronicle Status to "Completed"
   - Identify insights to promote to CLAUDE.md
2. **If chronicle decision was "NOT NEEDED":** Check the plan file's WORKFLOW STATE `Chronicle:` field for the reason. Confirm it's still valid given what was discovered during implementation. If significant discoveries were made (check `## Implementation Log`), consider creating a chronicle retroactively.
3. **Update relevant CLAUDE.md files** with new patterns, rules, or knowledge
4. **Update WORKFLOW STATE:** Set `Status: Completed`, `Current Phase: 7 (Complete)`

The plan file is now the **complete record** of this workflow: task requirements, clarifications, plan, implementation reasoning, verification trail, and review audit log.

**Gate:** State **"CHRONICLE FINALIZED — [filename]"** (or confirm "CHRONICLE: NOT NEEDED" if skipped earlier)

## 7b: Align Documentation

Invoke `development-skills:align-docs` via Skill tool. This ensures all project docs (CLAUDE.md, plugin READMEs, MEMORY.md) reflect the changes made during this workflow.

## 7c: Integration — How to land the changes

**If the implementer ran in a worktree** (default), present these options:

```
Implementation complete. How would you like to land the changes?

1. Merge to current branch locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

**STOP and wait for the user's choice.** Then execute:

| Option | Actions |
|--------|---------|
| **1. Merge locally** | `git checkout <base-branch>` -> `git merge <feature-branch>` -> run tests on merged result -> `git branch -d <feature-branch>` -> cleanup worktree |
| **2. Create PR** | `git push -u origin <feature-branch>` -> create PR via `gh pr create` with summary from plan file -> keep branch |
| **3. Keep as-is** | Report branch name and worktree path. No cleanup. |
| **4. Discard** | Confirm with user ("Type 'discard' to confirm"). Then `git checkout <base-branch>` -> `git branch -D <feature-branch>` -> cleanup worktree |

**If NOT in a worktree** (lightweight mode or legacy): skip this step — changes are already on the current branch.

## Expected Artifacts
- Chronicle finalized (Status: Completed) or confirmed NOT NEEDED
- CLAUDE.md updated with new patterns/rules (if any)
- Documentation aligned with current disk state (via align-docs)
- Changes integrated per user's choice (merge/PR/keep/discard)
- WORKFLOW STATE: `Status: Completed`, `Current Phase: 7 (Complete)`

State: **"WORKFLOW COMPLETE"**
