# Comprehensive Deep-Dive: Claude Code MCP (Model Context Protocol)

This guide covers everything about MCP with Claude Code, from architecture to implementation to best practices.

## 1. What is MCP - Full Definition & Architecture

### Definition

**MCP (Model Context Protocol)** is an open-source standard for connecting AI applications to external systems. Think of it like a USB-C port for AI applications—just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external data sources, tools, and workflows.

**Key characteristics:**

* Open-source standard managed by Anthropic
* Client-server architecture
* JSON-RPC 2.0 based protocol
* Language-agnostic (SDKs available for Python, TypeScript, Go, Java, etc.)
* Designed to be stateful and secure

### What MCP Enables

With MCP servers connected to Claude Code, you can ask Claude to:

* **Implement features from issue trackers**: "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
* **Analyze monitoring data**: "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
* **Query databases**: "Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database."
* **Integrate designs**: "Update our standard email template based on the new Figma designs that were posted in Slack"
* **Automate workflows**: "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."

### Core Architecture Components

MCP consists of two distinct layers:

#### Data Layer
- **Purpose**: Defines the JSON-RPC 2.0 based protocol for client-server communication
- **Includes**:
  * Lifecycle management (connection initialization, capability negotiation, termination)
  * Server features (tools, resources, prompts)
  * Client features (sampling, elicitation, logging)
  * Notifications for real-time updates
  * Utility features like progress tracking

#### Transport Layer
- **Purpose**: Defines communication mechanisms and channels for data exchange
- **Handles**:
  * Connection establishment
  * Message framing
  * Authorization and secure communication
  * Transport-specific implementation details

### Key Participants in MCP Architecture

**MCP Host** (AI Application)
- The application coordinating and managing MCP clients
- Examples: Claude Code, Claude Desktop, custom applications
- Maintains one MCP client per connected MCP server
- Responsible for routing tool calls and managing context

**MCP Client**
- Component that maintains connection to a single MCP server
- Obtains context from the server for the host to use
- Handles lifecycle management and capability negotiation
- Routes requests between host and server

**MCP Server**
- Program that provides context to MCP clients
- Can run locally (stdio transport) or remotely (HTTP/SSE transport)
- Exposes tools, resources, and prompts
- Manages its own capabilities and state

### Architecture Diagram

```
┌─────────────────────────────────┐
│     MCP Host (Claude Code)      │
│  ┌─────────────┐ ┌─────────────┐│
│  │ MCP Client1 │ │ MCP Client2 ││
│  │ MCP Client3 │ │ MCP Client4 ││
│  └──────┬──────┘ └──────┬──────┘│
└─────────┼────────────────┼───────┘
          │                │
    ┌─────▼──────┐   ┌────▼──────┐
    │ MCP Server │   │ MCP Server │
    │   (Local)  │   │  (Remote)  │
    └────────────┘   └────────────┘
```

---

## 2. MCP Server Configuration in Claude Code

### How Configuration Works

MCP servers are configured through different scopes that determine accessibility and sharing:

```bash
# Basic command structure
claude mcp add [OPTIONS] <name> <configuration>

# All options must come BEFORE server name and command/URL
```

### Configuration Scopes

#### Local Scope (Default)
- **Storage**: `~/.claude.json` (home directory)
- **Visibility**: Only you, in the current project
- **Use case**: Personal servers, experimental configs, sensitive credentials
- **Sharing**: Not shared with team

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
# or explicitly
claude mcp add --transport http --scope local stripe https://mcp.stripe.com
```

#### Project Scope
- **Storage**: `.mcp.json` at project root
- **Visibility**: Team members (checked into version control)
- **Use case**: Team-shared servers, project-specific tools
- **Sharing**: Checked into git, shared with entire team
- **Security**: Prompts for approval before using project-scoped servers

```bash
claude mcp add --transport http --scope project paypal https://mcp.paypal.com/mcp
```

The resulting `.mcp.json` file:
```json
{
  "mcpServers": {
    "paypal": {
      "type": "http",
      "url": "https://mcp.paypal.com/mcp"
    }
  }
}
```

#### User Scope
- **Storage**: `~/.claude.json` (home directory)
- **Visibility**: Cross-project, personal to your user
- **Use case**: Frequently used personal tools, development utilities
- **Sharing**: Not shared, available across all projects

```bash
claude mcp add --transport http --scope user hubspot https://mcp.hubspot.com/anthropic
```

### Scope Hierarchy & Precedence

When servers with the same name exist at multiple scopes:

1. **Local scope** (highest priority) - overrides project and user
2. **Project scope** (medium priority) - overrides user
3. **User scope** (lowest priority)

This allows personal configurations to override shared ones when needed.

### Configuration File Locations

| Scope | Location |
|-------|----------|
| Local | `~/.claude.json` (project-specific path) |
| Project | `.mcp.json` (project root) |
| User | `~/.claude.json` (global) |
| Managed | `/Library/Application Support/ClaudeCode/managed-mcp.json` (macOS) |
| Managed | `/etc/claude-code/managed-mcp.json` (Linux/WSL) |
| Managed | `C:\Program Files\ClaudeCode\managed-mcp.json` (Windows) |

### Environment Variable Expansion

Claude Code supports environment variable expansion in `.mcp.json`:

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**Syntax:**
- `${VAR}` - Expands to environment variable
- `${VAR:-default}` - Uses default if variable not set
- Expansions work in: `command`, `args`, `env`, `url`, `headers`

### Management Commands

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# Reset project-scope approval choices
claude mcp reset-project-choices

# Check server status (within Claude Code)
/mcp

# Authenticate remote servers (within Claude Code)
/mcp  # Then select "Authenticate"
```

### Dynamic Tool Updates

Claude Code supports MCP `list_changed` notifications, allowing MCP servers to dynamically update available tools without disconnecting and reconnecting. When a server sends a notification, Claude Code automatically refreshes capabilities.

### Plugin-Provided MCP Servers

Plugins can bundle MCP servers automatically. They work identically to user-configured servers:

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Features:**
- Automatic lifecycle management
- Environment variables with `${CLAUDE_PLUGIN_ROOT}`
- Multiple transport types supported
- Appear in `/mcp` command listing

---

## 3. MCP Server Types - Differences & When to Use Each

### Three Main Transport Types

#### 1. HTTP (Streamable HTTP) - RECOMMENDED

**What it is:**
- Uses HTTP POST for client-to-server messages
- Optional Server-Sent Events (SSE) for streaming
- Standard HTTP authentication (Bearer tokens, API keys, custom headers)
- Supports OAuth 2.0

**When to use:**
- Cloud-based/remote MCP servers (recommended)
- Services running on external platforms
- When you need to support multiple clients
- When HTTP infrastructure is already in place

**Advantages:**
- Wide network compatibility
- Firewall-friendly
- Supports standard HTTP auth
- Good for cloud deployments
- Single server can serve many clients

**Disadvantages:**
- Network latency vs local
- Requires network connectivity
- HTTP/TLS overhead

**Configuration:**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With authentication header
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"

