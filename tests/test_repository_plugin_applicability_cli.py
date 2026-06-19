from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"
REGISTRY = FIXTURES / "generic-registry.example.json"
STATIC_EVIDENCE = FIXTURES / "static-evidence-envelope.example.json"


def test_repository_plugin_applicability_detect_cli_writes_report_and_summary(
    tmp_path: Path,
    capsys,
) -> None:
    output = tmp_path / "repository-plugin-applicability-report.json"

    result = main(
        [
            "repository-plugin-applicability-detect",
            "--registry",
            str(REGISTRY),
            "--static-evidence-envelope",
            str(STATIC_EVIDENCE),
            "--out",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_payload == {
        "status": "ok",
        "output": str(output),
        "apiVersion": "spec-harvester.repository-plugin-applicability/v0",
        "kind": "SpecHarvesterRepositoryPluginApplicabilityReport",
        "authority": "producer_plugin_applicability_only",
        "summary": {
            "selectedCount": 3,
            "rejectedCount": 0,
            "fallbackCount": 0,
            "blockedCount": 2,
            "diagnosticCount": 5,
        },
    }
    assert file_payload["summary"] == stdout_payload["summary"]
    assert file_payload["sidecarBoundary"] == {
        "appliedToDrafting": False,
        "registryAuthority": False,
        "evaluatorExecution": "deterministic_static_metadata_only",
    }


def test_repository_plugin_applicability_detect_cli_reports_bad_registry_identity(
    tmp_path: Path,
    capsys,
) -> None:
    registry = read_json(REGISTRY)
    registry["apiVersion"] = "example.invalid/v0"
    registry_path = tmp_path / "registry.json"
    write_json(registry_path, registry)
    output = tmp_path / "report.json"

    result = main(
        [
            "repository-plugin-applicability-detect",
            "--registry",
            str(registry_path),
            "--static-evidence-envelope",
            str(STATIC_EVIDENCE),
            "--out",
            str(output),
        ]
    )

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "Unsupported plugin registry apiVersion" in payload["message"]
    assert not output.exists()


def test_repository_plugin_applicability_detect_cli_rejects_unsafe_static_path(
    tmp_path: Path,
    capsys,
) -> None:
    envelope = read_json(STATIC_EVIDENCE)
    envelope["evidence"][0]["path"] = "../inputs/repositories.yml"
    envelope_path = tmp_path / "static-evidence-envelope.json"
    write_json(envelope_path, envelope)
    output = tmp_path / "report.json"

    result = main(
        [
            "repository-plugin-applicability-detect",
            "--registry",
            str(REGISTRY),
            "--static-evidence-envelope",
            str(envelope_path),
            "--out",
            str(output),
        ]
    )

    assert result == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert "unsafe static evidence path" in payload["message"]
    assert not output.exists()


def test_repository_plugin_applicability_detect_cli_preserves_missing_evidence_fallback(
    tmp_path: Path,
    capsys,
) -> None:
    envelope = read_json(STATIC_EVIDENCE)
    envelope["evidenceKinds"].remove("operator_label")
    envelope["evidence"] = [
        item for item in envelope["evidence"] if item["kind"] != "operator_label"
    ]
    envelope_path = tmp_path / "static-evidence-envelope.json"
    write_json(envelope_path, envelope)
    output = tmp_path / "report.json"

    result = main(
        [
            "repository-plugin-applicability-detect",
            "--registry",
            str(REGISTRY),
            "--static-evidence-envelope",
            str(envelope_path),
            "--out",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_payload["summary"]["fallbackCount"] == 1
    fallback = {item["pluginId"]: item for item in file_payload["fallbackPlugins"]}
    assert fallback["spec_harvester.generic.parser_profile.v0"]["missingEvidenceKinds"] == [
        "operator_label"
    ]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
