from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.cli import main


def test_collect_batch_snapshots_writes_deterministic_candidate_paths(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    checkouts = tmp_path / "checkouts"
    out = tmp_path / "candidates"
    inputs.mkdir()
    alpha = make_checkout(checkouts / "alpha", "# Alpha\n")
    beta = make_checkout(checkouts / "beta", "# Beta\n")
    (inputs / "a.yml").write_text(
        f"""
repositories:
  - id: alpha
    repository: https://github.com/example/alpha
    revision: aaa
    checkout: {relative_to(alpha, inputs)}
""",
        encoding="utf-8",
    )
    (inputs / "z.yml").write_text(
        f"""
repositories:
  - id: beta
    repository: https://github.com/example/beta
    revision: bbb
    checkout: {relative_to(beta, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=out,
            selected_ids=("beta", "alpha"),
        )
    )

    assert [item["id"] for item in result["collected"]] == ["alpha", "beta"]
    assert result["skipped"] == []
    assert (out / "alpha" / "harvest.json").is_file()
    assert (out / "beta" / "harvest.json").is_file()
    alpha_snapshot = json.loads((out / "alpha" / "harvest.json").read_text(encoding="utf-8"))
    assert alpha_snapshot["source"]["repository"] == "https://github.com/example/alpha"
    assert alpha_snapshot["source"]["revision"] == "aaa"
    assert alpha_snapshot["summary"]["fileCount"] == 1


def test_collect_batch_snapshots_records_unselected_repositories(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    checkouts = tmp_path / "checkouts"
    out = tmp_path / "candidates"
    inputs.mkdir()
    alpha = make_checkout(checkouts / "alpha", "# Alpha\n")
    beta = make_checkout(checkouts / "beta", "# Beta\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: alpha
    repository: https://github.com/example/alpha
    revision: aaa
    checkout: {relative_to(alpha, inputs)}
  - id: beta
    repository: https://github.com/example/beta
    revision: bbb
    checkout: {relative_to(beta, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, selected_ids=("alpha",))
    )

    assert [item["id"] for item in result["collected"]] == ["alpha"]
    assert result["skipped"] == [{"id": "beta", "reason": "not_selected"}]
    assert (out / "alpha" / "harvest.json").is_file()
    assert not (out / "beta").exists()


def test_collect_batch_snapshots_does_not_emit_interface_indexes_by_default(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (checkout / "demo.py").write_text("def public_api():\n    return None\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert "interfaceIndex" not in result["collected"][0]
    assert not (out / "demo" / "public-interface-index.json").exists()


def test_collect_batch_snapshots_uses_scoped_target_from_source_manifest(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Root\n")
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    feature = checkout / "Modules" / "Feature"
    feature.mkdir(parents=True)
    (feature / "API.swift").write_text("public struct FeatureAPI {}\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: feature
    repository: https://github.com/example/monorepo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: Modules/Feature
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert result["collected"][0]["target"] == "Modules/Feature"
    snapshot = json.loads((out / "feature" / "harvest.json").read_text(encoding="utf-8"))
    assert snapshot["source"]["target"] == {
        "kind": "folder",
        "path": "Modules/Feature",
        "label": "Feature",
    }
    assert [item["path"] for item in snapshot["files"]] == [
        "LICENSE",
        "Modules/Feature/API.swift",
    ]


def test_collect_batch_snapshots_runs_interface_analyzer_on_scoped_target(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Root\n")
    feature = checkout / "Modules" / "Feature"
    other = checkout / "Modules" / "Other"
    feature.mkdir(parents=True)
    other.mkdir(parents=True)
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (feature / "API.swift").write_text("public struct FeatureAPI {}\n", encoding="utf-8")
    (other / "Other.swift").write_text("public struct OtherAPI {}\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: feature
    repository: https://github.com/example/monorepo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: Modules/Feature
    packageId: feature.swift
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_interface_indexes=True)
    )

    assert result["collected"][0]["interfaceIndex"]["status"] == "complete"
    index = json.loads((out / "feature" / "public-interface-index.json").read_text())
    assert index["packages"][0]["id"] == "feature.swift"
    assert index["packages"][0]["entrypoints"][0]["path"] == "API.swift"
    assert "Other.swift" not in json.dumps(index)


def test_collect_batch_snapshots_keeps_python_scoped_analyzer_out_of_vendor(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Root\n")
    feature = checkout / "services" / "feature"
    vendor = feature / "vendor"
    feature.mkdir(parents=True)
    vendor.mkdir()
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (feature / "api.py").write_text("def public_api():\n    return None\n", encoding="utf-8")
    (vendor / "private_api.py").write_text(
        "def leaked_vendor_api():\n    return None\n",
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: feature
    repository: https://github.com/example/monorepo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: services/feature
    packageId: feature.python
""",
        encoding="utf-8",
    )

    collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_interface_indexes=True)
    )

    snapshot = json.loads((out / "feature" / "harvest.json").read_text(encoding="utf-8"))
    assert [item["path"] for item in snapshot["files"]] == [
        "LICENSE",
        "services/feature/api.py",
    ]
    index = json.loads((out / "feature" / "public-interface-index.json").read_text())
    assert index["packages"][0]["entrypoints"][0]["path"] == "api.py"
    assert "leaked_vendor_api" not in json.dumps(index)


