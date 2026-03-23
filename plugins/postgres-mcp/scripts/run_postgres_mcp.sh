#!/bin/bash
# Run postgres-mcp server with DATABASE_URI from environment.
# Usage: called by Claude Code via mcpServers config.
#
# Required env var:
#   DATABASE_URI  - PostgreSQL connection string
#                   e.g. postgresql://user:password@host:5432/dbname
#
# Optional env var:
#   ACCESS_MODE   - unrestricted (default, full read/write) or restricted (read-only)

ACCESS_MODE="${ACCESS_MODE:-unrestricted}"

if [ -z "$DATABASE_URI" ]; then
    echo "Error: DATABASE_URI env var is not set." >&2
    echo "Set it in your mcpServers config env section." >&2
    exit 1
fi

if [ "$ACCESS_MODE" != "unrestricted" ] && [ "$ACCESS_MODE" != "restricted" ]; then
    echo "Error: Invalid ACCESS_MODE '$ACCESS_MODE'. Use 'unrestricted' or 'restricted'." >&2
    exit 1
fi

# Launch MCP server: uvx → pipx → docker
if command -v uvx &> /dev/null; then
    exec uvx postgres-mcp --access-mode="$ACCESS_MODE"
elif command -v pipx &> /dev/null; then
    exec pipx run postgres-mcp --access-mode="$ACCESS_MODE"
elif command -v docker &> /dev/null && docker info &> /dev/null 2>&1; then
    exec docker run --rm -i \
        -e DATABASE_URI="$DATABASE_URI" \
        -e ACCESS_MODE="$ACCESS_MODE" \
        crystaldba/postgres-mcp:latest
else
    echo "Error: No supported runtime found." >&2
    echo "Install uv (recommended): curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi
