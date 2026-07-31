# ruff: noqa: E501

from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.local_candidate_review_details import (
    LocalCandidateReviewDetailsOptions,
    build_local_candidate_review_details,
)
from spec_harvester.local_review_decision_service import LocalReviewDecisionStore

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz"
CATALOG = ROOT / "SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json"
DIGEST = "db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63"
SEMANTIC_ARCHIVE = ROOT / "SPECS/EVIDENCE/P55-T10/P55-T10_Semantic_Proposal_Records.tar.gz"
SEMANTIC_DIGEST = "233f78f2541eee35b61e3bac5a1e00113e98041b9729ee67d4ce61209ae4f07f"


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


def test_detail_builder_overlays_retained_semantic_campaign(tmp_path: Path) -> None:
    output = tmp_path / "details.json"
    result = build_local_candidate_review_details(
        LocalCandidateReviewDetailsOptions(
            ARCHIVE,
            DIGEST,
            CATALOG,
            output,
            SEMANTIC_ARCHIVE,
            SEMANTIC_DIGEST,
        )
    )

    payload = json.loads(output.read_text())
    assert result["semanticPortableCount"] == 42
    assert result["semanticRejectedCount"] == 58
    assert payload["semanticCampaignSha256"] == SEMANTIC_DIGEST
    openai = next(
        item for item in payload["comparisons"] if item["binding"]["candidateId"] == "openai-codex"
    )
    assert openai["ai"]["status"] == "complete_portable"
    assert openai["semantic"]["ai"]["claims"]["purpose"]
    rtk = next(
        item for item in payload["comparisons"] if item["binding"]["candidateId"] == "rtk-ai-rtk"
    )
    assert rtk["ai"]["status"] == "campaign_rejected"
    assert rtk["ai"]["qualityStatus"] == "rejected"
    store = LocalReviewDecisionStore(tmp_path / "review-state", CATALOG, output)
    assert store.source_bundle_sha256 == payload["sourceBundleSha256"]


def test_detail_builder_requires_complete_semantic_archive_binding(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must be supplied together"):
        build_local_candidate_review_details(
            LocalCandidateReviewDetailsOptions(
                ARCHIVE,
                DIGEST,
                CATALOG,
                tmp_path / "details.json",
                semantic_campaign_archive=SEMANTIC_ARCHIVE,
            )
        )
