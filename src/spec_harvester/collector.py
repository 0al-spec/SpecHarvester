from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.classifier_registry import default_classifier_policy
from spec_harvester.go_public_api import go_source_files
from spec_harvester.license_files import is_license_filename
from spec_harvester.semantic_keyword_taxonomy import SEMANTIC_KEYWORD_TAXONOMY
from spec_harvester.swift_public_api import swift_source_files
from spec_harvester.swift_text import strip_swift_comments
from spec_harvester.tuist_manifest import parse_tuist_manifest

SNAPSHOT_KIND = "SpecHarvesterEvidenceSnapshot"
SNAPSHOT_SCHEMA_VERSION = 1
ANALYZER_TRUST_POLICY_SCHEMA_VERSION = 1
PROJECT_PROFILE_SCHEMA_VERSION = 1
DEFAULT_MAX_FILE_BYTES = 512 * 1024
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}

ROOT_FILES = [
    "README.md",
    "README",
    "Project.swift",
    "Workspace.swift",
    "Tuist.swift",
    "package.json",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "Package.swift",
    "pnpm-workspace.yaml",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "turbo.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "gradle.properties",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "composer.json",
    "composer.lock",
    "CMakeLists.txt",
    "meson.build",
    "configure.ac",
    "configure.in",
    "Makefile",
    "conanfile.txt",
    "conanfile.py",
    "vcpkg.json",
    "Podfile",
    "Podfile.lock",
    "Gemfile",
    "Gemfile.lock",
]

SAFE_GLOBS = [
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "docs/*.md",
    "SPECS/PRD/*.md",
    "Sources/*/Documentation.docc/*.md",
    "Sources/*/Documentation.docc/Concepts/*.md",
    "packages/*/README.md",
    "packages/*/package.json",
    "packages/*/pyproject.toml",
    "packages/*/Package.swift",
    "packages/*/Cargo.toml",
    "packages/*/go.mod",
    "packages/*/composer.json",
    "packages/*/CMakeLists.txt",
    "packages/*/Gemfile",
    "packages/*/*.gemspec",
    "packages/*/src/index.ts",
    "packages/*/src/index.tsx",
    "packages/*/src/index.js",
    "apps/*/package.json",
    "apps/*/pyproject.toml",
    "apps/*/Package.swift",
    "apps/*/Cargo.toml",
    "apps/*/go.mod",
    "apps/*/composer.json",
    "apps/*/CMakeLists.txt",
    "apps/*/Podfile",
    "apps/*/*.xcodeproj/project.pbxproj",
    "*.gemspec",
    "*.xcodeproj/project.pbxproj",
    "*.xcworkspace/contents.xcworkspacedata",
    "examples/README.md",
]

IGNORED_NESTED_SWIFT_MANIFEST_DIRS = {
    ".build",
    ".git",
    ".swiftpm",
    "Derived",
    "DerivedData",
    "build",
    "node_modules",
}

SOURCE_FILE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".m",
    ".mm",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".swift",
    ".ts",
    ".tsx",
}
IGNORED_SOURCE_DIRS = {
    ".build",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".swiftpm",
    ".tox",
    ".venv",
    "Carthage",
    "Derived",
    "DerivedData",
    "Pods",
    "SourcePackages",
    "__pycache__",
    "build",
    "checkouts",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "testdata",
    "tmp",
    "vendor",
}
SOURCE_PROFILE_BY_EXTENSION = {
    ".go": {
        "language": "go",
        "ecosystem": "go",
        "packageManager": "go",
        "analyzerId": "spec_harvester.go_public_api",
        "reason": "Go source evidence can feed deterministic Go public API analysis.",
    },
    ".py": {
        "language": "python",
        "ecosystem": "pypi",
        "packageManager": "python-packaging",
        "analyzerId": "spec_harvester.python_public_api",
        "reason": "Python source evidence can feed deterministic Python ast public API analysis.",
    },
    ".swift": {
        "language": "swift",
        "ecosystem": "swift-source",
        "packageManager": "none",
        "analyzerId": "spec_harvester.swift_public_api",
        "reason": "Swift source evidence can feed deterministic Swift public API analysis.",
    },
}
MARKDOWN_EXTENSIONS = {".md", ".markdown"}
PROJECT_PROFILE_MANIFEST_KINDS = {"package_manifest", "workspace_manifest"}
LICENSE_TEXT_HINTS = (
    ("MIT", ("permission is hereby granted", "copyright")),
    ("Apache-2.0", ("apache license", "version 2.0")),
)
SWIFT_PACKAGE_NAME_PATTERN = re.compile(r"\bPackage\s*\(\s*name\s*:\s*\"([^\"]+)\"")
SWIFT_PRODUCT_PATTERN = re.compile(
    r"\.(library|executable|plugin|macro)\s*\(\s*name\s*:\s*\"([^\"]+)\""
)


