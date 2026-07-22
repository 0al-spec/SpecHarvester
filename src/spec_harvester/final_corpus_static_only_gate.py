from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from spec_harvester.autonomous_candidate_batch import (
    AI_DIRNAME,
    AI_DRAFT_PROPOSAL_FILENAME,
    AI_DRAFT_REQUEST_FILENAME,
    AI_ENRICHMENT_PROPOSAL_FILENAME,
    AI_ENRICHMENT_REQUEST_FILENAME,
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    AutonomousCandidateBatchOptions,
    run_autonomous_candidate_batch,
)
from spec_harvester.controlled_calibration import write_json
from spec_harvester.final_corpus_checkout_readiness import (
    MAXIMUM_REPOSITORY_COUNT,
    MINIMUM_REPOSITORY_COUNT,
)
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.source_manifest import read_repository_source_manifests

FINAL_CORPUS_STATIC_ONLY_GATE_API_VERSION = "spec-harvester.final-corpus-static-only-gate/v0"
FINAL_CORPUS_STATIC_ONLY_GATE_KIND = "SpecHarvesterFinalCorpusStaticOnlyGateReport"
FINAL_CORPUS_STATIC_ONLY_GATE_REPORT_FILENAME = "final-corpus-static-only-gate-report.json"
MINIMUM_STATIC_COMPLETION_RATE = 0.95
BATCH_VALIDATION_REPORT_RELATIVE_PATH = Path("reports/batch-validation-report.json")
AI_ARTIFACT_FILENAMES = frozenset(
    {
        AI_DRAFT_REQUEST_FILENAME,
        AI_DRAFT_PROPOSAL_FILENAME,
        AI_ENRICHMENT_REQUEST_FILENAME,
        AI_ENRICHMENT_PROPOSAL_FILENAME,
    }
)


@dataclass(frozen=True)
class FinalCorpusStaticOnlyGateOptions:
    inputs: Path
    readiness: Path
    readiness_sha256: str
    out: Path


class FinalCorpusStaticOnlyGate:
    def __init__(
        self,
        options: FinalCorpusStaticOnlyGateOptions,
        *,
        batch_runner: Callable[[AutonomousCandidateBatchOptions], dict[str, Any]] = (
            run_autonomous_candidate_batch
        ),
    ) -> None:
        self.options = options
        self.batch_runner = batch_runner

    @property
    def static_root(self) -> Path:
        return self.options.out / "static-only"

    def run(self) -> dict[str, Any]:
        sources = read_repository_source_manifests(self.options.inputs)
        source_ids = [string_value(source.get("id")) for source in sources]
        validate_source_ids(source_ids)
        readiness = read_json_object(self.options.readiness, "P52-T5 readiness report")
        readiness_digest = sha256_file(self.options.readiness)
        validate_readiness(
            readiness,
            expected_digest=self.options.readiness_sha256,
            observed_digest=readiness_digest,
            source_ids=source_ids,
        )
        batch = self.batch_runner(
            AutonomousCandidateBatchOptions(
                inputs=self.options.inputs,
                out=self.static_root,
                skip_ai=True,
                repository_profile_selection="auto",
            )
        )
        report = build_static_only_gate_report(
            options=self.options,
            source_ids=source_ids,
            readiness_digest=readiness_digest,
            batch=batch,
            static_report_path=self.static_root / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
            validation_report_path=self.static_root / BATCH_VALIDATION_REPORT_RELATIVE_PATH,
        )
        self.options.out.mkdir(parents=True, exist_ok=True)
        write_json(self.options.out / FINAL_CORPUS_STATIC_ONLY_GATE_REPORT_FILENAME, report)
        return report


def run_final_corpus_static_only_gate(
    options: FinalCorpusStaticOnlyGateOptions,
) -> dict[str, Any]:
    return FinalCorpusStaticOnlyGate(options).run()


