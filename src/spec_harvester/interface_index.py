from __future__ import annotations

import json
import re
from typing import Any

PUBLIC_INTERFACE_INDEX_KIND = "SpecHarvesterPublicInterfaceIndex"
PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION = 1

ALLOWED_ANALYZER_EXECUTIONS = {"none", "metadata_tool_only", "build_tool_sandboxed"}
ALLOWED_NETWORK_ACCESS = {"none"}
ALLOWED_PACKAGE_SCRIPT_MODES = {"not_run"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_INDEX_STATUSES = {"complete", "partial", "failed"}
ALLOWED_SYMBOL_KINDS = {
    "function",
    "class",
    "struct",
    "enum",
    "interface",
    "type",
    "constant",
    "variable",
    "unknown",
}
ALLOWED_DIAGNOSTIC_LEVELS = {"info", "warning", "error"}

SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def new_public_interface_index(
    *,
    source_revision: str | None = None,
    analyzers: list[dict[str, Any]] | None = None,
    packages: list[dict[str, Any]] | None = None,
    diagnostics: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    analyzer_records = list(analyzers or [])
    package_records = list(packages or [])
    diagnostic_records = list(diagnostics or [])
    return {
        "schemaVersion": PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION,
        "kind": PUBLIC_INTERFACE_INDEX_KIND,
        "sourceRevision": source_revision,
        "analyzers": analyzer_records,
        "packages": package_records,
        "diagnostics": diagnostic_records,
        "summary": summarize_public_interface(package_records, diagnostic_records),
    }


def analyzer_record(
    analyzer_id: str,
    version: str,
    *,
    execution: str = "none",
    network_access: str = "none",
    package_scripts: str = "not_run",
    confidence: str = "medium",
) -> dict[str, Any]:
    return {
        "id": analyzer_id,
        "version": version,
        "execution": execution,
        "networkAccess": network_access,
        "packageScripts": package_scripts,
        "confidence": confidence,
    }


def evidence_record(path: str, sha256: str) -> dict[str, str]:
    return {"path": path, "sha256": sha256}


def render_public_interface_index_json(index: dict[str, Any]) -> str:
    validate_public_interface_index(index)
    return json.dumps(index, indent=2, sort_keys=True) + "\n"


def validate_public_interface_index(index: dict[str, Any]) -> None:
    errors = public_interface_index_errors(index)
    if errors:
        raise ValueError("Invalid PublicInterfaceIndex: " + "; ".join(errors))


def public_interface_index_errors(index: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(index, dict):
        return ["index must be an object"]

    if index.get("kind") != PUBLIC_INTERFACE_INDEX_KIND:
        errors.append(f"kind must be {PUBLIC_INTERFACE_INDEX_KIND}")
    if index.get("schemaVersion") != PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION:
        errors.append(f"schemaVersion must be {PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION}")

    source_revision = index.get("sourceRevision")
    if source_revision is not None and not isinstance(source_revision, str):
        errors.append("sourceRevision must be a string or null")

    analyzers = require_list(index, "analyzers", errors)
    for analyzer_index, analyzer in enumerate(analyzers):
        validate_analyzer(analyzer, f"analyzers[{analyzer_index}]", errors)

    packages = require_list(index, "packages", errors)
    for package_index, package in enumerate(packages):
        validate_package(package, f"packages[{package_index}]", errors)

    diagnostics = require_list(index, "diagnostics", errors)
    for diagnostic_index, diagnostic in enumerate(diagnostics):
        validate_diagnostic(diagnostic, f"diagnostics[{diagnostic_index}]", errors)

    expected_summary = summarize_public_interface(packages, diagnostics)
    if index.get("summary") != expected_summary:
        errors.append(f"summary must equal {expected_summary}")

    return errors


def summarize_public_interface(
    packages: list[Any],
    diagnostics: list[Any],
) -> dict[str, int]:
    entrypoint_count = 0
    symbol_count = 0
    for package in packages:
        if not isinstance(package, dict):
            continue
        entrypoints = package.get("entrypoints")
        if not isinstance(entrypoints, list):
            continue
        entrypoint_count += len(entrypoints)
        for entrypoint in entrypoints:
            if isinstance(entrypoint, dict) and isinstance(entrypoint.get("symbols"), list):
                symbol_count += len(entrypoint["symbols"])
    return {
        "status": public_interface_status(packages, diagnostics),
        "packageCount": len(packages),
        "entrypointCount": entrypoint_count,
        "symbolCount": symbol_count,
        "diagnosticCount": len(diagnostics),
    }


def public_interface_status(packages: list[Any], diagnostics: list[Any]) -> str:
    if not diagnostics:
        return "complete"
    if packages:
        return "partial"
    return "failed"


def require_list(record: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = record.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return []
    return value


def validate_analyzer(record: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{prefix} must be an object")
        return
    require_non_empty_string(record, "id", prefix, errors)
    require_non_empty_string(record, "version", prefix, errors)
    require_allowed(record, "execution", ALLOWED_ANALYZER_EXECUTIONS, prefix, errors)
    require_allowed(record, "networkAccess", ALLOWED_NETWORK_ACCESS, prefix, errors)
    require_allowed(record, "packageScripts", ALLOWED_PACKAGE_SCRIPT_MODES, prefix, errors)
    require_allowed(record, "confidence", ALLOWED_CONFIDENCE, prefix, errors)


def validate_package(record: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{prefix} must be an object")
        return
    require_non_empty_string(record, "id", prefix, errors)
    require_non_empty_string(record, "path", prefix, errors)
    if "language" in record and not isinstance(record["language"], str):
        errors.append(f"{prefix}.language must be a string")
    entrypoints = record.get("entrypoints")
    if not isinstance(entrypoints, list):
        errors.append(f"{prefix}.entrypoints must be a list")
        return
    for entrypoint_index, entrypoint in enumerate(entrypoints):
        validate_entrypoint(entrypoint, f"{prefix}.entrypoints[{entrypoint_index}]", errors)


def validate_entrypoint(record: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{prefix} must be an object")
        return
    require_non_empty_string(record, "path", prefix, errors)
    symbols = record.get("symbols")
    if not isinstance(symbols, list):
        errors.append(f"{prefix}.symbols must be a list")
        return
    for symbol_index, symbol in enumerate(symbols):
        validate_symbol(symbol, f"{prefix}.symbols[{symbol_index}]", errors)


def validate_symbol(record: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{prefix} must be an object")
        return
    require_non_empty_string(record, "name", prefix, errors)
    require_allowed(record, "kind", ALLOWED_SYMBOL_KINDS, prefix, errors)
    require_non_empty_string(record, "visibility", prefix, errors)
    for optional_key in ("signature", "doc"):
        if optional_key in record and not isinstance(record[optional_key], str):
            errors.append(f"{prefix}.{optional_key} must be a string")
    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        errors.append(f"{prefix}.evidence must be an object")
        return
    validate_evidence(evidence, f"{prefix}.evidence", errors)


def validate_diagnostic(record: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{prefix} must be an object")
        return
    require_allowed(record, "level", ALLOWED_DIAGNOSTIC_LEVELS, prefix, errors)
    require_non_empty_string(record, "message", prefix, errors)
    if "path" in record and (not isinstance(record["path"], str) or not record["path"].strip()):
        errors.append(f"{prefix}.path must be non-empty when present")
    evidence = record.get("evidence")
    if evidence is not None:
        if not isinstance(evidence, dict):
            errors.append(f"{prefix}.evidence must be an object")
        else:
            validate_evidence(evidence, f"{prefix}.evidence", errors)


def validate_evidence(record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    path = record.get("path")
    if not isinstance(path, str) or not path.strip():
        errors.append(f"{prefix}.path must be non-empty")
    sha256 = record.get("sha256")
    if not isinstance(sha256, str) or not SHA256_RE.match(sha256):
        errors.append(f"{prefix}.sha256 must be a sha256 hex digest")


def require_non_empty_string(
    record: dict[str, Any],
    key: str,
    prefix: str,
    errors: list[str],
) -> None:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}.{key} must be non-empty")


def require_allowed(
    record: dict[str, Any],
    key: str,
    allowed: set[str],
    prefix: str,
    errors: list[str],
) -> None:
    value = record.get(key)
    if value not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        errors.append(f"{prefix}.{key} must be one of: {allowed_values}")
