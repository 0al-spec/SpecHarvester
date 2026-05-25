"""Advisory duplicate-code report for local source quality checks.

The detector is intentionally conservative and dependency-free.  It scans local
text files, normalizes significant source lines, and reports repeated line
windows as review signals.  It does not execute source code or import scanned
modules.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CODE_DUPLICATION_REPORT_KIND = "SpecHarvesterCodeDuplicationReport"
CODE_DUPLICATION_REPORT_SCHEMA_VERSION = 1
DEFAULT_MIN_LINES = 8
DEFAULT_EXTENSIONS = (".py",)
EXCLUDED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}

TRUST_BOUNDARY_NOTES = [
    "Code duplication report generation reads local text files only.",
    (
        "No repository code execution, dependency installation, network access, "
        "or imports from scanned modules occur."
    ),
    "The report is advisory by default and does not mutate source files.",
]


@dataclass(frozen=True)
class NormalizedLine:
    path: Path
    line_number: int
    text: str


def build_code_duplication_report(
    paths: list[Path],
    *,
    min_lines: int = DEFAULT_MIN_LINES,
    extensions: tuple[str, ...] = DEFAULT_EXTENSIONS,
) -> dict[str, Any]:
    if min_lines < 2:
        raise ValueError("--min-lines must be at least 2.")
    if not paths:
        raise ValueError("At least one path must be provided.")

    files = list_source_files(paths, extensions=extensions)
    windows: dict[tuple[str, ...], list[dict[str, Any]]] = {}

    for file_path in files:
        lines = normalized_source_lines(file_path)
        if len(lines) < min_lines:
            continue
        for index in range(0, len(lines) - min_lines + 1):
            window = tuple(line.text for line in lines[index : index + min_lines])
            occurrence = {
                "path": file_path.as_posix(),
                "startLine": lines[index].line_number,
                "endLine": lines[index + min_lines - 1].line_number,
            }
            windows.setdefault(window, []).append(occurrence)

    duplicate_blocks = []
    for window, occurrences in windows.items():
        unique_occurrences = _unique_occurrences(occurrences)
        if len(unique_occurrences) < 2:
            continue
        duplicate_blocks.append(
            {
                "fingerprint": _fingerprint(window),
                "lineCount": len(window),
                "normalizedPreview": list(window[: min(3, len(window))]),
                "occurrences": unique_occurrences,
            }
        )

    duplicate_blocks.sort(
        key=lambda block: (
            block["occurrences"][0]["path"],
            block["occurrences"][0]["startLine"],
            block["fingerprint"],
        )
    )
    occurrence_count = sum(len(block["occurrences"]) for block in duplicate_blocks)

    return {
        "schemaVersion": CODE_DUPLICATION_REPORT_SCHEMA_VERSION,
        "kind": CODE_DUPLICATION_REPORT_KIND,
        "status": "attention" if duplicate_blocks else "ok",
        "summary": {
            "pathCount": len(paths),
            "fileCount": len(files),
            "minLines": min_lines,
            "duplicateBlockCount": len(duplicate_blocks),
            "duplicateOccurrenceCount": occurrence_count,
        },
        "duplicates": duplicate_blocks,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def write_code_duplication_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def list_source_files(paths: list[Path], *, extensions: tuple[str, ...]) -> list[Path]:
    files: list[Path] = []
    normalized_extensions = tuple(extension.lower() for extension in extensions)
    for root in paths:
        if not root.exists():
            raise ValueError(f"Scan path does not exist: {root}")
        if root.is_file():
            if _is_supported_source_file(root, normalized_extensions):
                files.append(root)
            continue
        for current_root, dir_names, file_names in os.walk(root):
            dir_names[:] = sorted(name for name in dir_names if name not in EXCLUDED_DIR_NAMES)
            current_path = Path(current_root)
            for file_name in sorted(file_names):
                candidate = current_path / file_name
                if _is_supported_source_file(candidate, normalized_extensions):
                    files.append(candidate)
    return sorted(files, key=lambda path: path.as_posix())


def normalized_source_lines(path: Path) -> list[NormalizedLine]:
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []

    normalized = []
    for index, line in enumerate(raw_lines, start=1):
        text = normalize_source_line(line)
        if text:
            normalized.append(NormalizedLine(path=path, line_number=index, text=text))
    return normalized


def normalize_source_line(line: str) -> str:
    without_comments = _strip_python_comment(line)
    normalized = re.sub(r"\s+", " ", without_comments).strip()
    if normalized.startswith(("from ", "import ")):
        return ""
    if normalized in {"(", ")", "),", "[", "]", "],", "{", "}", "},"}:
        return ""
    return normalized


def _is_supported_source_file(path: Path, extensions: tuple[str, ...]) -> bool:
    return path.suffix.lower() in extensions


def _fingerprint(window: tuple[str, ...]) -> str:
    payload = "\n".join(window).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def _strip_python_comment(line: str) -> str:
    try:
        tokens = tokenize.generate_tokens(io.StringIO(line).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                return line[: token.start[1]]
    except tokenize.TokenError:
        return line
    return line


def _unique_occurrences(occurrences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    unique = []
    for occurrence in occurrences:
        key = (occurrence["path"], occurrence["startLine"], occurrence["endLine"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(occurrence)
    return unique
