# COMPREHENSIVE DEEP-DIVE: Claude Code Skills (SKILL.md Files)

This is a complete reference for understanding, creating, and mastering Claude Code Skills.

---

## 1. WHAT ARE SKILLS - Full Definition and Purpose

### Definition
**Skills are reusable instruction sets** that extend Claude Code's capabilities. A skill is a collection of guidelines, templates, reference material, and optional supporting scripts that teach Claude how to perform specialized tasks. Skills follow the open standard [Agent Skills](https://agentskills.io), which works across multiple AI tools.

Skills appear as **slash commands** (e.g., `/explain-code`, `/deploy`) and Claude can invoke them automatically when they're relevant to your request, or you can invoke them manually.

### Purpose
Skills serve multiple purposes:

1. **Encapsulate domain knowledge** - Store coding conventions, API patterns, architectural decisions, and team standards
2. **Create reusable workflows** - Define repeatable processes for common tasks (deployments, code reviews, migrations)
3. **Extend Claude's capabilities** - Teach Claude specialized techniques and approaches specific to your project
4. **Reduce context burden** - Move large reference material into discrete, loadable units
5. **Enable code generation** - Bundle templates that Claude fills in to generate consistent output
6. **Automate repetitive actions** - Create `/slash-commands` for manual workflows you trigger frequently

### How Skills Work

When you invoke a skill:

```
/skill-name arguments
```

Claude Code:
1. Finds the `SKILL.md` file for `skill-name`
2. Loads the skill's frontmatter configuration
3. Replaces any placeholders (like `$ARGUMENTS`, `$SESSION_ID`)
4. Executes any dynamic content (shell commands with the `!`command`` syntax)
5. Sends the fully-rendered skill content to Claude as part of the system prompt
6. Claude then executes the instructions in the skill

Skills can run **inline** (in your main conversation) or in a **forked subagent** (isolated context).

---

## 2. SKILL.MD FILE FORMAT - Complete Specification

Every skill is a directory containing a **`SKILL.md`** file. The `SKILL.md` file has two parts:

### File Structure

```
skill-name/
├── SKILL.md                    # Required: frontmatter + instructions
├── template.md                 # Optional: output template for Claude to fill in
├── examples.md                 # Optional: example outputs showing expected format
├── reference.md                # Optional: detailed reference material
└── scripts/                    # Optional: executable scripts Claude can run
    ├── validate.sh
    └── generate-report.py
```

### SKILL.md Format

```yaml
---
name: skill-name
description: What this skill does and when Claude should use it
disable-model-invocation: false
user-invocable: true
argument-hint: [optional-args]
allowed-tools: Read, Grep
model: inherit
context: inline
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---

# Your skill instructions here

Keep the markdown content focused and clear. Reference supporting files as needed.
```

---

## 3. SKILL.MD Frontmatter Reference - All Fields

The YAML frontmatter section between `---` markers configures the skill's behavior:

