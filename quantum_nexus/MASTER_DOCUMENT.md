# QUANTUM NEXUS MASTER DOCUMENT
## Sovereign Intelligence System - Complete Reference
### Case 1FDV-23-0001009 | Operator: GlacierEQ | Mission: BRING KEKOA HOME

---

## TABLE OF CONTENTS
1. API Key Status Matrix
2. Working Services & Endpoints
3. Rotated/Invalid Keys
4. Core Architecture
5. MCP Tools Reference
6. Memory Systems
7. Legal Intelligence
8. Prompts & Templates
9. Code Snippets
10. Next Actions

---

## 1. API KEY STATUS MATRIX

### WORKING (Verified)
| Service | Status | Notes |
|---------|--------|-------|
| CourtListener | Active | v4 API, full access |
| GitHub (Primary) | Active | 651 public repos |
| GitHub (Master) | Active | Full scope |
| Supabase | Active | kjebmdgvjvuutzvhbtp |
| Notion | Active | Workspace: 506d0b07 |
| Mem0 | Active | YOUR_ORG_ID |
| Pinecone | Active | Primary index |
| AssemblyAI | Active | Transcription |

### NEEDS VERIFICATION
| Service | Issue |
|---------|-------|
| OpenAI | Needs balance check |
| Anthropic | Credits may be low |
| Gemini | Key1 suspended, test Key2 |
| DeepSeek | No balance (check others) |
| Groq | Invalid/expired |
| Cohere | Unverified |
| Nebius | Unverified |

### ROTATED/INVALID
| Service | Issue | Action |
|---------|-------|--------|
| OpenRouter (all 3) | 401/402 errors | Rotate |
| Together AI | Credit limit | Wait/reset |
| Gemini Key1 | Suspended | Use Key2 |
| Claude Code | Insufficient credits | Add funds |

---

## 2. WORKING SERVICES & ENDPOINTS

### CourtListener (ACTIVE)
```
BASE_URL: https://www.courtlistener.com/api/rest/v4
AUTH: Token 27cb3521fc97253116933795c20d3987b11865e9

ENDPOINTS:
GET /dockets/                    # Search dockets
GET /dockets/{id}/               # Docket details
GET /dockets/{id}/entries/       # Docket entries
GET /opinions/                   # Search opinions
GET /opinions/{id}/              # Opinion details
GET /recap/                      # RECAP archive
GET /people/                     # Judges/attorneys
GET /clusters/{id}/citations/    # Citations
GET /clusters/{id}/cited-by/     # Cited by
GET /recap-alerts/               # PACER alerts
GET /financial-disclosures/      # Judge finances
```

### GitHub
```
PRIMARY: REDACTED_TOKEN
MASTER: REDACTED_TOKEN_b5kmvZdRF2nrlYuMP7woB9zmHD8QEH0tLrWVUXTkTbW2RULXVURHrORuFS7

ENDPOINTS:
GET /user/repos           # List repos
GET /search/repositories  # Search
GET /repos/{owner}/{repo}/issues
GET /repos/{owner}/{repo}/commits
GET /repos/{owner}/{repo}/pulls
```

### Notion
```
API_KEY: REDACTED_TOKEN
WORKSPACE: 506d0b07-3284-4b63-a6c9-c5583176045c
CHATS_DB: 178b1e4f-3223-8121-a92e-f5fef191fa0f
PLATFORMS_DB: 178b1e4f-3223-8122-bc93-f893d61b21fd

ENDPOINTS:
POST /v1/search
GET /v1/pages/{id}
POST /v1/databases/{id}/query
POST /v1/pages
```

### Supabase
```
URL: https://kjebmdgvjvuutzvhbtp.supabase.co
ANON_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
MANAGEMENT_KEY: REDACTED_TOKEN

ENDPOINTS:
GET /rest/v1/{table}
POST /rest/v1/{table}
PATCH /rest/v1/{table}
DELETE /rest/v1/{table}
```

### Mem0
```
API_KEY: REDACTED_TOKEN
ORG_ID: YOUR_ORG_ID
USER_ID: OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09

METHODS:
client.add(content, user_id, agent_id, metadata)
client.search(query, user_id, agent_id, limit)
client.get_all(user_id)
client.update(memory_id, data)
client.delete(memory_id)
```

