from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from spec_harvester.go_public_api import analyze_go_public_api
from spec_harvester.interface_index import (
    new_public_interface_index,
    validate_public_interface_index,
)
from spec_harvester.js_ts_public_api import analyze_js_ts_public_api
from spec_harvester.python_public_api import analyze_python_public_api
from spec_harvester.repository_parsing_profile import repository_parsing_profile
from spec_harvester.swift_public_api import analyze_swift_public_api

PUBLIC_INTERFACE_INDEX_FILENAME = "public-interface-index.json"

PYTHON_PROJECT_PROFILE_ANALYZER_ID = "spec_harvester.python_public_api"
JS_TS_PROJECT_PROFILE_ANALYZER_ID = "spec_harvester.js_ts_public_api"
GO_PROJECT_PROFILE_ANALYZER_ID = "spec_harvester.go_public_api"
SWIFT_PROJECT_PROFILE_ANALYZER_ID = "spec_harvester.swift_public_api"
RECOMMENDED_ANALYZER_STATUS = "recommended"

AnalyzerFunction = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class AnalyzerAdapter:
    plan_id: str
    analyze: AnalyzerFunction
    uses_manifest_package_ids: bool = False
    supports_parser_profile: bool = False


ANALYZER_ADAPTERS: dict[str, AnalyzerAdapter] = {
    PYTHON_PROJECT_PROFILE_ANALYZER_ID: AnalyzerAdapter(
        plan_id=PYTHON_PROJECT_PROFILE_ANALYZER_ID,
        analyze=analyze_python_public_api,
        supports_parser_profile=True,
    ),
    JS_TS_PROJECT_PROFILE_ANALYZER_ID: AnalyzerAdapter(
        plan_id=JS_TS_PROJECT_PROFILE_ANALYZER_ID,
        analyze=analyze_js_ts_public_api,
        uses_manifest_package_ids=True,
    ),
    GO_PROJECT_PROFILE_ANALYZER_ID: AnalyzerAdapter(
        plan_id=GO_PROJECT_PROFILE_ANALYZER_ID,
        analyze=analyze_go_public_api,
    ),
    SWIFT_PROJECT_PROFILE_ANALYZER_ID: AnalyzerAdapter(
        plan_id=SWIFT_PROJECT_PROFILE_ANALYZER_ID,
        analyze=analyze_swift_public_api,
    ),
}


def run_project_profile_analyzers(
    *,
    source: Path,
    snapshot: dict[str, Any],
    package_id: str | None = None,
    cache_dir: Path | None = None,
    parser_profile_id: str | None = None,
) -> dict[str, Any]:
    repository_parsing_profile(parser_profile_id)
    plan_entries = project_profile_analyzer_plan(snapshot)
    source_revision = snapshot_source_revision(snapshot)
    indexes: list[dict[str, Any]] = []
    diagnostics: list[dict[str, str]] = []
    skipped_plans: list[dict[str, str]] = []
    executed_analyzer_ids: list[str] = []

    for plan in plan_entries:
        plan_id = str(plan.get("id") or "")
        status = str(plan.get("status") or "")
        if status != RECOMMENDED_ANALYZER_STATUS:
            skipped_plans.append(
                {
                    "id": plan_id,
                    "status": status or "unknown",
                    "reason": "project_profile_plan_not_recommended",
                }
            )
            continue

        adapter = ANALYZER_ADAPTERS.get(plan_id)
        if adapter is None:
            skipped_plans.append(
                {
                    "id": plan_id,
                    "status": status,
                    "reason": "unsupported_project_profile_analyzer",
                }
            )
            continue

        try:
            analyzer_kwargs: dict[str, Any] = {
                "package_id": None if adapter.uses_manifest_package_ids else package_id,
                "source_revision": source_revision,
                "cache_dir": cache_dir,
            }
            if adapter.supports_parser_profile:
                analyzer_kwargs["parser_profile_id"] = parser_profile_id
            index = adapter.analyze(source, **analyzer_kwargs)
        except (OSError, RuntimeError, ValueError) as exc:
            diagnostics.append(
                {
                    "level": "error",
                    "message": f"Analyzer {plan_id} failed: {exc}",
                }
            )
            continue

        validate_public_interface_index(index)
        indexes.append(index)
        executed_analyzer_ids.append(plan_id)

    index = merge_public_interface_indexes(indexes, source_revision=source_revision)
    status = orchestration_status(index, diagnostics, plan_entries, skipped_plans)
    return {
        "status": status,
        "index": index,
        "plannedAnalyzerIds": [str(plan.get("id") or "") for plan in plan_entries],
        "executedAnalyzerIds": sorted(executed_analyzer_ids),
        "parserProfileId": parser_profile_id,
        "skippedAnalyzerPlans": sorted(
            skipped_plans,
            key=lambda item: (item["id"], item["reason"], item["status"]),
        ),
        "diagnostics": sorted(
            diagnostics,
            key=lambda item: (item["level"], item.get("message", "")),
        ),
    }


