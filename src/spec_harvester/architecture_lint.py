"""Project-specific architecture lint guardrails.

These checks intentionally cover a narrow set of SpecHarvester refactor risks.
They are not a general Elegant Objects validator.  The report is advisory by
default and should only become blocking after baseline policy is explicit.
"""

from __future__ import annotations

import ast
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ARCHITECTURE_LINT_REPORT_KIND = "SpecHarvesterArchitectureLintReport"
ARCHITECTURE_LINT_SCHEMA_VERSION = 1

HELPER_NAME_RE = re.compile(r"(Helper|Manager|Processor|Service|Utils?)$")
IO_CALLS = {
    "json.loads",
    "open",
    "os.walk",
    "read_text",
    "subprocess.run",
}
IO_CALL_SUFFIXES = (".read_text", ".rglob")
STATIC_ALLOWED_PREFIXES = ("from_",)
STATIC_ALLOWED_NAMES = {"to_dict"}
MANIFEST_PATTERN_TERMS = ("parse_state", "foreignArtifacts", "metadata:")
DEFAULT_PATHS = (Path("src/spec_harvester"),)

TRUST_BOUNDARY_NOTES = [
    "Architecture lint reads local Python source files only.",
    "No repository code execution, dependency installation, network access, or imports occur.",
    "The report is advisory by default and does not mutate source files.",
]


@dataclass(frozen=True)
class SourceFile:
    path: Path
    text: str
    tree: ast.AST


def build_architecture_lint_report(paths: list[Path] | None = None) -> dict[str, Any]:
    roots = paths or list(DEFAULT_PATHS)
    files = read_source_files(roots)
    issues = []
    for source in files:
        issues.extend(helper_name_relapse_issues(source))
        issues.extend(constructor_io_issues(source))
        issues.extend(static_domain_helper_issues(source))
        issues.extend(manifest_parser_pattern_issues(source))
    issues.sort(key=lambda item: (item["path"], item["line"], item["code"], item["name"]))

    issue_counts = {
        code: sum(1 for issue in issues if issue["code"] == code)
        for code in sorted({issue["code"] for issue in issues})
    }

    return {
        "schemaVersion": ARCHITECTURE_LINT_SCHEMA_VERSION,
        "kind": ARCHITECTURE_LINT_REPORT_KIND,
        "status": "attention" if issues else "ok",
        "summary": {
            "pathCount": len(roots),
            "fileCount": len(files),
            "issueCount": len(issues),
            "issuesByCode": issue_counts,
        },
        "issues": issues,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def write_architecture_lint_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_source_files(paths: list[Path]) -> list[SourceFile]:
    files = []
    for path in python_source_paths(paths):
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=path.as_posix())
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        files.append(SourceFile(path=path, text=text, tree=tree))
    return files


def python_source_paths(paths: list[Path]) -> list[Path]:
    source_paths: list[Path] = []
    for root in paths:
        if not root.exists():
            raise ValueError(f"Architecture lint path does not exist: {root}")
        if root.is_file():
            if root.suffix == ".py":
                source_paths.append(root)
            continue
        for current_root, dir_names, file_names in os.walk(root):
            dir_names[:] = sorted(name for name in dir_names if name not in {".git", "__pycache__"})
            for file_name in sorted(file_names):
                candidate = Path(current_root) / file_name
                if candidate.suffix == ".py":
                    source_paths.append(candidate)
    return sorted(source_paths, key=lambda item: item.as_posix())


def helper_name_relapse_issues(source: SourceFile) -> list[dict[str, Any]]:
    issues = []
    for node in ast.walk(source.tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if HELPER_NAME_RE.search(node.name):
                issues.append(
                    issue(
                        source,
                        code="helper_name_relapse",
                        line=node.lineno,
                        name=node.name,
                        message=(
                            "Avoid broad Helper/Manager/Processor/Service/Utils names; "
                            "name the object by owned behavior."
                        ),
                    )
                )
    return issues


def constructor_io_issues(source: SourceFile) -> list[dict[str, Any]]:
    issues = []
    for class_node in [node for node in ast.walk(source.tree) if isinstance(node, ast.ClassDef)]:
        for item in class_node.body:
            if not isinstance(item, ast.FunctionDef) or item.name != "__init__":
                continue
            for call in [node for node in ast.walk(item) if isinstance(node, ast.Call)]:
                call_name = dotted_call_name(call.func)
                if call_name in IO_CALLS or call_name.endswith(IO_CALL_SUFFIXES):
                    issues.append(
                        issue(
                            source,
                            code="constructor_io",
                            line=call.lineno,
                            name=f"{class_node.name}.__init__",
                            message=(
                                "Keep constructors simple; move I/O, parsing, walking, "
                                "or subprocess work into explicit behavior."
                            ),
                        )
                    )
    return issues


def static_domain_helper_issues(source: SourceFile) -> list[dict[str, Any]]:
    issues = []
    for class_node in [node for node in ast.walk(source.tree) if isinstance(node, ast.ClassDef)]:
        for item in class_node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            decorators = {dotted_call_name(decorator) for decorator in item.decorator_list}
            if not decorators.intersection({"staticmethod", "classmethod"}):
                continue
            if item.name in STATIC_ALLOWED_NAMES or item.name.startswith(STATIC_ALLOWED_PREFIXES):
                continue
            issues.append(
                issue(
                    source,
                    code="static_domain_helper",
                    line=item.lineno,
                    name=f"{class_node.name}.{item.name}",
                    message=(
                        "Avoid static/class helper methods in domain objects; prefer "
                        "owned instance behavior or explicit factory naming."
                    ),
                )
            )
    return issues


def manifest_parser_pattern_issues(source: SourceFile) -> list[dict[str, Any]]:
    if source.path.name == "architecture_lint.py":
        return []
    if not all(term in source.text for term in MANIFEST_PATTERN_TERMS):
        return []
    return [
        issue(
            source,
            code="manifest_parser_pattern",
            line=1,
            name=source.path.name,
            message=(
                "This file contains repeated specpm.yaml parser markers; consider "
                "moving manifest parsing into a shared behavior-rich object."
            ),
        )
    ]


def dotted_call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted_call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def issue(
    source: SourceFile,
    *,
    code: str,
    line: int,
    name: str,
    message: str,
) -> dict[str, Any]:
    return {
        "code": code,
        "path": source.path.as_posix(),
        "line": line,
        "name": name,
        "severity": "advisory",
        "message": message,
    }
