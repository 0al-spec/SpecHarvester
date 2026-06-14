from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.selected_candidate_handoff_proposal import (
    SELECTED_CANDIDATE_HANDOFF_PROPOSAL_API_VERSION,
    SELECTED_CANDIDATE_HANDOFF_PROPOSAL_KIND,
    SelectedCandidateHandoffProposalOptions,
    build_selected_candidate_handoff_proposal,
    build_selected_candidate_handoff_proposal_markdown,
)

ROOT = Path(__file__).resolve().parents[1]
DRY_RUN_FIXTURE = (
    ROOT
    / "tests"
    / "fixtures"
    / "limited_popular_library_selected_handoff_dry_run"
    / "p30-t5-limited-popular-libraries.example.json"
)
P31_T3_FIXTURE = (
    ROOT
    / "tests"
    / "fixtures"
    / "selected_candidate_handoff_proposal"
    / "p31-t3-real-selected-candidate-handoff.example.json"
)


def test_selected_candidate_handoff_proposal_builds_review_artifact(
    tmp_path: Path,
) -> None:
    artifacts = write_selected_candidate_artifacts(tmp_path)

    proposal = build_selected_candidate_handoff_proposal(
        SelectedCandidateHandoffProposalOptions(
            selected_handoff_dry_run=artifacts["dry_run"],
            candidate_root=artifacts["candidate_root"],
            preflight_root=artifacts["preflight_root"],
            viewer_root=artifacts["viewer_root"],
        )
    )

    assert proposal["apiVersion"] == SELECTED_CANDIDATE_HANDOFF_PROPOSAL_API_VERSION
    assert proposal["kind"] == SELECTED_CANDIDATE_HANDOFF_PROPOSAL_KIND
    assert proposal["schemaVersion"] == 1
    assert proposal["authority"] == "producer_preview_evidence_only"
    assert proposal["summary"] == {
        "deferredCandidateCount": 6,
        "registryMutationCount": 0,
        "requiredEvidenceRoleCount": 11,
        "selectedCandidateCount": 3,
        "specpmPullRequestCreated": False,
    }
    assert proposal["source"]["selectedDryRunFixture"]["digest"].startswith("sha256:")
    assert [item["id"] for item in proposal["selectedCandidates"]] == [
        "flask.core",
        "gin.core",
        "docc2context.core",
    ]
    assert {item["id"] for item in proposal["deferredCandidates"]} == {
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "cupertino.core",
        "navigation_split_view.core",
    }
    assert {item["role"] for item in proposal["requiredEvidenceRoles"]} == {
        "candidate_bundle",
        "manifest",
        "boundary_spec",
        "producer_receipt",
        "validation_report",
        "diagnostics",
        "quality_report",
        "producer_preflight",
        "static_viewer",
        "static_viewer_payload",
        "selected_handoff_dry_run",
    }

    flask = proposal["selectedCandidates"][0]
    assert flask["id"] == "flask.core"
    assert flask["previewOnly"] is True
    assert flask["producerPreflight"]["status"] == "passed"
    assert flask["producerPreflight"]["warningCount"] == 0
    assert flask["producerPreflight"]["errorCount"] == 0
    assert flask["staticViewer"]["status"] == "ok"
    assert flask["registryAcceptanceDecision"] == {
        "producerAuthority": "evidence_only",
        "requiredFor": "public_index_acceptance",
        "status": "external_required",
    }

    evidence = {item["role"]: item for item in flask["evidenceLinks"]}
    assert set(evidence) == {item["role"] for item in proposal["requiredEvidenceRoles"]}
    assert evidence["candidate_bundle"]["status"] == "present"
    assert evidence["manifest"]["digestSource"] == "local_file"
    assert evidence["manifest"]["digest"] == file_digest(
        artifacts["candidate_root"] / "flask.core" / "candidate" / "specpm.yaml"
    )
    assert evidence["producer_preflight"]["digestSource"] == "local_file"
    assert evidence["static_viewer"]["digestSource"] == "local_file"
    assert evidence["static_viewer_payload"]["digestSource"] == "local_file"
    assert evidence["selected_handoff_dry_run"]["digestSource"] == "local_file"

    non_authority = " ".join(proposal["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not create a SpecPM pull request" in non_authority


def test_selected_candidate_handoff_proposal_markdown_mentions_boundary(
    tmp_path: Path,
) -> None:
    artifacts = write_selected_candidate_artifacts(tmp_path)
    proposal = build_selected_candidate_handoff_proposal(
        SelectedCandidateHandoffProposalOptions(
            selected_handoff_dry_run=artifacts["dry_run"],
            candidate_root=artifacts["candidate_root"],
            preflight_root=artifacts["preflight_root"],
            viewer_root=artifacts["viewer_root"],
        )
    )

    body = build_selected_candidate_handoff_proposal_markdown(proposal)

    assert "# SpecPM Selected Candidate Handoff Proposal" in body
    assert "| `flask.core` | `flask` | `passed` | `ok` | `external_required` |" in body
    assert "`xyflow.workspace`" in body
    assert "`candidate_bundle`" in body
    assert "Verify every required evidence role" in body
    assert "does not accept packages" in body
    assert "create a SpecPM pull request" in body


def test_selected_candidate_handoff_proposal_cli_writes_json_and_markdown(
    tmp_path: Path,
    capsys,
) -> None:
    artifacts = write_selected_candidate_artifacts(tmp_path)
    output = tmp_path / "handoff" / "selected-candidate-handoff-proposal.json"
    body = tmp_path / "handoff" / "selected-candidate-handoff-proposal.md"

    exit_code = main(
        [
            "selected-candidate-handoff-proposal",
            "--selected-handoff-dry-run",
            str(artifacts["dry_run"]),
            "--candidate-root",
            str(artifacts["candidate_root"]),
            "--preflight-root",
            str(artifacts["preflight_root"]),
            "--viewer-root",
            str(artifacts["viewer_root"]),
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
    assert written["kind"] == SELECTED_CANDIDATE_HANDOFF_PROPOSAL_KIND
    assert "docc2context.core" in body.read_text(encoding="utf-8")


def test_selected_candidate_handoff_proposal_keeps_relative_dry_run_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(ROOT)

    proposal = build_selected_candidate_handoff_proposal(
        SelectedCandidateHandoffProposalOptions(
            selected_handoff_dry_run=Path(
                "tests/fixtures/limited_popular_library_selected_handoff_dry_run/"
                "p30-t5-limited-popular-libraries.example.json"
            )
        )
    )

    expected_path = (
        "tests/fixtures/limited_popular_library_selected_handoff_dry_run/"
        "p30-t5-limited-popular-libraries.example.json"
    )
    assert proposal["source"]["selectedDryRunFixture"]["path"] == expected_path
    for candidate in proposal["selectedCandidates"]:
        evidence = {item["role"]: item for item in candidate["evidenceLinks"]}
        assert evidence["selected_handoff_dry_run"]["path"] == expected_path
        assert evidence["selected_handoff_dry_run"]["digest"] == file_digest(DRY_RUN_FIXTURE)


def test_p31_t3_real_selected_candidate_handoff_fixture_records_helper_run() -> None:
    payload = json.loads(P31_T3_FIXTURE.read_text(encoding="utf-8"))

    assert payload["apiVersion"] == SELECTED_CANDIDATE_HANDOFF_PROPOSAL_API_VERSION
    assert payload["kind"] == SELECTED_CANDIDATE_HANDOFF_PROPOSAL_KIND
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_preview_evidence_only"
    assert payload["summary"] == {
        "deferredCandidateCount": 6,
        "registryMutationCount": 0,
        "requiredEvidenceRoleCount": 11,
        "selectedCandidateCount": 3,
        "specpmPullRequestCreated": False,
    }
    assert payload["source"]["selectedDryRunFixture"] == {
        "apiVersion": "spec-harvester.limited-popular-library-selected-handoff-dry-run/v0",
        "digest": file_digest(DRY_RUN_FIXTURE),
        "kind": "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun",
        "path": (
            "tests/fixtures/limited_popular_library_selected_handoff_dry_run/"
            "p30-t5-limited-popular-libraries.example.json"
        ),
        "status": "selected_handoff_dry_run_ready",
    }

    selected = {item["id"]: item for item in payload["selectedCandidates"]}
    assert list(selected) == ["flask.core", "gin.core", "docc2context.core"]
    assert {item["id"] for item in payload["deferredCandidates"]} == {
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "cupertino.core",
        "navigation_split_view.core",
    }
    required_roles = {item["role"] for item in payload["requiredEvidenceRoles"]}
    for candidate_id, candidate in selected.items():
        assert candidate["candidateBundlePath"].startswith("/tmp/specharvester-p30-t3.")
        assert candidate["previewOnly"] is True
        assert candidate["producerPreflight"]["status"] == "passed"
        assert candidate["producerPreflight"]["warningCount"] == 0
        assert candidate["producerPreflight"]["errorCount"] == 0
        assert candidate["staticViewer"]["status"] == "ok"
        assert candidate["registryAcceptanceDecision"] == {
            "producerAuthority": "evidence_only",
            "requiredFor": "public_index_acceptance",
            "status": "external_required",
        }
        evidence = {item["role"]: item for item in candidate["evidenceLinks"]}
        assert set(evidence) == required_roles
        assert evidence["manifest"]["path"].startswith("/tmp/specharvester-p30-t3.")
        assert evidence["manifest"]["digestSource"] == "local_file"
        assert evidence["producer_preflight"]["path"].endswith(f"/{candidate_id}.json")
        assert evidence["producer_preflight"]["digestSource"] == "local_file"
        assert evidence["static_viewer"]["path"].endswith(f"/{candidate_id}/index.html")
        assert evidence["static_viewer_payload"]["path"].endswith(
            f"/{candidate_id}/spec-package.json"
        )
        assert evidence["selected_handoff_dry_run"]["path"] == (
            "tests/fixtures/limited_popular_library_selected_handoff_dry_run/"
            "p30-t5-limited-popular-libraries.example.json"
        )
        assert evidence["selected_handoff_dry_run"]["digest"] == file_digest(DRY_RUN_FIXTURE)

    non_authority = " ".join(payload["nonAuthority"])
    assert "review evidence only" in non_authority
    assert "not SpecPM registry acceptance" in non_authority
    assert "does not accept packages" in non_authority
    assert "does not create a SpecPM pull request" in non_authority


def test_selected_candidate_handoff_proposal_rejects_invalid_dry_run_identity(
    tmp_path: Path,
) -> None:
    artifacts = write_selected_candidate_artifacts(tmp_path)
    payload = json.loads(artifacts["dry_run"].read_text(encoding="utf-8"))
    payload["kind"] = "WrongKind"
    artifacts["dry_run"].write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="kind"):
        build_selected_candidate_handoff_proposal(
            SelectedCandidateHandoffProposalOptions(
                selected_handoff_dry_run=artifacts["dry_run"],
                candidate_root=artifacts["candidate_root"],
            )
        )


def test_selected_candidate_handoff_proposal_rejects_failed_preflight(
    tmp_path: Path,
) -> None:
    artifacts = write_selected_candidate_artifacts(tmp_path)
    payload = json.loads(artifacts["dry_run"].read_text(encoding="utf-8"))
    payload["selectedCandidates"][0]["producerPreflight"]["status"] = "failed"
    artifacts["dry_run"].write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="producer preflight must be passed"):
        build_selected_candidate_handoff_proposal(
            SelectedCandidateHandoffProposalOptions(
                selected_handoff_dry_run=artifacts["dry_run"],
                candidate_root=artifacts["candidate_root"],
            )
        )


def test_selected_candidate_handoff_proposal_rejects_warning_preflight_report(
    tmp_path: Path,
) -> None:
    artifacts = write_selected_candidate_artifacts(tmp_path)
    preflight = artifacts["preflight_root"] / "flask.core.json"
    payload = json.loads(preflight.read_text(encoding="utf-8"))
    payload["summary"]["warningCount"] = 1
    preflight.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with pytest.raises(ValueError, match="warningCount must be 0"):
        build_selected_candidate_handoff_proposal(
            SelectedCandidateHandoffProposalOptions(
                selected_handoff_dry_run=artifacts["dry_run"],
                candidate_root=artifacts["candidate_root"],
                preflight_root=artifacts["preflight_root"],
            )
        )


def write_selected_candidate_artifacts(tmp_path: Path) -> dict[str, Path]:
    dry_run = tmp_path / "p30-t5-selected-handoff.json"
    dry_run.write_text(DRY_RUN_FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    payload = json.loads(dry_run.read_text(encoding="utf-8"))
    candidate_root = tmp_path / "selected"
    preflight_root = tmp_path / "preflight"
    viewer_root = tmp_path / "viewer"

    for candidate in payload["selectedCandidates"]:
        candidate_id = candidate["id"]
        candidate_dir = candidate_root / candidate_id / "candidate"
        for item in candidate["requiredFiles"]:
            path = candidate_dir / item["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"{candidate_id}:{item['role']}:{item['path']}\n",
                encoding="utf-8",
            )
        preflight_root.mkdir(parents=True, exist_ok=True)
        (preflight_root / f"{candidate_id}.json").write_text(
            json.dumps(
                {
                    "authority": "producer_side_preflight",
                    "candidate": str(candidate_dir),
                    "diagnostics": [],
                    "kind": "SpecHarvesterCandidateBundlePreflightReport",
                    "schemaVersion": 1,
                    "status": "passed",
                    "summary": {
                        "diagnosticCount": 0,
                        "errorCount": 0,
                        "warningCount": 0,
                    },
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        viewer_dir = viewer_root / candidate_id
        viewer_dir.mkdir(parents=True, exist_ok=True)
        (viewer_dir / "index.html").write_text(
            f"<h1>{candidate_id}</h1>\n",
            encoding="utf-8",
        )
        (viewer_dir / "spec-package.json").write_text(
            json.dumps({"packageId": candidate_id}, sort_keys=True),
            encoding="utf-8",
        )

    return {
        "candidate_root": candidate_root,
        "dry_run": dry_run,
        "preflight_root": preflight_root,
        "viewer_root": viewer_root,
    }


def file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"
