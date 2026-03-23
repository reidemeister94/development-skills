# Claude Code Reference Documentation

Comprehensive reference documentation for building Claude Code plugins, skills, agents, and extensions. This is the knowledge base for the **opensource-ai-utils** (Claude Code Marketplace) project.

> **Source:** Official Claude Code documentation, Agent SDK docs, and MCP specification.
> **Last updated:** 2026-02-25

---

## Documents

### [01 - Skills (SKILL.md)](./01-skills.md)
Complete reference for Claude Code Skills — reusable instruction sets that extend capabilities.
- SKILL.md file format and frontmatter specification
- Skill discovery, loading, and invocation
- Slash commands, automatic detection, parameters
- Skill scoping (project, user, global)
- Dynamic content injection (`!`command``)
- Advanced patterns: conditional logic, tool restrictions, agent delegation
- Debugging and sharing

### [02 - Hooks](./02-hooks.md)
Complete reference for Claude Code Hooks — deterministic automation at lifecycle events.
- All 17+ hook event types (SessionStart, PreToolUse, PostToolUse, Stop, etc.)
- Hook configuration format, locations, and scope hierarchy
- Matchers (regex patterns for tool names, events)
- Three hook types: command, prompt, agent
- Response formats (exit codes, JSON output, permission decisions)
- Environment variables (`CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE`, etc.)
- Real-world examples (formatting, protection, notifications, testing)
- Advanced patterns (chaining, multi-stage validation, CI/CD integration)

### [03 - MCP Servers](./03-mcp-servers.md)
Complete reference for Model Context Protocol integration.
- MCP architecture (client-server, JSON-RPC 2.0)
- Transport types: stdio, SSE, streamable HTTP
- Server configuration and lifecycle management
- MCP tools, resources, and prompts
- Building custom MCP servers (Python, TypeScript)
- Security considerations and best practices
- Popular MCP servers for common integrations

### [04 - Agent SDK](./04-agent-sdk.md)
Complete reference for the Claude Agent SDK and agent system.
- Agent types (general-purpose, Explore, Plan, custom, teams)
- Task tool and subagent delegation
- Building agents (Python SDK, TypeScript SDK, filesystem-based)
- Orchestration patterns (sequential, parallel, hierarchical, map-reduce)
- Agent isolation (context, worktrees, sandbox)
- SDK API reference (query, Options, AgentDefinition, message types)
- Headless/CI mode and Docker deployment

### [05 - Configuration & Settings](./05-configuration.md)
Complete reference for all Claude Code configuration options.
- CLAUDE.md specification (hierarchy, imports, scoping)
- Settings files (settings.json locations, all available settings)
- All slash commands (/help, /clear, /compact, /config, /model, etc.)
- Keyboard shortcuts and customization
- Permission modes and permission rules
- IDE integrations (VS Code, JetBrains)
- CLI flags and options
- Environment variables
- Context management and compression
- Model selection and cost management
- Git integration
- Security model and sandboxing

### [06 - Best Practices & Patterns](./06-best-practices.md)
Curated best practices for power users and plugin developers.
- Prompt engineering techniques
- CLAUDE.md optimization strategies
- Workflow patterns (plan-then-implement, TDD, writer/reviewer)
- Performance and token/cost optimization
- Multi-file editing and monorepo patterns
- Testing integration strategies
- Code review workflows
- CI/CD integration
- Team collaboration
- Security best practices
- Common pitfalls and how to avoid them
- Power user tips (keyboard shortcuts, session management, worktrees)

---

## Quick Links

| Topic | File | Key Section |
|-------|------|-------------|
| Creating a skill | [01-skills.md](./01-skills.md) | SKILL.md File Format |
| Hook events reference | [02-hooks.md](./02-hooks.md) | Hook Types |
| Setting up MCP server | [03-mcp-servers.md](./03-mcp-servers.md) | MCP Server Configuration |
| Building custom agent | [04-agent-sdk.md](./04-agent-sdk.md) | Building Custom Agents |
| CLAUDE.md structure | [05-configuration.md](./05-configuration.md) | CLAUDE.md Files |
| All slash commands | [05-configuration.md](./05-configuration.md) | Slash Commands |
| Permission system | [05-configuration.md](./05-configuration.md) | Permission Modes |
| CI/CD setup | [06-best-practices.md](./06-best-practices.md) | CI/CD Integration |
| Cost optimization | [06-best-practices.md](./06-best-practices.md) | Token/Cost Optimization |
| Keyboard shortcuts | [06-best-practices.md](./06-best-practices.md) | Power User Tips |

---

## How This Relates to opensource-ai-utils

This reference documentation serves as the foundation for building and improving Claude Code marketplace plugins. Key applications:

- **Plugin development:** Use Skills, Hooks, and Agent patterns documented here
- **Quality standards:** Follow best practices for SKILL.md, hooks, and agent definitions
- **MCP integration:** Build MCP servers for database, cloud, and service integrations
- **CI/CD automation:** Leverage headless mode and GitHub Actions for automated workflows
- **Team sharing:** Distribute plugins as shared skills, agents, and MCP configurations
