from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.autonomous_candidate_batch import (
    AUTONOMOUS_CANDIDATE_BATCH_API_VERSION,
    AUTONOMOUS_CANDIDATE_BATCH_KIND,
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    REPOSITORY_PROFILE_DETECTION_FILENAME,
    AutonomousCandidateBatch,
    AutonomousCandidateBatchOptions,
    ai_proposal_record,
    run_autonomous_candidate_batch,
)
from spec_harvester.cli import main


def test_autonomous_candidate_batch_runs_offline_preview_pipeline(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
        )
    )

    assert report["apiVersion"] == AUTONOMOUS_CANDIDATE_BATCH_API_VERSION
    assert report["kind"] == AUTONOMOUS_CANDIDATE_BATCH_KIND
    assert report["status"] == "passed"
    assert report["ai"]["mode"] == "disabled"
    assert report["repositoryProfileSelection"]["mode"] == "none"
    assert report["repositoryProfileSelection"]["authority"] == "producer_profile_selection_only"
    assert report["repositoryProfileSelection"]["advisoryHintsAppliedToDrafting"] is False
    assert report["summary"]["processedCount"] == 1
    assert report["summary"]["passedPreflightCount"] == 1
    assert report["summary"]["repositoryProfileDetectionCount"] == 1
    assert report["summary"]["repositoryProfileDisabledCount"] == 1
    assert report["summary"]["repositoryProfileSelectedCount"] == 0
    repository = report["repositories"][0]
    assert repository["status"] == "passed"
    assert repository["repositoryProfileDetection"]["status"] == "completed"
    assert repository["repositoryProfileDetection"]["decision"] == "disabled"
    assert repository["repositoryProfileDetection"]["selectedProfileId"] is None
    assert repository["repositoryProfileDetection"]["path"].endswith(
        REPOSITORY_PROFILE_DETECTION_FILENAME
    )
    assert repository["packageSetDraft"]["candidateCount"] == 3
    assert repository["packageSetDraft"]["relationCount"] == 2
    assert repository["preflight"]["status"] == "passed"
    assert repository["aiDraft"]["status"] == "skipped"
    assert repository["aiEnrichment"]["status"] == "skipped"
    assert repository["aiEnrichedPreview"]["status"] == "skipped"
    assert repository["authorReadyDraftSummary"]["decision"] == "stop_for_author_review"
    assert report["summary"]["aiEnrichedPreviewAppliedCount"] == 0
    assert report["summary"]["aiEnrichedPreviewSkippedCount"] == 0
    assert report["summary"]["aiEnrichedPreviewFailedCount"] == 0

    saved = json.loads(
        (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).read_text(encoding="utf-8")
    )
    assert saved["status"] == "passed"
    assert (output / "collected" / "demo" / "workspace-inventory.json").is_file()
    assert (output / "package-sets" / "demo" / "package-set-draft.json").is_file()
    assert (output / "package-sets" / "demo" / "bundle-set-preflight.json").is_file()
    detection = json.loads(
        Path(repository["repositoryProfileDetection"]["path"]).read_text(encoding="utf-8")
    )
    assert detection["selection"]["decision"] == "disabled"
    assert detection["selection"]["mode"] == "none"
    assert detection["authority"] == "producer_profile_selection_only"


