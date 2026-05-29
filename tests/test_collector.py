from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.collector import (
    HarvestOptions,
    classify_file,
    collect_local_repository,
    is_license_filename,
    markdown_headings,
    markdown_semantic_hints,
    nested_swift_package_manifests,
    parse_package_json,
    parse_swift_package_manifest,
)
from spec_harvester.drafter import (
    DraftOptions,
    draft_spec_package,
    public_interface_semantic_terms,
    render_scalar,
)
from spec_harvester.interface_index import (
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    render_public_interface_index_json,
)
from spec_harvester.promoter import (
    PrepareAcceptedManifestEntryOptions,
    PromoteOptions,
    append_local_manifest_entry,
    infer_manifest_entry_path,
    prepare_accepted_manifest_entry,
    promote_candidate,
    validate_with_specpm,
)


def public_symbol(name: str, kind: str, path: str) -> dict[str, object]:
    return {
        "name": name,
        "kind": kind,
        "visibility": "public",
        "evidence": evidence_record(path, "a" * 64),
    }


def rendered_evidence_item(spec: str, evidence_id: str) -> str:
    in_evidence = False
    current_block: list[str] = []
    evidence_blocks: list[list[str]] = []
    for line in spec.splitlines():
        if line == "evidence:":
            in_evidence = True
            continue
        if not in_evidence:
            continue
        if line and not line.startswith(" "):
            break
        if line.startswith("  - "):
            if current_block:
                evidence_blocks.append(current_block)
            current_block = [line]
        elif current_block:
            current_block.append(line)
    if current_block:
        evidence_blocks.append(current_block)

    expected_header = f"- id: {evidence_id}"
    for block in evidence_blocks:
        if block and block[0].strip() == expected_header:
            return "\n".join(block)
    raise AssertionError(f"Evidence item not found: {evidence_id}")


def test_collect_local_repository_extracts_safe_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n\n## Usage\n\ncontent\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/demo",
                "version": "1.2.3",
                "description": "Demo package",
                "license": "MIT",
                "scripts": {"build": "vite build", "test": "vitest"},
                "dependencies": {"react": "^19.0.0"},
                "peerDependencies": {"react-dom": "^19.0.0"},
                "exports": {".": "./dist/index.js"},
            }
        ),
        encoding="utf-8",
    )
    package_dir = repo / "packages" / "core"
    package_dir.mkdir(parents=True)
    (package_dir / "package.json").write_text(
        json.dumps({"name": "@example/core", "version": "0.1.0"}),
        encoding="utf-8",
    )

    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/demo",
            revision="abc123",
        )
    )

    assert snapshot["kind"] == "SpecHarvesterEvidenceSnapshot"
    assert snapshot["source"]["repository"] == "https://github.com/example/demo"
    assert snapshot["source"]["revision"] == "abc123"
    assert snapshot["source"]["label"] == "demo"
    assert "path" not in snapshot["source"]
    assert "generatedAt" not in snapshot
    assert snapshot["policy"]["execution"] == "none"
    assert snapshot["analyzerPolicy"] == {
        "schemaVersion": 1,
        "inputAuthority": "untrusted_repository_content",
        "outputAuthority": "untrusted_analyzer_metadata",
        "allowedExecutions": ["none"],
        "networkAccess": "none",
        "packageScripts": "not_run",
        "allowedConfidence": ["high", "medium", "low"],
        "requiresAnalyzerId": True,
        "requiresAnalyzerVersion": True,
        "requiresSourceRevision": True,
        "requiresSourceDigests": True,
    }
    assert snapshot["classifierPolicy"]["defaultMode"] == "disabled"
    assert snapshot["classifierPolicy"]["allowedExecutions"] == ["none"]
    assert snapshot["classifierPolicy"]["outputAuthority"] == "advisory_untrusted_metadata"
    assert snapshot["classifierPolicy"]["manifestEvidencePrecedence"] == "manifest_first"
    assert snapshot["summary"]["fileCount"] == 4
    assert snapshot["summary"]["packageManifestCount"] == 2
    assert snapshot["projectProfile"] == {
        "schemaVersion": 1,
        "languages": [
            {
                "id": "javascript",
                "confidence": "high",
                "reason": "package.json manifest parsed as npm package evidence.",
                "evidencePaths": ["package.json", "packages/core/package.json"],
            }
        ],
        "ecosystems": [
            {
                "id": "npm",
                "language": "javascript",
                "packageManager": "npm",
                "confidence": "high",
                "reason": "package.json manifest parsed as npm package evidence.",
                "evidencePaths": ["package.json", "packages/core/package.json"],
            }
        ],
        "manifests": [
            {
                "path": "package.json",
                "kind": "package_manifest",
                "language": "javascript",
                "ecosystem": "npm",
                "packageManager": "npm",
                "confidence": "high",
                "reason": "package.json manifest parsed as npm package evidence.",
                "sha256": next(
                    item["sha256"] for item in snapshot["files"] if item["path"] == "package.json"
                ),
                "parser": "spec_harvester.package_json",
            },
            {
                "path": "packages/core/package.json",
                "kind": "package_manifest",
                "language": "javascript",
                "ecosystem": "npm",
                "packageManager": "npm",
                "confidence": "high",
                "reason": "package.json manifest parsed as npm package evidence.",
                "sha256": next(
                    item["sha256"]
                    for item in snapshot["files"]
                    if item["path"] == "packages/core/package.json"
                ),
                "parser": "spec_harvester.package_json",
            },
        ],
        "analyzerPlan": [
            {
                "id": "spec_harvester.js_ts_public_api",
                "language": "javascript",
                "ecosystem": "npm",
                "status": "recommended",
                "reason": "package.json evidence can feed JavaScript/TypeScript export analysis.",
                "evidencePaths": ["package.json", "packages/core/package.json"],
            }
        ],
        "diagnostics": [],
    }

    by_path = {item["path"]: item for item in snapshot["files"]}
    assert by_path["README.md"]["headings"] == ["Demo", "Usage"]
    assert by_path["package.json"]["package"]["name"] == "@example/demo"
    assert by_path["package.json"]["package"]["scripts"] == ["build", "test"]
    assert by_path["package.json"]["package"]["dependencies"] == ["react"]
    assert by_path["package.json"]["package"]["peerDependencies"] == ["react-dom"]
    assert by_path["package.json"]["package"]["exports"] == ["."]


