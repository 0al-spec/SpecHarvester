from __future__ import annotations

import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit

from spec_harvester.batch_collection import resolve_checkout
from spec_harvester.controlled_calibration import git_dirty_status, git_head, write_json
from spec_harvester.final_corpus_checkout_readiness import tracked_file_bytes
from spec_harvester.mass_corpus_source_manifest import read_mass_corpus_selection_metadata
from spec_harvester.source_manifest import read_repository_source_manifests

MASS_CORPUS_READINESS_API_VERSION = "spec-harvester.mass-corpus-checkout-readiness/v0"
MASS_CORPUS_READINESS_KIND = "SpecHarvesterMassCorpusCheckoutReadiness"
EXPECTED_WAVES = {f"wave-{number}": 25 for number in range(1, 5)}
LICENSE_FILENAMES = frozenset({"license", "copying", "notice"})


@dataclass(frozen=True)
class MassCorpusCheckoutReadinessOptions:
    inputs: Path
    metadata: Path
    output: Path


class MassCorpusCheckoutReadiness:
    def __init__(
        self,
        options: MassCorpusCheckoutReadinessOptions,
        *,
        head_reader: Callable[[Path], str | None] = git_head,
        dirty_reader: Callable[[Path], str | None] = git_dirty_status,
        origin_reader: Callable[[Path], str | None] | None = None,
        size_reader: Callable[[Path], int | None] = tracked_file_bytes,
        license_reader: Callable[[Path], list[str]] | None = None,
    ) -> None:
        self.options = options
        self.head_reader = head_reader
        self.dirty_reader = dirty_reader
        self.origin_reader = origin_reader or git_origin
        self.size_reader = size_reader
        self.license_reader = license_reader or root_license_files

    def run(self) -> dict[str, Any]:
        sources = read_repository_source_manifests(self.options.inputs)
        payload = read_mass_corpus_selection_metadata(self.options.metadata)
        metadata = _metadata_by_id(payload)
        _validate_structure(sources, metadata)
        records = [self.repository_record(source, metadata[source["id"]]) for source in sources]
        summary = readiness_summary(records)
        passed = summary["readyCount"] == 100 and summary["wavePolicyPassed"]
        report = {
            "apiVersion": MASS_CORPUS_READINESS_API_VERSION,
            "kind": MASS_CORPUS_READINESS_KIND,
            "schemaVersion": 1,
            "phase": "P53",
            "task": "P53-T4",
            "status": "passed" if passed else "failed",
            "authority": "producer_checkout_readiness_evidence_only",
            "repositories": records,
            "summary": summary,
            "gateFailures": [] if passed else ["checkout_source_policy_not_ready"],
            "decision": {
                "p53T5Unlocked": passed,
                "selectedDecision": "unlock_p53_t5" if passed else "block_p53_t5",
            },
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

    def repository_record(self, source: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
        failures: list[str] = []
        try:
            checkout = resolve_checkout(self.options.inputs.resolve(), source)
        except ValueError:
            checkout = None
            failures.append("checkout_missing")

        head = self.head_reader(checkout) if checkout else None
        dirty = self.dirty_reader(checkout) if checkout else None
        origin = self.origin_reader(checkout) if checkout else None
        observed_bytes = self.size_reader(checkout) if checkout else None
        license_paths = self.license_reader(checkout) if checkout else []
        if head != source["revision"]:
            failures.append("checkout_revision_mismatch")
        if dirty is None:
            failures.append("checkout_status_unavailable")
        elif dirty:
            failures.append("checkout_dirty")
        if _canonical_origin(origin) != _canonical_origin(source["repository"]):
            failures.append("checkout_origin_mismatch")
        maximum_bytes = metadata["sizeBudget"].get("maximumBytes")
        if observed_bytes is None:
            failures.append("tracked_size_unavailable")
        elif observed_bytes > maximum_bytes:
            failures.append("size_budget_exceeded")
        if not license_paths:
            failures.append("license_evidence_unavailable")
        return {
            "id": source["id"],
            "position": metadata["position"],
            "wave": metadata["wave"],
            "repository": source["repository"],
            "revision": source["revision"],
            "checkout": source["checkout"],
            "ecosystem": metadata["ecosystem"],
            "repositoryShape": metadata["repositoryShape"],
            "provenance": {
                "expectedOrigin": source["repository"],
                "observedOrigin": origin,
                "status": (
                    "resolved" if "checkout_origin_mismatch" not in failures else "unresolved"
                ),
            },
            "licenseProvenance": {
                "paths": license_paths,
                "status": "resolved" if license_paths else "unresolved",
            },
            "sizeBudget": {
                "observedBytes": observed_bytes,
                "maximumBytes": maximum_bytes,
                "withinBudget": observed_bytes is not None and observed_bytes <= maximum_bytes,
            },
            "status": "ready" if not failures else "blocked",
            "failures": failures,
        }


def run_mass_corpus_checkout_readiness(
    options: MassCorpusCheckoutReadinessOptions,
) -> dict[str, Any]:
    return MassCorpusCheckoutReadiness(options).run()


def git_origin(checkout: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(checkout), "remote", "get-url", "origin"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def root_license_files(checkout: Path) -> list[str]:
    try:
        return sorted(
            path.name
            for path in checkout.iterdir()
            if path.is_file()
            and path.name.split(".", 1)[0].split("-", 1)[0].lower() in LICENSE_FILENAMES
        )
    except OSError:
        return []


def readiness_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    waves = Counter(record["wave"] for record in records)
    expected_waves = {f"wave-{((record['position'] - 1) // 25) + 1}" for record in records}
    wave_positions_match = all(
        record["wave"] == f"wave-{((record['position'] - 1) // 25) + 1}" for record in records
    )
    return {
        "repositoryCount": len(records),
        "readyCount": sum(record["status"] == "ready" for record in records),
        "blockedCount": sum(record["status"] == "blocked" for record in records),
        "waveDistribution": dict(sorted(waves.items())),
        "wavePolicyPassed": (
            dict(waves) == EXPECTED_WAVES and wave_positions_match and len(expected_waves) == 4
        ),
        "failureCounts": dict(
            sorted(Counter(failure for record in records for failure in record["failures"]).items())
        ),
    }


def _metadata_by_id(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = payload.get("repositories")
    if not isinstance(records, list) or len(records) != 100:
        raise ValueError("P53-T4 selection metadata must contain exactly 100 records")
    mapped = {
        record["id"]: record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("id"), str)
    }
    if len(mapped) != len(records):
        raise ValueError("P53-T4 selection metadata ids must be unique and valid")
    return mapped


def _validate_structure(sources: list[dict[str, Any]], metadata: dict[str, dict[str, Any]]) -> None:
    if len(sources) != 100 or {source["id"] for source in sources} != set(metadata):
        raise ValueError("P53-T4 source manifest and metadata must contain matching 100 records")
    for source in sources:
        record = metadata[source["id"]]
        required = {"position", "wave", "ecosystem", "repositoryShape", "sizeBudget"}
        if not required <= set(record):
            raise ValueError(f"P53-T4 metadata is incomplete for {source['id']!r}")
        position = record["position"]
        maximum_bytes = record["sizeBudget"].get("maximumBytes")
        if not isinstance(position, int) or not 1 <= position <= 100:
            raise ValueError(f"P53-T4 position is invalid for {source['id']!r}")
        if record["wave"] != f"wave-{((position - 1) // 25) + 1}":
            raise ValueError(f"P53-T4 wave does not match position for {source['id']!r}")
        if not isinstance(maximum_bytes, int) or maximum_bytes <= 0:
            raise ValueError(f"P53-T4 size budget is invalid for {source['id']!r}")


def _canonical_origin(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    if value.startswith("git@github.com:"):
        path = value.removeprefix("git@github.com:")
    else:
        parsed = urlsplit(value)
        if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
            return None
        path = parsed.path
    normalized_path = path.strip("/").removesuffix(".git")
    if normalized_path.count("/") != 1:
        return None
    return normalized_path.lower()
