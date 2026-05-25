from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import spec_harvester.code_duplication_report as code_duplication_report
from spec_harvester.cli import main
from spec_harvester.code_duplication_report import (
    build_code_duplication_report,
    build_pylint_code_duplication_report,
    list_source_files,
    normalize_source_line,
    normalized_source_lines,
)


def test_build_code_duplication_report_detects_repeated_blocks(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    (source / "alpha.py").write_text(
        """
def first(value):
    total = value + 1
    result = total * 2
    return result
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (source / "beta.py").write_text(
        """
def second(value):
    total = value + 1
    result = total * 2
    return result
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_code_duplication_report([source], min_lines=3)

    assert report["kind"] == "SpecHarvesterCodeDuplicationReport"
    assert report["status"] == "attention"
    assert report["summary"]["duplicateBlockCount"] == 1
    duplicate = report["duplicates"][0]
    assert duplicate["lineCount"] == 3
    assert [Path(item["path"]).name for item in duplicate["occurrences"]] == [
        "alpha.py",
        "beta.py",
    ]


def test_code_duplication_report_ignores_comments_and_blank_lines(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    (source / "alpha.py").write_text(
        """
def shared(value):
    # local explanation
    total = value + 1

    return total
""".strip()
        + "\n",
        encoding="utf-8",
    )
    (source / "beta.py").write_text(
        """
def shared(value):
    total = value + 1  # inline explanation
    return total
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_code_duplication_report([source], min_lines=3)

    assert report["summary"]["duplicateBlockCount"] == 1
    assert report["duplicates"][0]["normalizedPreview"] == [
        "def shared(value):",
        "total = value + 1",
        "return total",
    ]


def test_normalize_source_line_removes_comments_and_collapses_spacing() -> None:
    assert normalize_source_line("    total   = value + 1  # comment") == "total = value + 1"
    assert normalize_source_line('line = raw_line.split("#", maxsplit=1)[0]') == (
        'line = raw_line.split("#", maxsplit=1)[0]'
    )
    assert normalize_source_line("from pathlib import Path") == ""
    assert normalize_source_line("   # comment only") == ""


def test_list_source_files_rejects_missing_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Scan path does not exist"):
        list_source_files([tmp_path / "missing"], extensions=(".py",))


def test_list_source_files_prunes_excluded_children_but_not_explicit_root(
    tmp_path: Path,
) -> None:
    explicit_build_root = tmp_path / "build" / "project"
    explicit_build_root.mkdir(parents=True)
    explicit_file = explicit_build_root / "alpha.py"
    explicit_file.write_text("a = 1\n", encoding="utf-8")
    nested_excluded = explicit_build_root / "node_modules"
    nested_excluded.mkdir()
    (nested_excluded / "ignored.py").write_text("b = 2\n", encoding="utf-8")

    assert list_source_files([explicit_build_root], extensions=(".py",)) == [explicit_file]


def test_normalized_source_lines_skips_io_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.py"
    source.write_text("a = 1\n", encoding="utf-8")

    def raise_os_error(path: Path, *, encoding: str) -> str:
        raise OSError("not readable")

    monkeypatch.setattr(code_duplication_report.Path, "read_text", raise_os_error)

    assert normalized_source_lines(source) == []


def test_cli_code_duplication_report_writes_output_file(tmp_path: Path, capsys) -> None:
    source = tmp_path / "src"
    source.mkdir()
    (source / "alpha.py").write_text("a = 1\nb = 2\n", encoding="utf-8")
    (source / "beta.py").write_text("a = 1\nb = 2\n", encoding="utf-8")
    output = tmp_path / "report.json"

    result = main(
        [
            "code-duplication-report",
            "--path",
            str(source),
            "--min-lines",
            "2",
            "--output",
            str(output),
        ]
    )

    assert result == 0
    stdout_report = json.loads(capsys.readouterr().out)
    file_report = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_report == file_report
    assert file_report["summary"]["duplicateBlockCount"] == 1


def test_cli_code_duplication_report_can_fail_on_duplicates(tmp_path: Path, capsys) -> None:
    source = tmp_path / "src"
    source.mkdir()
    (source / "alpha.py").write_text("a = 1\nb = 2\n", encoding="utf-8")
    (source / "beta.py").write_text("a = 1\nb = 2\n", encoding="utf-8")

    result = main(
        [
            "code-duplication-report",
            "--path",
            str(source),
            "--min-lines",
            "2",
            "--fail-on-duplicates",
        ]
    )

    assert result == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "attention"


def test_pylint_backend_converts_r0801_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "src"
    source.mkdir()
    alpha = source / "alpha.py"
    beta = source / "beta.py"
    alpha.write_text("a = 1\nb = 2\nc = 3\n", encoding="utf-8")
    beta.write_text("a = 1\nb = 2\nc = 3\n", encoding="utf-8")

    def fake_run(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        assert command[:4] == [
            "pylint",
            "--disable=all",
            "--enable=duplicate-code",
            "--min-similarity-lines=3",
        ]
        assert check is False
        assert capture_output is True
        assert text is True
        payload = [
            {
                "message-id": "R0801",
                "message": ("Similar lines in 2 files\n==alpha:[1:3]\n==beta:[1:3]\na = 1\nb = 2"),
            }
        ]
        return subprocess.CompletedProcess(command, 8, json.dumps(payload), "")

    monkeypatch.setattr(code_duplication_report.subprocess, "run", fake_run)

    report = build_pylint_code_duplication_report([source], min_lines=3)

    assert report["summary"]["backend"] == "pylint"
    assert report["summary"]["tool"]["name"] == "pylint"
    assert report["summary"]["tool"]["returnCode"] == 8
    assert report["summary"]["duplicateBlockCount"] == 1
    duplicate = report["duplicates"][0]
    assert duplicate["lineCount"] == 3
    assert duplicate["normalizedPreview"] == ["a = 1", "b = 2"]
    assert [Path(item["path"]).name for item in duplicate["occurrences"]] == [
        "alpha.py",
        "beta.py",
    ]


def test_pylint_backend_reports_missing_tool(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_text("a = 1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Cannot run pylint duplicate-code backend"):
        build_pylint_code_duplication_report(
            [source],
            min_lines=3,
            pylint_command="missing-pylint-command",
        )


def test_pylint_backend_fails_closed_on_usage_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.py"
    source.write_text("a = 1\n", encoding="utf-8")

    def fake_run(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 32, "[]", "bad invocation")

    monkeypatch.setattr(code_duplication_report.subprocess, "run", fake_run)

    with pytest.raises(ValueError, match="return code 32"):
        build_pylint_code_duplication_report([source], min_lines=3)


def test_pylint_backend_fails_closed_on_empty_error_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.py"
    source.write_text("a = 1\n", encoding="utf-8")

    def fake_run(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 8, "", "duplicate-code failed")

    monkeypatch.setattr(code_duplication_report.subprocess, "run", fake_run)

    with pytest.raises(ValueError, match="without JSON output"):
        build_pylint_code_duplication_report([source], min_lines=3)


def test_cli_code_duplication_report_accepts_pylint_backend(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    source = tmp_path / "source.py"
    source.write_text("a = 1\n", encoding="utf-8")

    def fake_run(
        command: list[str],
        *,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0, "[]", "")

    monkeypatch.setattr(code_duplication_report.subprocess, "run", fake_run)

    result = main(
        [
            "code-duplication-report",
            "--backend",
            "pylint",
            "--path",
            str(source),
        ]
    )

    assert result == 0
    report = json.loads(capsys.readouterr().out)
    assert report["summary"]["backend"] == "pylint"
    assert report["summary"]["duplicateBlockCount"] == 0


def test_cli_code_duplication_report_rejects_tiny_windows(capsys) -> None:
    result = main(["code-duplication-report", "--min-lines", "1"])

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"


def test_cli_code_duplication_report_rejects_missing_path(tmp_path: Path, capsys) -> None:
    result = main(["code-duplication-report", "--path", str(tmp_path / "missing")])

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "Scan path does not exist" in payload["message"]
