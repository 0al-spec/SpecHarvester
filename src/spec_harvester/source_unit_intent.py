from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SourceUnitIntentBoundary:
    source: Mapping[str, Any]
    has_package_manifest: bool

    @classmethod
    def from_snapshot(cls, snapshot: Mapping[str, Any]) -> SourceUnitIntentBoundary:
        source = snapshot.get("source")
        files = snapshot.get("files")
        return cls(
            source=source if isinstance(source, Mapping) else {},
            has_package_manifest=contains_package_manifest(files),
        )

    def intent_kind(self) -> str:
        target_kind = self.source_target_kind()
        if target_kind == "file":
            return "single_file"
        if self.has_package_manifest:
            return "package"
        if target_kind == "folder":
            return "folder_module"
        return "repository"

    def source_target_kind(self) -> str:
        target = self.source.get("target")
        if not isinstance(target, Mapping):
            return "repository"
        target_kind = target.get("kind")
        if target_kind in {"repository", "folder", "file"}:
            return str(target_kind)
        return "repository"

    def metadata(self) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "intentKind": self.intent_kind(),
            "sourceTargetKind": self.source_target_kind(),
            "claimScope": self.claim_scope(),
            "packageManagerOwnership": self.package_manager_ownership(),
            "reviewInstruction": self.review_instruction(),
        }
        target_path = self.source_target_path()
        if target_path is not None:
            metadata["sourceTargetPath"] = target_path
        return metadata

    def source_target_path(self) -> str | None:
        target = self.source.get("target")
        if not isinstance(target, Mapping):
            return None
        target_path = target.get("path")
        if isinstance(target_path, str) and target_path.strip():
            return target_path
        return None

    def claim_scope(self) -> str:
        intent_kind = self.intent_kind()
        if intent_kind == "package":
            if self.source_target_kind() == "repository":
                return "repository_package"
            return "scoped_package"
        if intent_kind == "folder_module":
            return "scoped_folder_module"
        if intent_kind == "single_file":
            return "scoped_single_file"
        return "repository"

    def package_manager_ownership(self) -> str:
        if self.intent_kind() == "package":
            return "claimed_from_harvested_package_manifest"
        if self.source_target_kind() in {"folder", "file"}:
            return "not_claimed_from_scoped_evidence"
        return "not_claimed_without_package_manifest"

    def package_summary(self, package_name: str, package_description: str | None) -> str:
        if package_description is not None:
            if self.intent_kind() == "package":
                return f"{package_name} public package boundary: {package_description}"
            return f"{self.summary_prefix(package_name)}: {package_description}"
        if self.intent_kind() == "package":
            return f"Observed public package boundary for {package_name}."
        return f"{self.summary_prefix(package_name)}."

    def fallback_capability_summary(self, package_name: str) -> str:
        if self.intent_kind() == "package":
            return f"Describe observed public package metadata for {package_name}."
        if self.intent_kind() == "folder_module":
            return f"Describe observed folder/module source-unit metadata for {package_name}."
        if self.intent_kind() == "single_file":
            return f"Describe observed single-file source-unit metadata for {package_name}."
        return f"Describe observed repository metadata for {package_name}."

    def boundary_title(self, package_name: str) -> str:
        if self.intent_kind() == "package":
            return f"{package_name} Generated Public Package Boundary"
        if self.intent_kind() == "folder_module":
            return f"{package_name} Generated Folder Module Boundary"
        if self.intent_kind() == "single_file":
            return f"{package_name} Generated Single File Boundary"
        return f"{package_name} Generated Repository Boundary"

    def scope_includes(self) -> list[str]:
        if self.intent_kind() == "package":
            return [
                "Describe observed public package metadata from an allowlisted harvest snapshot.",
                "Claim package-manager identity only from harvested package manifest evidence.",
                (
                    "Preserve source repository provenance, source target, "
                    "and harvest policy metadata."
                ),
            ]
        if self.intent_kind() == "folder_module":
            return [
                (
                    "Describe observed folder/module source-unit metadata from an "
                    "allowlisted scoped harvest snapshot."
                ),
                (
                    "Keep capabilities and intent IDs scoped to the harvested folder/module "
                    "unless additional repository or package evidence is present."
                ),
                (
                    "Preserve source repository, source target, and harvest policy "
                    "provenance metadata."
                ),
            ]
        if self.intent_kind() == "single_file":
            return [
                (
                    "Describe observed single-file source-unit metadata from an "
                    "allowlisted scoped harvest snapshot."
                ),
                (
                    "Keep capabilities and intent IDs scoped to the harvested file unless "
                    "additional repository or package evidence is present."
                ),
                (
                    "Preserve source repository, source target, and harvest policy "
                    "provenance metadata."
                ),
            ]
        return [
            "Describe observed repository metadata from an allowlisted harvest snapshot.",
            (
                "Declare repository-level capabilities and intent IDs only from static "
                "metadata and evidence present in the harvest snapshot."
            ),
            "Preserve source repository provenance and harvest policy metadata.",
        ]

    def constraint(self) -> dict[str, str]:
        return {
            "id": "source_unit_intent_boundary",
            "level": "MUST",
            "statement": self.constraint_statement(),
        }

    def constraint_statement(self) -> str:
        if self.intent_kind() == "package":
            return (
                "Package-manager ownership claims must remain limited to harvested "
                "package manifest evidence and the recorded source target."
            )
        if self.intent_kind() == "folder_module":
            return (
                "Folder/module candidates must not claim repository-level or "
                "package-manager ownership unless additional evidence is supplied."
            )
        if self.intent_kind() == "single_file":
            return (
                "Single-file candidates must not claim repository-level or "
                "package-manager ownership unless additional evidence is supplied."
            )
        return (
            "Repository candidates must not claim package-manager ownership without "
            "harvested package manifest evidence."
        )

    def review_instruction(self) -> str:
        if self.intent_kind() == "package":
            return "Review package claims against harvested package manifest evidence."
        if self.intent_kind() == "folder_module":
            return "Keep review scoped to the harvested folder/module target."
        if self.intent_kind() == "single_file":
            return "Keep review scoped to the harvested single-file target."
        return "Review repository-level claims without inferring package-manager ownership."

    def summary_prefix(self, package_name: str) -> str:
        if self.intent_kind() == "folder_module":
            return f"Observed folder/module source-unit boundary for {package_name}"
        if self.intent_kind() == "single_file":
            return f"Observed single-file source-unit boundary for {package_name}"
        return f"Observed repository boundary for {package_name}"


def contains_package_manifest(files: Any) -> bool:
    if not isinstance(files, list):
        return False
    return any(
        isinstance(item, Mapping)
        and item.get("kind") == "package_manifest"
        and isinstance(item.get("package"), Mapping)
        for item in files
    )
