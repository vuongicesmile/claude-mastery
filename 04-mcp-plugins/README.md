# Module 04 — MCP Plugins (Model Context Protocol)

> MCP = cách extend Claude với external tools, data sources, APIs
> Giống như "USB ports" cho Claude — cắm tool nào vào là Claude dùng được tool đó

## 🔌 MCP Architecture

```
Claude Code
    ↕ MCP Protocol
MCP Servers (tools)
    ↕
External Services (GitHub, DB, Slack, Browser...)
```

## ⚙️ Cấu hình MCP

Trong `~/.claude/settings.json` hoặc `.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://..."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-key"
      }
    }
  }
}
```

## 🛠 Popular MCP Servers

### Official (Anthropic)
```bash
@modelcontextprotocol/server-github      # GitHub repos, PRs, issues
@modelcontextprotocol/server-postgres    # Query PostgreSQL
@modelcontextprotocol/server-sqlite      # Query SQLite
@modelcontextprotocol/server-filesystem  # Read/write files
@modelcontextprotocol/server-brave-search # Web search
@modelcontextprotocol/server-slack       # Slack messages
@modelcontextprotocol/server-puppeteer   # Browser automation
```

### Community
```bash
mcp-server-supabase     # Supabase queries
mcp-server-redis        # Redis operations
mcp-server-docker       # Docker container management
mcp-server-kubernetes   # K8s cluster management
mcp-server-datadog      # Logs & metrics
mcp-server-jira         # Jira tickets
mcp-server-notion       # Notion pages
```

## 🐙 GitHub MCP — Use Cases

Sau khi config GitHub MCP:

```
"Show me all open PRs in vuonglearning/vuonglearning"
"Find issues labeled 'bug' from last week"
"What changed in the auth module in the last 10 commits?"
"Create an issue: [title and description]"
"Review PR #123 and leave inline comments"
```

## 🗄 Database MCP — Use Cases

```
"How many active users signed up this month?"
"Find the top 10 users by token usage"
"Are there any orphaned records in the sessions table?"
"Optimize this slow query: [SQL]"
"Show the schema for the progress table"
```

## 🌐 Browser/Puppeteer MCP

```
"Navigate to localhost:3000 and take a screenshot"
"Fill out the login form and check if it works"
"Scrape the pricing table from [url]"
"Run the E2E test flow manually and report issues"
```

## 🔨 Build Your Own MCP Server

```typescript
// my-mcp-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js"

const server = new Server(
  { name: "my-tools", version: "1.0.0" },
  { capabilities: { tools: {} } }
)

// Define a tool
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "get_weather",
    description: "Get current weather for a city",
    inputSchema: {
      type: "object",
      properties: {
        city: { type: "string", description: "City name" }
      },
      required: ["city"]
    }
  }]
}))

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "get_weather") {
    const city = request.params.arguments?.city
    // Call weather API...
    return { content: [{ type: "text", text: `Weather in ${city}: Sunny, 28°C` }] }
  }
})

// Start
const transport = new StdioServerTransport()
await server.connect(transport)
```

```json
// Add to settings.json
{
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["tsx", "/path/to/my-mcp-server.ts"]
    }
  }
}
```

## 🔒 Security Best Practices

```
✅ Store API keys in env vars, never hardcode
✅ Use read-only tokens where possible
✅ Scope permissions minimally (read vs write vs admin)
✅ Review what tools are available before sensitive operations
⚠️  MCP servers run with YOUR system permissions
⚠️  Be careful with filesystem MCP — can read/write any file
⚠️  Never give MCP servers production DB write access
```
