from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.drafter import DraftOptions, draft_spec_package


@dataclass(frozen=True)
class SmokeMatrixCase:
    repository_id: str
    package_id: str
    files: dict[str, str]
    expected_languages: set[str]
    expected_ecosystems: set[str]
    expected_analyzer_plan_ids: set[str]
    expected_analyzer_plan_statuses: dict[str, str]
    expected_manifest_paths: set[str]
    expected_diagnostics: set[str] = frozenset()


def test_multi_language_smoke_matrix_collects_expected_project_profiles(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    checkouts = tmp_path / "checkouts"
    candidates = tmp_path / "candidates"
    report_path = tmp_path / "batch-validation.json"
    inputs.mkdir()
    checkouts.mkdir()
    cases = smoke_matrix_cases()

    for case in cases:
        write_smoke_fixture(checkouts / case.repository_id, case.files)
    write_source_manifest(inputs / "repositories.yml", checkouts, cases)

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=candidates, report=report_path)
    )

    assert result["status"] == "ok"
    assert result["collectedCount"] == len(cases)
    assert result["skippedCount"] == 0

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "ok"
    assert report["summary"]["collectedCount"] == len(cases)
    assert report["summary"]["errorCount"] == 0
    assert report["summary"]["warningCount"] == 1
    assert report["summary"]["mediumConfidenceCount"] == 1

    for case in cases:
        snapshot = json.loads(
            (candidates / case.repository_id / "harvest.json").read_text(encoding="utf-8")
        )
        profile = snapshot["projectProfile"]
        assert {item["id"] for item in profile["languages"]} == case.expected_languages
        assert {item["id"] for item in profile["ecosystems"]} == case.expected_ecosystems
        assert {item["path"] for item in profile["manifests"]} == case.expected_manifest_paths
        assert {item["id"] for item in profile["analyzerPlan"]} == (case.expected_analyzer_plan_ids)
        assert {item["id"] for item in profile["diagnostics"]} == case.expected_diagnostics

        analyzer_statuses = {item["id"]: item["status"] for item in profile["analyzerPlan"]}
        assert analyzer_statuses == case.expected_analyzer_plan_statuses
        assert snapshot["policy"]["execution"] == "none"
        assert snapshot["policy"]["networkAccess"] == "none"
        assert snapshot["policy"]["packageScripts"] == "not_run"


def test_multi_language_smoke_matrix_drafts_documentation_first_fixture(
    tmp_path: Path,
) -> None:
    docs_case = next(case for case in smoke_matrix_cases() if case.repository_id == "docs-contract")
    repo = tmp_path / docs_case.repository_id
    write_smoke_fixture(repo, docs_case.files)
    candidates = tmp_path / "candidate"
    candidates.mkdir()
    snapshot_path = candidates / "harvest.json"

    inputs = tmp_path / "inputs"
    inputs.mkdir()
    write_source_manifest(inputs / "repositories.yml", tmp_path, [docs_case])
    collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=tmp_path / "batch"))

    snapshot = json.loads(
        (tmp_path / "batch" / docs_case.repository_id / "harvest.json").read_text(encoding="utf-8")
    )
    snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidates, out=candidates, package_id=docs_case.package_id)
    )

    readme = next(item for item in snapshot["files"] if item["path"] == "README.md")
    assert "api contract" in readme["semanticHints"]
    assert "openapi" in readme["semanticHints"]
    assert "schema" in readme["semanticHints"]
    assert "content" not in readme
    assert "body" not in readme

    manifest = (candidates / "specpm.yaml").read_text(encoding="utf-8")
    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "intent.api.contract_surface" in manifest
    assert "intent.metadata.schema_validation" in manifest
    assert "intent.workflow.automation_pipeline" in manifest
    assert "intent.package.public_repository_metadata" not in manifest
    assert "id: semantic_intent_static_evidence" in spec
    assert "README.md" in spec