def test_autonomous_candidate_batch_records_auto_repository_profile_selection(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="auto",
        )
    )

    repository = report["repositories"][0]
    detection = repository["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert report["repositoryProfileSelection"]["mode"] == "auto"
    assert report["summary"]["repositoryProfileDetectionCount"] == 1
    assert report["summary"]["repositoryProfileSelectedCount"] == 1
    assert report["summary"]["repositoryProfileDisabledCount"] == 0
    assert detection["decision"] == "selected"
    assert detection["selectedProfileId"] == "generic.package_set.v0"
    assert detection["confidence"] == "high"
    assert detection["advisoryHintCount"] >= 3
    assert repository["packageSetDraft"]["candidateCount"] == 3
    assert repository["packageSetDraft"]["relationCount"] == 2

    payload = json.loads(Path(detection["path"]).read_text(encoding="utf-8"))
    assert payload["kind"] == "SpecHarvesterRepositoryProfileDetection"
    assert payload["selection"]["selectedProfileId"] == "generic.package_set.v0"
    assert "does_not_treat_plugin_decisions_as_registry_truth" in payload["nonAuthorityStatements"]
    assert {"hint": "package_set_root", "path": "."} in [
        {"hint": item["hint"], "path": item["path"]} for item in payload["advisoryDownstreamHints"]
    ]


def test_autonomous_candidate_batch_uses_harvested_manifest_evidence_when_inventory_empty(
    tmp_path: Path,
) -> None:
    inputs = write_single_package_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="auto",
        )
    )

    repository = report["repositories"][0]
    detection = repository["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert report["summary"]["repositoryProfileSelectedCount"] == 1
    assert detection["decision"] == "selected"
    assert detection["selectedProfileId"] == "generic.single_package.v0"
    assert detection["confidence"] == "high"
    assert detection["reasonCodes"] == ["root_manifest_present"]

    inventory = json.loads(
        (output / "collected" / "gin" / "workspace-inventory.json").read_text(encoding="utf-8")
    )
    assert inventory["summary"]["packageManifestCount"] == 0

    harvest = json.loads(
        (output / "collected" / "gin" / "harvest.json").read_text(encoding="utf-8")
    )
    assert harvest["summary"]["packageManifestCount"] == 1
    assert [
        item["path"] for item in harvest["files"] if item.get("kind") == "package_manifest"
    ] == ["go.mod"]

    payload = json.loads(Path(detection["path"]).read_text(encoding="utf-8"))
    candidates = {candidate["profileId"]: candidate for candidate in payload["candidateProfiles"]}
    assert candidates["generic.single_package.v0"]["evidencePaths"] == ["go.mod"]
    assert payload["diagnostics"][0]["evidencePaths"] == ["go.mod"]
    assert "does_not_treat_plugin_decisions_as_registry_truth" in payload["nonAuthorityStatements"]


def test_autonomous_candidate_batch_normalizes_repository_profile_selection(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection=" auto ",
        )
    )

    detection = report["repositories"][0]["repositoryProfileDetection"]

    assert report["repositoryProfileSelection"]["mode"] == "auto"
    assert detection["mode"] == "auto"


