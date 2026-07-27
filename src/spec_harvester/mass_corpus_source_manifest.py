from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from spec_harvester.source_manifest import read_repository_source_manifests

MASS_CORPUS_METADATA_API_VERSION = "spec-harvester.mass-corpus-selection-metadata/v0"
MASS_CORPUS_METADATA_KIND = "SpecHarvesterMassCorpusSelectionMetadata"
EXPECTED_ECOSYSTEM_COUNTS = {
    "python": 15,
    "typescript": 15,
    "javascript": 15,
    "go": 15,
    "rust": 15,
    "java": 10,
    "c_cpp": 10,
    "swift": 5,
}
EXPECTED_WAVE_COUNTS = {f"wave-{number}": 25 for number in range(1, 5)}
MINIMUM_SHAPE_COUNTS = {
    "documentation_heavy": 10,
    "multi_component": 20,
    "workspace": 20,
    "single_package": 20,
}
_PINNED_REVISION = re.compile(r"^[0-9a-f]{40}$")


def read_mass_corpus_selection_metadata(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ValueError("P53-T3 selection metadata is unavailable") from error
    except json.JSONDecodeError as error:
        raise ValueError("P53-T3 selection metadata is invalid JSON") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("repositories"), list):
        raise ValueError("P53-T3 selection metadata must contain repositories")
    return payload


def validate_mass_corpus_source_manifest(
    inputs: Path, metadata_path: Path, p52_inputs: Path
) -> dict[str, int]:
    """Validate P53-T3's immutable source-selection boundary before P53-T4."""
    sources = read_repository_source_manifests(inputs)
    p52_sources = read_repository_source_manifests(p52_inputs)
    payload = read_mass_corpus_selection_metadata(metadata_path)
    if payload.get("apiVersion") != MASS_CORPUS_METADATA_API_VERSION:
        raise ValueError("P53-T3 selection metadata apiVersion mismatch")
    if payload.get("kind") != MASS_CORPUS_METADATA_KIND:
        raise ValueError("P53-T3 selection metadata kind mismatch")
    if payload.get("authority") != "operator_source_selection_evidence_only":
        raise ValueError("P53-T3 selection metadata authority mismatch")
    if payload.get("phase") != "P53" or payload.get("task") != "P53-T3":
        raise ValueError("P53-T3 selection metadata task identity mismatch")

    records = payload["repositories"]
    if len(sources) != 100 or len(records) != 100:
        raise ValueError("P53-T3 requires exactly 100 source and metadata records")
    metadata_by_id = _records_by_id(records)
    source_ids = {source["id"] for source in sources}
    if source_ids != set(metadata_by_id):
        raise ValueError("P53-T3 source manifest and metadata ids must match")
    source_origins = {_canonical_repository_identity(source["repository"]) for source in sources}
    if len(source_origins) != len(sources):
        raise ValueError("P53-T3 source origins must be unique")
    p52_urls = {_canonical_repository_identity(source["repository"]) for source in p52_sources}
    if source_ids & {source["id"] for source in p52_sources}:
        raise ValueError("P53-T3 source ids must not reuse P52 identities")

    ecosystems: dict[str, int] = {}
    waves: dict[str, int] = {}
    shapes: dict[str, int] = {}
    positions: list[int] = []
    for source in sources:
        repository_id = source["id"]
        record = metadata_by_id[repository_id]
        _validate_source_record(source, record, p52_urls)
        ecosystem = record["ecosystem"]
        wave = record["wave"]
        shape = record["repositoryShape"]
        position = record["position"]
        if not isinstance(position, int) or not 1 <= position <= 100:
            raise ValueError(f"P53-T3 position is invalid for {repository_id!r}")
        expected_wave = f"wave-{((position - 1) // 25) + 1}"
        if wave != expected_wave:
            raise ValueError(f"P53-T3 wave does not match position for {repository_id!r}")
        ecosystems[ecosystem] = ecosystems.get(ecosystem, 0) + 1
        waves[wave] = waves.get(wave, 0) + 1
        shapes[shape] = shapes.get(shape, 0) + 1
        positions.append(position)

    if ecosystems != EXPECTED_ECOSYSTEM_COUNTS:
        raise ValueError("P53-T3 ecosystem quota mismatch")
    if waves != EXPECTED_WAVE_COUNTS:
        raise ValueError("P53-T3 wave quota mismatch")
    if sorted(positions) != list(range(1, 101)):
        raise ValueError("P53-T3 positions must be a complete immutable ordering")
    for shape, minimum in MINIMUM_SHAPE_COUNTS.items():
        if shapes.get(shape, 0) < minimum:
            raise ValueError(f"P53-T3 repository shape quota failed for {shape}")
    if payload.get("quotas", {}).get("ecosystemExactCounts") != EXPECTED_ECOSYSTEM_COUNTS:
        raise ValueError("P53-T3 documented ecosystem quota mismatch")
    if payload.get("quotas", {}).get("waveExactCounts") != EXPECTED_WAVE_COUNTS:
        raise ValueError("P53-T3 documented wave quota mismatch")
    return {"repositoryCount": len(sources), "waveCount": len(waves)}


