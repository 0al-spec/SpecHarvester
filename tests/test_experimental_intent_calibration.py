from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import spec_harvester.experimental_intent_calibration as calibration
from spec_harvester.experimental_intent_calibration import (
    EXPECTED_REPOSITORY_IDS,
    ExperimentalIntentCalibrationOptions,
    canonical_digest,
    load_calibration_plan,
    run_experimental_intent_calibration,
    summarize_calibration,
    target_metrics,
    validate_calibration_plan,
)
from spec_harvester.semantic_author_pass import ProviderCompletion, SemanticAuthorPassOptions
from spec_harvester.semantic_proposal_quality import load_semantic_author_quality_policy

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / (
    "tests/fixtures/experimental_intent_calibration/p55-t10b-calibration-plan.example.json"
)
RUBRIC = ROOT / "tests/fixtures/targeted_semantic_calibration/p55-t9-target-rubric.example.json"
EVIDENCE = ROOT / ("SPECS/EVIDENCE/P55-T10B/P55-T10B_Targeted_Experimental-Intent_Calibration.json")


class FocusAwareProvider:
    provider_id = "gpt-5.3-codex-spark"
    model = "gpt-5.3-codex-spark"

    def complete(self, request: dict, options: SemanticAuthorPassOptions) -> ProviderCompletion:
        evidence = request["request"]["evidence"][0]
        source_digest = request["request"]["sourceBundleSha256"]
        focus = request["semanticFocus"]
        purpose_terms = [group[0] for group in focus["purposeConceptGroups"]]
        specific_term = focus["specificTerms"][0]
        observed_id = request["observedIntents"][0]["intentId"]

        def claim(claim_id: str, kind: str, text: str) -> dict:
            return {"id": claim_id, "kind": kind, "text": text, "evidence": [evidence]}

        return ProviderCompletion(
            payload={
                "apiVersion": "spec-harvester.ai-semantic-proposal/v0",
                "kind": "SpecHarvesterAISemanticProposal",
                "schemaVersion": 1,
                "authority": "semantic_author_proposal_only",
                "proposalId": "targeted-experimental-proposal",
                "candidateId": request["request"]["candidateId"],
                "sourceBundleSha256": source_digest,
                "claims": [
                    claim("purpose", "purpose", f"Help users {' '.join(purpose_terms)}."),
                    claim("capability", "capability", f"Perform {specific_term} work."),
                    claim("interface", "interface", "Expose the documented interface."),
                    claim(
                        "nearby",
                        "nearby_intent_difference",
                        "Express the user outcome rather than package shape.",
                    ),
                    claim("non_goal", "non_goal", "Do not define registry truth."),
                ],
                "intentDecisions": [
                    {
                        "apiVersion": "spec-harvester.ai-semantic-experimental-intent/v0",
                        "kind": "SpecHarvesterAISemanticExperimentalIntent",
                        "schemaVersion": 1,
                        "state": "proposed_experimental",
                        "intentId": (
                            f"intent.experimental.describe_user_outcome.{source_digest[:8]}"
                        ),
                        "userNeedClaimId": "purpose",
                        "nearbyIntentIds": [observed_id],
                        "nearbyIntentClaimIds": ["nearby"],
                        "nonGoalClaimIds": ["non_goal"],
                    }
                ],
            },
            receipt={
                "providerKind": "codex_exec",
                "modelId": "gpt-5.3-codex-spark",
                "durationMs": 1,
            },
        )


def create_candidate(root: Path, repository_id: str, directory: str) -> None:
    candidate = root / repository_id / "candidate" / directory
    (candidate / "specs").mkdir(parents=True)
    candidate_id = f"{repository_id.replace('-', '_')}.package"
    capability_id = f"{candidate_id}.primary"
    (candidate / "specpm.yaml").write_text(
        "kind: SpecPackage\n"
        f"metadata:\n  id: {candidate_id}\n"
        "preview_only: true\n"
        "specs:\n  - path: specs/core.spec.yaml\n"
        "index:\n  provides:\n"
        f"    capabilities:\n      - {capability_id}\n"
        "    intents:\n      - intent.package.javascript_library\n",
        encoding="utf-8",
    )
    (candidate / "specs/core.spec.yaml").write_text(
        "kind: BoundarySpec\n"
        f"metadata:\n  id: {candidate_id}\n"
        "provides:\n  capabilities:\n"
        f"    - id: {capability_id}\n"
        "      role: primary\n"
        "      summary: Provide the documented outcome.\n"
        "      intentIds:\n        - intent.package.javascript_library\n",
        encoding="utf-8",
    )
    (candidate / "harvest.json").write_text("{}\n", encoding="utf-8")


