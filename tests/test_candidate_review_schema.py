from __future__ import annotations

from spec_harvester.candidate_review_schema import (
    SCHEMA_NAME,
    load_candidate_review_schema,
)


def test_candidate_review_schema_loader_returns_packaged_contract() -> None:
    schema = load_candidate_review_schema()

    assert schema["$id"].endswith(SCHEMA_NAME)
    assert "decision" in schema["$defs"]