def test_collect_batch_snapshots_covers_scoped_source_validation_matrix(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_scoped_source_matrix_checkout(tmp_path / "checkout")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: tuist-player
    repository: https://github.com/example/mobile-monorepo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: Apps/Player
    packageId: mobile.player
  - id: python-service
    repository: https://github.com/example/mobile-monorepo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: services/catalog
    packageId: services.catalog
  - id: single-tool
    repository: https://github.com/example/mobile-monorepo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: tools/report.py
    packageId: tools.report
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_interface_indexes=True)
    )

    assert [item["id"] for item in result["collected"]] == [
        "tuist-player",
        "python-service",
        "single-tool",
    ]
    assert result["skipped"] == []
    snapshots = {
        item["id"]: json.loads((out / item["id"] / "harvest.json").read_text(encoding="utf-8"))
        for item in result["collected"]
    }
    assert snapshots["tuist-player"]["source"]["target"] == {
        "kind": "folder",
        "path": "Apps/Player",
        "label": "Player",
    }
    assert snapshots["python-service"]["source"]["target"] == {
        "kind": "folder",
        "path": "services/catalog",
        "label": "catalog",
    }
    assert snapshots["single-tool"]["source"]["target"] == {
        "kind": "file",
        "path": "tools/report.py",
        "label": "report",
    }
    assert snapshot_paths(snapshots["tuist-player"]) == [
        "Apps/Player/Project.swift",
        "Apps/Player/Sources/PlayerAPI.swift",
        "LICENSE",
    ]
    assert snapshot_paths(snapshots["python-service"]) == [
        "LICENSE",
        "services/catalog/api.py",
    ]
    assert snapshot_paths(snapshots["single-tool"]) == [
        "LICENSE",
        "tools/report.py",
    ]
    assert snapshots["tuist-player"]["files"][0]["package"]["ecosystem"] == "tuist"
    assert "Apps/Other/Other.swift" not in json.dumps(snapshots)
    assert "services/other/api.py" not in json.dumps(snapshots)
    assert "tools/ignored.py" not in json.dumps(snapshots)

    assert_interface_index_symbols(out, "tuist-player", ["PlayerAPI"])
    assert_interface_index_symbols(out, "python-service", ["catalog_items"])
    assert_interface_index_symbols(out, "single-tool", ["render_report"])


