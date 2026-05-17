from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Any

from spec_harvester.interface_index import (
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    validate_public_interface_index,
)

PYTHON_PUBLIC_API_ANALYZER_ID = "python-ast-public-api"
PYTHON_PUBLIC_API_ANALYZER_VERSION = "0.1.0"

IGNORED_DIR_NAMES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "venv",
}


def analyze_python_public_api(
    source: Path,
    *,
    package_id: str | None = None,
    source_revision: str | None = None,
) -> dict[str, Any]:
    root = source.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Python source root does not exist or is not a directory: {source}")

    entrypoints: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for path in python_source_files(root):
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        text = data.decode("utf-8", errors="replace")
        try:
            module = ast.parse(text, filename=relative)
        except (SyntaxError, ValueError) as exc:
            diagnostics.append(parse_diagnostic(relative, digest, exc))
            continue

        symbols = module_symbols(module, relative, digest)
        entrypoints.append(
            {
                "path": relative,
                "symbols": symbols,
            }
        )

    index = new_public_interface_index(
        source_revision=source_revision,
        analyzers=[
            analyzer_record(
                PYTHON_PUBLIC_API_ANALYZER_ID,
                PYTHON_PUBLIC_API_ANALYZER_VERSION,
                execution="none",
                confidence="high",
            )
        ],
        packages=[
            {
                "id": package_id or root.name,
                "path": ".",
                "language": "python",
                "entrypoints": entrypoints,
            }
        ],
        diagnostics=diagnostics,
    )
    validate_public_interface_index(index)
    return index


def python_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if should_skip(path, root):
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def should_skip(path: Path, root: Path) -> bool:
    if path.is_symlink() or not path.is_file():
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in IGNORED_DIR_NAMES for part in relative.parts[:-1])


def parse_diagnostic(path: str, digest: str, exc: SyntaxError | ValueError) -> dict[str, Any]:
    if isinstance(exc, SyntaxError):
        message = exc.msg
        if exc.lineno is not None:
            message = f"{message} at line {exc.lineno}"
    else:
        message = str(exc)
    return {
        "level": "error",
        "path": path,
        "message": message,
        "evidence": evidence_record(path, digest),
    }


def module_symbols(module: ast.Module, path: str, digest: str) -> list[dict[str, Any]]:
    explicit_exports = module_all_exports(module)
    symbols: list[dict[str, Any]] = []
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if include_name(node.name, explicit_exports):
                symbols.append(function_symbol(node, node.name, path, digest))
            continue
        if isinstance(node, ast.ClassDef):
            if include_name(node.name, explicit_exports):
                symbols.append(class_symbol(node, path, digest))
                symbols.extend(class_method_symbols(node, path, digest))
            continue
        for name in assignment_names(node):
            if name == "__all__":
                continue
            if include_name(name, explicit_exports):
                symbols.append(assignment_symbol(name, path, digest))
    return symbols


def module_all_exports(module: ast.Module) -> set[str] | None:
    for node in module.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets: list[ast.expr] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
            value = node.value
        else:
            targets = [node.target]
            value = node.value
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
            continue
        exports = string_sequence(value)
        if exports is not None:
            return exports
    return None


def string_sequence(node: ast.AST | None) -> set[str] | None:
    if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return None
    exports: set[str] = set()
    for item in node.elts:
        if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
            return None
        exports.add(item.value)
    return exports


def include_name(name: str, explicit_exports: set[str] | None) -> bool:
    if explicit_exports is not None:
        return name in explicit_exports
    return not name.startswith("_")


def function_symbol(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    name: str,
    path: str,
    digest: str,
) -> dict[str, Any]:
    symbol: dict[str, Any] = {
        "name": name,
        "kind": "function",
        "visibility": "public",
        "signature": function_signature(node, name),
        "evidence": evidence_record(path, digest),
    }
    doc = ast.get_docstring(node)
    if doc:
        symbol["doc"] = doc
    return symbol


def class_symbol(node: ast.ClassDef, path: str, digest: str) -> dict[str, Any]:
    symbol: dict[str, Any] = {
        "name": node.name,
        "kind": "class",
        "visibility": "public",
        "evidence": evidence_record(path, digest),
    }
    doc = ast.get_docstring(node)
    if doc:
        symbol["doc"] = doc
    return symbol


def class_method_symbols(node: ast.ClassDef, path: str, digest: str) -> list[dict[str, Any]]:
    symbols: list[dict[str, Any]] = []
    for child in node.body:
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if child.name.startswith("_"):
            continue
        symbols.append(function_symbol(child, f"{node.name}.{child.name}", path, digest))
    return symbols


def assignment_symbol(name: str, path: str, digest: str) -> dict[str, Any]:
    return {
        "name": name,
        "kind": "constant" if name.isupper() else "variable",
        "visibility": "public",
        "evidence": evidence_record(path, digest),
    }


def assignment_names(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Assign):
        return [
            name
            for target in node.targets
            for name in target_names(target)
            if isinstance(name, str)
        ]
    if isinstance(node, ast.AnnAssign):
        return target_names(node.target)
    return []


def target_names(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        return [
            name for element in node.elts for name in target_names(element) if isinstance(name, str)
        ]
    return []


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef, name: str) -> str:
    args = node.args
    parts: list[str] = []

    positional = list(args.posonlyargs) + list(args.args)
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    for arg, default in zip(positional, defaults):
        parts.append(argument_text(arg, default))

    if args.vararg is not None:
        parts.append("*" + annotated_name(args.vararg))
    elif args.kwonlyargs:
        parts.append("*")

    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(argument_text(arg, default))

    if args.kwarg is not None:
        parts.append("**" + annotated_name(args.kwarg))

    result = f"{name}({', '.join(parts)})"
    returns = unparse_or_none(node.returns)
    if returns:
        result = f"{result} -> {returns}"
    return result


def argument_text(arg: ast.arg, default: ast.expr | None) -> str:
    text = annotated_name(arg)
    if default is not None:
        separator = " = " if arg.annotation is not None else "="
        text = f"{text}{separator}{unparse_or_none(default) or '...'}"
    return text


def annotated_name(arg: ast.arg) -> str:
    annotation = unparse_or_none(arg.annotation)
    return f"{arg.arg}: {annotation}" if annotation else arg.arg


def unparse_or_none(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None