# With OAuth
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
# Then authenticate with /mcp command
```

**Example implementation:**
```python
# Pseudo-code for HTTP server
from fastapi import FastAPI

app = FastAPI()

@app.post("/mcp")
async def mcp_handler(request):
    # Handle JSON-RPC requests
    return handle_jsonrpc(request)
```

#### 2. SSE (Server-Sent Events) - DEPRECATED

**What it is:**
- HTTP-based streaming protocol
- One-way communication from server to client
- Client sends requests via HTTP POST
- Server sends events via SSE stream

**When to use:**
- Legacy configurations (use HTTP instead)
- Systems already using SSE infrastructure

**Advantages:**
- Works over standard HTTP
- Supports streaming responses
- Firewall-friendly

**Disadvantages:**
- Deprecated in favor of HTTP
- More complex bidirectional handling
- Not recommended for new integrations

**Configuration:**
```bash
# Not recommended - use HTTP instead
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

#### 3. Stdio (Standard Input/Output) - LOCAL ONLY

**What it is:**
- Direct process communication via stdin/stdout
- Local only (same machine as Claude Code)
- No network overhead
- Zero latency

**When to use:**
- Local development servers
- Custom Python/Node.js scripts
- Direct file system access tools
- Single-user tools
- High-performance local operations
- Tools that need direct system access

**Advantages:**
- Zero network latency
- No network overhead
- Optimal for local tools
- Easy development/debugging
- Direct process control

**Disadvantages:**
- Local only (not shareable across network)
- Single client at a time typically
- Requires process management
- Need to manage executable paths

**Configuration:**
```bash
# Basic syntax: all options BEFORE server name, -- separates from command
claude mcp add [options] <name> -- <command> [args...]

# Example: Airtable
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server

# Example: Python script
claude mcp add --transport stdio my-tool -- python /path/to/server.py --port 8000

# Example: Node.js
claude mcp add --transport stdio local-api -- node /path/to/server.js
```

**Important note - Option ordering:**
```bash
# CORRECT: options before name, -- before command
claude mcp add --transport stdio --env KEY=value myserver -- npx server

# WRONG: command options get mixed up
claude mcp add --transport stdio myserver -- npx server --port 8080
# This tries to pass --port 8080 to Claude, not the server

# CORRECT with command args:
claude mcp add --transport stdio myserver -- npx server --port 8080
```

**Windows special handling:**
On native Windows (not WSL), stdio servers using `npx` require `cmd /c` wrapper:

```bash
# Windows: need cmd /c for npx
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package

# This works because Windows cmd can execute npx directly
# Without cmd /c, you get "Connection closed" errors
```

### Transport Comparison Table

| Feature | HTTP | SSE | Stdio |
|---------|------|-----|-------|
| **Latency** | Medium (network) | Medium (network) | Low (none) |
| **Scope** | Remote | Remote | Local only |
| **Clients** | Multiple | Multiple | Typically 1 |
| **Authentication** | Bearer, API Key, OAuth | Bearer, API Key | Env vars |
| **Recommended** | Yes | No (deprecated) | Yes (local) |
| **Network Required** | Yes | Yes | No |
| **Setup Complexity** | Medium | Medium | Low |
| **Example** | Sentry, Notion, GitHub | Legacy services | Custom scripts |

---

## 4. Built-in MCP Tools in Claude Code

Claude Code provides built-in tools automatically available to all MCP servers it connects to:

### Client-Side Primitives (Servers Can Request)

These allow MCP servers to request things FROM Claude Code:

#### Sampling
```json
{
  "method": "sampling/complete",
  "params": {
    "messages": [{"role": "user", "content": "..."}],
    "systemPrompt": "...",
    "maxTokens": 1024
  }
}
```
- Servers can request language model completions
- Useful when server needs Claude's intelligence
- Keeps server model-agnostic

#### Elicitation
```json
{
  "method": "elicitation/request",
  "params": {
    "prompt": "What email address should we use?"
  }
}
```
- Servers can request user input
- Useful for confirmations or additional data
- Claude Code handles UI prompting

#### Logging
- Servers can send log messages to Claude Code
- Useful for debugging and monitoring
- Displayed in Claude's session output

### Server Capabilities Provided to Claude

#### Tools (Executable Functions)

Tools are the primary way servers provide actions:

```json
{
  "name": "calculator",
  "title": "Calculator",
  "description": "Perform mathematical calculations",
  "inputSchema": {
    "type": "object",
    "properties": {
      "expression": {
        "type": "string",
        "description": "Math expression (e.g., '2 + 3 * 4')"
      }
    },
    "required": ["expression"]
  }
}
```

**How Claude Code uses them:**
- Discovers all tools via `tools/list`
- Claude can invoke tools during conversations
- Tools execute and return results
- Results are fed back to Claude

#### Resources (Data Sources)

Resources provide contextual information:

```
@server:protocol://resource/path
```

**Usage in Claude Code:**
```
Can you analyze @github:issue://123 and suggest a fix?
```

**Resource types:**
- Text files and documentation
- Database schemas
- API documentation
- Configuration files
- Any structured data

**How Claude Code uses them:**
- Discovers via `resources/list`
- Fetches via `resources/read`
- Includes as attachments in prompts
- Fuzzy-searchable with `@` mentions

#### Prompts (Reusable Templates)

Prompts become commands in Claude Code:

```
/mcp__servername__promptname <args>
```

**Examples:**
```
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug in login" high
```

**How Claude Code uses them:**
- Discovered as `/` commands
- Can accept arguments
- Results injected directly into conversation
- Pre-structured interactions

### Notifications (Real-time Updates)

When server capabilities change, servers can notify Claude Code:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list_changed"
}
```

Claude Code automatically refreshes available tools. This enables:
- Dynamic tool availability based on server state
- Permission changes
- Feature toggles
- Temporary unavailability

### MCP Tool Search (Context Optimization)

When you have many MCP servers, tool definitions can consume significant context. Claude Code automatically enables Tool Search:

**How it works:**
1. MCP tools are deferred rather than preloaded
2. Claude uses a search tool to discover relevant tools on-demand
3. Only needed tools are loaded into context
4. Tools work exactly the same to you

**Configuration:**
```bash
# Auto mode (default) - activates at 10% context threshold
ENABLE_TOOL_SEARCH=auto claude

# Custom threshold (5%)
ENABLE_TOOL_SEARCH=auto:5 claude

# Always enabled
ENABLE_TOOL_SEARCH=true claude

# Disabled (all tools preloaded)
ENABLE_TOOL_SEARCH=false claude
```

**Via settings.json:**
```json
{
  "env": {
    "ENABLE_TOOL_SEARCH": "auto:5"
  }
}
```

**Note:** Requires Sonnet 4+ or Opus 4+. Not supported on Haiku.

### Output Limits and Warnings

Claude Code manages large MCP tool outputs:

- **Warning threshold**: When output exceeds 10,000 tokens
- **Default maximum**: 25,000 tokens
- **Configurable**: Via `MAX_MCP_OUTPUT_TOKENS` environment variable

```bash
# Allow larger MCP outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Useful for:
- Large database queries
- Detailed reports/documentation
- Extensive log files
- Complex data processing

