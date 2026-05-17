from __future__ import annotations

import hashlib
import json
import re
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from spec_harvester.interface_index import (
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    validate_public_interface_index,
)

JS_TS_PUBLIC_API_ANALYZER_ID = "js-ts-manifest-export-analyzer"
JS_TS_PUBLIC_API_ANALYZER_VERSION = "0.1.0"

IGNORED_MANIFEST_DIR_NAMES = {
    ".cache",
    ".git",
    ".hg",
    ".next",
    ".npm",
    ".nuxt",
    ".pnpm-store",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
    ".turbo",
    ".yarn",
    "coverage",
    "dist",
    "node_modules",
    "temp",
    "tmp",
}

JS_TS_EXTENSIONS = {
    ".cjs",
    ".cts",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".ts",
    ".tsx",
}

EXPORT_DECLARATION_RE = re.compile(
    r"^\s*export\s+"
    r"(?:(?P<default>default)\s+)?"
    r"(?:(?P<async>async)\s+)?"
    r"(?:(?P<kind>function|class|interface|type|enum)\b"
    r"(?:\s+(?P<name>[A-Za-z_$][\w$]*))?"
    r"(?:\s*\((?P<params>[^)]*)\))?"
    r"|(?P<var_kind>const|let|var)\s+(?P<vars>[^;\n]+))",
    re.MULTILINE,
)
NAMED_EXPORT_RE = re.compile(
    r"^\s*export\s+(?P<type_only>type\s+)?\{(?P<specifiers>[^}]+)\}",
    re.MULTILINE | re.DOTALL,
)
LINE_COMMENT_RE = re.compile(r"//.*?$", re.MULTILINE)
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def analyze_js_ts_public_api(
    source: Path,
    *,
    package_id: str | None = None,
    source_revision: str | None = None,
) -> dict[str, Any]:
    root = source.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(
            f"JavaScript/TypeScript source root does not exist or is not a directory: {source}"
        )

    packages: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for manifest_path in package_manifest_files(root):
        package_record = analyze_package_manifest(
            root,
            manifest_path,
            package_id=package_id,
            diagnostics=diagnostics,
        )
        if package_record is not None:
            packages.append(package_record)

    index = new_public_interface_index(
        source_revision=source_revision,
        analyzers=[
            analyzer_record(
                JS_TS_PUBLIC_API_ANALYZER_ID,
                JS_TS_PUBLIC_API_ANALYZER_VERSION,
                execution="none",
                confidence="medium",
            )
        ],
        packages=packages,
        diagnostics=diagnostics,
    )
    validate_public_interface_index(index)
    return index


def package_manifest_files(root: Path) -> list[Path]:
    manifests: list[Path] = []
    for path in root.rglob("package.json"):
        if should_skip_manifest(path, root):
            continue
        manifests.append(path)
    return sorted(manifests, key=lambda item: item.relative_to(root).as_posix())


def should_skip_manifest(path: Path, root: Path) -> bool:
    if path.is_symlink() or not path.is_file():
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in IGNORED_MANIFEST_DIR_NAMES for part in relative.parts[:-1])


def analyze_package_manifest(
    root: Path,
    manifest_path: Path,
    *,
    package_id: str | None,
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any] | None:
    relative_manifest = manifest_path.relative_to(root).as_posix()
    data = manifest_path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    try:
        manifest = json.loads(data.decode("utf-8", errors="replace"))
    except JSONDecodeError as exc:
        diagnostics.append(
            {
                "level": "error",
                "path": relative_manifest,
                "message": f"Invalid package.json: {exc.msg} at line {exc.lineno}",
                "evidence": evidence_record(relative_manifest, digest),
            }
        )
        return None

    if not isinstance(manifest, dict):
        diagnostics.append(
            {
                "level": "error",
                "path": relative_manifest,
                "message": "Invalid package.json: expected object",
                "evidence": evidence_record(relative_manifest, digest),
            }
        )
        return None

    package_root = manifest_path.parent
    entrypoints = package_entrypoints(
        root,
        package_root,
        manifest,
        relative_manifest,
        digest,
        diagnostics,
    )
    package_path = package_root.relative_to(root).as_posix()
    if package_path == "":
        package_path = "."
    return {
        "id": package_id or manifest_package_id(manifest, package_root),
        "path": package_path,
        "language": "javascript-typescript",
        "entrypoints": entrypoints,
    }


def manifest_package_id(manifest: dict[str, Any], package_root: Path) -> str:
    name = manifest.get("name")
    if isinstance(name, str) and name.strip():
        return name
    return package_root.name


