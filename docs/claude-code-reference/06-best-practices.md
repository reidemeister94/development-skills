# Claude Code Best Practices, Patterns & Power User Tips

## 1. Prompt Engineering for Claude Code

### Principles of Effective Prompts

**Be specific upfront.** Instead of "fix the login bug," try: "The checkout flow is broken for users with expired cards. Check src/payments/ for the issue, especially token refresh. Write a failing test first, then fix it."

**Provide verification criteria.** Claude performs dramatically better when it can verify its own work:
- Test cases (unit, integration, or e2e tests)
- Screenshots of expected UI
- Expected output or behavior
- Lint rules or type checking that should pass

**Give Claude rich content:**
- Use `@file.js` to reference files directly
- Paste images/screenshots directly (copy/paste or drag & drop)
- Use URLs for documentation and API references
- Pipe data: `cat error.log | claude`

**Point to sources.** Instead of "why does ExecutionFactory have such a weird api?" ask Claude to "look through ExecutionFactory's git history and summarize how its api came to be."

**Reference existing patterns.** "Look at how existing widgets are implemented. HotDogWidget.php is a good example. Follow the pattern to implement a new calendar widget."

### The Four-Phase Workflow

1. **Explore (Plan Mode):** Read files and answer questions without making changes
2. **Plan:** Create a detailed implementation plan based on the codebase
3. **Implement:** Switch to Normal Mode and code, verifying against the plan
4. **Commit:** Commit with descriptive messages and create a PR

---

## 2. CLAUDE.md Best Practices

### What to Include

Include only things Claude can't infer from code alone:

- Bash commands Claude can't guess (build systems, test runners, deploy scripts)
- Code style rules that differ from defaults
- Testing instructions and preferred test runners
- Repository etiquette (branch naming, PR conventions)
- Architectural decisions specific to your project
- Common gotchas or non-obvious behaviors

### What NOT to Include

- Anything Claude can figure out by reading code
- Standard language conventions Claude already knows
- Detailed API documentation (link to docs instead)
- File-by-file descriptions of the codebase
- Self-evident practices like "write clean code"

### Structure Example

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible
- Use 2-space indentation

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, not the whole test suite, for performance

# Build
- Run `npm run build` to compile TypeScript
- Run `npm test` to run the full test suite
- Run `npm run lint` to check code style

