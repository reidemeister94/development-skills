# Claude Agent SDK & Agents in Claude Code

## 1. Overview

The **Claude Agent SDK** is Anthropic's framework for building autonomous AI agents with Claude as a library. It provides the same agentic loop, tools, and context management that power Claude Code, but programmatically available for Python and TypeScript.

| Tool | Use Case | Interface |
|------|----------|-----------|
| **Client SDK** | Direct API control, implement your own tool loop | Low-level APIs |
| **Agent SDK** | Autonomous agents with built-in tools | High-level, async generators |
| **Claude Code CLI** | Interactive development, exploration | Terminal UI |
| **Claude Code Desktop** | Desktop IDE integration | GUI |

---

## 2. Agent Types in Claude Code

### 2.1 General-Purpose Agent

The default agent invoked via the Task tool. No special configuration needed.

- Handles diverse tasks without specialization
- Available when `Task` tool is in `allowedTools`
- Full context window and tool access (inherited from parent)

### 2.2 Custom Subagents (Programmatic)

Specialized agents defined in code or `.claude/agents/` markdown files.

**Configuration options:**
- `description`: Natural language hint for when to use
- `prompt`: System prompt defining the agent's expertise
- `tools`: Array of allowed tools (read-only, execution, etc.)
- `model`: Override the default model

### 2.3 Explore Agent

Built-in agent optimized for **investigation and discovery**:
- Fast iterative exploration
- Optimized for reading and searching codebases
- Returns focused findings rather than exhaustive analysis

### 2.4 Plan Agent

Built-in agent optimized for **safe analysis and planning**:
- No tool execution (read-only analysis)
- Creates detailed implementation plans
- Previews changes without making them
- Supports `AskUserQuestion` for clarification

### 2.5 Agent Teams (Experimental)

Multiple agents working simultaneously on the same problem:
- Lead agent spawns teammates
- Parallel execution (faster than sequential)
- Each teammate has same codebase context
- Results aggregated by lead agent

---

## 3. Task Tool & Subagent System

### How Task Tool Works

```typescript
interface AgentInput {
  description: string;           // 3-5 word task description
  prompt: string;                // Full task instructions
  subagent_type: string;         // Name of the subagent or "general-purpose"
  isolation?: "worktree";        // Optional: git worktree isolation
  model?: "sonnet" | "opus" | "haiku";  // Optional: model override
  run_in_background?: boolean;   // Optional: run async
  max_turns?: number;            // Optional: limit turns
  resume?: string;               // Optional: resume previous agent
}
```

### Subagent Context & Communication

- **Isolation:** Each subagent maintains separate context (no pollution of main conversation)
- **Communication:** Results returned as tool output; main agent sees only final result
- **Tracking:** Messages from subagents include `parent_tool_use_id` field
- **Resuming:** Subagents can be resumed by passing the agent ID from previous execution

---

## 4. Building Custom Agents

### 4.1 SDK-Based Agents (Python)

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review this code for performance issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Task"],
            agents={
                "performance-reviewer": AgentDefinition(
                    description="Performance optimization specialist",
                    prompt="""You are a performance expert. When reviewing code:
1. Identify performance bottlenecks
2. Check algorithm complexity
3. Look for memory leaks
4. Suggest optimizations with specific examples""",
                    tools=["Read", "Grep", "Glob"],
                    model="opus"
                ),
                "test-runner": AgentDefinition(
                    description="Runs tests and analyzes results",
                    prompt="Execute tests and provide clear analysis.",
                    tools=["Bash", "Read", "Grep"]
                ),
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)
```

### 4.2 SDK-Based Agents (TypeScript)

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review this code for performance issues",
  options: {
    allowedTools: ["Read", "Grep", "Glob", "Task"],
    agents: {
      "performance-reviewer": {
        description: "Performance optimization specialist",
        prompt: `You are a performance expert...`,
        tools: ["Read", "Grep", "Glob"],
        model: "opus"
      },
      "test-runner": {
        description: "Runs tests and analyzes results",
        prompt: "Execute tests and provide clear analysis.",
        tools: ["Bash", "Read", "Grep"]
      }
    }
  }
})) {
  if ("result" in message) {
    console.log(message.result);
  }
}
```

