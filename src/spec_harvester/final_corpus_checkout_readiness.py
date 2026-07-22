from __future__ import annotations

import json
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit

from spec_harvester.batch_collection import resolve_checkout
from spec_harvester.controlled_calibration import git_dirty_status, git_head, write_json
from spec_harvester.source_manifest import read_repository_source_manifests

FINAL_CORPUS_READINESS_API_VERSION = "spec-harvester.final-corpus-checkout-readiness/v0"
FINAL_CORPUS_READINESS_KIND = "SpecHarvesterFinalCorpusCheckoutReadiness"
MINIMUM_REPOSITORY_COUNT = 50
MAXIMUM_REPOSITORY_COUNT = 100
REQUIRED_STOP_POLICY_FLAGS = (
    "excludeOnDirtyCheckout",
    "excludeOnRevisionMismatch",
    "excludeOnSizeBudgetExceeded",
    "excludeOnUnresolvedProvenance",
)


@dataclass(frozen=True)
class FinalCorpusCheckoutReadinessOptions:
    inputs: Path
    metadata: Path
    output: Path


class FinalCorpusCheckoutReadiness:
    def __init__(
        self,
        options: FinalCorpusCheckoutReadinessOptions,
        *,
        head_reader: Callable[[Path], str | None] = git_head,
        dirty_reader: Callable[[Path], str | None] = git_dirty_status,
        size_reader: Callable[[Path], int | None] | None = None,
    ) -> None:
        self.options = options
        self.head_reader = head_reader
        self.dirty_reader = dirty_reader
        self.size_reader = size_reader or tracked_file_bytes

    def run(self) -> dict[str, Any]:
        sources = read_repository_source_manifests(self.options.inputs)
        metadata = read_metadata(self.options.metadata)
        validate_corpus_structure(sources, metadata)
        records = [self.repository_record(source, metadata[source["id"]]) for source in sources]
        passed = all(record["status"] == "ready" for record in records)
        report = {
            "apiVersion": FINAL_CORPUS_READINESS_API_VERSION,
            "kind": FINAL_CORPUS_READINESS_KIND,
            "schemaVersion": 1,
            "phase": "P52",
            "task": "P52-T5",
            "status": "passed" if passed else "failed",
            "repositories": records,
            "summary": readiness_summary(records),
            "decision": {
                "p52T6Unlocked": passed,
                "selectedDecision": "unlock_p52_t6" if passed else "block_p52_t6",
            },
            "authority": "producer_checkout_readiness_evidence_only",
            "executionBoundary": {
                "createsOrRestoresCheckouts": False,
                "clonesOrFetchesRepositories": False,
                "installsDependencies": False,
                "invokesPackageManagers": False,
                "executesHarvestedCode": False,
                "runsAdapters": False,
                "runsAI": False,
            },
        }
        write_json(self.options.output, report)
        return report

    def repository_record(
        self,
        source: dict[str, Any],
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        checkout = resolve_checkout(self.options.inputs.resolve(), source)
        revision = source["revision"]
        head = self.head_reader(checkout)
        dirty = self.dirty_reader(checkout)
        observed_bytes = self.size_reader(checkout)
        failures = []
        if not is_public_github_repository(source["repository"]):
            failures.append("repository_not_public_https_github")
        if head != revision:
            failures.append("checkout_revision_mismatch")
        if dirty is None:
            failures.append("checkout_status_unavailable")
        elif dirty:
            failures.append("checkout_dirty")
        provenance = object_value(metadata.get("provenance"))
        license_provenance = object_value(metadata.get("licenseProvenance"))
        size_budget = object_value(metadata.get("sizeBudget"))
        stop_policy = object_value(metadata.get("stopPolicy"))
        if provenance.get("status") != "resolved":
            failures.append("provenance_unresolved")
        if provenance.get("repository") != source["repository"]:
            failures.append("provenance_repository_mismatch")
        if license_provenance.get("status") != "resolved":
            failures.append("license_provenance_unresolved")
        if any(stop_policy.get(flag) is not True for flag in REQUIRED_STOP_POLICY_FLAGS):
            failures.append("stop_policy_incomplete")
        maximum_bytes = integer_value(size_budget.get("maximumBytes"))
        declared_bytes = integer_value(size_budget.get("observedBytes"))
        if observed_bytes is None:
            failures.append("tracked_size_unavailable")
        elif observed_bytes != declared_bytes:
            failures.append("tracked_size_mismatch")
        if observed_bytes is not None and observed_bytes > maximum_bytes:
            failures.append("size_budget_exceeded")
        return {
            "id": source["id"],
            "repository": source["repository"],
            "revision": revision,
            "ecosystem": metadata["ecosystem"],
            "repositoryShape": metadata["repositoryShape"],
            "importanceSignals": metadata["importanceSignals"],
            "selectionRationale": metadata["selectionRationale"],
            "provenance": provenance,
            "licenseProvenance": license_provenance,
            "stopPolicy": stop_policy,
            "sizeBudget": {
                "observedBytes": observed_bytes,
                "maximumBytes": maximum_bytes,
                "withinBudget": observed_bytes is not None and observed_bytes <= maximum_bytes,
            },
            "status": "ready" if not failures else "blocked",
            "failures": failures,
        }


def run_final_corpus_checkout_readiness(
    options: FinalCorpusCheckoutReadinessOptions,
) -> dict[str, Any]:
    return FinalCorpusCheckoutReadiness(options).run()


def read_metadata(path: Path) -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("P52-T5 selection metadata is unavailable") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("repositories"), list):
        raise ValueError("P52-T5 selection metadata must contain repositories")
    records = payload["repositories"]
    valid_records = all(
        isinstance(record, dict) and isinstance(record.get("id"), str) for record in records
    )
    if not valid_records:
        raise ValueError("P52-T5 selection metadata repository records are invalid")
    mapped = {record["id"]: record for record in records}
    if len(mapped) != len(records):
        raise ValueError("P52-T5 selection metadata has duplicate repository ids")
    return mapped