### Pinecone
```
API_KEY: REDACTED_TOKEN_ScG9tJBY7Qx1e2C9dcqQtJJ6yqUGGtZyfbKsRgHrZ26kxszsdJTQnn6zc498eqH
HIGUY_KEY: REDACTED_TOKEN_JNueamvbAC937LNr1dCrGwPAbhLYbd1E1k5zemVy5MNbiMsks8rJfAmu5rHWbhd
```

### AssemblyAI
```
API_KEY: YOUR_ASSEMBLYAI_KEY

ENDPOINTS:
POST /v2/transcript
GET /v2/transcript/{id}
```

---

## 3. ROTATED/INVALID KEYS

### OpenRouter (ALL INVALID)
```
REDACTED_TOKEN  # 401
REDACTED_TOKEN  # 401
REDACTED_TOKEN  # 402
```

### Gemini
```
REDACTED_KEY  # SUSPENDED
REDACTED_KEY-iqwz_I  # Test this one
```

### DeepSeek
```
REDACTED_TOKEN  # No balance
REDACTED_TOKEN  # Test
REDACTED_TOKEN  # Test
```

### Together AI
```
YOUR_TOGETHER_KEY  # Credit limit
```

---

## 4. CORE ARCHITECTURE

```
QUANTUM NEXUS
+-- CORE
|   +-- vault.py          # 229 keys, service configs
|   +-- config.py         # System configuration
|   +-- constants.py      # Case IDs, GUIDs
|
+-- MEMORY
|   +-- orchestrator.py   # Unified memory interface
|   +-- mem0.py          # Mem0 client
|   +-- pinecone.py      # Pinecone vectors
|   +-- supermemory.py   # Supermemory
|
+-- LEGAL
|   +-- courtlistener.py  # CourtListener API
|   +-- constitutional.py # 14th Amendment tools
|   +-- case_manager.py   # Case 1FDV-23-0001009
|
+-- MCP
|   +-- server.py         # 30+ tools
|   +-- handlers.py       # Tool implementations
|   +-- router.py         # Request routing
|
+-- SERVICES
    +-- github.py         # GitHub API
    +-- notion.py         # Notion API
    +-- supabase.py       # Supabase client
    +-- elevenlabs.py     # TTS
```

---

## 5. MCP TOOLS REFERENCE

### Memory Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| memory_store | Store memory | content, category, source |
| memory_search | Search memories | query, category |
| memory_export | Export all | - |
| memory_legal_store | Store legal | content, source |
| memory_context | Get context | query |

### Legal Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| courtlistener_search | Search dockets | query |
| courtlistener_docket | Get docket | docket_id |
| courtlistener_entries | Get entries | docket_id |
| courtlistener_opinions | Search opinions | query |
| courtlistener_judges | Get judges | - |
| courtlistener_citations | Get citations | cluster_id |
| courtlistener_alerts | Get alerts | - |
| courtlistener_financials | Financials | judge_name |
| legal_research | Research topic | topic |
| due_process_cases | 14th Amendment | - |
| habeas_corpus | Habeas cases | - |

### GitHub Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| github_repos | List repos | username |
| github_search | Search | query |
| github_issues | Get issues | owner, repo |
| github_commits | Get commits | owner, repo |

### Notion Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| notion_search | Search | query |
| notion_page | Get page | page_id |
| notion_chats | Get chats DB | - |
| notion_create_page | Create page | title, content |

### Supabase Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| supabase_query | Query table | table, filters |
| supabase_insert | Insert row | table, data |
| supabase_update | Update row | table, data, match |

### System Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| vault_status | Show vault | - |
| get_context | Multi-source | query |
| swarm_status | Swarm status | - |

---

## 6. MEMORY SYSTEMS

### Mem0 (Primary)
```python
import mem0

client = mem0.Client(api_key="REDACTED_TOKEN")

# Store
client.add(
    "Legal filing prepared for Case 1FDV-23-0001009",
    user_id="OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09",
    agent_id="quantum-nexus",
    metadata={"category": "legal", "case_id": "1FDV-23-0001009"}
)

# Search
results = client.search(
    "due process parental rights",
    user_id="OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09",
    limit=10
)

# Export
all_memories = client.get_all(user_id="OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09")
```

