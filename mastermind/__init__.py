"""Mastermind — Canonical mission-control operating system for the GlacierEQ agent family.

This package provides the unified runtime, lane system, identity layer,
and shadow integration for all Mastermind components.
"""

from .runtime.spine import MastermindRuntime
from .runtime.identity import IdentityLayer, AgentCard, Authority
from .runtime.receipt import ReceiptChain
from .runtime.lane import Lane, LaneManager
from .runtime.config import MastermindConfig

__version__ = "2.0.0"

__all__ = [
    "MastermindRuntime",
    "IdentityLayer",
    "AgentCard",
    "Authority",
    "ReceiptChain",
    "Lane",
    "LaneManager",
    "MastermindConfig",
]
