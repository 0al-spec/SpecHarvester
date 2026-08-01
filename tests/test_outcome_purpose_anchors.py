from __future__ import annotations

import copy
import hashlib

import pytest

from spec_harvester.outcome_purpose_anchors import (
    assess_purpose_specificity,
    build_outcome_purpose_anchors,
    validate_outcome_purpose_anchors,
)


def fixture() -> tuple[dict, list[dict], str]:
    source_bundle = "b" * 64
    profile = {
        "profileSha256": "a" * 64,
        "repository": {"owner": "rtk-ai", "name": "rtk"},
        "package": {
            "candidateId": "rtk_ai_rtk.package",
            "name": "rtk",
            "description": "Reduce token usage while preserving useful command output",
            "targetLabel": "RTK package",
        },
        "technology": {
            "languages": [{"id": "javascript"}],
            "ecosystems": [{"id": "npm"}],
            "analyzerSignals": ["javascript.public_api"],
        },
        "documents": [
            {
                "evidencePath": "README.md",
                "sourcePath": "README.md",
                "sha256": "c" * 64,
            }
        ],
    }
    evidence = [
        {
            "sourcePath": "semantic-product-profile.json",
            "sha256": "d" * 64,
            "content": "{}",
        },
        {
            "sourcePath": "README.md",
            "sha256": "c" * 64,
            "content": "RTK filters noisy command output so coding agents consume fewer tokens.",
        },
    ]
    return profile, evidence, source_bundle


def test_builds_deterministic_source_bound_outcome_anchors() -> None:
    profile, evidence, source_bundle = fixture()

    first = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )
    second = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    assert first == second
    assert (
        first["anchorsSha256"]
        == hashlib.sha256(
            __import__("json")
            .dumps(
                {key: value for key, value in first.items() if key != "anchorsSha256"},
                sort_keys=True,
                separators=(",", ":"),
            )
            .encode()
        ).hexdigest()
    )
    assert {"reduce", "token", "usage"} <= set(first["anchors"][0]["outcomeTerms"])
    assert "rtk" not in first["anchors"][0]["outcomeTerms"]
    assert first["anchors"][1]["sourcePath"] == "README.md"
    assert all(anchor["untrusted"] for anchor in first["anchors"])


def test_specificity_distinguishes_outcome_missing_and_mechanics_only() -> None:
    profile, evidence, source_bundle = fixture()
    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    assert assess_purpose_specificity(record, "Reduce token usage for coding agents") == "specific"
    assert assess_purpose_specificity(record, "Schedule meetings for teams") == "missing_anchor"
    assert assess_purpose_specificity(record, "A JavaScript package library and CLI tool") == (
        "mechanics_only"
    )


def test_validation_rejects_stale_digest_and_evidence_binding() -> None:
    profile, evidence, source_bundle = fixture()
    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )
    stale = copy.deepcopy(record)
    stale["anchors"][0]["phrase"] = "changed"
    with pytest.raises(ValueError, match="record is invalid"):
        validate_outcome_purpose_anchors(stale)

    with pytest.raises(ValueError, match="evidence binding is stale"):
        validate_outcome_purpose_anchors(record, profile=profile, evidence=evidence[:1])

    stale_profile = copy.deepcopy(profile)
    stale_profile["profileSha256"] = "e" * 64
    with pytest.raises(ValueError, match="profile binding is stale"):
        validate_outcome_purpose_anchors(record, profile=stale_profile, evidence=evidence)

    malformed = copy.deepcopy(record)
    malformed["mechanicsTerms"] = ["tool", "tool"]
    malformed["anchorsSha256"] = hashlib.sha256(
        __import__("json")
        .dumps(
            {key: value for key, value in malformed.items() if key != "anchorsSha256"},
            sort_keys=True,
            separators=(",", ":"),
        )
        .encode()
    ).hexdigest()
    with pytest.raises(ValueError, match="content is invalid"):
        validate_outcome_purpose_anchors(malformed)


def test_builder_requires_profile_and_profile_evidence_bindings() -> None:
    profile, evidence, source_bundle = fixture()
    profile["profileSha256"] = "invalid"
    with pytest.raises(ValueError, match="profile binding is invalid"):
        build_outcome_purpose_anchors(
            profile,
            evidence,
            candidate_id="rtk_ai_rtk.package",
            source_bundle_sha256=source_bundle,
        )

    profile["profileSha256"] = "a" * 64
    with pytest.raises(ValueError, match="profile evidence is unavailable"):
        build_outcome_purpose_anchors(
            profile,
            evidence[1:],
            candidate_id="rtk_ai_rtk.package",
            source_bundle_sha256=source_bundle,
        )


def test_builder_ignores_malformed_unbound_and_mechanics_only_candidates() -> None:
    profile, evidence, source_bundle = fixture()
    profile["package"]["description"] = "A package library and CLI tool"
    profile["documents"] = ["bad", {"evidencePath": "missing.md", "sha256": "f" * 64}]

    record = build_outcome_purpose_anchors(
        profile,
        evidence[:1],
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    assert record["anchors"] == []


def test_builder_deduplicates_identical_profile_and_document_phrases() -> None:
    profile, evidence, source_bundle = fixture()
    profile["package"]["description"] = evidence[1]["content"]

    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    assert len(record["anchors"]) == 1
