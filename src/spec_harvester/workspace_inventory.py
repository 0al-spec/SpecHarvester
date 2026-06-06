from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.collector import DEFAULT_MAX_FILE_BYTES, parse_package_json

WORKSPACE_INVENTORY_FILENAME = "workspace-inventory.json"
WORKSPACE_INVENTORY_API_VERSION = "spec-harvester.workspace-inventory/v0"
WORKSPACE_INVENTORY_KIND = "SpecHarvesterWorkspaceInventory"
WORKSPACE_INVENTORY_SCHEMA_VERSION = 1
PACKAGE_MANIFEST_NAMES = ("package.json",)


@dataclass(frozen=True)
class WorkspaceInventoryRequest:
    checkout: Path
    repository: dict[str, Any]
    snapshot: dict[str, Any]
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES


class WorkspaceInventory:
    def __init__(self, request: WorkspaceInventoryRequest):
        self.request = request
        self.checkout = request.checkout.resolve()

    def payload(self) -> dict[str, Any]:
        diagnostics: list[dict[str, Any]] = []
        workspace_manifests = self.workspace_manifests(diagnostics)
        packages = self.package_records(workspace_manifests, diagnostics)
        return {
            "apiVersion": WORKSPACE_INVENTORY_API_VERSION,
            "kind": WORKSPACE_INVENTORY_KIND,
            "schemaVersion": WORKSPACE_INVENTORY_SCHEMA_VERSION,
            "source": self.source_record(),
            "workspaceManifests": workspace_manifests,
            "packages": packages,
            "summary": {
                "workspaceManifestCount": len(workspace_manifests),
                "packageManifestCount": len(packages),
                "packageCount": len(packages),
                "diagnosticCount": len(diagnostics),
            },
            "diagnostics": sorted(
                diagnostics, key=lambda item: (item["level"], item["code"], item.get("path", ""))
            ),
            "privacy": {
                "rawSourceIncluded": False,
                "manifestContentsIncluded": False,
                "evidenceIncludesDigests": True,
                "packageScriptsExecuted": False,
                "dependenciesInstalled": False,
            },
            "authority": "producer_observed_review_evidence",
        }

    def source_record(self) -> dict[str, Any]:
        repository = self.request.repository
        source = self.request.snapshot.get("source", {})
        revision = exact_revision(self.checkout, repository)
        record = {
            "repository": repository["repository"],
            "exactRevision": revision["exactRevision"],
            "revisionAuthority": revision["revisionAuthority"],
            "declaredRef": repository.get("ref"),
            "sourceManifest": repository["sourceManifest"],
        }
        if isinstance(source, dict) and isinstance(source.get("target"), dict):
            record["target"] = source["target"]
        return record

    def workspace_manifests(self, diagnostics: list[dict[str, Any]]) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for manifest_path in sorted(self.workspace_manifest_paths()):
            absolute = self.checkout / manifest_path
            patterns = workspace_patterns(absolute, diagnostics, self.request.max_file_bytes)
            detector = manifest_profile(self.request.snapshot, manifest_path)
            records.append(
                {
                    "path": manifest_path,
                    "ecosystem": detector.get("ecosystem", workspace_ecosystem(manifest_path)),
                    "packageManager": detector.get(
                        "packageManager", workspace_package_manager(manifest_path)
                    ),
                    "includePatterns": sorted(
                        pattern for pattern in patterns if not is_exclude_pattern(pattern)
                    ),
                    "excludePatterns": sorted(
                        pattern[1:] for pattern in patterns if is_exclude_pattern(pattern)
                    ),
                    "evidence": evidence_reference(absolute, manifest_path),
                }
            )
        return records

    def workspace_manifest_paths(self) -> set[str]:
        paths: set[str] = set()
        for manifest in project_profile_manifests(self.request.snapshot):
            path = manifest.get("path")
            if not isinstance(path, str):
                continue
            if manifest.get("kind") == "workspace_manifest":
                paths.add(path)
                continue
            if Path(path).name == "package.json" and workspace_patterns(
                self.checkout / path, [], self.request.max_file_bytes
            ):
                paths.add(path)
        return paths

    def package_records(
        self, workspace_manifests: list[dict[str, Any]], diagnostics: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        paths = self.package_manifest_paths(workspace_manifests, diagnostics)
        namespace = proposed_namespace(self.request.repository)
        profiles = {
            manifest["path"]: manifest
            for manifest in project_profile_manifests(self.request.snapshot)
            if isinstance(manifest.get("path"), str)
        }
        records = [
            package_record(
                checkout=self.checkout,
                manifest_path=path,
                profile=profiles.get(path, {}),
                namespace=namespace,
                workspace_paths={item["path"] for item in workspace_manifests},
                max_file_bytes=self.request.max_file_bytes,
                diagnostics=diagnostics,
            )
            for path in sorted(paths)
        ]
        return deduplicate_proposed_ids(records)

    def package_manifest_paths(
        self, workspace_manifests: list[dict[str, Any]], diagnostics: list[dict[str, Any]]
    ) -> set[str]:
        paths = {
            manifest["path"]
            for manifest in project_profile_manifests(self.request.snapshot)
            if manifest.get("kind") == "package_manifest" and isinstance(manifest.get("path"), str)
        }
        for workspace_manifest in workspace_manifests:
            manifest_dir = Path(workspace_manifest["path"]).parent
            include_paths: set[str] = set()
            for pattern in workspace_manifest["includePatterns"]:
                include_paths.update(
                    package_manifests_for_pattern(
                        self.checkout,
                        manifest_dir,
                        pattern,
                        diagnostics,
                        self.request.max_file_bytes,
                    )
                )
            exclude_paths: set[str] = set()
            for pattern in workspace_manifest["excludePatterns"]:
                exclude_paths.update(
                    package_manifests_for_pattern(
                        self.checkout,
                        manifest_dir,
                        pattern,
                        diagnostics,
                        self.request.max_file_bytes,
                    )
                )
            paths.difference_update(exclude_paths)
            paths.update(include_paths - exclude_paths)
        return paths


def build_workspace_inventory(request: WorkspaceInventoryRequest) -> dict[str, Any]:
    return WorkspaceInventory(request).payload()


def render_workspace_inventory_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def write_workspace_inventory(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(render_workspace_inventory_json(payload), encoding="utf-8")
    return path


def workspace_inventory_batch_record(payload: dict[str, Any], output_path: Path) -> dict[str, Any]:
    return {
        "status": "complete",
        "output": str(output_path),
        "kind": payload["kind"],
        "schemaVersion": payload["schemaVersion"],
        "summary": payload["summary"],
    }


def exact_revision(checkout: Path, repository: dict[str, Any]) -> dict[str, str]:
    revision = repository.get("revision")
    if isinstance(revision, str) and revision:
        return {
            "exactRevision": revision,
            "revisionAuthority": "source_manifest_revision",
        }
    head = git_head_revision(checkout)
    if head is None:
        repository_id = repository.get("id", "<unknown>")
        raise ValueError(
            f"Repository id {repository_id!r} requires exact revision for workspace inventory; "
            "set revision or use a git checkout with HEAD available"
        )
    return {
        "exactRevision": head,
        "revisionAuthority": "git_head",
    }


def git_head_revision(checkout: Path) -> str | None:
    result = subprocess.run(  # noqa: S603
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    if re.fullmatch(r"[0-9a-fA-F]{40}", value) is None:
        return None
    return value.lower()


def project_profile_manifests(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    profile = snapshot.get("projectProfile")
    if not isinstance(profile, dict):
        return []
    manifests = profile.get("manifests")
    if not isinstance(manifests, list):
        return []
    return [manifest for manifest in manifests if isinstance(manifest, dict)]


def manifest_profile(snapshot: dict[str, Any], path: str) -> dict[str, Any]:
    for manifest in project_profile_manifests(snapshot):
        if manifest.get("path") == path:
            return manifest
    return {}


def workspace_patterns(
    path: Path, diagnostics: list[dict[str, Any]], max_file_bytes: int
) -> list[str]:
    if not path.is_file():
        return []
    if path.stat().st_size > max_file_bytes:
        diagnostics.append(
            {
                "level": "warning",
                "code": "workspace_manifest_too_large",
                "message": "Workspace manifest was too large to parse for include patterns.",
                "path": path.name,
            }
        )
        return []
    if path.name == "pnpm-workspace.yaml":
        return pnpm_workspace_patterns(path, diagnostics)
    if path.name == "package.json":
        return package_json_workspace_patterns(path, diagnostics)
    return []


def pnpm_workspace_patterns(path: Path, diagnostics: list[dict[str, Any]]) -> list[str]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        diagnostics.append(
            {
                "level": "warning",
                "code": "workspace_manifest_parse_failed",
                "message": f"Could not parse pnpm workspace manifest: {exc}",
                "path": path.name,
            }
        )
        return []
    if not isinstance(payload, dict):
        return []
    packages = payload.get("packages")
    if not isinstance(packages, list):
        return []
    return sorted(str(item) for item in packages if isinstance(item, str) and item.strip())


def package_json_workspace_patterns(path: Path, diagnostics: list[dict[str, Any]]) -> list[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        diagnostics.append(
            {
                "level": "warning",
                "code": "workspace_manifest_parse_failed",
                "message": f"Could not parse package.json workspace metadata: {exc.msg}",
                "path": path.name,
            }
        )
        return []
    if not isinstance(payload, dict):
        return []
    workspaces = payload.get("workspaces")
    if isinstance(workspaces, list):
        return sorted(str(item) for item in workspaces if isinstance(item, str) and item.strip())
    if isinstance(workspaces, dict):
        packages = workspaces.get("packages")
        if isinstance(packages, list):
            return sorted(str(item) for item in packages if isinstance(item, str) and item.strip())
    return []


def package_manifests_for_pattern(
    checkout: Path,
    manifest_dir: Path,
    pattern: str,
    diagnostics: list[dict[str, Any]],
    max_file_bytes: int,
) -> set[str]:
    if unsafe_workspace_pattern(pattern):
        diagnostics.append(
            {
                "level": "warning",
                "code": "workspace_pattern_unsafe",
                "message": "Workspace include pattern was skipped because it is not repo-relative.",
                "path": pattern,
            }
        )
        return set()
    matches: set[str] = set()
    normalized = pattern.rstrip("/")
    search_root = checkout / manifest_dir
    for name in PACKAGE_MANIFEST_NAMES:
        for path in search_root.glob(f"{normalized}/{name}"):
            if path.is_file() and is_inside(checkout, path.resolve()):
                if path.stat().st_size > max_file_bytes:
                    diagnostics.append(
                        {
                            "level": "warning",
                            "code": "package_manifest_too_large",
                            "message": (
                                "Workspace package manifest was too large to record "
                                "as inventory evidence."
                            ),
                            "path": path.relative_to(checkout).as_posix(),
                        }
                    )
                    continue
                matches.add(path.relative_to(checkout).as_posix())
    return matches


def unsafe_workspace_pattern(pattern: str) -> bool:
    if not pattern or pattern.startswith("!") or pattern.startswith("/"):
        return True
    return any(part == ".." for part in Path(pattern).parts)


def package_record(
    *,
    checkout: Path,
    manifest_path: str,
    profile: dict[str, Any],
    namespace: str,
    workspace_paths: set[str],
    max_file_bytes: int,
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any]:
    absolute = checkout / manifest_path
    package = package_metadata(absolute, diagnostics, max_file_bytes)
    role = package_role(manifest_path, package, workspace_paths)
    subject = package_subject(manifest_path, package, role, namespace)
    return {
        "manifestPath": manifest_path,
        "sourceTargetPath": source_target_path(manifest_path),
        "ecosystem": profile.get("ecosystem", package_ecosystem(manifest_path)),
        "packageManager": profile.get("packageManager", package_manager(manifest_path)),
        "name": package.get("name"),
        "version": package.get("version"),
        "proposedSpecpmPackageId": f"{namespace}.{subject}",
        "role": role,
        "evidenceReferences": [
            evidence_reference(absolute, manifest_path, kind="package_manifest")
        ],
    }


def package_metadata(
    path: Path, diagnostics: list[dict[str, Any]], max_file_bytes: int
) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if path.stat().st_size > max_file_bytes:
        diagnostics.append(
            {
                "level": "warning",
                "code": "package_manifest_too_large",
                "message": "Package manifest was too large to parse for package metadata.",
                "path": path.name,
            }
        )
        return {}
    if path.name == "package.json":
        parsed = parse_package_json(path.read_text(encoding="utf-8"))
        return parsed if parsed is not None else {}
    return {}


def package_role(manifest_path: str, package: dict[str, Any], workspace_paths: set[str]) -> str:
    name = str(package.get("name") or "").lower()
    subject = subject_slug(name, manifest_path)
    if manifest_path in workspace_paths:
        return "workspace"
    if subject in {"react", "react-flow"} or "react" in subject.split("-"):
        return "react_binding"
    if subject in {"svelte", "svelte-flow"} or "svelte" in subject.split("-"):
        return "svelte_binding"
    if subject in {"core", "system", "runtime"}:
        return "core_runtime"
    return "member_package"


def package_subject(manifest_path: str, package: dict[str, Any], role: str, namespace: str) -> str:
    if role == "workspace":
        return "workspace"
    subject = subject_slug(str(package.get("name") or ""), manifest_path)
    if subject == namespace:
        return "system"
    return subject or "package"


def subject_slug(name: str, manifest_path: str) -> str:
    if name:
        subject = name.split("/")[-1]
    else:
        parent = Path(manifest_path).parent
        subject = parent.name if parent.as_posix() != "." else Path(manifest_path).stem
    return specpm_segment(subject)


def proposed_namespace(repository: dict[str, Any]) -> str:
    package_id = repository.get("packageId")
    if isinstance(package_id, str) and package_id.strip():
        return specpm_segment(package_id.split(".", 1)[0])
    repository_id = repository.get("id")
    if isinstance(repository_id, str) and repository_id.strip():
        return specpm_segment(repository_id)
    return specpm_segment(Path(str(repository.get("repository", "workspace"))).stem)


def specpm_segment(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "package"


def deduplicate_proposed_ids(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for record in records:
        proposed = str(record["proposedSpecpmPackageId"])
        candidate = proposed
        if candidate in seen:
            suffix = specpm_segment(record["sourceTargetPath"].replace("/", "-"))
            candidate = f"{proposed}.{suffix}"
        counter = 2
        while candidate in seen:
            candidate = f"{proposed}.{counter}"
            counter += 1
        seen.add(candidate)
        result.append({**record, "proposedSpecpmPackageId": candidate})
    return result


def source_target_path(manifest_path: str) -> str:
    parent = Path(manifest_path).parent.as_posix()
    return "." if parent == "." else parent


def evidence_reference(
    path: Path, public_path: str, kind: str = "workspace_manifest"
) -> dict[str, Any]:
    return {
        "kind": kind,
        "path": public_path,
        "digest": {
            "algorithm": "sha256",
            "value": hashlib.sha256(path.read_bytes()).hexdigest(),
        },
    }


def is_exclude_pattern(pattern: str) -> bool:
    return pattern.startswith("!")


def workspace_ecosystem(path: str) -> str:
    if Path(path).name == "package.json":
        return "npm"
    if Path(path).name == "pnpm-workspace.yaml":
        return "pnpm"
    return "workspace"


def workspace_package_manager(path: str) -> str:
    if Path(path).name == "pnpm-workspace.yaml":
        return "pnpm"
    if Path(path).name == "package.json":
        return "npm"
    return "unknown"


def package_ecosystem(path: str) -> str:
    if Path(path).name == "package.json":
        return "npm"
    return "unknown"


def package_manager(path: str) -> str:
    if Path(path).name == "package.json":
        return "npm"
    return "unknown"


def is_inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True
