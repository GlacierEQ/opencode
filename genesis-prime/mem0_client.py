"""
MEM0 UNIFIED CLIENT
Complete Memory Integration - All Functions & Resources
Platform: m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U (Casey Pro)
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

try:
    from mem0 import MemoryClient, AsyncMemoryClient
except ImportError:
    import subprocess
    subprocess.check_call(["pip3", "install", "mem0ai"])
    from mem0 import MemoryClient, AsyncMemoryClient


class Mem0UnifiedClient:
    """
    Unified Mem0 client with all advanced features.
    Supports: Platform API, Graph Memory, Batch Ops, Async, Metadata filtering.
    """
    
    # Platform endpoints
    PRO_API_KEY = "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U"
    REGULAR_API_KEY = "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj"
    
    # User identifiers
    PRO_USER = "casey@hi-classhomeservices.com"
    REGULAR_USER = "higuy.vids@gmail.com"
    
    # Bucket identifiers
    GLOBAL_BUCKET = "LFVBLPUL3N8N8K2FLYGCSCKMSMSRHSG9"
    DIRECT_BUCKET = "yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1"
    
    def __init__(self, tier: str = "pro", async_mode: bool = False):
        """
        Initialize Mem0 client.
        
        Args:
            tier: "pro" or "regular"
            async_mode: Use async client for non-blocking operations
        """
        self.tier = tier
        self.api_key = self.PRO_API_KEY if tier == "pro" else self.REGULAR_API_KEY
        self.user_id = self.PRO_USER if tier == "pro" else self.REGULAR_USER
        self.bucket = self.GLOBAL_BUCKET if tier == "pro" else self.DIRECT_BUCKET
        
        if async_mode:
            self.client = AsyncMemoryClient(api_key=self.api_key)
        else:
            self.client = MemoryClient(api_key=self.api_key)
        
        self.async_mode = async_mode
    
    # ==================== CORE MEMORY OPERATIONS ====================
    
    def add_memory(
        self,
        messages: List[Dict[str, str]],
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        app_id: Optional[str] = None,
        run_id: Optional[str] = None,
        infer: bool = True,
        output_format: str = "v1.1",
        immutable: bool = False,
        expiration_date: Optional[str] = None,
        custom_categories: Optional[Dict[str, str]] = None,
        custom_instructions: Optional[str] = None,
        includes: Optional[str] = None,
        excludes: Optional[str] = None,
        version: str = "v2"
    ) -> Dict[str, Any]:
        """
        Add memories with full parameter control.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            metadata: Additional metadata (location, time, case info, etc.)
            user_id: User identifier (defaults to initialized user)
            agent_id: Agent identifier for multi-agent systems
            app_id: Application identifier
            run_id: Run/session identifier
            infer: Whether to infer memories from messages
            output_format: "v1.1" recommended
            immutable: Whether memory can be updated
            expiration_date: Expiration in "YYYY-MM-DD" format
            custom_categories: Custom category definitions
            custom_instructions: Project-specific guidelines
            includes: Specific preferences to include
            excludes: Specific preferences to exclude
            version: API version ("v2" recommended)
        
        Returns:
            API response with memory ID and status
        """
        params = {
            "messages": messages,
            "infer": infer,
            "output_format": output_format,
            "immutable": immutable,
            "version": version
        }
        
        # Add optional parameters
        if metadata:
            params["metadata"] = metadata
        if user_id or self.user_id:
            params["user_id"] = user_id or self.user_id
        if agent_id:
            params["agent_id"] = agent_id
        if app_id:
            params["app_id"] = app_id
        if run_id:
            params["run_id"] = run_id
        if expiration_date:
            params["expiration_date"] = expiration_date
        if custom_categories:
            params["custom_categories"] = custom_categories
        if custom_instructions:
            params["custom_instructions"] = custom_instructions
        if includes:
            params["includes"] = includes
        if excludes:
            params["excludes"] = excludes
        
        return self.client.add(**params)
    
    def search_memories(
        self,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        app_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        threshold: float = 0.0,
        version: str = "v2"
    ) -> Dict[str, Any]:
        """
        Search memories with advanced filtering.
        
        Args:
            query: Search query text
            user_id: Filter by user
            agent_id: Filter by agent
            app_id: Filter by app
            run_id: Filter by run
            metadata_filter: Metadata filtering (supports AND/OR/NOT)
            limit: Max results to return
            threshold: Minimum similarity score (0.0-1.0)
            version: API version
        
        Returns:
            Search results with relevance scores
        """
        params = {
            "query": query,
            "limit": limit,
            "threshold": threshold,
            "version": version
        }
        
        if user_id or self.user_id:
            params["user_id"] = user_id or self.user_id
        if agent_id:
            params["agent_id"] = agent_id
        if app_id:
            params["app_id"] = app_id
        if run_id:
            params["run_id"] = run_id
        if metadata_filter:
            params["metadata"] = metadata_filter
        
        return self.client.search(**params)
    
    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """Get a specific memory by ID."""
        return self.client.get(memory_id)
    
    def get_all_memories(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get all memories for a user/agent."""
        params = {"limit": limit}
        if user_id or self.user_id:
            params["user_id"] = user_id or self.user_id
        if agent_id:
            params["agent_id"] = agent_id
        return self.client.get_all(**params)
    
    def update_memory(
        self,
        memory_id: str,
        messages: List[Dict[str, str]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update an existing memory."""
        params = {"messages": messages}
        if metadata:
            params["metadata"] = metadata
        return self.client.update(memory_id, **params)
    
    def delete_memory(self, memory_id: str) -> Dict[str, Any]:
        """Delete a specific memory."""
        return self.client.delete(memory_id)
    
    def delete_all_memories(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Delete all memories for a user/agent."""
        params = {}
        if user_id or self.user_id:
            params["user_id"] = user_id or self.user_id
        if agent_id:
            params["agent_id"] = agent_id
        return self.client.delete_all(**params)
    
    def export_memories(self, output_format: str = "json") -> Any:
        """Export all memories in specified format."""
        return self.client.export(output_format=output_format)
    
    def get_memory_history(self, memory_id: str) -> Dict[str, Any]:
        """Get history of changes for a memory."""
        return self.client.history(memory_id)
    
    # ==================== BATCH OPERATIONS ====================
    
    def batch_add(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple memories in batch (up to 1000).
        
        Args:
            batch: List of memory dicts with messages, metadata, etc.
        """
        return self.client.batch.add(batch)
    
    def batch_update(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update multiple memories in batch.
        
        Args:
            batch: List of dicts with id and messages
        """
        return self.client.batch.update(batch)
    
    def batch_delete(self, memory_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple memories by IDs.
        
        Args:
            memory_ids: List of memory IDs to delete
        """
        return self.client.batch.delete(memory_ids)
    
    # ==================== FEEDBACK ====================
    
    def add_feedback(
        self,
        memory_id: str,
        feedback: str,
        score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Add feedback for memory quality.
        
        Args:
            memory_id: Memory to provide feedback for
            feedback: "positive" or "negative"
            score: Optional numeric score
        """
        return self.client.feedback(memory_id=memory_id, feedback=feedback, score=score)
    
    # ==================== ASYNC OPERATIONS ====================
    
    async def async_add_memory(self, **kwargs) -> Dict[str, Any]:
        """Async version of add_memory."""
        return await self.client.add(**kwargs)
    
    async def async_search(self, **kwargs) -> Dict[str, Any]:
        """Async version of search."""
        return await self.client.search(**kwargs)
    
    async def async_get_all(self, **kwargs) -> Dict[str, Any]:
        """Async version of get_all."""
        return await self.client.get_all(**kwargs)
    
    # ==================== CASE-SPECIFIC METHODS ====================
    
    def store_legal_document(
        self,
        document_name: str,
        content: str,
        case_id: str = "1FDV-23-0001009",
        doc_type: str = "motion",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store a legal document in memory with case metadata.
        
        Args:
            document_name: Name of the document
            content: Document content or summary
            case_id: Case number
            doc_type: Document type (motion, order, evidence, etc.)
            additional metadata
        """
        base_metadata = {
            "case_id": case_id,
            "document_type": doc_type,
            "source": "courtlistener",
            "timestamp": datetime.utcnow().isoformat(),
            "resonance": 0.95
        }
        if metadata:
            base_metadata.update(metadata)
        
        return self.add_memory(
            messages=[
                {"role": "user", "content": f"Document: {document_name}"},
                {"role": "assistant", "content": content}
            ],
            metadata=base_metadata
        )
    
    def search_case_documents(
        self,
        query: str,
        case_id: str = "1FDV-23-0001009",
        doc_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search documents for a specific case.
        
        Args:
            query: Search query
            case_id: Case number filter
            doc_type: Optional document type filter
        """
        metadata_filter = {"case_id": case_id}
        if doc_type:
            metadata_filter["document_type"] = doc_type
        
        return self.search_memories(query=query, metadata_filter=metadata_filter)
    
    def store_forensic_evidence(
        self,
        evidence_name: str,
        description: str,
        hash_sha256: str,
        hash_blake2b: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store forensic evidence with hash chain.
        
        Args:
            evidence_name: Name of evidence
            description: Description
            hash_sha256: SHA-256 hash
            hash_blake2b: Blake2b hash
            source: Evidence source
        """
        evidence_metadata = {
            "type": "forensic_evidence",
            "hash_sha256": hash_sha256,
            "hash_blake2b": hash_blake2b,
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "admissible": True,
            "federal_rule": "FRE 902(13)"
        }
        if metadata:
            evidence_metadata.update(metadata)
        
        return self.add_memory(
            messages=[
                {"role": "user", "content": f"Evidence: {evidence_name}"},
                {"role": "assistant", "content": description}
            ],
            metadata=evidence_metadata
        )


# ==================== STANDALONE USAGE ====================

if __name__ == "__main__":
    print("=" * 70)
    print("  MEM0 UNIFIED CLIENT - Complete Memory Integration")
    print("  Platform: Pro Account (casey@hi-classhomeservices.com)")
    print("=" * 70)
    
    # Initialize client
    mem = Mem0UnifiedClient(tier="pro")
    
    # Test connection
    try:
        result = mem.search_memories(query="test", limit=1)
        print("\n[OK] Connected to Mem0 Platform")
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
    
    # Example: Store a legal document
    print("\n--- Example: Store Legal Document ---")
    try:
        result = mem.store_legal_document(
            document_name="Motion to Compel Discovery",
            content="Plaintiff moves this Court to compel Defendant to respond to discovery requests served on...",
            doc_type="motion",
            metadata={"federal_vector": "42 USC §1983", "judge": "Judge Smith"}
        )
        print(f"Stored: {result.get('id', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example: Search case documents
    print("\n--- Example: Search Case Documents ---")
    try:
        results = mem.search_case_documents(query="custody order")
        print(f"Found: {len(results.get('results', []))} documents")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example: Batch add
    print("\n--- Example: Batch Add ---")
    try:
        batch = [
            {
                "messages": [{"role": "user", "content": f"Memory {i}"}],
                "metadata": {"batch": True, "index": i}
            }
            for i in range(3)
        ]
        result = mem.batch_add(batch)
        print(f"Batch added: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("  Ready for production use")
    print("=" * 70)