@dataclass(frozen=True)
class HarvestOptions:
    source: Path
    repository: str | None = None
    revision: str | None = None
    target: Path | None = None
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES


@dataclass(frozen=True)
class SourceTarget:
    root: Path
    path: str
    absolute: Path
    kind: str
    label: str

    def record(self) -> dict[str, str]:
        return {
            "kind": self.kind,
            "path": self.path,
            "label": self.label,
        }


@dataclass(frozen=True)
class ManifestDetector:
    language: str
    ecosystem: str
    package_manager: str
    parser: str
    reason: str
    kind: str = "package_manifest"
    confidence: str = "high"
    requires_package: bool = False


MANIFEST_DETECTORS_BY_NAME: dict[str, ManifestDetector] = {
    "package.json": ManifestDetector(
        language="javascript",
        ecosystem="npm",
        package_manager="npm",
        parser="spec_harvester.package_json",
        reason="package.json manifest parsed as npm package evidence.",
        requires_package=True,
    ),
    "package-lock.json": ManifestDetector(
        language="javascript",
        ecosystem="npm",
        package_manager="npm",
        parser="spec_harvester.manifest_path",
        reason="package-lock.json collected as npm lockfile evidence.",
    ),
    "npm-shrinkwrap.json": ManifestDetector(
        language="javascript",
        ecosystem="npm",
        package_manager="npm",
        parser="spec_harvester.manifest_path",
        reason="npm-shrinkwrap.json collected as npm lockfile evidence.",
    ),
    "pnpm-workspace.yaml": ManifestDetector(
        language="javascript",
        ecosystem="pnpm",
        package_manager="pnpm",
        parser="spec_harvester.manifest_path",
        reason="pnpm-workspace.yaml collected as pnpm workspace evidence.",
        kind="workspace_manifest",
    ),
    "pnpm-lock.yaml": ManifestDetector(
        language="javascript",
        ecosystem="pnpm",
        package_manager="pnpm",
        parser="spec_harvester.manifest_path",
        reason="pnpm-lock.yaml collected as pnpm lockfile evidence.",
    ),
    "yarn.lock": ManifestDetector(
        language="javascript",
        ecosystem="yarn",
        package_manager="yarn",
        parser="spec_harvester.manifest_path",
        reason="yarn.lock collected as Yarn lockfile evidence.",
    ),
    "bun.lock": ManifestDetector(
        language="javascript",
        ecosystem="bun",
        package_manager="bun",
        parser="spec_harvester.manifest_path",
        reason="bun.lock collected as Bun lockfile evidence.",
    ),
    "bun.lockb": ManifestDetector(
        language="javascript",
        ecosystem="bun",
        package_manager="bun",
        parser="spec_harvester.manifest_path",
        reason="bun.lockb collected as Bun lockfile evidence.",
    ),
    "pyproject.toml": ManifestDetector(
        language="python",
        ecosystem="pypi",
        package_manager="python-packaging",
        parser="spec_harvester.manifest_path",
        reason="pyproject.toml collected as Python packaging evidence.",
    ),
    "setup.py": ManifestDetector(
        language="python",
        ecosystem="pypi",
        package_manager="setuptools",
        parser="spec_harvester.manifest_path",
        reason="setup.py collected as setuptools evidence.",
    ),
    "setup.cfg": ManifestDetector(
        language="python",
        ecosystem="pypi",
        package_manager="setuptools",
        parser="spec_harvester.manifest_path",
        reason="setup.cfg collected as setuptools evidence.",
    ),
    "requirements.txt": ManifestDetector(
        language="python",
        ecosystem="pypi",
        package_manager="pip",
        parser="spec_harvester.manifest_path",
        reason="requirements.txt collected as pip dependency evidence.",
    ),
    "Package.swift": ManifestDetector(
        language="swift",
        ecosystem="swiftpm",
        package_manager="swiftpm",
        parser="spec_harvester.swift_package_manifest",
        reason="Package.swift manifest parsed as SwiftPM evidence.",
        requires_package=True,
    ),
    "Project.swift": ManifestDetector(
        language="swift",
        ecosystem="tuist",
        package_manager="tuist",
        parser="spec_harvester.manifest_path",
        reason="Project.swift collected as Tuist project manifest evidence.",
        confidence="medium",
    ),
    "Workspace.swift": ManifestDetector(
        language="swift",
        ecosystem="tuist",
        package_manager="tuist",
        parser="spec_harvester.manifest_path",
        reason="Workspace.swift collected as Tuist workspace manifest evidence.",
        kind="workspace_manifest",
        confidence="medium",
    ),
    "Tuist.swift": ManifestDetector(
        language="swift",
        ecosystem="tuist",
        package_manager="tuist",
        parser="spec_harvester.manifest_path",
        reason="Tuist.swift collected as Tuist configuration manifest evidence.",
        kind="workspace_manifest",
        confidence="medium",
    ),
    "pom.xml": ManifestDetector(
        language="java-kotlin",
        ecosystem="maven",
        package_manager="maven",
        parser="spec_harvester.manifest_path",
        reason="pom.xml collected as Maven project evidence.",
    ),
    "build.gradle": ManifestDetector(
        language="java-kotlin",
        ecosystem="gradle",
        package_manager="gradle",
        parser="spec_harvester.manifest_path",
        reason="build.gradle collected as Gradle project evidence.",
    ),
    "build.gradle.kts": ManifestDetector(
        language="java-kotlin",
        ecosystem="gradle",
        package_manager="gradle",
        parser="spec_harvester.manifest_path",
        reason="build.gradle.kts collected as Gradle Kotlin DSL project evidence.",
    ),
    "settings.gradle": ManifestDetector(
        language="java-kotlin",
        ecosystem="gradle",
        package_manager="gradle",
        parser="spec_harvester.manifest_path",
        reason="settings.gradle collected as Gradle workspace evidence.",
        kind="workspace_manifest",
    ),
    "settings.gradle.kts": ManifestDetector(
        language="java-kotlin",
        ecosystem="gradle",
        package_manager="gradle",
        parser="spec_harvester.manifest_path",
        reason="settings.gradle.kts collected as Gradle workspace evidence.",
        kind="workspace_manifest",
    ),
    "gradle.properties": ManifestDetector(
        language="java-kotlin",
        ecosystem="gradle",
        package_manager="gradle",
        parser="spec_harvester.manifest_path",
        reason="gradle.properties collected as Gradle project evidence.",
    ),
    "go.mod": ManifestDetector(
        language="go",
        ecosystem="go",
        package_manager="go",
        parser="spec_harvester.manifest_path",
        reason="go.mod collected as Go module evidence.",
    ),
    "composer.json": ManifestDetector(
        language="php",
        ecosystem="composer",
        package_manager="composer",
        parser="spec_harvester.manifest_path",
        reason="composer.json collected as Composer package evidence.",
    ),
    "composer.lock": ManifestDetector(
        language="php",
        ecosystem="composer",
        package_manager="composer",
        parser="spec_harvester.manifest_path",
        reason="composer.lock collected as Composer lockfile evidence.",
    ),
    "CMakeLists.txt": ManifestDetector(
        language="c-cpp",
        ecosystem="cmake",
        package_manager="cmake",
        parser="spec_harvester.manifest_path",
        reason="CMakeLists.txt collected as CMake project evidence.",
    ),
    "meson.build": ManifestDetector(
        language="c-cpp",
        ecosystem="meson",
        package_manager="meson",
        parser="spec_harvester.manifest_path",
        reason="meson.build collected as Meson project evidence.",
    ),
    "configure.ac": ManifestDetector(
        language="c-cpp",
        ecosystem="autotools",
        package_manager="autotools",
        parser="spec_harvester.manifest_path",
        reason="configure.ac collected as Autotools project evidence.",
    ),
    "configure.in": ManifestDetector(
        language="c-cpp",
        ecosystem="autotools",
        package_manager="autotools",
        parser="spec_harvester.manifest_path",
        reason="configure.in collected as Autotools project evidence.",
    ),
    "Makefile": ManifestDetector(
        language="c-cpp",
        ecosystem="make",
        package_manager="make",
        parser="spec_harvester.manifest_path",
        reason="Makefile collected as ambiguous make project evidence.",
        confidence="low",
    ),
    "conanfile.txt": ManifestDetector(
        language="c-cpp",
        ecosystem="conan",
        package_manager="conan",
        parser="spec_harvester.manifest_path",
        reason="conanfile.txt collected as Conan package evidence.",
    ),
    "conanfile.py": ManifestDetector(
        language="c-cpp",
        ecosystem="conan",
        package_manager="conan",
        parser="spec_harvester.manifest_path",
        reason="conanfile.py collected as Conan package evidence.",
    ),
    "vcpkg.json": ManifestDetector(
        language="c-cpp",
        ecosystem="vcpkg",
        package_manager="vcpkg",
        parser="spec_harvester.manifest_path",
        reason="vcpkg.json collected as vcpkg package evidence.",
    ),
    "Podfile": ManifestDetector(
        language="objective-c",
        ecosystem="cocoapods",
        package_manager="cocoapods",
        parser="spec_harvester.manifest_path",
        reason="Podfile collected as CocoaPods project evidence.",
    ),
    "Podfile.lock": ManifestDetector(
        language="objective-c",
        ecosystem="cocoapods",
        package_manager="cocoapods",
        parser="spec_harvester.manifest_path",
        reason="Podfile.lock collected as CocoaPods lockfile evidence.",
    ),
    "Gemfile": ManifestDetector(
        language="ruby",
        ecosystem="bundler",
        package_manager="bundler",
        parser="spec_harvester.manifest_path",
        reason="Gemfile collected as Bundler dependency evidence.",
    ),
    "Gemfile.lock": ManifestDetector(
        language="ruby",
        ecosystem="bundler",
        package_manager="bundler",
        parser="spec_harvester.manifest_path",
        reason="Gemfile.lock collected as Bundler lockfile evidence.",
    ),
    "Cargo.toml": ManifestDetector(
        language="rust",
        ecosystem="cargo",
        package_manager="cargo",
        parser="spec_harvester.manifest_path",
        reason="Cargo.toml collected as Cargo package evidence.",
    ),
    "Cargo.lock": ManifestDetector(
        language="rust",
        ecosystem="cargo",
        package_manager="cargo",
        parser="spec_harvester.manifest_path",
        reason="Cargo.lock collected as Cargo lockfile evidence.",
    ),
}

