from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.procedural_style_report import (
    PROCEDURAL_STYLE_REPORT_KIND,
    build_procedural_style_report,
)


def test_procedural_style_report_counts_top_level_and_method_span(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_text(
        """
from dataclasses import dataclass


@dataclass
class Pair:
    left: int
    right: int


class Rich:
    def first(self):
        return 1

    def second(self):
        return 2


def alpha():
    value = 1
    return value


def beta():
    result = 2
    return result
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_procedural_style_report([source], hotspot_min_top_level_count=3)

    assert report["kind"] == PROCEDURAL_STYLE_REPORT_KIND
    assert report["status"] == "ok"
    assert report["summary"]["fileCount"] == 1
    assert report["summary"]["topLevelFunctionCount"] == 2
    assert report["summary"]["methodCount"] == 2
    assert report["summary"]["behaviorRichClassCount"] == 1
    assert report["summary"]["dtoOnlyClassCount"] == 1
    assert report["summary"]["exceptionLikeClassCount"] == 0
    assert report["summary"]["hotspotCount"] == 0
    metric = report["fileMetrics"][0]
    assert metric["path"] == source.as_posix()
    assert metric["topLevelFunctionCount"] == 2
    assert metric["methodCount"] == 2
    assert metric["behaviorRichClassCount"] == 1
    assert metric["dtoOnlyClassCount"] == 1
    assert report["largestTopLevelFunctions"][0]["name"] == "alpha"


def test_procedural_style_report_detects_hotspots_by_top_level_count(tmp_path: Path) -> None:
    source = tmp_path / "hotspot.py"
    source.write_text(
        """
def one():
    return 1


def two():
    return 2


def three():
    return 3
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_procedural_style_report([source], hotspot_min_top_level_count=3)

    assert report["status"] == "attention"
    assert report["summary"]["hotspotCount"] == 1
    assert report["hotspots"][0]["path"] == source.as_posix()


def test_procedural_style_report_detects_exception_like_classes(tmp_path: Path) -> None:
    source = tmp_path / "errors.py"
    source.write_text(
        """
class CustomError(Exception):
    pass
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_procedural_style_report([source], hotspot_min_top_level_count=3)

    assert report["summary"]["classCount"] == 1
    assert report["summary"]["exceptionLikeClassCount"] == 1
    assert report["summary"]["behaviorRichClassCount"] == 0
    assert report["summary"]["dtoOnlyClassCount"] == 0


def test_procedural_style_report_reports_unparsed_sources(tmp_path: Path) -> None:
    source = tmp_path / "broken.py"
    source.write_text("def broken(:\n    pass\n", encoding="utf-8")

    report = build_procedural_style_report([source])

    assert report["summary"]["fileCount"] == 1
    assert report["summary"]["analyzedFileCount"] == 0
    assert report["summary"]["skippedFileCount"] == 1
    assert report["skippedFiles"][0]["reason"] == "syntax_error"


def test_procedural_style_report_rejects_invalid_hotspot_thresholds(tmp_path: Path) -> None:
    source = tmp_path / "clean.py"
    source.write_text("def clean():\n    return 1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="--hotspot-min-top-level-count"):
        build_procedural_style_report([source], hotspot_min_top_level_count=0)


def test_cli_procedural_style_report_writes_output_file(tmp_path: Path, capsys) -> None:
    source = tmp_path / "source.py"
    source.write_text("def clean():\n    return 1\n", encoding="utf-8")
    output = tmp_path / "procedural-style.json"

    result = main(["procedural-style-report", "--path", str(source), "--output", str(output)])

    assert result == 0
    stdout_report = json.loads(capsys.readouterr().out)
    file_report = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_report == file_report
    assert file_report["kind"] == PROCEDURAL_STYLE_REPORT_KIND


def test_cli_procedural_style_report_can_fail_on_hotspots(tmp_path: Path, capsys) -> None:
    source = tmp_path / "source.py"
    source.write_text(
        """
def one():
    return 1


def two():
    return 2


def three():
    return 3
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = main(
        [
            "procedural-style-report",
            "--path",
            str(source),
            "--hotspot-min-top-level-count",
            "3",
            "--fail-on-hotspots",
        ]
    )

    assert result == 1
    report = json.loads(capsys.readouterr().out)
    assert report["summary"]["hotspotCount"] == 1


def test_cli_procedural_style_report_missing_path_errors(tmp_path: Path, capsys) -> None:
    result = main(["procedural-style-report", "--path", str(tmp_path / "missing")])

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
