"""Identity layer — who am I, what can I do, what can't I do."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable


@dataclass(frozen=True)
class AgentCard:
    """Identity card for a component."""

    name: str
    version: str = "1.0.0"
    lane: str = "unknown"
    capabilities: tuple[str, ...] = ()
    authority: tuple[str, ...] = ()
    restrictions: tuple[str, ...] = ()
    tower_floors: tuple[str, ...] = ()
    evidence_level: str = "DECLARED"
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "lane": self.lane,
            "capabilities": list(self.capabilities),
            "authority": list(self.authority),
            "restrictions": list(self.restrictions),
            "tower_floors": list(self.tower_floors),
            "evidence_level": self.evidence_level,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> AgentCard:
        return cls(
            name=data["name"],
            version=data.get("version", "1.0.0"),
            lane=data.get("lane", "unknown"),
            capabilities=tuple(data.get("capabilities", [])),
            authority=tuple(data.get("authority", [])),
            restrictions=tuple(data.get("restrictions", [])),
            tower_floors=tuple(data.get("tower_floors", [])),
            evidence_level=data.get("evidence_level", "DECLARED"),
            description=data.get("description", ""),
        )

    @classmethod
    def from_yaml(cls, path: str | Path) -> AgentCard:
        """Load an agent card from a YAML file."""
        import yaml

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)


@dataclass(frozen=True)
class Authority:
    """Result of an identity verification check."""

    allowed: bool
    reason: str = ""
    component: str = ""
    action: str = ""
    evidence_level: str = "DECLARED"


@runtime_checkable
class IdentityProvider(Protocol):
    """Protocol for identity verification providers."""

    def verify(self, component: str, action: str) -> Authority:
        """Verify if a component can perform an action."""
        ...

    def get_card(self, component: str) -> AgentCard | None:
        """Get the identity card for a component."""
        ...

    def get_capabilities(self) -> list[str]:
        """List all registered capabilities."""
        ...


class IdentityLayer:
    """Manages component identity, capabilities, and authority enforcement."""

    def __init__(self, strict: bool = True) -> None:
        self._cards: dict[str, AgentCard] = {}
        self._strict = strict

    def register(self, card: AgentCard) -> None:
        """Register an agent card."""
        self._cards[card.name] = card

    def unregister(self, name: str) -> None:
        """Unregister an agent card."""
        self._cards.pop(name, None)

    def get_card(self, name: str) -> AgentCard | None:
        """Get an agent card by name."""
        return self._cards.get(name)

    def all_cards(self) -> dict[str, AgentCard]:
        """Get all registered cards."""
        return dict(self._cards)

    def verify(self, component: str, action: str) -> Authority:
        """Verify if a component can perform an action."""
        card = self._cards.get(component)
        if card is None:
            if self._strict:
                return Authority(
                    allowed=False,
                    reason=f"component '{component}' not registered",
                    component=component,
                    action=action,
                )
            return Authority(
                allowed=True,
                reason="non-strict mode: component not registered",
                component=component,
                action=action,
            )

        # Check restrictions first
        for restriction in card.restrictions:
            if self._matches_pattern(action, restriction):
                return Authority(
                    allowed=False,
                    reason=f"action '{action}' matches restriction '{restriction}'",
                    component=component,
                    action=action,
                    evidence_level=card.evidence_level,
                )

        # Check authority
        if card.authority:
            for auth in card.authority:
                if self._matches_pattern(action, auth):
                    return Authority(
                        allowed=True,
                        component=component,
                        action=action,
                        evidence_level=card.evidence_level,
                    )
            return Authority(
                allowed=False,
                reason=f"action '{action}' not in authority list",
                component=component,
                action=action,
                evidence_level=card.evidence_level,
            )

        # No authority list means allowed (permissive default)
        return Authority(
            allowed=True,
            component=component,
            action=action,
            evidence_level=card.evidence_level,
        )

    def can_execute(self, component: str, action: str) -> bool:
        """Check if a component can execute an action."""
        return self.verify(component, action).allowed

    def get_capabilities(self) -> list[str]:
        """List all registered capabilities."""
        caps = set()
        for card in self._cards.values():
            caps.update(card.capabilities)
        return sorted(caps)

    def get_components_with_capability(self, capability: str) -> list[str]:
        """Find all components with a given capability."""
        return [
            card.name
            for card in self._cards.values()
            if capability in card.capabilities
        ]

    @staticmethod
    def _matches_pattern(action: str, pattern: str) -> bool:
        """Simple pattern matching (supports * wildcard)."""
        if pattern == "*":
            return True
        if "*" in pattern:
            prefix, suffix = pattern.split("*", 1)
            return action.startswith(prefix) and action.endswith(suffix)
        return action == pattern

    def load_from_directory(self, directory: str | Path) -> int:
        """Load all YAML agent cards from a directory."""
        dir_path = Path(directory)
        if not dir_path.exists():
            return 0

        count = 0
        for yaml_file in dir_path.glob("**/*.yaml"):
            try:
                card = AgentCard.from_yaml(yaml_file)
                self.register(card)
                count += 1
            except Exception:
                continue
        for yml_file in dir_path.glob("**/*.yml"):
            try:
                card = AgentCard.from_yaml(yml_file)
                self.register(card)
                count += 1
            except Exception:
                continue
        return count
