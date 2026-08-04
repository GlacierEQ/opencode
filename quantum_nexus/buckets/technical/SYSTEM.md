# TECHNICAL BUCKET
## System Architecture & Configuration

### Core Components
```
quantum_nexus/
├── core/vault.py          # 229 API keys
├── memory/orchestrator.py # Mem0, Pinecone, Supermemory
├── legal/courtlistener.py # CourtListener API v4
├── mcp/server.py          # 30+ MCP tools
└── run.py                 # CLI interface
```

### Installed Tools
- **opencode:** v1.18.11 (binary in /usr/local/bin)
- **Desktop Commander:** v0.2.46 (MCP connected)
- **rclone:** Cloud storage sync
- **GitHub CLI:** v2.97.0 (authenticated)

### MCP Servers
| Server | Status | Tools |
|--------|--------|-------|
| desktop-commander | ✓ Connected | Terminal, Files |

### API Endpoints
| Service | URL | Auth |
|---------|-----|------|
| CourtListener | courtlistener.com/api/rest/v4 | Token |
| GitHub | api.github.com | Bearer |
| Notion | api.notion.com/v1 | Bearer |
| Supabase | kjebmdgvjvuutzvhbtp.supabase.co | JWT |

### Python Packages
- mem0ai
- aiohttp
- python-dotenv
- google-auth
- google-api-python-client
- notion-client

### Node Packages
- opencode-ai
- @wonderwhy-er/desktop-commander
- npx (global)
