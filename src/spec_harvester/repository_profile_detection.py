from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.source_manifest import read_repository_source_manifests

API_VERSION = "spec-harvester.repository-profile-detection/v0"
KIND = "SpecHarvesterRepositoryProfileDetection"
AUTHORITY = "producer_profile_selection_only"
SCHEMA_VERSION = 1

PACKAGE_SET_PROFILE_ID = "generic.package_set.v0"
SINGLE_PACKAGE_PROFILE_ID = "generic.single_package.v0"
DOCUMENTATION_SITE_PROFILE_ID = "generic.documentation_site.v0"
GENERIC_FALLBACK_PROFILE_ID = "generic.repository.v0"

NON_AUTHORITY_STATEMENTS = [
    "does_not_clone_or_fetch_repositories",
    "does_not_install_dependencies",
    "does_not_execute_harvested_code",
    "does_not_invoke_package_managers",
    "does_not_run_ai",
    "does_not_draft_packages",
    "does_not_publish_registry_metadata",
    "does_not_accept_packages",
    "does_not_accept_relations",
    "does_not_seed_baselines",
    "does_not_remove_preview_only",
    "does_not_treat_plugin_decisions_as_registry_truth",
    "does_not_treat_ai_output_as_registry_truth",
]

MANIFEST_FILENAMES = {
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "Package.swift",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
}
WORKSPACE_FILENAMES = {
    "workspace.yaml",
    "workspace.yml",
    "pnpm-workspace.yaml",
    "pnpm-workspace.yml",
    "lerna.json",
    "rush.json",
    "turbo.json",
}


@dataclass(frozen=True)
class RepositoryIdentity:
    repository_id: str
    repository_url: str
    ref: str | None
    revision: str | None
    source_manifest_path: str | None = None
    source_manifest_entry_id: str | None = None
    declared_repository_profile: str | None = None


@dataclass(frozen=True)
class RepositoryProfileDetectionOptions:
    repository: RepositoryIdentity
    selection: str = "auto"
    evidence_paths: tuple[str, ...] = ()


def repository_identity_from_source_manifest(
    inputs: Path,
    *,
    source_id: str | None = None,
    declared_repository_profile: str | None = None,
) -> RepositoryIdentity:
    records = read_repository_source_manifests(inputs, include_disabled=True)
    if source_id is None:
        if len(records) != 1:
            raise ValueError("--source-id is required when source manifest has multiple entries")
        record = records[0]
    else:
        matches = [record for record in records if record["id"] == source_id]
        if not matches:
            raise ValueError(f"Source manifest entry not found: {source_id}")
        record = matches[0]

    return RepositoryIdentity(
        repository_id=record["id"],
        repository_url=record["repository"],
        ref=record["ref"],
        revision=record["revision"],
        source_manifest_path=record["sourceManifest"]["path"],
        source_manifest_entry_id=record["id"],
        declared_repository_profile=declared_repository_profile,
    )


def build_repository_profile_detection(
    options: RepositoryProfileDetectionOptions,
) -> dict[str, Any]:
    selection = options.selection.strip()
    if not selection:
        raise ValueError("selection must be non-empty")

    evidence_paths = tuple(normalize_evidence_paths(options.evidence_paths))
    candidates = candidate_profiles(evidence_paths)

    if selection == "none":
        selected_profile_id: str | None = None
        override_source = "operator_disabled"
        confidence = "blocked"
        decision = "disabled"
        reason_codes = ["profile_selection_disabled"]
        diagnostics = [
            diagnostic(
                "info",
                "repository_profile_selection_disabled",
                "Repository profile selection was disabled by operator input.",
                [],
            )
        ]
    elif selection == "auto":
        selected = auto_selected_candidate(candidates)
        selected_profile_id = selected["profileId"] if selected is not None else None
        override_source = "none"
        confidence = selected["confidence"] if selected is not None else "low"
        decision = "selected" if selected is not None else "fallback"
        reason_codes = (
            list(selected["reasonCodes"])
            if selected is not None
            else ["insufficient_high_confidence_profile_evidence"]
        )
        diagnostics = [
            diagnostic(
                "info" if selected is not None else "warning",
                "repository_profile_selected"
                if selected is not None
                else "repository_profile_fallback",
                f"Selected {selected_profile_id} from static repository evidence."
                if selected is not None
                else "Falling back to generic.repository.v0 from static repository evidence.",
                list(selected["evidencePaths"]) if selected is not None else list(evidence_paths),
            )
        ]
    else:
        selected_profile_id = selection
        override_source = "cli"
        confidence = "high"
        decision = "selected"
        reason_codes = ["explicit_cli_profile_override"]
        candidates = ensure_explicit_candidate(candidates, selected_profile_id, evidence_paths)
        diagnostics = [
            diagnostic(
                "info",
                "repository_profile_cli_override",
                f"Selected {selected_profile_id} from explicit CLI profile override.",
                list(evidence_paths),
            )
        ]

    rejected = rejected_profiles(candidates, selected_profile_id)
    return {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schemaVersion": SCHEMA_VERSION,
        "authority": AUTHORITY,
        "repository": repository_payload(options.repository),
        "sourceManifest": source_manifest_payload(options.repository),
        "selection": {
            "mode": selection,
            "overrideSource": override_source,
            "selectedProfileId": selected_profile_id,
            "fallbackProfileId": GENERIC_FALLBACK_PROFILE_ID,
            "confidence": confidence,
            "decision": decision,
            "reasonCodes": reason_codes,
        },
        "candidateProfiles": candidates,
        "rejectedProfiles": rejected,
        "diagnostics": diagnostics,
        "advisoryDownstreamHints": advisory_downstream_hints(evidence_paths, selected_profile_id),
        "nonAuthorityStatements": NON_AUTHORITY_STATEMENTS,
        "followUp": {
            "batchIntegrationTask": "P37-T4",
            "hintVocabularyTask": "P37-T5",
            "crossEcosystemFixturesTask": "P37-T6",
            "realRepositoryValidationTask": "P37-T7",
        },
    }


