# Claude Code Hooks: Comprehensive Deep Dive

## 1. What are Hooks - Full Definition

**Hooks** are user-defined shell commands or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. They provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them.

**Purpose:**
- Enforce project rules automatically
- Automate repetitive tasks
- Integrate Claude Code with existing development tools
- Control Claude's behavior through structured decision points
- Format, validate, audit, and protect code

**How They Work:**
1. An event fires at a specific point in Claude Code's lifecycle
2. If configured matchers match the event context, the hook handler executes
3. The handler receives event-specific JSON data via stdin
4. The handler processes the data and returns a decision via exit codes or JSON output
5. Claude Code acts on the decision (allow, block, modify, or continue)

---

## 2. Hook Types - All Available Hook Events

### Session Lifecycle Events

**`SessionStart`** - Fires when a session begins or resumes
- When: Session startup, resume, after /clear, or after compaction
- Use for: Loading context, setting environment variables, initializing state
- Runs once per session

**`SessionEnd`** - Fires when a session terminates
- When: User logs out, session clears, or session exits
- Use for: Cleanup, logging, persisting state
- Cannot block session termination

**`PreCompact`** - Fires before context compaction
- When: Context window fills up and compaction is about to run
- Use for: Backing up context, preventing unwanted compactions
- Matcher: `manual`, `auto`

### User Input Events

**`UserPromptSubmit`** - Fires when you submit a prompt
- When: Before Claude processes the user's input
- Use for: Validating input, injecting context, blocking certain requests
- Can inject context or block the prompt

### Tool Execution Events

**`PreToolUse`** - Fires before a tool call executes
- When: Before Claude uses any tool (Bash, Read, Edit, Write, etc.)
- Use for: Blocking dangerous operations, validating commands, auto-approving safe operations
- Can block, allow, deny, or modify tool input
- Matcher: Tool name (e.g., `Bash`, `Edit`, `Write`, `mcp__github__.*`)

**`PostToolUse`** - Fires after a tool succeeds
- When: After a tool execution completes successfully
- Use for: Auto-formatting code, logging commands, running tests, validation
- Cannot undo the tool action (already executed)
- Matcher: Tool name

**`PostToolUseFailure`** - Fires after a tool fails
- When: After a tool execution fails with an error
- Use for: Recovery logging, error reporting, alternative actions
- Matcher: Tool name

**`PermissionRequest`** - Fires when a permission dialog appears
- When: Claude needs permission to use a restricted tool
- Use for: Auto-approving known-safe operations, enforcing security policies
- Matcher: Tool name
- Cannot fire in non-interactive mode (`-p`)

### Notification Events

