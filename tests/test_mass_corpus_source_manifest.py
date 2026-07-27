from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.mass_corpus_source_manifest import (
    _records_by_id,
    read_mass_corpus_selection_metadata,
    validate_mass_corpus_source_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs/p53-mass-corpus"
METADATA = INPUTS / "selection-metadata.json"
P52_INPUTS = ROOT / "inputs/p52-final-corpus"


def test_mass_corpus_manifest_freezes_one_hundred_new_sources() -> None:
    assert validate_mass_corpus_source_manifest(INPUTS, METADATA, P52_INPUTS) == {
        "repositoryCount": 100,
        "waveCount": 4,
    }


def test_p52_source_reuse_is_rejected(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    manifest = (INPUTS / "repositories.yml").read_text(encoding="utf-8")
    (inputs / "repositories.yml").write_text(
        manifest.replace(
            "https://github.com/public-apis/public-apis", "https://github.com/PALLETS/FLASK"
        ),
        encoding="utf-8",
    )
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata["repositories"][0]["provenance"]["repository"] = "https://github.com/PALLETS/FLASK"
    invalid = tmp_path / "metadata.json"
    invalid.write_text(json.dumps(metadata), encoding="utf-8")

    with pytest.raises(ValueError, match="must not reuse a P52 repository"):
        validate_mass_corpus_source_manifest(inputs, invalid, P52_INPUTS)


def test_invalid_wave_assignment_is_rejected(tmp_path: Path) -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata["repositories"][0]["wave"] = "wave-5"
    invalid = tmp_path / "metadata.json"
    invalid.write_text(json.dumps(metadata), encoding="utf-8")

    with pytest.raises(ValueError, match="manifest labels do not match metadata"):
        validate_mass_corpus_source_manifest(INPUTS, invalid, P52_INPUTS)


def test_metadata_reader_and_record_index_fail_closed(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unavailable"):
        read_mass_corpus_selection_metadata(tmp_path / "missing.json")

    invalid = tmp_path / "invalid.json"
    invalid.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        read_mass_corpus_selection_metadata(invalid)

    invalid.write_text(json.dumps({"repositories": {}}), encoding="utf-8")
    with pytest.raises(ValueError, match="must contain repositories"):
        read_mass_corpus_selection_metadata(invalid)

    with pytest.raises(ValueError, match="records are invalid"):
        _records_by_id([{"id": "valid"}, {"id": 1}])
    with pytest.raises(ValueError, match="ids must be unique"):
        _records_by_id([{"id": "same"}, {"id": "same"}])


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("apiVersion", "wrong", "apiVersion mismatch"),
        ("kind", "wrong", "kind mismatch"),
        ("authority", "wrong", "authority mismatch"),
        ("phase", "P52", "task identity mismatch"),
        ("task", "P53-T2", "task identity mismatch"),
    ],
)
def test_metadata_identity_mismatch_is_rejected(
    tmp_path: Path, field: str, value: str, message: str
) -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata[field] = value
    invalid = tmp_path / "metadata.json"
    invalid.write_text(json.dumps(metadata), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        validate_mass_corpus_source_manifest(INPUTS, invalid, P52_INPUTS)


def test_documented_quota_mismatch_is_rejected(tmp_path: Path) -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata["quotas"]["ecosystemExactCounts"] = {}
    invalid = tmp_path / "metadata.json"
    invalid.write_text(json.dumps(metadata), encoding="utf-8")

    with pytest.raises(ValueError, match="documented ecosystem quota mismatch"):
        validate_mass_corpus_source_manifest(INPUTS, invalid, P52_INPUTS)


def test_incomplete_metadata_and_pending_policy_fields_are_rejected(tmp_path: Path) -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata["repositories"] = metadata["repositories"][:-1]
    invalid = tmp_path / "missing-record.json"
    invalid.write_text(json.dumps(metadata), encoding="utf-8")
    with pytest.raises(ValueError, match="exactly 100"):
        validate_mass_corpus_source_manifest(INPUTS, invalid, P52_INPUTS)

    for field, value, message in (
        ("checkoutVerification", "ready", "checkout status is invalid"),
        ("licenseStatus", "resolved", "license status is invalid"),
        ("sizeStatus", "verified", "size status is invalid"),
        ("maximumBytes", 0, "size budget is invalid"),
    ):
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        record = metadata["repositories"][0]
        if field == "checkoutVerification":
            record["provenance"][field] = value
        elif field == "licenseStatus":
            record["licenseProvenance"]["status"] = value
        elif field == "sizeStatus":
            record["sizeBudget"]["status"] = value
        else:
            record["sizeBudget"][field] = value
        invalid = tmp_path / f"{field}.json"
        invalid.write_text(json.dumps(metadata), encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            validate_mass_corpus_source_manifest(INPUTS, invalid, P52_INPUTS)


def test_source_and_metadata_identity_mismatch_is_rejected(tmp_path: Path) -> None:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    metadata["repositories"][0]["id"] = "different-source-id"
    invalid = tmp_path / "metadata.json"
    invalid.write_text(json.dumps(metadata), encoding="utf-8")

    with pytest.raises(ValueError, match="ids must match"):
        validate_mass_corpus_source_manifest(INPUTS, invalid, P52_INPUTS)


def test_operator_documentation_states_the_p53_t4_boundary() -> None:
    document = (ROOT / "docs/MASS_CORPUS_SOURCE_MANIFEST.md").read_text(encoding="utf-8")
    normalized = " ".join(document.split())

    for required in (
        "P53-T3",
        "exactly 100 new public GitHub repositories",
        "four sequential waves of 25",
        "P53-T4",
        "pending",
        "Codex Spark",
        "LM Studio",
        "preview_only",
        "registry truth",
    ):
        assert required in normalized
