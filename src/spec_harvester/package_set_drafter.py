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
PACKAGE_RELATION_PROPOSALS_FILENAME = "package-relation-proposals.json"
PACKAGE_RELATION_PROPOSALS_API_VERSION = "spec-harvester.package-relation-proposals/v0"
PACKAGE_RELATION_PROPOSALS_KIND = "SpecHarvesterPackageRelationProposals"
PACKAGE_RELATION_PROPOSALS_SCHEMA_VERSION = 1
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
        if any(self.options.out.iterdir()):
            raise ValueError(f"Package-set draft output directory is not empty: {self.options.out}")
        candidates = self.write_candidates()
        skipped = self.skipped_packages(candidates)
        relations = relation_records(self.inventory, candidates)
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
            "relationProposals": {
                "path": PACKAGE_RELATION_PROPOSALS_FILENAME,
                "reviewStatus": "producer_observed",
                "relationCount": len(relations),
            },
            "summary": {
                "candidateCount": len(candidates),
                "skippedCount": len(skipped),
                "packageInventoryCount": len(package_records(self.inventory)),
                "relationProposalCount": len(relations),
            },
            "authority": "producer_observed_review_evidence",
            "nonGoals": [
                "bundle_set_preflight",
                "specpm_acceptance",
                "relation_acceptance",
                "package_execution",
                "dependency_installation",
            ],
        }
        output_path = self.options.out / PACKAGE_SET_DRAFT_FILENAME
        output_path.write_text(render_package_set_draft_json(payload), encoding="utf-8")
        relation_path = self.options.out / PACKAGE_RELATION_PROPOSALS_FILENAME
        relation_path.write_text(
            render_relation_proposals_json(
                relation_proposals_payload(
                    inventory=self.inventory,
                    inventory_path=self.inventory_path,
                    package_set_draft_path=output_path,
                    relations=relations,
                )
            ),
            encoding="utf-8",
        )
        return {
            "status": "ok",
            "output": str(self.options.out),
            "summary": str(output_path),
            "relationProposals": str(relation_path),
            "candidateCount": len(candidates),
            "skippedCount": len(skipped),
            "relationCount": len(relations),
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


def relation_records(
    inventory: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    packages_by_id = package_records_by_id(inventory)
    workspace_candidates = [
        candidate for candidate in candidates if candidate.get("role") == "workspace"
    ]
    target_candidates = [
        candidate for candidate in candidates if candidate.get("role") != "workspace"
    ]
    records: list[dict[str, Any]] = []
    for source in sorted(workspace_candidates, key=lambda item: str(item.get("packageId") or "")):
        for target in sorted(target_candidates, key=lambda item: str(item.get("packageId") or "")):
            relation_id = relation_proposal_id(
                "contains",
                str(source["packageId"]),
                str(target["packageId"]),
            )
            records.append(
                {
                    "id": relation_id,
                    "type": "contains",
                    "source": relation_endpoint(source),
                    "target": relation_endpoint(target),
                    "reviewStatus": "producer_observed",
                    "authority": "producer_observed_review_evidence",
                    "evidence": relation_evidence(
                        inventory=inventory,
                        relation_id=relation_id,
                        source_package=packages_by_id.get(str(source["packageId"]), {}),
                        target_package=packages_by_id.get(str(target["packageId"]), {}),
                    ),
                }
            )
    return sorted(records, key=lambda item: item["id"])


def package_records_by_id(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for package in package_records(inventory):
        package_id = package.get("proposedSpecpmPackageId")
        if isinstance(package_id, str) and package_id:
            records[package_id] = package
    return records


def relation_endpoint(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "packageId": candidate.get("packageId"),
        "role": candidate.get("role"),
        "candidatePath": candidate.get("candidatePath"),
        "sourceTargetPath": candidate.get("sourceTargetPath"),
        "manifestPath": candidate.get("manifestPath"),
    }


def relation_evidence(
    *,
    inventory: dict[str, Any],
    relation_id: str,
    source_package: dict[str, Any],
    target_package: dict[str, Any],
) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for workspace_manifest in workspace_manifest_evidence_records(inventory):
        evidence.append({**workspace_manifest, "supports": [relation_id]})
    for role, package in (("source", source_package), ("target", target_package)):
        for package_evidence in package_manifest_evidence_records(package, role):
            evidence.append({**package_evidence, "supports": [relation_id]})
    return sorted(
        evidence, key=lambda item: (item["kind"], item["path"], item.get("packageRole", ""))
    )


def workspace_manifest_evidence_records(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    manifests = inventory.get("workspaceManifests")
    if not isinstance(manifests, list):
        return []
    records: list[dict[str, Any]] = []
    for manifest in manifests:
        if not isinstance(manifest, dict):
            continue
        evidence = manifest.get("evidence")
        if not isinstance(evidence, dict):
            evidence = {}
        path = evidence.get("path") or manifest.get("path")
        if not isinstance(path, str) or not path:
            continue
        record: dict[str, Any] = {
            "kind": evidence.get("kind") or "workspace_manifest",
            "path": path,
            "packageManager": manifest.get("packageManager"),
            "includePatterns": list_if_strings(manifest.get("includePatterns")),
            "excludePatterns": list_if_strings(manifest.get("excludePatterns")),
        }
        digest = evidence.get("digest")
        if isinstance(digest, dict):
            record["digest"] = digest
        records.append(record)
    return sorted(records, key=lambda item: item["path"])


def package_manifest_evidence_records(
    package: dict[str, Any],
    package_role: str,
) -> list[dict[str, Any]]:
    references = package.get("evidenceReferences")
    if not isinstance(references, list):
        references = []
    records: list[dict[str, Any]] = []
    for reference in references:
        if not isinstance(reference, dict) or reference.get("kind") != "package_manifest":
            continue
        path = reference.get("path")
        if not isinstance(path, str) or not path:
            continue
        record: dict[str, Any] = {
            "kind": "package_manifest",
            "path": path,
            "packageRole": package_role,
            "packageId": package.get("proposedSpecpmPackageId"),
        }
        digest = reference.get("digest")
        if isinstance(digest, dict):
            record["digest"] = digest
        records.append(record)
    if records:
        return sorted(records, key=lambda item: item["path"])
    manifest_path = package.get("manifestPath")
    if not isinstance(manifest_path, str) or not manifest_path:
        return []
    return [
        {
            "kind": "package_manifest",
            "path": manifest_path,
            "packageRole": package_role,
            "packageId": package.get("proposedSpecpmPackageId"),
        }
    ]


def list_if_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(item for item in value if isinstance(item, str))


def relation_proposal_id(relation_type: str, source: str, target: str) -> str:
    return f"{source}.{relation_type}.{target}"


def relation_proposals_payload(
    *,
    inventory: dict[str, Any],
    inventory_path: Path,
    package_set_draft_path: Path,
    relations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "apiVersion": PACKAGE_RELATION_PROPOSALS_API_VERSION,
        "kind": PACKAGE_RELATION_PROPOSALS_KIND,
        "schemaVersion": PACKAGE_RELATION_PROPOSALS_SCHEMA_VERSION,
        "source": source_record_from_inventory(inventory),
        "inputs": {
            "workspaceInventory": {
                "path": inventory_path.name,
                "digest": digest_record(sha256_file(inventory_path)),
                "apiVersion": inventory["apiVersion"],
                "kind": inventory["kind"],
            },
            "packageSetDraft": {
                "path": PACKAGE_SET_DRAFT_FILENAME,
                "digest": digest_record(sha256_file(package_set_draft_path)),
                "apiVersion": PACKAGE_SET_DRAFT_API_VERSION,
                "kind": PACKAGE_SET_DRAFT_KIND,
            },
        },
        "relations": relations,
        "summary": {
            "relationCount": len(relations),
            "containsCount": sum(1 for relation in relations if relation["type"] == "contains"),
            "sourcePackageCount": len({relation["source"]["packageId"] for relation in relations}),
            "targetPackageCount": len({relation["target"]["packageId"] for relation in relations}),
        },
        "reviewStatus": "producer_observed",
        "authority": "producer_observed_review_evidence",
        "nonGoals": [
            "relation_acceptance",
            "bundle_set_preflight",
            "specpm_acceptance",
            "package_execution",
            "dependency_installation",
        ],
    }


def source_record_from_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    source = inventory.get("source")
    if not isinstance(source, dict):
        return {}
    return {
        "repository": source.get("repository"),
        "exactRevision": source.get("exactRevision"),
        "revisionAuthority": source.get("revisionAuthority"),
        "declaredRef": source.get("declaredRef"),
    }


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
    if source_target_path == ".":
        return {"kind": "repository", "path": ".", "label": "workspace"}
    if role == "workspace":
        return {
            "kind": "folder",
            "path": source_target_path,
            "label": Path(source_target_path).name,
        }
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
        "size": package_size(package, manifest_path),
        "sha256": digest,
        "package": {
            "name": package.get("name") or package.get("proposedSpecpmPackageId"),
            "version": package.get("version") or "0.0.0",
            "ecosystem": package.get("ecosystem"),
            "packageManager": package.get("packageManager"),
            "description": package_description(package),
            "capabilityLabel": package_capability_label(package),
        },
    }
    license_name = package.get("license")
    if isinstance(license_name, str) and license_name.strip():
        record["package"]["license"] = license_name.strip()
    return record


def package_size(package: dict[str, Any], manifest_path: str) -> int:
    evidence_references = package.get("evidenceReferences")
    if not isinstance(evidence_references, list):
        return 0

    fallback_size = 0
    for evidence in evidence_references:
        if not isinstance(evidence, dict):
            continue
        size = evidence.get("size")
        if not isinstance(size, int) or size < 0:
            continue
        if fallback_size == 0:
            fallback_size = size
        if evidence.get("path") == manifest_path:
            return size
    return fallback_size


def package_digest(package: dict[str, Any]) -> str:
    evidence_references = package.get("evidenceReferences")
    if not isinstance(evidence_references, list):
        evidence_references = []
    for evidence in evidence_references:
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
    description = package.get("description")
    if isinstance(description, str) and description.strip():
        return description.strip()
    role = str(package.get("role") or "member_package")
    package_id = str(package.get("proposedSpecpmPackageId") or "package")
    role_summary = {
        "workspace": "aggregate workspace package-set entrypoint for repository discovery",
        "core_runtime": "framework-agnostic system utility package boundary",
        "react_binding": "React Flow package boundary",
        "svelte_binding": "Svelte Flow package boundary",
    }.get(role, "member package boundary")
    return f"Generated preview for {role_summary}: {package_id}."


def package_capability_label(package: dict[str, Any]) -> str:
    role = str(package.get("role") or "")
    if role == "workspace":
        return "workspace"
    if role == "core_runtime" and has_flow_system_evidence(package):
        return "flow_system_utilities"
    if role in {"react_binding", "svelte_binding"} and has_flow_canvas_evidence(package):
        return "flow_canvas"
    return "package_boundary"


def package_evidence_text(package: dict[str, Any]) -> str:
    fields = (
        "name",
        "description",
        "proposedSpecpmPackageId",
        "manifestPath",
        "sourceTargetPath",
    )
    return " ".join(
        value.strip()
        for field in fields
        if isinstance((value := package.get(field)), str) and value.strip()
    ).lower()


def has_flow_canvas_evidence(package: dict[str, Any]) -> bool:
    text = package_evidence_text(package)
    return (
        "xyflow" in text
        or "react flow" in text
        or "svelte flow" in text
        or "flow chart" in text
        or "flow charts" in text
        or (("node-based" in text or "node based" in text) and "diagram" in text)
    )


def has_flow_system_evidence(package: dict[str, Any]) -> bool:
    text = package_evidence_text(package)
    return (
        "xyflow" in text
        or "flow system" in text
        or "flow utilities" in text
        or ("core system" in text and "flow" in text)
    )


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
        "qualityReport": relative_output_path(output_root, draft_result["qualityReport"]),
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


def render_relation_proposals_json(payload: dict[str, Any]) -> str:
    return render_json(payload)


def render_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