def write_repository_profile_detection(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_evidence_paths(paths: tuple[str, ...]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for raw_path in paths:
        path = raw_path.strip()
        if not path:
            raise ValueError("evidence paths must be non-empty")
        if "\\" in path:
            raise ValueError(f"evidence path must use forward slashes: {raw_path}")
        pure = Path(path)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError(f"evidence path must be repository-relative: {raw_path}")
        normalized_path = pure.as_posix()
        if normalized_path not in seen:
            normalized.append(normalized_path)
            seen.add(normalized_path)
    return sorted(normalized)


def candidate_profiles(evidence_paths: tuple[str, ...]) -> list[dict[str, Any]]:
    package_set = package_set_candidate(evidence_paths)
    single_package = single_package_candidate(evidence_paths, package_set["confidence"])
    documentation_site = documentation_candidate(evidence_paths, package_set["confidence"])
    return [package_set, single_package, documentation_site]


def package_set_candidate(evidence_paths: tuple[str, ...]) -> dict[str, Any]:
    workspace_paths = [path for path in evidence_paths if is_workspace_path(path)]
    member_manifest_paths = [path for path in evidence_paths if is_member_manifest_path(path)]
    score = 0.92 if workspace_paths and len(member_manifest_paths) >= 2 else 0.35
    if score < 0.9 and (workspace_paths or len(member_manifest_paths) >= 2):
        score = 0.74
    return {
        "profileId": PACKAGE_SET_PROFILE_ID,
        "title": "Generic Package-Set Repository",
        "confidence": confidence_for_score(score),
        "score": score,
        "evidencePaths": workspace_paths + member_manifest_paths,
        "reasonCodes": reason_codes_for_package_set(workspace_paths, member_manifest_paths),
        "conflicts": [] if score >= 0.8 else [SINGLE_PACKAGE_PROFILE_ID],
        "recommendedAction": "select" if score >= 0.8 else "fallback",
    }


def single_package_candidate(
    evidence_paths: tuple[str, ...],
    package_set_confidence: str,
) -> dict[str, Any]:
    root_manifests = [path for path in evidence_paths if is_root_manifest_path(path)]
    score = 0.86 if root_manifests and package_set_confidence != "high" else 0.24
    if root_manifests and package_set_confidence == "high":
        score = 0.54
    return {
        "profileId": SINGLE_PACKAGE_PROFILE_ID,
        "title": "Generic Single-Package Repository",
        "confidence": confidence_for_score(score),
        "score": score,
        "evidencePaths": root_manifests,
        "reasonCodes": reason_codes_for_single_package(root_manifests, package_set_confidence),
        "conflicts": [PACKAGE_SET_PROFILE_ID] if package_set_confidence == "high" else [],
        "recommendedAction": "select" if score >= 0.8 else "fallback",
    }


def documentation_candidate(
    evidence_paths: tuple[str, ...],
    package_set_confidence: str,
) -> dict[str, Any]:
    docs_paths = [path for path in evidence_paths if is_documentation_path(path)]
    score = 0.65 if docs_paths and package_set_confidence != "high" else 0.18
    return {
        "profileId": DOCUMENTATION_SITE_PROFILE_ID,
        "title": "Generic Documentation Site Repository",
        "confidence": confidence_for_score(score),
        "score": score,
        "evidencePaths": docs_paths,
        "reasonCodes": reason_codes_for_documentation_site(docs_paths, package_set_confidence),
        "conflicts": [PACKAGE_SET_PROFILE_ID] if package_set_confidence == "high" else [],
        "recommendedAction": "require_override" if score < 0.8 else "select",
    }


def confidence_for_score(score: float) -> str:
    if score >= 0.8:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"


def reason_codes_for_package_set(
    workspace_paths: list[str],
    member_manifest_paths: list[str],
) -> list[str]:
    reasons: list[str] = []
    if workspace_paths:
        reasons.append("workspace_manifest_present")
    if len(member_manifest_paths) >= 2:
        reasons.append("multiple_member_manifests_present")
    if not reasons:
        reasons.append("missing_package_set_evidence")
    return reasons


def reason_codes_for_single_package(
    root_manifests: list[str],
    package_set_confidence: str,
) -> list[str]:
    if not root_manifests:
        return ["missing_root_manifest"]
    if package_set_confidence == "high":
        return ["root_manifest_present", "member_manifests_make_single_package_incomplete"]
    return ["root_manifest_present"]


def reason_codes_for_documentation_site(
    docs_paths: list[str],
    package_set_confidence: str,
) -> list[str]:
    if not docs_paths:
        return ["missing_documentation_site_evidence"]
    if package_set_confidence == "high":
        return ["documentation_path_present", "package_manifests_are_primary"]
    return ["documentation_path_present"]


def auto_selected_candidate(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    selectable = [
        candidate
        for candidate in candidates
        if candidate["confidence"] == "high" and candidate["recommendedAction"] == "select"
    ]
    if len(selectable) != 1:
        return None
    return selectable[0]


def ensure_explicit_candidate(
    candidates: list[dict[str, Any]],
    selected_profile_id: str,
    evidence_paths: tuple[str, ...],
) -> list[dict[str, Any]]:
    override_candidate = {
        "profileId": selected_profile_id,
        "title": "Explicit CLI Repository Profile",
        "confidence": "high",
        "score": 1.0,
        "evidencePaths": list(evidence_paths),
        "reasonCodes": ["explicit_cli_profile_override"],
        "conflicts": [],
        "recommendedAction": "select",
    }
    for index, candidate in enumerate(candidates):
        if candidate["profileId"] == selected_profile_id:
            updated = dict(override_candidate)
            updated["title"] = candidate["title"]
            return [*candidates[:index], updated, *candidates[index + 1 :]]
    return [
        override_candidate,
        *candidates,
    ]


def rejected_profiles(
    candidates: list[dict[str, Any]],
    selected_profile_id: str | None,
) -> list[dict[str, Any]]:
    rejected: list[dict[str, Any]] = []
    for candidate in candidates:
        if candidate["profileId"] == selected_profile_id:
            continue
        reason_codes = ["not_selected"]
        if candidate["confidence"] != "high":
            reason_codes.append(f"{candidate['confidence']}_confidence")
        if candidate["conflicts"]:
            reason_codes.append("conflicts_with_selected_profile")
        rejected.append({"profileId": candidate["profileId"], "reasonCodes": reason_codes})
    return rejected


def advisory_downstream_hints(
    evidence_paths: tuple[str, ...],
    selected_profile_id: str | None,
) -> list[dict[str, Any]]:
    hints: list[dict[str, Any]] = []
    if selected_profile_id == PACKAGE_SET_PROFILE_ID:
        for path in evidence_paths:
            if is_workspace_path(path):
                hints.append(
                    hint(
                        "package_set_root",
                        workspace_root_for_path(path),
                        "high",
                        ["workspace_manifest_present"],
                    )
                )
            elif is_member_manifest_path(path):
                hints.append(
                    hint(
                        "member_package",
                        str(Path(path).parent.as_posix()),
                        "high",
                        ["member_manifest_present"],
                    )
                )
            elif is_documentation_path(path):
                hints.append(
                    hint(
                        "documentation_source",
                        path.split("/", 1)[0],
                        "medium",
                        ["documentation_path_present"],
                    )
                )
    return unique_hints(hints)


def hint(
    name: str,
    path: str,
    confidence: str,
    reason_codes: list[str],
) -> dict[str, Any]:
    return {
        "hint": name,
        "path": path,
        "confidence": confidence,
        "reasonCodes": reason_codes,
    }


def unique_hints(hints: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for item in hints:
        key = (item["hint"], item["path"])
        if key not in seen:
            unique.append(item)
            seen.add(key)
    return unique


def is_workspace_path(path: str) -> bool:
    return Path(path).name in WORKSPACE_FILENAMES


def workspace_root_for_path(path: str) -> str:
    parent = Path(path).parent.as_posix()
    return "." if parent == "." else parent


def is_root_manifest_path(path: str) -> bool:
    pure = Path(path)
    return len(pure.parts) == 1 and pure.name in MANIFEST_FILENAMES


def is_member_manifest_path(path: str) -> bool:
    pure = Path(path)
    return len(pure.parts) > 1 and pure.name in MANIFEST_FILENAMES


def is_documentation_path(path: str) -> bool:
    return path == "docs" or path.startswith("docs/")


def diagnostic(
    severity: str,
    code: str,
    message: str,
    evidence_paths: list[str],
) -> dict[str, Any]:
    return {
        "severity": severity,
        "code": code,
        "message": message,
        "evidencePaths": evidence_paths,
    }


def repository_payload(repository: RepositoryIdentity) -> dict[str, Any]:
    return {
        "id": repository.repository_id,
        "name": repository.repository_id.rsplit(".", 1)[-1],
        "url": repository.repository_url,
        "ref": repository.ref,
        "revision": repository.revision,
    }


def source_manifest_payload(repository: RepositoryIdentity) -> dict[str, Any]:
    return {
        "path": repository.source_manifest_path,
        "entryId": repository.source_manifest_entry_id or repository.repository_id,
        "declaredRepositoryProfile": repository.declared_repository_profile,
    }
