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
from spec_harvester.public_api_entrypoint_cache import (
    read_cached_public_api_entrypoint,
    write_cached_public_api_entrypoint,
)
from spec_harvester.swift_text import mask_swift_block_comment, strip_swift_comments

SWIFT_PUBLIC_API_ANALYZER_ID = "swift-source-public-api"
SWIFT_PUBLIC_API_ANALYZER_VERSION = "0.1.0"

IGNORED_DIR_NAMES = {
    ".build",
    ".git",
    ".hg",
    ".swiftpm",
    "Carthage",
    "Derived",
    "DerivedData",
    "Pods",
    "SourcePackages",
    "build",
    "checkouts",
    "node_modules",
}

TEST_DIR_NAMES = {
    "Tests",
    "UITests",
}

IDENTIFIER_RE = r"(?:`[^`]+`|[A-Za-z_][A-Za-z0-9_]*)"
QUALIFIED_IDENTIFIER_RE = rf"{IDENTIFIER_RE}(?:\.{IDENTIFIER_RE})*"
PACKAGE_NAME_RE = re.compile(r"\bPackage\s*\(\s*name\s*:\s*\"([^\"]+)\"")
ACCESS_RE = re.compile(r"\b(public|open)\b")
TYPE_DECL_RE = re.compile(
    rf"\b(?P<kind>class|struct|protocol|enum|actor)\s+(?P<name>{IDENTIFIER_RE})"
)
EXTENSION_DECL_RE = re.compile(rf"\bextension\s+(?P<name>{QUALIFIED_IDENTIFIER_RE})")
FUNC_DECL_RE = re.compile(rf"\bfunc\s+(?P<name>{IDENTIFIER_RE}|[~!=<>+\-*/%&|^.?]+)")
INIT_DECL_RE = re.compile(r"\binit\s*[?!]?\s*(?:<[^>{}]+>)?\s*\(")
SUBSCRIPT_DECL_RE = re.compile(r"\bsubscript\s*\(")
PROPERTY_DECL_RE = re.compile(r"\b(?P<kind>var|let)\s+(?P<names>[^:=\{\n]+)")
TYPEALIAS_DECL_RE = re.compile(rf"\btypealias\s+(?P<name>{IDENTIFIER_RE})")
ASSOCIATEDTYPE_DECL_RE = re.compile(rf"\bassociatedtype\s+(?P<name>{IDENTIFIER_RE})")
ENUM_CASE_DECL_RE = re.compile(r"\bcase\s+(?P<cases>.+)")


@dataclass(frozen=True)
class SwiftScope:
    name: str
    kind: str
    visibility: str | None
    depth: int


def analyze_swift_public_api(
    source: Path | PublicApiAnalyzerOptions,
    **kwargs: Any,
) -> dict[str, Any]:
    options = PublicApiAnalyzerOptions.from_call(source, **kwargs)
    return analyze_swift_public_api_with_options(options)


def analyze_swift_public_api_with_options(options: PublicApiAnalyzerOptions) -> dict[str, Any]:
    root = options.root("Swift")
    cache = options.cache()
    package_roots = swift_package_roots(root)
    all_entrypoint_count = 0
    diagnostics: list[dict[str, Any]] = []
    packages: list[dict[str, Any]] = []

    for package_root in package_roots:
        excluded_roots = nested_package_roots(package_root, package_roots)
        entrypoints = swift_entrypoints(root, package_root, excluded_roots, diagnostics, cache)
        if not entrypoints:
            continue
        all_entrypoint_count += len(entrypoints)
        package_path = relative_package_path(root, package_root)
        packages.append(
            {
                "id": swift_package_id(options, root, package_root),
                "path": package_path,
                "language": "swift",
                "entrypoints": entrypoints,
            }
        )

    if all_entrypoint_count == 0 and not diagnostics:
        diagnostics.append(
            {
                "level": "warning",
                "message": "No Swift source files were found.",
            }
        )

    index = new_public_interface_index(
        source_revision=options.source_revision,
        analyzers=[
            analyzer_record(
                SWIFT_PUBLIC_API_ANALYZER_ID,
                SWIFT_PUBLIC_API_ANALYZER_VERSION,
                execution="none",
                confidence="medium",
            )
        ],
        packages=sorted(packages, key=lambda item: item["path"]),
        diagnostics=sorted(diagnostics, key=diagnostic_sort_key),
    )
    validate_public_interface_index(index)
    return index