def smoke_matrix_cases() -> list[SmokeMatrixCase]:
    return [
        SmokeMatrixCase(
            repository_id="npm-package",
            package_id="smoke.npm",
            files={
                "README.md": "# npm package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "package.json": json.dumps(
                    {
                        "name": "@smoke/npm-package",
                        "version": "1.0.0",
                        "description": "Synthetic npm package.",
                        "exports": {".": "./src/index.ts"},
                    }
                ),
            },
            expected_languages={"javascript"},
            expected_ecosystems={"npm"},
            expected_analyzer_plan_ids={"spec_harvester.js_ts_public_api"},
            expected_analyzer_plan_statuses={"spec_harvester.js_ts_public_api": "recommended"},
            expected_manifest_paths={"package.json"},
        ),
        SmokeMatrixCase(
            repository_id="spm-package",
            package_id="smoke.spm",
            files={
                "README.md": "# SPM package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "Package.swift": textwrap.dedent(
                    """
                    import PackageDescription
                    let package = Package(
                        name: "SmokeSPM",
                        products: [.library(name: "SmokeSPM", targets: ["SmokeSPM"])]
                    )
                    """
                ),
            },
            expected_languages={"swift"},
            expected_ecosystems={"swiftpm"},
            expected_analyzer_plan_ids={"spec_harvester.swift_manifest_public_interface"},
            expected_analyzer_plan_statuses={
                "spec_harvester.swift_manifest_public_interface": "manifest_only"
            },
            expected_manifest_paths={"Package.swift"},
        ),
        SmokeMatrixCase(
            repository_id="gradle-maven",
            package_id="smoke.jvm",
            files={
                "README.md": "# Gradle and Maven package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "pom.xml": "<project><modelVersion>4.0.0</modelVersion></project>\n",
                "build.gradle.kts": 'plugins { kotlin("jvm") version "2.0.0" }\n',
            },
            expected_languages={"java-kotlin"},
            expected_ecosystems={"gradle", "maven"},
            expected_analyzer_plan_ids={"spec_harvester.java_kotlin_manifest_profile"},
            expected_analyzer_plan_statuses={
                "spec_harvester.java_kotlin_manifest_profile": "manifest_only"
            },
            expected_manifest_paths={"build.gradle.kts", "pom.xml"},
        ),
        SmokeMatrixCase(
            repository_id="go-module",
            package_id="smoke.go",
            files={
                "README.md": "# Go module\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "go.mod": "module example.com/smoke\n\ngo 1.24\n",
            },
            expected_languages={"go"},
            expected_ecosystems={"go"},
            expected_analyzer_plan_ids={"spec_harvester.go_manifest_profile"},
            expected_analyzer_plan_statuses={"spec_harvester.go_manifest_profile": "manifest_only"},
            expected_manifest_paths={"go.mod"},
        ),
        SmokeMatrixCase(
            repository_id="composer-package",
            package_id="smoke.php",
            files={
                "README.md": "# Composer package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "composer.json": json.dumps({"name": "smoke/composer-package"}),
            },
            expected_languages={"php"},
            expected_ecosystems={"composer"},
            expected_analyzer_plan_ids={"spec_harvester.php_manifest_profile"},
            expected_analyzer_plan_statuses={
                "spec_harvester.php_manifest_profile": "manifest_only"
            },
            expected_manifest_paths={"composer.json"},
        ),
        SmokeMatrixCase(
            repository_id="cmake-package",
            package_id="smoke.cmake",
            files={
                "README.md": "# CMake package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "CMakeLists.txt": "cmake_minimum_required(VERSION 3.28)\nproject(smoke)\n",
            },
            expected_languages={"c-cpp"},
            expected_ecosystems={"cmake"},
            expected_analyzer_plan_ids={"spec_harvester.c_cpp_manifest_profile"},
            expected_analyzer_plan_statuses={
                "spec_harvester.c_cpp_manifest_profile": "manifest_only"
            },
            expected_manifest_paths={"CMakeLists.txt"},
        ),
        SmokeMatrixCase(
            repository_id="xcode-cocoapods",
            package_id="smoke.ios",
            files={
                "README.md": "# Xcode CocoaPods package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "Podfile": "platform :ios, '17.0'\ntarget 'Smoke' do\nend\n",
                "Smoke.xcodeproj/project.pbxproj": "// !$*UTF8*$!\n",
            },
            expected_languages={"objective-c"},
            expected_ecosystems={"cocoapods", "xcode"},
            expected_analyzer_plan_ids={"spec_harvester.objective_c_manifest_profile"},
            expected_analyzer_plan_statuses={
                "spec_harvester.objective_c_manifest_profile": "manifest_only"
            },
            expected_manifest_paths={"Podfile", "Smoke.xcodeproj/project.pbxproj"},
        ),
        SmokeMatrixCase(
            repository_id="rubygems-package",
            package_id="smoke.ruby",
            files={
                "README.md": "# RubyGems package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "Gemfile": "source 'https://rubygems.org'\n",
                "smoke.gemspec": "Gem::Specification.new do |s|\n  s.name = 'smoke'\nend\n",
            },
            expected_languages={"ruby"},
            expected_ecosystems={"bundler", "rubygems"},
            expected_analyzer_plan_ids={"spec_harvester.ruby_manifest_profile"},
            expected_analyzer_plan_statuses={
                "spec_harvester.ruby_manifest_profile": "manifest_only"
            },
            expected_manifest_paths={"Gemfile", "smoke.gemspec"},
        ),
        SmokeMatrixCase(
            repository_id="python-package",
            package_id="smoke.python",
            files={
                "README.md": "# Python package\n",
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
                "pyproject.toml": "[project]\nname = 'smoke-python'\n",
            },
            expected_languages={"python"},
            expected_ecosystems={"pypi"},
            expected_analyzer_plan_ids={"spec_harvester.python_public_api"},
            expected_analyzer_plan_statuses={"spec_harvester.python_public_api": "recommended"},
            expected_manifest_paths={"pyproject.toml"},
        ),
        SmokeMatrixCase(
            repository_id="docs-contract",
            package_id="smoke.docs_contract",
            files={
                "README.md": textwrap.dedent(
                    """
                    # Documentation Contract

                    ## API Contract

                    OpenAPI schema request and response validation for metadata manifests.

                    ## Workflow Automation

                    CLI commands validate schema configuration.
                    """
                ),
                "LICENSE": "MIT License\nCopyright 2026 Example\nPermission is hereby granted.\n",
            },
            expected_languages=set(),
            expected_ecosystems=set(),
            expected_analyzer_plan_ids=set(),
            expected_analyzer_plan_statuses={},
            expected_manifest_paths=set(),
            expected_diagnostics={"no_supported_package_manifest"},
        ),
    ]


def write_smoke_fixture(root: Path, files: dict[str, str]) -> None:
    root.mkdir(parents=True)
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def write_source_manifest(
    path: Path,
    checkouts_root: Path,
    cases: list[SmokeMatrixCase],
) -> None:
    lines = ["repositories:"]
    for index, case in enumerate(cases, start=1):
        checkout = checkouts_root / case.repository_id
        lines.extend(
            [
                f"  - id: {case.repository_id}",
                f"    repository: https://github.com/example/{case.repository_id}",
                f"    revision: {'a' * 39}{index % 10}",
                f"    checkout: {checkout}",
                f"    packageId: {case.package_id}",
                "    labels: [synthetic-smoke, multi-language]",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