GEMSPEC_DETECTOR = ManifestDetector(
    language="ruby",
    ecosystem="rubygems",
    package_manager="rubygems",
    parser="spec_harvester.manifest_path",
    reason="*.gemspec collected as RubyGems package evidence.",
)
XCODEPROJ_DETECTOR = ManifestDetector(
    language="objective-c",
    ecosystem="xcode",
    package_manager="xcodebuild",
    parser="spec_harvester.manifest_path",
    reason="*.xcodeproj/project.pbxproj collected as Xcode project evidence.",
)
XCWORKSPACE_DETECTOR = ManifestDetector(
    language="objective-c",
    ecosystem="xcode",
    package_manager="xcodebuild",
    parser="spec_harvester.manifest_path",
    reason="*.xcworkspace workspace metadata collected as Xcode workspace evidence.",
    kind="workspace_manifest",
)


def collect_local_repository(options: HarvestOptions) -> dict[str, Any]:
    target = resolve_source_target(options)

    files: list[dict[str, Any]] = []
    skipped_files: list[dict[str, Any]] = []
    for path in candidate_files_for_target(target):
        rel = path.relative_to(target.root).as_posix()
        resolved_path = path.resolve()
        if not is_inside(target.root, resolved_path):
            skipped_files.append(
                {
                    "path": rel,
                    "reason": "path_outside_source",
                }
            )
            continue
        if path.is_symlink():
            skipped_files.append(
                {
                    "path": rel,
                    "reason": "symlink_unsupported",
                }
            )
            continue
        if not path.is_file():
            skipped_files.append(
                {
                    "path": rel,
                    "reason": "not_regular_file",
                }
            )
            continue
        stat = path.stat()
        if stat.st_size > options.max_file_bytes:
            skipped_files.append(
                {
                    "path": rel,
                    "reason": "file_too_large",
                    "size": stat.st_size,
                    "maxFileBytes": options.max_file_bytes,
                }
            )
            continue
        files.append(collect_file(target.root, path))

    files.sort(key=lambda item: item["path"])
    skipped_files.sort(key=lambda item: item["path"])
    return {
        "schemaVersion": SNAPSHOT_SCHEMA_VERSION,
        "kind": SNAPSHOT_KIND,
        "source": {
            "kind": "local_checkout",
            "label": target.root.name,
            "repository": options.repository,
            "revision": options.revision,
            "target": target.record(),
        },
        "policy": {
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "contentAuthority": "untrusted_metadata",
        },
        "analyzerPolicy": default_analyzer_trust_policy(),
        "classifierPolicy": default_classifier_policy(),
        "projectProfile": build_project_profile(
            files,
            source=target.root,
            target_root=target.absolute,
        ),
        "files": files,
        "skippedFiles": skipped_files,
        "summary": {
            "targetKind": target.kind,
            "fileCount": len(files),
            "skippedFileCount": len(skipped_files),
            "packageManifestCount": sum(1 for item in files if item["kind"] == "package_manifest"),
            "licenseFileCount": sum(1 for item in files if item["kind"] == "license"),
        },
    }


