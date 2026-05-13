# Phase 3: IMPLEMENT + VERIFY — GATE

**Cannot start without user-approved plan.** No approval? Go back to Phase 1.

Implementation runs **in main thread**. Test verification runs inline via `Bash`. You own the discipline.

Apply [Iron Rules](../iron-rules.md) throughout — especially #2 (no positive claims without evidence), #3 (WHY comments), #4 (RED-GREEN-REFACTOR), #6 (every gate explicit).

---

## Step 1: Update plan file BEFORE implementation

**Before writing any code:**

1. **Update WORKFLOW STATE:** `Current Phase: 3 (Implement + Verify)`, remove completed phases.
2. **Add `## Task Checklist`** with one line per task from the plan:
   ```markdown
   ## Task Checklist
   - [ ] Task 1: [description]
   - [ ] Task 2: [description]
   ```
3. **Verify** — Read plan file back to confirm both updates persisted.

**Do NOT touch any source file until the plan file has both updates.**

---

## Implementation Discipline (main-thread standing instructions)

### Surgical changes
Only modify what's required. No bundled cleanup. No refactoring of nearby code beyond what the task demands.

### Decompose
Functions >70 lines → split (single responsibility, 20-40 lines).

### TDD cycle per behavior
**RED** — Write ONE test. Run — must FAIL for the expected reason.
**GREEN** — Write simplest passing code. Run — must PASS. No regressions.
**REFACTOR** — Duplication? Unclear names? >70 lines? Run tests after.

One test = one cycle. Multiple behaviors = separate cycles. Skip RED = test proves nothing. Skip REFACTOR = design quality lost. **If you wrote production code before the test: delete it. Start with the test.**

### Anti-Slop Self-Check (during REFACTOR)

- **Restating comments?** Delete `x += 1  # increment x` and friends.
- **Defensive try/catch on safe paths?** Remove. Only handle errors at boundaries.
- **Wrapper for nothing?** Inline functions that wrap a single call without adding logic.
- **Naming drift?** Grep for similar entities. Match conventions.
- **Dependencies for trivial ops?** Stdlib first; new deps need justification.