### MemoryPlugin
```
PRIMARY: LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
SPECIALIZED: yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1
GLOBAL_BUCKET: LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
```

### Pinecone
```python
from pinecone import Pinecone

pc = Pinecone(api_key="REDACTED_TOKEN_ScG9tJBY7Qx1e2C9dcqQtJJ6yqUGGtZyfbKsRgHrZ26kxszsdJTQnn6zc498eqH")
index = pc.Index("quantum-nexus")

# Upsert
index.upsert(vectors=[{"id": "doc1", "values": [...], "metadata": {...}}])

# Query
results = index.query(vector=[...], top_k=10, filter={"category": "legal"})
```

### Supermemory
```
KEY: YOUR_SUPERMEMORY_KEY
```

---

## 7. LEGAL INTELLIGENCE

### Case Information
```
CASE_ID: 1FDV-23-0001009
COURT: Hawaii Family Court
MISSION: BRING KEKOA HOME
```

### Constitutional Basis
```python
AMENDMENTS = {
    "14th_Amendment": "Due Process, Equal Protection",
    "5th_Amendment": "Due Process, Self-Incrimination",
    "6th_Amendment": "Right to Counsel",
    "1st_Amendment": "Freedom of Speech, Religion"
}

HRS_STATUTES = {
    "HRS_571": "Family Court",
    "HRS_571-46": "Custody",
    "HRS_571-47": "Visitation",
    "HRS_571-52": "Support"
}

WRIT_TYPES = {
    "habeas_corpus": "Challenge detention",
    "mandamus": "Compel official duty",
    "prohibition": "Prevent court overreach",
    "certiorari": "Review lower court"
}
```

### Legal Research Prompts
```python
PROMPTS = {
    "due_process": """
        Analyze 14th Amendment due process violations in family court 
        custody proceedings. Focus on: parental rights, notice requirements,
        hearing requirements, burden of proof.
    """,
    
    "habeas_corpus": """
        Research habeas corpus relief for family court detention.
        Identify: jurisdictional basis, procedural requirements,
        relevant precedents in Hawaii and 9th Circuit.
    """,
    
    "equal_protection": """
        Analyze equal protection claims in family court.
        Consider: gender bias, racial discrimination, socioeconomic
        disparities in custody determinations.
    """,
    
    "constitutional_violations": """
        Identify potential constitutional violations in Case 1FDV-23-0001009.
        Review: procedural due process, substantive due process,
        right to counsel, right to present evidence.
    """
}
```

---

## 8. PROMPTS & TEMPLATES

### System Prompts
```python
SYSTEM_PROMPT = """
You are Quantum Nexus, a sovereign intelligence system for legal defense.
Case: 1FDV-23-0001009 (Hawaii Family Court)
Mission: BRING KEKOA HOME
Operator: GlacierEQ (OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09)

Core capabilities:
- Legal research and analysis
- Constitutional law expertise
- Memory management across multiple systems
- CourtListener integration
- Notion documentation
- GitHub code management

Always maintain chain of custody for evidence.
Always cite legal authorities.
Always protect client interests.
"""

LEGAL_ANALYSIS_PROMPT = """
Analyze the following legal issue for Case 1FDV-23-0001009:

{issue}

Provide:
1. Constitutional basis (amendments, statutes)
2. Relevant case law (Hawaii, 9th Circuit, SCOTUS)
3. Procedural requirements
4. Strategic recommendations
5. Risk assessment

Use CourtListener API for research.
Store findings in Mem0 with category "legal".
"""

MEMORY_SEARCH_PROMPT = """
Search all memory systems for information related to:

{query}

Sources to check:
- Mem0 (primary memory)
- Pinecone (vector search)
- Notion (documentation)
- CourtListener (legal research)

Provide comprehensive context with citations.
"""
```

