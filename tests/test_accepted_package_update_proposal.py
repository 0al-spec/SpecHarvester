from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.accepted_update_proposal import (
    AcceptedPackageUpdateProposalOptions,
    build_accepted_package_update_proposal,
)
from spec_harvester.cli import main


def test_build_accepted_package_update_proposal_builds_upstream_revision_payload(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.workflow"],
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    write_harvest_json(candidate)
    write_producer_bundle_evidence(candidate)

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
        )
    )

    assert result["kind"] == "SpecHarvesterAcceptedPackageUpdateProposal"
    assert result["status"] == "ok"
    assert result["packageId"] == "demo.core"
    assert result["oldPackageVersion"] == "1.0.0"
    assert result["newPackageVersion"] == "1.1.0"
    assert result["updateKind"] == "upstream_revision"
    assert result["sourceRevision"] == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    assert result["validationStatus"] == {"specpm": "skipped"}
    assert result["evidenceDigests"]["harvestJson"].startswith("sha256:")
    assert result["evidenceDigests"]["specpmYaml"].startswith("sha256:")
    producer_links = {entry["role"]: entry for entry in result["producerEvidenceLinks"]}
    assert producer_links["accepted_source_bundle"]["path"] == (
        "public-index/generated/demo.core/1.1.0"
    )
    assert producer_links["accepted_source_bundle"]["pathScope"] == "repo_relative"
    assert producer_links["accepted_source_bundle"]["status"] == "expected"
    assert producer_links["boundary_spec"]["path"] == (
        "public-index/generated/demo.core/1.1.0/specs/demo.spec.yaml"
    )
    assert producer_links["boundary_spec"]["pathScope"] == "repo_relative"
    assert producer_links["boundary_spec"]["status"] == "present"
    assert producer_links["boundary_spec"]["digest"].startswith("sha256:")
    assert producer_links["producer_receipt"]["path"] == (
        "public-index/generated/demo.core/1.1.0/producer-receipt.json"
    )
    assert producer_links["producer_receipt"]["pathScope"] == "repo_relative"
    assert producer_links["producer_receipt"]["status"] == "present"
    assert producer_links["producer_receipt"]["digest"].startswith("sha256:")
    assert producer_links["validation_report"]["path"] == (
        "public-index/generated/demo.core/1.1.0/validation-report.json"
    )
    assert producer_links["diagnostics"]["path"] == (
        "public-index/generated/demo.core/1.1.0/diagnostics.json"
    )
    assert producer_links["producer_preflight"]["path"] == "preflight-report.json"
    assert producer_links["producer_preflight"]["status"] == "present"
    assert producer_links["static_viewer"]["path"] == "static-viewer/index.html"
    assert producer_links["static_viewer"]["status"] == "present"
    assert producer_links["accepted_source_diff"]["path"] == "pull-request-diff"
    assert producer_links["accepted_source_diff"]["pathScope"] == "pull_request"
    assert producer_links["accepted_source_diff"]["status"] == "expected"
    decision = result["registryAcceptanceDecision"]
    assert decision["status"] == "external_required"
    assert decision["requiredFor"] == ["public_index_acceptance"]
    assert decision["recordKind"] == "SpecPMRegistryAcceptanceDecision"
    assert decision["producerReceiptAuthority"] == "evidence_only"
    assert result["changedClaims"] == [
        "capability:demo.stream",
        "intent:intent.package.utility",
        "intent:intent.package.workflow",
    ]


def test_build_accepted_package_update_proposal_infers_metadata_errata(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="cccccccccccccccccccccccccccccccccccccccc",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.1",
        capabilities=["demo.read"],
        intents=["intent.package.utility", "intent.package.workflow"],
        upstream_revision="cccccccccccccccccccccccccccccccccccccccc",
        extra_metadata={"licenseEvidence": "evidence.txt"},
    )

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
            reviewer_notes=("metadata-only review reason",),
        )
    )

    assert result["updateKind"] == "metadata_errata"
    assert result["status"] == "ok"
    assert result["reviewerNotes"] == ["metadata-only review reason"]
    assert "intent:intent.package.workflow" in result["changedClaims"]


def test_build_accepted_package_update_proposal_rejects_escaping_boundary_spec_path(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"
    outside = tmp_path / "candidates" / "outside.spec.yaml"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.1",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )
    outside.write_text("apiVersion: specpm.dev/v0.1\n", encoding="utf-8")
    manifest_text = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    (candidate / "specpm.yaml").write_text(
        manifest_text.replace("  - path: specs/demo.spec.yaml", "  - path: ../outside.spec.yaml"),
        encoding="utf-8",
    )
    write_producer_bundle_evidence(candidate)

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
        )
    )

    producer_links = {entry["role"]: entry for entry in result["producerEvidenceLinks"]}
    boundary_spec = producer_links["boundary_spec"]
    assert boundary_spec["path"] == "public-index/generated/demo.core/1.0.1/specs"
    assert boundary_spec["pathScope"] == "repo_relative"
    assert boundary_spec["status"] == "missing"
    assert "digest" not in boundary_spec


