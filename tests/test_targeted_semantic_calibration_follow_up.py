from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "SPECS/EVIDENCE/P55-T9/P55-T9_Targeted_Semantic_Quality_Calibration.json"
EVIDENCE = (
    ROOT / "SPECS/EVIDENCE/P55-T9A/P55-T9A_Semantic_Provider_Output_Conformance_Follow-Up.json"
)
RUBRIC = ROOT / ("tests/fixtures/targeted_semantic_calibration/p55-t9-target-rubric.example.json")
POLICY_DIGEST = "687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82"


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def test_follow_up_is_bound_to_unchanged_baseline_rubric_and_policy() -> None:
    report = json.loads(EVIDENCE.read_text())
    rubric = json.loads(RUBRIC.read_text())

    assert report["runId"] == "p55-t9a"
    assert report["baselineEvidenceSha256"] == hashlib.sha256(BASELINE.read_bytes()).hexdigest()
    assert report["rubricSha256"] == digest(rubric)
    assert report["policySha256"] == POLICY_DIGEST
    assert report["scope"] == {
        "fullFrozenTargetSet": True,
        "repositoryIds": [target["repositoryId"] for target in rubric["targets"]],
        "providerIds": ["codex_spark", "lm_studio"],
    }


def test_follow_up_completes_every_provider_target_and_unblocks_p55_t10() -> None:
    report = json.loads(EVIDENCE.read_text())

    assert report["decision"] == {
        "p55T10Unblocked": True,
        "thresholdsRedefined": False,
    }
    for provider in report["providers"].values():
        assert provider["summary"]["targetCount"] == 4
        assert provider["summary"]["completedCount"] == 4
        assert provider["summary"]["failedCount"] == 0
        assert provider["summary"]["passed"] is True
        assert all(gate["passed"] for gate in provider["summary"]["frozenGates"].values())
        assert all(record["status"] == "completed" for record in provider["records"])
        assert all(record["metrics"]["purposeAccurate"] for record in provider["records"])
        assert all(record["metrics"]["schemaValid"] for record in provider["records"])
        assert all(
            record["metrics"]["evidenceSupportRate"] == 1.0 for record in provider["records"]
        )


def test_follow_up_preserves_diagnostics_privacy_and_non_authority() -> None:
    report = json.loads(EVIDENCE.read_text())
    serialized = EVIDENCE.read_text().lower()

    assert report["materializationCount"] == 0
    assert report["registryMutationCount"] == 0
    assert not any(report["privacy"].values())
    assert "capability_namespace_violation" in serialized
    assert "generic_intent_reuse" in serialized
    for forbidden in (
        "/users/egor",
        "api_key",
        "authorization",
        '"rawprompt"',
        '"rawresponse"',
    ):
        assert forbidden not in serialized
    for provider in report["providers"].values():
        for record in provider["records"]:
            receipt = record["providerReceipt"]
            assert receipt["rawPromptPersisted"] is False
            assert receipt["rawResponsePersisted"] is False
            assert receipt["chainOfThoughtPersisted"] is False


def test_follow_up_docs_record_transport_and_gate_outcome() -> None:
    markdown = (ROOT / "docs/SEMANTIC_PROVIDER_OUTPUT_CONFORMANCE_FOLLOW_UP.md").read_text()
    docc = (
        ROOT / "Sources/SpecHarvester/Documentation.docc/"
        "SemanticProviderOutputConformanceFollowUp.md"
    ).read_text()

    for text in (markdown, docc):
        assert "Codex 5.3 Spark" in text
        assert "LM Studio" in text
        assert "4/4" in text
        assert "P55-T10" in text
        assert "proposal-only" in text