def test_collect_batch_snapshots_keeps_parent_analysis_for_manifest_file_target(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (checkout / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (checkout / "demo.py").write_text("def public_api():\n    return None\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: manifest-file
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    target: pyproject.toml
    packageId: demo.python
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_interface_indexes=True)
    )

    interface_index = result["collected"][0]["interfaceIndex"]
    index = json.loads((out / "manifest-file" / "public-interface-index.json").read_text())
    assert interface_index["status"] == "complete"
    assert interface_index["diagnostics"] == []
    assert index["packages"][0]["entrypoints"][0]["path"] == "demo.py"
    assert index["packages"][0]["entrypoints"][0]["symbols"][0]["name"] == "public_api"


def test_collect_batch_snapshots_emits_python_interface_index_when_requested(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    cache = tmp_path / "cache"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (checkout / "demo.py").write_text("def public_api():\n    return None\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    packageId: demo.python
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=out,
            emit_interface_indexes=True,
            analyzer_cache_dir=cache,
        )
    )

    index_path = out / "demo" / "public-interface-index.json"
    assert index_path.is_file()
    interface_index = result["collected"][0]["interfaceIndex"]
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert interface_index["status"] == "complete"
    assert interface_index["output"] == str(index_path)
    assert interface_index["executedAnalyzerIds"] == ["spec_harvester.python_public_api"]
    assert interface_index["summary"]["symbolCount"] == 1
    assert index["packages"][0]["id"] == "demo.python"
    assert index["analyzers"][0]["execution"] == "none"
    assert any(cache.joinpath("demo").glob("*.json"))


def test_collect_batch_snapshots_applies_opt_in_parser_profile(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "fastapi", "# FastAPI\n")
    (checkout / "pyproject.toml").write_text("[project]\nname = 'fastapi'\n", encoding="utf-8")
    (checkout / "fastapi").mkdir()
    (checkout / "docs_src").mkdir()
    (checkout / "fastapi" / "applications.py").write_text(
        "class FastAPI:\n    pass\n",
        encoding="utf-8",
    )
    (checkout / "docs_src" / "tutorial.py").write_text(
        "def tutorial_app():\n    pass\n",
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: fastapi
    repository: https://github.com/fastapi/fastapi
    revision: abc
    checkout: {relative_to(checkout, inputs)}
    packageId: fastapi.core
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=out,
            emit_interface_indexes=True,
            parser_profile_id="python.web_framework.v0",
        )
    )

    interface_index = result["collected"][0]["interfaceIndex"]
    assert interface_index["parserProfileId"] == "python.web_framework.v0"
    index = json.loads((out / "fastapi" / "public-interface-index.json").read_text())
    package = index["packages"][0]
    assert [entrypoint["path"] for entrypoint in package["entrypoints"]] == [
        "fastapi/applications.py"
    ]
    decisions = {decision["path"]: decision for decision in package["pathClassification"]}
    assert decisions["docs_src/tutorial.py"]["publicInterfaceEligible"] is False
    assert decisions["fastapi/applications.py"]["publicInterfaceEligible"] is True


def test_collect_batch_snapshots_emits_deterministic_workspace_inventory(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    repeat_out = tmp_path / "repeat-candidates"
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

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_workspace_inventory=True)
    )
    repeated = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=repeat_out, emit_workspace_inventory=True)
    )

    inventory_path = out / "xyflow" / "workspace-inventory.json"
    repeat_inventory_path = repeat_out / "xyflow" / "workspace-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    assert result["collected"][0]["workspaceInventory"]["output"] == str(inventory_path)
    assert result["collected"][0]["workspaceInventory"]["summary"]["packageCount"] == 8
    assert repeated["collected"][0]["workspaceInventory"]["summary"]["packageCount"] == 8
    assert inventory_path.read_text(encoding="utf-8") == repeat_inventory_path.read_text(
        encoding="utf-8"
    )
    assert inventory["apiVersion"] == "spec-harvester.workspace-inventory/v0"
    assert inventory["kind"] == "SpecHarvesterWorkspaceInventory"
    assert inventory["schemaVersion"] == 1
    assert inventory["source"]["repository"] == "https://github.com/xyflow/xyflow"
    assert inventory["source"]["exactRevision"] == "abc123"
    assert inventory["source"]["revisionAuthority"] == "source_manifest_revision"
    assert inventory["source"]["packageId"] == "xyflow.workspace"
    assert inventory["privacy"]["rawSourceIncluded"] is False
    assert inventory["privacy"]["packageScriptsExecuted"] is False

    workspace_by_path = {item["path"]: item for item in inventory["workspaceManifests"]}
    assert workspace_by_path["pnpm-workspace.yaml"]["includePatterns"] == [
        "examples/*",
        "packages/*",
        "tests/*",
        "tooling/*",
    ]
    assert workspace_by_path["pnpm-workspace.yaml"]["excludePatterns"] == ["**/test-fixtures/**"]

    packages = {item["manifestPath"]: item for item in inventory["packages"]}
    assert packages["package.json"]["role"] == "workspace"
    assert packages["package.json"]["proposedSpecpmPackageId"] == "xyflow.workspace"
    assert packages["packages/system/package.json"]["role"] == "core_runtime"
    assert packages["packages/system/package.json"]["proposedSpecpmPackageId"] == "xyflow.system"
    assert packages["packages/react/package.json"]["name"] == "@xyflow/react"
    assert packages["packages/react/package.json"]["version"] == "12.0.0"
    assert packages["packages/react/package.json"]["description"] == (
        "React Flow - A highly customizable React library for building node-based "
        "editors and interactive flow charts."
    )
    assert packages["packages/react/package.json"]["license"] == "MIT"
    assert packages["packages/react/package.json"]["role"] == "react_binding"
    assert packages["packages/react/package.json"]["sourceTargetPath"] == "packages/react"
    assert packages["packages/react/package.json"]["proposedSpecpmPackageId"] == "xyflow.react"
    assert packages["packages/svelte/package.json"]["role"] == "svelte_binding"
    assert packages["examples/react/package.json"]["role"] == "example_package"
    assert packages["examples/react/package.json"]["sourceTargetPath"] == "examples/react"
    assert packages["examples/react/package.json"]["proposedSpecpmPackageId"] == (
        "xyflow.react_examples"
    )
    assert packages["examples/svelte/package.json"]["role"] == "example_package"
    assert packages["tooling/cli/package.json"]["role"] == "tooling_package"
    assert packages["tooling/cli/package.json"]["proposedSpecpmPackageId"] == "xyflow.cli"
    assert packages["tests/e2e/package.json"]["role"] == "test_package"
    assert "pnpm-lock.yaml" not in packages
    for record in packages.values():
        evidence = record["evidenceReferences"][0]
        assert evidence["kind"] == "package_manifest"
        assert evidence["size"] > 0
        assert evidence["size"] == (checkout / record["manifestPath"]).stat().st_size
        assert evidence["digest"]["algorithm"] == "sha256"
        assert len(evidence["digest"]["value"]) == 64