def swift_entrypoints(
    root: Path,
    package_root: Path,
    excluded_roots: list[Path],
    diagnostics: list[dict[str, Any]],
    cache: AnalyzerCache | None,
) -> list[dict[str, Any]]:
    entrypoints: list[dict[str, Any]] = []
    for path in swift_source_files(package_root, excluded_roots=excluded_roots):
        relative = path.relative_to(root).as_posix()
        try:
            data = path.read_bytes()
        except OSError as exc:
            diagnostics.append(
                {
                    "level": "error",
                    "path": relative,
                    "message": f"Unable to read Swift source file: {exc}",
                }
            )
            continue
        digest = hashlib.sha256(data).hexdigest()
        cached_payload = read_cached_public_api_entrypoint(
            cache,
            analyzer_id=SWIFT_PUBLIC_API_ANALYZER_ID,
            analyzer_version=SWIFT_PUBLIC_API_ANALYZER_VERSION,
            path=relative,
            digest=digest,
        )
        if cached_payload is not None:
            entrypoint, file_diagnostics = cached_payload
            if entrypoint is not None:
                entrypoints.append(entrypoint)
            diagnostics.extend(file_diagnostics)
            continue

        text = data.decode("utf-8", errors="replace")
        entrypoint = {
            "path": relative,
            "symbols": swift_symbols(text, relative, digest),
        }
        entrypoints.append(entrypoint)
        write_cached_public_api_entrypoint(
            cache,
            analyzer_id=SWIFT_PUBLIC_API_ANALYZER_ID,
            analyzer_version=SWIFT_PUBLIC_API_ANALYZER_VERSION,
            digest=digest,
            entrypoint=entrypoint,
            diagnostics=[],
        )
    return sorted(entrypoints, key=lambda item: item["path"])


def swift_source_files(root: Path, *, excluded_roots: list[Path] | None = None) -> list[Path]:
    excluded = [path.resolve() for path in excluded_roots or []]
    files: list[Path] = []
    for current_root, dirs, filenames in os.walk(root, followlinks=False):
        current = Path(current_root)
        dirs[:] = [
            dirname for dirname in sorted(dirs) if not should_skip_swift_dir(current / dirname)
        ]
        if any(is_relative_to(current.resolve(), excluded_root) for excluded_root in excluded):
            dirs[:] = []
            continue
        for filename in sorted(filenames):
            path = current / filename
            if should_skip_swift_source(path, root):
                continue
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def should_skip_swift_dir(path: Path) -> bool:
    return (
        path.is_symlink()
        or path.name.startswith(".")
        or path.name in IGNORED_DIR_NAMES
        or path.name in TEST_DIR_NAMES
        or path.name.endswith("Tests")
    )


def should_skip_swift_source(path: Path, root: Path) -> bool:
    if path.name == "Package.swift" or path.suffix != ".swift":
        return True
    if path.is_symlink() or not path.is_file():
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(
        part.startswith(".")
        or part in IGNORED_DIR_NAMES
        or part in TEST_DIR_NAMES
        or part.endswith("Tests")
        for part in relative.parts[:-1]
    )


def swift_package_roots(root: Path) -> list[Path]:
    manifests = swift_package_manifest_files(root)
    if not manifests:
        return [root]
    return sorted({manifest.parent for manifest in manifests}, key=lambda item: item.as_posix())


def swift_package_manifest_files(root: Path) -> list[Path]:
    manifests: list[Path] = []
    for current_root, dirs, filenames in os.walk(root, followlinks=False):
        current = Path(current_root)
        dirs[:] = [
            dirname for dirname in sorted(dirs) if not should_skip_swift_dir(current / dirname)
        ]
        if "Package.swift" in filenames:
            path = current / "Package.swift"
            if path.is_file() and not path.is_symlink():
                manifests.append(path)
    return sorted(manifests, key=lambda item: item.relative_to(root).as_posix())


def nested_package_roots(package_root: Path, package_roots: list[Path]) -> list[Path]:
    return [
        root
        for root in package_roots
        if root != package_root and is_relative_to(root.resolve(), package_root.resolve())
    ]


def relative_package_path(root: Path, package_root: Path) -> str:
    relative = package_root.relative_to(root).as_posix()
    return relative or "."


def swift_package_id(
    options: PublicApiAnalyzerOptions,
    root: Path,
    package_root: Path,
) -> str:
    if package_root == root:
        return options.package_id_or(swift_package_name(package_root) or root.name)
    return swift_package_name(package_root) or package_root.name


