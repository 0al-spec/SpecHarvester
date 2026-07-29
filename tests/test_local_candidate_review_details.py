# ruff: noqa: E501

from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.local_candidate_review_details import (
    LocalCandidateReviewDetailsOptions,
    build_local_candidate_review_details,
)

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz"
CATALOG = ROOT / "SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json"
DIGEST = "db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63"


def test_detail_builder_emits_bound_inert_records(tmp_path: Path) -> None:
    output = tmp_path / "details.json"
    result = build_local_candidate_review_details(
        LocalCandidateReviewDetailsOptions(ARCHIVE, DIGEST, CATALOG, output)
    )

    payload = json.loads(output.read_text())
    assert result["detailCount"] == 100
    assert len(payload["details"]) == 100
    bitcoin = next(
        item for item in payload["details"] if item["binding"]["candidateId"] == "bitcoin-bitcoin"
    )
    assert bitcoin["previewOnly"] is True
    assert bitcoin["sections"]
    assert all("content" in section for section in bitcoin["sections"])
    assert payload["comparisons"]
    assert {comparison["ai"]["status"] for comparison in payload["comparisons"]} <= {
        "portable",
        "summary_only_not_portable",
    }


def test_detail_builder_rejects_catalog_binding_drift(tmp_path: Path) -> None:
    catalog = json.loads(CATALOG.read_text())
    catalog["items"][0]["packetSha256"] = "0" * 64
    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(json.dumps(catalog))

    with pytest.raises(ValueError, match="differs from catalog"):
        build_local_candidate_review_details(
            LocalCandidateReviewDetailsOptions(
                ARCHIVE, DIGEST, catalog_path, tmp_path / "details.json"
            )
        )
