from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from spec_harvester.analyzer_cache import AnalyzerCache
from spec_harvester.interface_index import (
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    validate_public_interface_index,
)

GO_PUBLIC_API_ANALYZER_ID = "go-source-public-api"
GO_PUBLIC_API_ANALYZER_VERSION = "0.1.0"

IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".ruff_cache",
    "build",
    "dist",
    "internal",
    "node_modules",
    "testdata",
    "tmp",
    "vendor",
}

GENERATED_MARKERS = (
    "code generated",
    "do not edit",
)

IDENTIFIER_RE = r"[A-Za-z_][A-Za-z0-9_]*"
PACKAGE_RE = re.compile(r"^\s*package\s+(?P<name>" + IDENTIFIER_RE + r")\b", re.MULTILINE)
MODULE_RE = re.compile(r"^\s*module\s+(?P<module>\S+)\s*$", re.MULTILINE)
FUNC_RE = re.compile(
    r"^func\s+"
    r"(?:(?P<receiver>\([^)]*\))\s*)?"
    r"(?P<name>" + IDENTIFIER_RE + r")\s*"
    r"(?P<params>\([^{}]*\))\s*"
    r"(?P<returns>.*)$",
    re.DOTALL,
)
TYPE_RE = re.compile(r"^type\s+(?P<name>" + IDENTIFIER_RE + r")\s*(?:=\s*)?(?P<body>.*)$")
VALUE_RE = re.compile(r"^(?P<name>" + IDENTIFIER_RE + r")\b(?P<body>.*)$")


def analyze_go_public_api(
    source: Path,
    *,
    package_id: str | None = None,
    source_revision: str | None = None,
    cache_dir: Path | None = None,
) -> dict[str, Any]:
    root = source.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Go source root does not exist or is not a directory: {source}")

    cache = AnalyzerCache(cache_dir) if cache_dir is not None else None
    module_path = go_module_path(root) or package_id or root.name
    package_entrypoints: dict[str, list[dict[str, Any]]] = {}
    diagnostics: list[dict[str, Any]] = []

    for path in go_source_files(root):
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        if is_generated_go_file(data):
            continue
        digest = hashlib.sha256(data).hexdigest()
        cached_payload = read_cached_go_payload(cache, relative, digest)
        if cached_payload is not None:
            package_path, _package_name, entrypoint, file_diagnostics = cached_payload
            package_entrypoints.setdefault(package_path, []).append(entrypoint)
            diagnostics.extend(file_diagnostics)
            continue

        text = data.decode("utf-8", errors="replace")
        package_name = package_name_from_source(text)
        if package_name is None:
            diagnostic = {
                "level": "error",
                "path": relative,
                "message": "Unable to find Go package declaration.",
                "evidence": evidence_record(relative, digest),
            }
            diagnostics.append(diagnostic)
            write_cached_go_payload(cache, digest, None, None, None, [diagnostic])
            continue

        package_path = package_path_for_file(path, root)
        symbols = go_symbols(text, relative, digest)
        entrypoint = {
            "path": relative,
            "symbols": symbols,
        }
        package_entrypoints.setdefault(package_path, []).append(entrypoint)
        write_cached_go_payload(cache, digest, package_path, package_name, entrypoint, [])

    packages = [
        {
            "id": package_import_path(module_path, package_path),
            "path": package_path,
            "language": "go",
            "entrypoints": sorted(entrypoints, key=lambda item: item["path"]),
        }
        for package_path, entrypoints in sorted(package_entrypoints.items())
    ]

    if not packages and not diagnostics:
        diagnostics.append(
            {
                "level": "warning",
                "message": "No non-generated Go source files were found.",
            }
        )

    index = new_public_interface_index(
        source_revision=source_revision,
        analyzers=[
            analyzer_record(
                GO_PUBLIC_API_ANALYZER_ID,
                GO_PUBLIC_API_ANALYZER_VERSION,
                execution="none",
                confidence="medium",
            )
        ],
        packages=packages,
        diagnostics=sorted(diagnostics, key=lambda item: (item["level"], item.get("path", ""))),
    )
    validate_public_interface_index(index)
    return index


def go_module_path(root: Path) -> str | None:
    path = root / "go.mod"
    if not path.exists() or not path.is_file() or path.is_symlink():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    clean = strip_line_comments(text)
    match = MODULE_RE.search(clean)
    if match is None:
        return None
    module = match.group("module").strip()
    return module or None


def go_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.go"):
        if should_skip_go_source(path, root):
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def should_skip_go_source(path: Path, root: Path) -> bool:
    if path.is_symlink() or not path.is_file() or path.name.endswith("_test.go"):
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part.startswith(".") or part in IGNORED_DIR_NAMES for part in relative.parts[:-1])


