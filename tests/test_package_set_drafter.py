from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest
import yaml

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.bundle_set_preflight import (
    BundleSetPreflightOptions,
    run_bundle_set_preflight,
)
from spec_harvester.candidate_bundle_preflight import (
    CandidateBundlePreflightOptions,
    run_candidate_bundle_preflight,
)
from spec_harvester.cli import main
from spec_harvester.package_set_drafter import (
    AUTONOMOUS_POPULAR_MVP_ROLE_SELECTION_PROFILE,
    PackageSetDraftOptions,
    draft_package_set,
)


def test_package_set_drafter_writes_scoped_candidate_bundles(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    result = draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))

    assert result["status"] == "ok"
    assert result["candidateCount"] == 4
    assert result["relationCount"] == 3
    assert [candidate["packageId"] for candidate in result["candidates"]] == [
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "xyflow.workspace",
    ]
    summary = json.loads((out / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["apiVersion"] == "spec-harvester.package-set-draft/v0"
    assert summary["kind"] == "SpecHarvesterPackageSetDraft"
    assert summary["workspaceInventory"]["kind"] == "SpecHarvesterWorkspaceInventory"
    assert summary["summary"] == {
        "candidateCount": 4,
        "packageInventoryCount": 8,
        "relationProposalCount": 3,
        "skippedCount": 4,
    }
    assert summary["authorReadyDraftSummary"]["status"] == "author_ready_draft"
    assert summary["authorReadyDraftSummary"]["decision"] == "stop_for_author_review"
    assert summary["authorReadyDraftSummary"]["memberCounts"] == {
        "author_ready_draft": 4,
        "blocked": 0,
        "needs_regeneration": 0,
        "total": 4,
    }
    assert summary["relationProposals"] == {
        "path": "package-relation-proposals.json",
        "relationCount": 3,
        "reviewStatus": "producer_observed",
    }
    assert all("qualityReport" in item for item in summary["candidates"])
    assert [item["packageId"] for item in summary["skipped"]] == [
        "xyflow.cli",
        "xyflow.e2e",
        "xyflow.react_examples",
        "xyflow.svelte_examples",
    ]
    assert all(
        item["reason"] == "role_not_selected_for_initial_package_set_draft"
        for item in summary["skipped"]
    )

    workspace_manifest = load_manifest(out, "xyflow.workspace")
    system_manifest = load_manifest(out, "xyflow.system")
    react_manifest = load_manifest(out, "xyflow.react")
    svelte_manifest = load_manifest(out, "xyflow.svelte")
    assert workspace_manifest["metadata"]["id"] == "xyflow.workspace"
    assert system_manifest["metadata"]["id"] == "xyflow.system"
    assert react_manifest["metadata"]["id"] == "xyflow.react"
    assert svelte_manifest["metadata"]["id"] == "xyflow.svelte"
    assert workspace_manifest["metadata"]["summary"] == (
        "Xyflow Workspace public package boundary: A highly customizable React library "
        "for building node-based editors and interactive flow charts"
    )
    assert system_manifest["metadata"]["summary"] == (
        "Xyflow System public package boundary: xyflow core system that powers React "
        "Flow and Svelte Flow."
    )
    assert react_manifest["metadata"]["summary"] == (
        "Xyflow React public package boundary: React Flow - A highly customizable React "
        "library for building node-based editors and interactive flow charts."
    )
    assert svelte_manifest["metadata"]["summary"] == (
        "Xyflow Svelte public package boundary: Svelte Flow - A highly customizable "
        "Svelte library for building node-based editors, workflow systems, diagrams "
        "and more."
    )
    assert workspace_manifest["metadata"]["license"] == "MIT"
    assert system_manifest["metadata"]["license"] == "MIT"
    assert react_manifest["metadata"]["license"] == "MIT"
    assert svelte_manifest["metadata"]["license"] == "MIT"
    assert workspace_manifest["index"]["provides"]["capabilities"] == ["xyflow.workspace.workspace"]
    assert system_manifest["index"]["provides"]["capabilities"] == [
        "xyflow.system.flow_system_utilities"
    ]
    assert react_manifest["index"]["provides"]["capabilities"] == ["xyflow.react.flow_canvas"]
    assert svelte_manifest["index"]["provides"]["capabilities"] == ["xyflow.svelte.flow_canvas"]
    assert "intent.ui.node_based_editor" in react_manifest["index"]["provides"]["intents"]
    assert "intent.ui.flow_diagramming" in react_manifest["index"]["provides"]["intents"]
    assert "intent.ui.diagramming" in svelte_manifest["index"]["provides"]["intents"]
    assert "intent.ui.flow_system_utilities" in system_manifest["index"]["provides"]["intents"]
    assert workspace_manifest["preview_only"] is True
    assert react_manifest["preview_only"] is True

    react_snapshot = json.loads((out / "xyflow.react" / "harvest.json").read_text())
    react_quality = json.loads(
        (out / "xyflow.react" / "author-ready-draft-quality-report.json").read_text()
    )
    assert react_snapshot["source"]["target"] == {
        "kind": "folder",
        "label": "react",
        "path": "packages/react",
    }
    assert react_snapshot["files"][0]["path"] == "packages/react/package.json"
    assert react_snapshot["files"][0]["size"] > 0
    assert react_snapshot["files"][0]["package"]["name"] == "@xyflow/react"
    assert react_snapshot["files"][0]["package"]["description"] == (
        "React Flow - A highly customizable React library for building node-based "
        "editors and interactive flow charts."
    )
    assert react_snapshot["files"][0]["package"]["license"] == "MIT"
    assert react_snapshot["files"][0]["package"]["capabilityLabel"] == "flow_canvas"
    assert react_quality["authorReadyDraft"]["status"] == "author_ready_draft"

    for package_id in ("xyflow.workspace", "xyflow.system", "xyflow.react", "xyflow.svelte"):
        preflight = run_candidate_bundle_preflight(
            CandidateBundlePreflightOptions(candidate=out / package_id)
        )
        assert preflight["status"] == "passed"


def test_package_set_drafter_generic_monorepo_profile_selects_members(
    tmp_path: Path,
) -> None:
    inventory = write_generic_monorepo_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    result = draft_package_set(
        PackageSetDraftOptions(
            inventory=inventory,
            out=out,
            role_profile="generic_monorepo",
        )
    )

    assert result["status"] == "ok"
    assert result["candidateCount"] == 3
    assert result["relationCount"] == 2
    assert [candidate["packageId"] for candidate in result["candidates"]] == [
        "tanstack_query.core",
        "tanstack_query.devtools",
        "tanstack_query.workspace",
    ]
    assert [item["packageId"] for item in result["skipped"]] == [
        "tanstack_query.example",
        "tanstack_query.scripts",
    ]
    summary = json.loads((out / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["selection"] == {
        "authority": "producer_preview_selection",
        "roleProfile": "generic_monorepo",
        "roles": ["workspace", "member_package"],
    }
    assert summary["summary"] == {
        "candidateCount": 3,
        "packageInventoryCount": 5,
        "relationProposalCount": 2,
        "skippedCount": 2,
    }
    relations = json.loads((out / "package-relation-proposals.json").read_text(encoding="utf-8"))
    assert {
        (relation["source"]["packageId"], relation["type"], relation["target"]["packageId"])
        for relation in relations["relations"]
    } == {
        ("tanstack_query.workspace", "contains", "tanstack_query.core"),
        ("tanstack_query.workspace", "contains", "tanstack_query.devtools"),
    }


def test_package_set_drafter_autonomous_popular_profile_keeps_primary_roles(
    tmp_path: Path,
) -> None:
    inventory = write_autonomous_popular_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    result = draft_package_set(
        PackageSetDraftOptions(
            inventory=inventory,
            out=out,
            role_profile=AUTONOMOUS_POPULAR_MVP_ROLE_SELECTION_PROFILE,
        )
    )

    assert result["status"] == "ok"
    assert [candidate["packageId"] for candidate in result["candidates"]] == [
        "popular.core",
        "popular.react",
        "popular.utils",
        "popular.workspace",
    ]
    assert [item["packageId"] for item in result["skipped"]] == [
        "popular.example",
        "popular.private_tools",
    ]
    assert result["relationCount"] == 3
    summary = json.loads((out / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["selection"]["roleProfile"] == AUTONOMOUS_POPULAR_MVP_ROLE_SELECTION_PROFILE
    assert summary["selection"]["roles"] == [
        "workspace",
        "core_runtime",
        "react_binding",
        "svelte_binding",
        "member_package",
    ]


def test_package_set_drafter_uses_single_package_fallback_for_python_repo(
    tmp_path: Path,
) -> None:
    inventory = write_single_package_inventory_fixture(
        tmp_path,
        repository_id="flask",
        repository="https://github.com/pallets/flask",
        package_id="flask.core",
        checkout=make_python_single_package_checkout(tmp_path / "flask"),
    )
    out = tmp_path / "draft-set"

    result = draft_package_set(
        PackageSetDraftOptions(
            inventory=inventory,
            out=out,
            role_profile=AUTONOMOUS_POPULAR_MVP_ROLE_SELECTION_PROFILE,
        )
    )

    assert result["status"] == "ok"
    assert result["candidateCount"] == 1
    assert result["relationCount"] == 0
    assert [candidate["packageId"] for candidate in result["candidates"]] == ["flask.core"]
    summary = json.loads((out / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["source"]["packageId"] == "flask.core"
    assert summary["summary"] == {
        "candidateCount": 1,
        "packageInventoryCount": 0,
        "relationProposalCount": 0,
        "skippedCount": 0,
    }
    assert summary["candidates"][0]["selectionReason"] == (
        "single_package_source_manifest_fallback"
    )
    assert summary["candidates"][0]["role"] == "single_package"
    assert summary["relationProposals"]["relationCount"] == 0
    relations = json.loads((out / "package-relation-proposals.json").read_text(encoding="utf-8"))
    assert relations["relations"] == []
    assert relations["summary"] == {
        "containsCount": 0,
        "relationCount": 0,
        "sourcePackageCount": 0,
        "targetPackageCount": 0,
    }

    manifest = load_manifest(out, "flask.core")
    assert manifest["metadata"]["id"] == "flask.core"
    assert manifest["preview_only"] is True
    assert (out / "flask.core" / "public-interface-index.json").is_file()
    assert (out / "flask.core" / "producer-receipt.json").is_file()
    assert (out / "flask.core" / "validation-report.json").is_file()
    assert (out / "flask.core" / "diagnostics.json").is_file()
    assert (out / "flask.core" / "author-ready-draft-quality-report.json").is_file()

    preflight = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))
    assert preflight["status"] == "passed"
    assert preflight["summary"] == {
        "candidateCount": 1,
        "candidatePreflightPassedCount": 1,
        "diagnosticCount": 0,
        "errorCount": 0,
        "relationCount": 0,
        "warningCount": 0,
    }


def test_package_set_drafter_sanitizes_single_package_manifest_id(
    tmp_path: Path,
) -> None:
    inventory = write_single_package_inventory_fixture(
        tmp_path,
        repository_id="unsafe",
        repository="https://github.com/example/unsafe",
        package_id="../..",
        checkout=make_python_single_package_checkout(tmp_path / "unsafe"),
    )
    out = tmp_path / "draft-set"

    result = draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))

    assert result["status"] == "ok"
    assert [candidate["packageId"] for candidate in result["candidates"]] == ["package.core"]
    assert (out / "package.core" / "specpm.yaml").is_file()
    assert not (tmp_path / "specpm.yaml").exists()


def test_package_set_drafter_explicit_roles_override_profile(tmp_path: Path) -> None:
    inventory = write_generic_monorepo_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    result = draft_package_set(
        PackageSetDraftOptions(
            inventory=inventory,
            out=out,
            roles=("workspace",),
            role_profile="generic_monorepo",
        )
    )

    assert result["candidateCount"] == 1
    assert result["relationCount"] == 0
    summary = json.loads((out / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["selection"] == {
        "authority": "producer_preview_selection",
        "roleProfile": "custom",
        "roles": ["workspace"],
    }


def test_package_set_drafter_writes_relation_proposals(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))

    payload = json.loads((out / "package-relation-proposals.json").read_text(encoding="utf-8"))
    assert payload["apiVersion"] == "spec-harvester.package-relation-proposals/v0"
    assert payload["kind"] == "SpecHarvesterPackageRelationProposals"
    assert payload["reviewStatus"] == "producer_observed"
    assert payload["authority"] == "producer_observed_review_evidence"
    assert payload["inputs"]["workspaceInventory"]["path"] == "workspace-inventory.json"
    assert payload["inputs"]["workspaceInventory"]["digest"]["algorithm"] == "sha256"
    assert payload["inputs"]["packageSetDraft"]["path"] == "package-set-draft.json"
    assert payload["inputs"]["packageSetDraft"]["digest"]["algorithm"] == "sha256"
    assert payload["summary"] == {
        "containsCount": 3,
        "relationCount": 3,
        "sourcePackageCount": 1,
        "targetPackageCount": 3,
    }

    relations = payload["relations"]
    assert [
        (item["source"]["packageId"], item["type"], item["target"]["packageId"])
        for item in relations
    ] == [
        ("xyflow.workspace", "contains", "xyflow.react"),
        ("xyflow.workspace", "contains", "xyflow.svelte"),
        ("xyflow.workspace", "contains", "xyflow.system"),
    ]
    assert all(item["reviewStatus"] == "producer_observed" for item in relations)
    assert all(item["authority"] == "producer_observed_review_evidence" for item in relations)

    react_relation = next(
        item for item in relations if item["target"]["packageId"] == "xyflow.react"
    )
    evidence_paths = {item["path"] for item in react_relation["evidence"]}
    assert {
        "package.json",
        "pnpm-workspace.yaml",
        "packages/react/package.json",
    }.issubset(evidence_paths)
    target_evidence = [
        item for item in react_relation["evidence"] if item.get("packageRole") == "target"
    ]
    assert target_evidence == [
        {
            "digest": {
                "algorithm": "sha256",
                "value": "7760572ec571e038759b8413beb099814cde566d944ad01533652b582ae2711e",
            },
            "kind": "package_manifest",
            "packageId": "xyflow.react",
            "packageRole": "target",
            "path": "packages/react/package.json",
            "supports": ["xyflow.workspace.contains.xyflow.react"],
        }
    ]


def test_bundle_set_preflight_passes_generated_package_set(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["apiVersion"] == "spec-harvester.bundle-set-preflight/v0"
    assert report["kind"] == "SpecHarvesterBundleSetPreflightReport"
    assert report["status"] == "passed"
    assert report["summary"] == {
        "candidateCount": 4,
        "candidatePreflightPassedCount": 4,
        "diagnosticCount": 0,
        "errorCount": 0,
        "relationCount": 3,
        "warningCount": 0,
    }
    assert [item["packageId"] for item in report["candidateReports"]] == [
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
        "xyflow.workspace",
    ]


def test_bundle_set_preflight_fails_dangling_relation_target(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    relation_path = out / "package-relation-proposals.json"
    relation_payload = json.loads(relation_path.read_text(encoding="utf-8"))
    relation_payload["relations"][0]["target"]["packageId"] = "xyflow.missing"
    relation_path.write_text(
        json.dumps(relation_payload, indent=2, sort_keys=True), encoding="utf-8"
    )

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "relation_target_missing" in diagnostic_codes(report)


def test_bundle_set_preflight_fails_package_set_draft_digest_mismatch(
    tmp_path: Path,
) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    draft_path = out / "package-set-draft.json"
    draft_payload = json.loads(draft_path.read_text(encoding="utf-8"))
    draft_payload["selection"]["roles"].append("extra_role")
    draft_path.write_text(json.dumps(draft_payload, indent=2, sort_keys=True), encoding="utf-8")

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "relation_package_set_draft_digest_mismatch" in diagnostic_codes(report)


def test_bundle_set_preflight_fails_duplicate_candidate_package_id(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    draft_path = out / "package-set-draft.json"
    draft_payload = json.loads(draft_path.read_text(encoding="utf-8"))
    duplicate = dict(draft_payload["candidates"][0])
    duplicate["candidatePath"] = draft_payload["candidates"][1]["candidatePath"]
    draft_payload["candidates"].append(duplicate)
    draft_payload["summary"]["candidateCount"] += 1
    draft_path.write_text(json.dumps(draft_payload, indent=2, sort_keys=True), encoding="utf-8")

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "candidate_package_id_duplicate" in diagnostic_codes(report)


def test_bundle_set_preflight_fails_swapped_candidate_path(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    draft_path = out / "package-set-draft.json"
    draft_payload = json.loads(draft_path.read_text(encoding="utf-8"))
    first = draft_payload["candidates"][0]
    second = draft_payload["candidates"][1]
    first["candidatePath"], second["candidatePath"] = (
        second["candidatePath"],
        first["candidatePath"],
    )
    draft_path.write_text(json.dumps(draft_payload, indent=2, sort_keys=True), encoding="utf-8")

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "candidate_package_id_mismatch" in diagnostic_codes(report)


def test_bundle_set_preflight_fails_candidate_diagnostics_status(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    diagnostics_path = out / "xyflow.react" / "diagnostics.json"
    diagnostics_payload = json.loads(diagnostics_path.read_text(encoding="utf-8"))
    diagnostics_payload["status"] = "failed"
    diagnostics_path.write_text(
        json.dumps(diagnostics_payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "candidate_diagnostics_status_failed" in diagnostic_codes(report)
    react_report = next(
        item for item in report["candidateReports"] if item["packageId"] == "xyflow.react"
    )
    assert react_report["diagnosticsStatus"] == "failed"


def test_bundle_set_preflight_rejects_escaped_candidate_diagnostics_report(
    tmp_path: Path,
) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    (tmp_path / "outside-diagnostics.json").write_text(
        json.dumps({"status": "clean"}), encoding="utf-8"
    )
    draft_path = out / "package-set-draft.json"
    draft_payload = json.loads(draft_path.read_text(encoding="utf-8"))
    draft_payload["candidates"][0]["diagnosticsReport"] = "../outside-diagnostics.json"
    draft_path.write_text(json.dumps(draft_payload, indent=2, sort_keys=True), encoding="utf-8")

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "bundle_set_path_escape" in diagnostic_codes(report)


def test_bundle_set_preflight_rejects_escaped_workspace_inventory_path(
    tmp_path: Path,
) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    outside_inventory = tmp_path / "outside-workspace-inventory.json"
    outside_inventory.write_text(inventory.read_text(encoding="utf-8"), encoding="utf-8")
    outside_digest = {"algorithm": "sha256", "value": sha256_text(outside_inventory)}
    draft_path = out / "package-set-draft.json"
    relation_path = out / "package-relation-proposals.json"
    draft_payload = json.loads(draft_path.read_text(encoding="utf-8"))
    relation_payload = json.loads(relation_path.read_text(encoding="utf-8"))
    for record in (
        draft_payload["workspaceInventory"],
        relation_payload["inputs"]["workspaceInventory"],
    ):
        record["path"] = "../outside-workspace-inventory.json"
        record["digest"] = outside_digest
    draft_path.write_text(json.dumps(draft_payload, indent=2, sort_keys=True), encoding="utf-8")
    relation_path.write_text(
        json.dumps(relation_payload, indent=2, sort_keys=True), encoding="utf-8"
    )

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "bundle_set_path_escape" in diagnostic_codes(report)


def test_bundle_set_preflight_fails_relation_record_authority(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))
    relation_path = out / "package-relation-proposals.json"
    relation_payload = json.loads(relation_path.read_text(encoding="utf-8"))
    relation_payload["relations"][0]["authority"] = "accepted_registry_relation"
    relation_path.write_text(
        json.dumps(relation_payload, indent=2, sort_keys=True), encoding="utf-8"
    )

    report = run_bundle_set_preflight(BundleSetPreflightOptions(bundle_set=out))

    assert report["status"] == "failed"
    assert "relation_record_authority_invalid" in diagnostic_codes(report)


def test_cli_preflight_bundle_set_reports_status(tmp_path: Path, capsys) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))

    result = main(["preflight-bundle-set", str(out)])

    assert result == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "passed"
    assert printed["summary"]["candidateCount"] == 4


def test_cli_preflight_bundle_set_fails_invalid_set(tmp_path: Path, capsys) -> None:
    out = tmp_path / "draft-set"
    out.mkdir()

    result = main(["preflight-bundle-set", str(out)])

    assert result == 1
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "failed"
    assert "required_file_missing" in diagnostic_codes(printed)


def test_package_set_drafter_is_deterministic(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"

    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=first))
    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=second))

    assert (first / "package-set-draft.json").read_text(encoding="utf-8") == (
        second / "package-set-draft.json"
    ).read_text(encoding="utf-8")
    assert (first / "package-relation-proposals.json").read_text(encoding="utf-8") == (
        second / "package-relation-proposals.json"
    ).read_text(encoding="utf-8")
    assert (first / "xyflow.react" / "specpm.yaml").read_text(encoding="utf-8") == (
        second / "xyflow.react" / "specpm.yaml"
    ).read_text(encoding="utf-8")


def test_package_set_drafter_refuses_non_empty_output(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"
    out.mkdir()
    (out / "stale-candidate").mkdir()

    with pytest.raises(ValueError, match="output directory is not empty"):
        draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out))


def test_package_set_drafter_preserves_nested_workspace_target(tmp_path: Path) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    payload = json.loads(inventory.read_text(encoding="utf-8"))
    workspace_package = next(
        package
        for package in payload["packages"]
        if package["proposedSpecpmPackageId"] == "xyflow.workspace"
    )
    workspace_package["manifestPath"] = "apps/web/package.json"
    workspace_package["sourceTargetPath"] = "apps/web"
    inventory.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    out = tmp_path / "draft-set"

    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out, roles=("workspace",)))

    snapshot = json.loads((out / "xyflow.workspace" / "harvest.json").read_text())
    assert snapshot["source"]["target"] == {
        "kind": "folder",
        "label": "web",
        "path": "apps/web",
    }
    assert snapshot["files"][0]["path"] == "apps/web/package.json"


def test_package_set_drafter_keeps_generic_react_binding_capability_neutral(
    tmp_path: Path,
) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    payload = json.loads(inventory.read_text(encoding="utf-8"))
    react_package = next(
        package for package in payload["packages"] if package["role"] == "react_binding"
    )
    react_package["name"] = "@demo/react-binding"
    react_package["description"] = "Generic React integration package."
    react_package["proposedSpecpmPackageId"] = "demo.react"
    react_package["manifestPath"] = "packages/react-binding/package.json"
    react_package["sourceTargetPath"] = "packages/react-binding"
    react_package["evidenceReferences"] = [
        {
            "kind": "package_manifest",
            "path": "packages/react-binding/package.json",
            "digest": {
                "algorithm": "sha256",
                "value": "0" * 64,
            },
        }
    ]
    inventory.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    out = tmp_path / "draft-set"

    draft_package_set(
        PackageSetDraftOptions(inventory=inventory, out=out, roles=("react_binding",))
    )

    manifest = load_manifest(out, "demo.react")
    assert manifest["index"]["provides"]["capabilities"] == ["demo.react.package_boundary"]
    assert "intent.ui.flow_diagramming" not in manifest["index"]["provides"]["intents"]
    snapshot = json.loads((out / "demo.react" / "harvest.json").read_text(encoding="utf-8"))
    assert snapshot["files"][0]["package"]["capabilityLabel"] == "package_boundary"


def test_package_set_drafter_falls_back_when_evidence_references_are_not_list(
    tmp_path: Path,
) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    payload = json.loads(inventory.read_text(encoding="utf-8"))
    system_package = next(
        package
        for package in payload["packages"]
        if package["proposedSpecpmPackageId"] == "xyflow.system"
    )
    system_package["evidenceReferences"] = None
    inventory.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    out = tmp_path / "draft-set"

    draft_package_set(PackageSetDraftOptions(inventory=inventory, out=out, roles=("core_runtime",)))

    snapshot = json.loads((out / "xyflow.system" / "harvest.json").read_text())
    digest = snapshot["files"][0]["sha256"]
    assert isinstance(digest, str)
    assert len(digest) == 64


def test_cli_draft_package_set_writes_summary(tmp_path: Path, capsys) -> None:
    inventory = write_workspace_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    result = main(["draft-package-set", str(inventory), "--out", str(out)])

    assert result == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "ok"
    assert printed["candidateCount"] == 4
    assert printed["relationCount"] == 3
    assert printed["summary"] == str(out / "package-set-draft.json")
    assert printed["relationProposals"] == str(out / "package-relation-proposals.json")
    assert (out / "xyflow.workspace" / "specpm.yaml").is_file()


def test_cli_draft_package_set_accepts_generic_monorepo_profile(
    tmp_path: Path,
    capsys,
) -> None:
    inventory = write_generic_monorepo_inventory_fixture(tmp_path)
    out = tmp_path / "draft-set"

    result = main(
        [
            "draft-package-set",
            str(inventory),
            "--out",
            str(out),
            "--role-profile",
            "generic_monorepo",
        ]
    )

    assert result == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["candidateCount"] == 3
    assert printed["relationCount"] == 2
    summary = json.loads((out / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["selection"]["roleProfile"] == "generic_monorepo"
    assert summary["selection"]["roles"] == ["workspace", "member_package"]


def write_workspace_inventory_fixture(tmp_path: Path) -> Path:
    inputs = tmp_path / "inputs"
    candidates = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_workspace_checkout(tmp_path / "xyflow")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: xyflow
    repository: https://github.com/xyflow/xyflow
    revision: abc123
    checkout: {relative_to(checkout, inputs)}
    packageId: xyflow.workspace
""",
        encoding="utf-8",
    )
    collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=candidates,
            emit_workspace_inventory=True,
        )
    )
    return candidates / "xyflow" / "workspace-inventory.json"


def write_generic_monorepo_inventory_fixture(tmp_path: Path) -> Path:
    inventory = tmp_path / "generic-workspace-inventory.json"
    payload = {
        "apiVersion": "spec-harvester.workspace-inventory/v0",
        "kind": "SpecHarvesterWorkspaceInventory",
        "schemaVersion": 1,
        "source": {
            "repository": "https://github.com/TanStack/query",
            "exactRevision": "feb1efd804c1262106f72c8adc1d82a8ce9cfbb0",
            "revisionAuthority": "operator_pinned",
            "declaredRef": "main",
        },
        "workspaceManifests": [
            {
                "path": "pnpm-workspace.yaml",
                "packageManager": "pnpm",
                "includePatterns": ["packages/*", "examples/*", "scripts/*"],
                "excludePatterns": [],
                "evidence": {
                    "kind": "workspace_manifest",
                    "path": "pnpm-workspace.yaml",
                    "digest": digest_for("pnpm-workspace.yaml"),
                },
            }
        ],
        "packages": [
            generic_package_record(
                "package.json",
                "tanstack_query.workspace",
                "workspace",
                "@tanstack/query-workspace",
            ),
            generic_package_record(
                "packages/query-core/package.json",
                "tanstack_query.core",
                "member_package",
                "@tanstack/query-core",
            ),
            generic_package_record(
                "packages/query-devtools/package.json",
                "tanstack_query.devtools",
                "member_package",
                "@tanstack/query-devtools",
            ),
            generic_package_record(
                "examples/react/package.json",
                "tanstack_query.example",
                "example_package",
                "react-query-example",
            ),
            generic_package_record(
                "scripts/package.json",
                "tanstack_query.scripts",
                "tooling_package",
                "@tanstack/query-scripts",
            ),
        ],
    }
    inventory.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return inventory


def write_autonomous_popular_inventory_fixture(tmp_path: Path) -> Path:
    inventory = tmp_path / "autonomous-popular-workspace-inventory.json"
    payload = {
        "apiVersion": "spec-harvester.workspace-inventory/v0",
        "kind": "SpecHarvesterWorkspaceInventory",
        "schemaVersion": 1,
        "source": {
            "repository": "https://github.com/example/popular",
            "exactRevision": "0123456789abcdef0123456789abcdef01234567",
            "revisionAuthority": "operator_pinned",
            "declaredRef": "main",
        },
        "workspaceManifests": [
            {
                "path": "pnpm-workspace.yaml",
                "packageManager": "pnpm",
                "includePatterns": ["packages/*", "examples/*", "tools/*"],
                "excludePatterns": [],
                "evidence": {
                    "kind": "workspace_manifest",
                    "path": "pnpm-workspace.yaml",
                    "digest": digest_for("pnpm-workspace.yaml"),
                },
            }
        ],
        "packages": [
            generic_package_record(
                "package.json",
                "popular.workspace",
                "workspace",
                "@popular/workspace",
            ),
            generic_package_record(
                "packages/core/package.json",
                "popular.core",
                "core_runtime",
                "@popular/core",
            ),
            generic_package_record(
                "packages/react/package.json",
                "popular.react",
                "react_binding",
                "@popular/react",
            ),
            generic_package_record(
                "packages/utils/package.json",
                "popular.utils",
                "member_package",
                "@popular/utils",
            ),
            generic_package_record(
                "examples/react/package.json",
                "popular.example",
                "example_package",
                "popular-react-example",
            ),
            generic_package_record(
                "tools/package.json",
                "popular.private_tools",
                "private_tooling_package",
                "@popular/tools",
            ),
        ],
    }
    inventory.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return inventory


def write_single_package_inventory_fixture(
    tmp_path: Path,
    *,
    repository_id: str,
    repository: str,
    package_id: str,
    checkout: Path,
) -> Path:
    inputs = tmp_path / f"{repository_id}-inputs"
    candidates = tmp_path / f"{repository_id}-candidates"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: {repository_id}
    repository: {repository}
    revision: 0123456789abcdef0123456789abcdef01234567
    checkout: {relative_to(checkout, inputs)}
    packageId: {package_id}
""",
        encoding="utf-8",
    )
    collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=candidates,
            emit_interface_indexes=True,
            emit_workspace_inventory=True,
        )
    )
    return candidates / repository_id / "workspace-inventory.json"


def make_python_single_package_checkout(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text(
        "# Flask\n\nA Python web framework for building web applications.\n",
        encoding="utf-8",
    )
    (path / "LICENSE.txt").write_text("BSD-3-Clause\n", encoding="utf-8")
    (path / "pyproject.toml").write_text(
        """
[project]
name = "flask"
version = "3.0.0"
description = "A simple framework for building complex web applications."
license = {text = "BSD-3-Clause"}
""".lstrip(),
        encoding="utf-8",
    )
    package_root = path / "src" / "flask"
    package_root.mkdir(parents=True)
    (package_root / "__init__.py").write_text(
        "class Flask:\n    pass\n\n__all__ = ['Flask']\n",
        encoding="utf-8",
    )
    return path


def generic_package_record(
    manifest_path: str,
    package_id: str,
    role: str,
    name: str,
) -> dict[str, object]:
    return {
        "manifestPath": manifest_path,
        "sourceTargetPath": "." if role == "workspace" else str(Path(manifest_path).parent),
        "proposedSpecpmPackageId": package_id,
        "role": role,
        "name": name,
        "version": "0.0.0",
        "ecosystem": "npm",
        "packageManager": "pnpm",
        "description": f"Generated fixture package for {package_id}.",
        "license": "MIT",
        "evidenceReferences": [
            {
                "kind": "package_manifest",
                "path": manifest_path,
                "size": 128,
                "digest": digest_for(manifest_path),
            }
        ],
    }


def digest_for(value: str) -> dict[str, str]:
    return {
        "algorithm": "sha256",
        "value": hashlib.sha256(value.encode("utf-8")).hexdigest(),
    }


def load_manifest(out: Path, package_id: str) -> dict[str, object]:
    return json.loads(
        json.dumps(yaml.safe_load((out / package_id / "specpm.yaml").read_text(encoding="utf-8")))
    )


def make_workspace_checkout(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text("# Xyflow\n", encoding="utf-8")
    (path / "package.json").write_text(
        json.dumps(
            {
                "name": "@xyflow/monorepo",
                "version": "0.0.0",
                "description": (
                    "A highly customizable React library for building node-based "
                    "editors and interactive flow charts"
                ),
                "license": "MIT",
                "private": True,
                "packageManager": "pnpm@9.2.0",
            }
        ),
        encoding="utf-8",
    )
    (path / "pnpm-lock.yaml").write_text("lockfileVersion: '9.0'\n", encoding="utf-8")
    (path / "pnpm-workspace.yaml").write_text(
        """
packages:
  - packages/*
  - examples/*
  - tooling/*
  - tests/*
  - "!**/test-fixtures/**"
""",
        encoding="utf-8",
    )
    packages = {
        "packages/system": {
            "name": "@xyflow/system",
            "version": "1.0.0",
            "description": "xyflow core system that powers React Flow and Svelte Flow.",
            "license": "MIT",
        },
        "packages/react": {
            "name": "@xyflow/react",
            "version": "12.0.0",
            "description": (
                "React Flow - A highly customizable React library for building "
                "node-based editors and interactive flow charts."
            ),
            "license": "MIT",
        },
        "packages/svelte": {
            "name": "@xyflow/svelte",
            "version": "1.0.0",
            "description": (
                "Svelte Flow - A highly customizable Svelte library for building "
                "node-based editors, workflow systems, diagrams and more."
            ),
            "license": "MIT",
        },
        "examples/react": {"name": "react-examples", "version": "0.0.0"},
        "examples/svelte": {"name": "svelte-examples", "version": "0.0.0"},
        "tooling/cli": {"name": "@xyflow/cli", "version": "0.1.0"},
        "tests/e2e": {"name": "@xyflow/e2e", "version": "0.0.0"},
    }
    for relative, payload in packages.items():
        package_dir = path / relative
        package_dir.mkdir(parents=True)
        (package_dir / "package.json").write_text(json.dumps(payload), encoding="utf-8")
    return path


def relative_to(path: Path, root: Path) -> str:
    return Path(os.path.relpath(path, root)).as_posix()


def sha256_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def diagnostic_codes(report: dict[str, object]) -> set[str]:
    diagnostics = report.get("diagnostics")
    assert isinstance(diagnostics, list)
    return {str(item["code"]) for item in diagnostics if isinstance(item, dict)}
