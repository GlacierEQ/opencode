"""
MEM0 UNIFIED CLIENT - COMPLETE INTEGRATION
All Functions, Resources, and Advanced Features
Platform: Pro (m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U)
          Regular (m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj)
MemoryPlugin: LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
"""

import os
import json
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call(["pip3", "install", "requests"])
    import requests


class Mem0PlatformClient:
    """
    Mem0 Platform API Client - Complete Implementation
    Covers: Add, Search, Get, Update, Delete, Export, History, Feedback
    Supports: Batch, Async, Graph Memory, Metadata Filtering
    """
    
    BASE_URL = "https://api.mem0.ai/v1"
    
    # Account Configuration
    PRO_API_KEY = "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U"
    REGULAR_API_KEY = "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj"
    PRO_USER_ID = "casey@hi-classhomeservices.com"
    REGULAR_USER_ID = "higuy.vids@gmail.com"
    
    # Bucket IDs
    GLOBAL_BUCKET = "LFVBLPUL3N8N8K2FLYGCSCKMSMSRHSG9"
    DIRECT_BUCKET = "yD4IKCdlI0VCXlfD4xLT1x5D0dEU9Hd1"
    
    # Organization
    ORG_ID = "org_Gsa76AGniLIDLWGIgbmljwb7GCdPoExd3ERGKVkm"
    ORG_NAME = "hi_guy-default-org"
    
    def __init__(self, tier: str = "pro"):
        self.api_key = self.PRO_API_KEY if tier == "pro" else self.REGULAR_API_KEY
        self.user_id = self.PRO_USER_ID if tier == "pro" else self.REGULAR_USER_ID
        self.tier = tier
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Mem0 API."""
        url = f"{self.BASE_URL}/{endpoint}/"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()
    
    # ==================== MEMORY OPERATIONS ====================
    
    def add_memory(
        self,
        messages: List[Dict[str, str]],
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        app_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        infer: bool = True,
        output_format: str = "v1.1",
        immutable: bool = False,
        async_mode: bool = False,
        timestamp: Optional[int] = None,
        expiration_date: Optional[str] = None,
        custom_categories: Optional[Dict[str, str]] = None,
        custom_instructions: Optional[str] = None,
        includes: Optional[str] = None,
        excludes: Optional[str] = None,
        version: str = "v2"
    ) -> Dict[str, Any]:
        """
        Add memories to Mem0 platform.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            user_id: User identifier (defaults to initialized user)
            agent_id: Agent identifier for multi-agent systems
            app_id: Application identifier
            run_id: Run/session identifier
            metadata: Additional metadata (case_id, source, etc.)
            infer: Whether to infer memories from messages
            output_format: "v1.1" recommended
            immutable: Whether memory can be updated
            async_mode: Non-blocking operation
            timestamp: Unix timestamp
            expiration_date: Format "YYYY-MM-DD"
            custom_categories: Custom category definitions
            custom_instructions: Project-specific guidelines
            includes: Specific preferences to include
            excludes: Specific preferences to exclude
            version: API version ("v2" recommended)
        
        Returns:
            API response with memory ID and status
        """
        payload = {
            "messages": messages,
            "infer": infer,
            "output_format": output_format,
            "immutable": immutable,
            "async_mode": async_mode,
            "version": version
        }
        
        # Add optional parameters
        if user_id or self.user_id:
            payload["user_id"] = user_id or self.user_id
        if agent_id:
            payload["agent_id"] = agent_id
        if app_id:
            payload["app_id"] = app_id
        if run_id:
            payload["run_id"] = run_id
        if metadata:
            payload["metadata"] = metadata
        if timestamp:
            payload["timestamp"] = timestamp
        if expiration_date:
            payload["expiration_date"] = expiration_date
        if custom_categories:
            payload["custom_categories"] = custom_categories
        if custom_instructions:
            payload["custom_instructions"] = custom_instructions
        if includes:
            payload["includes"] = includes
        if excludes:
            payload["excludes"] = excludes
        
        return self._request("POST", "memories", json=payload)
    
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
        payload = {
            "query": query,
            "limit": limit,
            "threshold": threshold,
            "version": version
        }
        
        if user_id or self.user_id:
            payload["user_id"] = user_id or self.user_id
        if agent_id:
            payload["agent_id"] = agent_id
        if app_id:
            payload["app_id"] = app_id
        if run_id:
            payload["run_id"] = run_id
        if metadata_filter:
            payload["metadata"] = metadata_filter
        
        return self._request("POST", "memories/search", json=payload)
    
    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """Get a specific memory by ID."""
        return self._request("GET", f"memories/{memory_id}")
    
    def get_all_memories(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        app_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """Get all memories with pagination."""
        params = {"page": page, "page_size": page_size}
        if user_id or self.user_id:
            params["user_id"] = user_id or self.user_id
        if agent_id:
            params["agent_id"] = agent_id
        if app_id:
            params["app_id"] = app_id
        return self._request("GET", "memories", params=params)
    
    def update_memory(
        self,
        memory_id: str,
        messages: List[Dict[str, str]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update an existing memory."""
        payload = {"messages": messages}
        if metadata:
            payload["metadata"] = metadata
        return self._request("PUT", f"memories/{memory_id}", json=payload)
    
    def batch_update(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Batch update multiple memories.
        
        Args:
            updates: List of dicts with 'id' and 'messages'
        """
        return self._request("PUT", "memories/batch", json={"updates": updates})
    
    def delete_memory(self, memory_id: str) -> Dict[str, Any]:
        """Delete a specific memory."""
        return self._request("DELETE", f"memories/{memory_id}")
    
    def batch_delete(self, memory_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple memories by IDs."""
        return self._request("DELETE", "memories/batch", json={"ids": memory_ids})
    
    def delete_all_memories(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Delete all memories for a user/agent."""
        payload = {}
        if user_id or self.user_id:
            payload["user_id"] = user_id or self.user_id
        if agent_id:
            payload["agent_id"] = agent_id
        return self._request("DELETE", "memories", json=payload)
    
    def get_memory_history(self, memory_id: str) -> Dict[str, Any]:
        """Get history of changes for a memory."""
        return self._request("GET", f"memories/{memory_id}/history")
    
    def export_memories(self, output_format: str = "json") -> Any:
        """Export all memories in specified format."""
        return self._request("POST", "memories/export", json={"format": output_format})
    
    def create_memory_export(self, **params) -> Dict[str, Any]:
        """Create a memory export job."""
        return self._request("POST", "memories/export", json=params)
    
    def get_memory_export(self, export_id: str) -> Dict[str, Any]:
        """Get status of memory export."""
        return self._request("GET", f"memories/export/{export_id}")
    
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
        payload = {"memory_id": memory_id, "feedback": feedback}
        if score is not None:
            payload["score"] = score
        return self._request("POST", "memories/feedback", json=payload)
    
    # ==================== BATCH OPERATIONS ====================
    
    def batch_add(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple memories in batch (up to 1000).
        
        Args:
            batch: List of memory dicts with messages, metadata, etc.
        """
        return self._request("POST", "memories/batch", json={"memories": batch})
    
    # ==================== ORGANIZATION & PROJECT ====================
    
    def list_organization_projects(self) -> Dict[str, Any]:
        """List all projects in organization."""
        return self._request("GET", f"organizations/{self.ORG_ID}/projects")
    
    def get_organization_members(self) -> Dict[str, Any]:
        """Get organization members."""
        return self._request("GET", f"organizations/{self.ORG_ID}/members")


class MemoryPluginClient:
    """
    MemoryPlugin MCP Server Client
    Token: LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9
    """
    
    API_URL = "https://www.memoryplugin.com/api/v2/memory"
    TOKEN = "LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or self.TOKEN
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    
    def store_memory(
        self,
        text: str,
        bucket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Store a new memory.
        
        Args:
            text: Memory content
            bucket_id: Optional bucket to store in
        """
        payload = {"text": text}
        if bucket_id:
            payload["bucketId"] = bucket_id
        
        response = requests.post(
            f"{self.API_URL}?client=python&v=2",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_memories(
        self,
        query: Optional[str] = None,
        latest: bool = False,
        count: int = 50,
        bucket_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Query memories with filters.
        
        Args:
            query: Search query
            latest: Get latest memories
            count: Number of memories to return
            bucket_id: Filter by bucket
        """
        params = {"client": "python", "v": "2"}
        if query:
            params["query"] = query
        if latest:
            params["latest"] = "true"
        if bucket_id:
            params["bucketId"] = bucket_id
        
        response = requests.get(
            self.API_URL,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """List all memory buckets with counts."""
        response = requests.get(
            f"{self.API_URL}/buckets",
            headers=self.headers,
            params={"client": "python", "v": "2"}
        )
        response.raise_for_status()
        return response.json()
    
    def create_bucket(self, name: str) -> Dict[str, Any]:
        """
        Create a new memory bucket.
        
        Args:
            name: Bucket name
        """
        response = requests.post(
            f"{self.API_URL}/buckets",
            headers=self.headers,
            json={"name": name},
            params={"client": "python", "v": "2"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_memories_and_buckets(
        self,
        query: Optional[str] = None,
        count: int = 50
    ) -> Dict[str, Any]:
        """
        Combined query for memories and buckets.
        
        Args:
            query: Search query
            count: Number of results
        """
        params = {"client": "python", "v": "2", "count": count}
        if query:
            params["query"] = query
        
        response = requests.get(
            f"{self.API_URL}/combined",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()


class UnifiedMemorySystem:
    """
    Unified Memory System combining Mem0 Platform + MemoryPlugin
    Provides single interface for all memory operations
    """
    
    def __init__(self, tier: str = "pro"):
        """
        Initialize unified memory system.
        
        Args:
            tier: "pro" or "regular" for Mem0 accounts
        """
        self.mem0 = Mem0PlatformClient(tier=tier)
        self.memory_plugin = MemoryPluginClient()
        self.tier = tier
    
    # ==================== UNIFIED OPERATIONS ====================
    
    def store(
        self,
        content: str,
        source: str = "direct",
        metadata: Optional[Dict[str, Any]] = None,
        bucket_id: Optional[str] = None,
        sync_to_plugin: bool = True
    ) -> Dict[str, Any]:
        """
        Store memory in both systems.
        
        Args:
            content: Memory content
            source: Source identifier
            metadata: Additional metadata
            bucket_id: MemoryPlugin bucket
            sync_to_plugin: Also store in MemoryPlugin
        """
        results = {"mem0": None, "memory_plugin": None}
        
        # Store in Mem0
        base_metadata = {
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "synced": True
        }
        if metadata:
            base_metadata.update(metadata)
        
        mem0_result = self.mem0.add_memory(
            messages=[{"role": "user", "content": content}],
            metadata=base_metadata
        )
        results["mem0"] = mem0_result
        
        # Store in MemoryPlugin
        if sync_to_plugin:
            plugin_result = self.memory_plugin.store_memory(
                text=content,
                bucket_id=bucket_id
            )
            results["memory_plugin"] = plugin_result
        
        return results
    
    def search(
        self,
        query: str,
        limit: int = 10,
        source: Optional[str] = None,
        search_plugin: bool = True
    ) -> Dict[str, Any]:
        """
        Search memories across both systems.
        
        Args:
            query: Search query
            limit: Max results
            source: Filter by source
            search_plugin: Also search MemoryPlugin
        """
        results = {"mem0": [], "memory_plugin": []}
        
        # Search Mem0
        metadata_filter = {}
        if source:
            metadata_filter["source"] = source
        
        mem0_results = self.mem0.search_memories(
            query=query,
            limit=limit,
            metadata_filter=metadata_filter if metadata_filter else None
        )
        results["mem0"] = mem0_results.get("results", [])
        
        # Search MemoryPlugin
        if search_plugin:
            plugin_results = self.memory_plugin.get_memories(query=query, count=limit)
            results["memory_plugin"] = plugin_results
        
        return results
    
    def store_legal_document(
        self,
        document_name: str,
        content: str,
        case_id: str = "1FDV-23-0001009",
        doc_type: str = "motion",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Store a legal document with case metadata.
        
        Args:
            document_name: Name of the document
            content: Document content or summary
            case_id: Case number
            doc_type: Document type (motion, order, evidence, etc.)
        """
        doc_metadata = {
            "case_id": case_id,
            "document_type": doc_type,
            "source": "courtlistener",
            "timestamp": datetime.utcnow().isoformat(),
            "resonance": 0.95,
            "federal_vector": "42 USC §1983"
        }
        if metadata:
            doc_metadata.update(metadata)
        
        return self.store(
            content=f"Document: {document_name}\n\n{content}",
            source="courtlistener",
            metadata=doc_metadata
        )
    
    def store_forensic_evidence(
        self,
        evidence_name: str,
        description: str,
        hash_sha256: str,
        hash_blake2b: str,
        source: str
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
        
        return self.store(
            content=f"Evidence: {evidence_name}\n\n{description}",
            source="forensic",
            metadata=evidence_metadata
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
        
        return self.mem0.search_memories(
            query=query,
            metadata_filter=metadata_filter
        )
    
    def generate_evidence_hash(self, data: Any) -> Dict[str, str]:
        """Generate forensic hash for evidence integrity."""
        serialized = json.dumps(data, sort_keys=True).encode()
        return {
            "sha256": hashlib.sha256(serialized).hexdigest(),
            "blake2b": hashlib.blake2b(serialized).hexdigest(),
            "timestamp": datetime.utcnow().isoformat()
        }


# ==================== STANDALONE USAGE ====================

if __name__ == "__main__":
    print("=" * 70)
    print("  MEM0 UNIFIED MEMORY SYSTEM")
    print("  Complete Integration - All Functions & Resources")
    print("=" * 70)
    
    # Initialize unified system
    mem = UnifiedMemorySystem(tier="pro")
    
    # Test Mem0 connection
    print("\n--- Testing Mem0 Platform ---")
    try:
        result = mem.mem0.search_memories(query="test", limit=1)
        print("[OK] Mem0 Platform connected")
    except Exception as e:
        print(f"[ERROR] Mem0 connection failed: {e}")
    
    # Test MemoryPlugin connection
    print("\n--- Testing MemoryPlugin ---")
    try:
        buckets = mem.memory_plugin.list_buckets()
        print(f"[OK] MemoryPlugin connected - {len(buckets)} buckets")
    except Exception as e:
        print(f"[ERROR] MemoryPlugin connection failed: {e}")
    
    # Example: Store a memory
    print("\n--- Example: Store Memory ---")
    try:
        result = mem.store(
            content="Test memory from unified system",
            source="test",
            metadata={"test": True}
        )
        print(f"Stored: {result['mem0'].get('id', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example: Search memories
    print("\n--- Example: Search Memories ---")
    try:
        results = mem.search(query="test", limit=5)
        print(f"Found: {len(results['mem0'])} in Mem0")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example: Store legal document
    print("\n--- Example: Store Legal Document ---")
    try:
        result = mem.store_legal_document(
            document_name="Motion to Compel",
            content="Plaintiff moves this Court to compel...",
            doc_type="motion"
        )
        print(f"Stored legal document: {result['mem0'].get('id', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("  Ready for production use")
    print("  Mem0 API Key: m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U")
    print("  MemoryPlugin Token: LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9")
    print("=" * 70)