def test_autonomous_candidate_batch_records_explicit_repository_profile_override(
    tmp_path: Path,
) -> None:
    inputs = write_single_package_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="custom.repository_profile.v0",
        )
    )

    detection = report["repositories"][0]["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert detection["decision"] == "selected"
    assert detection["overrideSource"] == "cli"
    assert detection["selectedProfileId"] == "custom.repository_profile.v0"
    assert detection["reasonCodes"] == ["explicit_cli_profile_override"]
    assert report["repositories"][0]["packageSetDraft"]["candidateCount"] == 1


def test_autonomous_candidate_batch_uses_single_package_fallback(
    tmp_path: Path,
) -> None:
    inputs = write_single_package_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
        )
    )

    assert report["status"] == "passed"
    assert report["summary"]["processedCount"] == 1
    assert report["summary"]["passedPreflightCount"] == 1
    repository = report["repositories"][0]
    assert repository["id"] == "gin"
    assert repository["packageId"] == "gin.core"
    assert repository["status"] == "passed"
    assert repository["packageSetDraft"]["candidateCount"] == 1
    assert repository["packageSetDraft"]["relationCount"] == 0
    assert repository["preflight"]["status"] == "passed"
    assert repository["preflight"]["candidateCount"] == 1
    assert repository["preflight"]["relationCount"] == 0
    assert repository["aiDraft"]["status"] == "skipped"
    assert repository["aiEnrichment"]["status"] == "skipped"
    assert repository["aiEnrichedPreview"]["status"] == "skipped"
    assert repository["authorReadyDraftSummary"]["memberCounts"]["total"] == 1

    bundle_set = output / "package-sets" / "gin"
    summary = json.loads((bundle_set / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["candidates"][0]["packageId"] == "gin.core"
    assert summary["candidates"][0]["selectionReason"] == (
        "single_package_source_manifest_fallback"
    )
    assert summary["relationProposals"]["relationCount"] == 0
    relation_payload = json.loads(
        (bundle_set / "package-relation-proposals.json").read_text(encoding="utf-8")
    )
    assert relation_payload["relations"] == []
    assert "id: gin.core" in (bundle_set / "gin.core" / "specpm.yaml").read_text(encoding="utf-8")
    assert "preview_only: true" in (bundle_set / "gin.core" / "specpm.yaml").read_text(
        encoding="utf-8"
    )
    assert (bundle_set / "gin.core" / "producer-receipt.json").is_file()
    assert (bundle_set / "gin.core" / "validation-report.json").is_file()
    assert (bundle_set / "gin.core" / "diagnostics.json").is_file()
    assert (bundle_set / "gin.core" / "author-ready-draft-quality-report.json").is_file()


def test_autonomous_candidate_batch_requires_model_without_skip_ai(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=tmp_path / "output",
            )
        )
    except ValueError as exc:
        assert "--lm-studio-model" in str(exc)
    else:
        raise AssertionError("expected missing LM Studio model to fail")


def test_autonomous_candidate_batch_rejects_lm_studio_credentials_before_report(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                lm_studio_base_url="http://token@127.0.0.1:1234",
                lm_studio_model="openai/gpt-oss-20b",
            )
        )
    except ValueError as exc:
        assert "must not include credentials" in str(exc)
    else:
        raise AssertionError("expected LM Studio URL with credentials to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_records_normalized_lm_studio_base_url(
    tmp_path: Path,
) -> None:
    batch = AutonomousCandidateBatch(
        AutonomousCandidateBatchOptions(
            inputs=tmp_path / "inputs.yml",
            out=tmp_path / "output",
            lm_studio_base_url="http://localhost:1234/v1",
            lm_studio_model="openai/gpt-oss-20b",
        )
    )

    assert batch.ai_mode_record()["baseUrl"] == "http://localhost:1234"
    assert batch.ai_mode_record()["jsonRepairMaxAttempts"] == 1


def test_autonomous_candidate_batch_ai_record_surfaces_json_repair_diagnostics(
    tmp_path: Path,
) -> None:
    proposal = {
        "status": "failed",
        "authority": "proposal_only_not_registry_acceptance",
        "summary": {},
        "diagnostics": [
            {"severity": "warning", "code": "ai_json_repair_needed"},
            {"severity": "error", "code": "ai_json_repair_exhausted"},
        ],
        "providerReceipt": {
            "jsonRepairNeeded": True,
            "jsonRepairAttemptCount": 1,
            "jsonRepairStatus": "exhausted",
        },
        "privacy": {"rawModelResponsesPersisted": False},
    }

    record = ai_proposal_record(
        tmp_path / "request.json",
        tmp_path / "proposal.json",
        proposal,
    )

    assert record["status"] == "failed"
    assert record["diagnosticCodes"] == [
        "ai_json_repair_exhausted",
        "ai_json_repair_needed",
    ]
    assert record["jsonRepair"] == {
        "attemptCount": 1,
        "needed": True,
        "status": "exhausted",
    }


def test_autonomous_candidate_batch_applies_clean_ai_enrichment_when_opted_in(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_draft_proposal",
        lambda _options: completed_ai_draft_proposal(),
    )
    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_enrichment_proposal",
        lambda _options: completed_ai_enrichment_proposal("demo.workspace"),
    )

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            lm_studio_model="openai/gpt-oss-20b",
            apply_ai_enrichment=True,
        )
    )

    assert report["status"] == "passed"
    assert report["summary"]["aiEnrichedPreviewAppliedCount"] == 1
    assert report["summary"]["aiEnrichedPreviewSkippedCount"] == 2
    assert report["summary"]["aiEnrichedPreviewFailedCount"] == 0
    enriched = report["repositories"][0]["aiEnrichedPreview"]
    assert enriched["status"] == "prepared"
    assert enriched["summary"] == {
        "appliedCount": 1,
        "failedCount": 0,
        "skippedCount": 2,
    }
    assert enriched["applied"][0]["packageId"] == "demo.workspace"
    assert enriched["applied"][0]["previewOnly"] is True
    assert enriched["applied"][0]["sourceMutated"] is False
    enriched_root = output / "package-sets" / "demo" / "enriched" / "demo.workspace"
    assert (enriched_root / "specpm.yaml").is_file()
    assert (enriched_root / "ai-enrichment-candidate-patch.json").is_file()
    assert "AI-enriched Demo Workspace" in (enriched_root / "specpm.yaml").read_text(
        encoding="utf-8"
    )


