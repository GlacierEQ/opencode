"""Mastermind configuration management."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class MastermindConfig:
    """Immutable configuration for the Mastermind runtime."""

    project_name: str = "mastermind"
    version: str = "2.0.0"
    environment: str = "development"
    log_level: str = "INFO"

    # Canonical runtime
    canonical_manifest: str = "engines/canonical/mastermind-family-v1.json"

    # Shadow layer
    shadow_enabled: bool = True
    shadow_encrypted: bool = True

    # Receipt chain
    receipt_export_path: str = "outputs/receipts/"
    receipt_chain_integrity: bool = True

    # Identity
    identity_strict: bool = True

    # Tower integration
    tower_enabled: bool = True

    # Paths
    base_dir: Path = field(default_factory=lambda: Path.cwd())
    engines_dir: Path = field(default_factory=lambda: Path.cwd() / "engines")
    shadow_dir: Path = field(default_factory=lambda: Path.cwd() / ".shadow")

    @classmethod
    def from_env(cls) -> MastermindConfig:
        """Load configuration from environment variables."""
        return cls(
            project_name=os.getenv("MASTERMIND_PROJECT", "mastermind"),
            version=os.getenv("MASTERMIND_VERSION", "2.0.0"),
            environment=os.getenv("MASTERMIND_ENV", "development"),
            log_level=os.getenv("MASTERMIND_LOG_LEVEL", "INFO"),
            canonical_manifest=os.getenv(
                "MASTERMIND_MANIFEST", "engines/canonical/mastermind-family-v1.json"
            ),
            shadow_enabled=os.getenv("MASTERMIND_SHADOW", "true").lower() == "true",
            shadow_encrypted=os.getenv("MASTERMIND_SHADOW_ENCRYPT", "true").lower() == "true",
            receipt_export_path=os.getenv("MASTERMIND_RECEIPT_PATH", "outputs/receipts/"),
            identity_strict=os.getenv("MASTERMIND_IDENTITY_STRICT", "true").lower() == "true",
            tower_enabled=os.getenv("MASTERMIND_TOWER", "true").lower() == "true",
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MastermindConfig:
        """Load configuration from a dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict[str, Any]:
        """Serialize configuration to a dictionary."""
        return {
            "project_name": self.project_name,
            "version": self.version,
            "environment": self.environment,
            "log_level": self.log_level,
            "canonical_manifest": self.canonical_manifest,
            "shadow_enabled": self.shadow_enabled,
            "shadow_encrypted": self.shadow_encrypted,
            "receipt_export_path": self.receipt_export_path,
            "receipt_chain_integrity": self.receipt_chain_integrity,
            "identity_strict": self.identity_strict,
            "tower_enabled": self.tower_enabled,
            "base_dir": str(self.base_dir),
            "engines_dir": str(self.engines_dir),
            "shadow_dir": str(self.shadow_dir),
        }
