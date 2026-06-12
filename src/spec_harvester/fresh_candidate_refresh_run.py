from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.package_set_drafter import (
    PACKAGE_SET_DRAFT_API_VERSION,
    PACKAGE_SET_DRAFT_FILENAME,
    PACKAGE_SET_DRAFT_KIND,
)
from spec_harvester.producer_receipt import digest_record, sha256_file

FRESH_CANDIDATE_REFRESH_RUN_API_VERSION = "spec-harvester.fresh-candidate-refresh-run/v0"
FRESH_CANDIDATE_REFRESH_RUN_KIND = "SpecHarvesterFreshCandidateRefreshRun"
FRESH_CANDIDATE_REFRESH_RUN_SCHEMA_VERSION = 1
FRESH_GENERATED_ROOT_LAYOUT = "specpm-public-index-generated-root/v0"
FRESH_GENERATED_PACKAGE_TEMPLATE = "<package_id>/<version>"


@dataclass(frozen=True)
class FreshCandidateRefreshRunOptions:
    bundle_set: Path
    fresh_generated_root: Path
    source_repository: str | None = None
    source_revision: str | None = None
    run_label: str = "local-refresh-evaluation"


def build_fresh_candidate_refresh_run(
    options: FreshCandidateRefreshRunOptions,
) -> dict[str, Any]:
    bundle_set = options.bundle_set.resolve(strict=False)
    fresh_root = options.fresh_generated_root.resolve(strict=False)
    if not bundle_set.is_dir():
        raise ValueError(f"Package-set directory does not exist: {bundle_set}")

    draft = read_json_object(bundle_set / PACKAGE_SET_DRAFT_FILENAME)
    check_package_set_draft_identity(draft)

    source = source_record(draft, options)
    packages = prepared_packages(bundle_set, fresh_root, draft)
    package_set_id = package_set_subject(packages)
    run_basis = {
        "source": source,
        "runLabel": options.run_label,
        "packages": [
            {
                "packageId": item["packageId"],
                "version": item["version"],
                "contractFiles": item["contractFiles"],
            }
            for item in packages
        ],
    }

    return {
        "apiVersion": FRESH_CANDIDATE_REFRESH_RUN_API_VERSION,
        "kind": FRESH_CANDIDATE_REFRESH_RUN_KIND,
        "schemaVersion": FRESH_CANDIDATE_REFRESH_RUN_SCHEMA_VERSION,
        "status": "prepared",
        "runId": f"fresh-candidate-refresh-{canonical_digest(run_basis)[:16]}",
        "runLabel": options.run_label,
        "source": source,
        "packageSet": {
            "id": package_set_id,
            "candidateCount": len(packages),
            "memberPackageIds": [item["packageId"] for item in packages],
        },
        "bundleSet": {
            "path": str(bundle_set),
            "packageSetDraft": PACKAGE_SET_DRAFT_FILENAME,
        },
        "freshGeneratedRoot": {
            "path": str(fresh_root),
            "layout": FRESH_GENERATED_ROOT_LAYOUT,
            "packagePathTemplate": FRESH_GENERATED_PACKAGE_TEMPLATE,
        },
        "packages": packages,
        "specpmConsumer": specpm_consumer_record(
            fresh_root=fresh_root,
            package_set_id=package_set_id,
            packages=packages,
            source=source,
            run_label=options.run_label,
        ),
        "authority": {
            "producerEvidenceAuthority": "evidence_only",
            "registryAuthority": "SpecPM maintainer review",
            "noRegistryMutation": True,
        },
        "nonGoals": [
            "specpm_acceptance",
            "registry_publication",
            "curated_artifact_mutation",
            "source_repository_execution",
            "package_manager_execution",
        ],
    }


def write_fresh_candidate_refresh_run(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(payload), encoding="utf-8")


def prepared_packages(
    bundle_set: Path,
    fresh_root: Path,
    draft: dict[str, Any],
) -> list[dict[str, Any]]:
    packages: list[dict[str, Any]] = []
    for candidate in sorted(candidate_records(draft), key=candidate_sort_key):
        candidate_dir = safe_bundle_dir(bundle_set, candidate["candidatePath"])
        manifest = read_yaml_object(candidate_dir / "specpm.yaml")
        metadata = manifest.get("metadata")
        if not isinstance(metadata, dict):
            raise ValueError(f"Candidate manifest lacks metadata object: {candidate_dir}")
        package_id = str(metadata.get("id") or "")
        version = str(metadata.get("version") or "")
        if not package_id:
            raise ValueError(f"Candidate manifest lacks metadata.id: {candidate_dir}")
        if not version:
            raise ValueError(f"Candidate manifest lacks metadata.version: {candidate_dir}")
        if package_id != candidate["packageId"]:
            raise ValueError(
                f"Candidate packageId mismatch: draft has {candidate['packageId']!r}, "
                f"manifest has {package_id!r}"
            )
        validate_single_path_segment(package_id, "package id")
        validate_single_path_segment(version, "version")

        artifact_dir = fresh_root / package_id / version
        if artifact_dir.exists():
            shutil.rmtree(artifact_dir)
        artifact_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(candidate_dir, artifact_dir)
        contract_files = contract_file_records(fresh_root, artifact_dir)
        packages.append(
            {
                "packageId": package_id,
                "version": version,
                "role": candidate.get("role", ""),
                "sourceCandidatePath": candidate["candidatePath"],
                "artifactPath": artifact_dir.relative_to(fresh_root).as_posix(),
                "manifestPath": (artifact_dir / "specpm.yaml").relative_to(fresh_root).as_posix(),
                "contractFiles": contract_files,
            }
        )
    return packages


