# Quantum Nexus - Sovereign Intelligence System

## Overview
Unified quantum legal intelligence architecture for Case 1FDV-23-0001009 (Hawaii Family Court).

## Structure
```
quantum_nexus/
├── __init__.py          # Package exports
├── run.py               # CLI launcher
├── core/
│   ├── __init__.py
│   └── vault.py         # 229 API keys, service configs
├── memory/
│   ├── __init__.py
│   └── orchestrator.py  # Mem0, Pinecone, Supermemory
├── legal/
│   ├── __init__.py
│   └── courtlistener.py # CourtListener API v4 client
└── mcp/
    ├── __init__.py
    └── server.py        # 30+ MCP tools
```

## Usage
```bash
# Show system status
PYTHONPATH=/root python3 /root/quantum_nexus/run.py status

# Store a memory
PYTHONPATH=/root python3 /root/quantum_nexus/run.py store "Legal filing prepared"

# Search memories
PYTHONPATH=/root python3 /root/quantum_nexus/run.py search "due process"

# Search CourtListener
PYTHONPATH=/root python3 /root/quantum_nexus/run.py court "family court"

# Get due process cases
PYTHONPATH=/root/python3 /root/quantum_nexus/run.py due-process

# Get habeas corpus cases
PYTHONPATH=/root/python3 /root/quantum_nexus/run.py habeas

# Research legal topic
PYTHONPATH=/root/python3 /root/quantum_nexus/run.py research "parental rights"

# Export all memories
PYTHONPATH=/root/python3 /root/quantum_nexus/run.py export

# Show vault info
PYTHONPATH=/root/python3 /root/quantum_nexus/run.py vault
```

## MCP Server
The quantum_nexus.mcp.server module exposes 30+ tools:
- memory_store, memory_search, memory_export, memory_legal_store, memory_context
- courtlistener_search, courtlistener_docket, courtlistener_entries, courtlistener_opinions
- courtlistener_judges, courtlistener_citations, courtlistener_alerts, courtlistener_financials
- legal_research, due_process_cases, habeas_corpus
- github_repos, github_search, github_issues, github_commits
- notion_search, notion_page, notion_chats, notion_create_page
- supabase_query, supabase_insert, supabase_update
- clickup_tasks, taskade_workspaces, elevenlabs_tts, assemblyai_transcribe
- vault_status, get_context, swarm_status

## Working Services
✓ CourtListener - Legal research
✓ GitHub - Code & repos
✓ Supabase - Database
✓ Mem0 - Memory
✓ Pinecone - Vector search
✓ Notion - Documentation

## Mission
BRING KEKOA HOME - Case 1FDV-23-0001009
Operator: OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09