def build_static_only_gate_report(
    *,
    options: FinalCorpusStaticOnlyGateOptions,
    source_ids: list[str],
    readiness_digest: str,
    batch: dict[str, Any],
    static_report_path: Path,
    validation_report_path: Path,
) -> dict[str, Any]:
    repositories = repository_records(batch, validation_report_path)
    result_ids = [record["id"] for record in repositories]
    source_coverage_passed = len(result_ids) == len(set(result_ids)) and set(result_ids) == set(
        source_ids
    )
    passed_count = sum(record["status"] == "passed" for record in repositories)
    metric = rate_metric(
        numerator=passed_count,
        denominator=len(source_ids),
        minimum=MINIMUM_STATIC_COMPLETION_RATE,
    )
    boundary = static_execution_boundary(batch, options.out)
    reports_available = static_report_path.is_file() and validation_report_path.is_file()
    unlocked = (
        source_coverage_passed and metric["passed"] and boundary["passed"] and reports_available
    )
    failed_ids = sorted(record["id"] for record in repositories if record["status"] != "passed")
    return {
        "apiVersion": FINAL_CORPUS_STATIC_ONLY_GATE_API_VERSION,
        "kind": FINAL_CORPUS_STATIC_ONLY_GATE_KIND,
        "schemaVersion": 1,
        "phase": "P52",
        "task": "P52-T6",
        "status": "passed" if unlocked else "failed",
        "readiness": {
            "path": str(options.readiness),
            "digest": digest_record(readiness_digest),
            "status": "passed",
        },
        "staticBatch": {
            "status": batch.get("status"),
            "report": (
                artifact_record(static_report_path, options.out)
                if static_report_path.is_file()
                else None
            ),
            "validationReport": (
                artifact_record(validation_report_path, options.out)
                if validation_report_path.is_file()
                else None
            ),
            "authority": batch.get("authority"),
        },
        "sourceCoverage": {
            "manifestCount": len(source_ids),
            "resultCount": len(result_ids),
            "uniqueResultCount": len(set(result_ids)),
            "missingIds": sorted(set(source_ids) - set(result_ids)),
            "unexpectedIds": sorted(set(result_ids) - set(source_ids)),
            "passed": source_coverage_passed,
        },
        "staticCompletionRate": metric,
        "failedRepositoryIds": failed_ids,
        "repositories": repositories,
        "staticExecutionBoundary": boundary,
        "decision": {
            "p52T7Unlocked": unlocked,
            "selectedDecision": "unlock_p52_t7" if unlocked else "block_p52_t7",
        },
        "authority": "producer_static_gate_evidence_only",
        "nonAuthority": {
            "acceptsPackages": False,
            "acceptsRelations": False,
            "publishesRegistryMetadata": False,
            "seedsBaselines": False,
            "removesPreviewOnly": False,
            "changesRegistryTruth": False,
        },
    }


def validate_source_ids(source_ids: list[str]) -> None:
    if not MINIMUM_REPOSITORY_COUNT <= len(source_ids) <= MAXIMUM_REPOSITORY_COUNT:
        raise ValueError("P52-T6 requires between 50 and 100 repositories")
    if any(not repository_id for repository_id in source_ids) or len(set(source_ids)) != len(
        source_ids
    ):
        raise ValueError("P52-T6 requires unique non-empty repository ids")


def validate_readiness(
    readiness: dict[str, Any],
    *,
    expected_digest: str,
    observed_digest: str,
    source_ids: list[str],
) -> None:
    if observed_digest != expected_digest:
        raise ValueError("P52-T5 readiness digest mismatch")
    decision = mapping_value(readiness.get("decision"))
    records = [
        record for record in list_value(readiness.get("repositories")) if isinstance(record, dict)
    ]
    readiness_ids = [string_value(record.get("id")) for record in records]
    if (
        readiness.get("task") != "P52-T5"
        or readiness.get("status") != "passed"
        or decision.get("p52T6Unlocked") is not True
    ):
        raise ValueError("P52-T5 readiness does not unlock P52-T6")
    if len(readiness_ids) != len(set(readiness_ids)) or set(readiness_ids) != set(source_ids):
        raise ValueError("P52-T5 readiness source ids do not match the P52-T6 manifest")
    if any(record.get("status") != "ready" for record in records):
        raise ValueError("P52-T5 readiness contains blocked repositories")


