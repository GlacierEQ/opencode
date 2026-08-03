"""Mastermind runtime spine — the unified entry point for all execution."""

from __future__ import annotations

import asyncio
from typing import Any, Mapping

from .config import MastermindConfig
from .identity import IdentityLayer, AgentCard, Authority
from .receipt import (
    GENESIS_HASH,
    ReceiptChain,
    MissionRecord,
    ActionRecord,
    Receipt,
    _canonical_hash,
    _utc_now,
)
from .lane import Lane, LaneManager


class MastermindRuntime:
    """
    The spine of Mastermind.

    Single entry point for all execution.
    Manages identity, routing, receipt, and handoff.
    """

    def __init__(self, config: MastermindConfig | None = None) -> None:
        self.config = config or MastermindConfig()
        self.identity = IdentityLayer(strict=self.config.identity_strict)
        self.lanes = LaneManager()
        self.receipts = ReceiptChain()
        self._adapters: dict[str, Any] = {}
        self._shadow: Any = None
        self._lock = asyncio.Lock()

    async def execute(self, mission: MissionRecord) -> Receipt:
        """
        Execute a mission through the runtime.

        Flow:
        1. Identity check — can this component do this?
        2. Route to correct lane
        3. Execute in lane
        4. Record receipt
        5. Return receipt
        """
        async with self._lock:
            started_at = _utc_now()

            # 1. Identity check
            if mission.target_component:
                authority = self.identity.verify(mission.target_component, mission.action_class)
                if not authority.allowed:
                    return self._record_receipt(
                        mission=mission,
                        component_id=mission.target_component,
                        lane="blocked",
                        started_at=started_at,
                        result=ActionRecord(
                            status="blocked",
                            error=f"identity denied: {authority.reason}",
                        ),
                    )

            # 2. Route to lane
            lane = self.lanes.route(mission)
            if lane is None:
                return self._record_receipt(
                    mission=mission,
                    component_id=mission.target_component or "unresolved",
                    lane="unroutable",
                    started_at=started_at,
                    result=ActionRecord(
                        status="blocked",
                        error="no lane matches this mission",
                    ),
                )

            # 3. Validate lane
            if not lane.validate(mission):
                return self._record_receipt(
                    mission=mission,
                    component_id=mission.target_component or "unresolved",
                    lane=lane.name,
                    started_at=started_at,
                    result=ActionRecord(
                        status="blocked",
                        error=f"lane '{lane.name}' rejected mission",
                    ),
                )

            # 4. Execute
            try:
                result = await lane.execute(mission)
            except Exception as exc:
                result = ActionRecord(
                    status="failed",
                    error=f"lane execution failed: {exc}",
                )

            # 5. Record receipt
            return self._record_receipt(
                mission=mission,
                component_id=mission.target_component or "resolved",
                lane=lane.name,
                started_at=started_at,
                result=result,
            )

    def _record_receipt(
        self,
        *,
        mission: MissionRecord,
        component_id: str,
        lane: str,
        started_at: str,
        result: ActionRecord,
    ) -> Receipt:
        """Record a receipt in the chain."""
        return self.receipts.append(
            mission=mission,
            component_id=component_id,
            lane=lane,
            status=result.status,
            started_at=started_at,
            result=result,
        )

    def health(self) -> dict[str, Any]:
        """Return runtime health status."""
        return {
            "runtime": "mastermind",
            "version": self.config.version,
            "environment": self.config.environment,
            "lanes": self.lanes.list_names(),
            "identity_cards": len(self.identity.all_cards()),
            "receipts": self.receipts.count(),
            "chain_valid": self.receipts.verify(),
        }

    def register_lane(self, lane: Lane) -> None:
        """Register a lane with the runtime."""
        self.lanes.register(lane)
        # Also register lane as an identity card
        card = AgentCard(
            name=f"lane-{lane.name}",
            lane=lane.name,
            capabilities=lane.capabilities,
            authority=lane.authority,
            restrictions=lane.restrictions,
            tower_floors=lane.tower_floors,
        )
        self.identity.register(card)

    def register_adapter(self, component_id: str, adapter: Any) -> None:
        """Register an adapter for a component."""
        self._adapters[component_id] = adapter

    def get_adapter(self, component_id: str) -> Any:
        """Get an adapter for a component."""
        return self._adapters.get(component_id)

    def verify_chain(self) -> bool:
        """Verify receipt chain integrity."""
        return self.receipts.verify()

    def export_receipts(self, path: str) -> str:
        """Export receipts to a file."""
        return str(self.receipts.export(path))
