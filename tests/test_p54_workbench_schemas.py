from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from spec_harvester.local_candidate_review_validation import (
    validate_decision_reason_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/local-candidate-review-workbench-v0.schema.json"
VALID = ROOT / "tests/fixtures/local_candidate_review_workbench_schemas/p54-t2-valid.example.json"
INVALID = (
    ROOT / "tests/fixtures/local_candidate_review_workbench_schemas/p54-t2-invalid.example.json"
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validator() -> Draft202012Validator:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_valid_fixture_covers_all_six_workbench_records() -> None:
    payload = load(VALID)

    validator().validate(payload)

    assert set(payload) == {
        "apiVersion",
        "kind",
        "catalog",
        "detail",
        "comparison",
        "decision",
        "reasons",
        "export",
    }


def test_invalid_fixtures_are_rejected() -> None:
    base = load(VALID)
    cases = load(INVALID)
    schema_validator = validator()

    for case in cases:
        payload = copy.deepcopy(base)
        target = payload
        for component in case["path"]:
            target = target[component]
        if "delete" in case:
            del target[case["delete"]]
        else:
            parent = payload
            for component in case["path"][:-1]:
                parent = parent[component]
            parent[case["path"][-1]] = case["value"]
        assert list(schema_validator.iter_errors(payload)), case["case"]


def test_packet_binding_and_export_remain_non_authoritative() -> None:
    payload = load(VALID)

    assert (
        payload["detail"]["binding"]["packetSha256"]
        == (payload["comparison"]["binding"]["packetSha256"])
    )
    assert (
        payload["decision"]["binding"]["packetSha256"]
        == (payload["detail"]["binding"]["packetSha256"])
    )
    assert payload["export"]["authority"] == "portable_local_review_evidence_only"
    assert payload["export"]["registryMutationCount"] == 0


def test_standalone_records_and_comparison_shape_are_validated() -> None:
    payload = load(VALID)
    schema_validator = validator()

    schema_validator.validate(payload["catalog"])
    schema_validator.validate(payload["comparison"])

    malformed = copy.deepcopy(payload["comparison"])
    malformed["ai"] = {}
    assert list(schema_validator.iter_errors(malformed))


def test_reason_taxonomy_enforces_decision_compatibility() -> None:
    payload = load(VALID)

    validate_decision_reason_compatibility([payload["decision"]], payload["reasons"])

    unknown = copy.deepcopy(payload["decision"])
    unknown["reasonCode"] = "unknown_reason"
    with pytest.raises(ValueError, match="unknown reason code"):
        validate_decision_reason_compatibility([unknown], payload["reasons"])

    incompatible = copy.deepcopy(payload["decision"])
    incompatible["disposition"] = "defer"
    with pytest.raises(ValueError, match="not allowed"):
        validate_decision_reason_compatibility([incompatible], payload["reasons"])
