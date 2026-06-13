from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.analyzer_cache import AnalyzerCache
from spec_harvester.interface_index import (
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    validate_public_interface_index,
)
from spec_harvester.public_api_analyzer_options import PublicApiAnalyzerOptions
from spec_harvester.public_api_payload_records import PublicApiPayloadPath

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
TYPE_PARAMETERS_RE = r"(?:\s*\[[^\]]+\])?"
PACKAGE_RE = re.compile(r"^\s*package\s+(?P<name>" + IDENTIFIER_RE + r")\b", re.MULTILINE)
MODULE_RE = re.compile(r"^\s*module\s+(?P<module>\S+)\s*$", re.MULTILINE)
FUNC_RE = re.compile(
    r"^func\s+"
    r"(?:(?P<receiver>\([^)]*\))\s*)?"
    r"(?P<name>" + IDENTIFIER_RE + r")" + TYPE_PARAMETERS_RE + r"\s*"
    r"(?P<params>\([^{}]*\))\s*"
    r"(?P<returns>.*)$",
    re.DOTALL,
)
TYPE_RE = re.compile(
    r"^type\s+(?P<name>" + IDENTIFIER_RE + r")" + TYPE_PARAMETERS_RE + r"\s*(?:=\s*)?(?P<body>.*)$"
)
VALUE_NAME_RE = re.compile(r"(?P<name>" + IDENTIFIER_RE + r")\b")


def analyze_go_public_api(
    source: Path | PublicApiAnalyzerOptions,
    **kwargs: Any,
) -> dict[str, Any]:
    options = PublicApiAnalyzerOptions.from_call(source, **kwargs)
    return analyze_go_public_api_with_options(options)


def analyze_go_public_api_with_options(options: PublicApiAnalyzerOptions) -> dict[str, Any]:
    return GoPublicApiAnalyzer(options).index()