def swift_package_name(package_root: Path) -> str | None:
    manifest = package_root / "Package.swift"
    if not manifest.exists() or not manifest.is_file() or manifest.is_symlink():
        return None
    try:
        text = manifest.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    match = PACKAGE_NAME_RE.search(strip_swift_comments(text))
    if match is None:
        return None
    name = match.group(1).strip()
    return name or None


def swift_symbols(text: str, path: str, digest: str) -> list[dict[str, Any]]:
    clean = mask_swift_non_code(text)
    clean_lines = clean.splitlines()
    original_lines = text.splitlines()
    symbols: dict[str, dict[str, Any]] = {}
    scopes: list[SwiftScope] = []
    pending_scope: SwiftScope | None = None
    brace_depth = 0

    for index, line in enumerate(clean_lines):
        stripped = line.strip()
        if not stripped:
            continue

        declaration = collect_declaration(clean_lines, index)
        scope_to_push = swift_scope_from_declaration(
            declaration,
            scopes,
            path,
            digest,
            leading_doc(original_lines, index),
            symbols,
        )
        if scope_to_push is None:
            add_member_symbol(
                declaration,
                scopes,
                path,
                digest,
                leading_doc(original_lines, index),
                symbols,
            )

        previous_depth = brace_depth
        brace_depth = max(0, brace_depth + brace_delta(line))
        if pending_scope is not None and "{" in line and brace_depth > previous_depth:
            scopes.append(
                SwiftScope(
                    name=pending_scope.name,
                    kind=pending_scope.kind,
                    visibility=pending_scope.visibility,
                    depth=brace_depth,
                )
            )
            pending_scope = None
        if scope_to_push is not None:
            if "{" in declaration and brace_depth > previous_depth:
                scopes.append(
                    SwiftScope(
                        name=scope_to_push.name,
                        kind=scope_to_push.kind,
                        visibility=scope_to_push.visibility,
                        depth=brace_depth,
                    )
                )
            elif "{" not in declaration:
                pending_scope = scope_to_push
        while scopes and brace_depth < scopes[-1].depth:
            scopes.pop()

    return [symbols[name] for name in sorted(symbols)]


def swift_scope_from_declaration(
    declaration: str,
    scopes: list[SwiftScope],
    path: str,
    digest: str,
    doc: str | None,
    symbols: dict[str, dict[str, Any]],
) -> SwiftScope | None:
    extension_match = EXTENSION_DECL_RE.search(declaration)
    type_match = TYPE_DECL_RE.search(declaration)
    if extension_match is not None and (
        type_match is None or extension_match.start() < type_match.start()
    ):
        visibility = explicit_access(declaration, extension_match.start())
        name = clean_identifier(extension_match.group("name"))
        return SwiftScope(name=name, kind="extension", visibility=visibility, depth=0)
    if type_match is None:
        return None

    visibility = declaration_visibility(declaration, type_match.start(), scopes)
    local_name = clean_identifier(type_match.group("name"))
    name = qualified_name(scopes, local_name)
    kind = swift_symbol_kind(type_match.group("kind"))
    if visibility is not None:
        symbols[name] = symbol_record(
            name,
            kind,
            visibility,
            path,
            digest,
            signature=signature_before_body(declaration),
            doc=doc,
        )
    return SwiftScope(
        name=local_name,
        kind=type_match.group("kind"),
        visibility=visibility,
        depth=0,
    )


def add_member_symbol(
    declaration: str,
    scopes: list[SwiftScope],
    path: str,
    digest: str,
    doc: str | None,
    symbols: dict[str, dict[str, Any]],
) -> None:
    for symbol in member_symbols(declaration, scopes, path, digest, doc):
        symbols[symbol["name"]] = symbol