| Field | Required | Type | Default | Description |
|:------|:---------|:-----|:--------|:------------|
| `name` | No | string | (directory name) | Display name for the skill. Used to create `/slash-command`. Lowercase letters, numbers, hyphens only. Max 64 characters. |
| `description` | Recommended | string | (first paragraph of markdown) | What the skill does and when Claude should invoke it automatically. Claude uses this to decide when to load the skill. |
| `argument-hint` | No | string | (none) | Hint shown in autocomplete showing expected arguments. Example: `[issue-number]` or `[filename] [format]` |
| `disable-model-invocation` | No | boolean | `false` | If `true`, Claude cannot invoke the skill automatically. Only you can use `/skill-name`. Use for workflows with side effects (deployments, commits). |
| `user-invocable` | No | boolean | `true` | If `false`, the skill doesn't appear in the `/` menu. Only Claude can invoke it automatically. Use for background knowledge. |
| `allowed-tools` | No | string | (none) | Comma-separated list of tools Claude can use without prompting when this skill is active. Example: `Read, Grep, Bash(python *)` |
| `model` | No | string | `inherit` | Which model to use: `sonnet`, `opus`, `haiku`, or `inherit` (use parent's model). |
| `context` | No | string | `inline` | Set to `fork` to run in isolated subagent. Default `inline` runs in main conversation. |
| `agent` | No | string | `general-purpose` | When `context: fork`, which subagent type to use: `Explore`, `Plan`, `general-purpose`, or custom subagent name. |
| `hooks` | No | object | (none) | [Lifecycle hooks](#skill-hooks) that fire during skill execution. See [Hooks reference](/en/hooks). |

### Frontmatter Details

#### `name` Field
- Generated from directory name if omitted
- Format: lowercase, alphanumeric + hyphens
- Creates the slash command: `name: foo-bar` → `/foo-bar`
- Max 64 characters

#### `description` Field
- Should include keywords users would naturally say
- Example: `"Deploy the application to production"` triggers when you say "deploy"
- If omitted, Claude uses the first paragraph of the markdown content
- Budget: skill descriptions are loaded into context (default 2% of window, min 16KB)
- If you have many skills and some are excluded, run `/context` to see warnings

#### `allowed-tools` Field
Grants Claude permission to use specific tools without per-use approval when the skill is active:

```yaml
allowed-tools: Read, Grep, Bash(python *)
```

Tools Claude can use:
- Read, Edit, Write
- Grep, Glob
- Bash
- WebFetch, WebSearch
- Task (for spawning subagents)
- MCP tools (by server name)

Syntax:
- `Read` - allow the Read tool
- `Read, Grep` - allow multiple tools (comma-separated)
- `Bash(python *)` - allow Bash but only commands starting with `python`
- `Task(subagent-name)` - allow spawning specific subagent types
- Pattern matching: `Write(src/*)` - restrict to `src/` directory

#### `context: fork` - Subagent Execution
When `context: fork` is set:
- Skill runs in an isolated subagent context
- Subagent receives only the skill content as its prompt
- No access to your conversation history
- Useful for focused tasks that don't need context
- Must have explicit instructions in the skill (not just guidelines)

Example:
```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files
2. Analyze code
3. Summarize findings
```

#### `model` Field
- `inherit` - use same model as parent (default)
- `sonnet` - Claude 3.5 Sonnet
- `opus` - Claude Opus 4.6
- `haiku` - Claude 3.5 Haiku (fast, cheap)

#### `hooks` Field
Lifecycle hooks that execute during skill operations:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
```

Supported hook events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, etc.

---

## 4. SKILL DISCOVERY AND LOADING - How Claude Code Finds and Loads Skills

### Where Skills Live (Scope and Priority)

Skills are discovered from multiple locations. When skills share the same name, higher-priority locations override lower ones:

| Priority | Location | Scope | Who can use |
|:---------|:---------|:------|:-----------|
| 1 (highest) | `--agents` CLI flag | Current session only | Only that session |
| 2 | `.claude/skills/` | Current project | Your team (checked in) |
| 3 | `~/.claude/skills/` | All your projects | Only your machine |
| 4 | Plugin's `skills/` | Where plugin is enabled | Depends on plugin scope |
| 5 (lowest) | Enterprise/managed | Organization-wide | All users in org |

### File Structure

Each skill is a **directory** with a `SKILL.md` file:

```
~/.claude/skills/
├── explain-code/
│   ├── SKILL.md
│   └── examples/
│       └── architecture-explanation.md
├── deploy/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── validate-deployment.sh
│   └── templates/
│       └── deployment-checklist.md
└── my-project-skill/
    ├── SKILL.md
    └── reference.md
```

### Automatic Discovery from Nested Directories

Claude Code **automatically discovers skills** in nested `.claude/skills/` directories. This supports monorepo setups where packages have their own skills.

Example:
```
my-monorepo/
├── .claude/skills/
│   ├── global-skill/
│   │   └── SKILL.md
│   └── testing/
│       └── SKILL.md
├── packages/
│   ├── frontend/
│   │   └── .claude/skills/
│   │       └── react-patterns/
│   │           └── SKILL.md
│   └── api/
│       └── .claude/skills/
│           └── rest-api-design/
│               └── SKILL.md
```

When working in `packages/frontend/`, Claude Code loads skills from:
- `packages/frontend/.claude/skills/`
- `.claude/skills/` (parent)
- `~/.claude/skills/` (user-level)

### Skills from Additional Directories

When you use `--add-dir` to add extra directories to a session, skills defined in `.claude/skills/` within those directories are automatically loaded:

```bash
claude --add-dir ~/my-utils --add-dir ~/team-standards
```

This loads:
- `~/my-utils/.claude/skills/` (all skills)
- `~/team-standards/.claude/skills/` (all skills)
- Plus all default skill locations

**Note**: CLAUDE.md files from `--add-dir` directories are **not** loaded by default. To enable them, set the environment variable:
```bash
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

### Live Change Detection

Skills in `.claude/skills/` support **live change detection**. If you edit a skill's `SKILL.md` file during a session, Claude Code automatically reloads it without restarting. This is very useful during skill development.

### Skill Loading Process

1. **Session start**: Claude Code scans all skill locations
2. **Context load**: Skill descriptions are loaded into context so Claude knows what's available
3. **On invocation**:
   - Full skill content is loaded (not just description)
   - String substitutions are performed (`$ARGUMENTS`, etc.)
   - Dynamic content is executed (shell commands with `!`` syntax)
   - Rendered skill becomes part of Claude's prompt

---

## 5. SKILL INVOCATION - How to Use Skills

### Manual Invocation (You invoke)

Type the skill name as a slash command:

```
/skill-name
/deploy
/explain-code src/auth.ts
/fix-issue 123
```

Autocomplete shows available skills when you type `/`:

```
/ex      → /explain-code (Deploy the app)
/dep     → /deploy (Deploy to prod)
```

The `argument-hint` in frontmatter helps users understand expected args:

```yaml
argument-hint: [filename] [format]
```

Shows in autocomplete as: `/convert filename format`

### Automatic Invocation (Claude invokes)

Claude automatically loads and uses skills when:

1. **Description matches your request**: You ask something that aligns with the skill's description
2. **Skill has `disable-model-invocation: false`** (default): The skill allows automatic invocation
3. **Skill has `user-invocable: true`** (default): The skill is eligible for automatic use

Example:
```yaml
---
name: api-design
description: API design patterns for this codebase. Use when designing REST endpoints or API contracts.
---
```

When you say: *"Design a new REST endpoint for user profiles"*, Claude might automatically use this skill because "designing API endpoints" matches the description.

### Automatic Invocation Control

Two frontmatter fields control invocation:

**`disable-model-invocation: true`** - Only you can invoke
- Claude cannot trigger it automatically
- Description is **not** loaded into context
- Good for: deployments, commits, side effects
- Skill still appears in `/` menu

**`user-invocable: false`** - Only Claude can invoke
- You cannot see it in the `/` menu
- Description **is** loaded into context
- Good for: background knowledge, style guides, patterns
- `/skill-name` command doesn't work

Truth table:

| Setting | You can invoke | Claude can invoke | In context | In `/` menu |
|:--------|:---------------|:-----------------|:-----------|:-----------|
| (default) | Yes | Yes | Description | Yes |
| `disable-model-invocation: true` | Yes | No | No | Yes |
| `user-invocable: false` | No | Yes | Description | No |

---

## 6. SKILL PARAMETERS AND ARGUMENTS - Passing Data to Skills

### String Substitution Variables

Skills support dynamic values through string substitution. These are processed **before** Claude sees the skill:

| Variable | Value | Example |
|:---------|:------|:--------|
| `$ARGUMENTS` | All arguments passed to the skill | If you run `/migrate-component SearchBar React Vue`, `$ARGUMENTS` becomes `SearchBar React Vue` |
| `$ARGUMENTS[N]` | Argument at index N (0-based) | `$ARGUMENTS[0]` = first arg, `$ARGUMENTS[1]` = second arg |
| `$N` | Shorthand for `$ARGUMENTS[N]` | `$0` = first arg, `$1` = second arg |
| `${CLAUDE_SESSION_ID}` | Current session ID | Useful for logging, creating session-specific files |

### Argument Passing Examples

#### Example 1: Simple Arguments

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

Steps:
1. Read the issue description
2. Understand requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

Usage:
```
/fix-issue 123
```

Claude receives: "Fix GitHub issue 123 following our coding standards..."

#### Example 2: Positional Arguments

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
argument-hint: [component-name] [from-framework] [to-framework]
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.

Steps:
1. Find the component at src/components/$0.tsx
2. Understand its current implementation in $1
3. Rewrite for $2
4. Run existing tests to verify
5. Test rendering and behavior
```

Usage:
```
/migrate-component SearchBar React Vue
```

Claude receives:
- `$0` = `SearchBar`
- `$1` = `React`
- `$2` = `Vue`

#### Example 3: Arguments in Conditional Logic

```yaml
---
name: deploy
description: Deploy to a specific environment
disable-model-invocation: true
argument-hint: [environment]
---

Deploy the application to $ARGUMENTS:

$ARGUMENTS = staging:
  1. Run test suite
  2. Build Docker image
  3. Push to staging registry
  4. Deploy to staging K8s cluster
  5. Run smoke tests

$ARGUMENTS = production:
  1. Verify all tests pass
  2. Create release tag
  3. Build optimized image
  4. Push to production registry
  5. Deploy with blue-green strategy
  6. Verify monitoring
```

### Arguments Without `$ARGUMENTS` Placeholder

If your skill doesn't include `$ARGUMENTS` in the content, Claude Code **automatically appends** arguments at the end:

```yaml
---
name: search-docs
description: Search documentation
---

Search our documentation for the query provided.
```

Becomes:
```
Search our documentation for the query provided.

ARGUMENTS: authentication patterns
```

This is a fallback. It's better to explicitly use `$ARGUMENTS` in your skill.

### Session ID for Logging

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS

Session ID for correlation: ${CLAUDE_SESSION_ID}
```

Usage:
```
/session-logger "Starting feature implementation"
```

Creates: `logs/abc123def456.log` with the message.

---

## 7. SKILL BEST PRACTICES - Official Recommendations

### 1. Write Clear Descriptions

The description is your primary communication tool for automatic invocation:

**Good**:
```yaml
description: Deploy the application to production. Use when the application is ready to ship and all tests pass.
```

**Bad**:
```yaml
description: Deployment tool
```

**Guidelines**:
- Include action verbs (Deploy, Design, Review, Analyze)
- Mention what triggers it (when tests pass, when code is ready)
- Include keywords users naturally say
- 1-2 sentences max

### 2. Keep SKILL.md Under 500 Lines

Move large reference material to supporting files:

```
my-skill/
├── SKILL.md (instructions and navigation - max 500 lines)
├── api-reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples)
└── templates/ (reusable templates)
```

Reference supporting files from `SKILL.md`:

```markdown
## Additional resources

For complete API details, see [api-reference.md](api-reference.md).
For usage examples, see [examples.md](examples.md).
```

### 3. Use Supporting Files Effectively

Supporting files stay in the skill directory but aren't loaded automatically. Claude loads them only when you reference them in `SKILL.md`.

**Structure**:
```
api-design/
├── SKILL.md (overview, guidelines, references)
├── patterns.md (REST pattern details)
├── error-handling.md (error response specs)
└── scripts/
    └── validate-openapi.sh (validation script)
```

**Reference in SKILL.md**:
```markdown
## API Patterns

When designing endpoints, follow patterns in [patterns.md](patterns.md).

## Error Handling

For error response formats, see [error-handling.md](error-handling.md).
```

Claude loads supporting files only when it needs them, saving context.

### 4. Design for Your Invocation Type

**Reference skills** (used by Claude automatically):
- Describe patterns, conventions, guidelines
- Don't require explicit action
- Keep descriptions focused
- Example: `api-conventions`, `style-guide`

```yaml
description: API design conventions for this codebase. Use when designing REST endpoints.
```

**Task skills** (you invoke manually):
- Explicit step-by-step instructions
- Describe actions Claude should take
- Set `disable-model-invocation: true`
- Use `argument-hint` for clarity
- Example: `deploy`, `commit`, `release`

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
argument-hint: [environment]
---

1. Verify all tests pass
2. Create release tag
3. Build and push image
...
```

### 5. Use `allowed-tools` for Security

Restrict Claude to only necessary tools:

```yaml
---
name: code-reviewer
description: Review code for quality
allowed-tools: Read, Grep, Glob, Bash(git *)
---
```

This skill can only:
- Read files
- Search with grep
- Find files with glob
- Run git commands

Cannot:
- Write or edit files
- Execute arbitrary bash

### 6. Test Automatic Invocation

To verify Claude detects your skill:

1. Start a session
2. Describe something matching your description
3. Check if Claude mentions the skill or invokes it

If Claude doesn't invoke it:
- Try rephrasing your request to match keywords in the description
- Make the description more specific
- Ask explicitly: `Use the foo skill to...`

### 7. Use `context: fork` for Isolated Work

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS:
1. Find relevant files
2. Analyze the code
3. Summarize findings
```

This creates an isolated subagent context. Use when:
- Work is self-contained
- Output is verbose but you only need a summary
- You want to enforce tool restrictions
- Task doesn't need conversation history

### 8. Reference SKILL.md in CLAUDE.md

In your project's `CLAUDE.md`, reference skills you want Claude to know about:

```markdown
## Available Skills

- `/deploy` - Deploy to production
- `/code-review` - Review code changes
- `/api-design` - Design REST endpoints
```

This reminds Claude what skills are available and when to use them.

---

## 8. SKILL SCOPING - Project-level vs User-level vs Global

### Scope Hierarchy and Priority

When skills with the same name exist in multiple locations, priority determines which is used:

1. **Session-level** (highest) - `--agents` CLI flag
2. **Project-level** - `.claude/skills/` in current project
3. **User-level** - `~/.claude/skills/` on your machine
4. **Plugin-level** - `plugin-name:skill-name` namespace
5. **Enterprise** (lowest) - Managed settings

If you have:
- `.claude/skills/deploy/SKILL.md` (project)
- `~/.claude/skills/deploy/SKILL.md` (user)

The **project version wins** when you run `/deploy`.

### Project-level Skills (`.claude/skills/`)

**Location**: `.claude/skills/<name>/SKILL.md` in your repository

**Scope**: Only available in this project

**Sharing**: Checked into version control, available to your team

**Use when**:
- Skill is specific to this codebase
- Want to share with team
- Conventions are project-specific

**Example**:
```
my-project/
├── .claude/
│   └── skills/
│       ├── deploy-to-staging/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── validate-staging.sh
│       └── code-review/
│           └── SKILL.md
└── src/
```

Team members cloning the repo automatically have these skills.

### User-level Skills (`~/.claude/skills/`)

**Location**: `~/.claude/skills/<name>/SKILL.md`

**Scope**: All your projects

**Sharing**: Personal to your machine

**Use when**:
- Skill useful across multiple projects
- Personal workflow or preference
- Don't want to commit to version control

**Example**:
```
~/.claude/skills/
├── explain-code/
│   └── SKILL.md (available in all projects)
├── research/
│   └── SKILL.md (available in all projects)
└── debugging/
    └── SKILL.md (available in all projects)
```

### Plugin-level Skills

**Location**: `<plugin>/skills/<name>/SKILL.md`

**Scope**: Where plugin is installed

**Sharing**: Distributed via plugin marketplace

**Use when**:
- Want to distribute skills to team
- Part of a larger plugin
- Building reusable skill packages

See [Skill Sharing](#share-skills) section below.

### Enterprise/Managed Skills

**Location**: Configured by administrator

**Scope**: Organization-wide

**Sharing**: All users see these

**Use when**:
- Organization-wide standards
- Distributed through managed settings
- Enforced across team

---

## 9. SKILL EXAMPLES - Real-world Well-Structured Skills

### Example 1: Reference Skill - API Design Conventions

```yaml
---
name: api-conventions
description: API design patterns for this codebase. Use when designing REST endpoints or API contracts.
user-invocable: true
disable-model-invocation: false
---

# API Design Conventions

When designing API endpoints, follow these patterns:

## Naming
- Use lowercase endpoints: `/users/search`, not `/Users/Search`
- Use plurals for collections: `/products`, `/orders`
- Use singular for resources: `/user/{id}`
- Use hyphens, not underscores: `/user-profiles`, not `/user_profiles`

## HTTP Methods
- GET: Retrieve data (no side effects)
- POST: Create new resource, perform actions with side effects
- PUT: Replace entire resource
- PATCH: Partial update
- DELETE: Remove resource

## Error Responses
All errors return JSON with consistent format:

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "details": {}
}
```

Status codes:
- 400: Bad request (invalid input)
- 401: Unauthorized (authentication required)
- 403: Forbidden (insufficient permissions)
- 404: Not found
- 500: Server error

## Query Parameters
- Filter: `?status=active&type=premium`
- Sort: `?sort=created_at:desc`
- Pagination: `?page=2&limit=25`
- Search: `?q=search+term`

## Request/Response Format
- Always use JSON
- Use ISO 8601 for timestamps: `2026-02-25T14:30:00Z`
- Use UTF-8 encoding
- Include `Content-Type: application/json`

## Versioning
Use URL versioning: `/api/v1/users`, `/api/v2/users`

For detailed patterns, see [patterns.md](patterns.md).
```

### Example 2: Task Skill - Deploy to Production

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash(git *), Bash(docker *), Read
model: sonnet
---

# Deploy to $ARGUMENTS

## Pre-deployment Checks

1. **Verify all tests pass**
   ```bash
   npm test -- --coverage
   ```

2. **Check git status is clean**
   ```bash
   git status
   ```

3. **Pull latest changes**
   ```bash
   git pull origin main
   ```

## Deployment Steps

### For staging environment:
1. Build Docker image with tag `staging-latest`
2. Push to staging registry
3. Update staging deployment manifests
4. Apply kubectl changes
5. Monitor deployment status
6. Run smoke tests

### For production environment:
1. Create git tag with version: `v1.2.3`
2. Build Docker image with version tag and `latest`
3. Push both tags to production registry
4. Update production deployment with blue-green strategy
5. Monitor new deployment for errors
6. Verify monitoring dashboards show healthy metrics
7. Drain old deployment after 5 minutes
8. Notify team of successful deployment

## Post-deployment Verification

1. Check application health endpoints
2. Verify database migrations completed
3. Monitor logs for errors
4. Check error tracking (Sentry) for spikes
5. Verify key features are working

## Rollback Procedure

If issues occur:
1. Revert kubectl to previous deployment
2. Monitor logs and metrics
3. Create incident post-mortem
```

### Example 3: Research Skill - Using Subagent

```yaml
---
name: security-audit
description: Audit code for security vulnerabilities. Use when reviewing code for security risks.
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(find *)
---

# Security Audit of $ARGUMENTS

Perform a thorough security audit:

## Check for Common Vulnerabilities

1. **SQL Injection**
   - Find all SQL queries
   - Check for parameterized queries
   - Look for string concatenation in queries

2. **Authentication Issues**
   - Check for hardcoded credentials
   - Verify password hashing
   - Check token validation

3. **Secrets Management**
   - Search for exposed API keys
   - Look for hardcoded database URLs
   - Check for leaked tokens

4. **Dependency Vulnerabilities**
   - Review dependencies for known CVEs
   - Check for outdated packages

## Report Format

Summarize findings with:
- Vulnerability type
- Location (file:line)
- Severity (Critical, High, Medium, Low)
- Fix recommendation
```

### Example 4: Template-based Skill

```yaml
---
name: release-notes
description: Generate release notes for a new version
disable-model-invocation: true
argument-hint: [version]
---

# Release Notes for v$ARGUMENTS

Fill in the template below for version $ARGUMENTS:

## Features

- [Feature 1]
- [Feature 2]
- [Feature 3]

## Bug Fixes

- [Bug 1]
- [Bug 2]

## Breaking Changes

- [If any breaking changes, list them]

## Upgrade Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Contributors

Thank you to:
- [@contributor1]
- [@contributor2]

## Downloads

- [Link to release]
- [Changelog](CHANGELOG.md)
```

### Example 5: Dynamic Content Skill

```yaml
---
name: pr-summary
description: Summarize a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull Request Summary

Analyze and summarize this PR:

### PR Information
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

### Your Analysis

Provide:
1. Summary of changes in 1-2 sentences
2. Impact assessment (what could break?)
3. Review checklist (code quality, testing, docs)
4. Risk level (Low/Medium/High)
5. Recommendation (Approve/Request Changes/Needs Review)
```

The `!` command syntax executes shell commands immediately and inserts their output.

---

## 10. SKILL DEBUGGING - How to Debug Skills That Aren't Working

### Issue 1: Skill Not Triggering Automatically

**Symptom**: You describe something matching the skill, but Claude doesn't use it.

**Diagnosis**:

1. **Check the description is specific enough**
   - Vague: `"Debugging tool"`
   - Better: `"Debug errors and fix bugs. Use when encountering exceptions or test failures"`

2. **Check keywords match your request**
   - Skill description: "Deploy to production"
   - You said: "How do I push this to staging?"
   - Won't match! "staging" ≠ "production"

3. **Verify `disable-model-invocation: false` (default)**
   ```yaml
   disable-model-invocation: true  # ← Prevents automatic invocation!
   ```

4. **Try invoking manually**
   ```
   /skill-name
   ```
   If this works, the issue is automatic detection, not the skill itself.

**Solutions**:

1. Ask Claude explicitly:
   ```
   Use the api-conventions skill to design this endpoint
   ```

2. Rephrase your request to match the description:
   - Skill: "Deploy to production"
   - You: "I'm ready to deploy"

3. Make the description more specific with keywords:
   ```yaml
   description: Deploy the application to production. Use when the application is ready to ship, all tests pass, and you want to push to prod.
   ```

### Issue 2: Skill Triggers Too Often

**Symptom**: Claude uses the skill when you don't want it to.

**Diagnosis**:

The description is too broad. Example:
```yaml
description: "Helps with code"  # Too vague!
```

**Solutions**:

1. Make the description more specific:
   ```yaml
   description: "Analyze code performance using profiling tools. Use only when debugging performance bottlenecks."
   ```

2. Set `disable-model-invocation: true` if it's a task Claude shouldn't trigger:
   ```yaml
   disable-model-invocation: true
   ```

3. Use fewer keywords in the description

### Issue 3: Claude Doesn't See All Skills

**Symptom**: You know you have skills but they don't appear in `/` or Claude doesn't mention them.

**Diagnosis**:

1. **Skill description budget exceeded**
   - Skill descriptions are limited to 2% of context window (default 16KB)
   - If you have many skills, some get excluded

2. **File not named `SKILL.md`**
   - Must be exactly `SKILL.md` (case-sensitive on Linux/Mac)
   - Not `skill.md`, not `Skill.md`

3. **Wrong directory structure**
   - Correct: `~/.claude/skills/my-skill/SKILL.md`
   - Wrong: `~/.claude/skills/my-skill.md`
   - Wrong: `~/.claude/my-skill/SKILL.md`

4. **Syntax error in frontmatter**
   - YAML must be valid
   - Check for missing colons, unclosed quotes
   - Use a YAML validator

**Solutions**:

1. Check your skill budget:
   ```
   /context
   ```
   Look for warnings about excluded skills.

2. Verify file structure:
   ```bash
   ls -la ~/.claude/skills/my-skill/
   # Should show: SKILL.md
   ```

3. Validate YAML:
   - Copy frontmatter to https://www.yamllint.com/
   - Fix any syntax errors

4. If you have too many skills:
   - Move some to project scope only
   - Combine related skills
   - Set `user-invocable: false` on background skills

### Issue 4: Skill Arguments Not Working

**Symptom**: You pass arguments but Claude doesn't see them.

**Diagnosis**:

1. **`$ARGUMENTS` not in skill content**
   - Claude Code appends arguments at the end if missing
   - But they won't be in the right place

2. **Wrong syntax**
   - Wrong: `$argument` (lowercase)
   - Wrong: `{ARGUMENTS}` (braces)
   - Correct: `$ARGUMENTS` or `$0`, `$1`

3. **No arguments provided**
   ```
   /skill-name              # ← No arguments
   /skill-name arg1 arg2    # ← With arguments
   ```

**Solutions**:

1. Include `$ARGUMENTS` in your skill:
   ```yaml
   Fix GitHub issue $ARGUMENTS following our standards.
   ```

2. Use correct syntax:
   ```yaml
   Migrate the $0 component from $1 to $2.
   ```

3. Provide arguments:
   ```
   /migrate-component SearchBar React Vue
   ```

### Issue 5: Supporting Files Not Loading

**Symptom**: You reference a supporting file but Claude doesn't see it.

**Diagnosis**:

1. **File doesn't exist**
   ```
   skill/
   ├── SKILL.md (references examples.md)
   └── (no examples.md!)
   ```

2. **Wrong path**
   - Relative paths in skill directory
   - Correct: `[examples.md](examples.md)`
   - Wrong: `[examples.md](/examples.md)`
   - Wrong: `[examples.md](../examples.md)`

3. **Claude hasn't opened it yet**
   - Supporting files load on-demand
   - Claude only loads when referenced
   - If Claude doesn't mention the file, it hasn't loaded it

**Solutions**:

1. Verify file exists in skill directory
2. Use relative paths: `[examples.md](examples.md)`
3. Make sure SKILL.md references it
4. Ask Claude: "See the examples in [examples.md](examples.md)"

### Issue 6: Script Execution Failing

**Symptom**: Dynamic content with `!`` commands doesn't work.

**Diagnosis**:

1. **Script not executable**
   ```bash
   -rw-r--r-- scripts/deploy.sh  # ← Not executable!
   ```

2. **Wrong path**
   - Relative to where skill runs
   - Best practice: use absolute paths

3. **Command not found**
   - Tool not installed
   - Path not in $PATH

**Solutions**:

1. Make script executable:
   ```bash
   chmod +x ~/.claude/skills/my-skill/scripts/deploy.sh
   ```

2. Use absolute paths in SKILL.md:
   ```yaml
   Output: !`$HOME/.claude/skills/my-skill/scripts/generate.sh`
   ```

3. Verify tools are installed:
   ```bash
   which python3
   which git
   which gh  # GitHub CLI
   ```

---

## 11. ADVANCED SKILL PATTERNS - Conditional Logic, Tool Restrictions, Agent Delegation

### Pattern 1: Conditional Logic in Skills

```yaml
---
name: deploy
description: Deploy to a specific environment
disable-model-invocation: true
argument-hint: [environment]
---

Deploy to $ARGUMENTS environment:

**If environment is staging:**
- Run full test suite
- Build and push Docker image to staging registry
- Deploy to staging K8s cluster
- Run smoke tests
- Keep old deployment running (blue-green ready)

**If environment is production:**
- Verify all tests pass in CI
- Create release tag
- Build and push Docker image with version tag
- Update load balancer for blue-green deployment
- Wait 5 minutes monitoring metrics
- Drain old deployment
- Notify team in Slack

**If environment is something else:**
- Request valid environment (staging or production)
```

Claude understands conditional logic and will follow different steps based on the argument.

### Pattern 2: Tool Restrictions for Safety

```yaml
---
name: code-reviewer
description: Review code without making changes
allowed-tools: Read, Grep, Glob, Bash(git *)
---

Review the code changes:

1. Check code quality
2. Verify test coverage
3. Look for security issues
4. Suggest improvements

Note: You cannot edit files. Provide suggestions only.
```

The `allowed-tools` field restricts Claude to read-only tools. If Claude tries to write, it gets an error.

### Pattern 3: Skill Hooks for Validation

```yaml
---
name: database-migration
description: Generate and test database migrations
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-migration.sh"
---

Generate a database migration:

1. Understand the schema change
2. Write migration SQL
3. Test migration (validates automatically)
4. Generate rollback
```

The `PostToolUse` hook runs a validation script after each bash command executes.

### Pattern 4: Combining Skills in Subagents

Create a skill that spawns a subagent with preloaded skills:

```yaml
---
name: implement-api
description: Implement a complete REST API endpoint
context: fork
agent: general-purpose
---

Implement a REST API endpoint for $ARGUMENTS using preloaded skills.

The api-conventions and error-handling skills are available.
Follow their patterns exactly.

Steps:
1. Design the endpoint (use api-conventions skill)
2. Implement with proper error handling
3. Write tests
4. Create documentation
```

### Pattern 5: Dynamic Content Injection

```yaml
---
name: pr-reviewer
description: Review a pull request
context: fork
allowed-tools: Bash(gh *)
---

## PR Review

Review the current pull request:

PR Details:
- Title: !`gh pr view --json title -q`
- Author: !`gh pr view --json author -q`
- Created: !`gh pr view --json createdAt -q`
- Diff: !`gh pr diff --color=never`

## Review Process

1. Analyze changes
2. Check for issues
3. Provide feedback
```

The `!`` syntax runs commands and inserts their output. This runs **before** Claude sees anything.

### Pattern 6: Context Isolation with `fork`

```yaml
---
name: security-audit
description: Audit code for security vulnerabilities
context: fork
agent: Explore
---

Security audit of $ARGUMENTS:

Search for:
1. SQL injection vulnerabilities
2. Hardcoded credentials
3. Unsafe deserialization
4. Missing input validation
5. Known CVEs in dependencies

Report findings with:
- Vulnerability type
- Location (file:line)
- Severity
- Fix recommendation
```

The subagent runs in isolation:
- No access to conversation history
- Own context window
- Read-only tools
- Returns summary to main conversation

### Pattern 7: Template Generation

```yaml
---
name: generate-test
description: Generate test files for a component
argument-hint: [component-name]
disable-model-invocation: true
---

Generate comprehensive tests for the $0 component:

**Test File Location**: `src/components/$0.test.tsx`

**Test Structure**:
```typescript
describe('$0', () => {
  // Rendering tests
  // Props tests
  // Event handler tests
  // Integration tests
})
```

**Coverage Target**: 90%+

**Include Tests For**:
- Component renders with props
- User interactions (click, typing)
- Props validation
- Error states
- Edge cases

Use the testing-conventions skill for patterns.
```

### Pattern 8: Multi-step Workflows with Handoff

```yaml
---
name: implement-feature
description: Implement a new feature end-to-end
---

Implement feature: $ARGUMENTS

## Phase 1: Design
1. Understand requirements
2. Check existing patterns
3. Propose architecture
4. Get confirmation

## Phase 2: Implementation
"Use the code-reviewer subagent to review your implementation"

## Phase 3: Testing
1. Write tests
2. Run test suite
3. Check coverage

## Phase 4: Documentation
1. Update README
2. Add code comments
3. Create examples

After each phase, confirm before proceeding.
```

This creates a structured workflow where each phase happens in sequence.

---

## 12. SKILL MARKETPLACE AND SHARING - How Skills Can Be Shared

### Sharing at Different Scopes

Skills can be shared based on their location:

| Scope | How to share | Example |
|:------|:-------------|:--------|
| **Project** | Commit to version control | Team on same repo sees `.claude/skills/` |
| **Personal** | Git push to personal repo | Clone into `~/.claude/skills/` |
| **Plugin** | Create plugin marketplace entry | Installed via plugin system |
| **Organization** | Managed settings | Admin distributes to all users |

### Creating a Shareable Plugin with Skills

Package skills in a plugin for distribution:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── api-reviewer/
│   │   ├── SKILL.md
│   │   └── reference.md
│   ├── db-migrator/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── validate.sh
│   └── security-audit/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── README.md
└── LICENSE
```

**plugin.json**:
```json
{
  "name": "dev-tools",
  "version": "1.0.0",
  "description": "Development utilities including code review, security audits",
  "skills": "./skills/",
  "keywords": ["review", "security", "database"]
}
```

### Distributing via Marketplace

Create a `marketplace.json` in your GitHub repo:

```json
{
  "name": "my-marketplace",
  "url": "https://raw.githubusercontent.com/user/plugins/main/marketplace.json",
  "plugins": [
    {
      "name": "dev-tools",
      "source": "https://github.com/user/plugins/tree/main/plugins/dev-tools",
      "description": "Code review, security audits, and more"
    },
    {
      "name": "team-standards",
      "source": "https://github.com/user/plugins/tree/main/plugins/team-standards",
      "description": "Team-wide coding conventions"
    }
  ]
}
```

Users can then add your marketplace and install skills.

### Generating Visual Output from Skills

Skills can generate interactive HTML visualizations:

```yaml
---
name: codebase-visualizer
description: Generate an interactive tree visualization of your codebase
allowed-tools: Bash(python *)
---

Generate an interactive codebase visualization:

Run the visualization script:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` with:
- Collapsible directory tree
- File sizes
- Directory totals
- File type breakdown
```

The skill includes a Python script that generates an interactive HTML file and opens it in the browser.

---

## 13. INTERACTION WITH CLAUDE.MD - How Skills Relate to CLAUDE.MD

### SKILL.MD vs CLAUDE.MD

| Aspect | SKILL.MD | CLAUDE.MD |
|:-------|:---------|:----------|
| **Scope** | Specific task or domain | Entire project context |
| **Invocation** | Manual (`/skill-name`) or automatic | Always loaded |
| **Reusability** | Portable across projects | Project-specific |
| **Context** | Loaded on-demand | Always in context |
| **Purpose** | Teach specific workflows | Provide project-wide context |
| **Best for** | Specialized tasks | General guidance |

### Complementary Usage

**CLAUDE.md** provides project foundation:
```markdown
# Project Overview

This is an e-commerce platform built with React, Node, and PostgreSQL.

## Key Patterns
- Use Redux for state management
- API follows REST conventions
- Database uses migrations
```

**Skills** add specialized knowledge:
```yaml
# .claude/skills/api-design/SKILL.md
---
name: api-design
description: Design REST API endpoints
---

Design REST endpoints following our conventions...
```

### Referencing Skills in CLAUDE.MD

In your `CLAUDE.md`, list available skills:

```markdown
## Available Skills

These skills extend Claude's capabilities:

- `/api-design` - Design REST API endpoints following conventions
- `/security-audit` - Audit code for security vulnerabilities
- `/database-migration` - Generate database migrations safely
- `/deploy` - Deploy to staging or production

Use these skills when appropriate, or call them explicitly with `/skill-name`.
```

### Moving Content from CLAUDE.MD to Skills

If your CLAUDE.md is getting too large:

1. **Identify discrete topics**
   - API conventions → `api-design` skill
   - Database patterns → `database-migration` skill
   - Security guidelines → `security-audit` skill

2. **Create skills for each topic**
3. **Reference skills in CLAUDE.md**
4. **Set appropriate invocation controls**
   - Background knowledge: `user-invocable: false`
   - Explicit tasks: `disable-model-invocation: true`

Example refactor:

**Before** (CLAUDE.md = 2000 lines):
```markdown
# API Design

## REST Conventions
- Use lowercase endpoints
- Use plurals for collections
- Use hyphens in names
...100 more lines...

# Database Patterns

## Migrations
- Always write rollbacks
- Test migrations first
...100 more lines...
```

**After**:

CLAUDE.md (100 lines):
```markdown
# API and Database Guidelines

See `/api-design` for REST endpoint conventions.
See `/database-migration` for safe database changes.
```

Skills (organized):
- `api-design/SKILL.md` - All API patterns
- `database-migration/SKILL.md` - All database patterns

This reduces CLAUDE.md to essential context while keeping detailed guidance accessible via skills.

---

## 14. COMPREHENSIVE SKILL TROUBLESHOOTING CHECKLIST

### Before Creating a Skill

- [ ] Define the skill's purpose clearly
- [ ] Decide: Reference or Task skill?
- [ ] Choose scope: Project, User, or Plugin?
- [ ] Plan skill structure (main + supporting files)
- [ ] Write description with specific keywords

### Creating a Skill

- [ ] Create directory: `~/.claude/skills/my-skill/`
- [ ] Create `SKILL.md` with frontmatter
- [ ] Write clear, concise instructions
- [ ] Add supporting files if needed (max SKILL.md = 500 lines)
- [ ] Test with `/my-skill`

### Frontmatter Checklist

- [ ] Name is lowercase, no spaces, max 64 chars
- [ ] Description is specific (include keywords)
- [ ] Set `disable-model-invocation` if task-based
- [ ] Set `user-invocable: false` if reference-only
- [ ] Define `allowed-tools` for safety
- [ ] Choose `context: fork` if isolated execution needed
- [ ] Add `hooks` if validation needed

### Testing Skills

- [ ] Manual invocation works: `/my-skill`
- [ ] Arguments work: `/my-skill arg1 arg2`
- [ ] Supporting files load: Claude can reference them
- [ ] Scripts execute: Dynamic content works
- [ ] Descriptions match keywords: Claude can find it automatically
- [ ] Tool restrictions work: Claude can't use denied tools

### Optimization Checklist

- [ ] Supporting files referenced in SKILL.md
- [ ] SKILL.md under 500 lines
- [ ] No sensitive information in skills
- [ ] Skills don't conflict with CLAUDE.md guidance
- [ ] Description specific enough for automatic invocation
- [ ] `allowed-tools` limited to necessary tools
- [ ] Hook scripts are executable

---

## 15. QUICK REFERENCE - Frontmatter Fields Summary

```yaml
---
name: lowercase-name                          # Display name for skill
description: "What this skill does..."        # When Claude should use it
argument-hint: "[arg1] [arg2]"               # Hint for arguments
disable-model-invocation: false               # Only you invoke (true) or Claude can too (false)
user-invocable: true                          # You can invoke (true) or only Claude (false)
allowed-tools: "Read, Grep, Bash(python *)"  # Tools Claude can use
model: "sonnet"                               # Model: sonnet, opus, haiku, inherit
context: "inline"                             # Execution context: inline or fork
agent: "general-purpose"                      # When context: fork, which agent
hooks:                                        # Lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
---
```

---

## 16. Complete Example - Full Skill from Start to Finish

### Goal: Create a skill for generating database migrations

### Step 1: Plan the Skill

```
Purpose: Help developers generate safe database migrations
Type: Task (explicit invocation)
Scope: Project-level (.claude/skills/)
Files: SKILL.md + supporting scripts
Audience: Developers on the team
Invocation: Manual (/db-migrate)
Context: Inline (needs access to conversation)
```

### Step 2: Create Directory Structure

```bash
mkdir -p .claude/skills/db-migrate/scripts
cd .claude/skills/db-migrate
touch SKILL.md
touch scripts/validate-migration.sh
touch templates.md
chmod +x scripts/validate-migration.sh
```

### Step 3: Write SKILL.md

```yaml
---
name: db-migrate
description: Generate and test database migrations safely. Use when adding or modifying database schema.
disable-model-invocation: true
argument-hint: [description]
allowed-tools: Read, Bash(npm *), Bash(node *), Bash(psql *), Write
model: sonnet
---

# Database Migration Generator

Generate a safe database migration for: $ARGUMENTS

## Checklist

Before generating, verify:
- You understand the schema change
- You've considered backward compatibility
- You know the rollback strategy

## Migration Naming

Follow the pattern: `migrations/YYYYMMDDHHMMSS_description.sql`

Example: `migrations/20260225143000_add_user_roles_table.sql`

## Generated Migration Template

Every migration must include:

```sql
-- Up: $ARGUMENTS
-- Date: [Current timestamp]

BEGIN;

-- Your changes here

COMMIT;

-- Down: Rollback for $ARGUMENTS

BEGIN;

-- Rollback changes here

COMMIT;
```

## Best Practices

1. **Keep migrations atomic** - One logical change per file
2. **Always include rollbacks** - Every UP must have a DOWN
3. **Test both directions** - Run up then down, verify it works
4. **Use transactions** - Wrap in BEGIN/COMMIT
5. **Add comments** - Explain why, not what

See [templates.md](templates.md) for more examples.

## Validation

Your migration will be validated:
- SQL syntax checking
- Rollback verification
- Performance analysis

After generation, run:

```bash
npm run migrate:validate ./migrations/YYYYMMDDHHMMSS_*.sql
```

## Next Steps

1. Generate the migration
2. Run validation: `npm run migrate:validate`
3. Test locally: `npm run migrate:test`
4. Commit to git with descriptive message
5. Deploy following our deployment process
```

### Step 4: Write Supporting File (templates.md)

```markdown
# Migration Templates

## Template 1: Add Table

```sql
-- Up: Add users table
BEGIN;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

COMMIT;

-- Down: Drop users table
BEGIN;

DROP TABLE users;

COMMIT;
```

## Template 2: Add Column with Default

```sql
-- Up: Add role column to users
BEGIN;

ALTER TABLE users
ADD COLUMN role VARCHAR(50) DEFAULT 'user' NOT NULL;

COMMIT;

-- Down: Remove role column
BEGIN;

ALTER TABLE users
DROP COLUMN role;

COMMIT;
```

## Template 3: Data Migration

```sql
-- Up: Backfill email from username
BEGIN;

UPDATE users
SET email = username || '@company.com'
WHERE email IS NULL;

ALTER TABLE users
ALTER COLUMN email SET NOT NULL;

COMMIT;

-- Down: Revert email changes
BEGIN;

ALTER TABLE users
ALTER COLUMN email DROP NOT NULL;

COMMIT;
```
```

### Step 5: Write Validation Script

```bash
#!/bin/bash
# scripts/validate-migration.sh

set -e

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Check for dangerous operations without safeguards
if echo "$COMMAND" | grep -iE 'DROP\s+TABLE|DELETE\s+FROM.*WHERE' > /dev/null; then
  if ! echo "$COMMAND" | grep -iE 'BEGIN|TRANSACTION' > /dev/null; then
    echo "ERROR: Dangerous operation must be wrapped in transaction" >&2
    exit 2
  fi
fi

# Check for rollback section
if echo "$COMMAND" | grep -i 'UP:' > /dev/null; then
  if ! echo "$COMMAND" | grep -i 'DOWN:\|-- Down:' > /dev/null; then
    echo "WARNING: Consider adding explicit DOWN/rollback section" >&2
  fi
fi

exit 0
```

### Step 6: Test the Skill

```bash
# Test manual invocation
/db-migrate "Add user roles table"

# Should show migration template and validation
```

### Step 7: Document in CLAUDE.md

```markdown
## Database Migrations

Use the `/db-migrate` skill to generate new database migrations safely.

```
/db-migrate "Add users table with email and username"
```

The skill will:
1. Generate migration file
2. Validate SQL syntax
3. Suggest rollback strategy
4. Check for best practices

See [db-migrate skill documentation](.claude/skills/db-migrate/SKILL.md) for details.
```

---

## Summary

This comprehensive guide covers everything about Claude Code Skills:

1. **Definition & Purpose** - What skills are and why you need them
2. **File Format** - SKILL.md structure and all frontmatter fields
3. **Discovery & Loading** - How Claude Code finds and loads skills
4. **Invocation** - Manual and automatic skill invocation
5. **Parameters** - String substitution and argument passing
6. **Best Practices** - Writing effective, maintainable skills
7. **Scoping** - Project, user, and plugin-level skills
8. **Examples** - Real-world, production-ready skill examples
9. **Debugging** - Troubleshooting common skill issues
10. **Advanced Patterns** - Conditional logic, hooks, subagents
11. **Sharing** - Distributing skills via plugins and marketplaces
12. **CLAUDE.md Integration** - Complementary relationship with CLAUDE.md

Skills are a powerful feature for extending Claude Code. Start with simple skills, gradually add complexity, and maintain a clear skill ecosystem for your project.
