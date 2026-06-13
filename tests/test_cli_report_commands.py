from __future__ import annotations

import argparse
import json
from pathlib import Path

from spec_harvester.cli_report_commands import (
    ArchitectureLintCommand,
    CodeDuplicationReportCommand,
    ProceduralStyleReportCommand,
)


def test_code_duplication_command_preserves_output_and_fail_policy(
    tmp_path: Path,
    capsys,
) -> None:
    source = tmp_path / "src"
    source.mkdir()
    (source / "alpha.py").write_text("a = 1\nb = 2\n", encoding="utf-8")
    (source / "beta.py").write_text("a = 1\nb = 2\n", encoding="utf-8")
    output = tmp_path / "duplicates.json"
    args = argparse.Namespace(
        path=[source],
        min_lines=2,
        backend="builtin",
        pylint_command="pylint",
        jscpd_command="jscpd",
        output=output,
        fail_on_duplicates=True,
    )

    result = CodeDuplicationReportCommand(args).run()

    assert result == 1
    stdout_report = json.loads(capsys.readouterr().out)
    file_report = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_report == file_report
    assert file_report["kind"] == "SpecHarvesterCodeDuplicationReport"
    assert file_report["summary"]["duplicateBlockCount"] == 1


def test_architecture_lint_command_preserves_output_file_behavior(
    tmp_path: Path,
    capsys,
) -> None:
    source = tmp_path / "source.py"
    source.write_text("class Clean:\n    pass\n", encoding="utf-8")
    output = tmp_path / "architecture-lint.json"
    args = argparse.Namespace(path=[source], output=output, fail_on_issues=False)

    result = ArchitectureLintCommand(args).run()

    assert result == 0
    stdout_report = json.loads(capsys.readouterr().out)
    file_report = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_report == file_report
    assert file_report["kind"] == "SpecHarvesterArchitectureLintReport"
    assert file_report["summary"]["issueCount"] == 0


def test_architecture_lint_command_preserves_json_error_exit(
    tmp_path: Path,
    capsys,
) -> None:
    args = argparse.Namespace(path=[tmp_path / "missing"], output=None, fail_on_issues=False)

    result = ArchitectureLintCommand(args).run()

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "Architecture lint path does not exist" in payload["message"]


def test_procedural_style_command_preserves_error_mapping(
    tmp_path: Path,
    capsys,
) -> None:
    args = argparse.Namespace(
        path=[tmp_path / "missing"],
        output=None,
        hotspot_min_top_level_count=15,
        hotspot_min_top_level_span=300,
        fail_on_hotspots=False,
    )

    result = ProceduralStyleReportCommand(args).run()

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert payload["message"].startswith("Procedural style report path does not exist:")
    assert "Architecture lint" not in payload["message"]


def test_procedural_style_command_preserves_hotspot_fail_policy(
    tmp_path: Path,
    capsys,
) -> None:
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
    args = argparse.Namespace(
        path=[source],
        output=None,
        hotspot_min_top_level_count=3,
        hotspot_min_top_level_span=300,
        fail_on_hotspots=True,
    )

    result = ProceduralStyleReportCommand(args).run()

    assert result == 1
    report = json.loads(capsys.readouterr().out)
    assert report["kind"] == "SpecHarvesterProceduralStyleReport"
    assert report["summary"]["hotspotCount"] == 1