def member_symbols(
    declaration: str,
    scopes: list[SwiftScope],
    path: str,
    digest: str,
    doc: str | None,
) -> list[dict[str, Any]]:
    func_match = FUNC_DECL_RE.search(declaration)
    if func_match is not None:
        visibility = declaration_visibility(declaration, func_match.start(), scopes)
        if visibility is None:
            return []
        name = qualified_name(scopes, clean_identifier(func_match.group("name")))
        return [
            symbol_record(
                name,
                "function",
                visibility,
                path,
                digest,
                signature=signature_before_body(declaration),
                doc=doc,
            )
        ]

    init_match = INIT_DECL_RE.search(declaration)
    if init_match is not None:
        visibility = declaration_visibility(declaration, init_match.start(), scopes)
        if visibility is None:
            return []
        return [
            symbol_record(
                qualified_name(scopes, "init"),
                "function",
                visibility,
                path,
                digest,
                signature=signature_before_body(declaration),
                doc=doc,
            )
        ]

    subscript_match = SUBSCRIPT_DECL_RE.search(declaration)
    if subscript_match is not None:
        visibility = declaration_visibility(declaration, subscript_match.start(), scopes)
        if visibility is None:
            return []
        return [
            symbol_record(
                qualified_name(scopes, "subscript"),
                "function",
                visibility,
                path,
                digest,
                signature=signature_before_body(declaration),
                doc=doc,
            )
        ]

    property_match = PROPERTY_DECL_RE.search(declaration)
    if property_match is not None:
        visibility = declaration_visibility(declaration, property_match.start(), scopes)
        if visibility is None:
            return []
        kind = "constant" if property_match.group("kind") == "let" else "variable"
        return [
            symbol_record(
                qualified_name(scopes, clean_identifier(name)),
                kind,
                visibility,
                path,
                digest,
                signature=property_signature(declaration),
                doc=doc,
            )
            for name in property_names(property_match.group("names"))
        ]

    typealias_match = TYPEALIAS_DECL_RE.search(declaration)
    if typealias_match is not None:
        visibility = declaration_visibility(declaration, typealias_match.start(), scopes)
        if visibility is None:
            return []
        return [
            symbol_record(
                qualified_name(scopes, clean_identifier(typealias_match.group("name"))),
                "type",
                visibility,
                path,
                digest,
                signature=signature_before_body(declaration),
                doc=doc,
            )
        ]

    associatedtype_match = ASSOCIATEDTYPE_DECL_RE.search(declaration)
    if associatedtype_match is not None:
        visibility = inherited_protocol_visibility(scopes)
        if visibility is None:
            return []
        return [
            symbol_record(
                qualified_name(scopes, clean_identifier(associatedtype_match.group("name"))),
                "type",
                visibility,
                path,
                digest,
                signature=signature_before_body(declaration),
                doc=doc,
            )
        ]

    case_match = ENUM_CASE_DECL_RE.search(declaration)
    if case_match is not None:
        visibility = inherited_enum_visibility(scopes)
        if visibility is None:
            return []
        return [
            symbol_record(
                qualified_name(scopes, case_name),
                "constant",
                visibility,
                path,
                digest,
                signature=signature_before_body(declaration),
                doc=doc,
            )
            for case_name in enum_case_names(case_match.group("cases"))
        ]

    return []


def declaration_visibility(
    declaration: str,
    keyword_start: int,
    scopes: list[SwiftScope],
) -> str | None:
    access = explicit_access(declaration, keyword_start)
    if access is not None:
        return access
    inherited = inherited_member_visibility(scopes)
    if inherited is not None:
        return inherited
    return None


def explicit_access(declaration: str, keyword_start: int) -> str | None:
    prefix = declaration[:keyword_start]
    matches = ACCESS_RE.findall(prefix)
    if "open" in matches:
        return "open"
    if "public" in matches:
        return "public"
    return None


def inherited_member_visibility(scopes: list[SwiftScope]) -> str | None:
    if not scopes:
        return None
    scope = scopes[-1]
    if scope.kind in {"extension", "protocol"} and scope.visibility in {"public", "open"}:
        return scope.visibility
    return None


def inherited_protocol_visibility(scopes: list[SwiftScope]) -> str | None:
    if not scopes:
        return None
    scope = scopes[-1]
    if scope.kind == "protocol" and scope.visibility in {"public", "open"}:
        return scope.visibility
    return None


def inherited_enum_visibility(scopes: list[SwiftScope]) -> str | None:
    if not scopes:
        return None
    scope = scopes[-1]
    if scope.kind == "enum" and scope.visibility in {"public", "open"}:
        return scope.visibility
    return None


def qualified_name(scopes: list[SwiftScope], name: str) -> str:
    parts = [scope.name for scope in scopes if scope.name]
    parts.append(name)
    return ".".join(parts)


def swift_symbol_kind(kind: str) -> str:
    if kind == "protocol":
        return "interface"
    if kind == "actor":
        return "type"
    return kind


def symbol_record(
    name: str,
    kind: str,
    visibility: str,
    path: str,
    digest: str,
    *,
    signature: str | None = None,
    doc: str | None = None,
) -> dict[str, Any]:
    symbol: dict[str, Any] = {
        "name": name,
        "kind": kind,
        "visibility": visibility,
        "evidence": evidence_record(path, digest),
    }
    if signature:
        symbol["signature"] = signature
    if doc:
        symbol["doc"] = doc
    return symbol