**`Notification`** - Fires when Claude needs user attention
- When: Claude is idle, needs permission, or waits for input
- Use for: Desktop notifications, alerts, status updates
- Cannot block notifications
- Matcher: Notification type (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`)

### Subagent Events

**`SubagentStart`** - Fires when a subagent is spawned
- When: Claude delegates work to a subagent
- Use for: Logging, monitoring, setup
- Matcher: Agent type (e.g., `Bash`, `Explore`, `Plan`, or custom agent names)

**`SubagentStop`** - Fires when a subagent finishes
- When: A subagent completes its task
- Use for: Logging, cleanup, result processing
- Matcher: Agent type

### Agent Team Events

**`TeammateIdle`** - Fires when an agent team teammate is about to go idle
- When: A teammate finishes work but the team is still active
- Use for: Reassigning work, keeping teammates active
- Matcher: Not supported

**`TaskCompleted`** - Fires when a task is being marked as completed
- When: Task list item completion
- Use for: Validation, logging, downstream automation
- Matcher: Not supported

### Configuration Events

**`ConfigChange`** - Fires when a configuration file changes during a session
- When: External process or editor modifies settings/skills files
- Use for: Auditing, enforcing security policies, blocking unauthorized changes
- Matcher: Configuration source (`user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`)

### Worktree Events

**`WorktreeCreate`** - Fires when a worktree is created
- When: Via `--worktree` flag or `isolation: "worktree"` subagent setting
- Use for: Custom initialization, replacing default git behavior
- Returns custom worktree path instead of default

**`WorktreeRemove`** - Fires when a worktree is removed
- When: Session exit or subagent finishes with isolated worktree
- Use for: Cleanup, state management
- Cannot block removal

### Response Completion Events

**`Stop`** - Fires when Claude finishes responding
- When: Claude completes a response and is about to wait for input
- Use for: Validation, deciding if more work is needed, testing
- Can block (continue working) or allow (wait for input)
- Matcher: Not supported

---

## 3. Hook Configuration - Where and How Hooks Are Defined

### Hook Configuration Locations (Scope Hierarchy)

| Location | Scope | Shareable | Use Case |
|----------|-------|-----------|----------|
| `~/.claude/settings.json` | All your projects | No (local machine) | Personal hooks for all projects |
| `.claude/settings.json` | Single project | Yes (commit to repo) | Team-shared project rules |
| `.claude/settings.local.json` | Single project | No (gitignored) | Local machine overrides |
| Plugin `hooks/hooks.json` | When plugin enabled | Yes (bundled) | Distribute with plugins |
| Skill/Agent frontmatter | While active | Yes (in component) | One-off task-specific hooks |
| Managed policy settings | Organization-wide | Yes (admin-controlled) | Enterprise-wide rules |

### JSON Format - Complete Configuration Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "pattern|regex",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "timeout": 600,
            "async": false
          },
          {
            "type": "prompt",
            "prompt": "Evaluate this condition...",
            "model": "claude-opus-4-6",
            "timeout": 30
          },
          {
            "type": "agent",
            "prompt": "Verify this with tools...",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Hook Configuration Fields

#### Common Fields (All Hook Types)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"command"`, `"prompt"`, or `"agent"` |
| `timeout` | number | No | Max seconds before canceling. Defaults: 600 (command), 30 (prompt), 60 (agent) |
| `async` | boolean | No | For commands only. Run in background without blocking |

#### Command Hook Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string | Yes | Shell command to execute. Receives JSON on stdin. |

#### Prompt Hook Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Instructions for Claude model to make a decision |
| `model` | string | No | Model to use. Default: `claude-haiku-4-5-20251001` |
| `timeout` | number | No | Seconds before timeout. Default: 30 |

#### Agent Hook Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Instructions for the subagent. Supports `$ARGUMENTS` placeholder |
| `model` | string | No | Model to use. Default: `claude-opus-4-6` |
| `timeout` | number | No | Seconds before timeout. Default: 60 |

---

## 4. Hook Matchers - Matching Specific Tools and Patterns

### Matcher Syntax

Matchers use **regex patterns** (ripgrep syntax) to filter which hook fires. They're case-sensitive.

### What Each Event Matches On

| Event | Matches On | Example Values |
|-------|-----------|-----------------|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` | Tool name | `Bash`, `Edit\|Write`, `Read`, `mcp__.*` |
| `SessionStart` | Session source | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | Session end reason | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` |
| `Notification` | Notification type | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `SubagentStart`, `SubagentStop` | Agent type | `Bash`, `Explore`, `Plan`, custom agent names |
| `PreCompact` | Compaction trigger | `manual`, `auto` |
| `ConfigChange` | Config source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | None | Hooks always fire |

### Matcher Examples

```json
// Match built-in tools
{ "matcher": "Bash" }

// Match multiple tools with OR
{ "matcher": "Edit|Write" }

// Match MCP tools
{ "matcher": "mcp__github__.*" }

// Match notification types
{ "matcher": "permission_prompt" }

// Match session sources
{ "matcher": "compact" }

// Empty matcher - fires on ALL occurrences
{ "matcher": "" }
```

### Common MCP Tool Naming Patterns

MCP tools use the format: `mcp__<server>__<tool>`

Examples:
- `mcp__github__search_repositories`
- `mcp__github__create_pull_request`
- `mcp__postgres__query_database`
- `mcp__filesystem__read_file`

---

## 5. Hook Commands - Environment Variables

### Available Environment Variables

#### Special Claude Variables

| Variable | Available In | Value |
|----------|-------------|-------|
| `CLAUDE_PROJECT_DIR` | All command hooks | Absolute path to project root |
| `CLAUDE_PLUGIN_ROOT` | Plugin hooks | Plugin's root directory |
| `CLAUDE_ENV_FILE` | SessionStart hooks only | Path to environment file |
| `CLAUDE_CODE_REMOTE` | All hooks (if remote) | `"true"` in web, unset in CLI |

### Hook Input as JSON on stdin

Every hook receives complete context as JSON:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/sarah/myproject",
  "hook_event_name": "PreToolUse",
  "hook_event_timestamp": "2026-02-25T14:30:00Z",
  "tool_name": "Bash",
  "tool_input": { "command": "npm test" }
}
```

### Referencing Scripts

Use environment variables for portable paths:

```json
{
  "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate.sh"
}
```

### Persist Environment Variables (SessionStart only)

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG=1' >> "$CLAUDE_ENV_FILE"
fi
```

---

## 6. Hook Responses - Approve, Deny, or Modify

### Exit Code Meanings

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| **0** | Success/Allow | Action proceeds. JSON output on stdout is parsed for decisions. |
| **2** | Block/Deny | Action is blocked. Stderr message is fed back to Claude as error. |
| **Any other** | Error (allow) | Action proceeds. Stderr logged but not shown to Claude. |

### JSON Output Formats

#### Top-Level `decision` Format (Most Events)

Used by: `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop`, `ConfigChange`

```json
{
  "decision": "block",
  "reason": "Why this was blocked"
}
```

#### `hookSpecificOutput` for PreToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Reason for decision",
    "modifiedToolInput": {
      "command": "safer version of the command"
    },
    "additionalContext": "Extra context for Claude"
  }
}
```

**`permissionDecision` values:**
- `"allow"`: Proceed without permission prompt
- `"deny"`: Cancel the tool call
- `"ask"`: Show permission prompt to user (default behavior)

#### `hookSpecificOutput` for PermissionRequest

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow"
    },
    "modifiedToolInput": {
      "command": "modified command"
    }
  }
}
```

