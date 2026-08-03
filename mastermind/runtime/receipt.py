"""Receipt chain — tamper-evident, hash-linked audit trail."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping
from uuid import UUID, uuid4


GENESIS_HASH = "0" * 64


def _canonical_hash(value: Any) -> str:
    """Deterministic SHA-256 hash of a JSON-serializable value."""
    payload = json.dumps(
        _json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _json_ready(value: Any) -> Any:
    """Convert non-JSON types to serializable form."""
    if hasattr(value, "value") and isinstance(value, str):
        return value.value
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    return value


def _utc_now() -> str:
    """Current UTC time as ISO string."""
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class MissionRecord:
    """A request to execute work through the runtime."""

    intent: str
    requested_by: str
    action_class: str = "plan"
    mission_id: UUID = field(default_factory=uuid4)
    target_component: str | None = None
    required_capability: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": str(self.mission_id),
            "intent": self.intent,
            "requested_by": self.requested_by,
            "action_class": self.action_class,
            "target_component": self.target_component,
            "required_capability": self.required_capability,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ActionRecord:
    """A result from executing a mission action."""

    status: str  # succeeded | failed | blocked
    output: Any = None
    error: str | None = None
    evidence_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "evidence_refs": list(self.evidence_refs),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class Receipt:
    """A single immutable audit record, hash-linked to its predecessor."""

    receipt_id: UUID = field(default_factory=uuid4)
    mission_id: str = ""
    action_id: str = ""
    component_id: str = ""
    lane: str = ""
    action_class: str = "plan"
    status: str = "blocked"
    started_at: str = ""
    completed_at: str = ""
    input_hash: str = ""
    output_hash: str | None = None
    evidence_refs: tuple[str, ...] = ()
    error: str | None = None
    previous_hash: str = GENESIS_HASH
    receipt_hash: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self, *, include_hash: bool = True) -> dict[str, Any]:
        data = {
            "receipt_id": str(self.receipt_id),
            "mission_id": self.mission_id,
            "action_id": self.action_id,
            "component_id": self.component_id,
            "lane": self.lane,
            "action_class": self.action_class,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "evidence_refs": list(self.evidence_refs),
            "error": self.error,
            "previous_hash": self.previous_hash,
            "metadata": dict(self.metadata),
        }
        if include_hash:
            data["receipt_hash"] = self.receipt_hash
        return data


class ReceiptChain:
    """Append-only, hash-chained receipt ledger."""

    def __init__(self) -> None:
        self._receipts: list[Receipt] = []

    def append(
        self,
        *,
        mission: MissionRecord,
        component_id: str,
        lane: str,
        status: str,
        started_at: str,
        result: ActionRecord,
    ) -> Receipt:
        """Append a new receipt to the chain."""
        previous_hash = self._receipts[-1].receipt_hash if self._receipts else GENESIS_HASH
        input_hash = _canonical_hash(mission.to_dict())
        output_hash = _canonical_hash(result.to_dict()) if result.output is not None else None

        # Build receipt data
        receipt_data = {
            "mission_id": str(mission.mission_id),
            "action_id": str(uuid4()),
            "component_id": component_id,
            "lane": lane,
            "action_class": mission.action_class,
            "status": status,
            "started_at": started_at,
            "completed_at": _utc_now(),
            "input_hash": input_hash,
            "output_hash": output_hash,
            "evidence_refs": list(result.evidence_refs),
            "error": result.error,
            "previous_hash": previous_hash,
            "metadata": dict(result.metadata),
        }
        # Compute hash from data without hash
        receipt_hash = _canonical_hash(receipt_data)
        receipt_data["receipt_hash"] = receipt_hash

        receipt = Receipt(**receipt_data)
        self._receipts.append(receipt)
        return receipt

    def verify(self) -> bool:
        """Verify the entire chain integrity."""
        previous_hash = GENESIS_HASH
        for receipt in self._receipts:
            if receipt.previous_hash != previous_hash:
                return False
            # Recompute hash from data excluding receipt_id and receipt_hash
            data = {
                "mission_id": receipt.mission_id,
                "action_id": receipt.action_id,
                "component_id": receipt.component_id,
                "lane": receipt.lane,
                "action_class": receipt.action_class,
                "status": receipt.status,
                "started_at": receipt.started_at,
                "completed_at": receipt.completed_at,
                "input_hash": receipt.input_hash,
                "output_hash": receipt.output_hash,
                "evidence_refs": list(receipt.evidence_refs),
                "error": receipt.error,
                "previous_hash": receipt.previous_hash,
                "metadata": dict(receipt.metadata),
            }
            expected_hash = _canonical_hash(data)
            if receipt.receipt_hash != expected_hash:
                return False
            previous_hash = receipt.receipt_hash
        return True

    def all(self) -> tuple[Receipt, ...]:
        """Return all receipts as an immutable tuple."""
        return tuple(self._receipts)

    def last(self) -> Receipt | None:
        """Return the most recent receipt, or None if empty."""
        return self._receipts[-1] if self._receipts else None

    def count(self) -> int:
        """Return the number of receipts."""
        return len(self._receipts)

    def export(self, path: str | Path) -> Path:
        """Export receipts as NDJSON."""
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        body = "\n".join(
            json.dumps(receipt.to_dict(), sort_keys=True, ensure_ascii=False)
            for receipt in self._receipts
        )
        if body:
            body += "\n"
        output_path.write_text(body, encoding="utf-8")
        return output_path

    def clear(self) -> None:
        """Clear the receipt chain (use with caution)."""
        self._receipts.clear()