def test_build_accepted_package_update_proposal_requires_correction_for_same_version(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )

    with pytest.raises(
        ValueError,
        match="correction mode",
    ):
        build_accepted_package_update_proposal(
            AcceptedPackageUpdateProposalOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                skip_validation=True,
            )
        )


def test_build_accepted_package_update_proposal_rejects_same_version_evidence_mutation(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_harvest_json(accepted_root / "demo" / "1.0.0", content='{"snapshot":"old"}')
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_harvest_json(candidate, content='{"snapshot":"new"}')

    with pytest.raises(
        ValueError,
        match="Accepted package version is immutable",
    ):
        build_accepted_package_update_proposal(
            AcceptedPackageUpdateProposalOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                skip_validation=True,
            )
        )


def test_build_accepted_package_update_proposal_allows_identical_same_version_evidence(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_harvest_json(accepted_root / "demo" / "1.0.0", content='{"snapshot":"same"}')
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_harvest_json(candidate, content='{"snapshot":"same"}')

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
        )
    )

    assert result["updateKind"] == "metadata_errata"
    assert result["comparison"]["status"] == "unchanged"
    assert "correction" not in result


def test_build_proposal_rejects_same_version_upstream_mutation(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )

    with pytest.raises(
        ValueError,
        match="Accepted package version is immutable",
    ):
        build_accepted_package_update_proposal(
            AcceptedPackageUpdateProposalOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                skip_validation=True,
            )
        )


def test_build_accepted_package_update_proposal_accepts_correction_with_upstream_change(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
            allow_correction=True,
            correction_notes=("upstream hash corrected",),
        )
    )

    assert result["updateKind"] == "correction"
    assert result["oldPackageVersion"] == "1.0.0"
    assert result["newPackageVersion"] == "1.0.0"
    assert result["comparison"]["status"] == "correction"
    assert result["correction"] == {
        "enabled": True,
        "reason": ["upstream hash corrected"],
        "source": "manual_review",
    }
    assert "upstream hash corrected" in result["reviewerNotes"]


def test_build_accepted_package_update_proposal_rejects_mutating_previous_accepted_version(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        accepted_root / "demo" / "1.1.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )

    with pytest.raises(
        ValueError,
        match="Accepted package version is immutable",
    ):
        build_accepted_package_update_proposal(
            AcceptedPackageUpdateProposalOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                skip_validation=True,
            )
        )


def test_build_accepted_package_update_proposal_accepts_correction_with_notes(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        extra_metadata={"licenseEvidence": "evidence.txt"},
    )

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
            allow_correction=True,
            correction_notes=("metadata cleanup",),
        )
    )

    assert result["updateKind"] == "correction"
    assert result["oldPackageVersion"] == "1.0.0"
    assert result["newPackageVersion"] == "1.0.0"
    assert result["comparison"]["status"] == "correction"
    assert result["correction"] == {
        "enabled": True,
        "reason": ["metadata cleanup"],
        "source": "manual_review",
    }
    assert "metadata cleanup" in result["reviewerNotes"]


def test_build_accepted_package_update_proposal_rejects_invalid_correction_override(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )

    with pytest.raises(ValueError, match="Manual correction"):
        build_accepted_package_update_proposal(
            AcceptedPackageUpdateProposalOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                skip_validation=True,
                allow_correction=True,
                correction_notes=("metadata cleanup",),
                update_kind="metadata_errata",
            )
        )


def test_build_accepted_package_update_proposal_records_validation_failures(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import spec_harvester.accepted_update_proposal as module

    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.1",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )

    def fail_validation(*_args, **_kwargs) -> dict[str, str]:
        raise ValueError("specpm validation failed")

    monkeypatch.setattr(module, "validate_with_specpm", fail_validation)

    result = module.build_accepted_package_update_proposal(
        options=AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=False,
        )
    )

    assert result["status"] == "partial"
    assert result["validationStatus"]["specpm"] == "failed"
    assert result["validationStatus"]["error"] == "specpm validation failed"
    assert {issue["code"] for issue in result["issues"]} == {"specpm_validation_failed"}


def test_build_accepted_package_update_proposal_ignores_promoted_candidate_path(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = accepted_root / "demo" / "1.1.0"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        accepted_root / "demo" / "1.1.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )

    result = build_accepted_package_update_proposal(
        AcceptedPackageUpdateProposalOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            skip_validation=True,
        )
    )

    assert result["oldPackageVersion"] == "1.0.0"
    assert result["newPackageVersion"] == "1.1.0"
    assert result["updateKind"] == "upstream_revision"
    assert result["changedClaims"] == ["capability:demo.stream"]


