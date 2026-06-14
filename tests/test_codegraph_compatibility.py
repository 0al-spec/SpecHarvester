from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.codegraph_compatibility import (
    CodeGraphCompatibilityOptions,
    build_codegraph_compatibility_report,
)

FIXTURE = Path(__file__).parent / "fixtures" / "codegraph_compatibility" / "codegraph-0.9.7.json"


def test_codegraph_compatibility_report_passes_pinned_fixture() -> None:
    report = build_codegraph_compatibility_report(CodeGraphCompatibilityOptions(fixture=FIXTURE))

    assert report["kind"] == "SpecHarvesterCodeGraphCompatibilityReport"
    assert report["status"] == "passed"
    assert report["package"]["name"] == "@colbymchenry/codegraph"
    assert report["package"]["version"] == "0.9.7"
    assert set(report["requiredJsonCommands"]) == {
        "affected",
        "callees",
        "callers",
        "files",
        "impact",
        "query",
        "status",
    }
    checks = {check["id"]: check for check in report["checks"]}
    assert checks["executable_available"]["status"] == "skipped"
    assert checks["normalized_schema_mapping"]["summary"]["nodeCount"] == 1
    assert "No CodeGraph install" in " ".join(report["trustBoundary"])


def test_codegraph_compatibility_report_fails_missing_json_command(
    tmp_path: Path,
) -> None:
    fixture = mutable_fixture(tmp_path)
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    payload["requiredJsonCommands"] = [
        command for command in payload["requiredJsonCommands"] if command["name"] != "affected"
    ]
    fixture.write_text(json.dumps(payload), encoding="utf-8")

    report = build_codegraph_compatibility_report(CodeGraphCompatibilityOptions(fixture=fixture))

    checks = {check["id"]: check for check in report["checks"]}
    assert report["status"] == "failed"
    assert checks["required_json_cli_commands"]["status"] == "failed"
    assert "affected" in checks["required_json_cli_commands"]["message"]


def test_codegraph_compatibility_report_fails_unpinned_package_metadata(
    tmp_path: Path,
) -> None:
    fixture = mutable_fixture(tmp_path)
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    payload["package"]["name"] = "malicious"
    payload["package"]["version"] = "999.0.0"
    payload["package"]["shasum"] = "unexpected"
    payload["package"]["platformPackage"]["integrity"] = "unexpected"
    fixture.write_text(json.dumps(payload), encoding="utf-8")

    report = build_codegraph_compatibility_report(CodeGraphCompatibilityOptions(fixture=fixture))

    checks = {check["id"]: check for check in report["checks"]}
    assert report["status"] == "failed"
    assert checks["pinned_package_metadata"]["status"] == "failed"
    assert "package.name" in checks["pinned_package_metadata"]["message"]
    assert "package.version" in checks["pinned_package_metadata"]["message"]
    assert "package.shasum" in checks["pinned_package_metadata"]["message"]
    assert "platformPackage.integrity" in checks["pinned_package_metadata"]["message"]


def test_codegraph_compatibility_report_fails_missing_json_flag(
    tmp_path: Path,
) -> None:
    fixture = mutable_fixture(tmp_path)
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    payload["requiredJsonCommands"][0]["args"] = ["affected"]
    fixture.write_text(json.dumps(payload), encoding="utf-8")

    report = build_codegraph_compatibility_report(CodeGraphCompatibilityOptions(fixture=fixture))

    checks = {check["id"]: check for check in report["checks"]}
    assert report["status"] == "failed"
    assert checks["required_json_cli_commands"]["status"] == "failed"
    assert "affected" in checks["required_json_cli_commands"]["message"]


def test_codegraph_compatibility_report_fails_bad_mapping_fixture(
    tmp_path: Path,
) -> None:
    fixture = mutable_fixture(tmp_path)
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    payload["sampleEvidence"]["files"][0]["path"] = "../secret.py"
    fixture.write_text(json.dumps(payload), encoding="utf-8")

    report = build_codegraph_compatibility_report(CodeGraphCompatibilityOptions(fixture=fixture))

    checks = {check["id"]: check for check in report["checks"]}
    assert report["status"] == "failed"
    assert checks["normalized_schema_mapping"]["status"] == "failed"
    assert "Unsafe CodeGraph path" in checks["normalized_schema_mapping"]["message"]


def test_codegraph_compatibility_cli_writes_report(tmp_path: Path, capsys) -> None:
    output = tmp_path / "compatibility.json"

    result = main(
        [
            "codegraph-compatibility-report",
            "--fixture",
            str(FIXTURE),
            "--output",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    output_payload = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_payload == output_payload
    assert output_payload["status"] == "passed"


def test_codegraph_compatibility_optional_executable_probe(tmp_path: Path) -> None:
    executable = tmp_path / "codegraph"
    executable.write_text("#!/bin/sh\necho 'codegraph 0.9.7'\n", encoding="utf-8")
    executable.chmod(0o755)

    report = build_codegraph_compatibility_report(
        CodeGraphCompatibilityOptions(fixture=FIXTURE, executable=executable)
    )

    checks = {check["id"]: check for check in report["checks"]}
    assert report["status"] == "passed"
    assert checks["executable_version"]["status"] == "passed"
    assert checks["executable_version"]["versionOutput"] == "codegraph 0.9.7"


def test_codegraph_compatibility_cli_returns_failure_for_failed_report(
    tmp_path: Path,
    capsys,
) -> None:
    fixture = mutable_fixture(tmp_path)
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    payload["package"].pop("integrity")
    fixture.write_text(json.dumps(payload), encoding="utf-8")

    result = main(["codegraph-compatibility-report", "--fixture", str(fixture)])

    report = json.loads(capsys.readouterr().out)
    assert result == 1
    assert report["status"] == "failed"
    assert (
        "integrity"
        in {check["id"]: check for check in report["checks"]}["pinned_package_metadata"]["message"]
    )


def test_codegraph_compatibility_cli_reports_unreadable_fixture_as_json(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    fixture = mutable_fixture(tmp_path)
    original_read_text = Path.read_text

    def blocked_read_text(self: Path, *args, **kwargs) -> str:
        if self == fixture:
            raise OSError("permission denied")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", blocked_read_text)

    result = main(["codegraph-compatibility-report", "--fixture", str(fixture)])

    report = json.loads(capsys.readouterr().out)
    assert result == 2
    assert report["status"] == "error"
    assert "Unable to read CodeGraph compatibility fixture" in report["message"]


def mutable_fixture(tmp_path: Path) -> Path:
    fixture = tmp_path / "codegraph-fixture.json"
    fixture.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    return fixture