def resolve_source_target(options: HarvestOptions) -> SourceTarget:
    source = options.source.resolve()
    if options.target is None:
        if source.is_dir():
            return SourceTarget(
                root=source,
                path=".",
                absolute=source,
                kind="repository",
                label=source.name,
            )
        if source.is_file():
            return SourceTarget(
                root=source.parent,
                path=source.name,
                absolute=source,
                kind="file",
                label=source.stem or source.name,
            )
        raise ValueError(f"Source target does not exist: {source}")

    if not source.exists() or not source.is_dir():
        raise ValueError(f"Source root does not exist or is not a directory: {source}")
    target_path = options.target
    if target_path.is_absolute():
        raise ValueError("Source target path must be relative to the source root")
    target_relative = normalize_target_path(target_path)
    target_absolute = (source / target_relative).resolve()
    if not is_inside(source, target_absolute):
        raise ValueError("Source target path must stay inside the source root")
    if not target_absolute.exists():
        raise ValueError(f"Source target does not exist: {target_absolute}")
    if target_absolute.is_dir():
        kind = "repository" if target_relative == "." else "folder"
        label = target_absolute.name
    elif target_absolute.is_file():
        kind = "file"
        label = target_absolute.stem or target_absolute.name
    else:
        raise ValueError(f"Source target is not a regular file or directory: {target_absolute}")
    return SourceTarget(
        root=source,
        path=target_relative,
        absolute=target_absolute,
        kind=kind,
        label=label,
    )