### 4.3 Filesystem-Based Agents (Claude Code)

Define agents in `.claude/agents/` markdown files:

```markdown
# .claude/agents/code-reviewer.md

---
name: code-reviewer
description: Expert code reviewer for security and quality
tools:
  - Read
  - Grep
  - Glob
model: sonnet
---

You are a code review specialist with expertise in:
- Security vulnerabilities
- Performance issues
- Maintainability

When reviewing code, provide specific line references and suggested fixes.
```

**Precedence:** Programmatic agents override filesystem-based agents with the same name.

---

## 5. Agent Orchestration Patterns

### Sequential Execution

```
Agent A (reads files) → Agent B (analyzes) → Agent C (refactors)
```

- Each agent builds on previous results
- Clear data flow, easier to debug
- Slower than parallel (total time = sum of all)

### Parallel Execution

```
┌─ Agent A (security review) ─┐
├─ Agent B (performance) ─────┤ → Aggregate
└─ Agent C (style check) ─────┘
```

- Faster than sequential
- Multiple perspectives
- Results need aggregation

### Hierarchical (Subagents)

```
Main Agent
├─ Task 1 → Specialist A
├─ Task 2 → Specialist B
└─ Task 3 → Specialist C
(Main agent aggregates and decides next steps)
```

- Parent maintains high-level context
- Children focus on specializations
- Communication via Task tool

### Map-Reduce Pattern

1. Divide work across agents
2. Each agent processes independently (map)
3. Aggregate results in parent (reduce)

---

## 6. Agent Tools & Permissions

### Available Built-in Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| **Read** | Read files (text, images, PDFs, notebooks) | Code analysis |
| **Write** | Create new files | Generate code, docs |
| **Edit** | Make precise string replacements | Code modifications |
| **Bash** | Execute shell commands | Build, test, deploy |
| **Glob** | Fast file pattern matching | Find files |
| **Grep** | Search file contents with regex | Code search |
| **WebSearch** | Search the internet | External research |
| **WebFetch** | Fetch and analyze web content | Parse APIs |
| **AskUserQuestion** | Ask clarifying questions | Interactive workflows |
| **Task** | Invoke subagents | Delegation |
| **TodoWrite** | Create/manage task lists | Progress tracking |

### Permission Modes

```python
ClaudeAgentOptions(permission_mode="default")           # Prompt for approval
ClaudeAgentOptions(permission_mode="acceptEdits")       # Auto-approve file ops
ClaudeAgentOptions(permission_mode="bypassPermissions") # Run all (dangerous!)
ClaudeAgentOptions(permission_mode="plan")              # No execution, analyze only
```