def specpm_consumer_record(
    *,
    fresh_root: Path,
    package_set_id: str,
    packages: list[dict[str, Any]],
    source: dict[str, str],
    run_label: str,
) -> dict[str, Any]:
    versions = sorted({item["version"] for item in packages})
    version = versions[0] if len(versions) == 1 else ""
    package_ids = [item["packageId"] for item in packages]
    arguments: dict[str, Any] = {
        "freshGeneratedRoot": str(fresh_root),
        "packages": package_ids,
        "packageId": package_set_id,
        "scope": "package_set",
        "sourceRepository": source.get("repository", ""),
        "sourceRevision": source.get("revision", ""),
        "runLabel": run_label,
    }
    if version:
        arguments["version"] = version
    if len(versions) > 1:
        arguments["versions"] = {item["packageId"]: item["version"] for item in packages}
    return {
        "command": "specpm producer-bundle prepare-refresh-decision",
        "arguments": arguments,
        "expectedArtifacts": [
            "refresh-decision.json",
            "prepare-report.json",
            "preflight-report.json",
        ],
        "contract": (
            "SpecPM compares only contract-bearing generated files from "
            "<package_id>/<version>/specpm.yaml and specs/*.spec.yaml."
        ),
    }


def source_record(
    draft: dict[str, Any],
    options: FreshCandidateRefreshRunOptions,
) -> dict[str, str]:
    draft_source = draft.get("source")
    if not isinstance(draft_source, dict):
        draft_source = {}
    repository = options.source_repository or string_value(draft_source.get("repository"))
    revision = (
        options.source_revision
        or string_value(draft_source.get("exactRevision"))
        or string_value(draft_source.get("revision"))
    )
    if not revision:
        raise ValueError(
            "Source revision is required; pass --source-revision or use a package-set draft "
            "with source.exactRevision."
        )
    return {
        "repository": repository,
        "revision": revision,
        "revisionAuthority": string_value(draft_source.get("revisionAuthority")),
    }


def contract_file_records(fresh_root: Path, artifact_dir: Path) -> list[dict[str, Any]]:
    paths = [artifact_dir / "specpm.yaml", *sorted((artifact_dir / "specs").glob("*.spec.yaml"))]
    records: list[dict[str, Any]] = []
    for path in paths:
        if not path.is_file():
            continue
        role = "manifest" if path.name == "specpm.yaml" else "boundary_spec"
        records.append(
            {
                "path": path.relative_to(fresh_root).as_posix(),
                "role": role,
                "digest": digest_record(sha256_file(path)),
            }
        )
    if not any(item["role"] == "manifest" for item in records):
        raise ValueError(f"Prepared package lacks specpm.yaml: {artifact_dir}")
    if not any(item["role"] == "boundary_spec" for item in records):
        raise ValueError(f"Prepared package lacks specs/*.spec.yaml: {artifact_dir}")
    return records


def candidate_records(draft: dict[str, Any]) -> list[dict[str, str]]:
    raw = draft.get("candidates")
    if not isinstance(raw, list):
        raise ValueError("Package-set draft candidates must be a list")
    records: list[dict[str, str]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"Package-set candidate at index {index} must be an object")
        package_id = string_value(item.get("packageId"))
        candidate_path = string_value(item.get("candidatePath"))
        if not package_id or not candidate_path:
            raise ValueError(
                f"Package-set candidate at index {index} lacks packageId/candidatePath"
            )
        records.append(
            {
                "packageId": package_id,
                "candidatePath": candidate_path,
                "role": string_value(item.get("role")),
            }
        )
    return records


def package_set_subject(packages: list[dict[str, Any]]) -> str:
    workspace = next((item for item in packages if item.get("role") == "workspace"), None)
    if workspace is not None:
        return str(workspace["packageId"])
    return str(packages[0]["packageId"]) if packages else "package-set"


def candidate_sort_key(candidate: dict[str, str]) -> tuple[int, str]:
    return (0 if candidate.get("role") == "workspace" else 1, candidate["packageId"])


def safe_bundle_dir(bundle_set: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise ValueError(f"Unsafe package-set candidate path: {relative!r}")
    candidate = (bundle_set / relative).resolve(strict=False)
    try:
        candidate.relative_to(bundle_set.resolve(strict=False))
    except ValueError as exc:
        raise ValueError(f"Package-set candidate path escapes bundle root: {relative!r}") from exc
    if not candidate.is_dir():
        raise ValueError(f"Package-set candidate directory does not exist: {relative}")
    return candidate


def validate_single_path_segment(value: str, label: str) -> None:
    if value in {"", ".", ".."} or "/" in value or "\\" in value:
        raise ValueError(f"Unsafe {label} for generated-root path segment: {value!r}")


def check_package_set_draft_identity(draft: dict[str, Any]) -> None:
    expected = {
        "apiVersion": PACKAGE_SET_DRAFT_API_VERSION,
        "kind": PACKAGE_SET_DRAFT_KIND,
        "schemaVersion": 1,
    }
    for key, value in expected.items():
        if draft.get(key) != value:
            raise ValueError(f"{PACKAGE_SET_DRAFT_FILENAME} {key} must be {value!r}")


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read JSON artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON artifact {path}: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return value


def read_yaml_object(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read YAML artifact: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML artifact: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"YAML artifact must be an object: {path}")
    return value


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def canonical_digest(payload: dict[str, Any]) -> str:
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    import hashlib

    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""
