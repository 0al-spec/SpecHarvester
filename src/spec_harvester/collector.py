from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SNAPSHOT_KIND = "SpecHarvesterEvidenceSnapshot"
SNAPSHOT_SCHEMA_VERSION = 1
DEFAULT_MAX_FILE_BYTES = 512 * 1024

ROOT_FILES = [
    "README.md",
    "README",
    "LICENSE",
    "LICENSE.md",
    "COPYING",
    "package.json",
    "pyproject.toml",
    "Package.swift",
    "pnpm-workspace.yaml",
    "turbo.json",
    "Cargo.toml",
    "go.mod",
]

SAFE_GLOBS = [
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "packages/*/README.md",
    "packages/*/package.json",
    "packages/*/src/index.ts",
    "packages/*/src/index.tsx",
    "packages/*/src/index.js",
    "apps/*/package.json",
    "examples/README.md",
]

MARKDOWN_EXTENSIONS = {".md", ".markdown"}
PACKAGE_MANIFEST_NAMES = {"package.json"}


@dataclass(frozen=True)
class HarvestOptions:
    source: Path
    repository: str | None = None
    revision: str | None = None
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES


def collect_local_repository(options: HarvestOptions) -> dict[str, Any]:
    source = options.source.resolve()
    if not source.exists() or not source.is_dir():
        raise ValueError(f"Source repository does not exist or is not a directory: {source}")

    files: list[dict[str, Any]] = []
    skipped_files: list[dict[str, Any]] = []
    for path in candidate_files(source):
        rel = path.relative_to(source).as_posix()
        resolved_path = path.resolve()
        if not is_inside(source, resolved_path):
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
        files.append(collect_file(source, path))

    files.sort(key=lambda item: item["path"])
    skipped_files.sort(key=lambda item: item["path"])
    return {
        "schemaVersion": SNAPSHOT_SCHEMA_VERSION,
        "kind": SNAPSHOT_KIND,
        "source": {
            "kind": "local_checkout",
            "label": source.name,
            "repository": options.repository,
            "revision": options.revision,
        },
        "policy": {
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "contentAuthority": "untrusted_metadata",
        },
        "files": files,
        "skippedFiles": skipped_files,
        "summary": {
            "fileCount": len(files),
            "skippedFileCount": len(skipped_files),
            "packageManifestCount": sum(1 for item in files if item["kind"] == "package_manifest"),
        },
    }


def candidate_files(root: Path) -> list[Path]:
    seen: dict[str, Path] = {}
    for relative in ROOT_FILES:
        path = root / relative
        if path.exists():
            seen[path.resolve().as_posix()] = path
    for pattern in SAFE_GLOBS:
        for path in root.glob(pattern):
            if path.exists():
                seen[path.resolve().as_posix()] = path
    return list(seen.values())


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

    if path.name in PACKAGE_MANIFEST_NAMES:
        package = parse_package_json(text)
        if package:
            record["package"] = package

    return record


def classify_file(path: Path) -> str:
    if path.name in PACKAGE_MANIFEST_NAMES:
        return "package_manifest"
    if path.name.lower().startswith("readme"):
        return "documentation"
    if path.name.lower().startswith(("license", "copying")):
        return "license"
    if path.suffix in {".yml", ".yaml"} and ".github/workflows" in path.as_posix():
        return "workflow"
    if path.name in {"pyproject.toml", "Package.swift", "Cargo.toml", "go.mod"}:
        return "package_manifest"
    if path.name in {"pnpm-workspace.yaml", "turbo.json"}:
        return "workspace_manifest"
    if path.name.startswith("index."):
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
