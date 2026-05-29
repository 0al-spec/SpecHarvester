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
import shlex
import subprocess
import tempfile
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CODE_DUPLICATION_REPORT_KIND = "SpecHarvesterCodeDuplicationReport"
CODE_DUPLICATION_REPORT_SCHEMA_VERSION = 1
DEFAULT_MIN_LINES = 8
DEFAULT_EXTENSIONS = (".py",)
BACKEND_BUILTIN = "builtin"
BACKEND_PYLINT = "pylint"
BACKEND_JSCPD = "jscpd"
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
JSCPD_TRUST_BOUNDARY_NOTES = [
    "SpecHarvester converts jscpd JSON output and does not execute or import scanned modules.",
    "The operator-provided jscpd command is an external tool trust boundary.",
    (
        "Network access or package installation by wrapper commands such as npx "
        "is outside SpecHarvester."
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
    backend: str = BACKEND_BUILTIN,
    pylint_command: str = "pylint",
    jscpd_command: str = "jscpd",
) -> dict[str, Any]:
    if min_lines < 2:
        raise ValueError("--min-lines must be at least 2.")
    if not paths:
        raise ValueError("At least one path must be provided.")
    if backend == BACKEND_PYLINT:
        return build_pylint_code_duplication_report(
            paths,
            min_lines=min_lines,
            extensions=extensions,
            pylint_command=pylint_command,
        )
    if backend == BACKEND_JSCPD:
        return build_jscpd_code_duplication_report(
            paths,
            min_lines=min_lines,
            jscpd_command=jscpd_command,
        )
    if backend != BACKEND_BUILTIN:
        raise ValueError(f"Unsupported duplicate-code backend: {backend}")

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
            "backend": BACKEND_BUILTIN,
            "pathCount": len(paths),
            "fileCount": len(files),
            "minLines": min_lines,
            "duplicateBlockCount": len(duplicate_blocks),
            "duplicateOccurrenceCount": occurrence_count,
        },
        "duplicates": duplicate_blocks,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def build_pylint_code_duplication_report(
    paths: list[Path],
    *,
    min_lines: int = DEFAULT_MIN_LINES,
    extensions: tuple[str, ...] = DEFAULT_EXTENSIONS,
    pylint_command: str = "pylint",
) -> dict[str, Any]:
    files = list_source_files(paths, extensions=extensions)
    if not files:
        return _new_report(
            paths=paths,
            files=files,
            min_lines=min_lines,
            backend=BACKEND_PYLINT,
            duplicates=[],
            tool={"name": "pylint", "messageCount": 0},
        )

    command = [
        pylint_command,
        "--disable=all",
        "--enable=duplicate-code",
        f"--min-similarity-lines={min_lines}",
        "--output-format=json",
        *[path.as_posix() for path in files],
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ValueError(f"Cannot run pylint duplicate-code backend: {exc}") from exc

    _validate_pylint_result(completed)
    stdout = completed.stdout.strip()
    try:
        messages = json.loads(stdout or "[]")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid pylint JSON output: {exc.msg}") from exc
    if not isinstance(messages, list):
        raise ValueError("Invalid pylint JSON output: expected a list.")

    module_map = _source_file_module_map(files)
    duplicates = [
        _pylint_message_to_duplicate_block(message, module_map)
        for message in messages
        if isinstance(message, dict) and message.get("message-id") == "R0801"
    ]
    duplicate_blocks = [block for block in duplicates if block is not None]
    duplicate_blocks.sort(
        key=lambda block: (
            block["occurrences"][0]["path"],
            block["occurrences"][0]["startLine"],
            block["fingerprint"],
        )
    )

    return _new_report(
        paths=paths,
        files=files,
        min_lines=min_lines,
        backend=BACKEND_PYLINT,
        duplicates=duplicate_blocks,
        tool={
            "name": "pylint",
            "messageCount": len(messages),
            "returnCode": completed.returncode,
        },
    )


def build_jscpd_code_duplication_report(
    paths: list[Path],
    *,
    min_lines: int = DEFAULT_MIN_LINES,
    jscpd_command: str = "jscpd",
) -> dict[str, Any]:
    command_prefix = shlex.split(jscpd_command)
    if not command_prefix:
        raise ValueError("Cannot run jscpd duplicate-code backend: command is empty.")
    with tempfile.TemporaryDirectory(prefix="specharvester-jscpd-") as output_dir:
        output_path = Path(output_dir)
        command = [
            *command_prefix,
            "--reporters",
            "json",
            "--output",
            output_path.as_posix(),
            "--min-lines",
            str(min_lines),
            "--mode",
            "weak",
            "--silent",
            "--exitCode",
            "0",
            "--ignore",
            _jscpd_ignore_patterns(),
            *[path.as_posix() for path in paths],
        ]
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise ValueError(f"Cannot run jscpd duplicate-code backend: {exc}") from exc

        _validate_jscpd_result(completed)
        report_path = output_path / "jscpd-report.json"
        try:
            payload = json.loads(report_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError("Invalid jscpd output: jscpd-report.json was not created.") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid jscpd JSON output: {exc.msg}") from exc

    reported_source_count = _jscpd_reported_source_count(payload)
    duplicates = _jscpd_duplicate_blocks(payload)
    duplicates.sort(
        key=lambda block: (
            block["occurrences"][0]["path"],
            block["occurrences"][0]["startLine"],
            block["fingerprint"],
        )
    )

    return _new_report(
        paths=paths,
        files=[],
        min_lines=min_lines,
        backend=BACKEND_JSCPD,
        duplicates=duplicates,
        file_count=reported_source_count,
        trust_boundary=JSCPD_TRUST_BOUNDARY_NOTES,
        tool={
            "name": "jscpd",
            "returnCode": completed.returncode,
            "reportedSourceCount": reported_source_count,
        },
    )


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


def _fingerprint_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _validate_pylint_result(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.returncode not in {0, 8}:
        stderr = completed.stderr.strip()
        detail = f" stderr: {stderr}" if stderr else ""
        raise ValueError(
            f"Pylint duplicate-code backend failed with return code {completed.returncode}.{detail}"
        )
    if completed.returncode != 0 and not completed.stdout.strip():
        stderr = completed.stderr.strip()
        detail = f" stderr: {stderr}" if stderr else ""
        raise ValueError(
            "Pylint duplicate-code backend failed without JSON output "
            f"(return code {completed.returncode}).{detail}"
        )


def _validate_jscpd_result(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        detail = f" stderr: {stderr}" if stderr else ""
        raise ValueError(
            f"jscpd duplicate-code backend failed with return code {completed.returncode}.{detail}"
        )


def _new_report(
    *,
    paths: list[Path],
    files: list[Path],
    min_lines: int,
    backend: str,
    duplicates: list[dict[str, Any]],
    file_count: int | None = None,
    trust_boundary: list[str] | None = None,
    tool: dict[str, Any] | None = None,
) -> dict[str, Any]:
    occurrence_count = sum(len(block["occurrences"]) for block in duplicates)
    summary: dict[str, Any] = {
        "backend": backend,
        "pathCount": len(paths),
        "fileCount": len(files) if file_count is None else file_count,
        "minLines": min_lines,
        "duplicateBlockCount": len(duplicates),
        "duplicateOccurrenceCount": occurrence_count,
    }
    if tool is not None:
        summary["tool"] = tool
    return {
        "schemaVersion": CODE_DUPLICATION_REPORT_SCHEMA_VERSION,
        "kind": CODE_DUPLICATION_REPORT_KIND,
        "status": "attention" if duplicates else "ok",
        "summary": summary,
        "duplicates": duplicates,
        "trustBoundary": TRUST_BOUNDARY_NOTES if trust_boundary is None else trust_boundary,
    }


def _jscpd_ignore_patterns() -> str:
    return ",".join(f"**/{name}/**" for name in sorted(EXCLUDED_DIR_NAMES))


def _jscpd_duplicate_blocks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    duplicates = payload.get("duplicates")
    if not isinstance(duplicates, list):
        raise ValueError("Invalid jscpd JSON output: duplicates must be a list.")
    return [_jscpd_duplicate_block(item) for item in duplicates]


def _jscpd_duplicate_block(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError("Invalid jscpd JSON output: duplicate item must be an object.")
    occurrences = _unique_occurrences(
        [
            _jscpd_file_occurrence(item.get("firstFile")),
            _jscpd_file_occurrence(item.get("secondFile")),
        ]
    )
    if len(occurrences) < 2:
        raise ValueError("Invalid jscpd JSON output: duplicate requires two file occurrences.")
    fragment = str(item.get("fragment") or "")
    preview = [line.strip() for line in fragment.splitlines() if line.strip()]
    fingerprint_payload = {
        "format": item.get("format"),
        "fragment": fragment,
        "occurrences": occurrences,
    }
    return {
        "fingerprint": _fingerprint_text(json.dumps(fingerprint_payload, sort_keys=True)),
        "lineCount": _jscpd_line_count(item, occurrences),
        "normalizedPreview": preview[:3],
        "occurrences": occurrences,
    }


def _jscpd_file_occurrence(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Invalid jscpd JSON output: file occurrence must be an object.")
    path = value.get("name")
    if not isinstance(path, str) or not path:
        raise ValueError("Invalid jscpd JSON output: file occurrence requires a name.")
    start_line = _jscpd_line_value(value, "start", "startLoc")
    end_line = _jscpd_line_value(value, "end", "endLoc")
    if end_line < start_line:
        raise ValueError("Invalid jscpd JSON output: occurrence end line precedes start line.")
    return {
        "path": path,
        "startLine": start_line,
        "endLine": end_line,
    }


def _jscpd_line_value(value: dict[str, Any], direct_key: str, loc_key: str) -> int:
    direct = value.get(direct_key)
    if isinstance(direct, int):
        return direct
    location = value.get(loc_key)
    if isinstance(location, dict) and isinstance(location.get("line"), int):
        return location["line"]
    raise ValueError(f"Invalid jscpd JSON output: missing {direct_key} line.")


def _jscpd_line_count(item: dict[str, Any], occurrences: list[dict[str, Any]]) -> int:
    lines = item.get("lines")
    if isinstance(lines, int) and lines >= 0:
        return lines
    first = occurrences[0]
    return first["endLine"] - first["startLine"] + 1


def _jscpd_reported_source_count(payload: dict[str, Any]) -> int:
    statistics = payload.get("statistics")
    if not isinstance(statistics, dict):
        statistics = payload.get("statistic")
    if not isinstance(statistics, dict):
        return 0
    total = statistics.get("total")
    if not isinstance(total, dict):
        return 0
    sources = total.get("sources")
    return sources if isinstance(sources, int) else 0


def _source_file_module_map(files: list[Path]) -> dict[str, Path]:
    module_map: dict[str, Path] = {}
    for path in files:
        without_suffix = path.with_suffix("")
        posix_key = without_suffix.as_posix()
        dotted_key = ".".join(without_suffix.parts)
        for key in {
            path.stem,
            posix_key,
            dotted_key,
            _strip_src_prefix(dotted_key),
        }:
            module_map[key] = path
    return module_map


def _strip_src_prefix(value: str) -> str:
    return value[4:] if value.startswith("src.") else value


def _pylint_message_to_duplicate_block(
    message: dict[str, Any],
    module_map: dict[str, Path],
) -> dict[str, Any] | None:
    message_text = str(message.get("message", ""))
    occurrences = []
    for line in message_text.splitlines():
        match = re.match(r"^==(?P<module>.+):\[(?P<start>\d+):(?P<end>\d+)\]$", line)
        if match is None:
            continue
        module = match.group("module")
        occurrences.append(
            {
                "path": _pylint_module_path(module, module_map),
                "startLine": int(match.group("start")),
                "endLine": int(match.group("end")),
            }
        )
    occurrences = _unique_occurrences(occurrences)
    if len(occurrences) < 2:
        return None

    preview = _pylint_message_preview(message_text)
    return {
        "fingerprint": _fingerprint_text(message_text),
        "lineCount": max(0, occurrences[0]["endLine"] - occurrences[0]["startLine"] + 1),
        "normalizedPreview": preview[:3],
        "occurrences": occurrences,
    }


def _pylint_module_path(module: str, module_map: dict[str, Path]) -> str:
    path = module_map.get(module)
    if path is not None:
        return path.as_posix()
    for key, candidate in module_map.items():
        if key.endswith(f".{module}") or module.endswith(f".{key}"):
            return candidate.as_posix()
    return module


def _pylint_message_preview(message: str) -> list[str]:
    preview = []
    for line in message.splitlines():
        if not line.strip() or line.startswith("Similar lines") or line.startswith("=="):
            continue
        preview.append(line.strip())
    return preview


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
