from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

import spec_harvester.semantic_materialization as semantic_materialization
from spec_harvester.cli import main
from spec_harvester.local_candidate_review_details import (
    _comparison,
    _detail_sections,
)
from spec_harvester.local_review_decision_service import LocalReviewDecisionStore
from spec_harvester.p53_portable_author_handoff import copy_semantic_proposal
from spec_harvester.portable_semantic_proposal import (
    _validate_receipt,
    build_portable_semantic_proposal,
    build_portable_semantic_proposal_from_directory,
    validate_portable_semantic_proposal,
)
from spec_harvester.semantic_author_input_pack import build_semantic_author_input_pack
from spec_harvester.semantic_author_pass import (
    ProviderCompletion,
    SemanticAuthorPassOptions,
    run_semantic_author_pass,
)
from spec_harvester.semantic_materialization import (
    SemanticMaterializationOptions,
    materialize_semantic_candidate,
)
from spec_harvester.semantic_proposal_quality import evaluate_semantic_proposal_quality
from spec_harvester.semantic_review import (
    build_semantic_reviewer_edit,
    validate_semantic_reviewer_edit,
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
            receipt={
                "providerKind": "test",
                "durationMs": 1,
                "rawPrompt": "must not survive normalization",
            },
        )


def semantic_triplet(tmp_path: Path, candidate_id: str = "demo.package") -> tuple[dict, ...]:
    workspace = tmp_path / "workspace"
    (workspace / "specs").mkdir(parents=True)
    (workspace / "specpm.yaml").write_text(
        "kind: SpecPackage\n"
        f"metadata:\n  id: {candidate_id}\n"
        "preview_only: true\n"
        "specs:\n  - path: specs/core.spec.yaml\n"
        "index:\n  provides:\n"
        f"    capabilities:\n      - {candidate_id}.context_selection\n"
        "    intents:\n      - intent.ai.context_selection\n",
        encoding="utf-8",
    )
    (workspace / "specs/core.spec.yaml").write_text(
        "kind: BoundarySpec\n"
        f"metadata:\n  id: {candidate_id}\n"
        "provides:\n  capabilities:\n"
        f"    - id: {candidate_id}.context_selection\n"
        "      role: primary\n"
        "      summary: Select relevant repository context.\n"
        "      intentIds:\n        - intent.ai.context_selection\n",
        encoding="utf-8",
    )
    (workspace / "harvest.json").write_text('{"repository":"demo"}\n', encoding="utf-8")
    (workspace / "README.md").write_text(
        "Select relevant repository context through a command-line interface.\n",
        encoding="utf-8",
    )
    catalog_payload = {
        "sourcePath": "catalog/intents.json",
        "intents": [{"intentId": "intent.ai.context_selection", "sha256": "a" * 64}],
    }
    catalog = {
        **catalog_payload,
        "sha256": digest(catalog_payload),
    }
    pack = build_semantic_author_input_pack(workspace, catalog)
    evidence = pack["request"]["evidence"][0]
    payload = {
        "apiVersion": "spec-harvester.ai-semantic-proposal/v0",
        "kind": "SpecHarvesterAISemanticProposal",
        "schemaVersion": 1,
        "authority": "semantic_author_proposal_only",
        "proposalId": f"{candidate_id}-semantic-v1",
        "proposalSha256": "0" * 64,
        "candidateId": candidate_id,
        "sourceBundleSha256": pack["sourceBundleSha256"],
        "provider": {"id": "placeholder", "receiptSha256": "0" * 64},
        "claims": [
            claim("purpose", "purpose", "Select relevant repository context.", evidence),
            claim("capability", "capability", "Select relevant repository context.", evidence),
            claim("interface", "interface", "Expose a command-line interface.", evidence),
            claim(
                "nearby",
                "nearby_intent_difference",
                "Focus on repository context selection.",
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
                "intentId": pack["observedIntents"][0]["intentId"],
                "observedIntentSha256": pack["observedIntents"][0]["observedIntentSha256"],
                "rationaleClaimId": "nearby",
            }
        ],
    }
    semantic_pass = run_semantic_author_pass(pack, FakeProvider(payload))
    quality = evaluate_semantic_proposal_quality(pack, semantic_pass)
    return pack, semantic_pass, quality


def claim(claim_id: str, kind: str, text: str, evidence: dict) -> dict:
    return {"id": claim_id, "kind": kind, "text": text, "evidence": [dict(evidence)]}