def project_profile_analyzer_plan(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    profile = snapshot.get("projectProfile")
    if not isinstance(profile, dict):
        return []
    plan = profile.get("analyzerPlan")
    if not isinstance(plan, list):
        return []
    return [
        item
        for item in plan
        if isinstance(item, dict) and isinstance(item.get("id"), str) and item["id"].strip()
    ]


def snapshot_source_revision(snapshot: dict[str, Any]) -> str | None:
    source = snapshot.get("source")
    if not isinstance(source, dict):
        return None
    revision = source.get("revision")
    return revision if isinstance(revision, str) and revision.strip() else None


def merge_public_interface_indexes(
    indexes: list[dict[str, Any]],
    *,
    source_revision: str | None,
) -> dict[str, Any] | None:
    if not indexes:
        return None

    analyzers = [
        analyzer
        for index in indexes
        for analyzer in index.get("analyzers", [])
        if isinstance(analyzer, dict)
    ]
    packages = [
        package
        for index in indexes
        for package in index.get("packages", [])
        if isinstance(package, dict)
    ]
    diagnostics = [
        diagnostic
        for index in indexes
        for diagnostic in index.get("diagnostics", [])
        if isinstance(diagnostic, dict)
    ]
    merged = new_public_interface_index(
        source_revision=source_revision,
        analyzers=sorted(analyzers, key=analyzer_sort_key),
        packages=sorted(packages, key=package_sort_key),
        diagnostics=sorted(diagnostics, key=diagnostic_sort_key),
    )
    validate_public_interface_index(merged)
    return merged


def orchestration_status(
    index: dict[str, Any] | None,
    diagnostics: list[dict[str, str]],
    plan_entries: list[dict[str, Any]],
    skipped_plans: list[dict[str, str]],
) -> str:
    has_orchestration_error = any(diagnostic.get("level") == "error" for diagnostic in diagnostics)
    if index is not None:
        summary = index.get("summary")
        if isinstance(summary, dict) and isinstance(summary.get("status"), str):
            if has_orchestration_error and summary["status"] == "complete":
                return "partial"
            return summary["status"]
        return "partial"
    if has_orchestration_error:
        return "failed"
    if plan_entries or skipped_plans:
        return "skipped"
    return "skipped"


def analyzer_sort_key(analyzer: dict[str, Any]) -> tuple[str, str]:
    return (str(analyzer.get("id") or ""), str(analyzer.get("version") or ""))


def package_sort_key(package: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(package.get("path") or ""),
        str(package.get("language") or ""),
        str(package.get("id") or ""),
    )


def diagnostic_sort_key(diagnostic: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(diagnostic.get("level") or ""),
        str(diagnostic.get("path") or ""),
        str(diagnostic.get("message") or ""),
    )


def interface_index_batch_record(
    result: dict[str, Any],
    *,
    output_path: Path | None = None,
) -> dict[str, Any]:
    record = {
        "status": result["status"],
        "plannedAnalyzerIds": result["plannedAnalyzerIds"],
        "executedAnalyzerIds": result["executedAnalyzerIds"],
        "parserProfileId": result.get("parserProfileId"),
        "skippedAnalyzerPlans": result["skippedAnalyzerPlans"],
        "diagnostics": result["diagnostics"],
    }
    index = result.get("index")
    if isinstance(index, dict):
        record["summary"] = index.get("summary")
    if output_path is not None:
        record["output"] = str(output_path)
    return record
