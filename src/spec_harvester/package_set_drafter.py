from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.classifier_registry import default_classifier_policy
from spec_harvester.collector import (
    PROJECT_PROFILE_SCHEMA_VERSION,
    SNAPSHOT_KIND,
    SNAPSHOT_SCHEMA_VERSION,
    default_analyzer_trust_policy,
)
from spec_harvester.drafter import (
    DEFAULT_AUTHOR,
    DEFAULT_SPEC_VERSION,
    DraftOptions,
    draft_spec_package,
)
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.workspace_inventory import (
    WORKSPACE_INVENTORY_API_VERSION,
    WORKSPACE_INVENTORY_KIND,
)

PACKAGE_SET_DRAFT_FILENAME = "package-set-draft.json"
PACKAGE_SET_DRAFT_API_VERSION = "spec-harvester.package-set-draft/v0"
PACKAGE_SET_DRAFT_KIND = "SpecHarvesterPackageSetDraft"
PACKAGE_SET_DRAFT_SCHEMA_VERSION = 1
DEFAULT_DRAFT_ROLES = ("workspace", "core_runtime", "react_binding", "svelte_binding")


@dataclass(frozen=True)
class PackageSetDraftOptions:
    inventory: Path
    out: Path
    version: str = DEFAULT_SPEC_VERSION
    author: str = DEFAULT_AUTHOR
    roles: tuple[str, ...] = DEFAULT_DRAFT_ROLES