def digest(value: dict) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def write_triplet(root: Path, triplet: tuple[dict, ...]) -> None:
    root.mkdir(parents=True)
    for name, value in zip(
        ("input-pack.json", "semantic-pass.json", "quality-report.json"),
        triplet,
        strict=True,
    ):
        (root / name).write_text(json.dumps(value), encoding="utf-8")


def test_builds_deterministic_complete_portable_record(tmp_path: Path) -> None:
    triplet = semantic_triplet(tmp_path)

    first = build_portable_semantic_proposal(*triplet)
    second = build_portable_semantic_proposal(*triplet)

    assert first == second
    assert first["qualityStatus"] == "eligible_for_calibration"
    assert first["proposal"] == triplet[1]["proposal"]
    assert first["qualityReport"] == triplet[2]
    assert first["providerReceipt"] == triplet[1]["providerReceipt"]
    assert first["privacy"] == {
        "rawPromptsPersisted": False,
        "rawProviderResponsesPersisted": False,
        "chainOfThoughtPersisted": False,
        "credentialsPersisted": False,
        "providerLocalPathsPersisted": False,
    }
    assert "rawPrompt" not in first["providerReceipt"]
    validate_portable_semantic_proposal(first)


def test_rejects_stale_quality_and_sensitive_receipt_fields(tmp_path: Path) -> None:
    pack, semantic_pass, quality = semantic_triplet(tmp_path)
    stale = copy.deepcopy(quality)
    stale["summary"]["warningCount"] += 1
    with pytest.raises(ValueError, match="quality report is stale"):
        build_portable_semantic_proposal(pack, semantic_pass, stale)

    sensitive = copy.deepcopy(semantic_pass)
    sensitive["providerReceipt"]["rawResponse"] = "secret"
    with pytest.raises(ValueError, match="fields are invalid"):
        build_portable_semantic_proposal(pack, sensitive, quality)

    incomplete = copy.deepcopy(semantic_pass)
    incomplete["providerReceipt"].pop("rawPromptPersisted")
    with pytest.raises(ValueError, match="fields are invalid"):
        build_portable_semantic_proposal(pack, incomplete, quality)


@pytest.mark.parametrize(
    ("record_name", "mutation"),
    [
        ("input", ("authority", "other")),
        ("input", ("executionBoundary", {"providerInvoked": True})),
        ("pass", ("apiVersion", "other")),
        ("pass", ("authority", "materialization_authority")),
        ("pass", ("executionBoundary", {"materializationPerformed": True})),
        ("quality", ("authority", "decision_authority")),
        ("quality", ("executionBoundary", {"specpmMutated": True})),
    ],
)
def test_rejects_source_record_identity_and_authority_drift(
    tmp_path: Path, record_name: str, mutation: tuple[str, object]
) -> None:
    pack, semantic_pass, quality = semantic_triplet(tmp_path)
    target = {"input": pack, "pass": semantic_pass, "quality": quality}[record_name]
    target[mutation[0]] = mutation[1]

    with pytest.raises(ValueError, match="inputs are malformed"):
        build_portable_semantic_proposal(pack, semantic_pass, quality)


def test_build_rejects_noncanonical_nested_receipt_values(tmp_path: Path) -> None:
    pack, semantic_pass, _quality = semantic_triplet(tmp_path)
    receipt = semantic_pass["providerReceipt"]
    receipt["usage"] = {"apiKey": "super-secret"}
    receipt["receiptSha256"] = digest(
        {key: value for key, value in receipt.items() if key != "receiptSha256"}
    )
    proposal = semantic_pass["proposal"]
    proposal["provider"]["receiptSha256"] = receipt["receiptSha256"]
    proposal["proposalSha256"] = digest(
        {key: value for key, value in proposal.items() if key != "proposalSha256"}
    )
    quality = evaluate_semantic_proposal_quality(pack, semantic_pass)

    with pytest.raises(ValueError, match="receipt is invalid"):
        build_portable_semantic_proposal(pack, semantic_pass, quality)


