from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.package_set_handoff_proposal import (
    PACKAGE_SET_HANDOFF_PROPOSAL_API_VERSION,
    PACKAGE_SET_HANDOFF_PROPOSAL_KIND,
    PackageSetHandoffProposalOptions,
    build_package_set_handoff_proposal,
    build_package_set_handoff_proposal_markdown,
)
from spec_harvester.xyflow_package_set_smoke import (
    XyflowPackageSetSmokeOptions,
    run_xyflow_package_set_smoke,
)


def test_package_set_handoff_proposal_builds_xyflow_review_artifact(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)

    proposal = build_package_set_handoff_proposal(
        PackageSetHandoffProposalOptions(
            bundle_set=smoke / "package-set",
            viewer=smoke / "viewer",
        )
    )

    assert proposal["apiVersion"] == PACKAGE_SET_HANDOFF_PROPOSAL_API_VERSION
    assert proposal["kind"] == PACKAGE_SET_HANDOFF_PROPOSAL_KIND
    assert proposal["status"] == "ok"
    assert proposal["packageSet"]["id"] == "xyflow.workspace"
    assert proposal["packageSet"]["candidateCount"] == 4
    assert proposal["packageSet"]["relationCount"] == 3
    assert proposal["preflight"]["status"] == "passed"
    assert proposal["viewer"]["status"] == "present"
    assert proposal["registryAcceptanceDecision"] == {
        "acceptanceAuthority": "SpecPM maintainer review",
        "producerAuthority": "evidence_only",
        "recordKind": "SpecPMRegistryAcceptanceDecision",
        "requiredFor": ["public_index_acceptance", "package_relation_acceptance"],
        "status": "external_required",
    }
    assert [member["packageId"] for member in proposal["members"]] == [
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
    ]
    assert relation_tuples(proposal) == {
        ("xyflow.workspace", "contains", "xyflow.react"),
        ("xyflow.workspace", "contains", "xyflow.svelte"),
        ("xyflow.workspace", "contains", "xyflow.system"),
    }
    link_roles = {link["role"] for link in proposal["evidenceLinks"]}
    assert {
        "package_set_draft",
        "package_relation_proposals",
        "bundle_set_preflight",
        "package_set_viewer",
        "member_candidate_bundle",
        "package_relation_summary",
    }.issubset(link_roles)
    trust_boundary = " ".join(proposal["trustBoundary"])
    assert "review evidence" in trust_boundary
    assert "SpecPM remains" in trust_boundary


def test_package_set_handoff_proposal_markdown_mentions_review_boundary(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    proposal = build_package_set_handoff_proposal(
        PackageSetHandoffProposalOptions(bundle_set=smoke / "package-set", viewer=smoke / "viewer")
    )

    body = build_package_set_handoff_proposal_markdown(proposal)

    assert "# SpecPM Package-Set Handoff Proposal: xyflow.workspace" in body
    assert "`xyflow.workspace` contains `xyflow.react`" in body
    assert "`package_set_viewer`" in body
    assert "Registry acceptance decision: `external_required`" in body
    assert "does not accept packages" in body
    assert "replace SpecPM maintainer review" in body


def test_package_set_handoff_proposal_cli_writes_json_and_markdown(
    tmp_path: Path,
    capsys,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    output = tmp_path / "handoff" / "proposal.json"
    body = tmp_path / "handoff" / "proposal.md"

    exit_code = main(
        [
            "package-set-handoff-proposal",
            "--bundle-set",
            str(smoke / "package-set"),
            "--viewer",
            str(smoke / "viewer"),
            "--output",
            str(output),
            "--proposal-body",
            str(body),
        ]
    )

    printed = json.loads(capsys.readouterr().out)
    written = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert printed == written
    assert written["kind"] == PACKAGE_SET_HANDOFF_PROPOSAL_KIND
    assert "xyflow.workspace" in body.read_text(encoding="utf-8")


def test_package_set_handoff_proposal_rejects_missing_relation_artifact(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    (smoke / "package-set" / "package-relation-proposals.json").unlink()

    with pytest.raises(ValueError, match="package-relation-proposals.json"):
        build_package_set_handoff_proposal(
            PackageSetHandoffProposalOptions(bundle_set=smoke / "package-set")
        )


def test_package_set_handoff_proposal_rejects_escaped_member_evidence_path(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    bundle_set = smoke / "package-set"
    outside = tmp_path / "outside-specpm.yaml"
    outside.write_text("secret-ish metadata", encoding="utf-8")
    draft_path = bundle_set / "package-set-draft.json"
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    draft["candidates"][0]["manifest"] = "../outside-specpm.yaml"
    draft_path.write_text(json.dumps(draft, indent=2, sort_keys=True), encoding="utf-8")

    proposal = build_package_set_handoff_proposal(
        PackageSetHandoffProposalOptions(bundle_set=bundle_set)
    )

    escaped_link = next(
        link
        for member in proposal["members"]
        for link in member["evidenceLinks"]
        if link["role"] == "member_manifest" and link["path"] == "../outside-specpm.yaml"
    )
    assert escaped_link["status"] == "rejected"
    assert "digest" not in escaped_link


def write_xyflow_smoke(tmp_path: Path) -> Path:
    smoke = tmp_path / "xyflow-smoke"
    report = run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=smoke))
    assert report["status"] == "passed"
    return smoke


def relation_tuples(report: dict[str, object]) -> set[tuple[str, str, str]]:
    relations = report["relations"]
    assert isinstance(relations, list)
    return {
        (
            str(item["source"]["packageId"]),
            str(item["type"]),
            str(item["target"]["packageId"]),
        )
        for item in relations
        if isinstance(item, dict)
        and isinstance(item.get("source"), dict)
        and isinstance(item.get("target"), dict)
    }