### Comments
Apply [Iron Rule #3](../iron-rules.md) — WHY for ambiguous/non-obvious code, no WHAT comments on clean code.

### Anti-Poisoning Verification

After each task, verify all references are grounded:
- Confirm file paths exist (Glob/Grep)
- Confirm function signatures match actual source
- Do NOT trust memory of file contents across tasks — re-read when uncertain

### Module Refactoring Discipline

**Before moving anything:**
1. `Grep` all imports of the source module across `src/` and `tests/`.
2. `Grep` all mock/patch paths referencing the source module in `tests/`.
3. Record every caller and mock path.

**After creating new modules:**
4. Update every caller's import.
5. Update every mock/patch path.
6. Run linter — zero unused/missing imports.
7. Run tests — zero `ImportError`s.

**Never claim a split complete without updating ALL callers and mock paths.**

### Progress Checkpoints (for 5+ tasks)

Every 3 completed tasks, mark `[x]` in plan file with affected files and write partial `## Implementation Log` entries. If context nears capacity, write all progress to disk and summarize.

---

## Step 2: Implement each task

For each task in `## Task Checklist`:

1. **Read relevant source files** (fresh — don't trust memory).
2. **If unclear:** STOP. Ask the user with specific questions. Do NOT guess.
3. **Run TDD cycle(s)** per behavior (RED → GREEN → REFACTOR).
4. **Update plan file** after the task:
   ```markdown
   - [x] Task N: [description]
     Files: src/file.py:15-42, tests/test_file.py (new)
   ```

---

## Step 3: 5-Step Verification Gate

**Before ANY positive claim** ("tests pass", "implementation complete", "no issues"):

1. **IDENTIFY** — What command proves this claim? Name it.
2. **RUN** — Execute the FULL command. Fresh, complete, no partial runs.
3. **READ** — Read full output. Check exit code. Count pass/fail.
4. **VERIFY** — Does the output actually confirm the claim?
   - YES → State claim WITH evidence (command + result).
   - NO → State actual status with evidence. Do NOT rationalize.
5. **CLAIM** — Only now make the assertion.

**Skip any step = lying, not verifying.** *"I'm confident"* is not a step.

---

## Step 4: Verification via inline Bash (no subagent)

Run verification commands from your language skill's config via the `Bash` tool:

- Run from project root.
- Capture FULL output. For long output (>200 lines), redirect to a temp file (e.g., `/tmp/verify-out-NNNN.log`) and read excerpts.
- Append details (or temp-file path) to plan file's `## Verification Results`.
- Keep ONLY the pass/fail summary + failing-line excerpts in your chat response.

```markdown
## Verification Results

### Iteration 1
- **Command:** `pytest tests/ -v`
- **Result:** 45/47 passed
- **Failures (from /tmp/verify-out-0015.log):**
  - `test_auth`: [error and root cause]
  - `test_validation`: [error and root cause]
- **Action:** [what was fixed]

### Final
- **Command:** `pytest tests/ -v && ruff check . && ruff format --check`
- **Result:** 47/47 passed, lint clean
```

### Tiers

- **Tier A — Projects with tests:** run all verification commands; add new tests for new/modified code first; coverage target 70-80%.
- **Tier B — Legacy without tests:** run verification commands inline. If a command mutates state (DB writes, network calls, file system changes beyond the working tree), confirm with the user before each run.
- **Language skills may define additional tiers** (e.g., Tier C for Xcode).

### Verification Honesty

Distinguish levels in the chat summary: `Tests: PASS (N/M)` · `Tests: COULD NOT RUN — [reason]. Linting: PASS` · `Tests: FAIL (N/M)`. Never report "all checks pass" if tests didn't execute. Always attempt the test command, not just the linter.

---

## Step 5: Fix-Verify cycle

If verification FAILS:

1. **Read failure details** from plan file `## Verification Results`.
2. **Code bug:** fix, re-run Step 4. Stay in this phase.
3. **Plan wrong:** return to Phase 1, get new approval, resume.
4. **Environmental:** document, ask user.

**Regression guard:** Track pass/fail across iterations. Net regression → STOP and reassess. Two consecutive regressions → return to Phase 1.

**After fix-verify cycle:** Run `/compact` before re-running.

---

## Step 6: Final Implementation Log

After all tasks complete and verification PASS, append `## Implementation Log` to plan file:

```markdown
## Implementation Log

### Task 1: [name]
- **Approach:** [why this, not alternatives]
- **TDD cycles:** [N — omit for single-cycle]
- **Refactoring:** [what improved — omit if none]
- **Discoveries:** [unexpected findings]
- **Decisions:** [design choices and rationale]

### Notes
[Cross-cutting observations, suggestions for future work]
```

Update chronicle (if created in Phase 2) with discoveries from Implementation Log.

---

## Quality Checklist (before claiming COMPLETE)

Each row maps to an [Iron Rule](../iron-rules.md) pillar — if you can't check a row, that's a real gap, not a formality.

- [ ] **Pillar 1 (simplicity):** simplest working solution; no over-engineering; no function > 70 lines
- [ ] **Pillar 2 (all signal, zero noise):** no dead code, no wrapper-for-nothing, no defensive try/catch on safe paths
- [ ] **Pillar 3 (zero regression):** verification output captured fresh this turn; 5-step gate honored
- [ ] **Pillar 5 (WHY comments):** ambiguous code has WHY; clean code has no WHAT
- [ ] **Pillar 6 (refactoring objective):** any refactor measurably improved at least one of clear/descriptive/efficient/performant/reliable/robust/maintainable
- [ ] **Rule B (TDD):** RED → GREEN → REFACTOR honored
- [ ] Plan file has Task Checklist `[x]` + Implementation Log + Verification Results

Also apply the language skill's quality checklist.

---

## Expected Artifacts

- All tasks `[x]` in plan file with affected files
- `## Implementation Log` with per-task reasoning
- `## Verification Results` with full audit trail
- Chronicle updated with discoveries
- WORKFLOW STATE: `Current Phase: 4 (Review + Finalize)`

**Gate:** State **"IMPLEMENT + VERIFY COMPLETE"** with evidence.

**→ Run `/compact` now** — this is the heaviest phase. Then proceed to Phase 4. Read `phase-4-review-finalize.md`.