def test_workspace_inventory_honors_workspace_exclude_patterns(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "workspace", "# Workspace\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "workspace", "version": "0.0.0"}),
        encoding="utf-8",
    )
    (checkout / "pnpm-workspace.yaml").write_text(
        """
packages:
  - packages/*
  - "!packages/private"
""",
        encoding="utf-8",
    )
    public_package = checkout / "packages" / "public"
    private_package = checkout / "packages" / "private"
    public_package.mkdir(parents=True)
    private_package.mkdir(parents=True)
    (public_package / "package.json").write_text(
        json.dumps({"name": "@example/public", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (private_package / "package.json").write_text(
        json.dumps({"name": "@example/private", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: workspace
    repository: https://github.com/example/workspace
    revision: abc123
    checkout: {relative_to(checkout, inputs)}
    packageId: workspace.workspace
""",
        encoding="utf-8",
    )

    collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_workspace_inventory=True)
    )

    inventory = json.loads(
        (out / "workspace" / "workspace-inventory.json").read_text(encoding="utf-8")
    )
    package_paths = {item["manifestPath"] for item in inventory["packages"]}
    assert "packages/public/package.json" in package_paths
    assert "packages/private/package.json" not in package_paths
    workspace_by_path = {item["path"]: item for item in inventory["workspaceManifests"]}
    assert workspace_by_path["pnpm-workspace.yaml"]["excludePatterns"] == ["packages/private"]


def test_workspace_inventory_resolves_patterns_from_manifest_directory(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "monorepo", "# Monorepo\n")
    root_package = checkout / "packages" / "root"
    nested_package = checkout / "apps" / "web" / "packages" / "ui"
    root_package.mkdir(parents=True)
    nested_package.mkdir(parents=True)
    (checkout / "apps" / "web").mkdir(parents=True, exist_ok=True)
    (checkout / "apps" / "web" / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/web",
                "version": "1.0.0",
                "workspaces": ["packages/*"],
            }
        ),
        encoding="utf-8",
    )
    (root_package / "package.json").write_text(
        json.dumps({"name": "@example/root", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (nested_package / "package.json").write_text(
        json.dumps({"name": "@example/ui", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: web
    repository: https://github.com/example/monorepo
    revision: abc123
    checkout: {relative_to(checkout, inputs)}
    target: apps/web
    packageId: web.workspace
""",
        encoding="utf-8",
    )

    collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_workspace_inventory=True)
    )

    inventory = json.loads((out / "web" / "workspace-inventory.json").read_text(encoding="utf-8"))
    package_paths = {item["manifestPath"] for item in inventory["packages"]}
    assert "apps/web/package.json" in package_paths
    assert "apps/web/packages/ui/package.json" in package_paths
    assert "packages/root/package.json" not in package_paths
    workspace_by_path = {item["path"]: item for item in inventory["workspaceManifests"]}
    assert workspace_by_path["apps/web/package.json"]["includePatterns"] == ["packages/*"]


def test_collect_batch_workspace_inventory_resolves_ref_to_git_head(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "demo", "version": "1.0.0", "workspaces": ["packages/*"]}),
        encoding="utf-8",
    )
    subprocess.run(["git", "init"], cwd=checkout, check=True, capture_output=True)
    subprocess.run(["git", "add", "README.md", "package.json"], cwd=checkout, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=SpecHarvester",
            "-c",
            "user.email=spec@example.invalid",
            "commit",
            "-m",
            "fixture",
        ],
        cwd=checkout,
        check=True,
        capture_output=True,
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    ref: main
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_workspace_inventory=True)
    )

    inventory = json.loads((out / "demo" / "workspace-inventory.json").read_text())
    assert inventory["source"]["exactRevision"] == head
    assert inventory["source"]["declaredRef"] == "main"
    assert inventory["source"]["revisionAuthority"] == "git_head"