def normalize_target_path(path: Path) -> str:
    text = path.as_posix().strip()
    if not text or text == ".":
        return "."
    target_path = Path(text)
    if any(part == ".." for part in target_path.parts):
        raise ValueError("Source target path must not contain '..' segments")
    return target_path.as_posix()


def build_project_profile(
    files: list[dict[str, Any]], *, source: Path | None = None, target_root: Path | None = None
) -> dict[str, Any]:
    languages: dict[str, dict[str, Any]] = {}
    ecosystems: dict[str, dict[str, Any]] = {}
    analyzer_plan: dict[str, dict[str, Any]] = {}
    manifests: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for item in files:
        if item.get("kind") not in PROJECT_PROFILE_MANIFEST_KINDS:
            continue
        manifest = project_manifest_entry(item)
        if manifest is None:
            diagnostics.append(
                {
                    "id": "unsupported_package_manifest",
                    "level": "info",
                    "message": (
                        "Package manifest is collected but not yet mapped into ProjectProfile."
                    ),
                    "path": item.get("path"),
                }
            )
            continue
        manifests.append(manifest)
        merge_profile_evidence(
            languages,
            manifest["language"],
            manifest["confidence"],
            manifest["reason"],
            manifest["path"],
        )
        merge_profile_evidence(
            ecosystems,
            manifest["ecosystem"],
            manifest["confidence"],
            manifest["reason"],
            manifest["path"],
            extra={
                "language": manifest["language"],
                "packageManager": manifest["packageManager"],
            },
        )
        plan = analyzer_plan_entry(manifest, source=source)
        if plan is not None:
            merge_analyzer_plan(analyzer_plan, plan)

    for source_entry in source_profile_entries(files):
        merge_profile_evidence(
            languages,
            source_entry["language"],
            "low",
            source_entry["reason"],
            source_entry["path"],
        )
        merge_profile_evidence(
            ecosystems,
            source_entry["ecosystem"],
            "low",
            source_entry["reason"],
            source_entry["path"],
            extra={
                "language": source_entry["language"],
                "packageManager": source_entry["packageManager"],
            },
        )
        plan = source_analyzer_plan_entry(source_entry, source=target_root)
        if plan is not None:
            merge_analyzer_plan(analyzer_plan, plan)

    if not manifests and not analyzer_plan:
        diagnostics.append(
            {
                "id": "no_supported_package_manifest",
                "level": "info",
                "message": "No supported package manifest evidence was found for ProjectProfile.",
            }
        )

    return {
        "schemaVersion": PROJECT_PROFILE_SCHEMA_VERSION,
        "languages": sorted_profile_entries(languages),
        "ecosystems": sorted_profile_entries(ecosystems),
        "manifests": sorted(manifests, key=lambda item: item["path"]),
        "analyzerPlan": sorted(analyzer_plan.values(), key=lambda item: item["id"]),
        "diagnostics": sorted(
            diagnostics, key=lambda item: (item["id"], str(item.get("path", "")))
        ),
    }


def project_manifest_entry(item: dict[str, Any]) -> dict[str, Any] | None:
    path = str(item.get("path") or "")
    detector = manifest_detector_for_path(path)
    if detector is None:
        return None
    if detector.requires_package and not isinstance(item.get("package"), dict):
        return None
    sha256 = item.get("sha256")
    return {
        "path": path,
        "kind": detector.kind,
        "language": detector.language,
        "ecosystem": detector.ecosystem,
        "packageManager": detector.package_manager,
        "confidence": detector.confidence,
        "reason": detector.reason,
        "sha256": sha256,
        "parser": detector.parser,
    }