def test_collect_local_repository_snapshot_is_deterministic(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")

    options = HarvestOptions(
        source=repo,
        repository="https://github.com/example/demo",
        revision="abc123",
    )

    assert collect_local_repository(options) == collect_local_repository(options)


def test_collect_local_repository_discovers_nested_swift_package_manifest(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    nested = repo / "Packages"
    nested.mkdir()
    (nested / "Package.swift").write_text(
        "// swift-tools-version: 6.0\nimport PackageDescription\n",
        encoding="utf-8",
    )
    ignored = repo / ".build" / "checkouts" / "dependency"
    ignored.mkdir(parents=True)
    (ignored / "Package.swift").write_text(
        "// swift-tools-version: 6.0\n",
        encoding="utf-8",
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["summary"]["fileCount"] == 1
    assert snapshot["summary"]["packageManifestCount"] == 1
    assert snapshot["files"][0]["path"] == "Packages/Package.swift"
    assert snapshot["files"][0]["kind"] == "package_manifest"


def test_collect_local_repository_extracts_swift_package_products(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription

        let package = Package(
            name: "Puzzle",
            products: [
                .library(name: "PuzzleCore", targets: ["PuzzleCore"]),
                .library(name: "PuzzleUIKit", targets: ["PuzzleUIKit"]),
                .executable(name: "PuzzleTool", targets: ["PuzzleTool"]),
            ]
        )
        """,
        encoding="utf-8",
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    package = snapshot["files"][0]["package"]
    assert package["ecosystem"] == "swift"
    assert package["language"] == "swift"
    assert package["name"] == "Puzzle"
    assert package["products"] == [
        {"name": "PuzzleTool", "type": "executable"},
        {"name": "PuzzleCore", "type": "library"},
        {"name": "PuzzleUIKit", "type": "library"},
    ]
    assert snapshot["projectProfile"]["languages"] == [
        {
            "id": "swift",
            "confidence": "high",
            "reason": "Package.swift manifest parsed as SwiftPM evidence.",
            "evidencePaths": ["Package.swift"],
        }
    ]
    assert snapshot["projectProfile"]["ecosystems"] == [
        {
            "id": "swiftpm",
            "language": "swift",
            "packageManager": "swiftpm",
            "confidence": "high",
            "reason": "Package.swift manifest parsed as SwiftPM evidence.",
            "evidencePaths": ["Package.swift"],
        }
    ]
    assert snapshot["projectProfile"]["manifests"] == [
        {
            "path": "Package.swift",
            "kind": "package_manifest",
            "language": "swift",
            "ecosystem": "swiftpm",
            "packageManager": "swiftpm",
            "confidence": "high",
            "reason": "Package.swift manifest parsed as SwiftPM evidence.",
            "sha256": snapshot["files"][0]["sha256"],
            "parser": "spec_harvester.swift_package_manifest",
        }
    ]
    assert snapshot["projectProfile"]["analyzerPlan"] == [
        {
            "id": "spec_harvester.swift_public_api",
            "language": "swift",
            "ecosystem": "swiftpm",
            "status": "manifest_only",
            "reason": (
                "Package.swift evidence is available, but no Swift source files were found."
            ),
            "evidencePaths": ["Package.swift"],
        }
    ]
    assert snapshot["projectProfile"]["diagnostics"] == []


def test_collect_local_repository_recommends_swift_public_api_when_sources_exist(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    source = repo / "Sources" / "Demo"
    source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription
        let package = Package(name: "Demo")
        """,
        encoding="utf-8",
    )
    (source / "API.swift").write_text("public struct API {}\n", encoding="utf-8")

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["projectProfile"]["analyzerPlan"] == [
        {
            "id": "spec_harvester.swift_public_api",
            "language": "swift",
            "ecosystem": "swiftpm",
            "status": "recommended",
            "reason": (
                "Package.swift evidence can feed deterministic Swift source public API analysis."
            ),
            "evidencePaths": ["Package.swift"],
        }
    ]
    assert snapshot["projectProfile"]["diagnostics"] == []


def test_collect_local_repository_project_profile_reports_missing_manifest(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["projectProfile"] == {
        "schemaVersion": 1,
        "languages": [],
        "ecosystems": [],
        "manifests": [],
        "analyzerPlan": [],
        "diagnostics": [
            {
                "id": "no_supported_package_manifest",
                "level": "info",
                "message": "No supported package manifest evidence was found for ProjectProfile.",
            }
        ],
    }


def test_collect_local_repository_project_profile_treats_empty_package_json_as_npm(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text("{}", encoding="utf-8")

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["files"][0]["package"] == {}
    assert snapshot["projectProfile"]["languages"] == [
        {
            "id": "javascript",
            "confidence": "high",
            "reason": "package.json manifest parsed as npm package evidence.",
            "evidencePaths": ["package.json"],
        }
    ]
    assert snapshot["projectProfile"]["ecosystems"] == [
        {
            "id": "npm",
            "language": "javascript",
            "packageManager": "npm",
            "confidence": "high",
            "reason": "package.json manifest parsed as npm package evidence.",
            "evidencePaths": ["package.json"],
        }
    ]
    assert snapshot["projectProfile"]["analyzerPlan"] == [
        {
            "id": "spec_harvester.js_ts_public_api",
            "language": "javascript",
            "ecosystem": "npm",
            "status": "recommended",
            "reason": "package.json evidence can feed JavaScript/TypeScript export analysis.",
            "evidencePaths": ["package.json"],
        }
    ]
    assert snapshot["projectProfile"]["diagnostics"] == []


def test_collect_local_repository_project_profile_detects_manifest_first_ecosystems(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "polyglot"
    repo.mkdir()
    files = {
        "pnpm-lock.yaml": "lockfileVersion: '9.0'\n",
        "yarn.lock": "# yarn lockfile\n",
        "bun.lock": "",
        "pyproject.toml": "[project]\nname = 'demo'\n",
        "setup.cfg": "[metadata]\nname = demo\n",
        "requirements.txt": "requests\n",
        "pom.xml": "<project />\n",
        "build.gradle.kts": "plugins {}\n",
        "settings.gradle": "rootProject.name = 'demo'\n",
        "go.mod": "module example.com/demo\n",
        "composer.json": "{}\n",
        "CMakeLists.txt": "project(demo)\n",
        "meson.build": "project('demo', 'cpp')\n",
        "configure.ac": "AC_INIT([demo], [1.0])\n",
        "conanfile.txt": "[requires]\n",
        "vcpkg.json": "{}\n",
        "Makefile": "all:\n",
        "Podfile": "platform :ios, '17.0'\n",
        "Gemfile": "source 'https://rubygems.org'\n",
        "demo.gemspec": "Gem::Specification.new do |s|\nend\n",
        "Cargo.toml": "[package]\nname = 'demo'\n",
    }
    for relative, content in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    xcodeproj = repo / "Demo.xcodeproj"
    xcodeproj.mkdir()
    (xcodeproj / "project.pbxproj").write_text("// !$*UTF8*$!\n", encoding="utf-8")
    xcworkspace = repo / "Demo.xcworkspace"
    xcworkspace.mkdir()
    (xcworkspace / "contents.xcworkspacedata").write_text("<Workspace />\n", encoding="utf-8")

    snapshot = collect_local_repository(HarvestOptions(source=repo))
    profile = snapshot["projectProfile"]

    assert {item["id"] for item in profile["languages"]} == {
        "c-cpp",
        "go",
        "java-kotlin",
        "javascript",
        "objective-c",
        "php",
        "python",
        "ruby",
        "rust",
    }
    c_cpp_language = next(item for item in profile["languages"] if item["id"] == "c-cpp")
    assert c_cpp_language["confidence"] == "high"
    assert c_cpp_language["reason"] != "Makefile collected as ambiguous make project evidence."
    assert {item["id"] for item in profile["ecosystems"]} == {
        "autotools",
        "bun",
        "bundler",
        "cargo",
        "cmake",
        "cocoapods",
        "composer",
        "conan",
        "go",
        "gradle",
        "maven",
        "meson",
        "make",
        "pnpm",
        "pypi",
        "rubygems",
        "vcpkg",
        "xcode",
        "yarn",
    }
    assert {item["path"] for item in profile["manifests"]} == {
        *files.keys(),
        "Demo.xcodeproj/project.pbxproj",
        "Demo.xcworkspace/contents.xcworkspacedata",
    }
    assert {item["id"] for item in profile["analyzerPlan"]} == {
        "spec_harvester.c_cpp_manifest_profile",
        "spec_harvester.go_public_api",
        "spec_harvester.java_kotlin_manifest_profile",
        "spec_harvester.js_ts_public_api",
        "spec_harvester.objective_c_manifest_profile",
        "spec_harvester.php_manifest_profile",
        "spec_harvester.python_public_api",
        "spec_harvester.ruby_manifest_profile",
        "spec_harvester.rust_manifest_profile",
    }
    assert profile["diagnostics"] == []


def test_collect_local_repository_project_profile_treats_makefile_as_low_confidence(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "make-only"
    repo.mkdir()
    (repo / "Makefile").write_text("all:\n", encoding="utf-8")

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["projectProfile"]["languages"] == [
        {
            "id": "c-cpp",
            "confidence": "low",
            "reason": "Makefile collected as ambiguous make project evidence.",
            "evidencePaths": ["Makefile"],
        }
    ]
    assert snapshot["projectProfile"]["ecosystems"] == [
        {
            "id": "make",
            "language": "c-cpp",
            "packageManager": "make",
            "confidence": "low",
            "reason": "Makefile collected as ambiguous make project evidence.",
            "evidencePaths": ["Makefile"],
        }
    ]


def test_parse_swift_package_manifest_returns_none_without_package_metadata() -> None:
    assert parse_swift_package_manifest("// swift-tools-version: 6.0\n") is None


def test_parse_swift_package_manifest_ignores_commented_declarations() -> None:
    package = parse_swift_package_manifest(
        """
        // let package = Package(name: "Template")
        /*
        let package = Package(name: "BlockTemplate")
        /*
        .library(name: "NestedDisabledCore", targets: ["NestedDisabledCore"])
        */
        .library(name: "DisabledCore", targets: ["DisabledCore"])
        */
        import PackageDescription

        let package = Package(
            name: "Real",
            products: [
                // .library(name: "OldCore", targets: ["OldCore"]),
                .library(name: "RealCore", targets: ["RealCore"]),
            ],
            targets: [
                .target(
                    name: "RealCore",
                    swiftSettings: [.define("URL", to: "https://example.com")]
                )
            ]
        )
        """
    )

    assert package == {
        "ecosystem": "swift",
        "language": "swift",
        "name": "Real",
        "products": [{"name": "RealCore", "type": "library"}],
    }


def test_nested_swift_manifest_discovery_ignores_root_and_broken_symlinks(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "Package.swift").write_text("// root\n", encoding="utf-8")
    nested = repo / "Feature"
    nested.mkdir()
    nested_manifest = nested / "Package.swift"
    nested_manifest.write_text("// nested\n", encoding="utf-8")
    broken = repo / "Broken"
    broken.mkdir()
    (broken / "Package.swift").symlink_to(repo / "missing")

    manifests = nested_swift_package_manifests(repo)

    assert manifests == [nested_manifest]


def test_collect_local_repository_rejects_missing_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        collect_local_repository(HarvestOptions(source=tmp_path / "missing"))


def test_collect_local_repository_skips_paths_outside_source(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "package.json").write_text(
        json.dumps({"name": "@outside/secret", "version": "1.0.0"}),
        encoding="utf-8",
    )
    packages = repo / "packages"
    packages.mkdir()
    (packages / "core").symlink_to(outside, target_is_directory=True)

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["summary"]["fileCount"] == 0
    assert snapshot["summary"]["skippedFileCount"] == 1
    assert snapshot["skippedFiles"] == [
        {
            "path": "packages/core/package.json",
            "reason": "path_outside_source",
        }
    ]


def test_collect_local_repository_logs_internal_symlink_skips(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    target = repo / "real-package.json"
    target.write_text(
        json.dumps({"name": "@example/real", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (repo / "package.json").symlink_to(target)

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["summary"]["fileCount"] == 0
    assert snapshot["summary"]["skippedFileCount"] == 1
    assert snapshot["skippedFiles"] == [
        {
            "path": "package.json",
            "reason": "symlink_unsupported",
        }
    ]


def test_collect_local_repository_sorts_skipped_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    target = repo / "real-package.json"
    target.write_text(
        json.dumps({"name": "@example/real", "version": "1.0.0"}),
        encoding="utf-8",
    )
    z_path = repo / "z-package.json"
    a_path = repo / "a-package.json"
    z_path.symlink_to(target)
    a_path.symlink_to(target)
    monkeypatch.setattr(
        "spec_harvester.collector.candidate_files",
        lambda _root: [z_path, a_path],
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert [item["path"] for item in snapshot["skippedFiles"]] == [
        "a-package.json",
        "z-package.json",
    ]


def test_collect_local_repository_logs_non_file_and_large_file_skips(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    package_dir = repo / "package.json"
    package_dir.mkdir()
    readme = repo / "README.md"
    readme.write_text("# Demo\ncontent\n", encoding="utf-8")
    monkeypatch.setattr(
        "spec_harvester.collector.candidate_files",
        lambda _root: [package_dir, readme],
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo, max_file_bytes=4))

    assert snapshot["summary"]["fileCount"] == 0
    assert snapshot["skippedFiles"] == [
        {"path": "README.md", "reason": "file_too_large", "size": 15, "maxFileBytes": 4},
        {"path": "package.json", "reason": "not_regular_file"},
    ]


def test_collect_local_repository_records_binary_file_without_text_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    package_dir = repo / "packages" / "core" / "src"
    package_dir.mkdir(parents=True)
    entrypoint = package_dir / "index.js"
    entrypoint.write_bytes(b"\xff\xfe\x00")

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    record = snapshot["files"][0]
    assert record["path"] == "packages/core/src/index.js"
    assert record["kind"] == "source_entrypoint"
    assert "package" not in record
    assert "headings" not in record


def test_metadata_helpers_cover_static_file_variants(tmp_path: Path) -> None:
    workflow = tmp_path / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True)
    workflow.touch()

    assert classify_file(workflow) == "workflow"
    assert classify_file(tmp_path / "pnpm-workspace.yaml") == "workspace_manifest"
    assert classify_file(tmp_path / "index.ts") == "source_entrypoint"
    assert classify_file(tmp_path / "LICENSE.txt") == "license"
    assert classify_file(tmp_path / "COPYING.md") == "license"
    assert classify_file(tmp_path / "notes.txt") == "metadata"
    assert is_license_filename(tmp_path / "LICENSE.txt")
    assert is_license_filename(tmp_path / "copying.rst")
    assert not is_license_filename(tmp_path / "LICENSE.png")
    assert not is_license_filename(tmp_path / "THIRD_PARTY_LICENSES.txt")
    assert markdown_headings("# One\n## Two\n### Three\n", limit=2) == ["One", "Two"]
    semantic_hints = markdown_semantic_hints(
        "# API Contract\n\nOpenAPI JSON Schema supports request and response validation "
        "metadata for a web framework route, routes, and middleware.\n"
    )
    assert {
        "api contract",
        "json schema",
        "api",
        "contract",
        "schema",
        "openapi",
        "request",
        "response",
        "validation",
        "metadata",
        "web framework",
        "route",
        "routes",
        "middleware",
    }.issubset(set(semantic_hints))
    assert parse_package_json("{") is None
    assert parse_package_json("[]") is None
    assert parse_package_json('{"exports":"./dist/index.js"}') == {"exports": ["."]}


def test_collect_local_repository_records_markdown_semantic_hints(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "contract-hub"
    repo.mkdir()
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # Contract Hub

            ## API Contract

            OpenAPI JSON Schema supports request and response validation metadata.
            """
        ),
        encoding="utf-8",
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    readme = snapshot["files"][0]
    assert readme["path"] == "README.md"
    assert readme["kind"] == "documentation"
    assert readme["headings"] == ["Contract Hub", "API Contract"]
    assert {
        "api contract",
        "json schema",
        "api",
        "contract",
        "schema",
        "openapi",
        "request",
        "response",
        "validation",
        "metadata",
    }.issubset(set(readme["semanticHints"]))


def test_cli_writes_harvest_snapshot(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")
    out = tmp_path / "out"

    result = main(["collect-local", str(repo), "--out", str(out)])

    assert result == 0
    snapshot = json.loads((out / "harvest.json").read_text(encoding="utf-8"))
    assert snapshot["summary"]["fileCount"] == 1
    assert json.loads(capsys.readouterr().out)["status"] == "ok"


def test_draft_spec_package_writes_candidate_files(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/react-flow",
                "version": "1.0.0",
                "description": "React library for building node-based editors.",
                "license": "MIT",
                "peerDependencies": {"react": "^19.0.0"},
            }
        ),
        encoding="utf-8",
    )
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/react-flow",
            revision="abc123",
        )
    )
    candidate = tmp_path / "candidate"
    (candidate / "harvest.json").parent.mkdir(parents=True)
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.react_flow",
        )
    )

    assert result["status"] == "ok"
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: example.react_flow" in manifest
    assert "preview_only: true" in manifest
    assert "example.react_flow.react_flow" in spec
    assert "intent.javascript.react_library" in spec
    assert "intent.ui.node_based_editor" in spec
    assert "path: harvest.json" in spec


def test_draft_spec_package_keeps_interfaces_matched_to_valid_packages(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"version": "1.0.0", "description": "Root package without a name."}),
        encoding="utf-8",
    )
    package_dir = repo / "packages" / "core"
    package_dir.mkdir(parents=True)
    (package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/core",
                "version": "1.0.0",
                "description": "Core package.",
                "license": "MIT",
            }
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="example.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: package.core" in spec
    assert "Observed import surface for @example/core." in spec


def test_draft_spec_package_keeps_interface_ids_unique_for_scoped_name_collisions(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    first_package_dir = repo / "packages" / "scope-a"
    second_package_dir = repo / "packages" / "scope-b"
    first_package_dir.mkdir(parents=True)
    second_package_dir.mkdir(parents=True)
    (first_package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@scope-a/core",
                "version": "1.0.0",
                "description": "First scoped core package.",
            }
        ),
        encoding="utf-8",
    )
    (second_package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@scope-b/core",
                "version": "1.0.0",
                "description": "Second scoped core package.",
            }
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="example.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: package.core\n" in spec
    assert "id: package.core_2\n" in spec
    assert "Observed import surface for @scope-a/core." in spec
    assert "Observed import surface for @scope-b/core." in spec


def test_draft_spec_package_enriches_interfaces_from_public_interface_index(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/core",
                "version": "1.0.0",
                "description": "Core package.",
                "license": "MIT",
                "exports": {".": "./src/index.ts"},
            }
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(source=repo, repository="https://github.com/example/core", revision="abc123")
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    interface_index_path = tmp_path / "public-api.json"
    interface_index_path.write_text(
        render_public_interface_index_json(public_interface_index_fixture()),
        encoding="utf-8",
    )

    result = draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.core",
            interface_index=interface_index_path,
        )
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    copied_index = candidate / "public-interface-index.json"
    assert copied_index.exists()
    assert result["interfaceIndex"] == str(copied_index)
    assert "id: public_interface_index" in spec
    assert "kind: public_interface_index" in spec
    assert "artifactKind: SpecHarvesterPublicInterfaceIndex" in spec
    assert "mediaType: application/vnd.spec-harvester.public-interface-index+json" in spec
    assert "schemaVersion: 2" in spec
    assert "summary:" in spec
    assert "packageCount: 1" in spec
    assert "path: public-interface-index.json" in spec
    assert "interfaces.inbound.package.core" in spec
    assert "Observed public interface for @example/core from PublicInterfaceIndex." in spec
    assert "name: public_symbols" in spec
    assert "application/vnd.spec-harvester.public-interface-index+json" in spec
    assert 'packageId: "@example/core"' in spec
    assert "path: src/index.ts" in spec
    assert "symbolCount: 2" in spec
    assert "name: createGraph" in spec
    assert 'signature: "createGraph(options)"' in spec
    assert "sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" in spec


def test_draft_spec_package_auto_detects_colocated_public_interface_index(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "source": {"label": "demo", "revision": "abc123"},
        "policy": {"execution": "none"},
        "files": [],
    }
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    (candidate / "public-interface-index.json").write_text(
        render_public_interface_index_json(public_interface_index_fixture()),
        encoding="utf-8",
    )

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert result["interfaceIndex"] == str(candidate / "public-interface-index.json")
    assert "id: package.core" in spec
    assert "source: public_interface_index" in spec


def test_draft_spec_package_rejects_invalid_public_interface_index(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "harvest.json").write_text(
        json.dumps({"kind": "SpecHarvesterEvidenceSnapshot", "files": []}),
        encoding="utf-8",
    )
    interface_index_path = tmp_path / "invalid-public-api.json"
    interface_index_path.write_text(json.dumps({"kind": "Wrong"}), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid PublicInterfaceIndex"):
        draft_spec_package(
            DraftOptions(
                snapshot=candidate,
                out=candidate,
                interface_index=interface_index_path,
            )
        )

    assert not (candidate / "specpm.yaml").exists()


def test_draft_spec_package_keeps_capability_ids_unique_for_slug_collisions(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"name": "@example/react-flow", "version": "1.0.0"}),
        encoding="utf-8",
    )
    package_dir = repo / "packages" / "react"
    package_dir.mkdir(parents=True)
    (package_dir / "package.json").write_text(
        json.dumps({"name": "@example/react_flow", "version": "1.0.0"}),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="example.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: example.core.react_flow\n" in spec
    assert "id: example.core.react_flow_2\n" in spec


def test_draft_spec_package_uses_fallback_metadata_without_package_manifests(
    tmp_path: Path,
) -> None:
    snapshot = {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "source": "unexpected",
        "policy": {"execution": "none"},
        "files": [],
    }
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "id: generated_package.core" in manifest
    assert "license: UNKNOWN" in manifest
    assert "intent.package.public_repository_metadata" in spec


def test_draft_spec_package_uses_documentation_semantics_without_package_manifests(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "contract-hub"
    repo.mkdir()
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # Contract Hub

            ## API Contract

            OpenAPI JSON Schema describes endpoint request and response payloads.

            ## Workflow Automation

            CLI commands run schema validation for metadata manifest configuration.
            """
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/contract-hub",
            revision="abc123",
        )
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="contract_hub.core")
    )

    readme = next(item for item in snapshot["files"] if item["path"] == "README.md")
    assert {
        "api contract",
        "openapi",
        "schema",
        "request",
        "response",
        "validation",
        "workflow",
        "automation",
        "cli",
        "commands",
        "manifest",
        "configuration",
    }.issubset(set(readme["semanticHints"]))

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.api.contract_surface" in manifest
    assert "intent.metadata.schema_validation" in manifest
    assert "intent.workflow.automation_pipeline" in manifest
    assert "intent.developer.tooling_surface" in manifest
    assert "intent.package.public_repository_metadata" not in manifest
    assert "Provide language-neutral API contract documentation" in spec
    assert "id: semantic_intent_static_evidence" in spec
    semantic_evidence = rendered_evidence_item(spec, "semantic_intent_static_evidence")
    assert "provides.capabilities.intentIds" not in semantic_evidence
    assert "provides.capabilities" in semantic_evidence
    assert "provides.capabilities.contract_hub.core" in semantic_evidence
    assert "id: api.contract_surface" in spec
    assert "id: metadata.schema_validation" in spec
    assert "id: workflow.automation_pipeline" in spec
    assert "id: developer.tooling_surface" in spec
    assert "README.md" in spec


def test_draft_spec_package_does_not_double_count_singular_plural_semantic_terms(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "commands-only"
    repo.mkdir()
    (repo / "README.md").write_text(
        "# Commands Only\n\n## Commands\n\nUse commands.\n",
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(source=repo, repository="https://github.com/example/commands-only")
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="commands_only.core")
    )

    readme = next(item for item in snapshot["files"] if item["path"] == "README.md")
    assert readme["semanticHints"] == ["commands"]

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.workflow.automation_pipeline" not in manifest
    assert "intent.developer.tooling_surface" not in manifest
    assert "semantic_intent_static_evidence" not in spec
    assert "intent.package.public_repository_metadata" in manifest


def test_draft_spec_package_keeps_manifest_intents_with_language_neutral_docs(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "react-contracts"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/react-contracts",
                "version": "1.0.0",
                "description": "React library for rendering contract docs.",
            }
        ),
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # React Contracts

            ## API Contract

            OpenAPI schema request and response validation.
            """
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="react_contracts.core")
    )

    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "intent.javascript.react_library" in manifest
    assert "intent.api.contract_surface" not in manifest
    assert "React library for rendering contract docs." in spec
    assert "id: semantic_intent_static_evidence" in spec
    assert "id: api.contract_surface" in spec


def test_draft_spec_package_uses_web_framework_intents_from_flask_like_index(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "source": {
            "repository": "https://github.com/pallets/flask",
            "revision": "abc123",
            "label": "flask",
        },
        "policy": {"execution": "none"},
        "files": [],
    }
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    index = new_public_interface_index(
        source_revision="abc123",
        analyzers=[analyzer_record("spec_harvester.python_public_api", "0.1.0")],
        packages=[
            {
                "id": "flask.core",
                "path": ".",
                "language": "python",
                "entrypoints": [
                    {
                        "path": "src/flask/app.py",
                        "symbols": [
                            public_symbol("Flask", "class", "src/flask/app.py"),
                            public_symbol("Blueprint", "class", "src/flask/blueprints.py"),
                            public_symbol("Flask.route", "function", "src/flask/app.py"),
                            public_symbol("Flask.add_url_rule", "function", "src/flask/app.py"),
                            public_symbol("RequestContext", "class", "src/flask/ctx.py"),
                            public_symbol("after_this_request", "function", "src/flask/ctx.py"),
                            public_symbol("before_request", "function", "src/flask/app.py"),
                            public_symbol("after_request", "function", "src/flask/app.py"),
                            public_symbol("jsonify", "function", "src/flask/json/__init__.py"),
                            public_symbol("render_template", "function", "src/flask/templating.py"),
                            public_symbol("session", "variable", "src/flask/globals.py"),
                            public_symbol("endpoint", "variable", "src/flask/app.py"),
                        ],
                    }
                ],
            }
        ],
    )
    (candidate / "public-interface-index.json").write_text(
        render_public_interface_index_json(index),
        encoding="utf-8",
    )

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="flask.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.web.framework_surface" in manifest
    assert "intent.web.http_routing" in manifest
    assert "intent.web.middleware_pipeline" in manifest
    assert "intent.web.request_response_context" in manifest
    assert "intent.package.public_repository_metadata" not in manifest
    assert "Provide a statically evidenced web framework surface" in spec
    assert "id: web.framework_surface" in spec
    assert "id: web.http_routing" in spec
    assert "id: web.middleware_pipeline" in spec
    assert "id: web.request_response_context" in spec
    assert "public-interface-index.json" in spec
    semantic_evidence = rendered_evidence_item(spec, "semantic_intent_static_evidence")
    assert "public-interface-index.json" not in semantic_evidence
    assert "provides.capabilities.intentIds" not in semantic_evidence
    assert "provides.capabilities.flask.core" in semantic_evidence
    assert "evidenceKinds:" in semantic_evidence
    assert "- public_interface_index" in semantic_evidence


def test_draft_spec_package_uses_web_framework_intents_from_gin_like_index(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "source": {
            "repository": "https://github.com/gin-gonic/gin",
            "revision": "abc123",
            "label": "gin",
        },
        "policy": {"execution": "none"},
        "files": [{"path": "go.mod", "kind": "package_manifest"}],
    }
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    index = new_public_interface_index(
        source_revision="abc123",
        analyzers=[analyzer_record("spec_harvester.go_public_api", "0.1.0")],
        packages=[
            {
                "id": "github.com/gin-gonic/gin",
                "path": ".",
                "language": "go",
                "entrypoints": [
                    {
                        "path": "gin.go",
                        "symbols": [
                            public_symbol("Engine", "struct", "gin.go"),
                            public_symbol("RouterGroup", "struct", "routergroup.go"),
                            public_symbol("IRoutes", "interface", "routergroup.go"),
                            public_symbol("RouteInfo", "struct", "routes.go"),
                            public_symbol("HandlerFunc", "type", "gin.go"),
                            public_symbol("HandlersChain", "type", "gin.go"),
                            public_symbol("Middleware", "function", "middleware.go"),
                            public_symbol("Context", "struct", "context.go"),
                            public_symbol("Context.Request", "variable", "context.go"),
                            public_symbol("Context.JSON", "function", "context.go"),
                            public_symbol("Context.BindJSON", "function", "context.go"),
                            public_symbol("RouterGroup.GET", "function", "routergroup.go"),
                            public_symbol("RouterGroup.Handle", "function", "routergroup.go"),
                        ],
                    }
                ],
            }
        ],
    )
    (candidate / "public-interface-index.json").write_text(
        render_public_interface_index_json(index),
        encoding="utf-8",
    )

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="gin.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.web.framework_surface" in manifest
    assert "intent.web.http_routing" in manifest
    assert "intent.web.middleware_pipeline" in manifest
    assert "intent.web.request_response_context" in manifest
    assert "intent.package.public_repository_metadata" not in manifest
    assert "id: web.framework_surface" in spec
    assert "matchedTerms:" in spec


def test_public_interface_semantic_terms_are_bounded_for_large_indexes() -> None:
    index = new_public_interface_index(
        source_revision="abc123",
        analyzers=[analyzer_record("spec_harvester.python_public_api", "0.1.0")],
        packages=[
            {
                "id": "huge.framework",
                "path": ".",
                "language": "python",
                "entrypoints": [
                    {
                        "path": "src/huge.py",
                        "symbols": [
                            public_symbol(
                                f"VeryLargeRouterHandlerSymbol{item}",
                                "function",
                                "src/huge.py",
                            )
                            | {"signature": "handle(" + "x: RequestContext, " * 80 + ")"}
                            for item in range(1_000)
                        ],
                    }
                ],
            }
        ],
    )

    terms = public_interface_semantic_terms(index)

    assert len(terms) == 2_000
    assert sum(len(term) + 1 for term in terms) <= 60_000
    assert all(len(term) <= 160 for term in terms)
    assert not any("x: requestcontext" in term for term in terms)


def test_draft_spec_package_applies_web_semantics_to_manifest_capabilities(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "web-adapter"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "web-adapter",
                "version": "1.0.0",
                "description": "Adapter package.",
            }
        ),
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # Web Adapter

            ## Web Framework

            Routes, router endpoints, and middleware handlers manage request
            and response context.
            """
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="web_adapter.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.web.framework_surface" in manifest
    assert "intent.web.http_routing" in manifest
    assert "intent.package.javascript_library" not in manifest
    assert "Adapter package." not in spec
    assert "Provide a statically evidenced web framework surface" in spec


def test_draft_spec_package_uses_swift_product_intents(tmp_path: Path) -> None:
    repo = tmp_path / "puzzle"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription

        let package = Package(
            name: "Puzzle",
            products: [
                .library(name: "PuzzleCore", targets: ["PuzzleCore"]),
                .library(name: "PuzzleUIKit", targets: ["PuzzleUIKit"]),
            ]
        )
        """,
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/SoundBlaster/Puzzle",
        )
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="puzzle.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.swift.product.puzzlecore" in spec
    assert "intent.swift.product.puzzleuikit" in spec
    assert "intent.package.public_repository_metadata" not in spec
    assert "intent.swift.product.puzzlecore" in manifest
    assert "intent.swift.product.puzzleuikit" in manifest
    assert "    - swift\n" in manifest
    assert "    - javascript\n" not in manifest
    assert "    - web\n" not in manifest
    assert "    - node\n" not in manifest


def test_draft_spec_package_infers_python_compatibility_from_project_profile(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "page-index"
    repo.mkdir()
    (repo / "pyproject.toml").write_text(
        "[project]\nname = 'page-index'\n",
        encoding="utf-8",
    )
    (repo / "Makefile").write_text("test:\n\tpython -m pytest\n", encoding="utf-8")
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(source=repo, repository="https://github.com/example/page-index")
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="page_index.core")
    )

    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "  languages:\n    - python\n" in manifest
    assert "  platforms:\n    - any\n" in manifest
    assert "    - c\n" not in manifest
    assert "    - c++\n" not in manifest
    assert "    - javascript\n" not in manifest
    assert "    - web\n" not in manifest
    assert "    - node\n" not in manifest


def test_draft_spec_package_infers_apple_compatibility_from_xcode_evidence(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "apple-kit"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "AppleKit",
            products: [.library(name: "AppleKit", targets: ["AppleKit"])]
        )
        """,
        encoding="utf-8",
    )
    xcode_project = repo / "AppleKit.xcodeproj"
    xcode_project.mkdir()
    (xcode_project / "project.pbxproj").write_text("// !$*UTF8*$!\n", encoding="utf-8")
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    draft_spec_package(DraftOptions(snapshot=candidate, out=candidate, package_id="apple_kit.core"))

    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "  platforms:\n    - ios\n    - macos\n" in manifest
    assert "  languages:\n    - swift\n    - objective-c\n" in manifest
    assert "    - linux\n" not in manifest


def test_draft_spec_package_prefers_semantic_ios_screen_intents(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "puzzle"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "Puzzle",
            products: [
                .library(name: "PuzzleCore", targets: ["PuzzleCore"]),
                .library(name: "PuzzleUIKit", targets: ["PuzzleUIKit"]),
            ]
        )
        """,
        encoding="utf-8",
    )
    prd = repo / "SPECS" / "PRD"
    prd.mkdir(parents=True)
    (prd / "Puzzle-Framework-PRD.md").write_text(
        textwrap.dedent(
            """
        # Puzzle Framework PRD

        ## Migration Glue at the Screen Boundary, Not App Framework

        ## Objective

        ## Collection Layer

        ## State Layer
        """
        ),
        encoding="utf-8",
    )
    docc = repo / "Sources" / "PuzzleUIKit" / "Documentation.docc"
    docc.mkdir(parents=True)
    (docc / "PuzzleUIKit.md").write_text(
        textwrap.dedent(
            """
        # PuzzleUIKit

        ## Compose UIKit and SwiftUI screens

        ## Collection layouts

        ## Diagnostics overlay
        """
        ),
        encoding="utf-8",
    )
    dependency = repo / "Derived" / "SourcePackages" / "checkouts" / "swift-syntax"
    dependency.mkdir(parents=True)
    (dependency / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "swift-syntax",
            products: [.library(name: "SwiftSyntax", targets: ["SwiftSyntax"])]
        )
        """,
        encoding="utf-8",
    )
    fixture = repo / "Tests" / "CompileFixtures" / "FixturePackage"
    fixture.mkdir(parents=True)
    (fixture / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "PuzzleFixture",
            products: [.library(name: "PuzzleFixture", targets: ["PuzzleFixture"])]
        )
        """,
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(source=repo, repository="https://github.com/SoundBlaster/Puzzle")
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="puzzle.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.ios.screen_level_composition" in spec
    assert "intent.ios.uikit_swiftui_migration" in spec
    assert "intent.ios.collection_layout_composition" in spec
    assert "intent.ios.screen_state_binding" in spec
    assert "intent.ios.screen_diagnostics" in spec
    assert "intent.swift.product.puzzlecore" not in spec
    assert "intent.swift.product.puzzleuikit" not in manifest
    assert "  platforms:\n    - ios\n    - macos\n" in manifest
    assert "  languages:\n    - swift\n" in manifest
    assert (
        "Provide a screen-level composition framework for incrementally migrating "
        "UIKit-heavy iOS screens to mixed UIKit/SwiftUI surfaces."
    ) in spec
    assert "id: semantic_intent_static_evidence" in spec
    assert "SPECS/PRD/Puzzle-Framework-PRD.md" in spec
    assert "Sources/PuzzleUIKit/Documentation.docc/PuzzleUIKit.md" in spec
    assert "package.swift_syntax" not in spec
    assert "package.puzzlefixture" not in spec


def test_draft_spec_package_does_not_assign_ios_intents_without_ios_evidence(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "screen-composer"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "screen-composer",
                "description": "Compose screen layouts for web dashboards.",
            }
        ),
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        "# Screen Composer\n\n## Screen composition\n\n## Container layout\n",
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="screen_composer.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.ios.screen_level_composition" not in spec
    assert "intent.ios.collection_layout_composition" not in spec
    assert "intent.package.javascript_library" in manifest


def test_draft_spec_package_does_not_assign_swift_semantic_intents_without_swift_evidence(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "feature-specs"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "feature-specs",
                "description": ("JavaScript package for conditional feature flag specifications."),
            }
        ),
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # Feature Specs

            ## Specification pattern
            ## Specifications
            ## Feature flags
            ## Conditional rollout rules
            """
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="feature_specs.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.swift.specification_pattern" not in spec
    assert "intent.swift.feature_gating" not in spec
    assert "intent.package.javascript_library" in manifest


def test_draft_spec_package_does_not_assign_swift_context_from_uikit_heading(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "ui-interop"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "ui-interop",
                "description": "Utilities for custom web UI widgets.",
            }
        ),
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # UI Interop

            ## UIKit Integration
            ## Conditional feature flags
            """
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="ui_interop.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.swift.specification_pattern" not in spec
    assert "intent.swift.feature_gating" not in spec
    assert "intent.package.javascript_library" in manifest


def test_draft_spec_package_uses_semantic_evidence_index_for_specification_pattern(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "SpecificationKit"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "SpecificationKit",
            products: [
                .library(name: "SpecificationKit", targets: ["SpecificationKit"]),
                .macro(name: "SpecificationKitMacros", targets: ["SpecificationKitMacros"]),
            ]
        )
        """,
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        textwrap.dedent(
            """
            # SpecificationKit

            ## Core Components
            ## Specifications
            ## PredicateSpec
            ## @ConditionalSatisfies - Runtime Specification Selection
            ## Feature Flag System
            ## Enhanced Reactive Wrappers
            ## SpecificationTracer
            """
        ),
        encoding="utf-8",
    )
    docc = repo / "Sources" / "SpecificationKit" / "Documentation.docc"
    docc.mkdir(parents=True)
    (docc / "SpecificationKit.md").write_text(
        textwrap.dedent(
            """
            # ``SpecificationKit``

            ## Composable Business Logic
            ## Decision Making
            ## Composition and Reusability
            ## Reactive Integration
            """
        ),
        encoding="utf-8",
    )
    (docc / "CompositeContextProvider.md").write_text(
        "# CompositeContextProvider\n\n## Context Providers\n",
        encoding="utf-8",
    )
    (docc / "ThresholdSpec.md").write_text(
        "# ThresholdSpec\n\n## Feature Gating\n",
        encoding="utf-8",
    )
    (docc / "SpecificationTracer.md").write_text(
        "# SpecificationTracer\n\n## Tracing\n\n## Performance Analysis\n",
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(source=repo, repository="git@github.com:SoundBlaster/SpecificationKit.git")
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="specificationkit.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.swift.specification_pattern" in manifest
    assert "intent.swift.predicate_composition" in manifest
    assert "intent.swift.context_driven_decisioning" in manifest
    assert "intent.swift.feature_gating" in manifest
    assert "intent.swift.reactive_specification_evaluation" in manifest
    assert "intent.swift.specification_tracing" in manifest
    assert "intent.swift.product.specificationkit" not in manifest
    assert (
        "Provide a Swift Specification Pattern toolkit for composing reusable "
        "predicates, context-driven decisions, feature gates, reactive evaluation, "
        "and diagnostic tracing."
    ) in spec
    assert "semanticEvidenceIndex:" in spec
    assert "id: swift.specification_pattern" in spec
    assert "id: swift.context_driven_decisioning" in spec
    assert "README.md" in spec
    assert "Sources/SpecificationKit/Documentation.docc/SpecificationKit.md" in spec


def test_draft_spec_package_preserves_reviewable_nested_swift_interfaces(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "workspace"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "Workspace",
            products: [.library(name: "Workspace", targets: ["Workspace"])]
        )
        """,
        encoding="utf-8",
    )
    feature = repo / "Packages" / "Feature"
    feature.mkdir(parents=True)
    (feature / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "Feature",
            products: [.library(name: "Feature", targets: ["Feature"])]
        )
        """,
        encoding="utf-8",
    )
    generated = repo / "Derived" / "SourcePackages" / "checkouts" / "swift-syntax"
    generated.mkdir(parents=True)
    (generated / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "swift-syntax",
            products: [.library(name: "SwiftSyntax", targets: ["SwiftSyntax"])]
        )
        """,
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="workspace.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "workspace.core.workspace" in manifest
    assert "workspace.core.feature" not in manifest
    assert "package.workspace" in spec
    assert "package.feature" in spec
    assert "package.swift_syntax" not in spec


def test_draft_spec_package_uses_root_swift_manifest_for_capability_intents(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "puzzle"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "Puzzle",
            products: [.library(name: "PuzzleCore", targets: ["PuzzleCore"])]
        )
        """,
        encoding="utf-8",
    )
    dependency = repo / "Derived" / "SourcePackages" / "checkouts" / "swift-syntax"
    dependency.mkdir(parents=True)
    (dependency / "Package.swift").write_text(
        """
        import PackageDescription
        let package = Package(
            name: "swift-syntax",
            products: [.library(name: "SwiftSyntax", targets: ["SwiftSyntax"])]
        )
        """,
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="puzzle.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "intent.swift.product.puzzlecore" in manifest
    assert "intent.swift.product.swiftsyntax" not in manifest
    assert "puzzle.core.swift_syntax" not in spec


def test_draft_spec_package_prefers_manifest_license_over_license_file(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/system",
                "description": "Core system",
                "license": "Apache-2.0",
            }
        ),
        encoding="utf-8",
    )
    (repo / "LICENSE").write_text("MIT License\nPermission is hereby granted.\n")
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/system",
        )
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    manifest = Path(result["manifest"]).read_text(encoding="utf-8")
    assert "license: Apache-2.0" in manifest


def test_draft_spec_package_infers_license_from_license_file(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/system",
                "description": "Core system",
            }
        ),
        encoding="utf-8",
    )
    (repo / "LICENSE").write_text(
        "MIT License\n"
        "Copyright 2026 Example\n"
        "Permission is hereby granted, free of charge, to any person\n"
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/system",
        )
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    manifest = Path(result["manifest"]).read_text(encoding="utf-8")
    assert "license: MIT" in manifest
    assert "licenseEvidence:" in manifest
    assert "source: license_file_hint" in manifest
    assert "paths:" in manifest
    assert "- LICENSE" in manifest