class PackageSetDrafter:
    def __init__(self, options: PackageSetDraftOptions):
        self.options = options
        self.inventory_path = options.inventory
        self.inventory = read_inventory(options.inventory)

    def write(self) -> dict[str, Any]:
        self.options.out.mkdir(parents=True, exist_ok=True)
        candidates = self.write_candidates()
        skipped = self.skipped_packages(candidates)
        payload = {
            "apiVersion": PACKAGE_SET_DRAFT_API_VERSION,
            "kind": PACKAGE_SET_DRAFT_KIND,
            "schemaVersion": PACKAGE_SET_DRAFT_SCHEMA_VERSION,
            "source": self.source_record(),
            "workspaceInventory": {
                "path": self.inventory_path.name,
                "digest": digest_record(sha256_file(self.inventory_path)),
                "apiVersion": self.inventory["apiVersion"],
                "kind": self.inventory["kind"],
            },
            "selection": {
                "roles": list(self.options.roles),
                "authority": "producer_preview_selection",
            },
            "candidates": candidates,
            "skipped": skipped,
            "summary": {
                "candidateCount": len(candidates),
                "skippedCount": len(skipped),
                "packageInventoryCount": len(package_records(self.inventory)),
            },
            "authority": "producer_observed_review_evidence",
            "nonGoals": [
                "relation_proposal_emission",
                "bundle_set_preflight",
                "specpm_acceptance",
                "package_execution",
                "dependency_installation",
            ],
        }
        output_path = self.options.out / PACKAGE_SET_DRAFT_FILENAME
        output_path.write_text(render_package_set_draft_json(payload), encoding="utf-8")
        return {
            "status": "ok",
            "output": str(self.options.out),
            "summary": str(output_path),
            "candidateCount": len(candidates),
            "skippedCount": len(skipped),
            "candidates": candidates,
            "skipped": skipped,
        }

    def write_candidates(self) -> list[dict[str, Any]]:
        records = selected_package_records(self.inventory, self.options.roles)
        candidates: list[dict[str, Any]] = []
        for record in records:
            package_id = record["proposedSpecpmPackageId"]
            candidate_root = self.options.out / safe_candidate_dir(package_id)
            candidate_root.mkdir(parents=True, exist_ok=True)
            snapshot = synthetic_snapshot(self.inventory, record)
            snapshot_path = candidate_root / "harvest.json"
            snapshot_path.write_text(render_json(snapshot), encoding="utf-8")
            draft_result = draft_spec_package(
                DraftOptions(
                    snapshot=snapshot_path,
                    out=candidate_root,
                    package_id=package_id,
                    name=package_display_name(record),
                    version=self.options.version,
                    author=self.options.author,
                )
            )
            candidates.append(
                candidate_record(record, self.options.out, candidate_root, draft_result)
            )
        return sorted(candidates, key=lambda item: item["packageId"])

    def skipped_packages(self, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        generated_ids = {candidate["packageId"] for candidate in candidates}
        skipped: list[dict[str, Any]] = []
        for record in package_records(self.inventory):
            package_id = record.get("proposedSpecpmPackageId")
            if package_id in generated_ids:
                continue
            skipped.append(
                {
                    "packageId": package_id,
                    "role": record.get("role"),
                    "manifestPath": record.get("manifestPath"),
                    "reason": "role_not_selected_for_initial_package_set_draft",
                }
            )
        return sorted(skipped, key=lambda item: str(item.get("packageId") or ""))

    def source_record(self) -> dict[str, Any]:
        source = self.inventory.get("source")
        if not isinstance(source, dict):
            return {}
        return {
            "repository": source.get("repository"),
            "exactRevision": source.get("exactRevision"),
            "revisionAuthority": source.get("revisionAuthority"),
            "declaredRef": source.get("declaredRef"),
        }


def draft_package_set(options: PackageSetDraftOptions) -> dict[str, Any]:
    return PackageSetDrafter(options).write()


def read_inventory(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Workspace inventory must be a JSON object")
    if payload.get("apiVersion") != WORKSPACE_INVENTORY_API_VERSION:
        raise ValueError(
            f"Unsupported workspace inventory apiVersion: {payload.get('apiVersion')!r}"
        )
    if payload.get("kind") != WORKSPACE_INVENTORY_KIND:
        raise ValueError(f"Unsupported workspace inventory kind: {payload.get('kind')!r}")
    return payload


def selected_package_records(
    inventory: dict[str, Any], roles: tuple[str, ...]
) -> list[dict[str, Any]]:
    selected_roles = set(roles)
    return sorted(
        [
            record
            for record in package_records(inventory)
            if isinstance(record.get("role"), str) and record["role"] in selected_roles
        ],
        key=lambda item: (
            role_rank(str(item.get("role") or "")),
            str(item.get("manifestPath") or ""),
        ),
    )


def package_records(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    packages = inventory.get("packages")
    if not isinstance(packages, list):
        return []
    return [record for record in packages if isinstance(record, dict)]


def role_rank(role: str) -> int:
    try:
        return DEFAULT_DRAFT_ROLES.index(role)
    except ValueError:
        return len(DEFAULT_DRAFT_ROLES)


def synthetic_snapshot(inventory: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    source = inventory.get("source")
    if not isinstance(source, dict):
        source = {}
    target = source_target_record(package)
    manifest_record = package_file_record(package)
    project_profile = project_profile_record(package, manifest_record)
    return {
        "schemaVersion": SNAPSHOT_SCHEMA_VERSION,
        "kind": SNAPSHOT_KIND,
        "source": {
            "kind": "workspace_inventory",
            "label": package_label(package),
            "repository": source.get("repository"),
            "revision": source.get("exactRevision"),
            "target": target,
        },
        "policy": {
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "contentAuthority": "untrusted_metadata",
        },
        "analyzerPolicy": default_analyzer_trust_policy(),
        "classifierPolicy": default_classifier_policy(),
        "projectProfile": project_profile,
        "files": [manifest_record],
        "skippedFiles": [],
        "summary": {
            "targetKind": target["kind"],
            "fileCount": 1,
            "skippedFileCount": 0,
            "packageManifestCount": 1,
            "licenseFileCount": 0,
        },
    }


def source_target_record(package: dict[str, Any]) -> dict[str, str]:
    source_target_path = str(package.get("sourceTargetPath") or ".")
    role = str(package.get("role") or "")
    if source_target_path == "." or role == "workspace":
        return {"kind": "repository", "path": ".", "label": "workspace"}
    return {
        "kind": "folder",
        "path": source_target_path,
        "label": Path(source_target_path).name,
    }


def package_file_record(package: dict[str, Any]) -> dict[str, Any]:
    manifest_path = str(package.get("manifestPath") or "package.json")
    digest = package_digest(package)
    record = {
        "path": manifest_path,
        "kind": "package_manifest",
        "size": 0,
        "sha256": digest,
        "package": {
            "name": package.get("name") or package.get("proposedSpecpmPackageId"),
            "version": package.get("version") or "0.0.0",
            "ecosystem": package.get("ecosystem"),
            "packageManager": package.get("packageManager"),
            "description": package_description(package),
        },
    }
    return record


def package_digest(package: dict[str, Any]) -> str:
    for evidence in package.get("evidenceReferences", []):
        if not isinstance(evidence, dict):
            continue
        digest = evidence.get("digest")
        if not isinstance(digest, dict):
            continue
        value = digest.get("value")
        if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value):
            return value.lower()
    return hashlib.sha256(render_json(package).encode("utf-8")).hexdigest()


def package_description(package: dict[str, Any]) -> str:
    role = str(package.get("role") or "member_package")
    package_id = str(package.get("proposedSpecpmPackageId") or "package")
    role_summary = {
        "workspace": "aggregate workspace package-set entrypoint",
        "core_runtime": "core runtime package boundary",
        "react_binding": "React package boundary",
        "svelte_binding": "Svelte package boundary",
    }.get(role, "member package boundary")
    return f"Generated preview for {role_summary} {package_id}."


def project_profile_record(
    package: dict[str, Any], manifest_record: dict[str, Any]
) -> dict[str, Any]:
    language = package_language(package)
    ecosystem = str(package.get("ecosystem") or "unknown")
    package_manager = str(package.get("packageManager") or "unknown")
    manifest_path = manifest_record["path"]
    return {
        "schemaVersion": PROJECT_PROFILE_SCHEMA_VERSION,
        "languages": [
            {
                "id": language,
                "confidence": "high",
                "reason": "Workspace inventory package manifest evidence.",
                "evidencePaths": [manifest_path],
            }
        ],
        "ecosystems": [
            {
                "id": ecosystem,
                "language": language,
                "packageManager": package_manager,
                "confidence": "high",
                "reason": "Workspace inventory package manifest evidence.",
                "evidencePaths": [manifest_path],
            }
        ],
        "manifests": [
            {
                "path": manifest_path,
                "kind": "package_manifest",
                "language": language,
                "ecosystem": ecosystem,
                "packageManager": package_manager,
                "confidence": "high",
                "reason": "Workspace inventory package manifest evidence.",
                "sha256": manifest_record["sha256"],
                "parser": "spec_harvester.workspace_inventory",
            }
        ],
        "analyzerPlan": [],
        "diagnostics": [],
    }


def package_language(package: dict[str, Any]) -> str:
    ecosystem = str(package.get("ecosystem") or "").lower()
    if ecosystem in {"npm", "pnpm", "yarn", "bun"}:
        return "javascript"
    if ecosystem in {"pypi", "python"}:
        return "python"
    if ecosystem in {"swift", "swiftpm"}:
        return "swift"
    return ecosystem or "unknown"


def candidate_record(
    package: dict[str, Any],
    output_root: Path,
    candidate_root: Path,
    draft_result: dict[str, Any],
) -> dict[str, Any]:
    candidate_path = candidate_root.relative_to(output_root).as_posix()
    return {
        "packageId": draft_result["packageId"],
        "role": package.get("role"),
        "sourceTargetPath": package.get("sourceTargetPath"),
        "manifestPath": package.get("manifestPath"),
        "candidatePath": candidate_path,
        "manifest": relative_output_path(output_root, draft_result["manifest"]),
        "spec": relative_output_path(output_root, draft_result["spec"]),
        "producerReceipt": relative_output_path(output_root, draft_result["producerReceipt"]),
        "validationReport": relative_output_path(output_root, draft_result["validationReport"]),
        "diagnosticsReport": relative_output_path(output_root, draft_result["diagnosticsReport"]),
        "status": draft_result["status"],
    }


def relative_output_path(output_root: Path, path: Any) -> str:
    value = Path(str(path))
    try:
        return value.relative_to(output_root).as_posix()
    except ValueError:
        return value.as_posix()


def safe_candidate_dir(package_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", package_id).strip("-") or "package"


def package_display_name(package: dict[str, Any]) -> str:
    package_id = str(package.get("proposedSpecpmPackageId") or "Package")
    return " ".join(part.capitalize() for part in package_id.split(".") if part)


def package_label(package: dict[str, Any]) -> str:
    source_target_path = str(package.get("sourceTargetPath") or "")
    if source_target_path and source_target_path != ".":
        return Path(source_target_path).name
    package_id = str(package.get("proposedSpecpmPackageId") or "workspace")
    return package_id.rsplit(".", 1)[-1]


def render_package_set_draft_json(payload: dict[str, Any]) -> str:
    return render_json(payload)


def render_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
