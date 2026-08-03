"""Lane system — clean boundaries, one job per lane, explicit interfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from .receipt import MissionRecord, ActionRecord


@runtime_checkable
class Lane(Protocol):
    """Protocol for all lane implementations."""

    name: str
    capabilities: tuple[str, ...]
    authority: tuple[str, ...]
    restrictions: tuple[str, ...]
    tower_floors: tuple[str, ...]

    async def execute(self, mission: MissionRecord) -> ActionRecord:
        """Execute a mission action within this lane."""
        ...

    def health(self) -> dict[str, Any]:
        """Return lane health status."""
        ...

    def validate(self, mission: MissionRecord) -> bool:
        """Validate that a mission can run in this lane."""
        ...


@dataclass
class BaseLane:
    """Base implementation for lane adapters."""

    name: str
    capabilities: tuple[str, ...] = ()
    authority: tuple[str, ...] = ("read", "plan")
    restrictions: tuple[str, ...] = ()
    tower_floors: tuple[str, ...] = ("PY",)

    async def execute(self, mission: MissionRecord) -> ActionRecord:
        """Execute a mission action — override in subclass."""
        return ActionRecord(
            status="failed",
            error=f"lane '{self.name}' does not implement execute()",
        )

    def health(self) -> dict[str, Any]:
        return {"lane": self.name, "state": "available"}

    def validate(self, mission: MissionRecord) -> bool:
        """Validate that the mission's required capability is in this lane."""
        if mission.required_capability:
            return mission.required_capability in self.capabilities
        if mission.target_component:
            return True  # Component routing happens at runtime
        return True


class LaneManager:
    """Manages lane registration and mission routing."""

    def __init__(self) -> None:
        self._lanes: dict[str, Lane] = {}
        self._capability_map: dict[str, str] = {}

    def register(self, lane: Lane) -> None:
        """Register a lane."""
        self._lanes[lane.name] = lane
        for cap in lane.capabilities:
            self._capability_map[cap] = lane.name

    def unregister(self, name: str) -> None:
        """Unregister a lane."""
        lane = self._lanes.pop(name, None)
        if lane:
            for cap in lane.capabilities:
                if self._capability_map.get(cap) == name:
                    del self._capability_map[cap]

    def get(self, name: str) -> Lane | None:
        """Get a lane by name."""
        return self._lanes.get(name)

    def route(self, mission: MissionRecord) -> Lane | None:
        """Route a mission to the appropriate lane."""
        # Route by capability first
        if mission.required_capability:
            lane_name = self._capability_map.get(mission.required_capability)
            if lane_name:
                return self._lanes.get(lane_name)

        # Route by target component
        if mission.target_component:
            for lane in self._lanes.values():
                if mission.target_component in lane.name.lower():
                    return lane

        # Default to first registered lane
        if self._lanes:
            return next(iter(self._lanes.values()))

        return None

    def all_lanes(self) -> dict[str, Lane]:
        """Get all registered lanes."""
        return dict(self._lanes)

    def list_names(self) -> list[str]:
        """List all lane names."""
        return sorted(self._lanes.keys())

    def list_capabilities(self) -> dict[str, str]:
        """Map capabilities to lane names."""
        return dict(self._capability_map)