def validate_corpus_structure(
    sources: list[dict[str, Any]],
    metadata: dict[str, dict[str, Any]],
) -> None:
    if not MINIMUM_REPOSITORY_COUNT <= len(sources) <= MAXIMUM_REPOSITORY_COUNT:
        raise ValueError("P52-T5 requires between 50 and 100 repositories")
    source_ids = {source["id"] for source in sources}
    if source_ids != set(metadata):
        raise ValueError("P52-T5 source manifest and metadata ids must match")
    for source in sources:
        revision = source.get("revision")
        if not isinstance(revision, str) or len(revision) != 40 or source.get("ref") is not None:
            raise ValueError(f"P52-T5 source {source['id']!r} must use a full pinned revision")
    for repository_id, record in metadata.items():
        required = {
            "ecosystem",
            "repositoryShape",
            "importanceSignals",
            "provenance",
            "licenseProvenance",
            "sizeBudget",
            "selectionRationale",
            "stopPolicy",
        }
        if not required <= set(record):
            raise ValueError(f"P52-T5 metadata is incomplete for {repository_id!r}")
        validate_metadata_record(repository_id, record)


def validate_metadata_record(repository_id: str, record: dict[str, Any]) -> None:
    for field in ("ecosystem", "repositoryShape", "selectionRationale"):
        if not isinstance(record[field], str) or not record[field]:
            raise ValueError(f"P52-T5 metadata field {field!r} is invalid for {repository_id!r}")
    importance_signals = record["importanceSignals"]
    if (
        not isinstance(importance_signals, list)
        or not importance_signals
        or not all(isinstance(value, str) and value for value in importance_signals)
    ):
        raise ValueError(f"P52-T5 importance signals are invalid for {repository_id!r}")
    for field in ("provenance", "licenseProvenance", "sizeBudget", "stopPolicy"):
        if not isinstance(record[field], dict):
            raise ValueError(f"P52-T5 metadata field {field!r} is invalid for {repository_id!r}")
    size_budget = record["sizeBudget"]
    observed_bytes = size_budget.get("observedBytes")
    maximum_bytes = size_budget.get("maximumBytes")
    if (
        integer_value(observed_bytes) != observed_bytes
        or integer_value(maximum_bytes) != maximum_bytes
        or observed_bytes < 0
        or maximum_bytes <= 0
    ):
        raise ValueError(f"P52-T5 size budget is invalid for {repository_id!r}")
    stop_policy = record["stopPolicy"]
    if any(not isinstance(stop_policy.get(flag), bool) for flag in REQUIRED_STOP_POLICY_FLAGS):
        raise ValueError(f"P52-T5 stop policy is invalid for {repository_id!r}")


def is_public_github_repository(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        path_parts = [part for part in parsed.path.split("/") if part]
        return (
            parsed.scheme == "https"
            and parsed.netloc == "github.com"
            and len(path_parts) == 2
            and not parsed.query
            and not parsed.fragment
        )
    except ValueError:
        return False


def tracked_file_bytes(checkout: Path) -> int | None:
    result = subprocess.run(
        ["git", "-C", str(checkout), "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    try:
        return sum(
            (checkout / value.decode()).stat().st_size
            for value in result.stdout.split(b"\0")
            if value
        )
    except (OSError, UnicodeDecodeError):
        return None


def readiness_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "repositoryCount": len(records),
        "readyCount": sum(record["status"] == "ready" for record in records),
        "blockedCount": sum(record["status"] == "blocked" for record in records),
        "ecosystemDistribution": dict(
            sorted(Counter(record["ecosystem"] for record in records).items())
        ),
        "repositoryShapeDistribution": dict(
            sorted(Counter(record["repositoryShape"] for record in records).items())
        ),
    }


def object_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
