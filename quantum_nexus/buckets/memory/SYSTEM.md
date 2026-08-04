# MEMORY BUCKET
## Memory Systems Status

### Memory Providers
| Provider | Status | Key Type | User |
|----------|--------|----------|------|
| Mem0 | ✓ Active | m0-* | OPR-NS8-GE8-KC3-001 |
| MemoryPlugin | ✓ Active | Bucket | Global bucket |
| Pinecone | ✓ Active | pcsk_* | Vector DB |
| Supermemory | ✓ Active | sm_* | Hermes |

### Mem0 Configuration
- **API Key:** m0-CkabsxFjhaYf28gYSET3JWE34k3vw6oRBP5ZUm5H
- **Org ID:** org_Gsa76AGniLIDLWGIgbmljwb7GCdPoExd3ERGKVkm
- **User ID:** OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09

### MemoryPlugin
- **Primary:** LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
- **Specialized:** yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1
- **Global Bucket:** LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9

### Pinecone
- **Primary:** pcsk_69yXbV_ScG9tJBY7Qx1e2C9dcq
- **HiGuy:** pcsk_2DjXch_JNueamvbAC937LNr1d

### Memory Operations
```python
# Store
from quantum_nexus import memory
await memory.store_legal("content", "source")

# Search
results = await memory.search("query", category="legal")

# Export
all_memories = await memory.export_all()
```

### Memory Categories
- **legal:** Case filings, precedents, constitutional analysis
- **technical:** System configs, API docs, code snippets
- **operational:** Session logs, decisions, actions
- **strategic:** Plans, tactics, recommendations