def source_profile_entries(files: list[dict[str, Any]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in files:
        if item.get("kind") != "source_entrypoint":
            continue
        path = item.get("path")
        if not isinstance(path, str):
            continue
        profile = SOURCE_PROFILE_BY_EXTENSION.get(Path(path).suffix.lower())
        if profile is None:
            continue
        key = (profile["language"], path)
        if key in seen:
            continue
        seen.add(key)
        entries.append(
            {
                "path": path,
                "language": profile["language"],
                "ecosystem": profile["ecosystem"],
                "packageManager": profile["packageManager"],
                "analyzerId": profile["analyzerId"],
                "reason": profile["reason"],
            }
        )
    return sorted(entries, key=lambda item: (item["language"], item["path"]))


def manifest_detector_for_path(path: str) -> ManifestDetector | None:
    path_obj = Path(path)
    detector = MANIFEST_DETECTORS_BY_NAME.get(path_obj.name)
    if detector is not None:
        return detector
    if path_obj.name.endswith(".gemspec"):
        return GEMSPEC_DETECTOR
    if path.endswith(".xcodeproj/project.pbxproj"):
        return XCODEPROJ_DETECTOR
    if path.endswith(".xcworkspace/contents.xcworkspacedata"):
        return XCWORKSPACE_DETECTOR
    return None


def merge_profile_evidence(
    entries: dict[str, dict[str, Any]],
    entry_id: str,
    confidence: str,
    reason: str,
    path: str,
    *,
    extra: dict[str, Any] | None = None,
) -> None:
    entry = entries.setdefault(
        entry_id,
        {
            "id": entry_id,
            "confidence": confidence,
            "reason": reason,
            "evidencePaths": [],
            **(extra or {}),
        },
    )
    if CONFIDENCE_RANK.get(confidence, -1) > CONFIDENCE_RANK.get(entry["confidence"], -1):
        entry["confidence"] = confidence
        entry["reason"] = reason
    if path not in entry["evidencePaths"]:
        entry["evidencePaths"].append(path)
        entry["evidencePaths"].sort()


def sorted_profile_entries(entries: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(entries.values(), key=lambda item: item["id"])


def analyzer_plan_entry(
    manifest: dict[str, Any], *, source: Path | None = None
) -> dict[str, Any] | None:
    if manifest["language"] == "javascript":
        return {
            "id": "spec_harvester.js_ts_public_api",
            "language": "javascript",
            "ecosystem": "npm",
            "status": "recommended",
            "reason": "package.json evidence can feed JavaScript/TypeScript export analysis.",
            "evidencePaths": [manifest["path"]],
        }
    if manifest["language"] == "swift":
        if source is not None and not has_swift_source_for_manifest(source, manifest["path"]):
            reason = (
                "Package.swift evidence is available, but no Swift source files were found."
                if manifest["ecosystem"] == "swiftpm"
                else "Swift manifest evidence is available, but no Swift source files were found."
            )
            return {
                "id": "spec_harvester.swift_public_api",
                "language": "swift",
                "ecosystem": manifest["ecosystem"],
                "status": "manifest_only",
                "reason": reason,
                "evidencePaths": [manifest["path"]],
            }
        reason = (
            "Package.swift evidence can feed deterministic Swift source public API analysis."
            if manifest["ecosystem"] == "swiftpm"
            else "Swift manifest evidence can feed deterministic Swift source public API analysis."
        )
        return {
            "id": "spec_harvester.swift_public_api",
            "language": "swift",
            "ecosystem": manifest["ecosystem"],
            "status": "recommended",
            "reason": reason,
            "evidencePaths": [manifest["path"]],
        }
    if manifest["language"] == "python":
        return {
            "id": "spec_harvester.python_public_api",
            "language": "python",
            "ecosystem": manifest["ecosystem"],
            "status": "recommended",
            "reason": "Python packaging evidence can feed Python ast public API analysis.",
            "evidencePaths": [manifest["path"]],
        }
    if manifest["language"] == "go":
        if source is not None and not has_go_source_for_manifest(source, manifest["path"]):
            return {
                "id": "spec_harvester.go_public_api",
                "language": "go",
                "ecosystem": "go",
                "status": "manifest_only",
                "reason": (
                    "go.mod evidence is available, but no non-generated Go source files were found."
                ),
                "evidencePaths": [manifest["path"]],
            }
        return {
            "id": "spec_harvester.go_public_api",
            "language": "go",
            "ecosystem": "go",
            "status": "recommended",
            "reason": "go.mod evidence can feed deterministic Go source public API analysis.",
            "evidencePaths": [manifest["path"]],
        }
    analyzer_id = f"spec_harvester.{manifest['language'].replace('-', '_')}_manifest_profile"
    return {
        "id": analyzer_id,
        "language": manifest["language"],
        "ecosystem": manifest["ecosystem"],
        "status": "manifest_only",
        "reason": (
            f"{manifest['ecosystem']} manifest evidence is available; no static public API "
            "analyzer is configured yet."
        ),
        "evidencePaths": [manifest["path"]],
    }


def source_analyzer_plan_entry(
    source_entry: dict[str, str], *, source: Path | None = None
) -> dict[str, Any] | None:
    analyzer_id = source_entry["analyzerId"]
    language = source_entry["language"]
    if source is not None and not source.is_dir() and not source.is_file():
        return None
    if language == "swift" and source is not None and not swift_source_files(source):
        return None
    if language == "go" and source is not None and not go_source_files(source):
        return None
    return {
        "id": analyzer_id,
        "language": language,
        "ecosystem": source_entry["ecosystem"],
        "status": "recommended",
        "reason": source_entry["reason"],
        "evidencePaths": [source_entry["path"]],
    }


def has_go_source_for_manifest(source: Path, manifest_path: str) -> bool:
    manifest_root = (source / manifest_path).parent
    if not manifest_root.exists() or not manifest_root.is_dir():
        return False
    return bool(go_source_files(manifest_root))


def has_swift_source_for_manifest(source: Path, manifest_path: str) -> bool:
    manifest_root = (source / manifest_path).parent
    if not manifest_root.exists() or not manifest_root.is_dir():
        return False
    return bool(swift_source_files(manifest_root))


def merge_analyzer_plan(
    entries: dict[str, dict[str, Any]],
    plan: dict[str, Any],
) -> None:
    entry = entries.setdefault(plan["id"], {**plan, "evidencePaths": []})
    for path in plan["evidencePaths"]:
        if path not in entry["evidencePaths"]:
            entry["evidencePaths"].append(path)
            entry["evidencePaths"].sort()


def default_analyzer_trust_policy() -> dict[str, Any]:
    return {
        "schemaVersion": ANALYZER_TRUST_POLICY_SCHEMA_VERSION,
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


def candidate_files(root: Path) -> list[Path]:
    seen: dict[str, Path] = {}
    for relative in ROOT_FILES:
        path = root / relative
        if path.exists():
            seen[path.resolve().as_posix()] = path
    for path in root.iterdir():
        if path.exists() and is_license_filename(path):
            seen[path.resolve().as_posix()] = path
    for pattern in SAFE_GLOBS:
        for path in root.glob(pattern):
            if path.exists():
                seen[path.resolve().as_posix()] = path
    for path in nested_swift_package_manifests(root):
        seen[path.resolve().as_posix()] = path
    return list(seen.values())


def candidate_files_for_target(target: SourceTarget) -> list[Path]:
    seen: dict[str, Path] = {}

    def add(path: Path) -> None:
        if path.exists():
            seen[path.absolute().as_posix()] = path

    if target.kind == "repository":
        for path in candidate_files(target.root):
            add(path)
    elif target.kind == "file":
        add(target.absolute)
        for path in root_license_files(target.root):
            add(path)
    else:
        for path in candidate_files(target.absolute):
            add(path)
        for path in target_source_files(target.absolute):
            add(path)
        for path in root_license_files(target.root):
            add(path)

    return sorted(seen.values(), key=lambda item: item.relative_to(target.root).as_posix())


def root_license_files(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return sorted(
        (path for path in root.iterdir() if path.exists() and is_license_filename(path)),
        key=lambda item: item.name,
    )


def target_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    if not root.exists() or not root.is_dir():
        return files
    for current_root, dirs, filenames in os.walk(root, followlinks=False):
        current = Path(current_root)
        dirs[:] = [
            dirname
            for dirname in sorted(dirs)
            if not should_skip_source_directory(current / dirname)
        ]
        for filename in sorted(filenames):
            path = current / filename
            if should_skip_source_file(path, root):
                continue
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def should_skip_source_directory(path: Path) -> bool:
    return path.is_symlink() or path.name.startswith(".") or path.name in IGNORED_SOURCE_DIRS


def should_skip_source_file(path: Path, root: Path) -> bool:
    if path.suffix.lower() not in SOURCE_FILE_EXTENSIONS:
        return True
    if path.is_symlink() or not path.is_file():
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part.startswith(".") or part in IGNORED_SOURCE_DIRS for part in relative.parts[:-1])


def nested_swift_package_manifests(root: Path) -> list[Path]:
    manifests: list[Path] = []
    for current_root, dirs, filenames in os.walk(root):
        dirs[:] = [
            name
            for name in sorted(dirs)
            if not (name.startswith(".") or name in IGNORED_NESTED_SWIFT_MANIFEST_DIRS)
        ]
        for filename in sorted(filenames):
            if filename != "Package.swift":
                continue
            path = Path(current_root, filename)
            if not path.exists():
                continue
            relative = path.relative_to(root)
            if len(relative.parts) == 1:
                continue
            parent_parts = relative.parts[:-1]
            if any(part.startswith(".") for part in parent_parts):
                continue
            manifests.append(path)
    return manifests


def is_inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def collect_file(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    relative = path.relative_to(root).as_posix()
    record: dict[str, Any] = {
        "path": relative,
        "kind": classify_file(path),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }

    text = decode_text(data)
    if text is None:
        return record

    if path.suffix.lower() in MARKDOWN_EXTENSIONS or path.name.upper().startswith("README"):
        headings = markdown_headings(text)
        if headings:
            record["headings"] = headings
        semantic_hints = markdown_semantic_hints(text)
        if semantic_hints:
            record["semanticHints"] = semantic_hints

    if path.name == "package.json":
        package = parse_package_json(text)
        if package is not None:
            record["package"] = package
    elif path.name == "Package.swift":
        package = parse_swift_package_manifest(text)
        if package:
            record["package"] = package
    elif path.name in {"Project.swift", "Workspace.swift", "Tuist.swift"}:
        package = parse_tuist_manifest(text, filename=path.name)
        if package:
            record["package"] = package
    elif is_license_filename(path):
        license_hint = infer_license_hint(text)
        if license_hint is not None:
            record["licenseHint"] = license_hint

    return record


def infer_license_hint(text: str) -> str | None:
    normalized = re.sub(r"\s+", " ", text.lower())
    for license_name, requirements in LICENSE_TEXT_HINTS:
        if all(requirement in normalized for requirement in requirements):
            return license_name
    return None


def classify_file(path: Path) -> str:
    detector = manifest_detector_for_path(path.as_posix())
    if detector is not None:
        return detector.kind
    path_text = path.as_posix()
    if path.name.lower().startswith("readme") or (
        path.suffix.lower() in MARKDOWN_EXTENSIONS
        and (
            "/Documentation.docc/" in path_text
            or "/SPECS/PRD/" in path_text
            or "/docs/" in path_text
        )
    ):
        return "documentation"
    if is_license_filename(path):
        return "license"
    if path.suffix in {".yml", ".yaml"} and ".github/workflows" in path.as_posix():
        return "workflow"
    if path.name == "turbo.json":
        return "workspace_manifest"
    if path.name.startswith("index.") or path.suffix.lower() in SOURCE_FILE_EXTENSIONS:
        return "source_entrypoint"
    return "metadata"


def decode_text(data: bytes) -> str | None:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def markdown_headings(text: str, limit: int = 30) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        heading = match.group(2).strip()
        if heading:
            headings.append(heading[:160])
        if len(headings) >= limit:
            break
    return headings


def markdown_semantic_hints(text: str, limit: int = 40) -> list[str]:
    normalized = re.sub(r"\s+", " ", text.lower())
    hints = [
        term
        for term in SEMANTIC_KEYWORD_TAXONOMY.markdown_hint_terms()
        if semantic_term_matches(normalized, term)
    ]
    return hints[:limit]


def semantic_term_matches(normalized_text: str, term: str) -> bool:
    if " " in term or "-" in term:
        return term in normalized_text
    return re.search(rf"\b{re.escape(term)}\b", normalized_text) is not None


def parse_package_json(text: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None

    package: dict[str, Any] = {}
    for key in ("name", "version", "description", "license", "type"):
        value = payload.get(key)
        if isinstance(value, str):
            package[key] = value

    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        value = payload.get(key)
        if isinstance(value, dict):
            package[key] = sorted(str(item) for item in value.keys())

    scripts = payload.get("scripts")
    if isinstance(scripts, dict):
        package["scripts"] = sorted(str(item) for item in scripts.keys())

    exports = payload.get("exports")
    if isinstance(exports, dict):
        package["exports"] = sorted(str(item) for item in exports.keys())
    elif isinstance(exports, str):
        package["exports"] = ["."]

    return package


def parse_swift_package_manifest(text: str) -> dict[str, Any] | None:
    package: dict[str, Any] = {
        "ecosystem": "swift",
        "language": "swift",
    }

    uncommented_text = strip_swift_comments(text)

    name_match = SWIFT_PACKAGE_NAME_PATTERN.search(uncommented_text)
    if name_match is not None:
        package["name"] = name_match.group(1)

    products = [
        {"type": product_type, "name": product_name}
        for product_type, product_name in SWIFT_PRODUCT_PATTERN.findall(uncommented_text)
    ]
    if products:
        package["products"] = sorted(products, key=lambda item: (item["type"], item["name"]))

    if "name" not in package and not products:
        return None
    return package
