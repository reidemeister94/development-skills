# COMPREHENSIVE CLAUDE CODE CONFIGURATION & ADVANCED FEATURES DEEP-DIVE

## Table of Contents

1. [CLAUDE.md Files - Complete Specification](#1-claudemd-files-complete-specification)
2. [Settings Files - All Available Settings](#2-settings-files-all-available-settings)
3. [Slash Commands - Complete Reference](#3-slash-commands-complete-reference)
4. [Keyboard Shortcuts & Customization](#4-keyboard-shortcuts--customization)
5. [Permission Modes & System](#5-permission-modes--system)
6. [IDE Integrations](#6-ide-integrations)
7. [CLI Flags & Options](#7-cli-flags--options)
8. [Environment Variables](#8-environment-variables)
9. [Context Management & Compression](#9-context-management--compression)
10. [Model Selection & Configuration](#10-model-selection--configuration)
11. [Cost Management & Tracking](#11-cost-management--tracking)
12. [Git Integration](#12-git-integration)
13. [Project Initialization](#13-project-initialization)
14. [Advanced CLI Usage & Scripting](#14-advanced-cli-usage--scripting)
15. [Debugging Claude Code](#15-debugging-claude-code)
16. [Security Model & Sandboxing](#16-security-model--sandboxing)

---

## 1. CLAUDE.md Files - Complete Specification

### Overview

CLAUDE.md files store persistent instructions and context for Claude Code that persist across sessions. They form a hierarchical system where more specific scopes override broader ones.

### Memory Type Hierarchy

| Memory Type | Location | Purpose | Shared | Scope |
|---|---|---|---|---|
| **Managed Policy** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux), `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows) | Organization-wide instructions managed by IT/DevOps | All users in organization | Highest priority |
| **Project CLAUDE.md** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions for the project | Via source control (git) | Project scope |
| **Project Rules** | `./.claude/rules/*.md` | Modular, topic-specific instructions | Via source control (git) | Project scope |
| **User CLAUDE.md** | `~/.claude/CLAUDE.md` | Personal preferences across all projects | Just you | All your projects |
| **Project Local** | `./CLAUDE.local.md` | Personal project-specific preferences | Just you (gitignored) | Current project only |
| **Auto Memory** | `~/.claude/projects/<project>/memory/` | Claude's automatic notes and learnings | Just you (per-project) | Current project only |

### Loading and Inheritance Rules

1. CLAUDE.md files in the directory hierarchy **above** the working directory are loaded in **full** at launch
2. CLAUDE.md files in **child directories** load **on demand** when Claude reads files in those directories
3. More specific instructions take precedence over broader ones
4. Auto memory loads only the **first 200 lines** of `MEMORY.md` into every session
5. All `.md` files in `.claude/rules/` are automatically discovered and loaded recursively

### CLAUDE.md Import Syntax

CLAUDE.md files support importing additional files using `@path/to/file` syntax:

```markdown
# Project Overview
See @README for overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- API standards: @~/.claude/api-standards.md

# Important Rules
Remember these principles @.claude/rules/general.md
```

**Import behavior:**
- Relative paths resolve relative to the file containing the import, not the working directory
- Both relative and absolute paths are allowed
- Max depth: 5 hops of recursive imports
- One-time approval dialog on first encounter (can be declined per-project)
- Imports are NOT evaluated inside markdown code spans or code blocks

### Path-Specific Rules in `.claude/rules/`

Rules can be scoped to specific files using YAML frontmatter:

```markdown
---
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"
---

# TypeScript Rules

- Use strict type checking
- All functions must have return type annotations
- Prefer interfaces over type aliases
```

**Glob patterns supported:**
- `**/*.ts` - All TypeScript files in any directory
- `src/**/*` - All files under src/ directory
- `*.md` - Markdown files in project root
- `src/components/*.tsx` - React components in specific directory
- `{src,lib}/**/*.ts` - Brace expansion for multiple paths

### Auto Memory System

Claude automatically records learnings and patterns:

**What Claude remembers:**
- Project patterns (build commands, test conventions, code style)
- Debugging insights (solutions to tricky problems, common error causes)
- Architecture notes (key files, module relationships, abstractions)
- Your preferences (communication style, workflow habits, tool choices)

**Storage structure:**
```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 200-line concise index (loaded into every session)
├── debugging.md       # Detailed debugging notes
├── api-conventions.md # API design decisions
└── ...                # Topic-specific files
```

**Management:**
- Enable/disable with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` (force on) or `1` (force off)
- Use `/memory` command to open and edit memory files
- Claude automatically reads and writes memory throughout sessions
- Topic files like `debugging.md` are loaded on-demand, not at startup

### Best Practices for CLAUDE.md

1. **Be specific**: "Use 2-space indentation" beats "Format code properly"
2. **Use structure**: Group related memories under descriptive markdown headings
3. **Keep it current**: Update as your project evolves
4. **Keep it concise**: Keep base CLAUDE.md under ~500 lines; move detailed instructions to skills
5. **Use rules files**: For larger projects, organize into `.claude/rules/` directory
6. **Import wisely**: Use imports for shared, reusable instructions across projects

### Initialization

Bootstrap a CLAUDE.md for your codebase:

```bash
claude /init
```

This walks you through creating a project-specific CLAUDE.md with key instructions.

---

## 2. Settings Files - All Available Settings

### File Locations by Scope

| Feature | User | Project | Local |
|---------|------|---------|-------|
| **Settings** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| **Subagents** | `~/.claude/agents/` | `.claude/agents/` | — |
| **MCP servers** | `~/.claude.json` | `.mcp.json` | per-project |
| **Plugins** | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` |
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` or `.claude/CLAUDE.md` | `CLAUDE.local.md` |

### Managed Settings Locations

**Delivered from Anthropic's servers:**
- Via Claude.ai admin console

**OS-level policies:**
- **macOS**: `com.anthropic.claudecode` managed preferences domain (via Jamf, Kandji, etc.)
- **Windows**: `HKLM\SOFTWARE\Policies\ClaudeCode` registry key or `HKCU\SOFTWARE\Policies\ClaudeCode`

**File-based:**
- **macOS**: `/Library/Application Support/ClaudeCode/`
- **Linux/WSL**: `/etc/claude-code/`
- **Windows**: `C:\Program Files\ClaudeCode\`

### Settings Precedence (Highest to Lowest)

1. **Managed** - Cannot be overridden (highest priority)
2. **Command line arguments** - Temporary session overrides
3. **Local** - Project-specific personal settings (`.claude/*.local.*`)
4. **Project** - Team-shared settings (`.claude/`)
5. **User** - Global personal settings (`~/.claude/`)

### Complete Settings Reference

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  // API & Authentication
  "apiKeyHelper": "/bin/generate_temp_api_key.sh",
  "forceLoginMethod": "claudeai",  // or "console"
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",

  // Permissions & Security
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Read(~/.zshrc)",
      "WebFetch(domain:github.com)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "WebFetch",
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "additionalDirectories": ["../docs/"],
    "defaultMode": "acceptEdits",  // or "plan", "dontAsk", "bypassPermissions"
    "disableBypassPermissionsMode": "disable"
  },

  // Sandboxing (Linux, macOS, WSL2)
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "allowUnsandboxedCommands": false,
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true,
      "allowAllUnixSockets": false,
      "allowManagedDomainsOnly": false,
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    },
    "enableWeakerNestedSandbox": false
  },

  // Environment & Context
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com"
  ],

  // Model Configuration
  "model": "claude-sonnet-4-6",
  "availableModels": ["sonnet", "haiku"],
  "effortLevel": "high",  // low, medium, high (Opus 4.6 only)
  "alwaysThinkingEnabled": true,

  // Attribution
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  },

  // File Operations
  "respectGitignore": true,
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  },

  // Status Line & UI
  "statusLine": {
    "type": "command",
    "command": "~/.claude/scripts/context-bar.sh"
  },
  "outputStyle": "Explanatory",
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting"]
  },
  "spinnerTipsEnabled": true,
  "spinnerTipsOverride": {
    "excludeDefault": true,
    "tips": ["Use tool X"]
  },
  "language": "japanese",

  // Sessions & Context
  "cleanupPeriodDays": 30,
  "plansDirectory": "./plans",
  "showTurnDuration": true,
  "prefersReducedMotion": true,
  "terminalProgressBarEnabled": true,

  // Hooks
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs attention\"'"
          }
        ]
      }
    ]
  },
  "disableAllHooks": false,
  "allowManagedHooksOnly": false,

  // MCP & External Tools
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": ["memory", "github"],
  "disabledMcpjsonServers": ["filesystem"],
  "allowedMcpServers": [
    { "serverName": "github" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ],
  "allowManagedMcpServersOnly": false,

  // Plugins
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  },
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    }
  ],
  "blockedMarketplaces": [
    {
      "source": "github",
      "repo": "untrusted/plugins"
    }
  ],

  // AWS & Cloud
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "awsCredentialExport": "/bin/generate_aws_grant.sh",

  // Telemetry & Monitoring
  "otelHeadersHelper": "/bin/generate_otel_headers.sh",

  // Advanced
  "autoUpdatesChannel": "stable",  // or "latest"
  "teenageMate": "auto"  // or "in-process", "tmux"
}
```

### Permission Rule Syntax Details

**Format**: `Tool` or `Tool(specifier)`

**Wildcard patterns (Bash only):**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",           // Commands starting with "npm run"
      "Bash(git * main)",           // Commands with git and main
      "Bash(* --version)",          // Commands ending with --version
      "Bash(ls *)",                 // Enforces word boundary (ls -la ✓, lsof ✗)
      "Bash(ls*)"                   // No word boundary (ls -la ✓, lsof ✓)
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

**File path rules:**
```json
{
  "permissions": {
    "allow": [
      "Read(~/.zshrc)",            // Home directory
      "Edit(/src/**/*.ts)",         // Project root relative
      "Read(//Users/alice/docs)",   // Absolute filesystem path
      "Read(src/*)",                // Current directory relative
      "Edit(docs/**)"               // Recursive pattern
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.aws/**)"
    ]
  }
}
```

**Tool-specific patterns:**
```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:github.com)",
      "mcp__github__search_repositories",
      "mcp__github__*",             // All GitHub MCP tools
      "mcp__*__write*",             // Write tools from any MCP server
      "Task(Explore)",              // Specific subagent
      "Task(my-custom-agent)"       // Custom subagent
    ]
  }
}
```

### Verify Active Settings

```bash
/status  # Shows which settings sources are active
/config  # Opens interactive settings UI
```

---

## 3. Slash Commands - Complete Reference

### Core Session Management

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/clear` | `/clear` | Clear conversation history (keeps code changes) |
| `/exit` | `/exit` | Exit the REPL session |
| `/rename` | `/rename <name>` | Rename current session for easier identification |
| `/resume` | `/resume [session]` | Resume a conversation by ID or name, or open picker |
| `/teleport` | `/teleport` | Resume a remote session from claude.ai (subscribers) |
| `/desktop` | `/desktop` | Hand off CLI session to Claude Code Desktop app (macOS, Windows) |

### Context & Performance

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/compact` | `/compact [instructions]` | Compact conversation with optional focus instructions |
| `/context` | `/context` | Visualize current context usage as a colored grid |
| `/cost` | `/cost` | Show token usage statistics and costs |
| `/stats` | `/stats` | Visualize daily usage, session history, streaks, model preferences |
| `/usage` | `/usage` | Show plan usage limits and rate limit status (subscribers) |

### Model & Configuration

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/model` | `/model [alias\|name]` | Select or change AI model (use arrows to adjust effort) |
| `/plan` | `/plan` | Enter plan mode directly from prompt |
| `/config` | `/config` | Open the Settings interface (Config tab) |
| `/status` | `/status` | Open Settings interface showing version, model, account, connectivity |
| `/permissions` | `/permissions` | View or update permissions |

### Debugging & Help

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/debug` | `/debug [description]` | Troubleshoot current session by reading debug log |
| `/doctor` | `/doctor` | Check health of Claude Code installation |
| `/help` | `/help` | Get usage help |
| `/hooks` | `/hooks` | Manage and view configured hooks |
| `/memory` | `/memory` | Edit CLAUDE.md memory files |

### File & Output Operations

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/export` | `/export [filename]` | Export current conversation to file or clipboard |
| `/copy` | `/copy` | Copy last assistant response to clipboard |

### Session Control

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/rewind` | `/rewind` | Rewind conversation and/or code, or summarize from message |
| `/tasks` | `/tasks` | List and manage background tasks |
| `/todos` | `/todos` | List current TODO items |

### Integrations & Tools

| Command | Syntax | Purpose |
|---------|--------|---------|
| `/mcp` | `/mcp` | Manage MCP server connections and OAuth authentication |
| `/theme` | `/theme` | Change the color theme |
| `/vim` | `/vim` | Enable/disable vim-style editing |
| `/statusline` | `/statusline` | Set up Claude Code's status line UI |
| `/init` | `/init` | Initialize project with CLAUDE.md guide |

### MCP Prompts

MCP servers can expose prompts that appear as commands:
- Format: `/mcp__<server>__<prompt>`
- Dynamically discovered from connected servers
- Example: `/mcp__github__search_repositories`

### Quick Commands at Prompt

| Prefix | Purpose | Example |
|--------|---------|---------|
| `/` | Trigger command or skill | `/debug`, `/model` |
| `!` | Run bash command directly | `! npm test` |
| `@` | File path mention/autocomplete | `@src/app.ts` |

---

## 4. Keyboard Shortcuts & Customization

### General Controls

| Shortcut | Action | Context |
|----------|--------|---------|
| `Ctrl+C` | Cancel current input or generation | Standard interrupt |
| `Ctrl+D` | Exit Claude Code session | EOF signal |
| `Ctrl+L` | Clear terminal screen | Keeps conversation history |
| `Ctrl+G` | Open in default text editor | Edit prompt in external editor |
| `Ctrl+O` | Toggle verbose output | Shows detailed tool usage |
| `Ctrl+R` | Reverse search command history | Interactive history search |
| `Ctrl+V` / `Cmd+V` / `Alt+V` | Paste image from clipboard | Paste image or image file path |
| `Ctrl+B` | Background running tasks | Move commands to background |
| `Ctrl+T` | Toggle task list | Show/hide task list |
| `Ctrl+F` | Kill all background agents | Double-press within 3s to confirm |
| `Left/Right arrows` | Cycle through dialog tabs | Permission dialogs, menus |
| `Up/Down arrows` | Navigate command history | Recall previous inputs |
| `Esc + Esc` | Rewind or summarize | Restore code/conversation to previous point |
| `Shift+Tab` | Toggle permission modes | Switch Auto-Accept, Plan, Normal |
| `Alt+P` / `Cmd+P` | Switch model | Switch models without clearing prompt |
| `Alt+T` / `Cmd+T` | Toggle extended thinking | Enable/disable extended thinking |

### Text Editing

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete entire line |
| `Ctrl+Y` | Paste deleted text |
| `Alt+Y` | Cycle paste history (after Ctrl+Y) |
| `Alt+B` | Move cursor back one word |
| `Alt+F` | Move cursor forward one word |

### Multiline Input Methods

| Method | Shortcut | Terminal Support |
|--------|----------|------------------|
| Quick escape | `\ + Enter` | All terminals |
| macOS default | `Option+Enter` | macOS |
| Standard | `Shift+Enter` | iTerm2, WezTerm, Ghostty, Kitty |
| Control sequence | `Ctrl+J` | All terminals (line feed) |
| Paste mode | Paste directly | Code blocks, logs |

### Vim Mode

Enable with `/vim` command or configure permanently via `/config`.

**Mode Switching:**
| Command | Action |
|---------|--------|
| `Esc` | Enter NORMAL mode from INSERT |
| `i` | Insert before cursor |
| `I` | Insert at beginning of line |
| `a` | Insert after cursor |
| `A` | Insert at end of line |
| `o` | Open line below |
| `O` | Open line above |

**Navigation (NORMAL mode):**
| Command | Action |
|---------|--------|
| `h/j/k/l` | Move left/down/up/right |
| `w` | Next word |
| `e` | End of word |
| `b` | Previous word |
| `0` | Beginning of line |
| `$` | End of line |
| `^` | First non-blank character |
| `gg` | Beginning of input |
| `G` | End of input |
| `f{char}` | Jump to next character occurrence |
| `F{char}` | Jump to previous character occurrence |
| `t{char}` | Jump to before next character |
| `T{char}` | Jump to after previous character |
| `;` | Repeat last f/F/t/T motion |
| `,` | Repeat last f/F/t/T in reverse |

**Editing (NORMAL mode):**
| Command | Action |
|---------|--------|
| `x` | Delete character |
| `dd` | Delete line |
| `D` | Delete to end of line |
| `dw/de/db` | Delete word/to end/back |
| `cc` | Change line |
| `C` | Change to end of line |
| `cw/ce/cb` | Change word/to end/back |
| `yy/Y` | Yank (copy) line |
| `yw/ye/yb` | Yank word/to end/back |
| `p` | Paste after cursor |
| `P` | Paste before cursor |
| `>>` | Indent line |
| `<<` | Dedent line |
| `J` | Join lines |
| `.` | Repeat last change |

**Text Objects:**
| Command | Action |
|---------|--------|
| `iw/aw` | Inner/around word |
| `iW/aW` | Inner/around WORD (whitespace-delimited) |
| `i"/a"` | Inner/around double quotes |
| `i'/a'` | Inner/around single quotes |
| `i(/a(` | Inner/around parentheses |
| `i[/a[` | Inner/around brackets |
| `i{/a{` | Inner/around braces |

### Customizing Keybindings

**File location:**
```bash
~/.claude/keybindings.json
```

**Configuration structure:**
```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null,  // Unbind default
        "ctrl+shift+s": "chat:stash"
      }
    },
    {
      "context": "Global",
      "bindings": {
        "ctrl+h": "app:toggleTodos"
      }
    }
  ]
}
```

### Available Contexts for Keybindings

| Context | Description |
|---------|-------------|
| `Global` | Applies everywhere in the app |
| `Chat` | Main chat input area |
| `Autocomplete` | Autocomplete menu is open |
| `Settings` | Settings menu |
| `Confirmation` | Permission and confirmation dialogs |
| `Tabs` | Tab navigation components |
| `Help` | Help menu is visible |
| `Transcript` | Transcript viewer |
| `HistorySearch` | History search mode (Ctrl+R) |
| `Task` | Background task is running |
| `ThemePicker` | Theme picker dialog |
| `Attachments` | Image/attachment bar navigation |
| `Footer` | Footer indicator navigation |
| `MessageSelector` | Rewind and summarize dialog |
| `DiffDialog` | Diff viewer navigation |
| `ModelPicker` | Model picker effort level |
| `Select` | Generic select/list components |
| `Plugin` | Plugin dialog (browse, discover, manage) |

### Available Actions by Context

**App actions (Global):**
- `app:interrupt` (Ctrl+C)
- `app:exit` (Ctrl+D)
- `app:toggleTodos` (Ctrl+T)
- `app:toggleTranscript` (Ctrl+O)

**Chat actions:**
- `chat:cancel` (Escape)
- `chat:cycleMode` (Shift+Tab)
- `chat:modelPicker` (Cmd+P)
- `chat:thinkingToggle` (Cmd+T)
- `chat:submit` (Enter)
- `chat:undo` (Ctrl+\_)
- `chat:externalEditor` (Ctrl+G)
- `chat:stash` (Ctrl+S)
- `chat:imagePaste` (Ctrl+V)

**History actions:**
- `history:search` (Ctrl+R)
- `history:previous` (Up)
- `history:next` (Down)

**Keystroke syntax:**
```json
{
  "ctrl+e": "action",              // Ctrl + E
  "shift+tab": "action",            // Shift + Tab
  "meta+p": "action",               // Cmd/Meta + P
  "ctrl+shift+c": "action",         // Multiple modifiers
  "K": "action",                    // Uppercase (implies Shift)
  "ctrl+k ctrl+s": "action",        // Chord (Ctrl+K, then Ctrl+S)
  "escape": "action",               // Special keys
  "enter": "action",
  "space": "action",
  "up": "action"
}
```

### macOS Terminal Configuration

For Alt/Option key shortcuts on macOS, configure terminal:

**iTerm2:**
- Settings → Profiles → Keys → Set Left/Right Option key to "Esc+"

**Terminal.app:**
- Settings → Profiles → Keyboard → Check "Use Option as Meta Key"

**VS Code:**
- Settings → Profiles → Keys → Set Left/Right Option key to "Esc+"

### Reserved & Conflicting Shortcuts

**Cannot be rebound:**
- `Ctrl+C` - Hardcoded interrupt/cancel
- `Ctrl+D` - Hardcoded exit

**Terminal conflicts:**
- `Ctrl+B` - tmux prefix (press twice to send)
- `Ctrl+A` - GNU screen prefix
- `Ctrl+Z` - Unix process suspend (SIGTSTP)

---

## 5. Permission Modes & System

### Permission Tiering

| Tool Type | Example | Approval Required | "Yes, don't ask again" |
|-----------|---------|-------------------|----------------------|
| Read-only | File reads, Grep | No | N/A |
| Bash commands | Shell execution | Yes | Permanently per project/command |
| File modification | Edit/write files | Yes | Until session end |

### Permission Modes

Press `Shift+Tab` to cycle through modes:

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Prompts for permission on first use of each tool | Standard security |
| `acceptEdits` | Auto-accepts file edit permissions for session | Faster iteration on safe tasks |
| `plan` | Claude can analyze but not modify files or execute commands | Safe exploration before coding |
| `dontAsk` | Auto-denies tools unless pre-approved via settings | Maximum safety |
| `bypassPermissions` | Skips all permission prompts | Only in isolated environments (VMs/containers) |

**Warning:** `bypassPermissions` disables all checks. Only use in isolated environments. Administrators can prevent with `disableBypassPermissionsMode: "disable"`.

### Permission Rule Syntax

**Format:** `Tool` or `Tool(specifier)`

**Match all uses:**
```json
{
  "permissions": {
    "allow": [
      "Bash",      // All bash commands
      "WebFetch",  // All web fetches
      "Read",      // All file reads
      "Edit"       // All file edits
    ]
  }
}
```

**Fine-grained control:**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build)",
      "Bash(git commit *)",
      "Read(./.env)",
      "WebFetch(domain:example.com)"
    ],
    "deny": [
      "Bash(git push *)",
      "Read(./secrets/**)",
      "WebFetch(domain:untrusted.com)"
    ]
  }
}
```

### Bash Wildcard Patterns

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",      // npm run <anything>
      "Bash(git * main)",     // git <anything> main
      "Bash(* --version)",    // <anything> --version
      "Bash(ls *)",           // ls <anything> (enforces word boundary)
      "Bash(ls*)"             // ls<anything> (no word boundary)
    ]
  }
}
```

**Important:** Space before `*` matters:
- `Bash(ls *)` matches `ls -la` but NOT `lsof`
- `Bash(ls*)` matches both `ls -la` and `lsof`

### File Path Rules

Path patterns follow gitignore specification:

```json
{
  "permissions": {
    "allow": [
      "Read(//Users/alice/docs)",     // Absolute path
      "Read(~/Documents/*.pdf)",      // Home directory
      "Edit(/src/**/*.ts)",           // Project root relative
      "Read(*.env)",                  // Current directory relative
      "Edit(docs/**)"                 // Recursive
    ]
  }
}
```

**Pattern types:**
| Pattern | Meaning | Example |
|---------|---------|---------|
| `//path` | Absolute filesystem path | `Read(//Users/alice/secrets/**)` |
| `~/path` | Home directory | `Read(~/Documents/*.pdf)` |
| `/path` | Project root relative | `Edit(/src/**/*.ts)` |
| `path` or `./path` | Current directory | `Read(*.env)` |

### Tool-Specific Rules

**Bash:**
```json
{
  "Bash(npm run build)",
  "Bash(npm run *)",
  "Bash(git * main)"
}
```

**Read and Edit (gitignore patterns):**
```json
{
  "Read(/docs/**)",
  "Edit(src/**/*.ts)",
  "Edit(~/.zshrc)"
}
```

**WebFetch (domain matching):**
```json
{
  "WebFetch(domain:github.com)",
  "WebFetch(domain:*.npmjs.org)"
}
```

**MCP (Model Context Protocol):**
```json
{
  "mcp__github",                    // Any tool from github server
  "mcp__github__search_repositories",  // Specific tool
  "mcp__*__write*"                  // Write tools from any server
}
```

**Task (Subagents):**
```json
{
  "Task(Explore)",
  "Task(Plan)",
  "Task(my-custom-agent)"
}
```

### Managed Settings (Admin Control)

**Managed-only settings:**
- `disableBypassPermissionsMode` - Prevent bypass mode
- `allowManagedPermissionRulesOnly` - Only managed rules apply
- `allowManagedHooksOnly` - Only managed hooks
- `allowManagedMcpServersOnly` - Only managed MCP servers
- `sandbox.network.allowManagedDomainsOnly` - Only managed domains

### Working Directories

**Default:** Files in directory where Claude was launched

**Extend access:**
```bash
# CLI flag
claude --add-dir ../docs ../lib

# During session
/add-dir ../shared-config

# Persistent (settings.json)
{
  "permissions": {
    "additionalDirectories": ["../docs/", "../shared/"]
  }
}
```

### Permission Interaction with Sandboxing

**Complementary security layers:**
- **Permissions** control which tools Claude can use
- **Sandboxing** provides OS-level filesystem/network enforcement
- Both apply to Bash commands for defense-in-depth

---

## 6. IDE Integrations

### VS Code Extension

**Installation:**
1. Open VS Code
2. Go to Extensions marketplace
3. Search for "Claude Code"
4. Click Install

**Features:**
- Prompt box integrated into VS Code
- Reference files and folders in prompts
- Resume past conversations
- Manage plugins
- Chrome browser automation
- Git integration
- Diff viewer

**Key commands:**
| Command | Shortcut | Action |
|---------|----------|--------|
| Claude: Start Session | Cmd/Ctrl+Shift+C | Open Claude Code |
| Claude: Switch to Terminal | Cmd/Ctrl+Shift+T | Move to terminal mode |
| Claude: Create Commit | Cmd/Ctrl+Shift+X | Create git commit |

**Configuration:**
- Settings available via VS Code settings UI
- Edit extension settings in `.vscode/settings.json`
- Configure prompt box location, auto-save, notifications

**Unique features:**
- Resume remote sessions from claude.ai
- Run CLI in VS Code terminal
- Include terminal output in prompts
- Monitor background processes
- Git worktree integration
- Connect external tools with MCP

### JetBrains IDEs

**Supported IDEs:**
- IntelliJ IDEA
- PyCharm
- WebStorm
- Rider
- GoLand
- Clion
- RubyMine
- PhpStorm
- AppCode

**Installation:**
1. Open IDE Preferences/Settings
2. Go to Plugins
3. Search for "Claude Code"
4. Click Install

**Usage modes:**

**From IDE:**
- Invoke directly from context menu
- Auto-opens Claude Code in terminal or IDE

**From External Terminals:**
- Seamlessly integrates with external terminal usage
- Maintains context awareness

**Configuration:**
- Plugin Settings in IDE preferences
- ESC key configuration for terminal
- Remote Development setup
- WSL Configuration

**Special configurations:**
- Remote Development support
- WSL (Windows Subsystem for Linux) support
- IDE detection and integration

### General IDE Integration Patterns

**Code selection:**
- Select code, invoke Claude Code to analyze or modify

**Terminal integration:**
- IDE terminal directly invokes Claude Code
- Output streams into IDE

**Git integration:**
- View diffs directly in IDE
- Create commits and PRs from IDE

**File references:**
- Drag and drop files into Claude Code
- @mention syntax in prompts

---

## 7. CLI Flags & Options

### Session Management

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `-p, --print` | | Query via SDK, then exit | `claude -p "explain this"` |
| `-c, --continue` | | Load most recent conversation | `claude -c` |
| `-r, --resume` | `<session>` | Resume specific session | `claude -r auth-refactor` |
| `--session-id` | `<uuid>` | Use specific session ID | `claude --session-id "550e8400..."` |
| `--fork-session` | | Create new session from resume | `claude -c --fork-session` |
| `--from-pr` | `<number\|url>` | Resume from GitHub PR | `claude --from-pr 123` |
| `-w, --worktree` | `<name>` | Create/use git worktree | `claude -w feature-auth` |
| `--remote` | `<description>` | Create web session | `claude --remote "Fix login"` |
| `--teleport` | | Resume web session locally | `claude --teleport` |

### Model & Configuration

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--model` | `<alias\|name>` | Set model | `claude --model opus` |
| `--betas` | `<headers>` | Beta headers (API users) | `claude --betas interleaved-thinking` |
| `--fallback-model` | `<model>` | Fallback on overload (print mode) | `claude -p --fallback-model sonnet` |
| `--settings` | `<file\|json>` | Load settings | `claude --settings ./settings.json` |
| `--setting-sources` | `<sources>` | Settings to load | `claude --setting-sources user,project` |
| `--strict-mcp-config` | | Only use specified MCP | `claude --strict-mcp-config --mcp-config ...` |
| `--mcp-config` | `<files>` | Load MCP servers | `claude --mcp-config ./mcp.json` |

### Permissions & Security

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--permission-mode` | `<mode>` | Set permission mode | `claude --permission-mode plan` |
| `--allowedTools` | `<rules>` | Pre-approve tools | `claude --allowedTools "Bash(git *)" "Read"` |
| `--disallowedTools` | `<rules>` | Block tools | `claude --disallowedTools "Bash(git push *)"` |
| `--dangerously-skip-permissions` | | Skip all prompts | `claude --dangerously-skip-permissions` |
| `--allow-dangerously-skip-permissions` | | Enable bypass option | `claude --allow-dangerously-skip-permissions` |
| `--permission-prompt-tool` | `<tool>` | MCP tool for approvals | `claude -p --permission-prompt-tool mcp_auth_tool` |

### System Prompt Customization

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--system-prompt` | `<text>` | Replace entire system prompt | `claude --system-prompt "You are Python expert"` |
| `--system-prompt-file` | `<path>` | Load system prompt from file | `claude -p --system-prompt-file ./prompt.txt` |
| `--append-system-prompt` | `<text>` | Append to default prompt | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | `<path>` | Append file to prompt | `claude -p --append-system-prompt-file ./extra.txt` |

### Tools & Capabilities

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--tools` | `<names>` | Restrict available tools | `claude --tools "Bash,Edit,Read"` |
| `--chrome` | | Enable Chrome browser | `claude --chrome` |
| `--no-chrome` | | Disable Chrome | `claude --no-chrome` |
| `--ide` | | Auto-connect to IDE | `claude --ide` |

### Agents & Subagents

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--agent` | `<name>` | Specify agent | `claude --agent my-custom-agent` |
| `--agents` | `<json>` | Define agents dynamically | `claude --agents '{"reviewer":{"description":"...","prompt":"..."}}' ` |

### Context & Output

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--add-dir` | `<paths>` | Add working directories | `claude --add-dir ../docs ../lib` |
| `--output-format` | `<format>` | Print mode output format | `claude -p --output-format json` |
| `--input-format` | `<format>` | Input format (stream-json, text) | `claude -p --input-format stream-json` |
| `--include-partial-messages` | | Include partial streaming events | `claude -p --include-partial-messages` |
| `--json-schema` | `<schema>` | Validate JSON output | `claude -p --json-schema '{"type":"object",...}'` |

### Execution Control

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `--max-turns` | `<number>` | Limit agentic turns | `claude -p --max-turns 3` |
| `--max-budget-usd` | `<amount>` | Spending limit | `claude -p --max-budget-usd 5.00` |
| `--init` | | Run init hooks and start | `claude --init` |
| `--init-only` | | Run init hooks and exit | `claude --init-only` |
| `--maintenance` | | Run maintenance hooks and exit | `claude --maintenance` |
| `--disable-slash-commands` | | Disable skills and commands | `claude --disable-slash-commands` |
| `--no-session-persistence` | | Don't save session | `claude -p --no-session-persistence` |
| `--verbose` | | Enable verbose logging | `claude --verbose` |
| `--debug` | `[categories]` | Debug mode with filtering | `claude --debug "api,hooks"` |

### Authentication & Info

| Flag | Argument | Purpose | Example |
|------|----------|---------|---------|
| `auth login` | `[--email] [--sso]` | Sign in to Anthropic | `claude auth login --email user@example.com` |
| `auth logout` | | Log out | `claude auth logout` |
| `auth status` | `[--text]` | Show auth status | `claude auth status --text` |
| `--version, -v` | | Show version | `claude -v` |

### Other Commands

| Command | Purpose |
|---------|---------|
| `claude update` | Update to latest version |
| `claude agents` | List configured subagents |
| `claude mcp` | Configure MCP servers |
| `claude remote-control` | Start Remote Control session |

### Flag Examples

**Query with custom model:**
```bash
claude -p --model opus "explain this code"
```

**Continue with plan mode:**
```bash
claude -c --permission-mode plan
```

**Headless with JSON output:**
```bash
claude -p --output-format json "analyze logs"
```

**Piped input:**
```bash
cat logs.txt | claude -p "find errors"
```

**Resume with fork:**
```bash
claude --resume old-session --fork-session
```

**Strict settings:**
```bash
claude --settings ./settings.json --strict-mcp-config --mcp-config ./mcp.json
```

---

## 8. Environment Variables

### API & Authentication

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | API key for Claude SDK | `export ANTHROPIC_API_KEY=sk-...` |
| `ANTHROPIC_AUTH_TOKEN` | Custom Authorization header value | `export ANTHROPIC_AUTH_TOKEN=token...` |
| `ANTHROPIC_CUSTOM_HEADERS` | Custom headers (newline-separated) | `export ANTHROPIC_CUSTOM_HEADERS="Header: Value"` |

### Model Configuration

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_MODEL` | Default model | `export ANTHROPIC_MODEL=claude-opus-4-6` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus alias mapping | `export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-6` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet alias mapping | `export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku alias mapping | `export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-3-5` |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents | `export CLAUDE_CODE_SUBAGENT_MODEL=haiku` |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort level for Opus | `export CLAUDE_CODE_EFFORT_LEVEL=high` |

### Context & Performance

| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | Disable 1M context window | `export CLAUDE_CODE_DISABLE_1M_CONTEXT=1` |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Context compaction threshold (1-100) | `export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens (default: 32K, max: 64K) | `export CLAUDE_CODE_MAX_OUTPUT_TOKENS=50000` |
| `MAX_THINKING_TOKENS` | Extended thinking token budget | `export MAX_THINKING_TOKENS=31999` |

### Execution & Behavior

| Variable | Purpose | Example |
|----------|---------|---------|
| `BASH_DEFAULT_TIMEOUT_MS` | Default bash timeout | `export BASH_DEFAULT_TIMEOUT_MS=300000` |
| `BASH_MAX_OUTPUT_LENGTH` | Max bash output characters | `export BASH_MAX_OUTPUT_LENGTH=1000000` |
| `BASH_MAX_TIMEOUT_MS` | Max bash timeout | `export BASH_MAX_TIMEOUT_MS=600000` |
| `CLAUDE_CODE_SHELL` | Override shell detection | `export CLAUDE_CODE_SHELL=/bin/zsh` |
| `CLAUDE_CODE_SIMPLE` | Run with minimal system prompt | `export CLAUDE_CODE_SIMPLE=1` |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Disable/enable auto memory | `export CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable background tasks | `export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | Enable prompt suggestions | `export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=true` |
| `CLAUDE_CODE_TASK_LIST_ID` | Named task list for sessions | `export CLAUDE_CODE_TASK_LIST_ID=my-project` |
| `CLAUDE_CODE_ENABLE_TASKS` | Enable task list (prev: todos) | `export CLAUDE_CODE_ENABLE_TASKS=true` |

### Cloud Providers

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_FOUNDRY_API_KEY` | Microsoft Foundry API key | `export ANTHROPIC_FOUNDRY_API_KEY=...` |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Foundry resource name | `export ANTHROPIC_FOUNDRY_RESOURCE=myresource` |
| `AWS_BEARER_TOKEN_BEDROCK` | Bedrock API key | `export AWS_BEARER_TOKEN_BEDROCK=...` |

### MCP & Tools

| Variable | Purpose | Example |
|----------|---------|---------|
| `ENABLE_TOOL_SEARCH` | MCP tool search control | `export ENABLE_TOOL_SEARCH=auto:5` |
| `MCP_TIMEOUT` | MCP server startup timeout (ms) | `export MCP_TIMEOUT=30000` |

### Telemetry & Monitoring

| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable OpenTelemetry | `export CLAUDE_CODE_ENABLE_TELEMETRY=1` |
| `DISABLE_TELEMETRY` | Opt out of telemetry | `export DISABLE_TELEMETRY=1` |

### Updates & Maintenance

| Variable | Purpose | Example |
|----------|---------|---------|
| `DISABLE_AUTOUPDATER` | Disable auto-updates | `export DISABLE_AUTOUPDATER=1` |

### Memory & Additional Directories

| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Load CLAUDE.md from additional dirs | `export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` |

### Prompt Caching

| Variable | Purpose |
|----------|---------|
| `DISABLE_PROMPT_CACHING` | Disable all prompt caching |
| `DISABLE_PROMPT_CACHING_HAIKU` | Disable for Haiku |
| `DISABLE_PROMPT_CACHING_SONNET` | Disable for Sonnet |
| `DISABLE_PROMPT_CACHING_OPUS` | Disable for Opus |

### Setting Environment Variables

**Bash/Zsh (.bashrc, .zshrc):**
```bash
export ANTHROPIC_API_KEY="sk-..."
export CLAUDE_CODE_EFFORT_LEVEL=high
export BASH_DEFAULT_TIMEOUT_MS=300000
```

**For specific command:**
```bash
ANTHROPIC_MODEL=opus claude
```

**Persistent in ~/.claude/settings.json:**
```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "BASH_DEFAULT_TIMEOUT_MS": "300000"
  }
}
```

---

## 9. Context Management & Compression

### Context Window Overview

Claude Code has a context window that holds:
- Conversation history
- File contents
- Command outputs
- CLAUDE.md and skills
- System instructions
- MCP tool definitions

### Automatic Context Management

**When context fills up:**
1. Claude Code clears older tool outputs first
2. Then summarizes conversation if needed
3. Your requests and key code snippets are preserved
4. Detailed instructions from early conversations may be lost

**Why this matters:**
- Put persistent rules in CLAUDE.md, not conversation history
- Early instructions can get lost during compaction
- Run `/context` to see what's consuming space

### Manual Compaction

**Run compaction with focus:**
```bash
/compact focus on the API changes
/compact keep testing details, discard implementation notes
/compact preserve authorization logic
```

**What happens:**
- Messages are summarized into a concise recap
- Older conversation history is replaced with summary
- Session stays the same (not like /clear)
- Full transcripts preserved for reference

### Context Visualization

**Check current context usage:**
```bash
/context
```

Returns colored grid showing:
- Total tokens used
- Available context remaining
- What's consuming space (tools, CLAUDE.md, conversation, etc.)
- Per-MCP server costs

### Custom Compaction Instructions in CLAUDE.md

```markdown
# Compact Instructions

When you are using compact, please:
- Focus on test output and code changes
- Discard verbose debugging logs
- Preserve the final solution
- Keep architecture decisions
```

### Managing Context Costs by Feature

**MCP Servers add significant overhead:**
- Each server's tools are loaded at startup
- Tool definitions persist in context
- Check costs with `/context` and `/mcp`

**Solutions:**
- Run `/mcp` to see per-server costs
- Disable unused MCP servers
- Tool search defers tools on-demand (threshold-based)

**Skills:**
- Skill descriptions load at startup
- Full content loads on-demand
- Disable auto-invocation to save context

**Subagents:**
- Get fresh, separate context window
- Verbose operations stay isolated
- Summary returns to main conversation

### Context Reduction Strategies

1. **Clear between tasks**: Use `/clear` to start fresh for unrelated work
2. **Use smaller models for subagents**: Set `model: haiku` in subagent config
3. **Offload to skills**: Move specialized instructions from CLAUDE.md to skills
4. **Use hooks for preprocessing**: Filter large logs before Claude sees them
5. **Disable unused MCP servers**: Review with `/mcp`
6. **Install code intelligence plugins**: Reduces file reads in typed languages

### Cost Tracking

```bash
/cost  # Shows token usage and costs for current session
```

Output includes:
- Total cost in USD
- Total API duration
- Code changes (lines added/removed)

---

## 10. Model Selection & Configuration

### Available Models

| Model Alias | Current Version | Best For | Token Limit |
|-------------|-----------------|----------|------------|
| `default` | Depends on tier | Recommended default | Standard |
| `sonnet` | Claude Sonnet 4.6 | General coding | Standard or 1M |
| `opus` | Claude Opus 4.6 | Complex reasoning | Standard or 1M |
| `haiku` | Claude Haiku 3.5 | Fast, simple tasks | Standard |
| `opusplan` | Opus (plan) → Sonnet (execute) | Planning then coding | Standard or 1M |
| `sonnet[1m]` | Sonnet with 1M context | Long sessions | 1M tokens |

### Setting Your Model

**By priority:**
1. `/model <alias|name>` during session (highest priority)
2. `claude --model <alias|name>` at startup
3. `ANTHROPIC_MODEL=<alias|name>` environment variable
4. `model` field in settings.json
5. Account default (lowest priority)

**Examples:**
```bash
# At startup
claude --model opus

# During session
/model sonnet

# Environment variable
export ANTHROPIC_MODEL=haiku

# Settings file
{ "model": "opus" }
```

### Restricted Model Selection (Admin)

**In managed settings:**
```json
{
  "availableModels": ["sonnet", "haiku"]
}
```

**Behavior:**
- Users cannot switch to models outside this list
- Default model always available
- Filter matches on alias, not full model ID

**Full control:**
```json
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### Special Model Behaviors

**`default` alias:**
- Max/Team Premium: Opus 4.6
- Pro/Team Standard: Sonnet 4.6
- Enterprise: Opus 4.6 available but not default
- Auto-fallback to Sonnet if Opus usage threshold hit

**`opusplan` alias:**
- Plan mode: uses Opus 4.6
- Execution mode: switches to Sonnet 4.6
- Cost-optimized reasoning + execution

### Effort Levels (Opus 4.6 only)

Opus 4.6 supports adaptive reasoning with effort levels:

| Level | Tokens | Cost | Use Case |
|-------|--------|------|----------|
| `low` | ~5K | Lowest | Simple, straightforward tasks |
| `medium` | ~15K | Medium | Moderate complexity |
| `high` | ~31K | Highest | Complex reasoning (default) |

**Set effort level:**
1. **In `/model` menu**: Use left/right arrows to adjust slider
2. **Environment variable**: `export CLAUDE_CODE_EFFORT_LEVEL=high`
3. **Settings file**: `"effortLevel": "high"`

### Extended Context (1M tokens)

**Availability:**
- **API users**: Full access
- **Paid subscribers**: Requires extra usage enabled

**Enable:**
```bash
# Use alias
/model sonnet[1m]

# Use full name
/model claude-sonnet-4-6[1m]
```

**Disable 1M context entirely:**
```bash
export CLAUDE_CODE_DISABLE_1M_CONTEXT=1
```

**Pricing:**
- Standard rate up to 200K tokens
- Long-context pricing beyond 200K tokens
- For subscribers: billed as extra usage

### Model Version Pinning (Cloud Providers)

**For Bedrock, Vertex, Foundry deployments:**

```bash
# Bedrock
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6-v1'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-3-5-v1'

# Vertex AI
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-3-5'

# Foundry
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-3-5'
```

### Checking Current Model

```bash
/status  # Shows model, version, account info
/model   # Opens model picker (shows current model)
```

---

## 11. Cost Management & Tracking

### Token Usage Tracking

**View session costs:**
```bash
/cost  # Shows: total cost, API duration, code changes
```

**Output includes:**
```
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

**View usage patterns:**
```bash
/stats  # Shows daily usage, streaks, model preferences
/usage  # Shows subscription plan limits (subscribers only)
```

### Team Cost Management

**Set workspace spend limits** (Claude Console):
- Workspace-level spending cap
- Admin view of cost reports
- Usage tracking by user

**CloudProviders** (Bedrock, Vertex, Foundry):
- No native metrics from Claude Code
- Use LiteLLM for cost tracking by API key

### Average Costs

- **Daily**: ~$6 per developer per day (90% of users < $12/day)
- **Monthly**: ~$100-200 per developer (varies by usage)

### Rate Limit Recommendations (Per User)

| Team Size | TPM | RPM |
|-----------|-----|-----|
| 1-5 users | 200k-300k | 5-7 |
| 5-20 users | 100k-150k | 2.5-3.5 |
| 20-50 users | 50k-75k | 1.25-1.75 |
| 50-100 users | 25k-35k | 0.62-0.87 |
| 100-500 users | 15k-20k | 0.37-0.47 |
| 500+ users | 10k-15k | 0.25-0.35 |

### Context Management for Cost Reduction

**Manage context proactively:**
1. **Use `/context`** to see what's consuming tokens
2. **Clear between tasks**: `/clear` to start fresh
3. **Add custom compaction**: `/compact Focus on code changes`
4. **Move instructions to CLAUDE.md**: Session context is cleaner

**MCP server overhead:**
- Each server adds tool definitions to context
- Check with `/context` and `/mcp`
- Disable unused servers

**Code intelligence plugins:**
- Reduce file reads in typed languages
- Use precise symbol navigation instead of grep

### Reduce Token Usage

| Strategy | Benefit |
|----------|---------|
| Choose Sonnet over Opus | ~50% cost reduction |
| Reduce effort level on Opus | Scales from 5K to 31K tokens |
| Use Haiku for subagents | 80% lower cost than Sonnet |
| Offload to subagents | Verbose output stays isolated |
| Use hooks for preprocessing | Filter logs before Claude sees them |
| Keep CLAUDE.md < 500 lines | Smaller base context |
| Move instructions to skills | Load on-demand instead of every session |
| Plan before implementing | Avoid expensive re-work |
| Use specific prompts | Narrow scope = fewer file reads |

### Extended Thinking Costs

Extended thinking is enabled by default with 31,999 token budget:
- Thinking tokens = output tokens (billed same)
- Improves complex tasks significantly
- For simpler tasks, reduce budget:

```bash
export MAX_THINKING_TOKENS=8000
```

Or disable in `/config`.

### Agent Team Costs

Each teammate maintains separate context:
- ~7x more tokens than single session in plan mode
- Each teammate runs as separate Claude instance
- Keep teams small (3-4 teammates)
- Use Sonnet for teammates
- Clean up when done

### Background Token Usage

Claude uses tokens for:
- Conversation summarization (background jobs)
- Command processing (e.g., `/cost` command)
- Typically < $0.04 per session

### Cost Optimization Checklist

1. Check `/context` and `/mcp` for overhead
2. Use `/cost` to track spending
3. Choose right model for task (Sonnet for most)
4. Keep CLAUDE.md concise
5. Disable unused MCP servers
6. Use specific, focused prompts
7. Separate exploration (plan mode) from execution
8. Delegate verbose operations to subagents
9. Install code intelligence plugins
10. Clear between unrelated tasks

---

## 12. Git Integration

### Git Access

Claude Code automatically sees:
- Current branch
- Uncommitted changes (diffs)
- Recent commit history
- Git status

### Git Operations Available

**Viewing:**
```bash
git status
git log --oneline
git diff
git branch -a
```

**Commits:**
```bash
git add .
git commit -m "message"
git commit --amend
```

**Branching:**
```bash
git checkout -b new-branch
git switch existing-branch
git merge branch-name
```

**Pushing:**
```bash
git push origin current-branch
git push --force-with-lease
```

### Git Permissions

**Default behavior:**
- Git read operations (log, diff, status) are allowed by default
- Git write operations (commit, push) require permission

**Restrict git operations:**
```json
{
  "permissions": {
    "allow": [
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(git status)"
    ],
    "ask": [
      "Bash(git commit *)",
      "Bash(git push *)"
    ]
  }
}
```

### Git Worktrees

**Create isolated parallel sessions:**
```bash
claude --worktree feature-auth
claude -w  # Auto-generates worktree name
```

**Benefits:**
- Each worktree has separate directory
- Independent Claude Code sessions
- Automatic cleanup
- Separate auto memory per worktree

**Manual worktree management:**
```bash
git worktree add .claude/worktrees/branch-name
git worktree remove .claude/worktrees/branch-name
```

### Pull Requests

**GitHub integration:**
```bash
# Create PR from current branch
gh pr create --title "Fix auth bug" --body "Fixes #123"

# Link session to PR
claude --from-pr 123
```

**PR status in Claude Code:**
- Shows clickable PR link in footer
- Color indicates review status:
  - Green: approved
  - Yellow: pending review
  - Red: changes requested
  - Gray: draft
  - Purple: merged

**Requirements:**
- `gh` CLI installed
- `gh auth login` authenticated

### Commit Attribution

**Default attribution:**
```
🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Customize in settings:**
```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

### Git-based Workflows

**Common flow:**
1. Ask Claude to fix a bug
2. Claude reads diff and relevant files
3. Claude makes changes
4. Claude runs tests to verify
5. Ask Claude to commit
6. Ask Claude to push

**Multi-branch work:**
1. Create branch: `git checkout -b feature/new-feature`
2. Start Claude: `claude`
3. Work on feature
4. When done, ask Claude to commit and push
5. Create PR with `gh pr create`

---

## 13. Project Initialization

### Bootstrap CLAUDE.md

**Command:**
```bash
/init
```

**What it does:**
1. Walks you through creating project CLAUDE.md
2. Asks about tech stack, key directories, conventions
3. Generates initial CLAUDE.md file
4. Saves to `./CLAUDE.md` or `./.claude/CLAUDE.md`

### CLAUDE.md Template Structure

```markdown
# Project Overview

Brief description of what this project does.

## Tech Stack

- **Language(s)**: Python, TypeScript, etc.
- **Framework(s)**: Django, React, etc.
- **Key dependencies**: List important libraries

## Key Directories

- `/src` - Main source code
- `/tests` - Test files
- `/docs` - Documentation
- `/scripts` - Utility scripts

## Build & Test Commands

- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run test` - Run tests
- `npm run lint` - Check code style

## Code Style & Conventions

- Use 2-space indentation
- Follow naming conventions: camelCase for functions, PascalCase for classes
- Write JSDoc comments for public functions
- Add unit tests for new functions

## Important Architectural Patterns

- [Describe key patterns, design decisions, or gotchas]

## Common Workflows

### Adding a Feature

1. Create feature branch
2. Write tests first
3. Implement feature
4. Run full test suite
5. Create PR

### Debugging Tips

- [Common issues and solutions]
- Important: [Something critical Claude should know]

## Current Status

What are you currently working on, any known issues?
```

### Initial Session Setup

**First session after `/init`:**
1. Claude reads CLAUDE.md
2. Claude understands project structure
3. Claude has context for subsequent tasks
4. More efficient interactions

### Organizing with `.claude/rules/`

**Create modular rules:**
```
.claude/
├── CLAUDE.md
└── rules/
    ├── typescript.md
    ├── testing.md
    ├── database.md
    └── frontend/
        ├── react.md
        └── styles.md
```

**Example rule file with path-specific scope:**
```markdown
---
paths:
  - "src/**/*.ts"
  - "lib/**/*.ts"
---

# TypeScript Rules

- Strict type checking required
- All functions must have explicit return types
- Prefer interfaces over type aliases
```

---

## 14. Advanced CLI Usage & Scripting

### Piping Content to Claude

**Pipe file content:**
```bash
cat logs.txt | claude -p "find errors"
cat file.json | claude -p "validate this JSON"
```

**Pipe command output:**
```bash
npm test | claude -p "fix these test failures"
git diff | claude -p "review this change"
```

**Heredoc (multiline input):**
```bash
claude -p "fix these errors" << EOF
TypeError: Cannot read property 'name' of undefined
  at processUser (app.js:42)
EOF
```

### Headless/Scriptable Mode

**Print mode (non-interactive):**
```bash
claude -p "your query here"
```

**Output formats:**
```bash
# JSON output (structured)
claude -p --output-format json "analyze this code" > result.json

# Stream JSON (includes progress)
claude -p --output-format stream-json "analyze this"

# Text output (default)
claude -p "your query"
```

### Structured Output (JSON Schema)

```bash
claude -p --json-schema '{
  "type": "object",
  "properties": {
    "errors": { "type": "array" },
    "suggestions": { "type": "array" }
  }
}' "analyze these logs"
```

### Execution Control

**Limit agentic turns (print mode):**
```bash
claude -p --max-turns 3 "fix the bug"
```

**Set spending limit:**
```bash
claude -p --max-budget-usd 5.00 "analyze the codebase"
```

**Continue conversation:**
```bash
claude -c -p "continue with the next step"
```

### Automated Workflows

**In shell scripts:**
```bash
#!/bin/bash
# Analyze test failures
failures=$(npm test 2>&1)
analysis=$(claude -p "identify root cause" <<< "$failures")
echo "Analysis: $analysis"

# Create PR with Claude
claude -p "create a PR that fixes the auth bug"
```

**In Git hooks:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Lint with Claude before commit
staged_files=$(git diff --cached --name-only)
claude -p "check for common issues" <<< "$staged_files"
```

**Continuous integration:**
```bash
# In CI/CD pipeline
claude -p --max-turns 5 "fix this failing build"
```

### Non-Interactive Permission Handling

**Skip all prompts (unsafe):**
```bash
claude -p --dangerously-skip-permissions "your query"
```

**Use specific permission rules:**
```bash
claude -p --allowedTools "Bash(npm test)" "Bash(git *)" "Read" "your query"
```

**MCP tool for approval (advanced):**
```bash
claude -p --permission-prompt-tool mcp_auth_tool "query"
```

### Combining Flags

**Complex example:**
```bash
cat requirements.txt | claude -p \
  --model opus \
  --max-turns 5 \
  --output-format json \
  --permission-mode plan \
  "analyze dependencies and security risks"
```

**Reuse across runs:**
```bash
# Save common flags to shell alias
alias claude-plan='claude --permission-mode plan --append-system-prompt "Use Plan Mode for safe analysis"'

# Use alias
claude-plan "refactor this component"
```

---

## 15. Debugging Claude Code

### Debug Mode

**Enable debug logging:**
```bash
claude --debug
claude --debug "api,hooks"  # Filter to specific categories
claude --debug "!statsig,!file"  # Exclude categories
```

**Debug categories:**
- `api` - API requests/responses
- `hooks` - Hook execution
- `mcp` - MCP server events
- `file` - File operations
- `permissions` - Permission system
- `stats` - Statistics/metrics
- `settings` - Configuration loading

### Verbose Output

**Toggle during session:**
```bash
Ctrl+O  # Toggle verbose mode
```

**Start in verbose mode:**
```bash
claude --verbose
```

**Shows:**
- Full turn-by-turn output
- All tool invocations
- Hook execution details
- Error messages with context

### Session Debug Log

**Access debug info:**
```bash
/debug [description]
```

Opens the session debug log showing:
- Session metadata
- Tool execution history
- Errors and warnings
- Configuration loaded
- Environment state

### Health Check

**Diagnose installation issues:**
```bash
/doctor
```

Checks:
- Claude Code version
- Installation integrity
- Network connectivity
- PATH configuration
- Dependencies installed
- Keybinding warnings
- Common issues

### Common Issues & Solutions

**Claude not responding:**
1. Run `/doctor` to diagnose
2. Check network connectivity: `ping api.anthropic.com`
3. Verify API key: `claude auth status`
4. Check for rate limits: `claude /usage`

**Permissions prompts repeatedly:**
1. Configure with `/permissions`
2. Add rules to settings.json
3. Check permission rule syntax with `/debug`

**Slow performance:**
1. Run `/context` to see what's consuming space
2. Check MCP server overhead with `/mcp`
3. Disable unused plugins
4. Use smaller model with `--model haiku`

**Memory issues:**
1. Use `/compact` to reduce context
2. Clear old sessions: sessions auto-delete after 30 days
3. Increase memory: `BASH_MAX_OUTPUT_LENGTH=500000`

**Git integration issues:**
1. Ensure `git` is in PATH: `which git`
2. Check git config: `git config --list`
3. Verify SSH/HTTPS access: `git clone test-repo`

**MCP server failures:**
1. Check MCP config: `claude /mcp`
2. View logs: `--debug mcp`
3. Test server directly: `mcp run server-name`

### Logging & Telemetry

**Enable telemetry:**
```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
```

**View session metrics:**
```bash
/cost  # Token usage
/stats  # Daily patterns
/usage  # Plan limits (subscribers)
```

### Technical Debugging

**Check version:**
```bash
claude --version
```

**Check configuration:**
```bash
/status  # Shows loaded settings
/config  # Opens settings UI
/hooks  # Lists active hooks
```

**Verify installation:**
```bash
/doctor
```

---

## 16. Security Model & Sandboxing

### Permission-Based Architecture

Claude Code uses **strict read-only permissions by default**. Additional actions require explicit permission:

| Action | Default | Require Approval |
|--------|---------|-----------------|
| Read files | Allowed | No |
| Edit files | Allowed once | Yes (per-session) |
| Run shell | Varies | Yes |
| Network access | Some | Yes |

### Permission Workflow

1. **First request**: Claude asks permission
2. **User choice**: Allow once, allow always, or deny
3. **Session-scoped**: Some permissions apply only to current session
4. **Pre-approved**: Configure `/permissions` to skip prompts for trusted commands

### Sandboxing

Sandbox provides OS-level filesystem and network isolation for Bash commands.

**Enable sandboxing:**
```bash
/sandbox
```

**Configure in settings:**
```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": false,
      "allowAllUnixSockets": false
    }
  }
}
```

**Sandbox modes:**
- **Enabled (macOS, Linux, WSL2)**: Commands execute in isolated environment
- **Filesystem isolation**: Access restricted to working directory + allowed paths
- **Network isolation**: Only configured domains allowed
- **Transparent operation**: Claude sees same filesystem structure

### Filesystem Isolation

**By default:**
- Claude can only **write** to working directory and subdirectories
- Claude can **read** outside working directory (system libraries, etc.)
- Explicit `/add-dir` needed for access outside working directory

**Configure with permissions:**
```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(~/.aws/**)"
    ],
    "allow": [
      "Read(~/Documents/shared)",
      "Edit(/tmp/scratch.txt)"
    ]
  }
}
```

### Network Security

**Default blocked:**
- `curl` and `wget` blocked by default (prefer WebFetch)
- External network access requires permission
- Isolated context for web fetches (prevents prompt injection)

**Allow specific domains:**
```json
{
  "sandbox": {
    "network": {
      "allowedDomains": [
        "github.com",
        "*.npmjs.org",
        "api.example.com"
      ]
    }
  }
}
```

**WebFetch rules:**
```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:github.com)",
      "WebFetch(domain:*.npmjs.org)"
    ],
    "deny": [
      "WebFetch(domain:unknown-site.com)"
    ]
  }
}
```

### Prompt Injection Protection

**Core protections:**
1. **Permission system**: Sensitive operations require approval
2. **Context-aware analysis**: Detects harmful instructions
3. **Input sanitization**: Prevents command injection
4. **Command blocklist**: Blocks risky commands like curl/wget by default

**Additional safeguards:**
- Network request approval by default
- Isolated context for web fetches
- First-time codebase verification
- Suspicious command detection
- Fail-closed matching (unknown commands ask for approval)

### Credential Management

**Secure storage:**
- API keys and tokens encrypted
- Stored in system keychain (macOS), credential manager (Windows), secure storage (Linux)
- Not exposed in logs or debug output

**API key helper:**
```json
{
  "apiKeyHelper": "/bin/generate_temp_api_key.sh"
}
```

**Temporary credentials:**
- Use helpers for short-lived tokens
- Refresh automatically between sessions
- Reduces exposure window

### Best Practices

1. **Review suggested commands** before approval
2. **Avoid piping untrusted content** directly to Claude
3. **Verify critical file changes** before approval
4. **Use VMs for external scripts** (especially from web services)
5. **Enable sandboxing** on sensitive machines
6. **Configure deny rules** for sensitive files (.env, secrets, SSH keys)
7. **Use organization policies** to enforce standards
8. **Audit permissions** regularly with `/permissions`
9. **Report suspicious behavior** with `/bug`

### Managed Security (Teams/Enterprise)

**Organization controls:**
```json
{
  "disableBypassPermissionsMode": "disable",
  "allowManagedPermissionRulesOnly": true,
  "allowManagedHooksOnly": true,
  "allowManagedMcpServersOnly": true,
  "blockedMarketplaces": [
    { "source": "github", "repo": "untrusted/plugins" }
  ]
}
```

**Audit logging:**
- Track configuration changes
- Monitor tool usage
- Log permission approvals
- Available via hooks and OpenTelemetry

### Security Compliance

**Certifications & Reports:**
- SOC 2 Type 2 report
- ISO 27001 certificate
- Available at Anthropic Trust Center

**Data handling:**
- Limited retention periods for sensitive data
- Restricted access to session data
- User control over training preferences
- Privacy policy: https://www.anthropic.com/legal/privacy

---

## Summary

This comprehensive guide covers all 16 aspects of Claude Code configuration and advanced features:

1. **CLAUDE.md** - Memory system with hierarchical scoping and auto-memory
2. **Settings** - Granular configuration across user, project, and organizational scopes
3. **Commands** - 20+ slash commands for session control, debugging, and integration
4. **Keyboard Shortcuts** - Customizable bindings with context-specific actions
5. **Permissions** - Fine-grained tool access control with rule syntax
6. **IDE Integration** - VS Code and JetBrains support with native features
7. **CLI Flags** - 50+ command-line options for scripting and automation
8. **Environment Variables** - 30+ variables for configuration and behavior
9. **Context Management** - Window visualization, compaction strategies, and cost reduction
10. **Model Selection** - Aliases, effort levels, and version pinning
11. **Cost Management** - Token tracking, rate limits, and optimization strategies
12. **Git Integration** - Git operations, worktrees, and PR linking
13. **Project Init** - Bootstrap CLAUDE.md and project structure
14. **Advanced CLI** - Piping, headless mode, and scripting patterns
15. **Debugging** - Debug mode, health checks, and troubleshooting
16. **Security** - Sandboxing, permissions, credential management, and audit logging

Use this reference to configure Claude Code for your specific needs, automate workflows, and optimize performance and cost.