def test_directory_and_handoff_pointer_preserve_all_digests(tmp_path: Path) -> None:
    source = tmp_path / "semantic" / "demo.package"
    write_triplet(source, semantic_triplet(tmp_path))
    record = build_portable_semantic_proposal_from_directory(source)
    packet_dir = tmp_path / "packet"
    packet_dir.mkdir()

    pointer = copy_semantic_proposal("demo.package", packet_dir, tmp_path / "semantic")

    assert pointer["status"] == "complete_portable"
    assert pointer["recordSha256"] == record["recordSha256"]
    assert pointer["proposalSha256"] == record["proposalSha256"]
    assert pointer["providerReceiptSha256"] == record["providerReceiptSha256"]
    assert pointer["qualityReportSha256"] == record["qualityReportSha256"]
    assert copy_semantic_proposal("missing", packet_dir, tmp_path / "semantic") == {
        "status": "not_available"
    }


def test_detail_surface_carries_inert_record_and_digest_comparison(tmp_path: Path) -> None:
    source = tmp_path / "semantic" / "demo.package"
    write_triplet(source, semantic_triplet(tmp_path))
    packet_dir = tmp_path / "packet"
    packet_dir.mkdir()
    pointer = copy_semantic_proposal("demo.package", packet_dir, tmp_path / "semantic")
    payload = (packet_dir / "semantic-proposal-record.json").read_bytes()
    package_yaml = (
        b"kind: SpecPackage\n"
        b"metadata:\n"
        b"  id: demo.package\n"
        b"  summary: Static package summary.\n"
        b"index:\n"
        b"  provides:\n"
        b"    capabilities:\n"
        b"      - demo.package.context_selection\n"
        b"    intents:\n"
        b"      - intent.ai.context_selection\n"
    )
    boundary_yaml = (
        b"kind: BoundarySpec\n"
        b"metadata:\n"
        b"  id: demo.package.core\n"
        b"intent:\n"
        b"  summary: Static boundary summary.\n"
        b"provides:\n"
        b"  capabilities:\n"
        b"    - id: demo.package.context_selection\n"
        b"      summary: Select repository context.\n"
        b"      intentIds:\n"
        b"        - intent.ai.context_selection\n"
        b"interfaces:\n"
        b"  inbound:\n"
        b"    - id: demo.package.cli\n"
        b"      kind: command-line\n"
        b"      summary: Command-line interface.\n"
        b"  outbound: []\n"
        b"evidence:\n"
        b"  - path: README.md\n"
    )
    files = [
        {"path": "specpm.yaml"},
        {"path": "specs/core.spec.yaml"},
    ]
    packet = {
        "candidate": {
            "fileCount": 2,
            "manifestCount": 1,
            "status": "portable",
            "files": files,
        },
        "repository": {"id": "demo.package"},
        "triage": {"status": "completed"},
        "aiProposal": {"status": "summary_only_not_portable", "summary": {}},
        "semanticProposal": pointer,
    }
    members = {
        "packets/demo.package/packet.json": (
            json.dumps(packet, indent=2, sort_keys=True) + "\n"
        ).encode(),
        "packets/demo.package/semantic-proposal-record.json": payload,
        "packets/demo.package/specpm.yaml": package_yaml,
        "packets/demo.package/specs/core.spec.yaml": boundary_yaml,
    }

    sections = _detail_sections("demo.package", packet, members)
    comparison = _comparison("demo.package", "a" * 64, packet, members)

    semantic_section = next(item for item in sections if item["id"] == "semantic-proposal-record")
    assert semantic_section["contentType"] == "application/json"
    assert json.loads(semantic_section["content"])["recordSha256"] == pointer["recordSha256"]
    assert comparison["ai"] == {
        "status": "complete_portable",
        "proposalSha256": pointer["proposalSha256"],
        "semanticRecordSha256": pointer["recordSha256"],
        "qualityReportSha256": pointer["qualityReportSha256"],
        "providerReceiptSha256": pointer["providerReceiptSha256"],
        "sourceBundleSha256": json.loads(payload)["sourceBundleSha256"],
        "qualityStatus": "eligible_for_calibration",
        "warningCount": 0,
    }
    assert comparison["semantic"]["ai"]["claims"]["purpose"][0]["text"] == (
        "Select relevant repository context."
    )
    assert comparison["semantic"]["ai"]["observedIntentReuse"] == [
        {
            "intentId": "intent.ai.context_selection",
            "rationaleClaimId": "nearby",
        }
    ]
    assert comparison["semantic"]["ai"]["experimentalIntents"] == []
    assert comparison["semantic"]["binding"]["semanticRecordSha256"] == pointer["recordSha256"]
    assert comparison["semantic"]["static"] == {
        "summaries": ["Static package summary.", "Static boundary summary."],
        "capabilities": [
            {
                "id": "demo.package.context_selection",
                "summary": "",
                "intentIds": [],
            },
            {
                "id": "demo.package.context_selection",
                "summary": "Select repository context.",
                "intentIds": ["intent.ai.context_selection"],
            },
        ],
        "intents": ["intent.ai.context_selection"],
        "interfaces": ["demo.package.cli · command-line · Command-line interface."],
        "evidence": ["README.md"],
    }


