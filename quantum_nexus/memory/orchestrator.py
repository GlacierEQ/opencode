import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict

from ..core.vault import vault

@dataclass
class MemoryEntry:
    """Universal memory format"""
    id: str
    content: str
    category: str  # legal, technical, operational, strategic
    source: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

class MemoryOrchestrator:
    """Unified interface for all memory systems"""
    
    def __init__(self):
        self.vault = vault
        self._initialized = False
    
    async def initialize(self):
        """Initialize all memory providers"""
        if self._initialized:
            return
        
        # Initialize Mem0
        try:
            import mem0
            self.mem0 = mem0.Client(api_key=self.vault.MEM0_API_KEY)
        except:
            self.mem0 = None
        
        self._initialized = True
    
    async def store(self, entry: MemoryEntry) -> Dict[str, Any]:
        """Store memory across all configured providers"""
        results = {}
        
        # Mem0 (primary)
        if self.mem0:
            try:
                result = self.mem0.add(
                    entry.content,
                    user_id=self.vault.OPERATOR_GUID,
                    agent_id="quantum-nexus",
                    metadata={
                        "category": entry.category,
                        "source": entry.source,
                        "case_id": self.vault.CASE_ID,
                        "importance": entry.importance
                    }
                )
                results["mem0"] = {"status": "success", "id": result.get("id")}
            except Exception as e:
                results["mem0"] = {"status": "error", "error": str(e)}
        
        # Pinecone (if configured)
        if self.vault.PINECONE_API_KEY:
            try:
                results["pinecone"] = await self._store_pinecone(entry)
            except Exception as e:
                results["pinecone"] = {"status": "error", "error": str(e)}
        
        return results
    
    async def search(self, query: str, category: Optional[str] = None, limit: int = 10) -> Dict[str, List[Dict]]:
        """Search across all memory providers"""
        results = {}
        
        # Mem0 search
        if self.mem0:
            try:
                filters = {}
                if category:
                    filters["category"] = category
                
                mem0_results = self.mem0.search(
                    query,
                    user_id=self.vault.OPERATOR_GUID,
                    agent_id="quantum-nexus",
                    filters=filters if filters else None,
                    limit=limit
                )
                results["mem0"] = mem0_results
            except Exception as e:
                results["mem0"] = {"error": str(e)}
        
        return results
    
    async def _store_pinecone(self, entry: MemoryEntry) -> Dict:
        """Store in Pinecone vector database"""
        # Simplified - full implementation would use embeddings
        return {"status": "pending", "note": "Requires embedding service"}
    
    async def store_legal(self, content: str, source: str, **kwargs) -> Dict:
        """Store legal memory"""
        entry = MemoryEntry(
            id=f"legal-{datetime.now().timestamp()}",
            content=content,
            category="legal",
            source=source,
            tags=kwargs.get("tags", ["courtlistener", "case-law"]),
            importance=kwargs.get("importance", 0.8),
            metadata={"case_id": self.vault.CASE_ID}
        )
        return await self.store(entry)
    
    async def store_technical(self, content: str, source: str, **kwargs) -> Dict:
        """Store technical memory"""
        entry = MemoryEntry(
            id=f"tech-{datetime.now().timestamp()}",
            content=content,
            category="technical",
            source=source,
            tags=kwargs.get("tags", ["architecture", "code"]),
            importance=kwargs.get("importance", 0.6)
        )
        return await self.store(entry)
    
    async def get_context(self, query: str) -> Dict[str, Any]:
        """Get multi-source context for a query"""
        search_results = await self.search(query, limit=5)
        
        context = {
            "query": query,
            "memories": search_results.get("mem0", []),
            "sources": list(search_results.keys()),
            "timestamp": datetime.now().isoformat()
        }
        
        return context
    
    async def export_all(self) -> Dict[str, Any]:
        """Export all memories"""
        if self.mem0:
            try:
                all_memories = self.mem0.get_all(user_id=self.vault.OPERATOR_GUID)
                return {
                    "mem0": all_memories,
                    "count": len(all_memories),
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                return {"error": str(e)}
        return {"error": "No memory providers configured"}

# Global instance
memory = MemoryOrchestrator()
