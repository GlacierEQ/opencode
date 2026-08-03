"""CLI entry point for Mastermind runtime."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Sequence

from .runtime.spine import MastermindRuntime
from .runtime.config import MastermindConfig
from .runtime.receipt import MissionRecord


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mastermind",
        description="Mastermind — Canonical mission-control operating system",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s 2.0.0"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # health command
    subparsers.add_parser("health", help="Show runtime health status")

    # execute command
    exec_parser = subparsers.add_parser("execute", help="Execute a mission")
    exec_parser.add_argument("intent", help="Mission intent description")
    exec_parser.add_argument(
        "--component", "-c", default=None, help="Target component"
    )
    exec_parser.add_argument(
        "--capability", "-cap", default=None, help="Required capability"
    )
    exec_parser.add_argument(
        "--action", "-a", default="plan", help="Action class (read, plan, write_internal)"
    )
    exec_parser.add_argument(
        "--requested-by", "-r", default="cli", help="Requester identity"
    )
    exec_parser.add_argument(
        "--metadata", "-m", default="{}", help="JSON metadata"
    )

    # chain command
    subparsers.add_parser("chain", help="Verify receipt chain integrity")

    # receipts command
    receipts_parser = subparsers.add_parser("receipts", help="List receipts")
    receipts_parser.add_argument(
        "--export", "-e", default=None, help="Export to file path"
    )

    # lanes command
    subparsers.add_parser("lanes", help="List registered lanes")

    # identity command
    identity_parser = subparsers.add_parser("identity", help="Identity operations")
    identity_sub = identity_parser.add_subparsers(dest="identity_command")
    identity_sub.add_parser("list", help="List all identity cards")
    check_parser = identity_sub.add_parser("check", help="Check authority")
    check_parser.add_argument("component", help="Component name")
    check_parser.add_argument("action", help="Action to check")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = MastermindConfig.from_env()
    runtime = MastermindRuntime(config)

    if args.command == "health":
        health = runtime.health()
        print(json.dumps(health, indent=2))
        return 0

    if args.command == "execute":
        metadata = json.loads(args.metadata)
        mission = MissionRecord(
            intent=args.intent,
            requested_by=args.requested_by,
            action_class=args.action,
            target_component=args.component,
            required_capability=args.capability,
            metadata=metadata,
        )
        receipt = asyncio.run(runtime.execute(mission))
        print(json.dumps(receipt.to_dict(), indent=2))
        return 0 if receipt.status == "succeeded" else 2

    if args.command == "chain":
        valid = runtime.verify_chain()
        print(json.dumps({"chain_valid": valid, "receipts": runtime.receipts.count()}))
        return 0 if valid else 1

    if args.command == "receipts":
        receipts = runtime.receipts.all()
        data = [r.to_dict() for r in receipts]
        if args.export:
            runtime.export_receipts(args.export)
            print(json.dumps({"exported": len(data), "path": args.export}))
        else:
            print(json.dumps(data, indent=2))
        return 0

    if args.command == "lanes":
        lanes = runtime.lanes.list_names()
        print(json.dumps({"lanes": lanes}))
        return 0

    if args.command == "identity":
        if args.identity_command == "list":
            cards = runtime.identity.all_cards()
            data = {k: v.to_dict() for k, v in cards.items()}
            print(json.dumps(data, indent=2))
            return 0
        if args.identity_command == "check":
            authority = runtime.identity.verify(args.component, args.action)
            print(json.dumps({
                "allowed": authority.allowed,
                "reason": authority.reason,
                "component": authority.component,
                "action": authority.action,
            }))
            return 0 if authority.allowed else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