def _records_by_id(records: list[Any]) -> dict[str, dict[str, Any]]:
    if not all(
        isinstance(record, dict) and isinstance(record.get("id"), str) for record in records
    ):
        raise ValueError("P53-T3 metadata records are invalid")
    indexed = {record["id"]: record for record in records}
    if len(indexed) != len(records):
        raise ValueError("P53-T3 metadata ids must be unique")
    return indexed


def _validate_source_record(
    source: dict[str, Any], record: dict[str, Any], p52_urls: set[str]
) -> None:
    repository_id = source["id"]
    if _canonical_repository_identity(source["repository"]) in p52_urls:
        raise ValueError(f"P53-T3 source {repository_id!r} must not reuse a P52 repository")
    if not source["repository"].startswith("https://github.com/"):
        raise ValueError(f"P53-T3 source {repository_id!r} must use a public GitHub HTTPS origin")
    if not isinstance(source["revision"], str) or not _PINNED_REVISION.fullmatch(
        source["revision"]
    ):
        raise ValueError(f"P53-T3 source {repository_id!r} must use a full pinned revision")
    if source["checkout"] != f"../../../../P53Sources/{repository_id}":
        raise ValueError(f"P53-T3 source {repository_id!r} has an invalid checkout path")
    if source["packageId"] != f"{repository_id}.core":
        raise ValueError(f"P53-T3 source {repository_id!r} has an invalid package id")
    required = {
        "position",
        "wave",
        "ecosystem",
        "repositoryShape",
        "importanceSignals",
        "provenance",
        "licenseProvenance",
        "sizeBudget",
        "stopPolicy",
    }
    if not required <= set(record):
        raise ValueError(f"P53-T3 metadata is incomplete for {repository_id!r}")
    if record["provenance"].get("repository") != source["repository"]:
        raise ValueError(f"P53-T3 provenance repository mismatch for {repository_id!r}")
    if record["provenance"].get("checkoutVerification") != "pending_p53_t4":
        raise ValueError(f"P53-T3 checkout status is invalid for {repository_id!r}")
    if record["licenseProvenance"].get("status") != "pending_checkout_file_verification":
        raise ValueError(f"P53-T3 license status is invalid for {repository_id!r}")
    if record["sizeBudget"].get("status") != "pending_checkout_verification":
        raise ValueError(f"P53-T3 size status is invalid for {repository_id!r}")
    if (
        not isinstance(record["sizeBudget"].get("maximumBytes"), int)
        or record["sizeBudget"]["maximumBytes"] <= 0
    ):
        raise ValueError(f"P53-T3 size budget is invalid for {repository_id!r}")
    expected_label = record["wave"].replace("-", "_")
    if expected_label not in source["labels"] or record["ecosystem"] not in source["labels"]:
        raise ValueError(f"P53-T3 manifest labels do not match metadata for {repository_id!r}")


def _canonical_repository_identity(repository: str) -> str:
    return repository.rstrip("/").lower()