@dataclass(frozen=True)
class GoPublicApiAnalyzer:
    options: PublicApiAnalyzerOptions

    def index(self) -> dict[str, Any]:
        root = self.root()
        package_entrypoints, diagnostics = self.package_entrypoints(root, self.cache())
        packages = self.package_records(root, package_entrypoints)
        if not packages and not diagnostics:
            diagnostics.append(self.no_source_diagnostic())

        index = new_public_interface_index(
            source_revision=self.options.source_revision,
            analyzers=[self.analyzer_record()],
            packages=packages,
            diagnostics=sorted(diagnostics, key=lambda item: (item["level"], item.get("path", ""))),
        )
        validate_public_interface_index(index)
        return index

    def root(self) -> Path:
        return self.options.root("Go")

    def cache(self) -> AnalyzerCache | None:
        return self.options.cache()

    def module_path(self, root: Path) -> str:
        return go_module_path(root) or self.options.package_id_or(root.name)

    def analyzer_record(self) -> dict[str, Any]:
        return analyzer_record(
            GO_PUBLIC_API_ANALYZER_ID,
            GO_PUBLIC_API_ANALYZER_VERSION,
            execution="none",
            confidence="medium",
        )

    def package_entrypoints(
        self,
        root: Path,
        cache: AnalyzerCache | None,
    ) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
        package_entrypoints: dict[str, list[dict[str, Any]]] = {}
        diagnostics: list[dict[str, Any]] = []
        for path in go_source_files(root):
            package_path, entrypoint, file_diagnostics = self.entrypoint(path, root, cache)
            if package_path is not None and entrypoint is not None:
                package_entrypoints.setdefault(package_path, []).append(entrypoint)
            diagnostics.extend(file_diagnostics)
        return package_entrypoints, diagnostics

    def entrypoint(
        self,
        path: Path,
        root: Path,
        cache: AnalyzerCache | None,
    ) -> tuple[str | None, dict[str, Any] | None, list[dict[str, Any]]]:
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        if is_generated_go_file(data):
            return None, None, []

        digest = hashlib.sha256(data).hexdigest()
        cached_payload = read_cached_go_payload(cache, relative, digest)
        if cached_payload is not None:
            package_path, _package_name, entrypoint, diagnostics = cached_payload
            return package_path, entrypoint, diagnostics

        text = data.decode("utf-8", errors="replace")
        package_name = package_name_from_source(text)
        if package_name is None:
            diagnostic = self.missing_package_diagnostic(relative, digest)
            write_cached_go_payload(cache, digest, None, None, None, [diagnostic])
            return None, None, [diagnostic]

        package_path = package_path_for_file(path, root)
        entrypoint = {
            "path": relative,
            "symbols": go_symbols(text, relative, digest),
        }
        write_cached_go_payload(cache, digest, package_path, package_name, entrypoint, [])
        return package_path, entrypoint, []

    def package_records(
        self,
        root: Path,
        package_entrypoints: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        module_path = self.module_path(root)
        return [
            {
                "id": package_import_path(module_path, package_path),
                "path": package_path,
                "language": "go",
                "entrypoints": sorted(entrypoints, key=lambda item: item["path"]),
            }
            for package_path, entrypoints in sorted(package_entrypoints.items())
        ]

    def missing_package_diagnostic(self, relative: str, digest: str) -> dict[str, Any]:
        return {
            "level": "error",
            "path": relative,
            "message": "Unable to find Go package declaration.",
            "evidence": evidence_record(relative, digest),
        }

    def no_source_diagnostic(self) -> dict[str, str]:
        return {
            "level": "warning",
            "message": "No non-generated Go source files were found.",
        }


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
    for current_root, dirs, filenames in os.walk(root, followlinks=False):
        current = Path(current_root)
        dirs[:] = [dirname for dirname in sorted(dirs) if not should_skip_go_dir(current / dirname)]
        for filename in sorted(filenames):
            path = current / filename
            if should_skip_go_source(path, root):
                continue
            try:
                data = path.read_bytes()
            except OSError:
                continue
            if is_generated_go_file(data):
                continue
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def should_skip_go_dir(path: Path) -> bool:
    return path.is_symlink() or path.name.startswith(".") or path.name in IGNORED_DIR_NAMES


def should_skip_go_source(path: Path, root: Path) -> bool:
    if not path.name.endswith(".go"):
        return True
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
    clean = strip_go_non_code(text)
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
    clean = strip_go_non_code(text)
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
                for symbol in value_symbols(
                    stripped.removeprefix("const ").strip(), "constant", path, digest
                ):
                    symbols[symbol["name"]] = symbol
            elif stripped.startswith("var ("):
                block, index = collect_parenthesized_declaration(lines, index)
                for symbol in grouped_value_symbols(block, "variable", path, digest):
                    symbols[symbol["name"]] = symbol
                continue
            elif stripped.startswith("var "):
                for symbol in value_symbols(
                    stripped.removeprefix("var ").strip(), "variable", path, digest
                ):
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
        for symbol in value_symbols(line, kind, path, digest):
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


def value_symbols(
    declaration: str,
    kind: str,
    path: str,
    digest: str,
) -> list[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []
    for name in value_names(declaration):
        if not is_exported_identifier(name):
            continue
        symbols.append(
            base_symbol(name, kind, path, digest, signature=normalize_spaces(declaration))
        )
    return symbols


def value_names(declaration: str) -> list[str]:
    left_side = declaration.split("=", 1)[0]
    names: list[str] = []
    for part in left_side.split(","):
        match = VALUE_NAME_RE.search(part.strip())
        if match is not None:
            names.append(match.group("name"))
    return names


def receiver_type_name(receiver: str | None) -> str | None:
    if receiver is None:
        return None
    clean = receiver.strip().removeprefix("(").removesuffix(")").strip()
    clean = clean.replace("*", " ")
    parts = [part for part in clean.split() if part]
    if not parts:
        return None
    return strip_type_parameters(parts[-1])


def strip_type_parameters(name: str) -> str:
    return re.sub(r"\[.*\]$", "", name)


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


def strip_go_non_code(text: str) -> str:
    result: list[str] = []
    index = 0
    quote: str | None = None
    escaped = False
    while index < len(text):
        char = text[index]
        if quote is None:
            if text.startswith("//", index):
                while index < len(text) and text[index] != "\n":
                    result.append(" ")
                    index += 1
                continue
            if text.startswith("/*", index):
                result.extend("  ")
                index += 2
                while index < len(text) - 1 and not text.startswith("*/", index):
                    result.append("\n" if text[index] == "\n" else " ")
                    index += 1
                if index < len(text) - 1:
                    result.extend("  ")
                    index += 2
                continue
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
) -> tuple[str | None, str | None, dict[str, Any] | None, list[dict[str, Any]]] | None:
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
    payload_path = PublicApiPayloadPath(path)
    if entrypoint is None:
        if not diagnostics:
            return None
        for diagnostic in diagnostics:
            if not payload_path.matches_diagnostic(diagnostic):
                return None
        return None, None, None, diagnostics
    if not isinstance(package_path, str) or not isinstance(package_name, str):
        return None
    if not payload_path.matches_entrypoint(entrypoint):
        return None
    for diagnostic in diagnostics:
        if not payload_path.matches_diagnostic(diagnostic):
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
