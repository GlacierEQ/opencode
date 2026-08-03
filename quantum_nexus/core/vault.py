import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv("/root/.vault_env")
except ImportError:
    pass

@dataclass
class QuantumVault:
    """Immutable vault of all API credentials"""
    
    # Core Identity
    OPERATOR_GUID: str = os.getenv("OPERATOR_GUID", "OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09")
    CASE_ID: str = "1FDV-23-0001009"
    GLOBAL_BUCKET: str = "LFVblPuL3N8N8k2FLyGcsCkMSMSrHsG9"
    
    # GitHub
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_PAT: str = os.getenv("GITHUB_PAT", "")
    GITHUB_PAT2: str = os.getenv("GITHUB_PAT2", "")
    GITHUB_PAT3: str = os.getenv("GITHUB_PAT3", "")
    GITHUB_USER: str = "GlacierEQ"
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_ADMIN_KEY: str = os.getenv("OPENAI_ADMIN_KEY", "")
    OPENAI_WINDSURF_KEY: str = os.getenv("OPENAI_WINDSURF_KEY", "")
    
    # Anthropic
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Google
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_DRIVE_API_KEY: str = os.getenv("GOOGLE_DRIVE_API_KEY", "")
    
    # AI/ML Services
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_KEY2: str = os.getenv("DEEPSEEK_API_KEY2", "")
    DEEPSEEK_API_KEY3: str = os.getenv("DEEPSEEK_API_KEY3", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_WRITE_TOKEN: str = os.getenv("HUGGINGFACE_WRITE_TOKEN", "")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    NEBIUS_API_KEY: str = os.getenv("NEBIUS_API_KEY", "")
    TOGETHER_AI_API_KEY: str = os.getenv("TOGETHER_AI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_KEY2: str = os.getenv("OPENROUTER_API_KEY2", "")
    PERPLEXITY_API_KEY: str = os.getenv("PERPLEXITY_API_KEY", "")
    
    # Memory Systems
    MEM0_API_KEY: str = os.getenv("MEM0_API_KEY", "")
    MEM0_ORG_ID: str = os.getenv("MEM0_ORG_ID", "")
    MEM0_ORG_NAME: str = os.getenv("MEM0_ORG_NAME", "hi_guy-default-org")
    MEM_API_KEY: str = os.getenv("MEM_API_KEY", "")
    MEM_API_KEY2: str = os.getenv("MEM_API_KEY2", "")
    MEMORY_PLUGIN_PRIMARY: str = os.getenv("MEMORY_PLUGIN_PRIMARY", "")
    MEMORY_PLUGIN_SPECIALIZED: str = os.getenv("MEMORY_PLUGIN_SPECIALIZED", "")
    SUPERMEMORY_KEY: str = os.getenv("SUPERMEMORY_KEY", "")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_HIGUY_KEY: str = os.getenv("PINECONE_HIGUY_KEY", "")
    
    # Notion
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    NOTION_WORKSPACE_ID: str = os.getenv("NOTION_WORKSPACE_ID", "")
    NOTION_CHATS_DB: str = "178b1e4f-3223-8121-a92e-f5fef191fa0f"
    NOTION_PLATFORMS_DB: str = "178b1e4f-3223-8122-bc93-f893d61b21fd"
    
    # Project Management
    CLICKUP_API_KEY: str = os.getenv("CLICKUP_API_KEY", "")
    TASKADE_API_KEY: str = os.getenv("TASKADE_API_KEY", "")
    
    # Cloud Storage
    SUPABASE_URL: str = "https://kjebmdgvjvuutzvhbtp.supabase.co"
    SUPABASE_API_KEY: str = os.getenv("SUPABASE_API_KEY", "")
    SUPABASE_GLACIEREQ_KEY: str = os.getenv("SUPABASE_GLACIEREQ_KEY", "")
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "")
    
    # Voice & Media
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ASSEMBLYAI_API_KEY: str = "61738597490848ed9ef61cf58eb3b16c"
    FIGMA_API_KEY: str = os.getenv("FIGMA_API_KEY", "")
    
    # DevOps
    RENDER_API_KEY: str = os.getenv("RENDER_API_KEY", "")
    POSTMAN_API_KEY: str = os.getenv("POSTMAN_API_KEY", "")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    AGENTOPS_API_KEY: str = os.getenv("AGENTOPS_API_KEY", "")
    
    # Legal & Court
    COURTLISTENER_API_KEY: str = "27cb3521fc97253116933795c20d3987b11865e9"
    APRYSE_SDK_KEY: str = os.getenv("APRYSE_SDK_KEY", "")
    
    # Document Processing
    PDF4ME_PRIMARY_KEY: str = os.getenv("PDF4ME_PRIMARY_KEY", "")
    PDF4ME_SECONDARY_KEY: str = os.getenv("PDF4ME_SECONDARY_KEY", "")
    TISANE_PRIMARY_KEY: str = os.getenv("TISANE_PRIMARY_KEY", "")
    TISANE_SECONDARY_KEY: str = os.getenv("TISANE_SECONDARY_KEY", "")
    
    # Misc
    SMITHERY_API_KEY: str = os.getenv("SMITHERY_API_KEY", "")
    E2B_API_KEY: str = os.getenv("E2B_API_KEY", "")
    NEO4J_API_KEY: str = os.getenv("NEO4J_API_KEY", "")
    MERMAID_TOKEN: str = os.getenv("MERMAID_TOKEN", "")
    NATIF_API_KEY: str = os.getenv("NATIF_API_KEY", "")
    ZAMAR_API_KEY: str = os.getenv("ZAMAR_API_KEY", "")
    CODY_API_KEY: str = os.getenv("CODY_API_KEY", "")
    HERD_TRAIL_API_KEY: str = os.getenv("HERD_TRAIL_API_KEY", "")
    SNYK_GITHUB_CONTAINER_KEY: str = os.getenv("SNYK_GITHUB_CONTAINER_KEY", "")
    
    # SSH/Git
    POLYGIT_SSH_PUBLIC: str = os.getenv("POLYGIT_SSH_PUBLIC", "")
    POLYGIT_SSH_PRIVATE: str = os.getenv("POLYGIT_SSH_PRIVATE", "")
    
    # Microsoft
    MICROSOFT_TENANT_KEY: str = os.getenv("MICROSOFT_TENANT_KEY", "")
    CONFLUENCE_API_KEY: str = os.getenv("CONFLUENCE_API_KEY", "")
    
    # Webhooks
    WEBHOOK_SIGNING_SECRET: str = os.getenv("WEBHOOK_SIGNING_SECRET", "")
    GITLAB_TOKEN: str = os.getenv("GITLAB_TOKEN", "")
    GITLAB_FEED_TOKEN: str = os.getenv("GITLAB_FEED_TOKEN", "")
    
    # AnythingLLM
    ANYTHING_LLM_URL: str = os.getenv("ANYTHING_LLM_URL", "http://localhost:3001/api")
    ANYTHING_LLM_KEY: str = os.getenv("ANYTHING_LLM_KEY", "")
    
    # Grok
    GROK_VOICE_URL: str = "wss://api.x.ai/v1/realtime"
    GROK_VOICE_SESSION: str = "gcf_LFvblPuL3N8N8k2FLyGcsCkMSMSrHsG9-20251229-APEX"
    
    # API Status
    def get_working_providers(self) -> List[str]:
        """Return known working AI providers"""
        working = []
        if self.COURTLISTENER_API_KEY:
            working.append("courtlistener")
        if self.GITHUB_TOKEN:
            working.append("github")
        if self.SUPABASE_API_KEY:
            working.append("supabase")
        if self.MEM0_API_KEY:
            working.append("mem0")
        if self.PINECONE_API_KEY:
            working.append("pinecone")
        if self.NOTION_API_KEY:
            working.append("notion")
        return working
    
    def get_llm_providers(self) -> Dict[str, str]:
        """Return available LLM providers"""
        return {
            "openai": self.OPENAI_API_KEY,
            "anthropic": self.ANTHROPIC_API_KEY,
            "gemini": self.GEMINI_API_KEY,
            "deepseek": self.DEEPSEEK_API_KEY,
            "groq": self.GROQ_API_KEY,
            "cohere": self.COHERE_API_KEY,
            "huggingface": self.HUGGINGFACE_API_KEY,
            "nebius": self.NEBIUS_API_KEY,
            "together": self.TOGETHER_AI_API_KEY,
            "openrouter": self.OPENROUTER_API_KEY,
            "perplexity": self.PERPLEXITY_API_KEY,
        }
    
    def get_memory_providers(self) -> Dict[str, str]:
        """Return memory system providers"""
        return {
            "mem0": self.MEM0_API_KEY,
            "memory_plugin": self.MEMORY_PLUGIN_PRIMARY,
            "pinecone": self.PINECONE_API_KEY,
            "supermemory": self.SUPERMEMORY_KEY,
        }
    
    def get_service_map(self) -> Dict[str, str]:
        """Return all service endpoints"""
        return {
            "github": "https://api.github.com",
            "supabase": self.SUPABASE_URL,
            "notion": "https://api.notion.com/v1",
            "courtlistener": "https://www.courtlistener.com/api/rest/v4",
            "grok": self.GROK_VOICE_URL,
            "mem0": "https://api.mem0.ai/v1",
            "pinecone": "https://api.pinecone.io",
            "elevenlabs": "https://api.elevenlabs.io/v1",
            "assemblyai": "https://api.assemblyai.com/v2",
        }

# Singleton vault
vault = QuantumVault()