def test_plan_is_digest_bound_to_provider_policies_and_targets() -> None:
    plan = load_calibration_plan(PLAN)

    assert [item["repositoryId"] for item in plan["targets"]] == list(EXPECTED_REPOSITORY_IDS)
    assert plan["provider"]["modelId"] == "gpt-5.3-codex-spark"
    assert plan["successCriteria"]["minimumEvidenceSupportedExperimentalIntentCount"] == 1
    assert all(value is False for value in plan["executionBoundary"].values())

    stale = copy.deepcopy(plan)
    stale["planSha256"] = "f" * 64
    with pytest.raises(ValueError, match="plan digest is stale"):
        validate_calibration_plan(stale)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("authority", "provider_owned", "identity is invalid"),
        ("targetRubric", {}, "rubric binding is invalid"),
        ("targets", [], "target set is invalid"),
        ("attemptBudget", {}, "attempt budget is invalid"),
        ("successCriteria", {}, "success criteria are invalid"),
        ("executionBoundary", {"publicationAllowed": True}, "execution boundary is invalid"),
    ),
)
def test_plan_rejects_contract_drift(field: str, value: object, message: str) -> None:
    plan = load_calibration_plan(PLAN)
    plan[field] = value

    with pytest.raises(ValueError, match=message):
        validate_calibration_plan(plan)


def test_runner_rejects_execution_budget_or_provider_drift(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="options violate the frozen plan"):
        run_experimental_intent_calibration(
            plan_path=PLAN,
            rubric_path=RUBRIC,
            candidate_root=tmp_path,
            source_root=tmp_path,
            source_manifest_dir=tmp_path,
            provider=FocusAwareProvider(),
            output_path=tmp_path / "output.json",
            options=ExperimentalIntentCalibrationOptions(provider_max_attempts=1),
        )

    provider = FocusAwareProvider()
    provider.model = "other-model"
    with pytest.raises(ValueError, match="does not match the frozen plan"):
        run_experimental_intent_calibration(
            plan_path=PLAN,
            rubric_path=RUBRIC,
            candidate_root=tmp_path,
            source_root=tmp_path,
            source_manifest_dir=tmp_path,
            provider=provider,
            output_path=tmp_path / "output.json",
        )


def test_source_revisions_require_the_complete_frozen_target_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = [
        {"id": repository_id, "revision": str(index) * 40}
        for index, repository_id in enumerate(EXPECTED_REPOSITORY_IDS, start=1)
    ]
    monkeypatch.setattr(calibration, "read_repository_source_manifests", lambda _path: records)

    revisions = calibration._source_revisions(Path("unused"))
    assert list(revisions) == list(EXPECTED_REPOSITORY_IDS)

    monkeypatch.setattr(calibration, "read_repository_source_manifests", lambda _path: records[:-1])
    with pytest.raises(ValueError, match="absent from the pinned manifest"):
        calibration._source_revisions(Path("unused"))


