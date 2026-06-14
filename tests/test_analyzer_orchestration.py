from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.analyzer_orchestration import (
    ANALYZER_ADAPTERS,
    GO_PROJECT_PROFILE_ANALYZER_ID,
    PYTHON_PROJECT_PROFILE_ANALYZER_ID,
    SWIFT_PROJECT_PROFILE_ANALYZER_ID,
    AnalyzerAdapter,
    run_project_profile_analyzers,
)
from spec_harvester.collector import HarvestOptions, collect_local_repository


def test_run_project_profile_analyzers_emits_python_public_interface_index(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "python-demo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (repo / "demo.py").write_text(
        "def create_item(name: str) -> str:\n    return name\n",
        encoding="utf-8",
    )
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(
        source=repo,
        snapshot=snapshot,
        package_id="demo.python",
    )

    index = result["index"]
    assert result["status"] == "complete"
    assert result["plannedAnalyzerIds"] == ["spec_harvester.python_public_api"]
    assert result["executedAnalyzerIds"] == ["spec_harvester.python_public_api"]
    assert result["skippedAnalyzerPlans"] == []
    assert index["sourceRevision"] == "abc123"
    assert index["analyzers"][0]["id"] == "python-ast-public-api"
    assert index["analyzers"][0]["execution"] == "none"
    assert index["analyzers"][0]["networkAccess"] == "none"
    assert index["analyzers"][0]["packageScripts"] == "not_run"
    assert index["packages"][0]["id"] == "demo.python"
    assert index["packages"][0]["language"] == "python"
    assert index["summary"]["symbolCount"] == 1


def test_run_project_profile_analyzers_applies_parser_profile_to_python_only(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "fastapi-style"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'fastapi'\n", encoding="utf-8")
    fastapi = repo / "fastapi"
    docs_src = repo / "docs_src"
    fastapi.mkdir()
    docs_src.mkdir()
    (fastapi / "applications.py").write_text("class FastAPI:\n    pass\n", encoding="utf-8")
    (docs_src / "tutorial.py").write_text("def tutorial_app():\n    pass\n", encoding="utf-8")
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(
        source=repo,
        snapshot=snapshot,
        package_id="fastapi.core",
        parser_profile_id="python.web_framework.v0",
    )

    index = result["index"]
    assert result["status"] == "complete"
    assert result["parserProfileId"] == "python.web_framework.v0"
    assert [entrypoint["path"] for entrypoint in index["packages"][0]["entrypoints"]] == [
        "fastapi/applications.py"
    ]
    decisions = {
        decision["path"]: decision for decision in index["packages"][0]["pathClassification"]
    }
    assert decisions["docs_src/tutorial.py"]["publicInterfaceEligible"] is False
    assert decisions["docs_src/tutorial.py"]["semanticUsageEligible"] is True


def test_run_project_profile_analyzers_emits_js_ts_public_interface_index(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "js-demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/demo",
                "version": "1.0.0",
                "exports": {".": "./src/index.ts"},
            }
        ),
        encoding="utf-8",
    )
    src = repo / "src"
    src.mkdir()
    (src / "index.ts").write_text(
        "export function createGraph(options) { return options }\n",
        encoding="utf-8",
    )
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    index = result["index"]
    assert result["status"] == "complete"
    assert result["plannedAnalyzerIds"] == ["spec_harvester.js_ts_public_api"]
    assert index["analyzers"][0]["id"] == "js-ts-manifest-export-analyzer"
    assert index["packages"][0]["id"] == "@example/demo"
    assert index["packages"][0]["language"] == "javascript-typescript"
    assert index["packages"][0]["entrypoints"][0]["path"] == "src/index.ts"
    assert index["summary"]["symbolCount"] == 1