def test_semantic_reviewer_edit_is_digest_bound_and_decision_service_portable(
    tmp_path: Path,
) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    candidate_id = record["candidateId"]
    semantic_pointer = {
        "status": "complete_portable",
        "path": "semantic-proposal-record.json",
        "recordSha256": record["recordSha256"],
        "proposalSha256": record["proposalSha256"],
        "providerReceiptSha256": record["providerReceiptSha256"],
        "qualityReportSha256": record["qualityReportSha256"],
        "qualityStatus": record["qualityStatus"],
    }
    packet_content = (
        json.dumps(
            {"repository": {"id": candidate_id}, "semanticProposal": semantic_pointer},
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    packet_sha256 = hashlib.sha256(packet_content.encode()).hexdigest()
    catalog = {
        "apiVersion": "spec-harvester.candidate-review-catalog/v0",
        "kind": "SpecHarvesterCandidateReviewCatalog",
        "authority": "local_review_catalog_evidence_only",
        "sourceBundleSha256": record["sourceBundleSha256"],
        "items": [
            {
                "candidateId": candidate_id,
                "packetSha256": packet_sha256,
                "reviewState": "unreviewed",
                "readiness": "ready_for_author_review",
                "ecosystem": "python",
                "packageShape": "single",
                "warningCount": 0,
                "corrected": False,
                "preflightStatus": "passed",
            }
        ],
    }
    catalog_path = tmp_path / "catalog.json"
    catalog_path.write_text(json.dumps(catalog))
    details = {
        "sourceBundleSha256": record["sourceBundleSha256"],
        "details": [
            {
                "binding": {"candidateId": candidate_id, "packetSha256": packet_sha256},
                "sections": [
                    {
                        "id": "packet-binding.json",
                        "contentType": "application/json",
                        "content": packet_content,
                    },
                    {
                        "id": "semantic-proposal-record",
                        "contentType": "application/json",
                        "content": json.dumps(record),
                    },
                ],
            }
        ],
    }
    details_path = tmp_path / "details.json"
    details_path.write_text(json.dumps(details))
    store = LocalReviewDecisionStore(tmp_path / "review", catalog_path, details_path)
    semantic_action = {
        "decision": "edited",
        "acceptedOrEditedClaimIds": ["purpose", "capability"],
        "editedClaims": [{"claimId": "purpose", "text": "Choose relevant context for a task."}],
        "proposalSha256": record["proposalSha256"],
        "sourceBundleSha256": record["sourceBundleSha256"],
        "semanticRecordSha256": record["recordSha256"],
    }

    result = store.record_action(
        {
            "candidateId": candidate_id,
            "disposition": "request_revision",
            "reviewer": "maintainer@example",
            "reasonCode": "evidence_revision_required",
            "notes": "Purpose needs a concise edit.",
            "priorDecisionSha256": None,
            "semanticAction": semantic_action,
        }
    )

    current = store.current(candidate_id)
    assert current is not None
    review = current["decision"]["semanticReview"]
    assert review["decision"] == "edited"
    assert review["editedClaims"] == semantic_action["editedClaims"]
    assert result["decisionSha256"]
    validate_semantic_reviewer_edit(review, record)
    exported = store.export()
    assert (
        exported["decisions"][0]["semanticReview"]["semanticRecordSha256"]
        == (record["recordSha256"])
    )

    other_pack, other_pass, _other_quality = semantic_triplet(tmp_path / "other")
    other_pass["proposal"]["claims"][0]["text"] = "Choose task-relevant context."
    other_pass["proposal"]["proposalSha256"] = digest(
        {key: value for key, value in other_pass["proposal"].items() if key != "proposalSha256"}
    )
    other_quality = evaluate_semantic_proposal_quality(other_pack, other_pass)
    substituted_record = build_portable_semantic_proposal(other_pack, other_pass, other_quality)
    substituted = json.loads(details_path.read_text())
    substituted["details"][0]["sections"][1]["content"] = json.dumps(substituted_record)
    substituted_path = tmp_path / "substituted-details.json"
    substituted_path.write_text(json.dumps(substituted))
    with pytest.raises(ValueError, match="differs from bound packet"):
        LocalReviewDecisionStore(tmp_path / "substituted", catalog_path, substituted_path)
    without_details = LocalReviewDecisionStore(tmp_path / "review-without-details", catalog_path)
    with pytest.raises(ValueError, match="Semantic proposal is unavailable"):
        without_details.record_action(
            {
                "candidateId": candidate_id,
                "disposition": "request_revision",
                "reviewer": "maintainer@example",
                "reasonCode": "evidence_revision_required",
                "notes": "",
                "priorDecisionSha256": None,
                "semanticAction": semantic_action,
            }
        )


def test_semantic_reviewer_edit_rejects_stale_unknown_and_incoherent_edits(
    tmp_path: Path,
) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    base = {
        "decision": "accepted",
        "acceptedOrEditedClaimIds": ["purpose"],
        "editedClaims": [],
        "proposalSha256": record["proposalSha256"],
        "sourceBundleSha256": record["sourceBundleSha256"],
        "semanticRecordSha256": record["recordSha256"],
    }
    valid = build_semantic_reviewer_edit(base, record, "maintainer@example")
    validate_semantic_reviewer_edit(valid, record)
    invalid_digest = copy.deepcopy(valid)
    invalid_digest["reviewerEditSha256"] = "0" * 64
    with pytest.raises(ValueError, match="digest is invalid"):
        validate_semantic_reviewer_edit(invalid_digest, record)

    for mutation, message in (
        ({"acceptedOrEditedClaimIds": []}, "requires selected claims"),
        ({"proposalSha256": "0" * 64}, "binding is stale"),
        ({"acceptedOrEditedClaimIds": ["unknown"]}, "unknown claim"),
        (
            {
                "decision": "edited",
                "acceptedOrEditedClaimIds": ["purpose"],
                "editedClaims": [],
            },
            "requires edited claim text",
        ),
        (
            {
                "decision": "edited",
                "acceptedOrEditedClaimIds": ["purpose"],
                "editedClaims": [
                    {"claimId": "purpose", "text": "First"},
                    {"claimId": "purpose", "text": "Second"},
                ],
            },
            "duplicate edited claims",
        ),
        (
            {
                "decision": "edited",
                "acceptedOrEditedClaimIds": ["capability"],
                "editedClaims": [{"claimId": "purpose", "text": "Unselected edit"}],
            },
            "not selected",
        ),
        (
            {
                "decision": "accepted",
                "editedClaims": [{"claimId": "purpose", "text": "Unexpected edit"}],
            },
            "Only an edited",
        ),
        (
            {
                "decision": "rejected",
                "acceptedOrEditedClaimIds": ["purpose"],
            },
            "cannot select claims",
        ),
        (
            {
                "decision": "edited",
                "acceptedOrEditedClaimIds": ["purpose"],
                "editedClaims": [{"claimId": "purpose", "text": "x" * 17000}],
            },
            "byte limit|too long",
        ),
    ):
        action = {**base, **mutation}
        with pytest.raises(ValueError, match=message):
            build_semantic_reviewer_edit(action, record, "maintainer@example")

    invalid_shape = dict(base)
    invalid_shape.pop("editedClaims")
    with pytest.raises(ValueError, match="action shape"):
        build_semantic_reviewer_edit(invalid_shape, record, "maintainer@example")


def _materialization_candidate(root: Path) -> Path:
    candidate = root / "candidate"
    (candidate / "specs").mkdir(parents=True)
    (candidate / "specpm.yaml").write_text(
        "apiVersion: specpm.dev/v0.1\n"
        "kind: SpecPackage\n"
        "metadata:\n"
        "  id: demo.package\n"
        "  name: Demo\n"
        "  version: 0.1.0\n"
        "  summary: Generic static summary.\n"
        "preview_only: true\n"
        "specs:\n"
        "  - path: specs/core.spec.yaml\n"
        "index:\n"
        "  provides:\n"
        "    capabilities:\n"
        "      - demo.package.context_selection\n"
        "    intents:\n"
        "      - intent.package.python_library\n",
        encoding="utf-8",
    )
    (candidate / "specs/core.spec.yaml").write_text(
        "apiVersion: specpm.dev/v0.1\n"
        "kind: BoundarySpec\n"
        "metadata:\n"
        "  id: demo.package\n"
        "intent:\n"
        "  summary: Generic static summary.\n"
        "scope:\n"
        "  includes: []\n"
        "  excludes: []\n"
        "provides:\n"
        "  capabilities:\n"
        "    - id: demo.package.context_selection\n"
        "      summary: Generic capability.\n"
        "      intentIds:\n"
        "        - intent.package.python_library\n",
        encoding="utf-8",
    )
    return candidate


def _materialization_decision(
    record: dict, reviewer_edit: dict, *, candidate_id: str | None = None
) -> dict:
    return {
        "apiVersion": "spec-harvester.candidate-review-decision/v0",
        "kind": "SpecHarvesterCandidateReviewDecision",
        "authority": "local_review_decision_evidence_only",
        "binding": {
            "candidateId": candidate_id or record["candidateId"],
            "packetSha256": "a" * 64,
        },
        "disposition": "accept_for_intake",
        "reviewer": reviewer_edit["reviewer"],
        "recordedAt": "2026-07-31T12:00:00Z",
        "reasonCode": "evidence_verified",
        "priorDecisionSha256": None,
        "semanticReview": reviewer_edit,
    }


def _valid_specpm_report() -> dict:
    return {
        "status": "valid",
        "error_count": 0,
        "warning_count": 0,
        "errors": [],
        "warnings": [],
        "package_identity": {
            "package_id": "demo.package",
            "name": "Demo",
            "version": "0.1.0",
        },
        "checked_files": ["specpm.yaml", "specs/core.spec.yaml"],
        "capabilities": ["demo.package.context_selection"],
        "intents": ["intent.ai.context_selection"],
        "intent_mappings": [
            {
                "capability_id": "demo.package.context_selection",
                "intent_id": "intent.ai.context_selection",
            }
        ],
    }


def test_materializes_only_selected_semantics_into_new_preview_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    action = {
        "decision": "edited",
        "acceptedOrEditedClaimIds": [
            "purpose",
            "capability",
            "interface",
            "nearby",
            "non_goal",
        ],
        "editedClaims": [
            {"claimId": "purpose", "text": "Choose relevant repository context for a task."}
        ],
        "proposalSha256": record["proposalSha256"],
        "sourceBundleSha256": record["sourceBundleSha256"],
        "semanticRecordSha256": record["recordSha256"],
    }
    review = build_semantic_reviewer_edit(action, record, "maintainer@example")
    candidate = _materialization_candidate(tmp_path)
    before = {
        path.relative_to(candidate): path.read_bytes()
        for path in candidate.rglob("*")
        if path.is_file()
    }
    record_path = tmp_path / "record.json"
    decision_path = tmp_path / "decision.json"
    record_path.write_text(json.dumps(record))
    decision_path.write_text(json.dumps(_materialization_decision(record, review)))
    monkeypatch.setattr(
        semantic_materialization,
        "_run_specpm_validation",
        lambda *_args, **_kwargs: _valid_specpm_report(),
    )

    report = materialize_semantic_candidate(
        SemanticMaterializationOptions(
            candidate=candidate,
            semantic_record=record_path,
            review_decision=decision_path,
            output=tmp_path / "materialized",
        )
    )

    manifest = yaml.safe_load((tmp_path / "materialized/candidate/specpm.yaml").read_text())
    boundary = yaml.safe_load(
        (tmp_path / "materialized/candidate/specs/core.spec.yaml").read_text()
    )
    assert manifest["metadata"]["summary"] == "Choose relevant repository context for a task."
    assert manifest["preview_only"] is True
    assert "intent.ai.context_selection" in manifest["index"]["provides"]["intents"]
    assert boundary["provides"]["capabilities"][0]["summary"] == (
        "Select relevant repository context."
    )
    assert "Expose a command-line interface." in boundary["scope"]["includes"]
    assert "Do not publish registry truth." in boundary["scope"]["excludes"]
    assert report["validation"]["specHarvester"] == "passed"
    assert report["validation"]["specPM"]["status"] == "valid"
    assert report["registryMutationCount"] == 0
    assert json.loads((tmp_path / "materialized/materialization-report.json").read_text()) == report
    schema = json.loads(
        (
            Path(__file__).resolve().parents[1] / "schemas/semantic-materialization-v0.schema.json"
        ).read_text()
    )
    assert list(Draft202012Validator(schema).iter_errors(report)) == []
    assert {
        path.relative_to(candidate): path.read_bytes()
        for path in candidate.rglob("*")
        if path.is_file()
    } == before


def test_materialization_rejects_non_authorizing_and_stale_decisions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    candidate = _materialization_candidate(tmp_path)
    record_path = tmp_path / "record.json"
    record_path.write_text(json.dumps(record))
    monkeypatch.setattr(
        semantic_materialization,
        "_run_specpm_validation",
        lambda *_args, **_kwargs: _valid_specpm_report(),
    )
    accepted_action = {
        "decision": "accepted",
        "acceptedOrEditedClaimIds": ["purpose"],
        "editedClaims": [],
        "proposalSha256": record["proposalSha256"],
        "sourceBundleSha256": record["sourceBundleSha256"],
        "semanticRecordSha256": record["recordSha256"],
    }
    accepted_review = build_semantic_reviewer_edit(accepted_action, record, "maintainer@example")
    missing_review = _materialization_decision(record, accepted_review)
    missing_review.pop("semanticReview")
    missing_review_path = tmp_path / "missing-review.json"
    missing_review_path.write_text(json.dumps(missing_review))
    with pytest.raises(ValueError, match="Semantic review decision is missing"):
        materialize_semantic_candidate(
            SemanticMaterializationOptions(
                candidate=candidate,
                semantic_record=record_path,
                review_decision=missing_review_path,
                output=tmp_path / "output-missing-review",
            )
        )
    for decision_name, candidate_id, message in (
        ("deferred", record["candidateId"], "accepted or edited"),
        ("accepted", "other.candidate", "candidate binding is stale"),
    ):
        action = {
            "decision": decision_name,
            "acceptedOrEditedClaimIds": (["purpose"] if decision_name == "accepted" else []),
            "editedClaims": [],
            "proposalSha256": record["proposalSha256"],
            "sourceBundleSha256": record["sourceBundleSha256"],
            "semanticRecordSha256": record["recordSha256"],
        }
        review = build_semantic_reviewer_edit(action, record, "maintainer@example")
        decision_path = tmp_path / f"{decision_name}.json"
        decision_path.write_text(
            json.dumps(_materialization_decision(record, review, candidate_id=candidate_id))
        )
        with pytest.raises(ValueError, match=message):
            materialize_semantic_candidate(
                SemanticMaterializationOptions(
                    candidate=candidate,
                    semantic_record=record_path,
                    review_decision=decision_path,
                    output=tmp_path / f"output-{decision_name}",
                )
            )


def test_semantic_materialization_cli_reports_success_and_validation_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    report = {
        "apiVersion": "spec-harvester.semantic-materialization/v0",
        "status": "passed",
    }
    monkeypatch.setattr(
        "spec_harvester.cli.materialize_semantic_candidate",
        lambda _options: report,
    )
    arguments = [
        "materialize-semantic-candidate",
        "--candidate",
        str(tmp_path / "candidate"),
        "--semantic-record",
        str(tmp_path / "record.json"),
        "--review-decision",
        str(tmp_path / "decision.json"),
        "--output",
        str(tmp_path / "output"),
    ]

    assert main(arguments) == 0
    assert json.loads(capsys.readouterr().out) == report

    def reject(_options: SemanticMaterializationOptions) -> dict:
        raise ValueError("stale semantic decision")

    monkeypatch.setattr("spec_harvester.cli.materialize_semantic_candidate", reject)
    assert main(arguments) == 2
    assert json.loads(capsys.readouterr().out)["message"] == "stale semantic decision"


@pytest.mark.parametrize(
    ("timeout", "report_bytes", "message"),
    [
        (0, 1024, "timeout must be positive"),
        (1, 0, "report byte limit is invalid"),
    ],
)
def test_semantic_materialization_rejects_invalid_validation_bounds(
    tmp_path: Path, timeout: int, report_bytes: int, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        materialize_semantic_candidate(
            SemanticMaterializationOptions(
                candidate=tmp_path / "candidate",
                semantic_record=tmp_path / "record.json",
                review_decision=tmp_path / "decision.json",
                output=tmp_path / "output",
                specpm_timeout_seconds=timeout,
                max_specpm_report_bytes=report_bytes,
            )
        )


def test_detail_surface_rejects_semantic_member_drift(tmp_path: Path) -> None:
    source = tmp_path / "semantic" / "demo.package"
    write_triplet(source, semantic_triplet(tmp_path))
    packet_dir = tmp_path / "packet"
    packet_dir.mkdir()
    pointer = copy_semantic_proposal("demo.package", packet_dir, tmp_path / "semantic")
    packet = {
        "candidate": {"fileCount": 0, "manifestCount": 0, "status": "portable", "files": []},
        "repository": {"id": "demo.package"},
        "triage": {"status": "completed"},
        "aiProposal": {"status": "summary_only_not_portable", "summary": {}},
        "semanticProposal": pointer,
    }
    members = {"packets/demo.package/semantic-proposal-record.json": b"{}"}

    with pytest.raises(ValueError, match="member digest differs"):
        _comparison("demo.package", "a" * 64, packet, members)


def test_embedded_validator_rejects_authority_boundary_drift(tmp_path: Path) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    record["executionBoundary"]["materializationPerformed"] = True
    record["recordSha256"] = digest(
        {key: value for key, value in record.items() if key != "recordSha256"}
    )

    with pytest.raises(ValueError, match="execution boundary"):
        validate_portable_semantic_proposal(record)


def test_portable_record_validators_fail_closed_for_identity_digest_and_privacy(
    tmp_path: Path,
) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    invalid = copy.deepcopy(record)
    invalid["kind"] = "Other"
    with pytest.raises(ValueError, match="identity"):
        validate_portable_semantic_proposal(invalid)

    invalid = copy.deepcopy(record)
    invalid["recordSha256"] = "0" * 64
    with pytest.raises(ValueError, match="record digest"):
        validate_portable_semantic_proposal(invalid)

    invalid = copy.deepcopy(record)
    invalid["privacy"]["credentialsPersisted"] = True
    invalid["recordSha256"] = digest(
        {key: value for key, value in invalid.items() if key != "recordSha256"}
    )
    with pytest.raises(ValueError, match="privacy boundary"):
        validate_portable_semantic_proposal(invalid)

    with pytest.raises(ValueError, match="source is unavailable"):
        build_portable_semantic_proposal_from_directory(tmp_path / "missing")


@pytest.mark.parametrize("target", ("record", "proposal", "quality"))
def test_embedded_validator_rejects_unknown_persisted_fields(tmp_path: Path, target: str) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    if target == "record":
        record["rawPrompt"] = "secret"
    elif target == "proposal":
        record["proposal"]["rawResponse"] = "secret"
        record["proposal"]["proposalSha256"] = digest(
            {key: value for key, value in record["proposal"].items() if key != "proposalSha256"}
        )
        record["proposalSha256"] = record["proposal"]["proposalSha256"]
        record["qualityReport"]["proposalSha256"] = record["proposalSha256"]
        record["qualityReportSha256"] = digest(record["qualityReport"])
    else:
        record["qualityReport"]["chainOfThought"] = "secret"
        record["qualityReportSha256"] = digest(record["qualityReport"])
    record["recordSha256"] = digest(
        {key: value for key, value in record.items() if key != "recordSha256"}
    )

    with pytest.raises(ValueError, match="identity|shape"):
        validate_portable_semantic_proposal(record)


def test_receipt_validator_rejects_raw_data_and_machine_local_paths(tmp_path: Path) -> None:
    record = build_portable_semantic_proposal(*semantic_triplet(tmp_path))
    receipt = copy.deepcopy(record["providerReceipt"])
    receipt["rawResponsePersisted"] = True
    with pytest.raises(ValueError, match="privacy boundary"):
        _validate_receipt(receipt)

    receipt = copy.deepcopy(record["providerReceipt"])
    receipt["modelId"] = "/Users/operator/private-model"
    with pytest.raises(ValueError, match="provider-local path"):
        _validate_receipt(receipt)


def test_docs_define_portable_record_privacy_and_authority() -> None:
    root = Path(__file__).resolve().parents[1]
    documents = (
        root / "docs/PORTABLE_SEMANTIC_PROPOSAL_RECORDS.md",
        root / "Sources/SpecHarvester/Documentation.docc/PortableSemanticProposalRecords.md",
    )
    for path in documents:
        text = " ".join(path.read_text(encoding="utf-8").lower().split())
        for required in (
            "p55-t6",
            "semantic-proposal-record.json",
            "raw prompts",
            "hidden reasoning",
            "specpm",
            "publication",
        ):
            assert required in text
