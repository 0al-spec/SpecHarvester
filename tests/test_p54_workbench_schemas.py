from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

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
