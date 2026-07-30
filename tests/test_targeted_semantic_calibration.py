from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
    assert codex["summary"]["completedCount"] == 2
    assert codex["summary"]["failedCount"] == 2
    assert lm_studio["summary"]["completedCount"] == 0
    assert lm_studio["summary"]["failedCount"] == 4
    assert all(not provider["summary"]["passed"] for provider in report["providers"].values())
    assert all(len(provider["records"]) == 4 for provider in report["providers"].values())
    assert all(
        not gate["passed"]
        for provider in report["providers"].values()
        for name, gate in provider["summary"]["frozenGates"].items()
        if name != "reviewerEditBurdenRate"
    )


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
    assert codex["burntsushi-ripgrep"]["status"] == "failed"
    assert codex["thedotmack-claude-mem"]["status"] == "failed"
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
