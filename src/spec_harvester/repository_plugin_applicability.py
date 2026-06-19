from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

API_VERSION = "spec-harvester.repository-plugin-applicability/v0"
KIND = "SpecHarvesterRepositoryPluginApplicabilityReport"
SCHEMA_VERSION = 1
AUTHORITY = "producer_plugin_applicability_only"

REGISTRY_API_VERSION = "spec-harvester.repository-plugins/v0"
REGISTRY_KIND = "SpecHarvesterRepositoryPluginRegistry"
REGISTRY_AUTHORITY = "producer_plugin_registry_only"

STATIC_EVIDENCE_API_VERSION = "spec-harvester.repository-plugin-static-evidence/v0"
STATIC_EVIDENCE_KIND = "SpecHarvesterRepositoryPluginStaticEvidenceEnvelope"
STATIC_EVIDENCE_AUTHORITY = "producer_plugin_static_evidence_only"

PLUGIN_OUTPUT_AUTHORITY = "producer_side_evidence_only"

DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")

NON_AUTHORITY_STATEMENTS = [
    "does_not_load_third_party_plugin_code",
    "does_not_execute_plugins",
    "does_not_run_plugin_code",
    "does_not_clone_or_fetch_repositories",
    "does_not_install_dependencies",
    "does_not_execute_harvested_code",
    "does_not_read_repository_source_files",
    "does_not_invoke_package_managers",
    "does_not_run_ai",
    "does_not_change_parser_profile_behavior",
    "does_not_change_repository_profile_scoring",
    "does_not_accept_packages",
    "does_not_accept_relations",
    "does_not_publish_registry_metadata",
    "does_not_seed_baselines",
    "does_not_remove_preview_only",
    "does_not_treat_plugin_evidence_as_registry_truth",
    "does_not_treat_plugin_decisions_as_registry_truth",
    "does_not_treat_plugin_output_as_registry_truth",
    "does_not_treat_ai_output_as_registry_truth",
]


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def write_repository_plugin_applicability_report(
    path: Path,
    payload: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def evaluate_repository_plugin_applicability(
    registry: dict[str, Any],
    static_evidence: dict[str, Any],
) -> dict[str, Any]:
    validate_registry(registry)
    validate_static_evidence(static_evidence)

    available_kinds = string_set(static_evidence.get("evidenceKinds"))
    evidence_by_kind = evidence_records_by_kind(static_evidence)
    selected_plugin_ids: set[str] = set()
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    fallback: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for plugin in plugin_records(registry):
        required_kinds = string_list(plugin.get("inputEvidenceKinds"))
        missing_kinds = [kind for kind in required_kinds if kind not in available_kinds]
        evidence_paths = evidence_paths_for(required_kinds, evidence_by_kind)
        output_kinds = string_list(plugin.get("outputArtifactKinds"))
        conflicts = [
            plugin_id
            for plugin_id in string_list(plugin.get("conflictsWith"))
            if plugin_id in selected_plugin_ids
        ]

        if conflicts:
            decision = decision_record(
                plugin,
                decision="rejected",
                confidence="low",
                reason_codes=["conflicting_plugin_selected"],
                evidence_paths=evidence_paths,
                output_artifact_kinds=output_kinds,
                extra={"conflictingPluginIds": conflicts},
            )
            rejected.append(decision)
            diagnostics.append(
                diagnostic_record(
                    "warning",
                    "plugin_rejected_conflict",
                    plugin,
                    "Plugin rejected because a conflicting plugin was already selected.",
                    evidence_paths,
                    reason_codes=decision["reasonCodes"],
                )
            )
            continue

        if not missing_kinds:
            decision = decision_record(
                plugin,
                decision="selected",
                confidence="high",
                reason_codes=["required_static_evidence_available"],
                evidence_paths=evidence_paths,
                output_artifact_kinds=output_kinds,
            )
            selected.append(decision)
            selected_plugin_ids.add(decision["pluginId"])
            diagnostics.append(
                diagnostic_record(
                    "info",
                    "plugin_selected",
                    plugin,
                    "Plugin selected because all declared input evidence is available.",
                    evidence_paths,
                    reason_codes=decision["reasonCodes"],
                )
            )
            continue

        fallback_behavior = fallback_behavior_record(plugin)
        fallback_reason = fallback_behavior.get("reasonCode", "missing_required_evidence")
        reason_codes = unique_strings(["missing_required_evidence", str(fallback_reason)])
        extra = {"missingEvidenceKinds": missing_kinds}
        if fallback_behavior.get("decision") == "fallback":
            decision = decision_record(
                plugin,
                decision="fallback",
                confidence="medium",
                reason_codes=reason_codes,
                evidence_paths=evidence_paths,
                output_artifact_kinds=output_kinds,
                extra=extra,
            )
            fallback.append(decision)
            diagnostics.append(
                diagnostic_record(
                    "warning",
                    "plugin_fallback",
                    plugin,
                    "Plugin fallback selected because required input evidence is missing.",
                    evidence_paths,
                    reason_codes=reason_codes,
                    missing_evidence_kinds=missing_kinds,
                )
            )
        else:
            decision = decision_record(
                plugin,
                decision="blocked",
                confidence="blocked",
                reason_codes=reason_codes,
                evidence_paths=evidence_paths,
                output_artifact_kinds=output_kinds,
                extra=extra,
            )
            blocked.append(decision)
            diagnostics.append(
                diagnostic_record(
                    "error",
                    "plugin_blocked_required_evidence_missing",
                    plugin,
                    "Plugin blocked because required input evidence is missing.",
                    evidence_paths,
                    reason_codes=reason_codes,
                    missing_evidence_kinds=missing_kinds,
                )
            )

    static_paths = [record["path"] for record in evidence_by_kind.values()]
    return {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schemaVersion": SCHEMA_VERSION,
        "authority": AUTHORITY,
        "mode": "auto",
        "registry": registry_ref(static_evidence, registry),
        "repository": static_evidence["repository"],
        "staticEvidence": {
            "inputAuthority": static_evidence["inputAuthority"],
            "paths": static_paths,
            "evidenceKinds": list(static_evidence["evidenceKinds"]),
            "signals": list(static_evidence.get("advisorySignals", [])),
        },
        "summary": {
            "selectedCount": len(selected),
            "rejectedCount": len(rejected),
            "fallbackCount": len(fallback),
            "blockedCount": len(blocked),
            "diagnosticCount": len(diagnostics),
        },
        "selectedPlugins": selected,
        "rejectedPlugins": rejected,
        "fallbackPlugins": fallback,
        "blockedPlugins": blocked,
        "diagnostics": diagnostics,
        "sidecarBoundary": {
            "appliedToDrafting": False,
            "registryAuthority": False,
            "evaluatorExecution": "deterministic_static_metadata_only",
        },
        "nonAuthorityStatements": unique_strings(
            [
                *string_list(static_evidence.get("nonAuthorityStatements")),
                *string_list(registry.get("nonAuthorityStatements")),
                *NON_AUTHORITY_STATEMENTS,
            ]
        ),
        "followUp": {
            "cliReportTask": "P39-T4",
            "batchIntegrationTask": "P39-T5",
            "realValidationTask": "P39-T6",
        },
    }


def validate_registry(registry: dict[str, Any]) -> None:
    expected = {
        "apiVersion": REGISTRY_API_VERSION,
        "kind": REGISTRY_KIND,
        "schemaVersion": SCHEMA_VERSION,
        "authority": REGISTRY_AUTHORITY,
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            raise ValueError(f"Unsupported plugin registry {key}: {registry.get(key)!r}")
    plugin_records(registry)


def validate_static_evidence(static_evidence: dict[str, Any]) -> None:
    expected = {
        "apiVersion": STATIC_EVIDENCE_API_VERSION,
        "kind": STATIC_EVIDENCE_KIND,
        "schemaVersion": SCHEMA_VERSION,
        "authority": STATIC_EVIDENCE_AUTHORITY,
    }
    for key, value in expected.items():
        if static_evidence.get(key) != value:
            raise ValueError(
                f"Unsupported static evidence envelope {key}: {static_evidence.get(key)!r}"
            )
    if static_evidence.get("inputAuthority") != "static_local_evidence_only":
        raise ValueError(
            "static evidence envelope inputAuthority must be static_local_evidence_only"
        )
    if not isinstance(static_evidence.get("repository"), dict):
        raise ValueError("static evidence envelope must include repository object")
    evidence_records_by_kind(static_evidence)


def plugin_records(registry: dict[str, Any]) -> list[dict[str, Any]]:
    plugins = registry.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise ValueError("plugin registry must include non-empty plugins array")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for plugin in plugins:
        if not isinstance(plugin, dict):
            raise ValueError("plugin registry plugins must be objects")
        plugin_id = string_field(plugin, "pluginId")
        if plugin_id in seen:
            raise ValueError(f"duplicate pluginId in registry: {plugin_id}")
        seen.add(plugin_id)
        string_field(plugin, "role")
        if plugin.get("authority") != PLUGIN_OUTPUT_AUTHORITY:
            raise ValueError(
                f"plugin {plugin_id} has unsupported authority: {plugin.get('authority')!r}"
            )
        string_list(plugin.get("inputEvidenceKinds"))
        string_list(plugin.get("outputArtifactKinds"))
        records.append(plugin)
    return records


def evidence_records_by_kind(static_evidence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    evidence = static_evidence.get("evidence")
    if not isinstance(evidence, list):
        raise ValueError("static evidence envelope must include evidence array")
    available_kinds = string_set(static_evidence.get("evidenceKinds"))
    records: dict[str, dict[str, Any]] = {}
    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError("static evidence records must be objects")
        kind = string_field(item, "kind")
        path = string_field(item, "path")
        digest = string_field(item, "digest")
        string_field(item, "authority")
        if kind not in available_kinds:
            raise ValueError(f"static evidence kind not declared in evidenceKinds: {kind}")
        if kind in records:
            raise ValueError(f"duplicate static evidence kind: {kind}")
        if not is_safe_relative_path(path):
            raise ValueError(f"unsafe static evidence path: {path}")
        if not DIGEST_PATTERN.match(digest):
            raise ValueError(f"static evidence digest must be sha256:<64 lowercase hex>: {path}")
        records[kind] = item
    return records


def decision_record(
    plugin: dict[str, Any],
    *,
    decision: str,
    confidence: str,
    reason_codes: list[str],
    evidence_paths: list[str],
    output_artifact_kinds: list[str],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "pluginId": plugin["pluginId"],
        "role": plugin["role"],
        "decision": decision,
        "decisionAuthority": AUTHORITY,
        "pluginOutputAuthority": plugin["authority"],
        "confidence": confidence,
        "reasonCodes": reason_codes,
        "evidencePaths": evidence_paths,
        "outputArtifactKinds": output_artifact_kinds,
    }
    if extra:
        record.update(extra)
    return record


def diagnostic_record(
    severity: str,
    code: str,
    plugin: dict[str, Any],
    message: str,
    evidence_paths: list[str],
    *,
    reason_codes: list[str],
    missing_evidence_kinds: list[str] | None = None,
) -> dict[str, Any]:
    record = {
        "severity": severity,
        "code": code,
        "pluginId": plugin["pluginId"],
        "message": message,
        "reasonCodes": reason_codes,
        "evidencePaths": evidence_paths,
    }
    if missing_evidence_kinds:
        record["missingEvidenceKinds"] = missing_evidence_kinds
    return record


def evidence_paths_for(
    evidence_kinds: list[str],
    evidence_by_kind: dict[str, dict[str, Any]],
) -> list[str]:
    paths: list[str] = []
    for kind in evidence_kinds:
        record = evidence_by_kind.get(kind)
        if record is not None:
            paths.append(record["path"])
    return unique_strings(paths)


def fallback_behavior_record(plugin: dict[str, Any]) -> dict[str, Any]:
    fallback_behavior = plugin.get("fallbackBehavior")
    if isinstance(fallback_behavior, dict):
        return fallback_behavior
    return {"decision": "skip", "reasonCode": "missing_required_evidence"}


def registry_ref(static_evidence: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    ref = static_evidence.get("registry")
    if isinstance(ref, dict):
        output = dict(ref)
    else:
        output = {}
    output.setdefault("kind", registry["kind"])
    output.setdefault("authority", registry["authority"])
    return output


def string_field(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"required string field missing: {key}")
    return value


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def string_set(value: Any) -> set[str]:
    values = string_list(value)
    if not values:
        raise ValueError("expected non-empty string array")
    return set(values)


def unique_strings(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def is_safe_relative_path(path: str) -> bool:
    if not path or path.startswith("/") or "\\" in path or "://" in path:
        return False
    parts = path.split("/")
    return all(part not in {"", ".", ".."} for part in parts)
