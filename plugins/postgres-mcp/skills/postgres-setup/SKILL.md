---
name: postgres-setup
description: "Add a PostgreSQL database connection to this project via MCP. Use when asked to 'connect to PostgreSQL', 'add a database connection', 'set up the Postgres MCP', 'configure database access for Claude', or 'I want Claude to query my database'."
compatibility: Claude Code
metadata:
  author: salvob41
  version: 1.0.0
  mcp-server: postgres
  category: infrastructure
---

# PostgreSQL MCP — Add Connection

Add a PostgreSQL database connection. Each invocation adds ONE connection.
Run `/postgres-setup` again to add more databases.

## When This Triggers

- User runs `/postgres-setup`
- User asks to "set up postgres", "add a database", "configure database connection", etc.
- A postgres MCP tool fails with a connection or setup error

## Setup Flow

### Step 1: Check Existing Configuration

```bash
cat .mcp.json 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    servers = [k for k in data.get('mcpServers', {}) if k.startswith('postgres-')]
    if servers:
        print('CONFIGURED: ' + ', '.join(servers))
    else:
        print('NOT_CONFIGURED')
except:
    print('NOT_CONFIGURED')
"
```

- If **NOT_CONFIGURED**: "Let's set up your first PostgreSQL connection."
- If **CONFIGURED**: show the existing server names and ask:
  "You already have these PostgreSQL connections: [list]. Do you want to **add another**, or are you having **issues with an existing one**?"
  - If adding another → proceed to Step 2
  - If troubleshooting → jump to Troubleshooting section

### Step 2: Check Prerequisites

```bash
command -v python3 &>/dev/null && echo "OK_PYTHON" || echo "MISSING_PYTHON"
command -v uvx &>/dev/null && echo "RUNTIME=uvx" || (command -v pipx &>/dev/null && echo "RUNTIME=pipx" || (command -v docker &>/dev/null && echo "RUNTIME=docker" || echo "NO_RUNTIME"))
```

- If MISSING_PYTHON: "Install Python 3 first"
- If NO_RUNTIME: "Install uv (recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`"

### Step 3: Ask for Connection Details

Ask the user these 3 questions using AskUserQuestion:

1. **Connection name**: "What name should this connection have? This becomes the MCP server name."
   - Examples: `postgres-shipping-dev`, `postgres-billing-prod`, `postgres-analytics-staging`
   - Must contain only letters, numbers, hyphens, underscores

2. **DATABASE_URI**: "What is the PostgreSQL connection string?"
   - Format: `postgresql://username:password@host:5432/dbname`
   - This stays on your machine only — never committed anywhere

3. **Access Mode**: "What access mode?"
   - `unrestricted` — full read/write (for dev/staging)
   - `restricted` — read-only (recommended for production)
   - Default: `unrestricted`

### Step 4: Find Plugin Path

Locate the run script:

```bash
find ~/.claude -name "run_postgres_mcp.sh" -path "*/postgres-mcp/*" 2>/dev/null | head -1
```

If not found:
```bash
find ~/Documents ~/dev ~/workspace -path "*/postgres-mcp/scripts/run_postgres_mcp.sh" 2>/dev/null | head -1
```

Store the absolute path to `run_postgres_mcp.sh` as SCRIPT_PATH.

### Step 5: Generate Configuration

Add this ONE server to both config files. **Always merge — never overwrite existing entries.**

**`.mcp.json`** in project root:

Read existing file (or start with `{}`), add the new server under `mcpServers`:

```json
{
  "mcpServers": {
    "<NAME>": {
      "command": "<SCRIPT_PATH>",
      "env": {
        "DATABASE_URI": "<DATABASE_URI>",
        "ACCESS_MODE": "<MODE>"
      }
    }
  }
}
```

Use Read to load existing `.mcp.json`, add the new key to `mcpServers`, use Write to save.
If the name already exists, overwrite that entry (allows reconfiguration).

**`.claude/settings.local.json`**:

Read existing file (or start with `{}`), append to the arrays (skip if already present):

- `enabledMcpjsonServers`: add `"<NAME>"`

### Step 6: Done

Tell the user:
1. "Added **<NAME>** to `.mcp.json`."
2. "**Restart Claude Code** to load the new MCP server."
3. "After restart, run `/mcp` to verify the server appears and is connected."
4. "Test it: 'List schemas using <NAME>'"
5. "To add another database connection, just run `/postgres-setup` again."

## Troubleshooting

If setup completed but tools still don't work:

1. **Check runtime**: `uvx --version` or `pipx --version` or `docker info`
2. **Test DATABASE_URI manually**: `psql "$DATABASE_URI" -c "SELECT 1"`
3. **Check .mcp.json**: verify the server entry and DATABASE_URI are correct
4. **Check /mcp**: run `/mcp` in Claude Code to see server status and errors

## Examples

### Example 1: Add a primary database
User says: "Connect Claude to our production database"
Actions: Ask for connection URI + name → write .mcp.json entry → confirm setup
Result: Database accessible as MCP tool, Claude can run queries

### Example 2: Add a second database
User says: "Also connect to our analytics database"
Actions: Read existing .mcp.json → ask for new URI + name → append entry
Result: Both databases accessible with distinct names
