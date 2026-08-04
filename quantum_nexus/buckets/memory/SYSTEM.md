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
- **API Key:** [REDACTED - see .vault_env]
- **Org ID:** [REDACTED - see .vault_env]
- **User ID:** [REDACTED - see .vault_env]

### MemoryPlugin
- **Primary:** [REDACTED - see .vault_env]
- **Specialized:** [REDACTED - see .vault_env]
- **Global Bucket:** [REDACTED - see .vault_env]

### Pinecone
- **Primary:** [REDACTED - see .vault_env]
- **HiGuy:** [REDACTED - see .vault_env]

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
