#!/usr/bin/env python3
"""
Quantum Nexus CLI - Unified Interface
Usage: python run.py [command] [args]
"""
import asyncio
import sys
import json
from pathlib import Path

# Load vault environment
try:
    from dotenv import load_dotenv
    load_dotenv(Path.home() / ".vault_env")
except ImportError:
    pass

from quantum_nexus import vault, memory, courtlistener, quantum_server

async def status():
    """Show system status"""
    print("=" * 60)
    print("QUANTUM NEXUS - SOVEREIGN INTELLIGENCE STATUS")
    print("=" * 60)
    
    vault_status = await quantum_server.vault_status()
    swarm_status = await quantum_server.swarm_status()
    
    print(f"\nCase ID: {vault_status['case_id']}")
    print(f"Operator: {vault_status['operator']}")
    print(f"Mission: {swarm_status['mission']}")
    
    print("\n--- API Keys ---")
    for provider, available in vault_status['llm_providers'].items():
        status = "✓" if available else "✗"
        print(f"  [{status}] {provider}")
    
    print("\n--- Memory Providers ---")
    for provider, available in vault_status['memory_providers'].items():
        status = "✓" if available else "✗"
        print(f"  [{status}] {provider}")
    
    print("\n--- Working Services ---")
    for service in vault_status['working_providers']:
        print(f"  ✓ {service}")
    
    print("\n--- Active Agents ---")
    for agent in swarm_status['agents']:
        print(f"  → {agent}")
    
    print("=" * 60)

async def store(content: str, category: str = "general", source: str = "cli"):
    """Store a memory"""
    result = await quantum_server.memory_store(content, category, source)
    print(f"Stored: {json.dumps(result, indent=2)}")

async def search(query: str, category: str = None):
    """Search memories"""
    result = await quantum_server.memory_search(query, category)
    print(f"Results: {json.dumps(result, indent=2)}")

async def court_search(query: str):
    """Search CourtListener"""
    result = await quantum_server.courtlistener_search(query)
    print(f"Court Results: {json.dumps(result, indent=2)}")

async def due_process():
    """Get due process cases"""
    result = await quantum_server.due_process_cases()
    print(f"Due Process Cases: {json.dumps(result, indent=2)}")

async def habeas():
    """Get habeas corpus cases"""
    result = await quantum_server.habeas_corpus()
    print(f"Habeas Corpus: {json.dumps(result, indent=2)}")

async def research(topic: str):
    """Research legal topic"""
    result = await quantum_server.legal_research(topic)
    print(f"Research: {json.dumps(result, indent=2)}")

async def export_memories():
    """Export all memories"""
    result = await quantum_server.memory_export()
    print(f"Export: {json.dumps(result, indent=2)}")

async def vault_info():
    """Show vault info"""
    result = await quantum_server.vault_status()
    print(f"Vault: {json.dumps(result, indent=2)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [command] [args]")
        print("Commands:")
        print("  status        - Show system status")
        print("  store [text]  - Store memory")
        print("  search [q]    - Search memories")
        print("  court [q]     - Search CourtListener")
        print("  due-process   - Get due process cases")
        print("  habeas        - Get habeas corpus cases")
        print("  research [t]  - Research legal topic")
        print("  export        - Export all memories")
        print("  vault         - Show vault info")
        return
    
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    if command == "status":
        asyncio.run(status())
    elif command == "store":
        asyncio.run(store(" ".join(args) if args else "Memory from CLI"))
    elif command == "search":
        asyncio.run(search(" ".join(args) if args else "*"))
    elif command == "court":
        asyncio.run(court_search(" ".join(args)))
    elif command == "due-process":
        asyncio.run(due_process())
    elif command == "habeas":
        asyncio.run(habeas())
    elif command == "research":
        asyncio.run(research(" ".join(args)))
    elif command == "export":
        asyncio.run(export_memories())
    elif command == "vault":
        asyncio.run(vault_info())
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
