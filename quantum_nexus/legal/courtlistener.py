import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from ..core.vault import vault

class CourtListenerClient:
    """Full CourtListener API v4 client for Case 1FDV-23-0001009"""
    
    BASE_URL = "https://www.courtlistener.com/api/rest/v4"
    
    def __init__(self):
        self.api_key = vault.COURTLISTENER_API_KEY
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.BASE_URL}{endpoint}"
            async with session.request(method, url, headers=self.headers, **kwargs) as resp:
                return await resp.json()
    
    # === Dockets ===
    async def search_dockets(self, query: str, **filters) -> Dict:
        """Search dockets"""
        params = {"q": query, **filters}
        return await self._request("GET", "/dockets/", params=params)
    
    async def get_docket(self, docket_id: int) -> Dict:
        """Get docket by ID"""
        return await self._request("GET", f"/dockets/{docket_id}/")
    
    async def get_docket_entries(self, docket_id: int) -> List[Dict]:
        """Get all entries for a docket"""
        data = await self._request("GET", f"/dockets/{docket_id}/entries/")
        return data.get("results", [])
    
    async def search_case_1FDV(self) -> Dict:
        """Search specifically for Case 1FDV-23-0001009"""
        return await self.search_dockets(
            case_name="Kekoa",
            court__in="haw",
            date_filed__gte="2023-01-01"
        )
    
    # === RECAP Archive ===
    async def search_recap(self, query: str) -> Dict:
        """Search RECAP archive for free documents"""
        params = {"q": query}
        return await self._request("GET", "/recap/", params=params)
    
    async def get_recap_documents(self, docket_id: int) -> List[Dict]:
        """Get RECAP documents for a docket"""
        data = await self._request("GET", f"/dockets/{docket_id}/recap-documents/")
        return data.get("results", [])
    
    # === Court Opinions ===
    async def search_opinions(self, query: str, **filters) -> Dict:
        """Search court opinions"""
        params = {"q": query, **filters}
        return await self._request("GET", "/opinions/", params=params)
    
    async def get_opinion(self, opinion_id: int) -> Dict:
        """Get opinion by ID"""
        return await self._request("GET", f"/opinions/{opinion_id}/")
    
    async def search_hawaii_opinions(self, query: str) -> Dict:
        """Search Hawaii family court opinions"""
        return await self.search_opinions(
            q=query,
            court__in="haw",
            date_filed__gte="2020-01-01"
        )
    
    # === People (Judges, Attorneys) ===
    async def search_people(self, query: str) -> Dict:
        """Search judges and attorneys"""
        params = {"q": query}
        return await self._request("GET", "/people/", params=params)
    
    async def get_person(self, person_id: int) -> Dict:
        """Get person by ID"""
        return await self._request("GET", f"/people/{person_id}/")
    
    async def get_judges(self) -> List[Dict]:
        """Get judges"""
        data = await self._request("GET", "/people/", params={"position_type": "judge"})
        return data.get("results", [])
    
    # === Citations ===
    async def get_citations(self, citation_id: int) -> Dict:
        """Get citations for a cluster"""
        return await self._request("GET", f"/clusters/{citation_id}/citations/")
    
    async def get_cited_by(self, cluster_id: int) -> Dict:
        """Get cases that cite a cluster"""
        return await self._request("GET", f"/clusters/{cluster_id}/cited-by/")
    
    # === Alerts ===
    async def create_alert(self, **kwargs) -> Dict:
        """Create a PACER alert"""
        return await self._request("POST", "/recap-alerts/", json=kwargs)
    
    async def get_alerts(self) -> List[Dict]:
        """Get all alerts"""
        data = await self._request("GET", "/recap-alerts/")
        return data.get("results", [])
    
    # === Financial Disclosures ===
    async def search_financials(self, judge_name: str) -> Dict:
        """Search financial disclosures"""
        params = {"q": judge_name}
        return await self._request("GET", "/financial-disclosures/", params=params)
    
    # === Case Law Research ===
    async def research_legal_basis(self, topic: str) -> Dict:
        """Research legal basis for family court case"""
        constitutional = await self.search_opinions(
            q=f"14th Amendment family court",
            court__scotus=True
        )
        hawaii = await self.search_hawaii_opinions(topic)
        
        return {
            "constitutional": constitutional,
            "hawaii_precedent": hawaii,
            "topic": topic,
            "researched_at": datetime.now().isoformat()
        }
    
    async def get_due_process_cases(self) -> List[Dict]:
        """Get due process cases relevant to family court"""
        results = await self.search_opinions(
            q="due process parental rights family court",
            court__in="scotus,ca9,haw",
            date_filed__gte="2000-01-01"
        )
        return results.get("results", [])
    
    async def get_habeas_corpus_cases(self) -> List[Dict]:
        """Get habeas corpus cases"""
        results = await self.search_opinions(
            q="habeas corpus family court detention",
            court__in="scotus,ca9,haw"
        )
        return results.get("results", [])

# Global instance
courtlistener = CourtListenerClient()