def test_autonomous_candidate_batch_skips_warning_ai_enrichment_application(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_draft_proposal",
        lambda _options: completed_ai_draft_proposal(),
    )
    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_enrichment_proposal",
        lambda _options: completed_ai_enrichment_proposal("demo.workspace", status="warning"),
    )

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            lm_studio_model="openai/gpt-oss-20b",
            apply_ai_enrichment=True,
        )
    )

    enriched = report["repositories"][0]["aiEnrichedPreview"]
    assert enriched["status"] == "skipped"
    assert enriched["reason"] == "ai_enrichment_not_clean"
    assert enriched["summary"]["appliedCount"] == 0
    assert enriched["summary"]["skippedCount"] == 3
    assert not (output / "package-sets" / "demo" / "enriched").exists()


def test_autonomous_candidate_batch_failed_ai_enrichment_application_fails_repository(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_draft_proposal",
        lambda _options: completed_ai_draft_proposal(),
    )
    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_enrichment_proposal",
        lambda _options: completed_ai_enrichment_proposal("demo.workspace"),
    )

    def fail_patch(_options: object) -> dict[str, object]:
        raise RuntimeError("unexpected patch failure")

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_ai_enrichment_candidate_patch",
        fail_patch,
    )

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            lm_studio_model="openai/gpt-oss-20b",
            apply_ai_enrichment=True,
        )
    )

    enriched = report["repositories"][0]["aiEnrichedPreview"]
    assert report["status"] == "failed"
    assert report["repositories"][0]["status"] == "failed"
    assert enriched["status"] == "failed"
    assert enriched["summary"]["failedCount"] == 3
    assert enriched["failed"][0]["reason"] == "ai_enrichment_patch_failed"


