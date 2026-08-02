from __future__ import annotations

import copy
import hashlib
import json

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
                "role": "repository_root",
                "evidencePath": "README.md",
                "sourcePath": "README.md",
                "sha256": "c" * 64,
            }
        ],
    }
    profile_content = json.dumps(profile, sort_keys=True, separators=(",", ":"))
    evidence = [
        {
            "sourcePath": "semantic-product-profile.json",
            "sha256": "d" * 64,
            "content": profile_content,
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

    fabricated = copy.deepcopy(record)
    fabricated["anchors"][0]["phrase"] = "Schedule meetings for distributed teams"
    fabricated["anchors"][0]["outcomeTerms"] = ["distributed", "meetings", "schedule", "teams"]
    fabricated["anchorsSha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in fabricated.items() if key != "anchorsSha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    with pytest.raises(ValueError, match="phrase is not present"):
        validate_outcome_purpose_anchors(fabricated, profile=profile, evidence=evidence)

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
    evidence[0]["content"] = json.dumps(profile, sort_keys=True, separators=(",", ":"))

    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    assert len(record["anchors"]) == 1


def test_source_authority_ranks_strong_documentation_over_weak_preview() -> None:
    profile, evidence, source_bundle = fixture()
    profile["package"]["description"] = "Generated preview for member package boundary context"
    profile["documents"] = [
        {
            "role": "repository_root",
            "evidencePath": "README.md",
            "sourcePath": "README.md",
            "sha256": "c" * 64,
        },
        {
            "role": "package_local",
            "evidencePath": "PACKAGE_README.md",
            "sourcePath": "packages/rtk/README.md",
            "sha256": "e" * 64,
        },
    ]
    evidence.append(
        {
            "sourcePath": "PACKAGE_README.md",
            "sha256": "e" * 64,
            "content": (
                "RTK helps coding agents preserve useful command output while reducing tokens."
            ),
        }
    )
    evidence[0]["content"] = json.dumps(profile, sort_keys=True, separators=(",", ":"))

    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    authorities = {anchor["sourceAuthority"] for anchor in record["anchors"]}
    assert record["schemaVersion"] == 2
    assert record["sourceAuthorityState"] == "strong_anchor_available"
    assert "generated_preview_mechanics" in authorities
    assert "package_local_documentation" in authorities
    assert assess_purpose_specificity(record, "Reduce token use for coding agents") == "specific"
    assert (
        assess_purpose_specificity(record, "Generated preview context for a member package")
        == "weak_source_only"
    )


@pytest.mark.parametrize(
    ("phrase", "authority"),
    [
        ("Generated preview context for consumers", "generated_preview_mechanics"),
        ("Member package boundary context for consumers", "member_package_boundary_mechanics"),
        ("Import context for consumers and tools", "import_mechanics"),
        ("Discovery context for consumers and tools", "discovery_mechanics"),
        ("Module context for consumers and tools", "module_mechanics"),
    ],
)
def test_mechanics_phrases_never_make_a_purpose_specific(phrase: str, authority: str) -> None:
    profile, evidence, source_bundle = fixture()
    profile["package"]["description"] = ""
    profile["documents"] = [
        {
            "role": "repository_root",
            "evidencePath": "README.md",
            "sourcePath": "README.md",
            "sha256": "c" * 64,
        }
    ]
    evidence[1]["content"] = phrase
    evidence[0]["content"] = json.dumps(profile, sort_keys=True, separators=(",", ":"))

    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )

    assert record["sourceAuthorityState"] == "weak_only"
    assert record["anchors"][0]["sourceAuthority"] == authority
    assert assess_purpose_specificity(record, phrase) != "specific"


def test_authority_classification_rejects_a_recomputed_outer_digest_tamper() -> None:
    profile, evidence, source_bundle = fixture()
    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )
    tampered = copy.deepcopy(record)
    strong_anchor = next(
        anchor for anchor in tampered["anchors"] if anchor["sourcePath"] == "README.md"
    )
    strong_anchor["sourceAuthority"] = "generated_candidate_preview"
    tampered["sourceAuthorityState"] = "weak_only"
    tampered["anchorsSha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in tampered.items() if key != "anchorsSha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()

    with pytest.raises(ValueError, match="source authority is stale"):
        validate_outcome_purpose_anchors(tampered, profile=profile, evidence=evidence)


def test_legacy_anchor_records_remain_readable_but_are_not_specific() -> None:
    profile, evidence, source_bundle = fixture()
    record = build_outcome_purpose_anchors(
        profile,
        evidence,
        candidate_id="rtk_ai_rtk.package",
        source_bundle_sha256=source_bundle,
    )
    legacy = copy.deepcopy(record)
    legacy["schemaVersion"] = 1
    legacy.pop("sourceAuthorityPolicy")
    legacy.pop("sourceAuthorityState")
    for anchor in legacy["anchors"]:
        anchor.pop("sourceAuthority")
    legacy["anchorsSha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in legacy.items() if key != "anchorsSha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()

    validate_outcome_purpose_anchors(legacy, profile=profile, evidence=evidence)
    assert assess_purpose_specificity(legacy, "Reduce token usage for coding agents") == (
        "legacy_unclassified"
    )
