from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.architecture_lint import (
    build_architecture_lint_report,
    python_source_paths,
)
from spec_harvester.cli import main


def test_architecture_lint_detects_helper_name_relapse(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_text(
        """
class ReportHelper:
    pass

def make_service():
    pass
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_architecture_lint_report([source])

    assert report["summary"]["issuesByCode"] == {"helper_name_relapse": 1}
    assert report["issues"][0]["name"] == "ReportHelper"


def test_architecture_lint_detects_constructor_io(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_text(
        """
class Manifest:
    def __init__(self, path):
        self.text = path.read_text(encoding="utf-8")
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_architecture_lint_report([source])

    assert report["summary"]["issuesByCode"] == {"constructor_io": 1}
    assert report["issues"][0]["name"] == "Manifest.__init__"


def test_architecture_lint_detects_static_domain_helpers(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_text(
        """
class Manifest:
    @staticmethod
    def parse(value):
        return value

class Allowed:
    @classmethod
    def from_path(cls, path):
        return cls()
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_architecture_lint_report([source])

    assert report["summary"]["issuesByCode"] == {"static_domain_helper": 1}
    assert report["issues"][0]["name"] == "Manifest.parse"


def test_architecture_lint_detects_manifest_parser_pattern(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_text(
        """
def parse_manifest(text):
    parse_state = "root"
    if "metadata:" in text and "foreignArtifacts" in text:
        return parse_state
""".strip()
        + "\n",
        encoding="utf-8",
    )

    report = build_architecture_lint_report([source])

    assert report["summary"]["issuesByCode"] == {"manifest_parser_pattern": 1}


def test_architecture_lint_rejects_missing_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Architecture lint path does not exist"):
        python_source_paths([tmp_path / "missing"])


def test_architecture_lint_deduplicates_overlapping_paths(tmp_path: Path) -> None:
    package = tmp_path / "package"
    package.mkdir()
    source = package / "source.py"
    source.write_text("class Clean:\n    pass\n", encoding="utf-8")

    paths = python_source_paths([tmp_path, package, source])
    report = build_architecture_lint_report([tmp_path, package, source])

    assert paths == [source]
    assert report["summary"]["fileCount"] == 1
    assert report["summary"]["analyzedFileCount"] == 1
    assert report["summary"]["skippedFileCount"] == 0


def test_architecture_lint_reports_unparsed_sources(tmp_path: Path) -> None:
    source = tmp_path / "broken.py"
    source.write_text("def broken(:\n    pass\n", encoding="utf-8")

    report = build_architecture_lint_report([source])

    assert report["status"] == "attention"
    assert report["summary"]["fileCount"] == 1
    assert report["summary"]["analyzedFileCount"] == 0
    assert report["summary"]["skippedFileCount"] == 1
    assert report["summary"]["issuesByCode"] == {"source_file_unavailable": 1}
    assert report["skippedFiles"][0]["path"] == source.as_posix()
    assert report["skippedFiles"][0]["reason"] == "syntax_error"


def test_cli_architecture_lint_writes_output_file(tmp_path: Path, capsys) -> None:
    source = tmp_path / "source.py"
    source.write_text("class Clean:\n    pass\n", encoding="utf-8")
    output = tmp_path / "architecture-lint.json"

    result = main(["architecture-lint", "--path", str(source), "--output", str(output)])

    assert result == 0
    stdout_report = json.loads(capsys.readouterr().out)
    file_report = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_report == file_report
    assert file_report["kind"] == "SpecHarvesterArchitectureLintReport"
    assert file_report["status"] == "ok"


def test_cli_architecture_lint_can_fail_on_issues(tmp_path: Path, capsys) -> None:
    source = tmp_path / "source.py"
    source.write_text("class DataManager:\n    pass\n", encoding="utf-8")

    result = main(["architecture-lint", "--path", str(source), "--fail-on-issues"])

    assert result == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "attention"


def test_cli_architecture_lint_missing_path_errors(tmp_path: Path, capsys) -> None:
    result = main(["architecture-lint", "--path", str(tmp_path / "missing")])

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"


def test_cli_architecture_lint_can_fail_on_unparsed_sources(tmp_path: Path, capsys) -> None:
    source = tmp_path / "broken.py"
    source.write_text("def broken(:\n    pass\n", encoding="utf-8")

    result = main(["architecture-lint", "--path", str(source), "--fail-on-issues"])

    assert result == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"]["skippedFileCount"] == 1