---

## 5. Creating Custom MCP Servers

### Server Development Overview

Creating an MCP server involves implementing the protocol in your language of choice. Anthropic provides SDKs for:

- **Python** - Most common for data tools
- **TypeScript/JavaScript** - Web services and Node.js
- **Go** - Performance-critical services
- **Java** - Enterprise systems
- **C#** - .NET environments
- **PHP** - Web services
- **Ruby** - Scripting and automation

### Basic Server Architecture

Every MCP server needs:

1. **Lifecycle Management**
   - Handle `initialize` requests
   - Declare capabilities
   - Manage connection state

2. **Tool Implementation**
   - Implement `tools/list` to advertise tools
   - Implement `tools/call` to execute tools
   - Define input schemas with JSON Schema

3. **Transport Handling**
   - For stdio: read/write JSON-RPC messages
   - For HTTP: handle POST requests
   - Send responses and notifications

4. **Error Handling**
   - Proper JSON-RPC error responses
   - Graceful degradation
   - Clear error messages

### Simple Python Server Example

```python
import json
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent

# Initialize server
server = Server("my-weather-server")

# Define a tool
TOOLS = [
    Tool(
        name="get_forecast",
        description="Get weather forecast for a location",
        inputSchema={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        }
    )
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_forecast":
        location = arguments["location"]
        # Your weather logic here
        return [TextContent(
            type="text",
            text=f"Weather forecast for {location}: Sunny, 72°F"
        )]
    return [TextContent(type="text", text="Unknown tool")]

if __name__ == "__main__":
    server.run(sys.stdin.buffer, sys.stdout.buffer)
```

### TypeScript Server Example

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { TextContent, Tool } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "my-api-server",
  version: "1.0.0"
});

