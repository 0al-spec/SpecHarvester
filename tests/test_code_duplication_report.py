from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.code_duplication_report import (
    build_code_duplication_report,
    normalize_source_line,
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


def test_cli_code_duplication_report_rejects_tiny_windows(capsys) -> None:
    result = main(["code-duplication-report", "--min-lines", "1"])

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
