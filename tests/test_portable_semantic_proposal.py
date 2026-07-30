from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.local_candidate_review_details import (
    _comparison,
    _detail_sections,
)
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
from spec_harvester.semantic_proposal_quality import evaluate_semantic_proposal_quality


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
    packet = {
        "candidate": {"fileCount": 0, "manifestCount": 0, "status": "portable", "files": []},
        "repository": {"id": "demo.package"},
        "triage": {"status": "completed"},
        "aiProposal": {"status": "summary_only_not_portable", "summary": {}},
        "semanticProposal": pointer,
    }
    members = {"packets/demo.package/semantic-proposal-record.json": payload}

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
