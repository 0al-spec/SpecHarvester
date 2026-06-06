from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import yaml

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.candidate_bundle_preflight import (
    CandidateBundlePreflightOptions,
    run_candidate_bundle_preflight,
)
from spec_harvester.cli import main
from spec_harvester.package_set_drafter import PackageSetDraftOptions, draft_package_set


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
        "packageInventoryCount": 7,
        "relationProposalCount": 3,
        "skippedCount": 3,
    }
    assert summary["relationProposals"] == {
        "path": "package-relation-proposals.json",
        "relationCount": 3,
        "reviewStatus": "producer_observed",
    }
    assert [item["packageId"] for item in summary["skipped"]] == [
        "xyflow.cli",
        "xyflow.e2e",
        "xyflow.playground",
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
    assert workspace_manifest["preview_only"] is True
    assert react_manifest["preview_only"] is True

    react_snapshot = json.loads((out / "xyflow.react" / "harvest.json").read_text())
    assert react_snapshot["source"]["target"] == {
        "kind": "folder",
        "label": "react",
        "path": "packages/react",
    }
    assert react_snapshot["files"][0]["path"] == "packages/react/package.json"
    assert react_snapshot["files"][0]["package"]["name"] == "@xyflow/react"

    for package_id in ("xyflow.workspace", "xyflow.system", "xyflow.react", "xyflow.svelte"):
        preflight = run_candidate_bundle_preflight(
            CandidateBundlePreflightOptions(candidate=out / package_id)
        )
        assert preflight["status"] == "passed"


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
                "value": "ec6adf9e9527fbcc23c66624675bc55ef23301a941460c8c61ba62b85a6c66b5",
            },
            "kind": "package_manifest",
            "packageId": "xyflow.react",
            "packageRole": "target",
            "path": "packages/react/package.json",
            "supports": ["xyflow.workspace.contains.xyflow.react"],
        }
    ]


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
                "name": "xyflow",
                "version": "0.0.0",
                "private": True,
                "workspaces": ["packages/*"],
            }
        ),
        encoding="utf-8",
    )
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
        "packages/system": {"name": "@xyflow/system", "version": "1.0.0"},
        "packages/react": {"name": "@xyflow/react", "version": "12.0.0"},
        "packages/svelte": {"name": "@xyflow/svelte", "version": "1.0.0"},
        "examples/playground": {"name": "@xyflow/playground", "version": "0.0.0"},
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