def test_collect_batch_workspace_inventory_skips_large_workspace_package_manifest(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "pnpm-workspace.yaml").write_text(
        "packages:\n  - packages/*\n",
        encoding="utf-8",
    )
    huge_package = checkout / "packages" / "huge"
    huge_package.mkdir(parents=True)
    (huge_package / "package.json").write_text(
        json.dumps({"name": "@example/huge", "description": "x" * 512}),
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=out,
            max_file_bytes=128,
            emit_workspace_inventory=True,
        )
    )

    inventory = json.loads((out / "demo" / "workspace-inventory.json").read_text())
    assert [item["manifestPath"] for item in inventory["packages"]] == []
    assert inventory["diagnostics"] == [
        {
            "code": "package_manifest_too_large",
            "level": "warning",
            "message": (
                "Workspace package manifest was too large to record as inventory evidence."
            ),
            "path": "packages/huge/package.json",
        }
    ]


def test_collect_batch_snapshots_records_interface_index_skips(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription
        let package = Package(name: "Demo")
        """,
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_interface_indexes=True)
    )

    interface_index = result["collected"][0]["interfaceIndex"]
    assert interface_index["status"] == "skipped"
    assert "output" not in interface_index
    assert interface_index["executedAnalyzerIds"] == []
    assert interface_index["skippedAnalyzerPlans"][0]["id"] == "spec_harvester.swift_public_api"
    assert not (out / "demo" / "public-interface-index.json").exists()


def test_collect_batch_snapshots_emits_swift_interface_index_when_requested(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    source = checkout / "Sources" / "Demo"
    source.mkdir(parents=True)
    (checkout / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription
        let package = Package(name: "Demo")
        """,
        encoding="utf-8",
    )
    (source / "API.swift").write_text("public struct API {}\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, emit_interface_indexes=True)
    )

    index_path = out / "demo" / "public-interface-index.json"
    interface_index = result["collected"][0]["interfaceIndex"]
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert interface_index["status"] == "complete"
    assert interface_index["output"] == str(index_path)
    assert interface_index["executedAnalyzerIds"] == ["spec_harvester.swift_public_api"]
    assert interface_index["summary"]["symbolCount"] == 1
    assert index["packages"][0]["language"] == "swift"
    assert index["packages"][0]["entrypoints"][0]["symbols"][0]["name"] == "API"


def test_collect_batch_snapshots_rejects_unknown_selected_ids(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unknown selected repository id"):
        collect_batch_snapshots(
            BatchCollectOptions(inputs=inputs, out=out, selected_ids=("missing",))
        )


def test_collect_batch_snapshots_rejects_duplicate_selected_ids(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate selected repository id"):
        collect_batch_snapshots(
            BatchCollectOptions(inputs=inputs, out=out, selected_ids=("demo", "demo"))
        )


def test_collect_batch_snapshots_requires_checkout_field(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="requires checkout"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))


def test_collect_batch_snapshots_rejects_missing_checkout_directory(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: ../missing
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="checkout does not exist"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))


