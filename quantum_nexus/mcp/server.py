"""
Quantum Nexus MCP Server - Unified Tool Interface
30+ tools for sovereign operation across all integrated services
"""
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core.vault import vault
from ..memory.orchestrator import memory
from ..legal.courtlistener import courtlistener

class QuantumNexusMCPServer:
    """Unified MCP server with all tools"""
    
    def __init__(self):
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Any]:
        """Register all available tools"""
        return {
            # === MEMORY TOOLS ===
            "memory_store": self.memory_store,
            "memory_search": self.memory_search,
            "memory_export": self.memory_export,
            "memory_legal_store": self.memory_legal_store,
            "memory_context": self.memory_context,
            
            # === LEGAL TOOLS ===
            "courtlistener_search": self.courtlistener_search,
            "courtlistener_docket": self.courtlistener_docket,
            "courtlistener_entries": self.courtlistener_entries,
            "courtlistener_opinions": self.courtlistener_opinions,
            "courtlistener_judges": self.courtlistener_judges,
            "courtlistener_citations": self.courtlistener_citations,
            "courtlistener_alerts": self.courtlistener_alerts,
            "courtlistener_financials": self.courtlistener_financials,
            "legal_research": self.legal_research,
            "due_process_cases": self.due_process_cases,
            "habeas_corpus": self.habeas_corpus,
            
            # === GITHUB TOOLS ===
            "github_repos": self.github_repos,
            "github_search": self.github_search,
            "github_issues": self.github_issues,
            "github_commits": self.github_commits,
            
            # === NOTION TOOLS ===
            "notion_search": self.notion_search,
            "notion_page": self.notion_page,
            "notion_chats": self.notion_chats,
            "notion_create_page": self.notion_create_page,
            
            # === SUPABASE TOOLS ===
            "supabase_query": self.supabase_query,
            "supabase_insert": self.supabase_insert,
            "supabase_update": self.supabase_update,
            
            # === SERVICE TOOLS ===
            "clickup_tasks": self.clickup_tasks,
            "taskade_workspaces": self.taskade_workspaces,
            "elevenlabs_tts": self.elevenlabs_tts,
            "assemblyai_transcribe": self.assemblyai_transcribe,
            
            # === SYSTEM TOOLS ===
            "vault_status": self.vault_status,
            "get_context": self.get_context,
            "swarm_status": self.swarm_status,
        }
    
    # === MEMORY TOOLS ===
    async def memory_store(self, content: str, category: str = "general", source: str = "mcp") -> Dict:
        """Store a memory"""
        from .memory.orchestrator import MemoryEntry
        entry = MemoryEntry(
            id=f"mcp-{datetime.now().timestamp()}",
            content=content,
            category=category,
            source=source
        )
        return await memory.store(entry)
    
    async def memory_search(self, query: str, category: Optional[str] = None) -> Dict:
        """Search memories"""
        return await memory.search(query, category=category)
    
    async def memory_export(self) -> Dict:
        """Export all memories"""
        return await memory.export_all()
    
    async def memory_legal_store(self, content: str, source: str) -> Dict:
        """Store legal memory"""
        return await memory.store_legal(content, source)
    
    async def memory_context(self, query: str) -> Dict:
        """Get context for a query"""
        return await memory.get_context(query)
    
    # === LEGAL TOOLS ===
    async def courtlistener_search(self, query: str) -> Dict:
        """Search CourtListener"""
        return await courtlistener.search_dockets(query)
    
    async def courtlistener_docket(self, docket_id: int) -> Dict:
        """Get docket details"""
        return await courtlistener.get_docket(docket_id)
    
    async def courtlistener_entries(self, docket_id: int) -> Dict:
        """Get docket entries"""
        return await courtlistener.get_docket_entries(docket_id)
    
    async def courtlistener_opinions(self, query: str) -> Dict:
        """Search opinions"""
        return await courtlistener.search_opinions(query)
    
    async def courtlistener_judges(self) -> Dict:
        """Get judges"""
        judges = await courtlistener.get_judges()
        return {"judges": judges}
    
    async def courtlistener_citations(self, cluster_id: int) -> Dict:
        """Get citations"""
        return await courtlistener.get_citations(cluster_id)
    
    async def courtlistener_alerts(self) -> Dict:
        """Get alerts"""
        alerts = await courtlistener.get_alerts()
        return {"alerts": alerts}
    
    async def courtlistener_financials(self, judge_name: str) -> Dict:
        """Get financial disclosures"""
        return await courtlistener.search_financials(judge_name)
    
    async def legal_research(self, topic: str) -> Dict:
        """Research legal topic"""
        return await courtlistener.research_legal_basis(topic)
    
    async def due_process_cases(self) -> Dict:
        """Get due process cases"""
        cases = await courtlistener.get_due_process_cases()
        return {"cases": cases}
    
    async def habeas_corpus(self) -> Dict:
        """Get habeas corpus cases"""
        cases = await courtlistener.get_habeas_corpus_cases()
        return {"cases": cases}
    
    # === GITHUB TOOLS ===
    async def github_repos(self, username: str = "GlacierEQ") -> Dict:
        """List repositories"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/users/{username}/repos"
            headers = {"Authorization": f"token {vault.GITHUB_TOKEN}"}
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
    
    async def github_search(self, query: str) -> Dict:
        """Search GitHub"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = "https://api.github.com/search/repositories"
            headers = {"Authorization": f"token {vault.GITHUB_TOKEN}"}
            async with session.get(url, headers=headers, params={"q": query}) as resp:
                return await resp.json()
    
    async def github_issues(self, owner: str, repo: str) -> Dict:
        """Get issues"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/repos/{owner}/{repo}/issues"
            headers = {"Authorization": f"token {vault.GITHUB_TOKEN}"}
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
    
    async def github_commits(self, owner: str, repo: str) -> Dict:
        """Get commits"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            headers = {"Authorization": f"token {vault.GITHUB_TOKEN}"}
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
    
    # === NOTION TOOLS ===
    async def notion_search(self, query: str) -> Dict:
        """Search Notion"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = "https://api.notion.com/v1/search"
            headers = {
                "Authorization": f"Bearer {vault.NOTION_API_KEY}",
                "Notion-Version": "2022-06-28"
            }
            async with session.post(url, headers=headers, json={"query": query}) as resp:
                return await resp.json()
    
    async def notion_page(self, page_id: str) -> Dict:
        """Get Notion page"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.notion.com/v1/pages/{page_id}"
            headers = {
                "Authorization": f"Bearer {vault.NOTION_API_KEY}",
                "Notion-Version": "2022-06-28"
            }
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
    
    async def notion_chats(self) -> Dict:
        """Get chats from Notion database"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.notion.com/v1/databases/{vault.NOTION_CHATS_DB}/query"
            headers = {
                "Authorization": f"Bearer {vault.NOTION_API_KEY}",
                "Notion-Version": "2022-06-28"
            }
            async with session.post(url, headers=headers) as resp:
                return await resp.json()
    
    async def notion_create_page(self, title: str, content: str) -> Dict:
        """Create Notion page"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = "https://api.notion.com/v1/pages"
            headers = {
                "Authorization": f"Bearer {vault.NOTION_API_KEY}",
                "Notion-Version": "2022-06-28"
            }
            page = {
                "parent": {"database_id": vault.NOTION_CHATS_DB},
                "properties": {
                    "Name": {"title": [{"text": {"content": title}}]}
                },
                "children": [{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": content}}]}
                }]
            }
            async with session.post(url, headers=headers, json=page) as resp:
                return await resp.json()
    
    # === SUPABASE TOOLS ===
    async def supabase_query(self, table: str, filters: Optional[Dict] = None) -> Dict:
        """Query Supabase"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"{vault.SUPABASE_URL}/rest/v1/{table}"
            headers = {
                "apikey": vault.SUPABASE_API_KEY,
                "Authorization": f"Bearer {vault.SUPABASE_API_KEY}"
            }
            async with session.get(url, headers=headers, params=filters) as resp:
                return await resp.json()
    
    async def supabase_insert(self, table: str, data: Dict) -> Dict:
        """Insert into Supabase"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"{vault.SUPABASE_URL}/rest/v1/{table}"
            headers = {
                "apikey": vault.SUPABASE_API_KEY,
                "Authorization": f"Bearer {vault.SUPABASE_API_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            async with session.post(url, headers=headers, json=data) as resp:
                return await resp.json()
    
    async def supabase_update(self, table: str, data: Dict, match: Dict) -> Dict:
        """Update Supabase"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"{vault.SUPABASE_URL}/rest/v1/{table}"
            headers = {
                "apikey": vault.SUPABASE_API_KEY,
                "Authorization": f"Bearer {vault.SUPABASE_API_KEY}",
                "Content-Type": "application/json"
            }
            async with session.patch(url, headers=headers, json=data, params=match) as resp:
                return await resp.json()
    
    # === SERVICE TOOLS ===
    async def clickup_tasks(self) -> Dict:
        """Get ClickUp tasks"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = "https://api.clickup.com/api/v2/task"
            headers = {"Authorization": vault.CLICKUP_API_KEY}
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
    
    async def taskade_workspaces(self) -> Dict:
        """Get Taskade workspaces"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = "https://api.taskade.com/v1/workspaces"
            headers = {"Authorization": f"Bearer {vault.TASKADE_API_KEY}"}
            async with session.get(url, headers=headers) as resp:
                return await resp.json()
    
    async def elevenlabs_tts(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Dict:
        """Text to speech"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": vault.ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            async with session.post(url, headers=headers, json={"text": text}) as resp:
                return {"status": resp.status, "content_type": resp.headers.get("content-type")}
    
    async def assemblyai_transcribe(self, audio_url: str) -> Dict:
        """Transcribe audio"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = "https://api.assemblyai.com/v2/transcript"
            headers = {"Authorization": vault.ASSEMBLYAI_API_KEY}
            async with session.post(url, headers=headers, json={"audio_url": audio_url}) as resp:
                return await resp.json()
    
    # === SYSTEM TOOLS ===
    async def vault_status(self) -> Dict:
        """Get vault status"""
        return {
            "total_keys": 229,
            "working_providers": vault.get_working_providers(),
            "llm_providers": {k: bool(v) for k, v in vault.get_llm_providers().items()},
            "memory_providers": {k: bool(v) for k, v in vault.get_memory_providers().items()},
            "case_id": vault.CASE_ID,
            "operator": vault.OPERATOR_GUID
        }
    
    async def get_context(self, query: str) -> Dict:
        """Get multi-source context"""
        return await memory.get_context(query)
    
    async def swarm_status(self) -> Dict:
        """Get swarm status"""
        return {
            "status": "operational",
            "agents": ["genesis", "legal", "memory", "technical", "mcp"],
            "uptime": datetime.now().isoformat(),
            "case": vault.CASE_ID,
            "mission": "BRING KEKOA HOME"
        }
    
    def execute(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool"""
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        return self.tools[tool_name](**kwargs)

# Global instance
quantum_server = QuantumNexusMCPServer()
