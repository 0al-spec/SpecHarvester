from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.semantic_author_input_pack import (
    SemanticAuthorInputPackOptions,
    build_semantic_author_input_pack,
)
from spec_harvester.semantic_author_pass import (
    ProviderCompletion,
    SemanticAuthorPassOptions,
    run_semantic_author_pass,
)
from spec_harvester.semantic_proposal_quality import (
    evaluate_semantic_proposal_quality,
    load_semantic_author_quality_policy,
    validate_semantic_author_quality_policy,
)


class FakeProvider:
    provider_id = "test_provider"

    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def complete(
        self, provider_payload: dict, options: SemanticAuthorPassOptions
    ) -> ProviderCompletion:
        return ProviderCompletion(
            payload=copy.deepcopy(self.payload),
            receipt={"providerKind": "test", "durationMs": 1},
        )


def catalog(*intent_ids: str) -> dict:
    value = {
        "sourcePath": "catalog/observed-intents.json",
        "intents": [
            {"intentId": intent_id, "sha256": chr(97 + index) * 64}
            for index, intent_id in enumerate(intent_ids)
        ],
    }
    value["sha256"] = digest(value)
    return value


def workspace(
    tmp_path: Path,
    *,
    manifest_capability: str = "demo.package.context_selection",
    boundary_capability: str = "demo.package.context_selection",
    manifest_intent: str = "intent.ai.context_selection",
    boundary_intent: str = "intent.ai.context_selection",
) -> Path:
    (tmp_path / "specs").mkdir()
    (tmp_path / "specpm.yaml").write_text(
        "kind: SpecPackage\n"
        "metadata:\n  id: demo.package\n"
        "preview_only: true\n"
        "specs:\n  - path: specs/core.spec.yaml\n"
        "index:\n  provides:\n"
        f"    capabilities:\n      - {manifest_capability}\n"
        f"    intents:\n      - {manifest_intent}\n",
        encoding="utf-8",
    )
    (tmp_path / "specs/core.spec.yaml").write_text(
        "kind: BoundarySpec\n"
        "metadata:\n  id: demo.package\n"
        "provides:\n  capabilities:\n"
        f"    - id: {boundary_capability}\n"
        "      role: primary\n"
        "      summary: Select relevant repository context.\n"
        f"      intentIds:\n        - {boundary_intent}\n",
        encoding="utf-8",
    )
    (tmp_path / "harvest.json").write_text('{"repository":"demo"}\n', encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "Demo selects relevant repository context for AI-assisted work. "
        "It exposes a command-line interface and does not publish registry truth.\n",
        encoding="utf-8",
    )
    return tmp_path


def input_pack(tmp_path: Path, *intent_ids: str, **workspace_options: str) -> dict:
    return build_semantic_author_input_pack(
        workspace(tmp_path, **workspace_options),
        catalog(*(intent_ids or ("intent.ai.context_selection",))),
        options=SemanticAuthorInputPackOptions(document_paths=("README.md",)),
    )