def test_collect_batch_snapshots_does_not_write_partial_outputs_on_validation_failure(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: valid
    repository: https://github.com/example/valid
    revision: abc
    checkout: {relative_to(checkout, inputs)}
  - id: missing
    repository: https://github.com/example/missing
    revision: def
    checkout: ../missing
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="checkout does not exist"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert not (out / "valid").exists()


def test_collect_batch_snapshots_rejects_unsafe_candidate_directory_ids(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: ../escape
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unsafe repository id"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))


def test_collect_batch_snapshots_rejects_staged_checkout_changes_in_strict_mode(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=checkout, check=True, capture_output=True)
    subprocess.run(["git", "add", "README.md"], cwd=checkout, check=True, capture_output=True)
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="staged changes"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert not out.exists()


def test_collect_batch_snapshots_ignores_staged_changes_outside_subdirectory_checkout(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    worktree = tmp_path / "worktree"
    checkout = make_checkout(worktree / "packages" / "demo", "# Demo\n")
    inputs.mkdir()
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (worktree / "outside.txt").write_text("staged but unrelated\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=worktree, check=True, capture_output=True)
    subprocess.run(["git", "add", "outside.txt"], cwd=worktree, check=True, capture_output=True)
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert result["status"] == "ok"
    assert (out / "demo" / "harvest.json").is_file()


def test_collect_batch_snapshots_rejects_staged_changes_inside_subdirectory_checkout(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    worktree = tmp_path / "worktree"
    checkout = make_checkout(worktree / "packages" / "demo", "# Demo\n")
    inputs.mkdir()
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=worktree, check=True, capture_output=True)
    subprocess.run(
        ["git", "add", "packages/demo/README.md"],
        cwd=worktree,
        check=True,
        capture_output=True,
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="packages/demo/README.md"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert not out.exists()


def test_collect_batch_snapshots_allows_staged_checkout_changes_in_relaxed_private_mode(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    subprocess.run(["git", "init"], cwd=checkout, check=True, capture_output=True)
    subprocess.run(["git", "add", "README.md"], cwd=checkout, check=True, capture_output=True)
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, strict_public=False)
    )

    assert result["status"] == "ok"
    assert (out / "demo" / "harvest.json").is_file()


def test_cli_collect_batch_prints_summary_and_writes_harvest_json(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(["collect-batch", str(inputs), "--out", str(out), "--select", "demo"])

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["status"] == "ok"
    assert summary["collectedCount"] == 1
    assert summary["collected"][0]["id"] == "demo"
    assert (out / "demo" / "harvest.json").is_file()


def test_cli_collect_batch_writes_validation_report(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    report_path = out / "batch-validation.json"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--report",
            str(report_path),
        ]
    )

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert summary["validationReport"] == str(report_path)
    assert report["summary"]["collectedCount"] == 1
    assert report["summary"]["highConfidenceCount"] == 1
    assert report["summary"]["errorCount"] == 0
    assert report["records"][0]["id"] == "demo"


def test_cli_collect_batch_emits_js_ts_interface_index_when_requested(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/demo",
                "version": "1.0.0",
                "exports": {".": "./src/index.ts"},
            }
        ),
        encoding="utf-8",
    )
    src = checkout / "src"
    src.mkdir()
    (src / "index.ts").write_text("export const answer = 42\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--emit-interface-indexes",
        ]
    )

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    index_path = out / "demo" / "public-interface-index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert summary["collected"][0]["interfaceIndex"]["output"] == str(index_path)
    assert summary["collected"][0]["interfaceIndex"]["status"] == "complete"
    assert index["packages"][0]["id"] == "@example/demo"
    assert index["summary"]["symbolCount"] == 1


def test_cli_collect_batch_emits_workspace_inventory_when_requested(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
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

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--emit-workspace-inventory",
        ]
    )

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    inventory_path = out / "xyflow" / "workspace-inventory.json"
    assert summary["collected"][0]["workspaceInventory"]["output"] == str(inventory_path)
    assert summary["collected"][0]["workspaceInventory"]["kind"] == (
        "SpecHarvesterWorkspaceInventory"
    )
    assert inventory_path.is_file()