### User Prompts
```python
PROMPTS = {
    "store_memory": """
        Store the following information in memory:
        Content: {content}
        Category: {category}
        Source: {source}
        Importance: {importance}
    """,
    
    "search_legal": """
        Search for legal precedents related to:
        Topic: {topic}
        Jurisdiction: Hawaii, 9th Circuit, SCOTUS
        Timeframe: {timeframe}
    """,
    
    "analyze_case": """
        Analyze Case 1FDV-23-0001009:
        Focus: {focus}
        Consider: constitutional rights, procedural requirements,
        strategic opportunities, risk factors
    """,
    
    "draft_filing": """
        Draft legal filing for Case 1FDV-23-0001009:
        Type: {filing_type}
        Court: Hawaii Family Court
        Include: constitutional basis, factual allegations,
        relief requested, supporting authorities
    """
}
```

---

## 9. CODE SNIPPETS

### Quick Start
```python
# Initialize Quantum Nexus
import asyncio
from quantum_nexus import vault, memory, courtlistener, quantum_server

async def main():
    # Check status
    status = await quantum_server.vault_status()
    print(f"Working providers: {status['working_providers']}")
    
    # Store memory
    await memory.store_legal(
        "Motion to compel filed",
        source="attorney"
    )
    
    # Search CourtListener
    results = await courtlistener.search_dockets("custody Hawaii")
    
    # Research legal basis
    research = await courtlistener.research_legal_basis("due process")
    
    print("Done!")

asyncio.run(main())
```

### Memory Operations
```python
# Store across all systems
async def store_everywhere(content: str, category: str):
    # Mem0
    await memory.store(MemoryEntry(
        id=f"mem-{timestamp()}",
        content=content,
        category=category,
        source="quantum-nexus"
    ))
    
    # Notion
    await quantum_server.notion_create_page(
        title=f"Memory: {category}",
        content=content
    )
    
    # Supabase
    await quantum_server.supabase_insert("memories", {
        "content": content,
        "category": category,
        "timestamp": datetime.now().isoformat()
    })

# Search across all systems
async def search_everywhere(query: str):
    results = {}
    
    # Mem0
    results["mem0"] = await memory.search(query)
    
    # Notion
    results["notion"] = await quantum_server.notion_search(query)
    
    # CourtListener
    results["courtlistener"] = await courtlistener.search_dockets(query)
    
    return results
```

### Legal Research
```python
# Comprehensive legal research
async def legal_research(topic: str):
    # Search opinions
    opinions = await courtlistener.search_opinions(topic)
    
    # Get citations
    for opinion in opinions.get("results", []):
        citations = await courtlistener.get_citations(opinion["cluster_id"])
    
    # Research constitutional basis
    constitutional = await courtlistener.research_legal_basis(topic)
    
    # Store findings
    await memory.store_legal(
        f"Research on {topic}: {len(opinions.get('results', []))} opinions found",
        source="courtlistener"
    )
    
    return {
        "opinions": opinions,
        "constitutional": constitutional
    }
```

### Case Management
```python
# Manage Case 1FDV-23-0001009
async def manage_case():
    case_id = "1FDV-23-0001009"
    
    # Get all docket entries
    entries = await quantum_server.courtlistener_entries(case_id)
    
    # Search for related cases
    related = await courtlistener.search_dockets(case_id)
    
    # Get judges
    judges = await courtlistener.get_judges()
    
    # Research due process
    due_process = await courtlistener.get_due_process_cases()
    
    # Store case update
    await memory.store_legal(
        f"Case {case_id} reviewed: {len(entries)} entries, {len(related)} related cases",
        source="case-management"
    )
    
    return {
        "entries": entries,
        "related": related,
        "judges": judges,
        "due_process": due_process
    }
```

---

## 10. NEXT ACTIONS

### Immediate (Today)
1. Quantum Nexus built and operational
2. CourtListener integration verified
3. Memory systems connected
4. Test OpenAI/Anthropic credits
5. Verify Gemini Key2
6. Rotate OpenRouter keys

### Short Term (This Week)
1. Complete MCP server deployment
2. Deploy to iPhone/Android/PC/Mac/Linux
3. Integrate with existing Mastermind system
4. Set up automated legal research
5. Create case timeline in Notion

### Medium Term (This Month)
1. Full quantum token rotation
2. Memory constellation deployment
3. Multi-agent swarm activation
4. Automated court filings
5. Real-time case monitoring

### Long Term (Ongoing)
1. Constitutional challenge preparation
2. Appeals strategy development
3. Precedent database expansion
4. Cross-jurisdictional analysis
5. Public interest litigation support