def proposal(pack: dict) -> dict:
    evidence = next(
        item for item in pack["request"]["evidence"] if item["sourcePath"] == "README.md"
    )
    observed = pack["observedIntents"][0]
    result = {
        "apiVersion": "spec-harvester.ai-semantic-proposal/v0",
        "kind": "SpecHarvesterAISemanticProposal",
        "schemaVersion": 1,
        "authority": "semantic_author_proposal_only",
        "proposalId": "demo-package-semantic-v1",
        "proposalSha256": "0" * 64,
        "candidateId": pack["candidateId"],
        "sourceBundleSha256": pack["sourceBundleSha256"],
        "provider": {"id": "placeholder", "receiptSha256": "0" * 64},
        "claims": [
            claim(
                "purpose",
                "purpose",
                "Select relevant repository context for AI-assisted work.",
                evidence,
            ),
            claim("capability", "capability", "Select relevant repository context.", evidence),
            claim("interface", "interface", "Expose a command-line interface.", evidence),
            claim(
                "nearby",
                "nearby_intent_difference",
                "Focus on context rather than broad AI tooling.",
                evidence,
            ),
            claim("non_goal", "non_goal", "Do not publish registry truth.", evidence),
        ],
        "intentDecisions": [
            {
                "apiVersion": "spec-harvester.ai-semantic-intent-reuse/v0",
                "kind": "SpecHarvesterAISemanticIntentReuse",
                "schemaVersion": 1,
                "state": "proposed_reuse",
                "intentId": observed["intentId"],
                "observedIntentSha256": observed["observedIntentSha256"],
                "rationaleClaimId": "nearby",
            },
            {
                "apiVersion": "spec-harvester.ai-semantic-experimental-intent/v0",
                "kind": "SpecHarvesterAISemanticExperimentalIntent",
                "schemaVersion": 1,
                "state": "proposed_experimental",
                "intentId": (
                    f"intent.experimental.ai_context_optimization.{pack['sourceBundleSha256'][:8]}"
                ),
                "userNeedClaimId": "purpose",
                "nearbyIntentIds": [observed["intentId"]],
                "nearbyIntentClaimIds": ["nearby"],
                "nonGoalClaimIds": ["non_goal"],
            },
        ],
    }
    if observed["intentId"].startswith("intent.package.") or observed["intentId"].startswith(
        "intent.repository."
    ):
        result["intentDecisions"] = result["intentDecisions"][:1]
    return result


def claim(claim_id: str, kind: str, text: str, evidence: dict) -> dict:
    return {"id": claim_id, "kind": kind, "text": text, "evidence": [dict(evidence)]}


def semantic_pass(pack: dict, payload: dict | None = None) -> dict:
    return run_semantic_author_pass(pack, FakeProvider(payload or proposal(pack)))


def refresh_proposal_digest(pass_report: dict) -> None:
    value = pass_report["proposal"]
    value["proposalSha256"] = digest(
        {key: item for key, item in value.items() if key != "proposalSha256"}
    )


def diagnostic_codes(report: dict) -> set[str]:
    return {item["code"] for item in report["diagnostics"]}


def digest(value: dict) -> str:
    payload = {key: item for key, item in value.items() if key != "sha256"}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def test_clean_quality_report_is_deterministic_and_eligible(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)

    first = evaluate_semantic_proposal_quality(pack, passed)
    second = evaluate_semantic_proposal_quality(pack, passed)

    assert first == second
    assert first["status"] == "eligible_for_calibration"
    assert first["summary"] == {"errorCount": 0, "warningCount": 0, "diagnosticCount": 0}
    assert first["metrics"]["schemaValid"] is True
    assert first["metrics"]["evidenceSupportRate"] == 1.0
    assert all(value is False for value in first["executionBoundary"].values())


def test_frozen_policy_has_exact_metrics_and_digest() -> None:
    policy = load_semantic_author_quality_policy()

    validate_semantic_author_quality_policy(policy)
    assert policy["metrics"] == {
        "purposeAccuracyRate": {"operator": "greater_than_or_equal", "threshold": 0.85},
        "evidenceSupportedClaimRate": {"operator": "greater_than_or_equal", "threshold": 0.95},
        "schemaValidProposalRate": {"operator": "equal", "threshold": 1.0},
        "reviewerEditBurdenRate": {"operator": "less_than_or_equal", "threshold": 0.25},
    }
    stale = copy.deepcopy(policy)
    stale["metrics"]["purposeAccuracyRate"]["threshold"] = 0.5
    with pytest.raises(ValueError, match="not frozen"):
        validate_semantic_author_quality_policy(stale)
    stale = copy.deepcopy(policy)
    stale["policySha256"] = "f" * 64
    with pytest.raises(ValueError, match="digest is stale"):
        validate_semantic_author_quality_policy(stale)


