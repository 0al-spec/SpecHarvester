from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from spec_harvester.semantic_proposal_quality import load_semantic_author_quality_policy

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "run_p55_t9_calibration", ROOT / "scripts/run_p55_t9_calibration.py"
)
assert SCRIPT_SPEC is not None and SCRIPT_SPEC.loader is not None
calibration = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(calibration)
RUBRIC = ROOT / "tests/fixtures/targeted_semantic_calibration/p55-t9-target-rubric.example.json"
EVIDENCE = ROOT / "SPECS/EVIDENCE/P55-T9/P55-T9_Targeted_Semantic_Quality_Calibration.json"
POLICY_DIGEST = "687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82"


def test_targeted_rubric_covers_required_and_comparable_repositories() -> None:
    rubric = json.loads(RUBRIC.read_text())

    assert rubric["policySha256"] == POLICY_DIGEST
    targets = {item["repositoryId"]: item for item in rubric["targets"]}
    assert set(targets) == {
        "rtk-ai-rtk",
        "openai-codex",
        "burntsushi-ripgrep",
        "thedotmack-claude-mem",
    }
    assert all(item["purposeConceptGroups"] for item in targets.values())
    assert all(item["specificTerms"] for item in targets.values())


def test_targeted_evidence_accounts_for_provider_failures_and_blocks_p55_t10() -> None:
    report = json.loads(EVIDENCE.read_text())

    assert report["policySha256"] == POLICY_DIGEST
    assert report["decision"] == {
        "p55T10Unblocked": False,
        "thresholdsRedefined": False,
    }
    assert report["materializationCount"] == 0
    assert report["registryMutationCount"] == 0
    assert set(report["providers"]) == {"codex_spark", "lm_studio"}
    codex = report["providers"]["codex_spark"]
    lm_studio = report["providers"]["lm_studio"]
    assert (
        report["sourceManifestSha256"]
        == "d1443331ff27845683d68a3bbafc146f45a337962ec7d1b9537aff37f967403d"
    )
    assert set(report["sourceRevisions"]) == {
        "rtk-ai-rtk",
        "openai-codex",
        "burntsushi-ripgrep",
        "thedotmack-claude-mem",
    }
    assert codex["summary"]["completedCount"] == 4
    assert codex["summary"]["failedCount"] == 0
    assert lm_studio["summary"]["completedCount"] == 0
    assert lm_studio["summary"]["failedCount"] == 4
    assert all(not provider["summary"]["passed"] for provider in report["providers"].values())
    assert all(len(provider["records"]) == 4 for provider in report["providers"].values())
    assert codex["summary"]["frozenGates"]["purposeAccuracyRate"]["passed"] is False
    assert codex["summary"]["frozenGates"]["reviewerEditBurdenRate"]["passed"] is False
    assert lm_studio["summary"]["metrics"]["reviewerEditBurdenRate"] == 1.0
    assert lm_studio["summary"]["frozenGates"]["reviewerEditBurdenRate"]["passed"] is False


def test_targeted_evidence_preserves_privacy_and_explains_quality_outcomes() -> None:
    report = json.loads(EVIDENCE.read_text())

    assert not any(report["privacy"].values())
    serialized = EVIDENCE.read_text().lower()
    for forbidden in (
        "/users/egor",
        "api_key",
        "authorization",
    ):
        assert forbidden not in serialized
    codex = {item["repositoryId"]: item for item in report["providers"]["codex_spark"]["records"]}
    assert codex["openai-codex"]["metrics"]["purposeAccurate"] is True
    assert codex["rtk-ai-rtk"]["metrics"]["purposeAccurate"] is False
    assert "capability_namespace_violation" in codex["rtk-ai-rtk"]["diagnosticCodes"]
    assert codex["burntsushi-ripgrep"]["status"] == "completed"
    assert codex["thedotmack-claude-mem"]["status"] == "completed"
    for item in codex.values():
        receipt = item.get("providerReceipt")
        if receipt:
            assert receipt["rawPromptPersisted"] is False
            assert receipt["rawResponsePersisted"] is False
            assert receipt["chainOfThoughtPersisted"] is False
    assert all(
        item["status"] == "failed" and "proposal schema validation failed" in item["failureCode"]
        for item in report["providers"]["lm_studio"]["records"]
    )


def test_rubric_terms_match_complete_normalized_tokens_only() -> None:
    target = {
        "purposeConceptGroups": [["code"]],
        "specificTerms": ["code"],
    }
    semantic_pass = {
        "proposal": {
            "claims": [
                {"kind": "purpose", "text": "Decode repository metadata."},
                {"kind": "capability", "text": "Use openai_codex.codex."},
            ],
            "intentDecisions": [],
        }
    }
    quality = {"metrics": {"evidenceSupportRate": 1.0, "schemaValid": True}}

    metrics = calibration.rubric_metrics(target, semantic_pass, quality)

    assert metrics["purposeAccurate"] is False
    assert metrics["capabilitySpecific"] is False
    assert calibration.contains_semantic_focus_term("code-aware assistant", "code") is True
    assert calibration.contains_semantic_focus_term("coding assistant", "code") is True
    assert calibration.contains_semantic_focus_term("searches files", "search") is True
    assert calibration.contains_semantic_focus_term("decode payload", "code") is False
    assert calibration.contains_semantic_focus_term("code", "---") is False


def test_failed_proposals_contribute_maximal_reviewer_edit_burden() -> None:
    records = [{"status": "failed", "failureCode": "invalid output"} for _index in range(4)]

    summary = calibration.provider_summary(records, load_semantic_author_quality_policy())

    assert summary["metrics"]["reviewerEditBurdenRate"] == 1.0
    assert summary["frozenGates"]["reviewerEditBurdenRate"]["passed"] is False


def test_retained_source_checkout_requires_pinned_clean_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "repo"
    source.mkdir()
    monkeypatch.setattr(calibration, "git_head", lambda _path: "a" * 40)
    monkeypatch.setattr(calibration, "git_dirty_status", lambda _path: "")
    calibration.validate_source_checkout(source, "a" * 40)

    monkeypatch.setattr(calibration, "git_head", lambda _path: "b" * 40)
    with pytest.raises(ValueError, match="revision mismatch"):
        calibration.validate_source_checkout(source, "a" * 40)

    monkeypatch.setattr(calibration, "git_head", lambda _path: "a" * 40)
    monkeypatch.setattr(calibration, "git_dirty_status", lambda _path: "?? local.txt\n")
    with pytest.raises(ValueError, match="checkout is dirty"):
        calibration.validate_source_checkout(source, "a" * 40)