def test_cli_accepted_package_update_proposal_writes_json_and_markdown(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidate = tmp_path / "candidates" / "demo"
    output = tmp_path / "proposal.json"
    body = tmp_path / "proposal.md"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=[],
    )
    write_manifest(
        candidate / "specpm.yaml",
        package_id="demo.core",
        version="1.0.1",
        capabilities=["demo.read"],
        intents=["intent.package.workflow"],
    )
    write_producer_bundle_evidence(candidate)

    exit_code = main(
        [
            "accepted-package-update-proposal",
            str(candidate),
            "--accepted-root",
            str(accepted_root),
            "--output",
            str(output),
            "--proposal-body",
            str(body),
            "--skip-validation",
        ]
    )

    assert exit_code == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    body_text = body.read_text(encoding="utf-8")
    producer_links = {entry["role"]: entry for entry in report["producerEvidenceLinks"]}
    assert report["kind"] == "SpecHarvesterAcceptedPackageUpdateProposal"
    assert producer_links["producer_receipt"]["path"] == (
        "public-index/generated/demo.core/1.0.1/producer-receipt.json"
    )
    assert "## Summary" in body_text
    assert "## Producer Bundle Evidence" in body_text
    assert (
        "accepted_source_bundle: `public-index/generated/demo.core/1.0.1` - expected, required"
    ) in body_text
    assert (
        "boundary_spec: `public-index/generated/demo.core/1.0.1/specs/demo.spec.yaml` "
        "- present, required"
    ) in body_text
    assert (
        "producer_receipt: `public-index/generated/demo.core/1.0.1/producer-receipt.json` "
        "- present, required"
    ) in body_text
    assert "producer_preflight: `preflight-report.json` - present, optional" in body_text
    assert "accepted_source_diff: `pull-request-diff` - expected, required" in body_text
    assert '"producerEvidenceLinks"' in body_text
    assert '"role": "boundary_spec"' in body_text
    assert "## Registry Acceptance Decision" in body_text
    assert "status: `external_required`" in body_text
    assert "record location: `SpecPM pull request or accepted-source review record`" in body_text
    assert "producer receipt authority: `evidence_only`" in body_text
    assert '"registryAcceptanceDecision"' in body_text
    assert report["registryAcceptanceDecision"]["status"] == "external_required"


def write_manifest(
    path: Path,
    *,
    package_id: str,
    version: str,
    capabilities: list[str],
    intents: list[str],
    name: str = "Demo",
    summary: str = "Demo package",
    license_name: str = "MIT",
    upstream_revision: str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    extra_metadata: dict[str, str] | None = None,
) -> None:
    metadata_lines = ""
    if extra_metadata:
        metadata_lines = "".join(f"  {key}: {value}\n" for key, value in extra_metadata.items())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            f"  id: {package_id}\n"
            f"  name: {name}\n"
            f"  version: {version}\n"
            f"  summary: {summary}\n"
            f"  license: {license_name}\n"
            f"{metadata_lines}"
            "specs:\n"
            "  - path: specs/demo.spec.yaml\n"
            "index:\n"
            "  provides:\n"
            "    capabilities:\n"
            + "".join(f"      - {capability}\n" for capability in capabilities)
            + "  intents:\n"
            + "".join(f"    - {intent}\n" for intent in intents)
            + "foreignArtifacts:\n"
            "  - id: upstream_repository\n"
            "    uri: https://github.com/example/demo\n"
            f"    revision: {upstream_revision}\n"
        ),
        encoding="utf-8",
    )
    boundary_spec = path.parent / "specs" / "demo.spec.yaml"
    boundary_spec.parent.mkdir(parents=True, exist_ok=True)
    boundary_spec.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: BoundarySpec\n"
            "metadata:\n"
            f"  id: {package_id}.boundary\n"
            f"  title: {name} Boundary\n"
            "scope:\n"
            "  includes: []\n"
            "  excludes: []\n"
        ),
        encoding="utf-8",
    )


def write_harvest_json(directory: Path, *, content: str = "{}") -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "harvest.json").write_text(content, encoding="utf-8")


def write_producer_bundle_evidence(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "producer-receipt.json").write_text(
        '{"kind":"SpecPMProducerReceipt"}\n',
        encoding="utf-8",
    )
    (directory / "validation-report.json").write_text(
        '{"status":"valid"}\n',
        encoding="utf-8",
    )
    (directory / "diagnostics.json").write_text(
        '{"status":"clean"}\n',
        encoding="utf-8",
    )
    (directory / "preflight-report.json").write_text(
        '{"status":"passed"}\n',
        encoding="utf-8",
    )
    static_viewer = directory / "static-viewer"
    static_viewer.mkdir(exist_ok=True)
    (static_viewer / "index.html").write_text("<!doctype html>\n", encoding="utf-8")