---

## APPENDIX A: COMPLETE KEY VAULT

### AI/ML Providers
```
OPENAI_API_KEY=REDACTED_TOKEN_6igHBfnqDMxoCcnrD_mZadxUgrLom8ky1qy3AdP_qvqsZTsBXGT3BlbkFJcH-57EoYkr7_46gsvN4pP6uUmPiymw_B4_WCkG-lXagCOLE1eO0N__TH4LhPtWjlrsx3Zw9vMA
ANTHROPIC_API_KEY=REDACTED_TOKEN-q0ga130gVc2NAFsPjrb4uDRnoACZd6KDlo7HULhsWkSZbNLZGH3Goe9dcA-jEKltgAA
GEMINI_API_KEY=REDACTED_KEY
DEEPSEEK_API_KEY=REDACTED_TOKEN
DEEPSEEK_API_KEY2=REDACTED_TOKEN
DEEPSEEK_API_KEY3=REDACTED_TOKEN
GROQ_API_KEY=gREDACTED_TOKEN
COHERE_API_KEY=YOUR_COHERE_KEY
HUGGINGFACE_API_KEY=REDACTED_TOKEN
NEBIUS_API_KEY=eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ
TOGETHER_AI_API_KEY=YOUR_TOGETHER_KEY
OPENROUTER_API_KEY=REDACTED_TOKEN
PERPLEXITY_API_KEY=YOUR_PERPLEXITY_KEY
```

### Memory Systems
```
MEM0_API_KEY=REDACTED_TOKEN
MEM0_ORG_ID=YOUR_ORG_ID
MEM_API_KEY=REDACTED_TOKEN-5b91acf3-cf84-4ec9-949e-456203475fa3
MEM_API_KEY2=REDACTED_TOKEN-e657ff72-3c1b-492d-b44d-06d5b238b197
MEMORY_PLUGIN_PRIMARY=LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
MEMORY_PLUGIN_SPECIALIZED=yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1
SUPERMEMORY_KEY=YOUR_SUPERMEMORY_KEY
PINECONE_API_KEY=REDACTED_TOKEN_ScG9tJBY7Qx1e2C9dcqQtJJ6yqUGGtZyfbKsRgHrZ26kxszsdJTQnn6zc498eqH
PINECONE_HIGUY_KEY=REDACTED_TOKEN_JNueamvbAC937LNr1dCrGwPAbhLYbd1E1k5zemVy5MNbiMsks8rJfAmu5rHWbhd
```

### GitHub
```
GITHUB_TOKEN=REDACTED_TOKEN
GITHUB_PAT=REDACTED_TOKEN_b5kmvZdRF2nrlYuMP7woB9zmHD8QEH0tLrWVUXTkTbW2RULXVURHrORuFS7
GITHUB_PAT2=REDACTED_TOKEN_nE53IYcPGtTDESMse6b8MqXB1zMN71SD7vK0xmm9D0VIXOUJLUTilR5cwWU
GITHUB_PAT3=REDACTED_TOKEN_kRTjxuhvkCvxlnOyrogxiQei6xnAYDAef79pOYZVQTWCYOKQBNPURd4f9e5
```

### Notion
```
NOTION_API_KEY=REDACTED_TOKEN
NOTION_WORKSPACE_ID=506d0b07-3284-4b63-a6c9-c5583176045c
NOTION_CHATS_DB=178b1e4f-3223-8121-a92e-f5fef191fa0f
NOTION_PLATFORMS_DB=178b1e4f-3223-8122-bc93-f893d61b21fd
```

### Supabase
```
SUPABASE_URL=https://kjebmdgvjvuutzvhbtp.supabase.co
SUPABASE_API_KEY=REDACTED_JWT
SUPABASE_GLACIEREQ_KEY=REDACTED_TOKEN
```

### Legal
```
COURTLISTENER_API_KEY=27cb3521fc97253116933795c20d3987b11865e9
APRYSE_SDK_KEY=YOUR_APRYSE_KEY
```