@pytest.mark.parametrize(
    ("workspace_options", "code"),
    [
        ({"manifest_capability": "other.context"}, "capability_namespace_violation"),
        ({"boundary_capability": "demo.package.other"}, "manifest_boundary_capability_mismatch"),
        ({"boundary_intent": "intent.ai.other"}, "manifest_boundary_intent_mismatch"),
    ],
)
def test_candidate_namespace_and_boundary_mismatches_reject(
    tmp_path: Path, workspace_options: dict[str, str], code: str
) -> None:
    pack = input_pack(tmp_path, **workspace_options)
    report = evaluate_semantic_proposal_quality(pack, semantic_pass(pack))

    assert report["status"] == "rejected"
    assert code in diagnostic_codes(report)


def test_stale_evidence_and_envelope_bindings_reject(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    pack["evidence"][0]["content"] += "tampered"
    passed["sourceBundleSha256"] = "f" * 64

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert {"evidence_content_binding_stale", "source_bundle_binding_mismatch"} <= diagnostic_codes(
        report
    )


def test_stale_request_binding_rejects(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    pack["request"]["sourceBundleSha256"] = "f" * 64

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "request_binding_mismatch" in diagnostic_codes(report)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("apiVersion", "spec-harvester.experimental-intent-decision-policy/v1"),
        ("kind", "OtherExperimentalIntentDecisionPolicy"),
    ),
)
def test_policy_binding_identity_rejects(tmp_path: Path, field: str, value: str) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    passed["experimentalIntentDecisionPolicy"][field] = value

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "experimental_intent_policy_binding_invalid" in diagnostic_codes(report)


def test_quality_rejects_candidate_namespace_in_experimental_identifier(
    tmp_path: Path,
) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    passed["proposal"]["intentDecisions"][1]["intentId"] = (
        f"intent.experimental.demo_context.{pack['sourceBundleSha256'][:8]}"
    )
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "experimental_intent_identifier_leaks_candidate_namespace" in diagnostic_codes(report)