def test_source_checkout_must_be_pinned_and_clean(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    monkeypatch.setattr(calibration, "git_head", lambda _path: "a" * 40)
    monkeypatch.setattr(calibration, "git_dirty_status", lambda _path: "")
    calibration._validate_source_checkout(source, "a" * 40)

    monkeypatch.setattr(calibration, "git_head", lambda _path: "b" * 40)
    with pytest.raises(ValueError, match="revision mismatch"):
        calibration._validate_source_checkout(source, "a" * 40)

    monkeypatch.setattr(calibration, "git_head", lambda _path: "a" * 40)
    monkeypatch.setattr(calibration, "git_dirty_status", lambda _path: " M README.md")
    with pytest.raises(ValueError, match="checkout is dirty"):
        calibration._validate_source_checkout(source, "a" * 40)


def test_target_metrics_count_false_novelty_as_edit_failure() -> None:
    semantic_pass = {
        "proposal": {
            "claims": [
                {"id": "purpose", "kind": "purpose", "text": "coding agent", "evidence": [{}]},
                {
                    "id": "nearby",
                    "kind": "nearby_intent_difference",
                    "text": "same outcome",
                    "evidence": [{}],
                },
                {"id": "non_goal", "kind": "non_goal", "text": "none", "evidence": [{}]},
            ],
            "intentDecisions": [
                {
                    "state": "proposed_experimental",
                    "intentId": "intent.experimental.coding_agent.12345678",
                    "userNeedClaimId": "purpose",
                    "nearbyIntentIds": ["intent.ai.coding_agent"],
                    "nearbyIntentClaimIds": ["nearby"],
                    "nonGoalClaimIds": ["non_goal"],
                }
            ],
        }
    }
    quality = {
        "metrics": {"schemaValid": True, "evidenceSupportRate": 1.0},
        "diagnostics": [{"code": "experimental_intent_false_novelty_risk"}],
    }
    target = {"purposeConceptGroups": [["coding"], ["agent"]]}

    metrics = target_metrics(target, semantic_pass, quality, "experimental_required")

    assert metrics["falseNovelty"] is True
    assert "false_novelty" in metrics["reviewerEditReasons"]
    assert metrics["reviewerEditBurdenRate"] == 0.25


def test_runner_accounts_for_four_targets_and_preserves_non_authority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    rubric = json.loads(RUBRIC.read_text())
    candidate_root = tmp_path / "candidates"
    source_root = tmp_path / "sources"
    manifest_root = tmp_path / "manifest"
    manifest_root.mkdir()
    (manifest_root / "repositories.yml").write_text("repositories: []\n", encoding="utf-8")
    for target in rubric["targets"]:
        create_candidate(candidate_root, target["repositoryId"], target["candidateDirectory"])
        source = source_root / target["repositoryId"]
        source.mkdir(parents=True)
        (source / "README.md").write_text("Documented repository outcome.\n", encoding="utf-8")

    monkeypatch.setattr(
        "spec_harvester.experimental_intent_calibration._source_revisions",
        lambda _path: {repository_id: "a" * 40 for repository_id in EXPECTED_REPOSITORY_IDS},
    )
    monkeypatch.setattr(
        "spec_harvester.experimental_intent_calibration._validate_source_checkout",
        lambda _source, _revision: None,
    )
    output = tmp_path / "report.json"

    report = run_experimental_intent_calibration(
        plan_path=PLAN,
        rubric_path=RUBRIC,
        candidate_root=candidate_root,
        source_root=source_root,
        source_manifest_dir=manifest_root,
        provider=FocusAwareProvider(),
        output_path=output,
    )

    assert output.is_file()
    assert report["summary"]["completedCount"] == 4
    assert report["summary"]["evidenceSupportedExperimentalIntentCount"] == 4
    assert report["summary"]["falseNoveltyCount"] == 0
    assert report["decision"] == {
        "p55T10CUnblocked": True,
        "thresholdsRedefined": False,
        "maintainerDecisionRecorded": False,
    }
    assert all(value is False for value in report["executionBoundary"].values())
    assert all(value is False for value in report["privacy"].values())
    assert "/users/" not in output.read_text().lower()


def test_summary_keeps_failures_in_frozen_gate_denominators() -> None:
    records = [
        {"status": "failed", "providerAttemptCount": 2},
        *[
            {
                "status": "completed",
                "providerAttemptCount": 1,
                "intentDecisions": [],
                "metrics": {
                    "purposeAccurate": True,
                    "evidenceSupportRate": 1.0,
                    "schemaValid": True,
                    "reviewerEditBurdenRate": 0.0,
                    "experimentalIntentCount": 0,
                    "evidenceSupportedExperimentalIntentCount": 0,
                    "justifiedReuseCount": 1,
                    "nearbyIntentDifferentiated": False,
                    "falseNovelty": False,
                },
            }
            for _index in range(3)
        ],
    ]

    summary = summarize_calibration(records, load_semantic_author_quality_policy())

    assert summary["completedCount"] == 3
    assert summary["failedCount"] == 1
    assert summary["providerAttemptCount"] == 5
    assert summary["metrics"]["purposeAccuracyRate"] == 0.75
    assert summary["metrics"]["reviewerEditBurdenRate"] == 0.25
    assert summary["frozenQualityGates"]["purposeAccuracyRate"]["passed"] is False
    assert canonical_digest(json.loads(RUBRIC.read_text())) == (
        "3346390190767c20c8067c0aa3dc71860173d044c4175afda88d27387e6c34ff"
    )


def test_real_evidence_passes_frozen_gates_with_useful_bounded_novelty() -> None:
    report = json.loads(EVIDENCE.read_text())
    summary = report["summary"]

    assert report["scope"] == {
        "fullFrozenTargetSet": True,
        "repositoryIds": list(EXPECTED_REPOSITORY_IDS),
    }
    assert report["provider"]["modelId"] == "gpt-5.3-codex-spark"
    assert summary["completedCount"] == 4
    assert summary["failedCount"] == 0
    assert summary["providerAttemptCount"] == 5
    assert summary["evidenceSupportedExperimentalIntentCount"] == 3
    assert summary["experimentalIntentProposalRate"] == 0.75
    assert summary["falseNoveltyCount"] == 0
    assert summary["duplicateExperimentalIntentIdCount"] == 0
    assert summary["metrics"] == {
        "purposeAccuracyRate": 1.0,
        "evidenceSupportedClaimRate": 1.0,
        "schemaValidProposalRate": 1.0,
        "reviewerEditBurdenRate": 0.0625,
    }
    assert all(gate["passed"] for gate in summary["frozenQualityGates"].values())
    assert report["decision"] == {
        "p55T10CUnblocked": True,
        "thresholdsRedefined": False,
        "maintainerDecisionRecorded": False,
    }


def test_real_evidence_preserves_rtk_gap_and_recovered_provider_failure() -> None:
    report = json.loads(EVIDENCE.read_text())
    records = {record["repositoryId"]: record for record in report["records"]}

    assert records["rtk-ai-rtk"]["metrics"]["experimentalIntentCount"] == 0
    assert records["rtk-ai-rtk"]["metrics"]["reviewerEditReasons"] == [
        "experimental_intent_missing_or_unsupported"
    ]
    assert records["rtk-ai-rtk"]["metrics"]["justifiedReuseCount"] == 0
    assert records["openai-codex"]["providerAttemptCount"] == 2
    assert (
        "generic observed intent reuse lacks an explicit comparison claim"
        in records["openai-codex"]["priorAttemptFailureCodes"][0]
    )
    experimental_ids = {
        repository_id: [
            decision["intentId"]
            for decision in record["intentDecisions"]
            if decision["state"] == "proposed_experimental"
        ]
        for repository_id, record in records.items()
    }
    assert experimental_ids["openai-codex"] == ["intent.experimental.local_coding_agent.48e6a87f"]
    assert experimental_ids["burntsushi-ripgrep"] == [
        "intent.experimental.search_text_in_files_pattern.bbfdc65a"
    ]
    assert experimental_ids["thedotmack-claude-mem"] == [
        "intent.experimental.preserve_coding_context_sessions.c6b2134c"
    ]


def test_real_evidence_contains_no_sensitive_or_authoritative_output() -> None:
    report = json.loads(EVIDENCE.read_text())
    serialized = EVIDENCE.read_text().lower()

    assert all(value is False for value in report["privacy"].values())
    assert all(value is False for value in report["executionBoundary"].values())
    for forbidden in (
        "/users/egor",
        "api_key",
        "authorization",
        '"rawprompt"',
        '"rawresponse"',
    ):
        assert forbidden not in serialized