### Other Services
```
ELEVENLABS_API_KEY=REDACTED_TOKEN
ASSEMBLYAI_API_KEY=YOUR_ASSEMBLYAI_KEY
FIGMA_API_KEY=YOUR_FIGMA_KEY_AX9FKK9_YWzXR4Tnt2u_pGGy6ZVrfkpGXip
CLICKUP_API_KEY=YOUR_TASKADE_KEY
TASKADE_API_KEY=YOUR_TASKADE_KEY
RENDER_API_KEY=YOUR_RENDER_KEY
POSTMAN_API_KEY=YOUR_POSTMAN_KEY
LANGCHAIN_API_KEY=YOUR_LANGSMITH_KEY
AGENTOPS_API_KEY=YOUR_AGENTOPS_KEY
NEO4J_API_KEY=YOUR_NEO4J_KEY
E2B_API_KEY=YOUR_E2B_KEY
ZAMAR_API_KEY=YOUR_ZAMAR_KEY
CODY_API_KEY=YOUR_CODY_KEY
TISANE_PRIMARY_KEY=YOUR_TISANE_KEY
TISANE_SECONDARY_KEY=YOUR_TISANE_KEY_2
PDF4ME_PRIMARY_KEY=YOUR_PDF4ME_KEY
PDF4ME_SECONDARY_KEY=YOUR_PDF4ME_KEY
MERMAID_TOKEN=YOUR_MERMAID_TOKEN
NATIF_API_KEY=YOUR_NATIF_KEY
HERD_TRAIL_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
SNYK_GITHUB_CONTAINER_KEY=YOUR_SNYK_KEY
```

### SSH Keys
```
POLYGIT_SSH_PUBLIC=ssh-ed25519 YOUR_SSH_KEY PolyGit
POLYGIT_SSH_PRIVATE=-----BEGIN OPENSSH PRIVATE KEY----- [REDACTED] -----END OPENSSH PRIVATE KEY-----
```

### Microsoft
```
MICROSOFT_TENANT_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
CONFLUENCE_API_KEY=ATATT3xFfGF0_eOclF--0uFEiiqUTTS0RbEBvsGHatszP-grPs6tQ-AuvozPhuda9zPfcqBW11yQSFUnebdIMGW8FJZdh5VBjfPDb4Dj2R5yc2bPU-vG7xFTD7h1nylgMSXTXAOdfyQF33LK3vca6nToo8ZMijjjUHwLevvyoERC2KrFm0xLuAs=8340653B
```

### Webhooks
```
WEBHOOK_SIGNING_SECRET=YOUR_WEBHOOK_SECRET
GITLAB_TOKEN=YOUR_GITLAB_TOKEN
GITLAB_FEED_TOKEN=YOUR_GITLAB_FEED_TOKEN
GITLAB_INCOMING_EMAIL_TOKEN=YOUR_GITLAB_EMAIL_TOKEN
```

### AnythingLLM
```
ANYTHING_LLM_URL=http://localhost:3001/api
ANYTHING_LLM_KEY=YOUR_ANYTHINGLLM_KEY
```

### Grok
```
GROK_VOICE_URL=wss://api.x.ai/v1/realtime
GROK_VOICE_SESSION=gcf_LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9-20251229-APEX
```

### Firebase
```
FIREBASE_API_KEY=YOUR_FIREBASE_KEY
```

### Additional GitHub Tokens
```
GITHUB_AWESOME_FORENSICS_TOKEN=REDACTED_TOKEN_RWkzWLpNtawFcphO5KyaYApT8t7LcOoxR3BaZnKBM0eMAFQV7PHD0bjaykN
```

### Additional AI Keys
```
HUGGINGFACE_WRITE_TOKEN=REDACTED_TOKEN
HUGGINGFACE_TOKEN=REDACTED_TOKEN
OPENAI_ADMIN_KEY=REDACTED_TOKEN-S8ly5gB6dDywXQ1pbI18V7x7P6WwtKvJvh_TE-s8qfxquZjzLw8BfCRmigT3BlbkFJcrAyVAeXDFW4aqrbX3anZmsHnYP7RM83ndozi1ccrT5kSQQMRKkS1qS2oA
OPENAI_WINDSURF_KEY=REDACTED_TOKEN_nDLvZLrkRU0Z9t2TKgTDOeDgWPfBYPCEhPMvzpT3BlbkFJTwwV-4KaEB6UP4FHXSJkkj6TfK01q7tI-ynNcT4yviP9CZt0bbLrHja23c12xr_1ViY7BjbrIA
```