def collect_declaration(lines: list[str], start: int, *, limit: int = 20) -> str:
    parts: list[str] = []
    paren_depth = 0
    bracket_depth = 0
    angle_depth = 0
    for offset, index in enumerate(range(start, min(len(lines), start + limit))):
        line = lines[index].strip()
        if not line:
            break
        parts.append(line)
        paren_depth += line.count("(") - line.count(")")
        bracket_depth += line.count("[") - line.count("]")
        angle_depth += angle_delta(line)
        if "{" in line:
            break
        if offset > 0 and max(paren_depth, bracket_depth, angle_depth) <= 0:
            break
        if offset == 0 and max(paren_depth, bracket_depth, angle_depth) <= 0:
            break
    return normalize_spaces(" ".join(parts))


def signature_before_body(declaration: str) -> str:
    return normalize_spaces(declaration.split("{", 1)[0].strip())


def property_signature(declaration: str) -> str:
    before_body = declaration.split("{", 1)[0]
    before_default = before_body.split("=", 1)[0]
    return normalize_spaces(before_default.strip())


def property_names(text: str) -> list[str]:
    return [clean_identifier(match.group(0)) for match in re.finditer(IDENTIFIER_RE, text)]


def enum_case_names(text: str) -> list[str]:
    names: list[str] = []
    for part in split_top_level_commas(text.split("{", 1)[0]):
        match = re.match(rf"\s*(?P<name>{IDENTIFIER_RE})", part)
        if match is not None:
            names.append(clean_identifier(match.group("name")))
    return names


def split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(text):
        if char in "([{<":
            depth += 1
        elif char in ")]}>":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])
    return parts


def leading_doc(lines: list[str], start: int) -> str | None:
    docs: list[str] = []
    index = start - 1
    while index >= 0:
        stripped = lines[index].strip()
        if stripped.startswith("///"):
            docs.append(stripped.removeprefix("///").strip())
            index -= 1
            continue
        if stripped.endswith("*/"):
            block, index = collect_block_doc(lines, index)
            if block:
                docs.extend(block)
                continue
        break
    text = "\n".join(reversed([line for line in docs if line])).strip()
    return text or None


def collect_block_doc(lines: list[str], end: int) -> tuple[list[str], int]:
    block: list[str] = []
    index = end
    while index >= 0:
        stripped = lines[index].strip()
        clean = stripped.removesuffix("*/").removeprefix("/**").strip()
        clean = clean.removeprefix("*").strip()
        if clean:
            block.append(clean)
        if stripped.startswith("/**"):
            return block, index - 1
        index -= 1
    return [], end - 1


def brace_delta(line: str) -> int:
    return line.count("{") - line.count("}")


def angle_delta(line: str) -> int:
    delta = 0
    for char in line:
        if char == "<":
            delta += 1
        elif char == ">":
            delta -= 1
    return delta


def clean_identifier(name: str) -> str:
    return ".".join(part.strip("`") for part in name.split("."))


def normalize_spaces(text: str) -> str:
    return " ".join(text.split())


def mask_swift_non_code(text: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith("//", index):
            index = mask_until_newline(text, index, result)
            continue
        if text.startswith("/*", index):
            index = mask_swift_block_comment(text, index, result)
            continue
        if text.startswith('"""', index):
            index = mask_multiline_string(text, index, result)
            continue
        if text[index] == '"':
            index = mask_string(text, index, result)
            continue
        result.append(text[index])
        index += 1
    return "".join(result)


def mask_until_newline(text: str, index: int, result: list[str]) -> int:
    while index < len(text) and text[index] != "\n":
        result.append(" ")
        index += 1
    return index


def mask_multiline_string(text: str, index: int, result: list[str]) -> int:
    result.extend("   ")
    index += 3
    while index < len(text):
        if text.startswith('"""', index):
            result.extend("   ")
            return index + 3
        result.append("\n" if text[index] == "\n" else " ")
        index += 1
    return index


def mask_string(text: str, index: int, result: list[str]) -> int:
    result.append(" ")
    index += 1
    escaped = False
    while index < len(text):
        char = text[index]
        if char == "\n":
            result.append("\n")
            return index + 1
        if char == "\\" and not escaped:
            result.append(" ")
            escaped = True
            index += 1
            continue
        if char == '"' and not escaped:
            result.append(" ")
            return index + 1
        result.append(" ")
        escaped = False
        index += 1
    return index


def diagnostic_sort_key(diagnostic: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(diagnostic.get("level") or ""),
        str(diagnostic.get("path") or ""),
        str(diagnostic.get("message") or ""),
    )


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
