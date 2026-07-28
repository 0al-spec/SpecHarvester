from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from spec_harvester.p53_portable_author_handoff import (
    P53PortableAuthorHandoffOptions,
    build_p53_portable_author_handoff,
)


def write_json(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def handoff_inputs(tmp_path: Path) -> P53PortableAuthorHandoffOptions:
    repositories = [
        {
            "id": f"repo-{position:03d}",
            "position": position,
            "wave": f"wave-{((position - 1) // 25) + 1}",
            "ecosystem": "python",
            "repositoryShape": "single_package",
            "provenance": {"repository": f"https://example.invalid/repo-{position:03d}"},
            "licenseProvenance": {"declaredSpdxId": "MIT"},
        }
        for position in range(1, 101)
    ]
    records = []
    for source in repositories:
        records.append(
            {
                "id": source["id"],
                "wave": source["wave"],
                "disposition": "selected_for_author_review",
                "status": "completed",
                "schemaValid": True,
                "repositorySpecific": True,
                "unsupportedClaimCount": 0,
                "proposal": {
                    "path": f"codex-spark/{source['id']}/package-set-ai-draft-proposal.json",
                    "status": "completed",
                    "digest": {"algorithm": "sha256", "value": "a" * 64},
                    "summary": {"selectedMemberCount": 1, "relationCount": 0},
                },
            }
        )
    metadata = write_json(
        tmp_path / "inputs" / "metadata.json",
        {
            "apiVersion": "spec-harvester.mass-corpus-selection-metadata/v0",
            "kind": "SpecHarvesterMassCorpusSelectionMetadata",
            "repositories": repositories,
        },
    )
    metadata_digest = sha256(metadata.read_bytes()).hexdigest()
    triage = write_json(
        tmp_path / "evidence" / "triage.json",
        {
            "apiVersion": "spec-harvester.p53-campaign-quality-triage/v0",
            "kind": "SpecHarvesterP53CampaignQualityTriage",
            "phase": "P53",
            "task": "P53-T13",
            "status": "passed",
            "authority": "producer_triage_evidence_only",
            "sourceArtifacts": {"metadata": {"sha256": metadata_digest}},
            "repositories": records,
            "privacy": {
                "rawPromptsPersisted": False,
                "rawProviderResponsesPersisted": False,
                "chainOfThoughtPersisted": False,
                "secretsPersisted": False,
            },
        },
    )
    candidate_root = tmp_path / "generated"
    for source in repositories:
        package = candidate_root / source["id"] / f"{source['id']}.core"
        package.mkdir(parents=True)
        (package / "specpm.yaml").write_text(
            "apiVersion: specpm.dev/v1alpha1\n"
            f"id: {source['id']}.core\n"
            "version: 0.1.0\n"
            "preview_only: true\n",
            encoding="utf-8",
        )
        write_json(package / "validation-report.json", {"status": "passed"})
        write_json(
            package / "bundle-set-preflight.json",
            {"candidateRoot": str(candidate_root / source["id"])},
        )
    return P53PortableAuthorHandoffOptions(
        triage=triage,
        metadata=metadata,
        packet_root=tmp_path / "handoff" / "packets",
        aggregate_output=tmp_path / "handoff" / "aggregate.json",
        report_output=tmp_path / "handoff" / "report.json",
        repo_root=tmp_path,
        candidate_root=candidate_root,
    )


def test_builds_one_portable_packet_per_selected_repository(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)

    result = build_p53_portable_author_handoff(options)

    assert result["status"] == "passed"
    assert result["summary"] == {
        "repositoryCount": 100,
        "packetCount": 100,
        "portableCandidateCount": 100,
        "portableAIProposalCount": 0,
        "summaryOnlyAIProposalCount": 100,
        "deferredCount": 0,
    }
    aggregate = json.loads(options.aggregate_output.read_text(encoding="utf-8"))
    assert aggregate["summary"]["selectedCandidateCount"] == 100
    assert aggregate["summary"]["deferredCandidateCount"] == 0
    assert len(aggregate["selectedCandidates"]) == 100
    packet_path = options.packet_root / "repo-001" / "packet.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["candidate"]["status"] == "portable"
    assert packet["candidate"]["previewOnly"] is True
    assert packet["aiProposal"]["status"] == "summary_only_not_portable"
    packet_text = "".join(
        path.read_text(encoding="utf-8")
        for path in (options.packet_root / "repo-001").rglob("*")
        if path.is_file()
    )
    assert str(tmp_path) not in packet_text
    normalized = json.loads(
        (
            options.packet_root
            / "repo-001"
            / "candidate"
            / "repo-001.core"
            / "bundle-set-preflight.json"
        ).read_text(encoding="utf-8")
    )
    assert normalized["candidateRoot"] == "candidate"


def test_copies_only_digest_matching_ai_proposal(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    proposal = {"repository": "repo-001", "members": []}
    proposal_path = write_json(
        tmp_path / "proposals" / "repo-001" / "package-set-ai-draft-proposal.json",
        proposal,
    )
    triage = json.loads(options.triage.read_text(encoding="utf-8"))
    triage["repositories"][0]["proposal"]["digest"]["value"] = sha256(
        proposal_path.read_bytes()
    ).hexdigest()
    write_json(options.triage, triage)
    options = P53PortableAuthorHandoffOptions(
        **{**options.__dict__, "proposal_root": tmp_path / "proposals"}
    )

    result = build_p53_portable_author_handoff(options)

    assert result["summary"]["portableAIProposalCount"] == 1
    packet = json.loads(
        (options.packet_root / "repo-001" / "packet.json").read_text(encoding="utf-8")
    )
    assert packet["aiProposal"]["status"] == "portable"


def test_rejects_ai_proposal_digest_drift(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    write_json(
        tmp_path / "proposals" / "repo-001" / "package-set-ai-draft-proposal.json",
        {"unexpected": "bytes"},
    )
    options = P53PortableAuthorHandoffOptions(
        **{**options.__dict__, "proposal_root": tmp_path / "proposals"}
    )

    with pytest.raises(ValueError, match="AI proposal digest mismatch"):
        build_p53_portable_author_handoff(options)


def test_rejects_candidate_without_preview_only(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    manifest = options.candidate_root / "repo-001" / "repo-001.core" / "specpm.yaml"
    manifest.write_text(
        "apiVersion: specpm.dev/v1alpha1\nid: repo-001.core\nversion: 0.1.0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="candidate manifest is not preview_only"):
        build_p53_portable_author_handoff(options)


def test_rejects_non_selected_triage_record(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    triage = json.loads(options.triage.read_text(encoding="utf-8"))
    triage["repositories"][0]["disposition"] = "deferred"
    write_json(options.triage, triage)

    with pytest.raises(ValueError, match="non-selected"):
        build_p53_portable_author_handoff(options)


def test_rejects_metadata_digest_drift(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    metadata = json.loads(options.metadata.read_text(encoding="utf-8"))
    metadata["repositories"][0]["ecosystem"] = "changed"
    write_json(options.metadata, metadata)

    with pytest.raises(ValueError, match="metadata digest does not match"):
        build_p53_portable_author_handoff(options)


def test_rejects_external_absolute_path_in_candidate_json(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    write_json(
        options.candidate_root / "repo-001" / "repo-001.core" / "external-path.json",
        {"source": str(tmp_path / "outside-candidate")},
    )

    with pytest.raises(ValueError, match="non-portable path"):
        build_p53_portable_author_handoff(options)


def test_rejects_output_outside_portable_root(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    options = P53PortableAuthorHandoffOptions(
        **{**options.__dict__, "report_output": tmp_path.parent / "outside.json"}
    )

    with pytest.raises(ValueError, match="outside the portable root"):
        build_p53_portable_author_handoff(options)


def test_rejects_candidate_symlink(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    source = options.candidate_root / "repo-001" / "external.json"
    source.symlink_to(options.metadata)

    with pytest.raises(ValueError, match="contains a symlink"):
        build_p53_portable_author_handoff(options)


def test_defers_missing_portable_candidate(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    options = P53PortableAuthorHandoffOptions(**{**options.__dict__, "candidate_root": None})

    result = build_p53_portable_author_handoff(options)

    assert result["status"] == "review_required"
    assert result["summary"]["portableCandidateCount"] == 0
    assert result["summary"]["deferredCount"] == 100
    aggregate = json.loads(options.aggregate_output.read_text(encoding="utf-8"))
    assert aggregate["summary"]["selectedCandidateCount"] == 0
    assert aggregate["summary"]["deferredCandidateCount"] == 100


def test_rejects_nonempty_packet_root(tmp_path: Path) -> None:
    options = handoff_inputs(tmp_path)
    options.packet_root.mkdir(parents=True)
    (options.packet_root / "stale.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="packet root must be empty"):
        build_p53_portable_author_handoff(options)