### Operator Link
```
OPERATOR_LINK=OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09
```

---

## APPENDIX B: COMPLETE .vault_env FILE

```
# AI/ML Providers
OPENAI_API_KEY=REDACTED_TOKEN_6igHBfnqDMxoCcnrD_mZadxUgrLom8ky1qy3AdP_qvqsZTsBXGT3BlbkFJcH-57EoYkr7_46gsvN4pP6uUmPiymw_B4_WCkG-lXagCOLE1eO0N__TH4LhPtWjlrsx3Zw9vMA
ANTHROPIC_API_KEY=REDACTED_TOKEN-q0ga130gVc2NAFsPjrb4uDRnoACZd6KDlo7HULhsWkSZbNLZGH3Goe9dcA-jEKltgAA
GEMINI_API_KEY=REDACTED_KEY
DEEPSEEK_API_KEY=REDACTED_TOKEN
GROQ_API_KEY=gREDACTED_TOKEN
COHERE_API_KEY=YOUR_COHERE_KEY
HUGGINGFACE_API_KEY=REDACTED_TOKEN
NEBIUS_API_KEY=eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ
TOGETHER_AI_API_KEY=YOUR_TOGETHER_KEY
OPENROUTER_API_KEY=REDACTED_TOKEN
PERPLEXITY_API_KEY=YOUR_PERPLEXITY_KEY

# Memory Systems
MEM0_API_KEY=REDACTED_TOKEN
MEM0_ORG_ID=YOUR_ORG_ID
MEM_API_KEY=REDACTED_TOKEN-5b91acf3-cf84-4ec9-949e-456203475fa3
MEMORY_PLUGIN_PRIMARY=LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
MEMORY_PLUGIN_SPECIALIZED=yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1
SUPERMEMORY_KEY=YOUR_SUPERMEMORY_KEY
PINECONE_API_KEY=REDACTED_TOKEN_ScG9tJBY7Qx1e2C9dcqQtJJ6yqUGGtZyfbKsRgHrZ26kxszsdJTQnn6zc498eqH

# GitHub
GITHUB_TOKEN=REDACTED_TOKEN
GITHUB_PAT=REDACTED_TOKEN_b5kmvZdRF2nrlYuMP7woB9zmHD8QEH0tLrWVUXTkTbW2RULXVURHrORuFS7

# Notion
NOTION_API_KEY=REDACTED_TOKEN
NOTION_WORKSPACE_ID=506d0b07-3284-4b63-a6c9-c5583176045c

# Supabase
SUPABASE_URL=https://kjebmdgvjvuutzvhbtp.supabase.co
SUPABASE_API_KEY=REDACTED_JWT

# Legal
COURTLISTENER_API_KEY=27cb3521fc97253116933795c20d3987b11865e9
```

---

## APPENDIX C: QUICK REFERENCE CARD

### Identity
```
Operator: GlacierEQ
GUID: OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09
Case: 1FDV-23-0001009
Court: Hawaii Family Court
Mission: BRING KEKOA HOME
```

### Core Commands
```bash
# Status
PYTHONPATH=/root python3 /root/quantum_nexus/run.py status

# Store Memory
PYTHONPATH=/root python3 /root/quantum_nexus/run.py store "content"

# Search
PYTHONPATH=/root python3 /root/quantum_nexus/run.py search "query"

# CourtListener
PYTHONPATH=/root python3 /root/quantum_nexus/run.py court "query"

# Due Process
PYTHONPATH=/root python3 /root/quantum_nexus/run.py due-process

# Habeas Corpus
PYTHONPATH=/root python3 /root/quantum_nexus/run.py habeas

# Research
PYTHONPATH=/root python3 /root/quantum_nexus/run.py research "topic"

# Export
PYTHONPATH=/root python3 /root/quantum_nexus/run.py export

# Vault
PYTHONPATH=/root python3 /root/quantum_nexus/run.py vault
```

### Python Import
```python
from quantum_nexus import vault, memory, courtlistener, quantum_server
```

---