def test_autonomous_candidate_batch_cli_writes_report(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    exit_code = main(
        [
            "autonomous-candidate-batch",
            str(inputs),
            "--out",
            str(output),
            "--skip-ai",
            "--repository-profile-selection",
            "auto",
        ]
    )

    assert exit_code == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "passed"
    assert printed["collection"]["validationReport"].endswith("batch-validation-report.json")
    assert printed["repositories"][0]["preflight"]["status"] == "passed"
    assert printed["repositories"][0]["repositoryProfileDetection"]["selectedProfileId"] == (
        "generic.package_set.v0"
    )


def write_source_manifest(tmp_path: Path) -> Path:
    inputs = tmp_path / "inputs"
    checkout = write_workspace_checkout(tmp_path / "demo")
    inputs.mkdir()
    (inputs / "repositories.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: 0123456789abcdef0123456789abcdef01234567
    checkout: {checkout}
    packageId: demo.workspace
""",
        encoding="utf-8",
    )
    return inputs


def write_single_package_source_manifest(tmp_path: Path) -> Path:
    inputs = tmp_path / "single-inputs"
    checkout = write_go_single_package_checkout(tmp_path / "gin")
    inputs.mkdir()
    (inputs / "repositories.yml").write_text(
        f"""
repositories:
  - id: gin
    repository: https://github.com/gin-gonic/gin
    revision: 0123456789abcdef0123456789abcdef01234567
    checkout: {checkout}
    packageId: gin.core
""",
        encoding="utf-8",
    )
    return inputs


def write_workspace_checkout(path: Path) -> Path:
    path.mkdir()
    (path / "README.md").write_text(
        "# Demo\n\nDemo workspace for autonomous candidate batch tests.\n",
        encoding="utf-8",
    )
    (path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (path / "package.json").write_text(
        json.dumps(
            {
                "name": "@demo/workspace",
                "private": True,
                "workspaces": ["packages/*"],
                "description": "Demo workspace.",
                "license": "MIT",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    write_package_manifest(
        path / "packages" / "data",
        "@demo/data",
        "Data package.",
    )
    write_package_manifest(
        path / "packages" / "ui",
        "@demo/ui",
        "UI binding package.",
    )
    return path


def write_go_single_package_checkout(path: Path) -> Path:
    path.mkdir()
    (path / "README.md").write_text(
        "# Gin\n\nGin is a web framework written in Go.\n",
        encoding="utf-8",
    )
    (path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (path / "go.mod").write_text(
        "module github.com/gin-gonic/gin\n\ngo 1.22\n",
        encoding="utf-8",
    )
    (path / "gin.go").write_text(
        "package gin\n\nfunc New() *Engine { return &Engine{} }\n\ntype Engine struct{}\n",
        encoding="utf-8",
    )
    return path


def write_package_manifest(package_root: Path, name: str, description: str) -> None:
    package_root.mkdir(parents=True)
    (package_root / "package.json").write_text(
        json.dumps(
            {
                "name": name,
                "version": "0.1.0",
                "description": description,
                "license": "MIT",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (package_root / "README.md").write_text(f"# {name}\n\n{description}\n", encoding="utf-8")


def completed_ai_draft_proposal() -> dict[str, object]:
    return {
        "apiVersion": "spec-harvester.package-set-ai-draft/v0",
        "kind": "SpecHarvesterPackageSetAIDraftProposal",
        "schemaVersion": 1,
        "status": "completed",
        "authority": "proposal_only_not_registry_acceptance",
        "summary": {"proposalCount": 1},
        "diagnostics": [],
        "providerReceipt": {
            "jsonRepairNeeded": False,
            "jsonRepairAttemptCount": 0,
            "jsonRepairStatus": "not_needed",
        },
        "privacy": {"rawModelResponsesPersisted": False},
    }


def completed_ai_enrichment_proposal(
    package_id: str, *, status: str = "completed"
) -> dict[str, object]:
    return {
        "apiVersion": "spec-harvester.package-set-ai-enrichment/v0",
        "kind": "SpecHarvesterPackageSetAIEnrichmentProposal",
        "schemaVersion": 1,
        "status": status,
        "authority": "proposal_only_not_registry_acceptance",
        "provider": {
            "name": "lm_studio",
            "model": "openai/gpt-oss-20b",
            "execution": "operator_opt_in_local",
        },
        "summary": {"proposalCount": 1},
        "diagnostics": [],
        "proposals": [
            {
                "packageId": package_id,
                "status": "proposed",
                "refinedSummary": (
                    "AI-enriched Demo Workspace captures the public workspace "
                    "contract for reviewable starter specs."
                ),
                "overallConfidence": "high",
                "capabilities": [
                    {
                        "id": "demo.workspace.ai_enriched_review",
                        "summary": "Provides AI-enriched review evidence for the demo workspace.",
                        "intentIds": ["intent.spec_authoring.review_ready_starter"],
                        "evidencePaths": [f"{package_id}/specpm.yaml"],
                        "confidence": "high",
                    }
                ],
                "interfaces": [
                    {
                        "id": f"package.{package_id}",
                        "kind": "library",
                        "summary": "Reviewable package interface for the demo workspace.",
                        "evidencePaths": [f"{package_id}/specpm.yaml"],
                        "confidence": "high",
                    }
                ],
                "evidenceGaps": [],
                "providerReceipt": {
                    "responseDigest": "sha256:test",
                    "jsonRepairNeeded": False,
                    "jsonRepairAttemptCount": 0,
                    "jsonRepairStatus": "not_needed",
                },
            }
        ],
        "privacy": {"rawModelResponsesPersisted": False},
    }