def repository_records(batch: dict[str, Any], validation_report_path: Path) -> list[dict[str, Any]]:
    validation_records = collection_validation_records(validation_report_path)
    records = []
    for item in list_value(batch.get("repositories")):
        if not isinstance(item, dict):
            continue
        preflight = mapping_value(item.get("preflight"))
        draft = mapping_value(item.get("packageSetDraft"))
        repository_id = string_value(item.get("id"))
        validation = validation_records.get(repository_id, {})
        validation_errors = diagnostic_codes(validation.get("errors"))
        validation_warnings = diagnostic_codes(validation.get("warnings"))
        batch_diagnostics = diagnostic_codes(item.get("diagnostics"))
        status = "passed" if item.get("status") == "passed" and not validation_errors else "failed"
        records.append(
            {
                "id": repository_id,
                "status": status,
                "batchStatus": item.get("status"),
                "collectionValidationStatus": "passed" if not validation_errors else "error",
                "preflightStatus": preflight.get("status"),
                "candidateCount": integer_value(draft.get("candidateCount")),
                "relationCount": integer_value(draft.get("relationCount")),
                "diagnosticCodes": sorted(
                    set(batch_diagnostics + validation_errors + validation_warnings)
                ),
            }
        )
    return records


def static_execution_boundary(batch: dict[str, Any], output_root: Path) -> dict[str, Any]:
    ai = mapping_value(batch.get("ai"))
    adapter = mapping_value(batch.get("repositoryPluginAdapterEvidence"))
    trusted_adapter = mapping_value(batch.get("trustedLocalAdapterRunEvidence"))
    repositories = [
        item for item in list_value(batch.get("repositories")) if isinstance(item, dict)
    ]
    ai_records_skipped = all(
        mapping_value(item.get(field)).get("status") == "skipped"
        for item in repositories
        for field in ("aiDraft", "aiEnrichment", "aiEnrichedPreview")
    )
    ai_artifacts = sorted(
        str(path.relative_to(output_root))
        for path in output_root.rglob("*")
        if path.is_file()
        and (
            AI_DIRNAME in path.relative_to(output_root).parts or path.name in AI_ARTIFACT_FILENAMES
        )
    )
    passed = (
        ai.get("mode") == "disabled"
        and ai.get("provider") is None
        and ai.get("model") is None
        and ai_records_skipped
        and adapter.get("adapterExecution") == "not_run"
        and trusted_adapter.get("adapterExecution") == "not_run"
        and not ai_artifacts
    )
    return {
        "passed": passed,
        "aiMode": ai.get("mode"),
        "provider": ai.get("provider"),
        "model": ai.get("model"),
        "repositoryAIRecordsSkipped": ai_records_skipped,
        "aiArtifactPaths": ai_artifacts,
        "adapterExecution": adapter.get("adapterExecution"),
        "trustedAdapterExecution": trusted_adapter.get("adapterExecution"),
        "invokesPackageManagers": False,
        "executesHarvestedCode": False,
    }


def rate_metric(*, numerator: int, denominator: int, minimum: float) -> dict[str, Any]:
    value = numerator / denominator if denominator else 0.0
    return {
        "value": value,
        "numerator": numerator,
        "denominator": denominator,
        "minimum": minimum,
        "passed": value >= minimum,
    }


def artifact_record(path: Path, output_root: Path) -> dict[str, Any]:
    try:
        display_path = path.relative_to(output_root).as_posix()
    except ValueError:
        display_path = path.name
    return {"path": display_path, "digest": digest_record(sha256_file(path))}


def collection_validation_records(path: Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    payload = read_json_object(path, "static batch validation report")
    return {
        string_value(record.get("id")): record
        for record in list_value(payload.get("records"))
        if isinstance(record, dict) and record.get("id")
    }


def diagnostic_codes(value: Any) -> list[str]:
    return sorted(
        {
            string_value(item.get("code"))
            for item in list_value(value)
            if isinstance(item, dict) and item.get("code")
        }
    )


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is unavailable") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object")
    return payload


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