const tools: Tool[] = [
  {
    name: "fetch_data",
    description: "Fetch data from an API",
    inputSchema: {
      type: "object" as const,
      properties: {
        endpoint: {
          type: "string",
          description: "API endpoint"
        }
      },
      required: ["endpoint"]
    }
  }
];

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "fetch_data") {
    const endpoint = request.params.arguments.endpoint;
    // Your API logic here
    return {
      content: [
        {
          type: "text" as const,
          text: `Data from ${endpoint}: {...}`
        }
      ]
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Server Implementation Patterns

#### Pattern 1: Database Server

Exposes database queries as tools:

```python
@server.call_tool()
async def query_database(name: str, arguments: dict):
    if name == "query_users":
        query = arguments["query"]
        results = db.execute(query)
        return [TextContent(type="text", text=json.dumps(results))]
```

#### Pattern 2: API Wrapper

Wraps external API calls:

```python
@server.call_tool()
async def api_call(name: str, arguments: dict):
    if name == "search_issues":
        response = requests.get(
            f"https://api.github.com/search/issues",
            params=arguments
        )
        return [TextContent(type="text", text=response.text)]
```

#### Pattern 3: File System Server

Provides file operations:

```python
@server.call_tool()
async def file_operations(name: str, arguments: dict):
    if name == "read_file":
        path = arguments["path"]
        with open(path) as f:
            content = f.read()
        return [TextContent(type="text", text=content)]
```

#### Pattern 4: Computation Server

Performs calculations or transformations:

```python
@server.call_tool()
async def compute(name: str, arguments: dict):
    if name == "calculate":
        expr = arguments["expression"]
        result = eval(expr)  # Or safer evaluation
        return [TextContent(type="text", text=str(result))]
```

### Building Resources

Resources provide data sources:

```python
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="db://schema/users",
            name="Users Schema",
            description="Database schema for users table",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "db://schema/users":
        schema = """
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        );
        """
        return [TextContent(type="text", text=schema)]
```

### Building Prompts

Prompts become commands in Claude Code:

```python
@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="analyze_logs",
            description="Analyze application logs",
            arguments=[
                {
                    "name": "time_range",
                    "description": "Time range to analyze",
                    "required": True
                }
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "analyze_logs":
        time_range = arguments.get("time_range")
        return PromptMessage(
            role="user",
            content=f"Analyze logs from {time_range}"
        )
```

### Error Handling

Proper error responses:

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # Tool logic
        pass
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        raise RequestHandlerException(f"Unexpected error: {str(e)}")
```

### Server Deployment

For stdio servers:
```bash
# Install dependencies
pip install mcp

# Run server directly
python server.py

# Or via npx for Node.js
npx my-mcp-server
```

For HTTP servers:
```bash
# Start on specific port
python server.py --port 8000

# Or with FastAPI
uvicorn server:app --port 8000
```

---

## 6. MCP Resources - How They Work

### What Are Resources?

Resources are **read-only data sources** that provide context to Claude Code:

- Text files and documentation
- Database schemas
- API responses
- Configuration snippets
- Any structured information

Resources are **referenced using @ mentions** in Claude Code, similar to how you reference files.

### Resource URI Format

```
@servername:protocol://path/to/resource
```

**Examples:**
```
@github:issue://456
@postgres:schema://users
@docs:file://api/endpoints
@notion:page://my-database
```

### Using Resources in Claude Code

```bash
# In Claude Code prompt:
Can you analyze @github:issue://123 and suggest a fix?

# Compare resources:
Compare @postgres:schema://users with @docs:file://database/user-model

# Reference multiple resources:
Based on @github:pr://456 and @docs:file://ARCHITECTURE.md, refactor this code
```

### Discovering Resources

**Type `@` to see available resources:**
```
@[fuzzy search through available resources]
```

Resources are automatically:
- Fetched from servers
- Included as attachments
- Highlighted in the conversation

### Resource vs Tool

| Aspect | Tool | Resource |
|--------|------|----------|
| **Purpose** | Execute actions | Provide context |
| **Invocation** | Called directly | Referenced with @ |
| **Input** | Arguments | None (read-only) |
| **Output** | Results | Content |
| **Latency** | May be slow | Should be fast |
| **Use case** | "Do something" | "Here's information" |

### Building Resource Servers

Example: Database schema server

```python
from mcp.server import Server
from mcp.types import Resource, TextContent

server = Server("db-schema-server")

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="postgres://schema/users",
            name="Users Table Schema",
            description="Schema definition for the users table",
            mimeType="text/plain"
        ),
        Resource(
            uri="postgres://schema/orders",
            name="Orders Table Schema",
            description="Schema definition for the orders table",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "postgres://schema/users":
        schema = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        return [TextContent(type="text", text=schema)]

    elif uri == "postgres://schema/orders":
        schema = """
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            total DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        return [TextContent(type="text", text=schema)]
```

### Resource Best Practices

1. **Keep resources fast** - They block when referenced
2. **Provide clear URIs** - Make resource paths meaningful
3. **Include descriptions** - Help Claude understand resource content
4. **Set correct MIME types** - Help with formatting
5. **Handle missing resources gracefully** - Return clear error messages

---

## 7. MCP Prompts - How They Work

### What Are Prompts?

MCP prompts are **reusable interaction templates** that become commands in Claude Code:

```
/mcp__servername__promptname [arguments]
```

Prompts allow servers to suggest structured ways for Claude to interact with them.

### Prompt Structure

```python
Prompt(
    name="review_code",
    description="Review and provide feedback on code",
    arguments=[
        {
            "name": "file_path",
            "description": "Path to the code file",
            "required": True
        },
        {
            "name": "focus_areas",
            "description": "Areas to focus on (security, performance, etc.)",
            "required": False
        }
    ]
)
```

### Using Prompts in Claude Code

```bash
# List available prompts
/  # Type forward slash to see commands

# Execute without arguments
/mcp__github__list_prs

# Execute with arguments
/mcp__github__pr_review 456

# With multiple arguments
/mcp__jira__create_issue "Bug in login flow" high
```

### Building Prompt Servers

```python
from mcp.server import Server
from mcp.types import Prompt, PromptMessage

server = Server("dev-tools-server")

@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="code_review",
            description="Conduct a code review",
            arguments=[
                {
                    "name": "pull_request_id",
                    "description": "GitHub PR number",
                    "required": True
                }
            ]
        ),
        Prompt(
            name="debug_error",
            description="Debug an error from logs",
            arguments=[
                {
                    "name": "error_id",
                    "description": "Error ID from Sentry",
                    "required": True
                },
                {
                    "name": "environment",
                    "description": "Environment (prod, staging, dev)",
                    "required": False
                }
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "code_review":
        pr_id = arguments.get("pull_request_id")
        return PromptMessage(
            role="user",
            content=f"""
            Please review the following pull request: #{pr_id}

            Focus on:
            1. Code quality and readability
            2. Potential bugs or edge cases
            3. Performance implications
            4. Test coverage
            """
        )

    elif name == "debug_error":
        error_id = arguments.get("error_id")
        env = arguments.get("environment", "prod")
        return PromptMessage(
            role="user",
            content=f"""
            Debug this error from {env}:
            Error ID: {error_id}

            Please provide:
            1. Root cause analysis
            2. Reproduction steps
            3. Proposed fix
            4. Testing strategy
            """
        )
```

### Prompt vs Tool

| Aspect | Prompt | Tool |
|--------|--------|------|
| **Invocation** | Command with `/` | Called by Claude |
| **Arguments** | Optional, explicit | Required via schema |
| **Return value** | Structured message | Any content type |
| **Use case** | Workflows, suggestions | Actions, calculations |
| **Interactivity** | Manual invocation | Automatic |

### Prompt Best Practices

1. **Clear descriptions** - Help users understand when to use
2. **Meaningful arguments** - Use descriptive names and help text
3. **Structured messages** - Format output for clarity
4. **Prompt templates** - Provide detailed interaction guidance
5. **Feedback integration** - Learn from how prompts are used

---

## 8. MCP Server Lifecycle - How Servers Are Started, Stopped, Managed

### Connection Lifecycle

Every MCP connection follows this sequence:

#### 1. Server Startup
```
Claude Code starts MCP server process
         ↓
Server initializes
         ↓
Server listens for connections
```

**For stdio servers:**
```bash
# Claude Code spawns process
claude mcp add --transport stdio myserver -- python server.py

# Process runs and waits for messages on stdin
```

**For HTTP servers:**
```bash
# Server already running on remote host
# Claude Code makes HTTP connections
```

#### 2. Initialization Handshake

```
Claude Code sends initialize request
         ↓
Server responds with capabilities
         ↓
Claude Code sends notifications/initialized
         ↓
Connection ready for use
```

**Initialization message:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "elicitation": {}
    },
    "clientInfo": {
      "name": "claude-code",
      "version": "1.0.0"
    }
  }
}
```

**Server responds:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": {}
    },
    "serverInfo": {
      "name": "my-server",
      "version": "1.0.0"
    }
  }
}
```

#### 3. Active Usage

```
Claude Code uses resources
         ↓
Claude Code calls tools
         ↓
Server sends notifications (optional)
         ↓
Claude Code uses updated tools
```

#### 4. Shutdown

```
Connection closed
         ↓
Stdio server process terminates
         ↓
HTTP connection closed
```

### Server Management Commands

```bash
# Start a server
claude mcp add --transport http myserver https://api.example.com/mcp

# List all servers
claude mcp list

# Get server details
claude mcp get myserver

# Check status (within Claude Code)
/mcp

# Remove server
claude mcp remove myserver

# Reset project approval choices
claude mcp reset-project-choices

# Import from Claude Desktop
claude mcp add-from-claude-desktop
```

### Timeout Configuration

Configure how long Claude Code waits for server startup:

```bash
# Set 10-second timeout
MCP_TIMEOUT=10000 claude

# Default is 10 seconds
```

### Server State Management

**Local stdio servers:**
- Process lives and dies with Claude Code session
- Fresh start each session
- No persistent state across sessions

**Remote HTTP servers:**
- External service manages state
- Connection pooling possible
- Persistent across sessions

**Plugin servers:**
- Start when plugin enabled
- Stop when plugin disabled
- Claude Code restart needed for changes

### Connection Pooling (HTTP)

Remote servers can share connections:

```
┌─────────────────────────┐
│   Claude Code Instance  │
│  Multiple Clients → One Server
└─────────────────────────┘
```

Multiple Claude Code instances can connect to same server, allowing:
- Shared authentication tokens
- Cached responses
- Server-side state

### Error Recovery

**Automatic reconnection:**
- If connection drops, Claude Code reconnects
- Tool list updates via notifications

**Manual recovery:**
```bash
# Restart connection
/mcp  # Shows server status

# Remove and re-add if stuck
claude mcp remove myserver
claude mcp add --transport http myserver https://api.example.com/mcp
```

---

## 9. MCP Configuration Locations - Project, User, Global

### Configuration File Locations Summary

| Scope | File | Location | Shared? |
|-------|------|----------|---------|
| **Local/Project** | `.mcp.json` | Project root | Yes (version control) |
| **User** | `~/.claude.json` | Home directory | No (personal) |
| **Local** | `~/.claude.json` | Home directory | No (personal, project-specific) |
| **Managed** | `managed-mcp.json` | System directory | Yes (admin-controlled) |

### Project-Level Configuration

File: `.mcp.json` at project root

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "local-db": {
      "type": "stdio",
      "command": "python",
      "args": ["./tools/db-server.py"],
      "env": {
        "DB_URL": "postgresql://localhost/dev"
      }
    }
  }
}
```

**Benefits:**
- Shared with team
- Version controlled
- Ensures consistency
- Approval prompts for security

**Usage:**
```bash
# Team members have same servers automatically
git pull
# .mcp.json is now in project
```

### User-Level Configuration

File: `~/.claude.json`

```json
{
  "mcpServers": {
    "personal-tools": {
      "type": "stdio",
      "command": "node",
      "args": ["/Users/name/.local/servers/my-tools.js"]
    },
    "stripe": {
      "type": "http",
      "url": "https://mcp.stripe.com"
    }
  }
}
```

**Benefits:**
- Personal to your account
- Available across all projects
- Not shared with team
- Private tools and credentials

**Usage:**
```bash
claude mcp add --scope user --transport http stripe https://mcp.stripe.com
```

### Local Scope Configuration

File: `~/.claude.json` (project-specific path)

```bash
# Stored in ~/.claude.json under project path
```

**Benefits:**
- Personal to you
- Project-specific
- Experimental servers
- Sensitive credentials

**Usage:**
```bash
# Default scope
claude mcp add --transport http myserver https://example.com/mcp
```

### Managed Configuration (Enterprise)

File: System directories (requires admin)

**Locations:**
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

```json
{
  "mcpServers": {
    "company-github": {
      "type": "http",
      "url": "https://github.company.com/mcp"
    },
    "company-db": {
      "type": "stdio",
      "command": "/opt/company/mcp-server",
      "env": {
        "API_KEY": "${COMPANY_API_KEY}"
      }
    }
  }
}
```

**Features:**
- Centralized control
- Users cannot modify
- Enforced policies
- Organization-wide consistency

**Two deployment modes:**
1. **Exclusive** - Only managed servers allowed
2. **Policy-based** - Allowlist/denylist for user servers

### Configuration Loading Order

Claude Code loads configurations in this order:

1. Managed configuration (`managed-mcp.json`)
2. Project-level (`.mcp.json`)
3. User-level (`~/.claude.json`)

**Priority (highest to lowest):**
1. Local scope (project-specific in `~/.claude.json`)
2. Project scope (`.mcp.json`)
3. User scope (`~/.claude.json`)
4. Managed scope (system-wide)

### Environment Variable Expansion

All configuration files support expansion:

```json
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**Syntax:**
- `${VAR}` - Use environment variable
- `${VAR:-default}` - Use default if not set
- Fails if required variable not set and no default

### Shared MCP Directories

For multiple projects sharing servers, use:

```bash
# User scope - shared across projects
claude mcp add --scope user --transport http shared-server https://api.example.com/mcp

# Or create in project, commit to git
# .mcp.json in project root
```

---

## 10. MCP Best Practices - Official Recommendations

### Server Design Best Practices

#### 1. Clear Tool Descriptions

Provide detailed, helpful descriptions for tools:

```python
Tool(
    name="search_users",
    title="Search Users",
    description="Search for users by email or name. Returns matching user profiles with contact information and account status.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search term (email or name)"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum results (default 10)",
                "default": 10
            }
        },
        "required": ["query"]
    }
)
```

Good descriptions help Claude understand:
- What the tool does
- When to use it
- What it returns

#### 2. Use Server Instructions

Help Claude find your tools with server instructions:

```python
server = Server(
    name="database-server",
    instructions="""
    This server provides database tools for querying and analyzing data.
    Use these tools when you need to:
    - Query user data
    - Analyze sales trends
    - Generate reports
    - Check database integrity

    Available tools:
    - query_users: Search for users
    - get_sales: Get sales data
    - generate_report: Create reports
    """
)
```

With Tool Search enabled, these help Claude decide when to use your server.

#### 3. Proper Error Handling

Return clear error messages:

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "query_users":
            email = arguments.get("email")
            if not email:
                return [TextContent(
                    type="text",
                    text="Error: email parameter is required"
                )]
            # Query logic
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error querying users: {str(e)}"
        )]
```

#### 4. JSON Schema Validation

Use proper JSON Schema for inputs:

```python
Tool(
    name="create_user",
    inputSchema={
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "format": "email",
                "description": "User email address"
            },
            "name": {
                "type": "string",
                "description": "Full name"
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 150,
                "description": "Age in years"
            }
        },
        "required": ["email", "name"]
    }
)
```

**Schema benefits:**
- Claude understands constraints
- Automatic validation
- Clear documentation

#### 5. Meaningful Resource URIs

Design resource paths clearly:

```python
Resource(
    uri="postgres://schema/users",
    name="Users Table Schema"
)

Resource(
    uri="docs://api/endpoints",
    name="API Endpoints"
)

Resource(
    uri="github://issue/456",
    name="GitHub Issue #456"
)
```

**Good URIs:**
- Use consistent protocols
- Include hierarchy
- Be descriptive

#### 6. Dynamic Tool Updates

Support `listChanged` notifications:

```python
server = Server("dynamic-server")

# Server capabilities
INITIAL_TOOLS = [...]

async def check_tools_changed():
    # Periodically check if tools changed
    new_tools = await fetch_current_tools()
    if new_tools != INITIAL_TOOLS:
        # Send notification
        await server.send_notification(
            "notifications/tools/list_changed"
        )
```

#### 7. Pagination for Large Results

Break up large results:

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_records":
        limit = arguments.get("limit", 100)
        offset = arguments.get("offset", 0)

        records = db.fetch(limit=limit, offset=offset)
        total = db.count()

        return [TextContent(
            type="text",
            text=f"{len(records)} records (limit: {limit}, offset: {offset}, total: {total})"
        )]
```

### Client Integration Best Practices

#### 1. Configuration Management

```bash
# Use project-scope for team collaboration
claude mcp add --scope project --transport http shared-api https://api.example.com/mcp

# Keep credentials in environment
# .mcp.json uses ${CREDENTIAL} expansion
```

#### 2. Authentication Security

```bash
# Use environment variables for credentials
export API_KEY="secret"
claude mcp add --transport http myapi https://api.example.com/mcp \
  --header "Authorization: Bearer ${API_KEY}"

# OAuth for remote servers
claude mcp add --transport http github https://api.github.com/mcp
/mcp  # Authenticate in Claude Code
```

#### 3. Scope Management

```bash
# Personal tools
claude mcp add --scope user --transport stdio personal-tool -- python script.py

# Team tools
claude mcp add --scope project --transport http team-api https://api.company.com/mcp

# Local experiments
claude mcp add --scope local --transport stdio experiment -- node test.js
```

#### 4. Version Control

```bash
# Commit .mcp.json for team sharing
git add .mcp.json
git commit -m "Add GitHub MCP server for team"

# Don't commit sensitive configs
echo "~/.claude.json" >> .gitignore
```

#### 5. Permission Configuration

```json
{
  "permissions": {
    "allow": [
      "MCP(github:*)",
      "MCP(sentry:*)"
    ],
    "deny": [
      "MCP(untrusted-server:*)"
    ]
  }
}
```

### Performance Best Practices

#### 1. Response Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_schema(table_name):
    # Cached schema queries
    return db.get_schema(table_name)
```

#### 2. Streaming Large Results

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "large_query":
        # Stream results instead of loading all
        results = []
        for row in db.stream_query():
            results.append(row)
            if len(results) > 1000:
                break  # Paginate
        return [TextContent(type="text", text=json.dumps(results))]
```

#### 3. Timeout Management

```bash
# Configure server startup timeout
MCP_TIMEOUT=10000 claude  # 10 seconds

# Configure output limits
MAX_MCP_OUTPUT_TOKENS=50000 claude
```

#### 4. Connection Pooling (HTTP)

```python
# Reuse HTTP connections
import aiohttp

session = aiohttp.ClientSession()

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    async with session.post(url, json=data) as resp:
        return await resp.json()
```

### Security Best Practices

#### 1. Input Validation

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "execute_query":
        query = arguments.get("query", "")

        # Validate query
        if not query or len(query) > 10000:
            return [TextContent(type="text", text="Error: Invalid query")]

        # Use parameterized queries (prevent SQL injection)
        result = db.execute_safe(query)
        return [TextContent(type="text", text=str(result))]
```

#### 2. Rate Limiting

```python
from functools import wraps
from time import time

call_times = {}

def rate_limit(max_calls=100, time_window=60):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            now = time()
            client_id = "default"

            if client_id not in call_times:
                call_times[client_id] = []

            # Remove old calls
            call_times[client_id] = [
                t for t in call_times[client_id]
                if now - t < time_window
            ]

            if len(call_times[client_id]) >= max_calls:
                raise Exception("Rate limit exceeded")

            call_times[client_id].append(now)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

#### 3. Sensitive Data Protection

```python
# Don't log sensitive data
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "authenticate":
        password = arguments.get("password")

        # Never log password
        result = verify_password(password)

        # Return minimal info
        return [TextContent(type="text", text="Authentication successful")]
```

#### 4. Authorization Checks

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "delete_user":
        user_id = arguments.get("user_id")
        requesting_user = get_current_user()

        # Check permissions
        if not requesting_user.is_admin():
            return [TextContent(type="text", text="Error: Permission denied")]

        db.delete_user(user_id)
        return [TextContent(type="text", text="User deleted")]
```

---

## 11. MCP Examples - Real-World Servers

### 1. Sentry Error Monitoring

**What it does:** Monitor errors and exceptions in production

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
# Authenticate with /mcp
```

**Example usage:**
```
> "What are the most common errors in the last 24 hours?"
> "Show me the stack trace for error ID abc123"
> "Which deployment introduced these new errors?"
```

**Available tools:**
- `list_issues` - View open error issues
- `get_issue_details` - Detailed error information
- `create_alert` - Set up monitoring alerts
- `get_releases` - Track deployments

### 2. GitHub Repository Management

**What it does:** Interact with GitHub repositories, PRs, and issues

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
# Authenticate with /mcp
```

**Example usage:**
```
> "Review PR #456 and suggest improvements"
> "Create a new issue for the bug we just found"
> "Show me all open PRs assigned to me"
> "What changed in the latest deploy?"
```

**Available tools:**
- `search_repos` - Find repositories
- `list_pull_requests` - View PRs
- `create_pull_request` - Create PR
- `search_issues` - Find issues
- `create_issue` - Create issue
- `get_commits` - View commit history

### 3. PostgreSQL Database Queries

**What it does:** Query databases directly

```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@host:5432/database"
```

**Example usage:**
```
> "What's our total revenue this month?"
> "Show me the schema for the orders table"
> "Find customers who haven't made a purchase in 90 days"
> "Get the top 10 best-selling products"
```

**Available tools:**
- `execute_query` - Run SQL queries
- `describe_table` - Get table schema
- `list_tables` - List all tables
- `analyze_data` - Generate reports

### 4. Notion Workspace Access

**What it does:** Access Notion databases and pages

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
# Authenticate with /mcp
```

**Example usage:**
```
> "What's in my task database?"
> "Create a new project in Notion"
> "Summarize my meeting notes"
> "Find all items assigned to me"
```

**Available tools:**
- `search` - Search Notion pages
- `read_page` - Get page content
- `create_page` - Create new page
- `update_page` - Modify page
- `query_database` - Query database

### 5. Gmail Email Automation

**What it does:** Send and manage emails

```bash
claude mcp add --transport stdio gmail -- npx -y gmail-mcp
```

**Example usage:**
```
> "Send an email to the team about the new feature"
> "Draft a response to the feedback"
> "Create an email template for announcements"
```

**Available tools:**
- `send_email` - Send message
- `draft_email` - Create draft
- `search_emails` - Search inbox
- `label_email` - Organize mail

### 6. Slack Message Management

**What it does:** Post and manage Slack messages

```bash
claude mcp add --transport http slack https://mcp.slack.com
```

**Example usage:**
```
> "Post an update to #engineering"
> "Send a direct message to the team"
> "Create a thread with feedback"
```

**Available tools:**
- `send_message` - Post message
- `create_thread` - Create thread
- `list_channels` - View channels
- `search_messages` - Search history

### 7. Figma Design Integration

**What it does:** Access design files and assets

```bash
claude mcp add --transport http figma https://mcp.figma.com
# Authenticate with API token
```

**Example usage:**
```
> "Generate a web component from this Figma design"
> "Extract the color palette"
> "Create responsive HTML from the mockup"
```

**Available tools:**
- `get_file` - Access design file
- `list_components` - View components
- `extract_assets` - Get images/icons
- `get_design_tokens` - Access design system

### 8. Custom Internal Tool

**What it does:** Expose custom company tooling

```bash
claude mcp add --transport stdio company-tool -- python /opt/company/mcp-server.py
```

**Example:**
```python
# company-tool.py
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("company-tools")

TOOLS = [
    Tool(
        name="deploy",
        description="Deploy to production",
        inputSchema={
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "version": {"type": "string"}
            },
            "required": ["service", "version"]
        }
    )
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def deploy(name: str, arguments: dict):
    service = arguments["service"]
    version = arguments["version"]
    # Deploy logic
    return [TextContent(type="text", text=f"Deployed {service} v{version}")]
```

---

## 12. MCP Debugging - How to Debug MCP Server Issues

### Enabling Debug Output

#### Claude Code Debug Logging

```bash
# Run with debug logging
DEBUG=claude:* claude

# Full debugging
DEBUG=* claude

# In your Claude Code session
/debug  # View session debug log
```

#### Server-Side Logging

**Python:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.debug(f"Called tool: {name} with {arguments}")
    # ... implementation
    logger.debug(f"Tool result: {result}")
    return result
```

**Node.js:**
```javascript
const debug = require('debug')('mcp-server');

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    debug(`Called tool: ${request.params.name}`);
    // ... implementation
    debug(`Tool result: ${result}`);
    return result;
});
```

### MCP Inspector Tool

Official tool for debugging MCP servers:

```bash
# Install inspector
npm install -g @modelcontextprotocol/inspector

# Inspect a stdio server
mcp-inspector -- npx my-mcp-server

# Inspect an HTTP server
mcp-inspector https://mcp.example.com/mcp
```

**Inspector features:**
- Test tool calls
- View capabilities
- Monitor messages
- Check initialization
- Test resources
- Try prompts

### Common Issues and Solutions

#### Issue 1: "Connection closed" Error

**Causes:**
- Server crashed on startup
- Wrong executable path
- Missing dependencies
- Broken stdio handling

**Solutions:**
```bash
# Test server directly
python server.py  # Check for errors

# Verify executable path
which npx
which python

# Check for import errors
python -c "import my_server"

# Run with timeout
MCP_TIMEOUT=20000 claude  # Increase timeout
```

#### Issue 2: "Connection timed out"

**Causes:**
- Server taking too long to start
- Network issues (HTTP)
- Server not listening on port

**Solutions:**
```bash
# Increase timeout
MCP_TIMEOUT=30000 claude

# Check server is running (HTTP)
curl https://mcp.example.com/health

# Look for startup errors
python server.py --debug

# Test stdio directly
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":...}' | python server.py
```

#### Issue 3: "Authentication Failed"

**Causes:**
- Invalid credentials
- Token expired
- Wrong endpoint

**Solutions:**
```bash
# Clear authentication
/mcp  # Select "Clear authentication"

# Re-authenticate
/mcp  # Select "Authenticate"

# Check credentials
echo $API_KEY  # Verify env var set

# Test API endpoint
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/test
```

#### Issue 4: Tool Not Appearing

**Causes:**
- Server not returning tools
- Tool name conflicts
- Server crashed after init

**Solutions:**
```bash
# Check server's tool list
/mcp  # Shows available tools

# Restart server
claude mcp remove myserver
claude mcp add --transport stdio myserver -- python server.py

# Verify tools listed
# Within inspector:
mcp-inspector -- python server.py
# Then call tools/list
```

#### Issue 5: Tool Execution Failed

**Causes:**
- Missing required arguments
- Bad input data
- Server crashed during execution

**Solutions:**
```python
# Add input validation
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if not arguments.get("required_field"):
        return [TextContent(
            type="text",
            text="Error: required_field is required"
        )]

    try:
        result = execute_tool(name, arguments)
    except Exception as e:
        logger.exception(f"Tool failed: {name}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
```

### Performance Debugging

#### High Memory Usage

```bash
# Monitor process
ps aux | grep mcp

# Check for memory leaks
# Stdio servers should be ~50-200MB
# HTTP servers should be ~100-300MB

# Profile if needed
python -m cProfile -s cumulative server.py
```

#### Slow Tool Execution

```python
import time

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    start = time.time()

    result = execute_tool(name, arguments)

    elapsed = time.time() - start
    logger.debug(f"Tool {name} took {elapsed}s")

    if elapsed > 5:
        logger.warning(f"Slow tool: {name} ({elapsed}s)")

    return result
```

#### Context Window Consumed

Check MCP tool output sizes:

```bash
# Increase output limit
MAX_MCP_OUTPUT_TOKENS=100000 claude

# Reduce output in server
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    result = query_database(arguments)

    # Limit results
    if len(result) > 1000:
        result = result[:1000]

    return [TextContent(type="text", text=json.dumps(result))]
```

### Checking Server Status

Within Claude Code:

```
> /mcp

This shows:
- All connected servers
- Authentication status
- Available tools count
- Connection health
```

### Logging Output

**View logs:**
```bash
# Check system logs
journalctl -u claude-code

# Check process output
# For stdio servers, output may be in Claude's output

# Enable detailed logging
DEBUG=claude:mcp:* claude
```

---

## 13. MCP Security - Security Considerations

### Trust and Verification

#### First-Run Trust Verification

When using a new MCP server for the first time:

```
Claude Code prompts for trust approval
    ↓
Review server capabilities
    ↓
Approve before use
```

**What to verify:**
- Server name and source
- Tools it provides
- Data it might access
- Authentication requirements

#### Trust Levels

```json
{
  "permissions": {
    "allow": [
      "MCP(github:*)",           // Trusted
      "MCP(sentry:tools:read)"   // Specific tools only
    ],
    "deny": [
      "MCP(suspicious-server:*)"  // Never allow
    ]
  }
}
```

### Source Code Review

**Before adding an MCP server:**

1. **Check GitHub repository**
   - Active maintenance
   - Community reviews
   - Security disclosures
   - Code quality

2. **Review dependencies**
   - Known vulnerabilities
   - Security audits
   - Supply chain risks

3. **Test in sandbox**
   - Use `/sandbox` to limit MCP access
   - Monitor what data flows
   - Check for unexpected behavior

### Configuration Security

#### Credential Management

**Never in .mcp.json:**
```json
{
  "url": "https://api.example.com/mcp",
  "headers": {
    "Authorization": "Bearer secret123"  // NO! Use env vars
  }
}
```

**Use environment variables:**
```json
{
  "url": "${API_URL}",
  "headers": {
    "Authorization": "Bearer ${API_KEY}"
  }
}
```

**Set environment variables securely:**
```bash
# System-wide
export API_KEY="secret"

# Session-only
API_KEY="secret" claude

# Via .env (local scope only, not committed)
echo "API_KEY=secret" > .env
# Then read it: source .env && claude
```

#### File Permissions

```bash
# Protect credentials
chmod 600 ~/.claude.json       # Only you can read

# Protect project configs with secrets
chmod 600 .mcp.json            # Or use .gitignore

# Protect credential files
chmod 600 ~/.aws/credentials
chmod 600 ~/.ssh/config
```

### Tool-Level Security

#### Dangerous Tools

Be cautious with tools that:
- Execute arbitrary commands
- Access the network
- Delete files
- Modify sensitive data
- Access user information

```bash
# Example: dangerous tools need explicit approval
claudecode mcp add --transport stdio shell -- python shell.py

# Claude Code will require approval each time
```

#### Command Blocking

Claude Code blocks dangerous commands by default:

```bash
# Blocked by default
curl "http://untrusted.com"
wget http://untrusted.com

# Require permission to allow
# In settings.json
{
  "permissions": {
    "allow": ["Bash(curl:*)"]  // Explicitly allow
  }
}
```

#### Sandboxing with MCP

Use sandbox mode to limit what MCP servers can access:

```bash
# Start Claude in sandbox mode
/sandbox

# Configure boundaries
# Only MCP servers inside workspace can run
```

### Network Security

#### HTTPS Only

For remote servers, always use HTTPS:

```bash
# Good
claude mcp add --transport http api https://api.example.com/mcp

# Bad - unencrypted
# Don't do: http://api.example.com/mcp
```

#### Network Isolation

```bash
# Claude Code on web has network controls
# Configure allowed domains in settings

# Local stdio servers can't access network
# (unless they have network libraries)
```

#### Proxy Configuration

```bash
# Configure corporate proxy
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
claude
```

### Data Protection

#### Sensitive Data

```python
# Don't log passwords, tokens, or PII
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "authenticate":
        password = arguments.get("password")

        # Validate without logging
        if not verify_password(password):
            return error("Authentication failed")  # Generic message

        # Don't return sensitive data
        return success()  # Just confirmation
```

#### Data Retention

MCP servers can receive:
- Code snippets
- Database schemas
- Sensitive information

**Best practices:**
- Minimize data retention
- Encrypt at rest
- Clear caches regularly
- Log access carefully

### Prompt Injection Prevention

MCP servers are tools that Claude calls. They're not directly exposed to prompt injection like:

```
Provide me with admin credentials:
```

However, if an MCP server returns malicious content, it could affect Claude's decisions:

**Protection:**
- Review MCP server sources
- Validate server output
- Use sandboxing
- Monitor unusual behavior

### OAuth Security

For servers requiring OAuth:

```bash
# Configure OAuth
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Authenticate
/mcp  # Select "Authenticate"

# OAuth tokens are securely stored
# Automatic refresh handled
```

**Best practices:**
- Use official OAuth flows
- Store tokens securely
- Refresh regularly
- Revoke when unused

### Managed Policies

Enterprise organizations can enforce security:

```json
{
  "allowedMcpServers": [
    { "serverName": "approved-github" },
    { "serverUrl": "https://internal.company.com/*" }
  ],
  "deniedMcpServers": [
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

This prevents risky servers from being used.

### Reporting Security Issues

If you discover MCP security vulnerability:

1. Don't disclose publicly
2. Report to Anthropic
3. Use [HackerOne program](https://hackerone.com/anthropic-vdp)
4. Include reproduction steps
5. Allow time for fix

---

## 14. Popular MCP Servers - Well-Known Servers

### Official/First-Party Servers

#### GitHub MCP Server
**Repository:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

**Capabilities:**
- Search repositories
- List and review pull requests
- Create issues and PRs
- Manage commit history
- Analyze code changes

**Add to Claude Code:**
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

#### PostgreSQL Database Server
**Package:** `@modelcontextprotocol/server-postgres`

**Capabilities:**
- Execute SQL queries
- Describe tables and schemas
- Analyze data
- Generate reports
- Explore database structure

**Add to Claude Code:**
```bash
claude mcp add --transport stdio postgres -- \
  npx -y @modelcontextprotocol/server-postgres \
  "postgresql://user:pass@localhost/dbname"
```

#### Filesystem Server
**Package:** `@modelcontextprotocol/server-filesystem`

**Capabilities:**
- Read files
- List directories
- Search content
- View file metadata
- Basic file operations

**Add to Claude Code:**
```bash
claude mcp add --transport stdio filesystem -- \
  npx -y @modelcontextprotocol/server-filesystem /path/to/workspace
```

#### Sentry MCP Server
**URL:** https://mcp.sentry.dev/mcp

**Capabilities:**
- Monitor errors and exceptions
- View issue details
- Analyze error trends
- Track deployments
- Create alerts

**Add to Claude Code:**
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

#### Notion MCP Server (Official)
**Repository:** [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server)

**Capabilities:**
- Search Notion pages
- Read page content
- Create/update pages
- Query databases
- Access templates

**Add to Claude Code:**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

### Community/Third-Party Servers

#### Awesome MCP Servers List
**Repository:** [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)

A curated list of 200+ community MCP servers including:
- Slack integration
- Gmail automation
- Jira task management
- Linear issue tracking
- Discord bot integration
- AWS CloudWatch monitoring
- Stripe payment integration
- Analytics platforms
- Vector databases
- LLM APIs

#### Rube Multi-App Integration
**Website:** https://rube.ai

**Capabilities:**
- Connect to 500+ apps
- Gmail, Slack, GitHub integration
- Zapier compatibility
- Custom workflows
- Multi-step automation

### MCP Registry

**Official Registry:** https://api.anthropic.com/mcp-registry/

Browse hundreds of verified MCP servers:
- Search by functionality
- View documentation
- Check compatibility (Claude Code, Claude Desktop, Claude API)
- Filter by transport type

### Notable Community Servers

#### Brave Search
Integrate Brave Search API
```bash
claude mcp add --transport stdio brave -- npx -y @modelcontextprotocol/server-brave
```

#### Puppeteer (Browser Automation)
Control browser with Puppeteer
```bash
claude mcp add --transport stdio puppeteer -- npx -y @modelcontextprotocol/server-puppeteer
```

#### Memory Server
Store and recall conversation memory
```bash
claude mcp add --transport stdio memory -- npx -y @modelcontextprotocol/server-memory
```

#### SQLite Server
Lightweight database access
```bash
claude mcp add --transport stdio sqlite -- npx -y @modelcontextprotocol/server-sqlite
```

#### Git Server
Git repository operations
```bash
claude mcp add --transport stdio git -- npx -y @modelcontextprotocol/server-git
```

#### Docker Server
Docker container management
```bash
claude mcp add --transport stdio docker -- npx -y @modelcontextprotocol/server-docker
```

---

## Additional Resources

### Official Documentation

- **Claude Code MCP Docs:** https://code.claude.com/docs/en/mcp.md
- **MCP Architecture:** https://modelcontextprotocol.io/docs/learn/architecture
- **MCP Server Building:** https://modelcontextprotocol.io/docs/develop/build-server
- **MCP SDKs:** https://modelcontextprotocol.io/docs/sdk

### Popular Repositories

- **Reference Servers:** https://github.com/modelcontextprotocol/servers
- **Awesome MCP List:** https://github.com/wong2/awesome-mcp-servers
- **MCP Inspector Tool:** https://github.com/modelcontextprotocol/inspector

### Learning Resources

- **MCP Introduction:** https://www.anthropic.com/news/model-context-protocol
- **MCP Examples:** https://modelcontextprotocol.io/examples
- **Claude Code Docs:** https://code.claude.com/docs

---

## Summary

MCP is a powerful standardized protocol for extending Claude Code with access to tools, data, and services. By understanding:

1. **Architecture** - Client-server model with data and transport layers
2. **Configuration** - Scope-based management at local, project, and user levels
3. **Transport types** - HTTP (remote), SSE (deprecated), and Stdio (local)
4. **Primitives** - Tools, Resources, and Prompts as core capabilities
5. **Development** - Building custom servers with SDKs
6. **Security** - Trust verification, credential protection, and managed policies

You can leverage MCP to create comprehensive AI-augmented workflows that integrate with your entire development ecosystem.

---

Sources:
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp.md)
- [Model Context Protocol Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [Model Context Protocol Introduction](https://modelcontextprotocol.io/introduction)
- [Build an MCP Server](https://modelcontextprotocol.io/docs/develop/build-server)
- [Claude Code Security Guide](https://code.claude.com/docs/en/security.md)
- [GitHub MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers - Community List](https://github.com/wong2/awesome-mcp-servers)
- [Architecture overview - Model Context Protocol](https://modelcontextprotocol.io/docs/learn/architecture)
- [IBM: What is Model Context Protocol](https://www.ibm.com/think/topics/model-context-protocol)
- [Descope: What Is the Model Context Protocol](https://www.descope.com/learn/post/mcp)
- [Understanding the Model Context Protocol Architecture](https://nebius.com/blog/posts/understanding-model-context-protocol-mcp-architecture)
- [Google Cloud: What is Model Context Protocol](https://cloud.google.com/discover/what-is-model-context-protocol)