def is_generated_go_file(data: bytes) -> bool:
    header = data[:4096].decode("utf-8", errors="replace").lower()
    return all(marker in header for marker in GENERATED_MARKERS)


def package_name_from_source(text: str) -> str | None:
    clean = strip_block_comments(strip_line_comments(text))
    match = PACKAGE_RE.search(clean)
    return match.group("name") if match is not None else None


def package_path_for_file(path: Path, root: Path) -> str:
    relative_parent = path.parent.relative_to(root).as_posix()
    return "." if relative_parent == "" else relative_parent


def package_import_path(module_path: str, package_path: str) -> str:
    if package_path == ".":
        return module_path
    return f"{module_path.rstrip('/')}/{package_path}"


def go_symbols(text: str, path: str, digest: str) -> list[dict[str, Any]]:
    clean = strip_strings(strip_block_comments(strip_line_comments(text)))
    symbols: dict[str, dict[str, Any]] = {}
    lines = clean.splitlines()
    index = 0
    brace_depth = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if brace_depth == 0:
            if stripped.startswith("func "):
                declaration, index = collect_func_declaration(lines, index)
                symbol = func_symbol(declaration, path, digest)
                if symbol is not None:
                    symbols[symbol["name"]] = symbol
                continue
            if stripped.startswith("type ("):
                block, index = collect_parenthesized_declaration(lines, index)
                for symbol in grouped_type_symbols(block, path, digest):
                    symbols[symbol["name"]] = symbol
                continue
            if stripped.startswith("type "):
                symbol = type_symbol(stripped, path, digest)
                if symbol is not None:
                    symbols[symbol["name"]] = symbol
            elif stripped.startswith("const ("):
                block, index = collect_parenthesized_declaration(lines, index)
                for symbol in grouped_value_symbols(block, "constant", path, digest):
                    symbols[symbol["name"]] = symbol
                continue
            elif stripped.startswith("const "):
                symbol = value_symbol(
                    stripped.removeprefix("const ").strip(), "constant", path, digest
                )
                if symbol is not None:
                    symbols[symbol["name"]] = symbol
            elif stripped.startswith("var ("):
                block, index = collect_parenthesized_declaration(lines, index)
                for symbol in grouped_value_symbols(block, "variable", path, digest):
                    symbols[symbol["name"]] = symbol
                continue
            elif stripped.startswith("var "):
                symbol = value_symbol(
                    stripped.removeprefix("var ").strip(), "variable", path, digest
                )
                if symbol is not None:
                    symbols[symbol["name"]] = symbol
        brace_depth = max(0, brace_depth + lines[index].count("{") - lines[index].count("}"))
        index += 1
    return [symbols[name] for name in sorted(symbols)]


def collect_func_declaration(lines: list[str], start: int) -> tuple[str, int]:
    parts: list[str] = []
    index = start
    paren_depth = 0
    while index < len(lines):
        line = lines[index].strip()
        before_body = line.split("{", 1)[0]
        parts.append(before_body)
        paren_depth += before_body.count("(") - before_body.count(")")
        if "{" in line or (paren_depth <= 0 and ")" in before_body):
            break
        index += 1
    return normalize_spaces(" ".join(parts)), index + 1


def collect_parenthesized_declaration(lines: list[str], start: int) -> tuple[list[str], int]:
    block: list[str] = []
    index = start + 1
    paren_depth = 1
    while index < len(lines):
        line = lines[index].strip()
        paren_depth += line.count("(") - line.count(")")
        if paren_depth <= 0:
            break
        if line:
            block.append(line)
        index += 1
    return block, index + 1


