# PostgreSQL MCP Plugin for Claude Code

Connect Claude Code to PostgreSQL databases using [CrystalDBA's postgres-mcp](https://github.com/crystaldba/postgres-mcp).

## Quick Start

1. Run `/postgres-setup` in Claude Code
2. Answer 3 questions: connection name, DATABASE_URI, access mode
3. Restart Claude Code
4. Verify: run `/mcp` to see the new server

To add more databases, run `/postgres-setup` again.

## Prerequisites

- **uv** (recommended) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- or **pipx** — `brew install pipx`
- or **Docker**

## Adding Connections

### Via Claude Code (recommended)

Run `/postgres-setup`. You'll be asked for:

| Input | Description | Example |
|-------|-------------|---------|
| **Name** | MCP server name (your choice) | `postgres-shipping-dev` |
| **DATABASE_URI** | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| **Access Mode** | `unrestricted` or `restricted` | `unrestricted` |

### Manual configuration

Add to `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "postgres-shipping-dev": {
      "command": "/path/to/postgres-mcp/scripts/run_postgres_mcp.sh",
      "env": {
        "DATABASE_URI": "postgresql://user:password@host:5432/dbname",
        "ACCESS_MODE": "unrestricted"
      }
    }
  }
}
```

Add multiple connections by adding more entries under `mcpServers`.

## How It Works

1. Claude Code launches `run_postgres_mcp.sh` on startup
2. The script reads `DATABASE_URI` from the env and starts `postgres-mcp` via uvx
3. Claude communicates with the MCP server over stdio

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_schemas` | List all schemas in the database |
| `list_objects` | List tables, views, sequences in a schema |
| `get_object_details` | Show detailed info about a table/view |
| `execute_sql` | Execute SQL queries |
| `explain_query` | Get execution plan with cost estimates |
| `analyze_query_indexes` | Recommend indexes for specific queries |
| `analyze_workload_indexes` | Analyze workload and recommend indexes |
| `analyze_db_health` | Check database health |
| `get_top_queries` | Report slowest/most resource-intensive queries |

## Access Modes

| Mode | Description | Use For |
|------|-------------|---------|
| `unrestricted` | Full read/write access | Development, Staging |
| `restricted` | Read-only access | Production |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No supported runtime found" | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| "DATABASE_URI is not set" | Check the `env` section in `.mcp.json` |
| MCP server not connecting | Restart Claude Code after changing `.mcp.json` |
| Server not listed in `/mcp` | Check `enabledMcpjsonServers` in `.claude/settings.local.json` |

## File Structure

```
postgres-mcp/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── postgres-setup/
│       └── SKILL.md         # /postgres-setup skill
├── scripts/
│   └── run_postgres_mcp.sh  # Launch MCP server (uvx → pipx → docker)
├── templates/
│   ├── mcp-config.json      # Template for .mcp.json
│   └── settings-local.json  # Template for settings.local.json
└── README.md
```