def test_draft_spec_package_keeps_unknown_for_ambiguous_license_file(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "LICENSE").write_text("All rights reserved. Internal use only.")
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/system",
        )
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    manifest = Path(result["manifest"]).read_text(encoding="utf-8")
    assert "license: UNKNOWN" in manifest
    assert "licenseEvidence:" in manifest
    assert "source: ambiguous_license_file" in manifest
    assert "- LICENSE" in manifest


def test_draft_spec_package_marks_absent_license_evidence(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/system",
        )
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    manifest = Path(result["manifest"]).read_text(encoding="utf-8")
    assert "license: UNKNOWN" in manifest
    assert "licenseEvidence:" in manifest
    assert "source: absent" in manifest
    assert "paths: []" in manifest


def test_draft_spec_package_rejects_unsupported_snapshot_kind(tmp_path: Path) -> None:
    snapshot = tmp_path / "harvest.json"
    snapshot.write_text(json.dumps({"kind": "OtherSnapshot"}), encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported harvest snapshot kind"):
        draft_spec_package(DraftOptions(snapshot=snapshot, out=tmp_path / "candidate"))


def test_render_scalar_quotes_yaml_reserved_words() -> None:
    assert render_scalar("true") == '"true"'
    assert render_scalar("FALSE") == '"FALSE"'
    assert render_scalar("null") == '"null"'
    assert render_scalar("yes") == '"yes"'
    assert render_scalar("off") == '"off"'
    assert render_scalar("~") == '"~"'


def test_cli_draft_writes_candidate_files(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"name": "@example/system", "description": "Core system", "license": "MIT"}),
        encoding="utf-8",
    )
    out = tmp_path / "candidate"
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    out.mkdir()
    (out / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = main(["draft", str(out), "--out", str(out), "--package-id", "example.core"])

    assert result == 0
    assert (out / "specpm.yaml").exists()
    assert (out / "specs" / "demo.spec.yaml").exists()
    assert json.loads(capsys.readouterr().out)["packageId"] == "example.core"


def test_cli_draft_accepts_public_interface_index(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"name": "@example/core", "description": "Core system", "license": "MIT"}),
        encoding="utf-8",
    )
    out = tmp_path / "candidate"
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    out.mkdir()
    (out / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    interface_index_path = tmp_path / "public-api.json"
    interface_index_path.write_text(
        render_public_interface_index_json(public_interface_index_fixture()),
        encoding="utf-8",
    )

    result = main(
        [
            "draft",
            str(out),
            "--out",
            str(out),
            "--package-id",
            "example.core",
            "--interface-index",
            str(interface_index_path),
        ]
    )

    cli_result = json.loads(capsys.readouterr().out)
    assert result == 0
    assert cli_result["interfaceIndex"] == str(out / "public-interface-index.json")
    assert "name: createGraph" in (out / "specs" / "demo.spec.yaml").read_text(encoding="utf-8")


def test_promote_candidate_copies_package_and_updates_manifest(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    validator = tmp_path / "specpm"
    validator.write_text('#!/bin/sh\nprintf \'{"status":"warning_only"}\\n\'\n', encoding="utf-8")
    validator.chmod(0o755)
    accepted_root = tmp_path / "accepted"
    manifest = tmp_path / "accepted-packages.yml"

    result = promote_candidate(
        PromoteOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            manifest=manifest,
            manifest_entry_path="accepted/example.core/0.1.0",
            specpm_command=str(validator),
        )
    )

    destination = accepted_root / "example.core" / "0.1.0"
    assert result["status"] == "ok"
    assert result["validationStatus"] == "warning_only"
    assert (destination / "specpm.yaml").exists()
    assert (destination / "harvest.json").exists()
    assert (destination / "specs" / "demo.spec.yaml").exists()
    assert "  - path: accepted/example.core/0.1.0\n" in manifest.read_text(encoding="utf-8")


def test_promote_candidate_rejects_candidate_symlinks(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    (candidate / "evidence-link").symlink_to(outside)

    with pytest.raises(ValueError, match="unsupported symlink"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                skip_validation=True,
            )
        )


def test_promote_candidate_rejects_missing_candidate_and_manifest(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Candidate directory does not exist"):
        promote_candidate(
            PromoteOptions(
                candidate=tmp_path / "missing",
                accepted_root=tmp_path / "accepted",
                skip_validation=True,
            )
        )

    candidate = tmp_path / "candidate"
    candidate.mkdir()
    with pytest.raises(ValueError, match="missing specpm.yaml"):
        promote_candidate(PromoteOptions(candidate=candidate, accepted_root=tmp_path / "accepted"))


def test_promote_candidate_rejects_existing_destination_without_force(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    destination = tmp_path / "accepted" / "example.core" / "0.1.0"
    destination.mkdir(parents=True)

    with pytest.raises(ValueError, match="Destination already exists"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                skip_validation=True,
            )
        )


def test_promote_candidate_rejects_escaping_package_subdir(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)

    with pytest.raises(ValueError, match="escapes accepted root"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                package_subdir="../escape",
                skip_validation=True,
            )
        )


def test_promote_candidate_rejects_invalid_specpm_validation(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    validator = tmp_path / "specpm"
    validator.write_text('#!/bin/sh\nprintf \'{"status":"invalid"}\\n\'\n', encoding="utf-8")
    validator.chmod(0o755)

    with pytest.raises(ValueError, match="SpecPM validation failed"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                specpm_command=str(validator),
            )
        )


def test_validate_with_specpm_reports_tool_failures(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()

    with pytest.raises(ValueError, match="was not found"):
        validate_with_specpm(candidate, command=str(tmp_path / "missing-specpm"))

    non_json = tmp_path / "non-json-specpm"
    non_json.write_text("#!/bin/sh\necho nope\n", encoding="utf-8")
    non_json.chmod(0o755)
    with pytest.raises(ValueError, match="did not return JSON"):
        validate_with_specpm(candidate, command=str(non_json))

    failed = tmp_path / "failed-specpm"
    failed.write_text('#!/bin/sh\nprintf \'{"status":"error"}\\n\'\nexit 2\n', encoding="utf-8")
    failed.chmod(0o755)
    with pytest.raises(ValueError, match="failed unexpectedly"):
        validate_with_specpm(candidate, command=str(failed), pythonpath="src")


def test_promote_candidate_inserts_manifest_entry_inside_packages_block(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text(
        "schemaVersion: 1\n"
        "packages:\n"
        "  - path: existing/package\n"
        "# keep comment\n"
        "metadata:\n"
        "  owner: test\n",
        encoding="utf-8",
    )

    promote_candidate(
        PromoteOptions(
            candidate=candidate,
            accepted_root=tmp_path / "accepted",
            manifest=manifest,
            manifest_entry_path="accepted/example.core/0.1.0",
            skip_validation=True,
        )
    )

    text = manifest.read_text(encoding="utf-8")
    assert "  - path: accepted/example.core/0.1.0\n" in text
    assert text.index("  - path: accepted/example.core/0.1.0") < text.index("metadata:")


def test_promote_candidate_accepts_empty_packages_list_with_inline_comment(
    tmp_path: Path,
) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text(
        "schemaVersion: 1\n"
        "packages: []  # generated packages are inserted here\n"
        "metadata:\n"
        "  owner: test\n",
        encoding="utf-8",
    )

    promote_candidate(
        PromoteOptions(
            candidate=candidate,
            accepted_root=tmp_path / "accepted",
            manifest=manifest,
            manifest_entry_path="accepted/example.core/0.1.0",
            skip_validation=True,
        )
    )

    text = manifest.read_text(encoding="utf-8")
    assert "packages:\n  - path: accepted/example.core/0.1.0\n" in text
    assert text.index("  - path: accepted/example.core/0.1.0") < text.index("metadata:")


def test_promote_candidate_rejects_unsafe_manifest_entry_path(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)

    with pytest.raises(ValueError, match="relative|parent|newlines"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                manifest=tmp_path / "accepted-packages.yml",
                manifest_entry_path="../accepted/example.core/0.1.0",
                skip_validation=True,
            )
        )


def test_append_local_manifest_entry_rejects_invalid_packages_field(tmp_path: Path) -> None:
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text("schemaVersion: 1\npackages: wrong\n", encoding="utf-8")

    with pytest.raises(ValueError, match="block list or an empty list"):
        append_local_manifest_entry(manifest, "accepted/example.core/0.1.0")


def test_infer_manifest_entry_path_requires_relative_manifest_path(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest-root" / "accepted-packages.yml"
    destination = tmp_path / "accepted" / "example.core" / "0.1.0"
    manifest.parent.mkdir()
    destination.mkdir(parents=True)

    with pytest.raises(ValueError, match="manifest entry path"):
        infer_manifest_entry_path(manifest, destination)


def test_promote_candidate_force_preserves_destination_when_copy_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = draft_demo_candidate(tmp_path)
    accepted_root = tmp_path / "accepted"
    destination = accepted_root / "example.core" / "0.1.0"
    destination.mkdir(parents=True)
    existing_file = destination / "keep.txt"
    existing_file.write_text("keep", encoding="utf-8")

    def fail_copytree(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise OSError("copy failed")

    monkeypatch.setattr("spec_harvester.promoter.shutil.copytree", fail_copytree)

    with pytest.raises(OSError, match="copy failed"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                force=True,
                skip_validation=True,
            )
        )

    assert existing_file.read_text(encoding="utf-8") == "keep"


def test_cli_promote_writes_json_result(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    candidate = draft_demo_candidate(tmp_path)
    accepted_root = tmp_path / "accepted"

    result = main(
        [
            "promote",
            str(candidate),
            "--accepted-root",
            str(accepted_root),
            "--skip-validation",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert result == 0
    assert output["packageId"] == "example.core"
    assert output["validationStatus"] == "skipped"
    assert (accepted_root / "example.core" / "0.1.0" / "specpm.yaml").exists()


def test_prepare_accepted_manifest_entry_defaults_to_public_index_generated_path(
    tmp_path: Path,
) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"

    result = prepare_accepted_manifest_entry(
        PrepareAcceptedManifestEntryOptions(
            candidate=candidate,
            manifest=manifest,
        )
    )

    assert result["status"] == "ok"
    assert result["packageId"] == "example.core"
    assert result["packageVersion"] == "0.1.0"
    assert result["packageSubdir"] == "example.core/0.1.0"
    assert result["manifest"]["entry"] == "public-index/generated/example.core/0.1.0"
    assert result["manifest"]["updated"] is True
    assert "  - path: public-index/generated/example.core/0.1.0\n" in manifest.read_text(
        encoding="utf-8"
    )


def test_prepare_accepted_manifest_entry_supports_custom_prefix_and_subdir(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"

    result = prepare_accepted_manifest_entry(
        PrepareAcceptedManifestEntryOptions(
            candidate=candidate,
            manifest=manifest,
            manifest_entry_prefix="review/generated",
            package_subdir="review/example.core/0.2.0",
        )
    )

    assert result["manifest"]["entry"] == "review/generated/review/example.core/0.2.0"
    assert "  - path: review/generated/review/example.core/0.2.0\n" in manifest.read_text(
        encoding="utf-8"
    )


def test_prepare_accepted_manifest_entry_supports_explicit_entry_path(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"

    result = prepare_accepted_manifest_entry(
        PrepareAcceptedManifestEntryOptions(
            candidate=candidate,
            manifest=manifest,
            manifest_entry_path="overrides/example.core/0.1.0",
        )
    )

    assert result["manifest"]["entry"] == "overrides/example.core/0.1.0"
    assert "  - path: overrides/example.core/0.1.0\n" in manifest.read_text(encoding="utf-8")


def test_prepare_accepted_manifest_entry_leaves_manifest_idempotent_when_entry_exists(
    tmp_path: Path,
) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text(
        "schemaVersion: 1\n"
        "packages:\n"
        "  - path: public-index/generated/example.core/0.1.0\n"
        "metadata:\n"
        "  owner: test\n",
        encoding="utf-8",
    )

    result = prepare_accepted_manifest_entry(
        PrepareAcceptedManifestEntryOptions(
            candidate=candidate,
            manifest=manifest,
        )
    )

    assert result["manifest"]["updated"] is False
    assert (
        manifest.read_text(encoding="utf-8").count(
            "  - path: public-index/generated/example.core/0.1.0\n"
        )
        == 1
    )


def test_prepare_accepted_manifest_entry_rejects_invalid_candidate(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()

    with pytest.raises(ValueError, match="Candidate is missing specpm.yaml"):
        prepare_accepted_manifest_entry(
            PrepareAcceptedManifestEntryOptions(
                candidate=candidate,
                manifest=tmp_path / "accepted-packages.yml",
            )
        )


def test_prepare_accepted_manifest_entry_rejects_candidate_symlinks(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    external_manifest = tmp_path / "external-specpm.yaml"
    external_manifest.write_text(
        "schemaVersion: 1\nmetadata:\n  id: external.core\n  version: 9.9.9\n",
        encoding="utf-8",
    )
    (candidate / "specpm.yaml").unlink()
    (candidate / "specpm.yaml").symlink_to(external_manifest)

    with pytest.raises(ValueError, match="unsupported symlink"):
        prepare_accepted_manifest_entry(
            PrepareAcceptedManifestEntryOptions(
                candidate=candidate,
                manifest=tmp_path / "accepted-packages.yml",
            )
        )


def test_cli_prepare_accepted_manifest_entry_writes_json_result(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"

    result = main(
        [
            "prepare-accepted-entry",
            str(candidate),
            "--manifest",
            str(manifest),
            "--manifest-entry-prefix",
            "public-index/generated",
            "--package-subdir",
            "example.core/0.1.0",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert result == 0
    assert output["manifest"]["entry"] == "public-index/generated/example.core/0.1.0"
    assert output["manifest"]["updated"] is True


def draft_demo_candidate(tmp_path: Path) -> Path:
    repo = tmp_path / "demo"
    repo.mkdir(exist_ok=True)
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/demo",
                "version": "1.0.0",
                "description": "Demo package",
                "license": "MIT",
            }
        ),
        encoding="utf-8",
    )
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/demo",
            revision="abc123",
        )
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir(exist_ok=True)
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.core",
        )
    )
    return candidate


def public_interface_index_fixture() -> dict:
    return new_public_interface_index(
        source_revision="abc123",
        analyzers=[
            analyzer_record(
                "js-ts-manifest-export-analyzer",
                "0.1.0",
                execution="none",
                confidence="medium",
            )
        ],
        packages=[
            {
                "id": "@example/core",
                "path": ".",
                "language": "javascript-typescript",
                "entrypoints": [
                    {
                        "path": "src/index.ts",
                        "symbols": [
                            {
                                "name": "GraphOptions",
                                "kind": "type",
                                "visibility": "public",
                                "evidence": evidence_record("src/index.ts", "a" * 64),
                            },
                            {
                                "name": "createGraph",
                                "kind": "function",
                                "visibility": "public",
                                "signature": "createGraph(options)",
                                "evidence": evidence_record("src/index.ts", "a" * 64),
                            },
                        ],
                    }
                ],
            }
        ],
    )