# Git conventions
- Feature branches: feature/short-description
- Bugfix branches: fix/issue-number-or-short-description
```

### Import Additional Files

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

### Multi-Level CLAUDE.md Files

- **Home folder** (`~/.claude/CLAUDE.md`): Applies to all sessions
- **Project root** (`./CLAUDE.md`): Check into git to share with your team
- **Project local** (`./CLAUDE.local.md`): Not checked in; personal preferences
- **Parent directories**: For monorepos
- **Child directories**: Pulled in on-demand

### When Claude Ignores Instructions

- **File is probably too long.** Important rules get lost in noise. Ruthlessly prune.
- **Phrasing is ambiguous.** Try rephrasing with emphasis ("IMPORTANT" or "YOU MUST")
- **Test changes.** Verify Claude's behavior actually shifts after CLAUDE.md edits.

---

## 3. Workflow Patterns

### Plan-Then-Implement

Best for multi-file changes, unfamiliar code, or complex requirements:
1. Start in Plan Mode with specific context
2. Let Claude analyze the codebase
3. Review the plan - discuss edge cases
4. Switch to Normal Mode and implement
5. Verify incrementally - run tests after each phase
6. Create a PR

### Test-Driven Development

1. Write failing tests first
2. Ask Claude to implement code to make tests pass
3. Run full test suite for regressions
4. Refactor with tests as safety net

### Writer/Reviewer Pattern

Use multiple sessions:
- **Session A (Writer):** "Implement a rate limiter"
- **Session B (Reviewer):** "Review the rate limiter. Look for edge cases, race conditions."
- **Session A:** "Address review feedback: [paste Session B output]"

Fresh context prevents bias toward code that was just written.

### Incremental Implementation

1. Implement and test one file at a time
2. Verify tests pass before moving to the next
3. Course-correct early
4. `/clear` between unrelated phases

---

## 4. Performance Optimization

### Context Window Management (Most Important)

Claude's context window fills fast and performance degrades as it fills.

**Strategies:**
- Run `/context` frequently to see what's consuming space
- Use `/clear` between unrelated tasks
- Use subagents for high-volume operations (tests, research)
- Use skills for domain knowledge instead of putting everything in CLAUDE.md
- Use hooks to preprocess data (filter logs to errors only)

**During long sessions:**
- Context is automatically compacted when you approach limits
- Add a "Compact Instructions" section to CLAUDE.md to control what's preserved
- Or run `/compact Focus on API changes` for manual compaction

**MCP server overhead:**
- Each MCP server adds tool definitions to every request, consuming context
- Run `/mcp` to see configured servers
- Disable unused servers
- Prefer CLI tools (`gh`, `aws`, `gcloud`) over MCP servers when available

### Model Selection

- **Sonnet:** Handles most coding tasks well and costs less. Default choice.
- **Opus:** Reserve for complex architectural decisions or multi-step reasoning.
- **Haiku:** Fast and cheap for simple subagent tasks.
- Use `/model` to switch mid-session

### Extended Thinking

- For Opus 4.6: Uses adaptive reasoning with effort levels (low, medium, high)
- For other models: Fixed thinking budget (up to 31,999 tokens)
- Toggle with `Option+T` (macOS) or `Alt+T`
- Better at complex architectural decisions and debugging

---

## 5. Token/Cost Optimization

### Cost Tracking

Use `/cost` to check token usage for the current session.

### Strategies

1. **Manage context proactively** - `/clear` between tasks, custom compaction
2. **Choose the right model** - Sonnet for most work, Opus only for complex reasoning
3. **Reduce MCP overhead** - Prefer CLI tools, disable unused servers
4. **Install code intelligence plugins** - Precise symbol navigation saves tokens
5. **Offload to hooks/skills** - Preprocess data, inject knowledge on-demand
6. **Move instructions from CLAUDE.md to skills** - Skills load only when invoked
7. **Delegate verbose operations to subagents** - Output stays in subagent context
8. **Write specific prompts** - Vague requests trigger broad scanning
9. **Plan before coding** - Prevents expensive rework
10. **Test incrementally** - Catches issues early when cheap to fix

### Average Costs

- Daily average: ~$6 per developer per day
- 90% of users: Below $12 per day
- Team average: ~$100-200/developer per month with Sonnet

---

## 6. Multi-File Editing Patterns

### Safe Large Refactors

1. Use Plan Mode first to identify all affected files
2. Review the plan before execution
3. Implement related files in one pass
4. Run tests after each major change
5. Stop immediately if tests fail (use `/rewind`)

### Monorepo Patterns

Use nested CLAUDE.md files:

```
my-monorepo/
├── CLAUDE.md (general instructions)
├── packages/
│   ├── frontend/
│   │   └── .claude/CLAUDE.md (React/frontend-specific)
│   └── backend/
│       └── .claude/CLAUDE.md (API/backend-specific)
```

### Fan-Out Pattern (Large Migrations)

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

Test on 2-3 files first, then run at scale.

---

## 7. Testing Integration

### Test-Driven Approach

1. Write failing tests first
2. Ask Claude to implement to make tests pass
3. Run full test suite for regressions
4. Refactor with tests as safety net

### Effective Test Specifications

Instead of "write a test for foo.py", use: "write a test for foo.py covering the edge case where the user is logged out. avoid mocks."

Be specific about:
- Which functions/modules to test
- Edge cases or scenarios to cover
- Test framework and assertion style
- Whether to use mocks or real implementations

---

## 8. Code Review Workflows

### Single-Session Review

```
Review my recent changes for security issues and code quality.
Check for edge cases I might have missed.
```

### Multi-Session Review (Recommended)

**Session A (Writer):** "Implement a feature"
**Session B (Reviewer):** "Review the implementation in @src/auth/oauth.ts"

Fresh context prevents bias.

### Code Review Subagents

```markdown
---
name: security-reviewer
description: Security-focused code review
tools: Read, Grep, Glob, Bash
model: opus
---

You are a senior security engineer reviewing code for vulnerabilities.
Check for injection attacks, authentication flaws, secrets, insecure data handling.
```

---

## 9. CI/CD Integration

### GitHub Actions

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Headless Mode

```bash
# Run without interactive UI
claude -p "Analyze security issues in recent changes"

# Pipe data
cat error.log | claude -p "Explain this error"

# Structured output for scripts
claude -p "List all API routes" --output-format json | jq '.[].route'

