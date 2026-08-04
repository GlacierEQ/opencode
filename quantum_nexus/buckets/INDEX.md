# BUCKETS INDEX
## Specialized Memory Buckets

### Bucket Structure
```
quantum_nexus/buckets/
├── identity/PROFILE.md    # Operator identity, accounts, mission
├── legal/CASE.md          # Case 1FDV-23-0001009, laws, writs
├── technical/SYSTEM.md    # Architecture, tools, APIs
├── memory/SYSTEM.md       # Mem0, Pinecone, Supermemory
├── services/ENDPOINTS.md  # External services, API keys
└── cloud/STATUS.md        # Cloud storage status
```

### Usage
```python
# Load specific bucket
with open("buckets/identity/PROFILE.md") as f:
    profile = f.read()

# Search across buckets
import glob
for bucket in glob.glob("buckets/**/*.md"):
    # Search contents
    pass
```

### Maintenance
- Update `identity/PROFILE.md` when accounts change
- Update `legal/CASE.md` when case status changes
- Update `technical/SYSTEM.md` when tools update
- Update `memory/SYSTEM.md` when providers change
- Update `services/ENDPOINTS.md` when API keys rotate
- Update `cloud/STATUS.md` when storage status changes

### Distilled Memory Rules
1. **Identity:** Who am I, what's my mission
2. **Legal:** What's the case, what laws apply
3. **Technical:** What tools do I have, how do they work
4. **Memory:** Where is knowledge stored, how to retrieve
5. **Services:** What external systems are connected
6. **Cloud:** Where are files stored, what's the status
