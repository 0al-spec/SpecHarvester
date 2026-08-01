from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

PROFILE_API_VERSION = "spec-harvester.semantic-product-profile/v0"
PROFILE_KIND = "SpecHarvesterSemanticProductProfile"
PROFILE_FILENAME = "semantic-product-profile.json"


def build_semantic_product_profile(
    *,
    repository_id: str,
    candidate_id: str,
    harvest: dict[str, Any],
    root_document: dict[str, Any],
    package_document: dict[str, Any] | None = None,
    manifest_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not repository_id or not candidate_id or not isinstance(harvest, dict):
        raise ValueError("semantic product profile identity is invalid")
    source = harvest.get("source") if isinstance(harvest.get("source"), dict) else {}
    target = source.get("target") if isinstance(source.get("target"), dict) else {}
    project = (
        harvest.get("projectProfile") if isinstance(harvest.get("projectProfile"), dict) else {}
    )
    package = _package_metadata(harvest)
    manifest = dict(manifest_metadata or {})
    repository_url = str(source.get("repository") or "")
    owner, name = _repository_coordinates(repository_url)
    target_path = _safe_relative(str(target.get("path") or "."))
    documents = [_document_binding(root_document, "repository_root")]
    if package_document is not None:
        documents.append(_document_binding(package_document, "package_local"))
    profile: dict[str, Any] = {
        "apiVersion": PROFILE_API_VERSION,
        "kind": PROFILE_KIND,
        "schemaVersion": 1,
        "authority": "deterministic_untrusted_metadata_projection",
        "repository": {
            "id": repository_id,
            "url": repository_url,
            "revision": str(source.get("revision") or ""),
            "owner": owner,
            "name": name,
            "evidencePaths": ["harvest.json"],
        },
        "package": {
            "candidateId": candidate_id,
            "role": "repository_root" if target_path == "." else "member_package",
            "targetKind": str(target.get("kind") or "unknown"),
            "targetPath": target_path,
            "targetLabel": str(target.get("label") or ""),
            "name": str(manifest.get("name") or package.get("name") or ""),
            "description": str(manifest.get("description") or package.get("description") or ""),
            "manifestPath": _optional_safe_relative(
                str(manifest.get("sourcePath") or _manifest_path(project) or "")
            ),
            "keywords": _keywords(manifest.get("keywords")),
            "evidencePaths": ["harvest.json"],
        },
        "technology": {
            "languages": _technology_entries(project.get("languages")),
            "ecosystems": _technology_entries(project.get("ecosystems")),
            "analyzerSignals": sorted(
                {
                    str(item.get("id"))
                    for item in project.get("analyzerPlan", [])
                    if isinstance(item, dict) and item.get("id")
                }
            ),
        },
        "documents": documents,
        "sourceBindings": [
            {
                "sourcePath": "harvest.json",
                "sha256": str(root_document.get("harvestSha256") or ""),
            },
            *[
                {
                    "sourcePath": item["sourcePath"],
                    "sha256": item["sha256"],
                }
                for item in documents
            ],
        ],
        "executionBoundary": {
            "repositoryCodeExecuted": False,
            "packageManagerInvoked": False,
            "networkAccessed": False,
            "providerInvoked": False,
            "materializationPerformed": False,
        },
    }
    if manifest.get("sha256"):
        profile["package"]["manifestSha256"] = manifest["sha256"]
        profile["sourceBindings"].append(
            {"sourcePath": profile["package"]["manifestPath"], "sha256": manifest["sha256"]}
        )
    profile["profileSha256"] = _digest_without(profile, "profileSha256")
    validate_semantic_product_profile(profile)
    return profile


def validate_semantic_product_profile(profile: dict[str, Any]) -> None:
    if (
        not isinstance(profile, dict)
        or profile.get("apiVersion") != PROFILE_API_VERSION
        or profile.get("kind") != PROFILE_KIND
        or profile.get("schemaVersion") != 1
        or profile.get("authority") != "deterministic_untrusted_metadata_projection"
    ):
        raise ValueError("semantic product profile identity is invalid")
    if profile.get("profileSha256") != _digest_without(profile, "profileSha256"):
        raise ValueError("semantic product profile digest is stale")
    repository = profile.get("repository")
    package = profile.get("package")
    documents = profile.get("documents")
    source_bindings = profile.get("sourceBindings")
    if (
        not isinstance(repository, dict)
        or not isinstance(repository.get("id"), str)
        or not repository["id"]
        or not isinstance(package, dict)
        or not isinstance(package.get("candidateId"), str)
        or not package["candidateId"]
        or not isinstance(documents, list)
        or not documents
        or not isinstance(source_bindings, list)
        or not source_bindings
    ):
        raise ValueError("semantic product profile content is malformed")
    _safe_relative(str(package.get("targetPath") or "."))
    _optional_safe_relative(str(package.get("manifestPath") or ""))
    bindings: set[tuple[str, str]] = set()
    binding_paths: set[str] = set()
    for item in source_bindings:
        if not isinstance(item, dict):
            raise ValueError("semantic product profile source binding is malformed")
        source_path = _safe_relative(str(item.get("sourcePath") or ""))
        sha256 = item.get("sha256")
        if not _sha256(sha256) or source_path in binding_paths:
            raise ValueError("semantic product profile source binding is malformed")
        bindings.add((source_path, sha256))
        binding_paths.add(source_path)
    for item in documents:
        if not isinstance(item, dict) or item.get("untrusted") is not True:
            raise ValueError("semantic product profile document binding is malformed")
        _safe_relative(str(item.get("evidencePath") or ""))
        source_path = _safe_relative(str(item.get("sourcePath") or ""))
        if (
            not _sha256(item.get("sha256"))
            or not isinstance(item.get("byteCount"), int)
            or item["byteCount"] < 0
            or (source_path, item["sha256"]) not in bindings
        ):
            raise ValueError("semantic product profile document digest is invalid")
    manifest_sha256 = package.get("manifestSha256")
    if manifest_sha256 is not None and (
        not package.get("manifestPath")
        or not _sha256(manifest_sha256)
        or (package["manifestPath"], manifest_sha256) not in bindings
    ):
        raise ValueError("semantic product profile manifest binding is invalid")


def write_semantic_product_profile(path: Path, profile: dict[str, Any]) -> None:
    validate_semantic_product_profile(profile)
    path.write_text(json.dumps(profile, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _package_metadata(harvest: dict[str, Any]) -> dict[str, Any]:
    for item in harvest.get("files", []):
        if isinstance(item, dict) and isinstance(item.get("package"), dict):
            return item["package"]
    return {}


def _manifest_path(project: dict[str, Any]) -> str:
    for item in project.get("manifests", []):
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            return item["path"]
    return ""


def _technology_entries(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [
        {
            key: item[key]
            for key in ("id", "confidence", "language", "packageManager", "evidencePaths")
            if key in item
        }
        for item in value[:32]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]


def _document_binding(value: dict[str, Any], role: str) -> dict[str, Any]:
    binding = {
        "role": role,
        "evidencePath": _safe_relative(str(value.get("evidencePath") or "")),
        "sourcePath": _safe_relative(str(value.get("sourcePath") or "")),
        "sha256": value.get("sha256"),
        "byteCount": value.get("byteCount"),
        "untrusted": True,
    }
    if not _sha256(binding["sha256"]) or not isinstance(binding["byteCount"], int):
        raise ValueError("semantic product profile document digest is invalid")
    return binding


def _repository_coordinates(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if parsed.hostname == "github.com" and len(parts) >= 2:
        return parts[0], parts[1].removesuffix(".git")
    return "", ""


def _keywords(value: Any) -> list[str]:
    values = value if isinstance(value, list) else [value] if isinstance(value, str) else []
    return sorted({item.strip()[:80] for item in values if isinstance(item, str) and item.strip()})[
        :32
    ]


def _safe_relative(value: str) -> str:
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe semantic product profile path: {value}")
    return path.as_posix()


def _optional_safe_relative(value: str) -> str:
    return _safe_relative(value) if value else ""


def _sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _digest_without(value: dict[str, Any], key: str) -> str:
    return hashlib.sha256(
        json.dumps(
            {name: item for name, item in value.items() if name != key},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