def test_cli_collect_batch_returns_error_for_missing_license_in_strict_report(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    report_path = out / "batch-validation.json"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--report",
            str(report_path),
        ]
    )

    assert result == 1
    summary = json.loads(capsys.readouterr().out)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert summary["status"] == "error"
    assert report["status"] == "error"
    assert report["records"][0]["errors"][0]["code"] == "missing_license_file"


def test_cli_collect_batch_accepts_license_txt_in_strict_report(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    report_path = out / "batch-validation.json"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (checkout / "LICENSE.txt").write_text(
        "MIT License\n\nPermission is hereby granted, copyright demo.\n",
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--report",
            str(report_path),
        ]
    )

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    harvest = json.loads((out / "demo" / "harvest.json").read_text(encoding="utf-8"))
    license_record = next(item for item in harvest["files"] if item["path"] == "LICENSE.txt")
    assert summary["status"] == "ok"
    assert report["status"] == "ok"
    assert report["summary"]["highConfidenceCount"] == 1
    assert report["records"][0]["evidence"]["licenseFileCount"] == 1
    assert report["records"][0]["errors"] == []
    assert license_record["kind"] == "license"
    assert license_record["licenseHint"] == "MIT"


def test_cli_collect_batch_treats_nested_swift_manifest_as_package_evidence(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    report_path = out / "batch-validation.json"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    package_dir = checkout / "Packages"
    package_dir.mkdir()
    (package_dir / "Package.swift").write_text(
        "// swift-tools-version: 6.0\nimport PackageDescription\n",
        encoding="utf-8",
    )
    (checkout / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: swift-demo
    repository: https://github.com/example/swift-demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--report",
            str(report_path),
        ]
    )

    assert result == 0
    capsys.readouterr()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["summary"]["highConfidenceCount"] == 1
    record = report["records"][0]
    assert record["evidence"]["packageManifestCount"] == 1
    assert record["warnings"] == []
    assert record["errors"] == []


def make_checkout(path: Path, readme: str) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text(readme, encoding="utf-8")
    return path


def make_scoped_source_matrix_checkout(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text("# Mobile Monorepo\n", encoding="utf-8")
    (path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    player = path / "Apps" / "Player"
    player_source = player / "Sources"
    player_source.mkdir(parents=True)
    (player / "Project.swift").write_text(
        """
        import ProjectDescription

        let project = Project(
            name: "Player",
            targets: [
                .target(
                    name: "PlayerKit",
                    product: .framework,
                    sources: .sources(
                        ["Sources/**"],
                        excluding: ["Sources/Generated/**"]
                    )
                )
            ]
        )
        """,
        encoding="utf-8",
    )
    (player_source / "PlayerAPI.swift").write_text(
        "public struct PlayerAPI {}\n",
        encoding="utf-8",
    )
    other_swift = path / "Apps" / "Other"
    other_swift.mkdir(parents=True)
    (other_swift / "Other.swift").write_text(
        "public struct OtherAPI {}\n",
        encoding="utf-8",
    )
    service = path / "services" / "catalog"
    service.mkdir(parents=True)
    (service / "api.py").write_text(
        "def catalog_items():\n    return []\n",
        encoding="utf-8",
    )
    other_service = path / "services" / "other"
    other_service.mkdir(parents=True)
    (other_service / "api.py").write_text(
        "def other_items():\n    return []\n",
        encoding="utf-8",
    )
    tools = path / "tools"
    tools.mkdir()
    (tools / "report.py").write_text(
        "def render_report():\n    return 'ok'\n",
        encoding="utf-8",
    )
    (tools / "ignored.py").write_text(
        "def ignored_tool():\n    return None\n",
        encoding="utf-8",
    )
    return path


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


def snapshot_paths(snapshot: dict[str, object]) -> list[str]:
    files = snapshot["files"]
    assert isinstance(files, list)
    return [item["path"] for item in files if isinstance(item, dict)]


def assert_interface_index_symbols(out: Path, candidate_id: str, expected: list[str]) -> None:
    index = json.loads(
        (out / candidate_id / "public-interface-index.json").read_text(encoding="utf-8")
    )
    symbols = [
        symbol["name"]
        for package in index["packages"]
        for entrypoint in package["entrypoints"]
        for symbol in entrypoint["symbols"]
    ]
    assert symbols == expected


def relative_to(path: Path, root: Path) -> str:
    return Path(os.path.relpath(path, root)).as_posix()