#### Prompt and Agent Hook Output

```json
{ "ok": true }
// or
{ "ok": false, "reason": "Why the action was blocked" }
```

### Decision Control Summary

| Event | Response Field | Values |
|-------|---|---|
| `PreToolUse` | `hookSpecificOutput.permissionDecision` | `allow`, `deny`, `ask` |
| `PermissionRequest` | `hookSpecificOutput.decision.behavior` | `allow`, `deny` |
| `UserPromptSubmit`, `PostToolUse`, `Stop`, etc. | `decision` | `block` (to block) |
| `Prompt/Agent hooks` | `ok` | `true` or `false` |

---

## 7. Hook Best Practices

1. **Use Absolute Paths** - Always use `$CLAUDE_PROJECT_DIR` for portable script references
2. **Keep Hooks Fast** - SessionStart hooks run on every session; use `async: true` for long tasks
3. **Handle Errors Gracefully** - Exit code 2 to block with user-friendly stderr message
4. **Avoid Shell Profile Output** - Wrap echo in `if [[ $- == *i* ]]; then ... fi` in `.zshrc`
5. **Security - Validate Input** - Whitelist patterns rather than blacklisting dangerous ones
6. **Deduplication** - Claude Code auto-deduplicates identical hook commands
7. **Async Hooks for Long Operations** - Set `"async": true` for background tasks
8. **Test Before Deployment** - Test hooks manually: `echo '{}' | ./hook.sh`
9. **Use `/hooks` Menu** - Interactive configuration, validation, and testing
10. **Document Hook Purpose** - Add comments or use skill frontmatter

---

## 8. Hook Examples

### Desktop Notifications (macOS)

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Auto-Formatting with Prettier

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### Block Protected Files

**Script:** `.claude/hooks/protect-files.sh`
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/" ".env.local")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

### Re-Inject Context After Compaction

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: Use TypeScript strict mode. Run pnpm test before committing.'"
          }
        ]
      }
    ]
  }
}
```

### Block Dangerous Commands

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

DANGEROUS_PATTERNS=("rm -rf" "drop table" "DELETE FROM" ":!rm")

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "Blocked: Command matches dangerous pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

### Validate Tests Pass Before Stopping (Agent Hook)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Run the test suite and verify all tests pass. Use Bash to run tests and Read to check output. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### Command Logging

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

---

## 9. Advanced Hook Patterns

### Hook Chaining

Multiple hooks run in parallel for the same event:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh", "timeout": 30 },
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint.sh", "timeout": 30 },
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/test.sh", "async": true, "timeout": 120 }
        ]
      }
    ]
  }
}
```

### Multi-Stage Validation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.sh" }]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-files.sh" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.sh" }]
      }
    ]
  }
}
```

### Agent-Based Validation

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify completeness: 1) Check tests pass. 2) Check coverage >80%. 3) Verify no TODO comments remain. Return {\"ok\": true} if all pass.",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## 10. Quick Reference Tables

### Hook Events Quick Reference

| Event | Fires When | Can Block? | Matcher Type |
|-------|-----------|-----------|--------------|
| `SessionStart` | Session begins/resumes | Yes | Source |
| `UserPromptSubmit` | User submits prompt | Yes | None |
| `PreToolUse` | Before tool execution | Yes | Tool name |
| `PermissionRequest` | Permission dialog | Yes | Tool name |
| `PostToolUse` | Tool succeeds | No | Tool name |
| `PostToolUseFailure` | Tool fails | No | Tool name |
| `Notification` | Claude needs attention | No | Notification type |
| `SubagentStart` | Subagent spawned | No | Agent type |
| `SubagentStop` | Subagent finishes | No | Agent type |
| `Stop` | Claude finishes responding | Yes | None |
| `TeammateIdle` | Team member idles | Yes | None |
| `TaskCompleted` | Task marked complete | Yes | None |
| `ConfigChange` | Config file changes | Yes | Config source |
| `WorktreeCreate` | Worktree created | Yes | None |
| `WorktreeRemove` | Worktree removed | No | None |
| `PreCompact` | Before compaction | Yes | Trigger |
| `SessionEnd` | Session terminates | No | End reason |

### Troubleshooting Reference

| Problem | Cause | Solution |
|---------|-------|----------|
| Hook not firing | Matcher doesn't match | Run `/hooks`, verify case-sensitive matcher |
| "command not found" | Path not absolute | Use `$CLAUDE_PROJECT_DIR` |
| JSON validation failed | Shell profile has echo | Wrap echo in interactive check |
| Hook timeout | Script too slow | Increase `timeout` field |
| Stop hook infinite loop | Not checking `stop_hook_active` | Parse field from stdin |
| Async hook still blocking | `async: true` not set | Ensure it's in hook config |
