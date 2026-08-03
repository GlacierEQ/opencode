"""
Quantum Nexus - Sovereign Intelligence System
Unified architecture for legal defense, memory systems, and MCP orchestration
"""
from .core.vault import vault, QuantumVault
from .memory.orchestrator import memory, MemoryOrchestrator, MemoryEntry
from .legal.courtlistener import courtlistener, CourtListenerClient
from .mcp.server import quantum_server, QuantumNexusMCPServer

__version__ = "1.0.0"
__codename__ = "QUANTUM-NEXUS-SOVEREIGN"

__all__ = [
    "vault",
    "QuantumVault",
    "memory",
    "MemoryOrchestrator",
    "MemoryEntry",
    "courtlistener",
    "CourtListenerClient",
    "quantum_server",
    "QuantumNexusMCPServer",
]
