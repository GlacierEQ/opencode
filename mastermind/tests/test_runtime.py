"""Tests for Mastermind runtime spine."""

import asyncio
import pytest
from mastermind.runtime.spine import MastermindRuntime
from mastermind.runtime.config import MastermindConfig
from mastermind.runtime.identity import AgentCard, Authority
from mastermind.runtime.receipt import (
    MissionRecord,
    ActionRecord,
    ReceiptChain,
    Receipt,
    GENESIS_HASH,
)
from mastermind.runtime.lane import BaseLane, LaneManager


# ─── Config Tests ───

def test_config_defaults():
    config = MastermindConfig()
    assert config.project_name == "mastermind"
    assert config.version == "2.0.0"
    assert config.environment == "development"
    assert config.shadow_enabled is True
    assert config.identity_strict is True

def test_config_from_dict():
    config = MastermindConfig.from_dict({"project_name": "test", "version": "1.0.0"})
    assert config.project_name == "test"
    assert config.version == "1.0.0"

def test_config_to_dict():
    config = MastermindConfig()
    data = config.to_dict()
    assert "project_name" in data
    assert "version" in data
    assert "shadow_enabled" in data


# ─── Receipt Tests ───

def test_genesis_hash():
    assert GENESIS_HASH == "0" * 64
    assert len(GENESIS_HASH) == 64

def test_receipt_chain_empty():
    chain = ReceiptChain()
    assert chain.count() == 0
    assert chain.last() is None
    assert chain.verify() is True

def test_receipt_chain_append():
    chain = ReceiptChain()
    mission = MissionRecord(intent="test", requested_by="tester")
    result = ActionRecord(status="succeeded", output="ok")
    receipt = chain.append(
        mission=mission,
        component_id="test-component",
        lane="test-lane",
        status="succeeded",
        started_at="2025-01-01T00:00:00",
        result=result,
    )
    assert receipt.status == "succeeded"
    assert receipt.previous_hash == GENESIS_HASH
    assert receipt.receipt_hash != ""
    assert chain.count() == 1
    assert chain.verify() is True

def test_receipt_chain_integrity():
    chain = ReceiptChain()
    for i in range(5):
        mission = MissionRecord(intent=f"test-{i}", requested_by="tester")
        result = ActionRecord(status="succeeded", output=f"output-{i}")
        chain.append(
            mission=mission,
            component_id="test-component",
            lane="test-lane",
            status="succeeded",
            started_at="2025-01-01T00:00:00",
            result=result,
        )
    assert chain.count() == 5
    assert chain.verify() is True
    assert chain.last().previous_hash == chain._receipts[-2].receipt_hash

def test_receipt_export(tmp_path):
    chain = ReceiptChain()
    mission = MissionRecord(intent="test", requested_by="tester")
    result = ActionRecord(status="succeeded", output="ok")
    chain.append(
        mission=mission,
        component_id="test-component",
        lane="test-lane",
        status="succeeded",
        started_at="2025-01-01T00:00:00",
        result=result,
    )
    path = tmp_path / "receipts.jsonl"
    chain.export(path)
    assert path.exists()
    content = path.read_text()
    assert "test-component" in content


# ─── Identity Tests ───

def test_identity_layer_register():
    from mastermind.runtime.identity import IdentityLayer
    layer = IdentityLayer()
    card = AgentCard(
        name="test-agent",
        lane="test",
        capabilities=("read", "write"),
        authority=("read", "write"),
    )
    layer.register(card)
    assert layer.get_card("test-agent") is not None
    assert layer.can_execute("test-agent", "read") is True
    assert layer.can_execute("test-agent", "delete") is False

def test_identity_layer_strict():
    from mastermind.runtime.identity import IdentityLayer
    layer = IdentityLayer(strict=True)
    assert layer.can_execute("unknown-component", "read") is False