# With options
claude -p "Fix failing tests" --max-turns 5 --model opus
```

### Cost Management in CI

- Use `--max-turns` to limit conversation length
- Specify a model: `--model sonnet`
- Use plan mode for analysis: `--permission-mode plan`
- Configure appropriate timeouts

---

## 10. Team Collaboration

### Sharing CLAUDE.md

Check `./CLAUDE.md` into git so your team follows the same conventions.

### Sharing Skills

Create project-level skills in `.claude/skills/` and check them into git.

### Sharing Subagents

Project subagents in `.claude/agents/` are shared the same way.

### Team Settings (Managed)

Deploy to:
- **macOS:** `/Library/Application Support/ClaudeCode/`
- **Linux/WSL:** `/etc/claude-code/`
- **Windows:** `C:\Program Files\ClaudeCode\`

---

## 11. Security Best Practices

### Protecting Sensitive Code

Block edits to sensitive files with hooks:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "script/block-sensitive.sh" }]
      }
    ]
  }
}
```

### Exclude Sensitive Files

```json
{
  "excludeFromContext": [".env*", "secrets/**", "*.key", "credentials.json"]
}
```

### Secret Management

- Never commit secrets
- Use `.env` files (add to `.gitignore`)
- Don't paste secrets into prompts
- Use environment variables for MCP authentication

### Permission Policies

```json
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(git *)", "Edit", "Read"],
    "deny": ["Bash(rm -rf *)", "Edit(.env)"]
  }
}
```

---

## 12. Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Kitchen Sink Session | Context full of irrelevant info | `/clear` between unrelated tasks |
| Correcting Over and Over | Context polluted with failed approaches | After two failed corrections, `/clear` and rewrite prompt |
| Over-Specified CLAUDE.md | >500 lines, Claude ignores half | Prune ruthlessly, move to skills |
| Trust-Then-Verify Gap | Plausible code that doesn't handle edge cases | Always provide verification (tests, screenshots) |
| Infinite Exploration | Unscoped investigation fills context | Scope investigations or use subagents |
| No Plan Mode for Complex Changes | Discover midway that approach is wrong | Use plan mode first for multi-file changes |
| Ignoring Test Output | Tests fail silently | Always ask Claude to show test output |

---

## 13. Power User Tips

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Esc` | Stop Claude mid-action (context preserved) |
| `Esc + Esc` | Open rewind menu |
| `Ctrl+O` | Toggle verbose mode |
| `Ctrl+G` | Open plan in text editor |
| `Ctrl+R` | Reverse history search |
| `Shift+Tab` | Cycle permission modes |
| `Ctrl+B` | Background a running task |
| `Tab` | Autocomplete `@` file references |
| `Option+T` / `Alt+T` | Toggle extended thinking |

### Session Management

```bash
claude --continue           # Most recent session
claude --resume             # Interactive picker
claude --resume "oauth-refactor"  # By name
claude --from-pr 456        # From PR number
```

### Worktrees for Parallel Work

```bash
claude --worktree feature-auth  # Isolated worktree
```

### Multi-Session Orchestration (Agent Teams)

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```

### Headless Mode for Automation

```bash
claude -p "Analyze security issues" --output-format json
cat error.log | claude -p "Explain this error"
```

### Shell Integration

```bash
# Quick Claude queries
alias ask='claude -p'
ask "What does this error mean: $1"

# Pipe errors
command 2>&1 | ask "Explain this error"
```

### Status Line

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/scripts/context-bar.sh"
  }
}
```

Shows context usage, duration, cost in real-time.

---

## 14. Key Principles Summary

1. **Context is your most precious resource.** Manage it aggressively with `/clear`, subagents, and skills.
2. **Verification is essential.** Give Claude tests, screenshots, or expected outputs.
3. **Plan before coding.** Use plan mode for complex changes to prevent rework.
4. **Iterate in tight loops.** Course-correct early with immediate feedback.
5. **Reuse configurations.** Check CLAUDE.md, skills, and subagents into git.
6. **Lean on subagents.** Delegate high-volume work to isolated agents.
7. **Automate with hooks.** Use hooks for deterministic workflows.
8. **Monitor costs.** Use `/cost` to track usage.
9. **Document architectural decisions.** Explain WHY in CLAUDE.md, not just HOW.
10. **Practice incrementally.** Implement one piece, test, verify, then continue.