def grouped_type_symbols(lines: list[str], path: str, digest: str) -> list[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []
    for line in lines:
        symbol = type_symbol(f"type {line}", path, digest)
        if symbol is not None:
            symbols.append(symbol)
    return symbols


def grouped_value_symbols(
    lines: list[str],
    kind: str,
    path: str,
    digest: str,
) -> list[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []
    for line in lines:
        symbol = value_symbol(line, kind, path, digest)
        if symbol is not None:
            symbols.append(symbol)
    return symbols


def func_symbol(declaration: str, path: str, digest: str) -> dict[str, Any] | None:
    match = FUNC_RE.match(declaration)
    if match is None:
        return None
    name = match.group("name")
    receiver = receiver_type_name(match.group("receiver"))
    if receiver is not None:
        if not is_exported_identifier(name) or not is_exported_identifier(receiver):
            return None
        public_name = f"{receiver}.{name}"
    else:
        if not is_exported_identifier(name):
            return None
        public_name = name
    signature = normalize_spaces(declaration)
    return base_symbol(public_name, "function", path, digest, signature=signature)


def type_symbol(declaration: str, path: str, digest: str) -> dict[str, Any] | None:
    match = TYPE_RE.match(declaration)
    if match is None:
        return None
    name = match.group("name")
    if not is_exported_identifier(name):
        return None
    body = match.group("body").strip()
    kind = "type"
    if body.startswith("struct"):
        kind = "struct"
    elif body.startswith("interface"):
        kind = "interface"
    return base_symbol(name, kind, path, digest, signature=normalize_spaces(declaration))


def value_symbol(
    declaration: str,
    kind: str,
    path: str,
    digest: str,
) -> dict[str, Any] | None:
    match = VALUE_RE.match(declaration)
    if match is None:
        return None
    name = match.group("name")
    if not is_exported_identifier(name):
        return None
    return base_symbol(name, kind, path, digest, signature=normalize_spaces(declaration))


def receiver_type_name(receiver: str | None) -> str | None:
    if receiver is None:
        return None
    clean = receiver.strip().removeprefix("(").removesuffix(")").strip()
    clean = clean.replace("*", " ")
    parts = [part for part in clean.split() if part]
    if not parts:
        return None
    return parts[-1]


def is_exported_identifier(name: str) -> bool:
    return bool(name) and "A" <= name[0] <= "Z"


def base_symbol(
    name: str,
    kind: str,
    path: str,
    digest: str,
    *,
    signature: str | None = None,
) -> dict[str, Any]:
    symbol: dict[str, Any] = {
        "name": name,
        "kind": kind,
        "visibility": "public",
        "evidence": evidence_record(path, digest),
    }
    if signature:
        symbol["signature"] = signature
    return symbol


def strip_line_comments(text: str) -> str:
    return re.sub(r"//.*?$", "", text, flags=re.MULTILINE)


def strip_block_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


def strip_strings(text: str) -> str:
    result: list[str] = []
    index = 0
    quote: str | None = None
    escaped = False
    while index < len(text):
        char = text[index]
        if quote is None:
            if char in {'"', "'", "`"}:
                quote = char
                result.append(" ")
            else:
                result.append(char)
        else:
            if char == "\n":
                result.append("\n")
                if quote != "`":
                    quote = None
                escaped = False
            elif quote != "`" and char == "\\" and not escaped:
                result.append(" ")
                escaped = True
            elif char == quote and not escaped:
                quote = None
                result.append(" ")
            else:
                result.append(" ")
                escaped = False
        index += 1
    return "".join(result)


def normalize_spaces(text: str) -> str:
    return " ".join(text.split())


def read_cached_go_payload(
    cache: AnalyzerCache | None,
    path: str,
    digest: str,
) -> tuple[str, str, dict[str, Any], list[dict[str, Any]]] | None:
    if cache is None:
        return None
    payload = cache.read(
        analyzer_id=GO_PUBLIC_API_ANALYZER_ID,
        analyzer_version=GO_PUBLIC_API_ANALYZER_VERSION,
        file_digest=digest,
    )
    if not isinstance(payload, dict):
        return None
    package_path = payload.get("packagePath")
    package_name = payload.get("packageName")
    entrypoint = payload.get("entrypoint")
    diagnostics = payload.get("diagnostics")
    if not isinstance(diagnostics, list):
        return None
    if entrypoint is None:
        return None
    if not isinstance(package_path, str) or not isinstance(package_name, str):
        return None
    if not is_entrypoint_for_path(entrypoint, path):
        return None
    for diagnostic in diagnostics:
        if not is_diagnostic_for_path(diagnostic, path):
            return None
    return package_path, package_name, entrypoint, diagnostics


def write_cached_go_payload(
    cache: AnalyzerCache | None,
    digest: str,
    package_path: str | None,
    package_name: str | None,
    entrypoint: dict[str, Any] | None,
    diagnostics: list[dict[str, Any]],
) -> None:
    if cache is None:
        return
    cache.write(
        analyzer_id=GO_PUBLIC_API_ANALYZER_ID,
        analyzer_version=GO_PUBLIC_API_ANALYZER_VERSION,
        file_digest=digest,
        payload={
            "packagePath": package_path,
            "packageName": package_name,
            "entrypoint": entrypoint,
            "diagnostics": diagnostics,
        },
    )


def is_entrypoint_for_path(value: Any, path: str) -> bool:
    if not isinstance(value, dict) or value.get("path") != path:
        return False
    symbols = value.get("symbols")
    if not isinstance(symbols, list):
        return False
    return all(is_symbol_for_path(symbol, path) for symbol in symbols)


def is_symbol_for_path(value: Any, path: str) -> bool:
    if not isinstance(value, dict):
        return False
    evidence = value.get("evidence")
    return isinstance(evidence, dict) and evidence.get("path") == path


def is_diagnostic_for_path(value: Any, path: str) -> bool:
    if not isinstance(value, dict) or value.get("path") != path:
        return False
    evidence = value.get("evidence")
    return isinstance(evidence, dict) and evidence.get("path") == path
