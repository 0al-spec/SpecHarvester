"""CLI command objects for local advisory report generation."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from spec_harvester.architecture_lint import (
    build_architecture_lint_report,
    write_architecture_lint_report,
)
from spec_harvester.code_duplication_report import (
    build_code_duplication_report,
    write_code_duplication_report,
)
from spec_harvester.procedural_style_report import (
    build_procedural_style_report,
    write_procedural_style_report,
)

ReportWriter = Callable[[Path, dict[str, Any]], None]


@dataclass(frozen=True)
class JsonReportOutput:
    path: Path | None

    def write(self, report: dict[str, Any], writer: ReportWriter) -> None:
        if self.path is not None:
            writer(self.path, report)
        print(json.dumps(report, indent=2, sort_keys=True))


@dataclass(frozen=True)
class CodeDuplicationReportCommand:
    args: argparse.Namespace

    def run(self) -> int:
        try:
            result = self.build_report()
        except ValueError as exc:
            print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
            return 2
        self.write_result(result)
        return self.exit_code_for(result)

    def build_report(self) -> dict[str, Any]:
        return build_code_duplication_report(
            self.paths(),
            min_lines=self.args.min_lines,
            backend=self.args.backend,
            pylint_command=self.args.pylint_command,
            jscpd_command=self.args.jscpd_command,
        )

    def paths(self) -> list[Path]:
        return self.args.path or [Path("src/spec_harvester")]

    def write_result(self, report: dict[str, Any]) -> None:
        JsonReportOutput(self.args.output).write(report, write_code_duplication_report)

    def exit_code_for(self, report: dict[str, Any]) -> int:
        if self.args.fail_on_duplicates and report["summary"]["duplicateBlockCount"] > 0:
            return 1
        return 0


@dataclass(frozen=True)
class ArchitectureLintCommand:
    args: argparse.Namespace

    def run(self) -> int:
        try:
            result = self.build_report()
        except ValueError as exc:
            print(json.dumps({"status": "error", "message": str(exc)}, indent=2))
            return 2
        self.write_result(result)
        return self.exit_code_for(result)

    def build_report(self) -> dict[str, Any]:
        return build_architecture_lint_report(self.paths())

    def paths(self) -> list[Path]:
        return self.args.path or [Path("src/spec_harvester")]

    def write_result(self, report: dict[str, Any]) -> None:
        JsonReportOutput(self.args.output).write(report, write_architecture_lint_report)

    def exit_code_for(self, report: dict[str, Any]) -> int:
        if self.args.fail_on_issues and report["summary"]["issueCount"] > 0:
            return 1
        return 0


@dataclass(frozen=True)
class ProceduralStyleReportCommand:
    args: argparse.Namespace

    def run(self) -> int:
        try:
            result = self.build_report()
        except ValueError as exc:
            print(
                json.dumps(
                    {"status": "error", "message": procedural_style_error(str(exc))},
                    indent=2,
                )
            )
            return 2
        self.write_result(result)
        return self.exit_code_for(result)

    def build_report(self) -> dict[str, Any]:
        return build_procedural_style_report(
            self.paths(),
            hotspot_min_top_level_count=self.args.hotspot_min_top_level_count,
            hotspot_min_top_level_span=self.args.hotspot_min_top_level_span,
        )

    def paths(self) -> list[Path]:
        return self.args.path or [Path("src/spec_harvester")]

    def write_result(self, report: dict[str, Any]) -> None:
        JsonReportOutput(self.args.output).write(report, write_procedural_style_report)

    def exit_code_for(self, report: dict[str, Any]) -> int:
        if self.args.fail_on_hotspots and report["summary"]["hotspotCount"] > 0:
            return 1
        return 0


def procedural_style_error(message: str) -> str:
    return message.replace("Architecture lint", "Procedural style report")


def run_code_duplication_report(args: argparse.Namespace) -> int:
    return CodeDuplicationReportCommand(args).run()


def run_architecture_lint(args: argparse.Namespace) -> int:
    return ArchitectureLintCommand(args).run()


def run_procedural_style_report(args: argparse.Namespace) -> int:
    return ProceduralStyleReportCommand(args).run()