def test_run_project_profile_analyzers_emits_go_public_interface_index(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "go-demo"
    repo.mkdir()
    (repo / "go.mod").write_text("module example.com/demo\n\ngo 1.24\n", encoding="utf-8")
    (repo / "api.go").write_text(
        "package demo\n\ntype Engine struct {}\nfunc New() *Engine { return &Engine{} }\n",
        encoding="utf-8",
    )
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    index = result["index"]
    assert result["status"] == "complete"
    assert result["plannedAnalyzerIds"] == [GO_PROJECT_PROFILE_ANALYZER_ID]
    assert result["executedAnalyzerIds"] == [GO_PROJECT_PROFILE_ANALYZER_ID]
    assert result["skippedAnalyzerPlans"] == []
    assert index["sourceRevision"] == "abc123"
    assert index["analyzers"][0]["id"] == "go-source-public-api"
    assert index["packages"][0]["id"] == "example.com/demo"
    assert index["packages"][0]["language"] == "go"
    assert index["packages"][0]["entrypoints"][0]["path"] == "api.go"
    assert index["summary"]["symbolCount"] == 2


def test_run_project_profile_analyzers_uses_package_id_fallback_for_nested_go_module(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "monorepo"
    repo.mkdir()
    package = repo / "packages" / "service"
    package.mkdir(parents=True)
    (package / "go.mod").write_text("module example.com/service\n", encoding="utf-8")
    (package / "api.go").write_text("package service\n\nfunc Visible() {}\n", encoding="utf-8")
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(
        source=repo,
        snapshot=snapshot,
        package_id="fallback.go",
    )

    index = result["index"]
    assert result["status"] == "complete"
    assert result["plannedAnalyzerIds"] == [GO_PROJECT_PROFILE_ANALYZER_ID]
    assert index["packages"][0]["id"] == "fallback.go/packages/service"
    assert index["summary"]["symbolCount"] == 1


def test_run_project_profile_analyzers_merges_multiple_recommended_indexes(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "polyglot"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/polyglot",
                "version": "1.0.0",
                "exports": {".": "./src/index.ts"},
            }
        ),
        encoding="utf-8",
    )
    (repo / "api.py").write_text("class Service:\n    pass\n", encoding="utf-8")
    src = repo / "src"
    src.mkdir()
    (src / "index.ts").write_text("export class Widget {}\n", encoding="utf-8")
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(
        source=repo,
        snapshot=snapshot,
        package_id="demo.polyglot",
    )

    index = result["index"]
    assert result["status"] == "complete"
    assert result["executedAnalyzerIds"] == [
        "spec_harvester.js_ts_public_api",
        "spec_harvester.python_public_api",
    ]
    assert [analyzer["id"] for analyzer in index["analyzers"]] == [
        "js-ts-manifest-export-analyzer",
        "python-ast-public-api",
    ]
    assert {package["language"] for package in index["packages"]} == {
        "javascript-typescript",
        "python",
    }
    assert index["summary"]["packageCount"] == 2
    assert index["summary"]["symbolCount"] == 2