### Permission Rules in Settings

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Read(**/*.py)",
      "WebFetch(domain:github.com)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Edit(.env)"
    ],
    "ask": [
      "Bash(*)"
    ]
  }
}
```

---

## 7. Agent Isolation

### Context Isolation
- Each subagent maintains separate conversation context
- Prevents information pollution
- Only final result returned to parent

### Worktrees (Git-Based Isolation)

```
main branch → worktree A (agent 1) → parallel work
           → worktree B (agent 2) → parallel work
```

- True filesystem isolation
- No file conflicts between agents
- Easy cleanup (delete worktree)

### Sandbox Configuration

```typescript
const result = await query({
  prompt: "Build and test",
  options: {
    sandbox: {
      enabled: true,
      autoAllowBashIfSandboxed: true,
      excludedCommands: ["docker"],
      network: {
        allowLocalBinding: true,
        allowUnixSockets: ["/var/run/docker.sock"]
      }
    }
  }
});
```

---

## 8. Agent Best Practices

### Design Principles

1. **Single Responsibility** - Each agent should have one clear purpose
2. **Clear Descriptions** - Help Claude decide when to invoke each agent
3. **Appropriate Tool Restrictions** - Give each agent only necessary tools
4. **Model Selection** - Match model to task complexity (Haiku=fast, Sonnet=balanced, Opus=complex)

### Cost Optimization

```python
# Haiku for simple tasks = ~20% of Opus cost
"formatter": AgentDefinition(model="haiku", tools=["Read", "Edit"])

# Opus for complex decisions
"architect": AgentDefinition(model="opus", tools=["Read", "Grep", "Glob"])
```

### Error Handling

```python
async def safe_agent_call(prompt, agent_def):
    try:
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                agents={"agent": agent_def},
                max_turns=10  # Prevent infinite loops
            )
        ):
            if hasattr(message, "result"):
                return message.result
    except Exception as e:
        return f"Agent failed: {e}"
```

---

## 9. SDK API Reference

### Core Functions

#### `query()` - Main Entry Point

```typescript
function query({
  prompt: string | AsyncIterable<SDKUserMessage>,
  options?: Options
}): Query
```

### Options Configuration

```typescript
interface Options {
  model?: string;
  allowed_tools?: string[];
  permission_mode?: "default" | "acceptEdits" | "bypassPermissions" | "plan";
  system_prompt?: string;
  agents?: Record<string, AgentDefinition>;
  resume?: string;
  fork_session?: boolean;
  cwd?: string;
  env?: Dict<string>;
  additional_directories?: string[];
  mcp_servers?: Record<string, McpServerConfig>;
  max_turns?: number;
  max_budget_usd?: number;
  max_thinking_tokens?: number;
  hooks?: Record<HookEvent, HookCallbackMatcher[]>;
  include_partial_messages?: boolean;
  output_format?: {type: "json_schema"; schema: JSONSchema};
  betas?: string[];
  plugins?: SdkPluginConfig[];
  sandbox?: SandboxSettings;
}
```

### AgentDefinition Schema

```typescript
interface AgentDefinition {
  description: string;        // Required: When to use this agent
  prompt: string;             // Required: System prompt/instructions
  tools?: string[];           // Optional: Allowed tools
  model?: "sonnet" | "opus" | "haiku" | "inherit";  // Optional
}
```

### Query Methods

```typescript
interface Query extends AsyncGenerator<SDKMessage, void> {
  interrupt(): Promise<void>;
  rewindFiles(userMessageUuid: string): Promise<void>;
  setPermissionMode(mode: PermissionMode): Promise<void>;
  setModel(model?: string): Promise<void>;
  setMaxThinkingTokens(maxThinkingTokens: number | null): Promise<void>;
  supportedCommands(): Promise<SlashCommand[]>;
  supportedModels(): Promise<ModelInfo[]>;
  mcpServerStatus(): Promise<McpServerStatus[]>;
  accountInfo(): Promise<AccountInfo>;
}
```

### Message Types

```typescript
type SDKMessage =
  | SDKAssistantMessage        // Agent thinking/decisions
  | SDKUserMessage             // User input
  | SDKResultMessage           // Final result
  | SDKSystemMessage           // Init, compaction events
  | SDKPartialAssistantMessage // Streaming updates
  | SDKCompactBoundaryMessage  // Conversation compaction
```

### Result Message

```typescript
interface SDKResultMessage {
  type: "result";
  subtype: "success" | "error_max_turns" | "error_during_execution";
  session_id: string;
  duration_ms: number;
  is_error: boolean;
  num_turns: number;
  result: string;
  total_cost_usd: number;
  usage: {
    input_tokens: number;
    output_tokens: number;
    cache_creation_input_tokens?: number;
    cache_read_input_tokens?: number;
  };
  structured_output?: unknown;
}
```

---

## 10. Headless & CI/CD Mode

### Headless Execution

```python
async for message in query(
    prompt="Run all tests and fix failures",
    options=ClaudeAgentOptions(
        allowed_tools=["Bash", "Read", "Edit"],
        permission_mode="bypassPermissions",
        max_turns=20
    )
):
    if hasattr(message, "result"):
        return message.result
```

### GitHub Actions Integration

```yaml
name: Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install SDK
        run: npm install @anthropic-ai/claude-agent-sdk
      - name: Run review agent
        run: node review-agent.js
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Docker Deployment

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["node", "agent.js"]
```

```bash
docker run \
  -e ANTHROPIC_API_KEY=$API_KEY \
  -v $(pwd):/workspace \
  -w /workspace \
  my-agent:latest
```