def test_quality_rejects_unbound_nearby_intent_comparison(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    decision = passed["proposal"]["intentDecisions"][1]
    decision["nearbyIntentIds"].append("intent.ai.second_observed")
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "experimental_intent_nearby_binding_count_mismatch" in diagnostic_codes(report)


def test_recomputed_source_bundle_digest_rejects_coordinated_evidence_tampering(
    tmp_path: Path,
) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    readme = next(item for item in pack["evidence"] if item["sourcePath"] == "README.md")
    readme["content"] += " Altered after pack creation."
    readme["byteCount"] = len(readme["content"].encode())
    readme["sha256"] = hashlib.sha256(readme["content"].encode()).hexdigest()
    request_readme = next(
        item for item in pack["request"]["evidence"] if item["sourcePath"] == "README.md"
    )
    request_readme["sha256"] = readme["sha256"]
    for claim_record in passed["proposal"]["claims"]:
        for evidence in claim_record["evidence"]:
            if evidence["sourcePath"] == "README.md":
                evidence["sha256"] = readme["sha256"]
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "source_bundle_digest_stale" in diagnostic_codes(report)


def test_unknown_evidence_and_invalid_identifier_reject(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    passed["proposal"]["claims"][0]["evidence"][0]["sourcePath"] = "forged.md"
    passed["proposal"]["intentDecisions"][1]["intentId"] = "not-an-intent"
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert {"proposal_schema_invalid", "claim_evidence_not_allowlisted"} <= diagnostic_codes(report)


def test_provider_authority_wording_and_unsupported_quantity_reject(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    passed["proposal"]["claims"][0]["text"] = (
        "According to the provider, the model approves a 50% token reduction."
    )
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert {
        "provider_specific_authority_wording",
        "unsupported_quantitative_claim",
    } <= diagnostic_codes(report)


def test_supported_quantitative_claim_is_allowed(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    readme = next(item for item in pack["evidence"] if item["sourcePath"] == "README.md")
    readme["content"] += "Measured reduction is 50%.\n"
    readme["byteCount"] = len(readme["content"].encode())
    readme["sha256"] = hashlib.sha256(readme["content"].encode()).hexdigest()
    binding = next(
        item for item in pack["request"]["evidence"] if item["sourcePath"] == "README.md"
    )
    binding["sha256"] = readme["sha256"]
    passed = semantic_pass(pack)
    passed["proposal"]["claims"][0]["text"] = "Measured reduction is 50%."
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert "unsupported_quantitative_claim" not in diagnostic_codes(report)


def test_quantitative_claim_requires_exact_evidence_token(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    readme = next(item for item in pack["evidence"] if item["sourcePath"] == "README.md")
    readme["content"] += "Measured reduction is 50%.\n"
    readme["byteCount"] = len(readme["content"].encode())
    readme["sha256"] = hashlib.sha256(readme["content"].encode()).hexdigest()
    binding = next(
        item for item in pack["request"]["evidence"] if item["sourcePath"] == "README.md"
    )
    binding["sha256"] = readme["sha256"]
    passed = semantic_pass(pack)
    passed["proposal"]["claims"][0]["text"] = "Measured reduction is 5%."
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert "unsupported_quantitative_claim" in diagnostic_codes(report)


def test_generic_duplicate_and_overlap_signals_require_review(tmp_path: Path) -> None:
    pack = input_pack(tmp_path, "intent.package.javascript_library")
    passed = semantic_pass(pack)
    passed["proposal"]["intentDecisions"].append(
        copy.deepcopy(passed["proposal"]["intentDecisions"][0])
    )
    duplicate_claim = copy.deepcopy(passed["proposal"]["claims"][1])
    duplicate_claim["id"] = "capability_duplicate"
    passed["proposal"]["claims"].append(duplicate_claim)
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "review_required"
    assert {
        "generic_intent_reuse",
        "duplicate_intent_decision",
        "overlapping_semantic_claims",
    } <= diagnostic_codes(report)


def test_experimental_intent_overlap_is_false_novelty_failure(tmp_path: Path) -> None:
    pack = input_pack(tmp_path, "intent.ai.context_optimization")
    passed = semantic_pass(pack)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert {
        "experimental_intent_overlaps_observed",
        "experimental_intent_false_novelty_risk",
    } <= diagnostic_codes(report)


def test_duplicate_experimental_intent_rejects(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    passed["proposal"]["intentDecisions"].append(
        copy.deepcopy(passed["proposal"]["intentDecisions"][1])
    )
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "duplicate_experimental_intent" in diagnostic_codes(report)


@pytest.mark.parametrize(
    ("decision_index", "field"),
    [
        (0, "rationaleClaimId"),
        (1, "userNeedClaimId"),
        (1, "nonGoalClaimIds"),
    ],
)
def test_unknown_intent_claim_reference_rejects(
    tmp_path: Path, decision_index: int, field: str
) -> None:
    pack = input_pack(tmp_path)
    passed = semantic_pass(pack)
    decision = passed["proposal"]["intentDecisions"][decision_index]
    decision[field] = ["missing"] if field == "nonGoalClaimIds" else "missing"
    refresh_proposal_digest(passed)

    report = evaluate_semantic_proposal_quality(pack, passed)

    assert report["status"] == "rejected"
    assert "intent_claim_reference_unknown" in diagnostic_codes(report)


def test_missing_proposal_returns_rejected_report(tmp_path: Path) -> None:
    pack = input_pack(tmp_path)
    report = evaluate_semantic_proposal_quality(pack, {})

    assert report["status"] == "rejected"
    assert report["metrics"]["schemaValid"] is False
    assert diagnostic_codes(report) == {"proposal_record_missing"}


def test_docs_describe_quality_states_thresholds_and_authority_boundary() -> None:
    root = Path(__file__).resolve().parents[1]
    documents = (
        root / "docs/SEMANTIC_PROPOSAL_QUALITY.md",
        root / "Sources/SpecHarvester/Documentation.docc/SemanticProposalQuality.md",
    )
    for path in documents:
        text = " ".join(path.read_text(encoding="utf-8").split())
        for required in (
            "P55-T5",
            "P55-T9",
            "0.85",
            "0.95",
            "1.0",
            "0.25",
            "materialize",
            "SpecPM",
        ):
            assert required in text