def test_run_project_profile_analyzers_marks_partial_when_one_analyzer_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "polyglot"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/polyglot",
                "version": "1.0.0",
                "exports": {".": "./src/index.ts"},
            }
        ),
        encoding="utf-8",
    )
    (repo / "api.py").write_text("class Service:\n    pass\n", encoding="utf-8")
    src = repo / "src"
    src.mkdir()
    (src / "index.ts").write_text("export class Widget {}\n", encoding="utf-8")
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    def fail_python_analyzer(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise ValueError("synthetic analyzer failure")

    adapters = dict(ANALYZER_ADAPTERS)
    adapters[PYTHON_PROJECT_PROFILE_ANALYZER_ID] = AnalyzerAdapter(
        plan_id=PYTHON_PROJECT_PROFILE_ANALYZER_ID,
        analyze=fail_python_analyzer,
    )
    monkeypatch.setattr("spec_harvester.analyzer_orchestration.ANALYZER_ADAPTERS", adapters)

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    assert result["status"] == "partial"
    assert result["index"]["summary"]["status"] == "complete"
    assert result["executedAnalyzerIds"] == ["spec_harvester.js_ts_public_api"]
    assert result["diagnostics"] == [
        {
            "level": "error",
            "message": (
                "Analyzer spec_harvester.python_public_api failed: synthetic analyzer failure"
            ),
        }
    ]


def test_run_project_profile_analyzers_skips_manifest_only_plans(tmp_path: Path) -> None:
    repo = tmp_path / "swift-demo"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription
        let package = Package(name: "SwiftDemo")
        """,
        encoding="utf-8",
    )
    snapshot = collect_local_repository(HarvestOptions(source=repo))

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    assert result["status"] == "skipped"
    assert result["index"] is None
    assert result["plannedAnalyzerIds"] == [SWIFT_PROJECT_PROFILE_ANALYZER_ID]
    assert result["executedAnalyzerIds"] == []
    assert result["skippedAnalyzerPlans"] == [
        {
            "id": SWIFT_PROJECT_PROFILE_ANALYZER_ID,
            "status": "manifest_only",
            "reason": "project_profile_plan_not_recommended",
        }
    ]


def test_run_project_profile_analyzers_emits_swift_public_interface_index(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "swift-demo"
    source = repo / "Sources" / "SwiftDemo"
    source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription
        let package = Package(name: "SwiftDemo")
        """,
        encoding="utf-8",
    )
    (source / "API.swift").write_text(
        "public struct Engine {}\npublic func makeEngine() -> Engine { Engine() }\n",
        encoding="utf-8",
    )
    snapshot = collect_local_repository(HarvestOptions(source=repo, revision="abc123"))

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    index = result["index"]
    assert result["status"] == "complete"
    assert result["plannedAnalyzerIds"] == [SWIFT_PROJECT_PROFILE_ANALYZER_ID]
    assert result["executedAnalyzerIds"] == [SWIFT_PROJECT_PROFILE_ANALYZER_ID]
    assert result["skippedAnalyzerPlans"] == []
    assert index["sourceRevision"] == "abc123"
    assert index["analyzers"][0]["id"] == "swift-source-public-api"
    assert index["packages"][0]["id"] == "SwiftDemo"
    assert index["packages"][0]["language"] == "swift"
    assert index["packages"][0]["entrypoints"][0]["path"] == "Sources/SwiftDemo/API.swift"
    assert index["summary"]["symbolCount"] == 2


def test_run_project_profile_analyzers_skips_go_manifest_without_sources(tmp_path: Path) -> None:
    repo = tmp_path / "go-demo"
    repo.mkdir()
    (repo / "go.mod").write_text("module example.com/demo\n", encoding="utf-8")
    snapshot = collect_local_repository(HarvestOptions(source=repo))

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    assert result["status"] == "skipped"
    assert result["index"] is None
    assert result["plannedAnalyzerIds"] == [GO_PROJECT_PROFILE_ANALYZER_ID]
    assert result["executedAnalyzerIds"] == []
    assert result["skippedAnalyzerPlans"] == [
        {
            "id": GO_PROJECT_PROFILE_ANALYZER_ID,
            "status": "manifest_only",
            "reason": "project_profile_plan_not_recommended",
        }
    ]


def test_run_project_profile_analyzers_skips_unknown_recommended_plans(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    snapshot = {
        "source": {"revision": "abc123"},
        "projectProfile": {
            "analyzerPlan": [
                {
                    "id": "spec_harvester.future_public_api",
                    "status": "recommended",
                }
            ]
        },
    }

    result = run_project_profile_analyzers(source=repo, snapshot=snapshot)

    assert result["status"] == "skipped"
    assert result["index"] is None
    assert result["executedAnalyzerIds"] == []
    assert result["skippedAnalyzerPlans"] == [
        {
            "id": "spec_harvester.future_public_api",
            "status": "recommended",
            "reason": "unsupported_project_profile_analyzer",
        }
    ]
