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


def relative_to(path: Path, root: Path) -> str:
    return Path(os.path.relpath(path, root)).as_posix()