def package_entrypoints(
    root: Path,
    package_root: Path,
    manifest: dict[str, Any],
    manifest_path: str,
    manifest_digest: str,
    diagnostics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    entrypoint_paths: dict[str, Path] = {}
    for target in manifest_entrypoint_targets(manifest):
        entrypoint_path = resolve_manifest_target(root, package_root, target)
        if entrypoint_path is None:
            continue
        relative = entrypoint_path.relative_to(root).as_posix()
        if not entrypoint_path.exists() or not entrypoint_path.is_file():
            diagnostics.append(
                {
                    "level": "warning",
                    "path": relative,
                    "message": f"Manifest entrypoint does not exist: {target}",
                    "evidence": evidence_record(manifest_path, manifest_digest),
                }
            )
            continue
        if entrypoint_path.suffix not in JS_TS_EXTENSIONS and not entrypoint_path.name.endswith(
            ".d.ts"
        ):
            continue
        entrypoint_paths[relative] = entrypoint_path

    return [
        source_entrypoint(root, entrypoint_paths[relative]) for relative in sorted(entrypoint_paths)
    ]


def manifest_entrypoint_targets(manifest: dict[str, Any]) -> list[str]:
    targets: list[str] = []
    for key in ("main", "module", "types", "typings"):
        value = manifest.get(key)
        if isinstance(value, str):
            targets.append(value)
    targets.extend(exports_targets(manifest.get("exports")))
    targets.extend(bin_targets(manifest.get("bin")))
    return targets


def exports_targets(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [target for item in value for target in exports_targets(item)]
    if isinstance(value, dict):
        return [target for key in sorted(value) for target in exports_targets(value[key])]
    return []


def bin_targets(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [value[key] for key in sorted(value) if isinstance(value[key], str)]
    return []


def resolve_manifest_target(root: Path, package_root: Path, target: str) -> Path | None:
    if "://" in target or target.startswith("#"):
        return None
    clean_target = target.split("?", 1)[0].split("#", 1)[0]
    if not clean_target:
        return None
    candidate = (package_root / clean_target).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    if candidate.is_symlink():
        return None
    return candidate


def source_entrypoint(root: Path, path: Path) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    text = data.decode("utf-8", errors="replace")
    return {
        "path": relative,
        "symbols": source_symbols(text, relative, digest),
    }


def source_symbols(text: str, path: str, digest: str) -> list[dict[str, Any]]:
    clean_text = strip_comments(text)
    symbols: dict[str, dict[str, Any]] = {}
    for match in EXPORT_DECLARATION_RE.finditer(clean_text):
        for symbol in declaration_symbols(match, path, digest):
            symbols[symbol["name"]] = symbol
    for match in NAMED_EXPORT_RE.finditer(clean_text):
        for symbol in named_export_symbols(match, path, digest):
            symbols[symbol["name"]] = symbol
    return [symbols[name] for name in sorted(symbols)]


def strip_comments(text: str) -> str:
    without_blocks = BLOCK_COMMENT_RE.sub("", text)
    return LINE_COMMENT_RE.sub("", without_blocks)


def declaration_symbols(
    match: re.Match[str],
    path: str,
    digest: str,
) -> list[dict[str, Any]]:
    default_export = match.group("default") is not None
    kind = match.group("kind")
    if kind is not None:
        symbol_kind = export_kind(kind)
        name = "default" if default_export else match.group("name")
        if name is None:
            name = "default"
        symbol = base_symbol(name, symbol_kind, path, digest)
        if symbol_kind == "function":
            params = normalize_params(match.group("params") or "")
            symbol["signature"] = f"{name}({params})"
        return [symbol]

    var_kind = match.group("var_kind")
    vars_text = match.group("vars")
    if var_kind is None or vars_text is None:
        return []
    symbol_kind = "constant" if var_kind == "const" else "variable"
    return [base_symbol(name, symbol_kind, path, digest) for name in variable_names(vars_text)]


def export_kind(kind: str) -> str:
    if kind == "function":
        return "function"
    if kind == "class":
        return "class"
    if kind == "interface":
        return "interface"
    if kind == "type":
        return "type"
    if kind == "enum":
        return "enum"
    return "unknown"


def variable_names(vars_text: str) -> list[str]:
    names: list[str] = []
    for match in re.finditer(r"(?:^|,)\s*([A-Za-z_$][\w$]*)\b", vars_text):
        names.append(match.group(1))
    return names


def named_export_symbols(
    match: re.Match[str],
    path: str,
    digest: str,
) -> list[dict[str, Any]]:
    type_only = match.group("type_only") is not None
    symbols: list[dict[str, Any]] = []
    for raw_specifier in match.group("specifiers").split(","):
        specifier = raw_specifier.strip()
        if not specifier:
            continue
        specifier_type_only = type_only or specifier.startswith("type ")
        if specifier_type_only and specifier.startswith("type "):
            specifier = specifier.removeprefix("type ").strip()
        export_name = exported_specifier_name(specifier)
        if export_name is None:
            continue
        kind = "type" if specifier_type_only else "unknown"
        symbols.append(base_symbol(export_name, kind, path, digest))
    return symbols


def exported_specifier_name(specifier: str) -> str | None:
    parts = re.split(r"\s+as\s+", specifier)
    name = parts[-1].strip()
    if not re.match(r"^[A-Za-z_$][\w$]*$", name):
        return None
    return name


def normalize_params(params: str) -> str:
    return " ".join(params.strip().split())


def base_symbol(name: str, kind: str, path: str, digest: str) -> dict[str, Any]:
    return {
        "name": name,
        "kind": kind,
        "visibility": "public",
        "evidence": evidence_record(path, digest),
    }