def test_identity_layer_permissive():
    from mastermind.runtime.identity import IdentityLayer
    layer = IdentityLayer(strict=False)
    assert layer.can_execute("unknown-component", "read") is True

def test_identity_layer_capabilities():
    from mastermind.runtime.identity import IdentityLayer
    layer = IdentityLayer()
    layer.register(AgentCard(name="a", capabilities=("read", "write")))
    layer.register(AgentCard(name="b", capabilities=("read", "execute")))
    caps = layer.get_capabilities()
    assert "read" in caps
    assert "write" in caps
    assert "execute" in caps

def test_identity_layer_restriction():
    from mastermind.runtime.identity import IdentityLayer
    layer = IdentityLayer()
    card = AgentCard(
        name="restricted-agent",
        authority=("*",),
        restrictions=("delete",),
    )
    layer.register(card)
    assert layer.can_execute("restricted-agent", "read") is True
    assert layer.can_execute("restricted-agent", "delete") is False


# ─── Lane Tests ───

class TestLane(BaseLane):
    async def execute(self, mission: MissionRecord) -> ActionRecord:
        return ActionRecord(status="succeeded", output=f"executed in {self.name}")

def test_lane_manager_register():
    manager = LaneManager()
    lane = TestLane(name="test", capabilities=("read", "write"))
    manager.register(lane)
    assert manager.get("test") is not None
    assert "test" in manager.list_names()

def test_lane_manager_route_by_capability():
    manager = LaneManager()
    lane = TestLane(name="legal", capabilities=("filing", "research"))
    manager.register(lane)
    mission = MissionRecord(
        intent="file motion",
        requested_by="tester",
        required_capability="filing",
    )
    routed = manager.route(mission)
    assert routed is not None
    assert routed.name == "legal"

def test_lane_manager_route_by_component():
    manager = LaneManager()
    lane = TestLane(name="engineering", capabilities=("code", "deploy"))
    manager.register(lane)
    mission = MissionRecord(
        intent="review code",
        requested_by="tester",
        target_component="engineering-service",
    )
    routed = manager.route(mission)
    assert routed is not None

def test_lane_validate():
    lane = TestLane(name="test", capabilities=("read",))
    mission_ok = MissionRecord(intent="read", requested_by="t", required_capability="read")
    mission_bad = MissionRecord(intent="write", requested_by="t", required_capability="write")
    assert lane.validate(mission_ok) is True
    assert lane.validate(mission_bad) is False


# ─── Runtime Integration Tests ───

def test_runtime_health():
    runtime = MastermindRuntime()
    health = runtime.health()
    assert health["runtime"] == "mastermind"
    assert health["version"] == "2.0.0"
    assert health["chain_valid"] is True

def test_runtime_execute_no_lane():
    runtime = MastermindRuntime()
    mission = MissionRecord(intent="test", requested_by="tester", target_component="unknown")
    receipt = asyncio.run(runtime.execute(mission))
    assert receipt.status == "blocked"
    # Identity check happens before lane routing
    assert "identity denied" in receipt.error.lower() or "not registered" in receipt.error.lower()

def test_runtime_execute_with_lane():
    runtime = MastermindRuntime()
    lane = TestLane(name="test-lane", capabilities=("read",))
    runtime.register_lane(lane)
    mission = MissionRecord(
        intent="read data",
        requested_by="tester",
        required_capability="read",
    )
    receipt = asyncio.run(runtime.execute(mission))
    assert receipt.status == "succeeded"
    assert receipt.lane == "test-lane"

def test_runtime_chain_verification():
    runtime = MastermindRuntime()
    lane = TestLane(name="test-lane", capabilities=("read",))
    runtime.register_lane(lane)
    for i in range(3):
        mission = MissionRecord(
            intent=f"mission-{i}",
            requested_by="tester",
            required_capability="read",
        )
        asyncio.run(runtime.execute(mission))
    assert runtime.verify_chain() is True
    assert runtime.receipts.count() == 3
