# Phase 7: CHRONICLE FINALIZATION — GATE

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

5. **Align documentation:** Invoke `development-skills:align-docs` via Skill tool. This ensures all project docs (CLAUDE.md, plugin READMEs, MEMORY.md) reflect the changes made during this workflow. Do NOT skip — stale docs cost more to fix later than to update now.

## Expected Artifacts
- Chronicle finalized (Status: Completed) or confirmed NOT NEEDED
- CLAUDE.md updated with new patterns/rules (if any)
- Documentation aligned with current disk state (via align-docs)
- WORKFLOW STATE: `Status: Completed`, `Current Phase: 7 (Complete)`
- Plan file is now the complete record of this workflow

State: **"WORKFLOW COMPLETE"**
