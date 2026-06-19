from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from spec_harvester.repository_plugin_applicability import (
    API_VERSION,
    AUTHORITY,
    KIND,
    evaluate_repository_plugin_applicability,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def registry() -> dict:
    return load_fixture("generic-registry.example.json")


def static_evidence() -> dict:
    return load_fixture("static-evidence-envelope.example.json")


def test_evaluator_emits_applicability_report_from_static_evidence_fixture() -> None:
    report = evaluate_repository_plugin_applicability(registry(), static_evidence())

    assert report["apiVersion"] == API_VERSION
    assert report["kind"] == KIND
    assert report["schemaVersion"] == 1
    assert report["authority"] == AUTHORITY
    assert report["mode"] == "auto"
    assert report["repository"]["id"] == "example-workspace"
    assert report["registry"]["path"] == (
        "tests/fixtures/repository_plugins/generic-registry.example.json"
    )
    assert report["staticEvidence"]["inputAuthority"] == "static_local_evidence_only"
    assert report["staticEvidence"]["paths"] == [
        "inputs/repositories.yml",
        "out/example-workspace/harvest.json",
        "out/example-workspace/workspace-inventory.json",
        "out/example-workspace/repository-profile-detection.json",
        "out/example-workspace/public-interface-index.json",
        "out/example-workspace/repository-parsing-profile-decision.json",
        "inputs/repository-plugin-labels.yml",
    ]
    assert report["summary"] == {
        "selectedCount": 3,
        "rejectedCount": 0,
        "fallbackCount": 0,
        "blockedCount": 2,
        "diagnosticCount": 5,
    }

    selected = {item["pluginId"]: item for item in report["selectedPlugins"]}
    blocked = {item["pluginId"]: item for item in report["blockedPlugins"]}
    assert set(selected) == {
        "spec_harvester.generic.parser_profile.v0",
        "spec_harvester.generic.repository_profile.v0",
        "spec_harvester.generic.manifest_summary.v0",
    }
    assert set(blocked) == {
        "spec_harvester.generic.package_topology.v0",
        "spec_harvester.generic.review_surface.v0",
    }
    assert report["rejectedPlugins"] == []
    assert report["fallbackPlugins"] == []

    decisions = [
        *report["selectedPlugins"],
        *report["rejectedPlugins"],
        *report["fallbackPlugins"],
        *report["blockedPlugins"],
    ]
    assert len(decisions) == len(registry()["plugins"])
    assert {item["pluginId"] for item in decisions} == {
        item["pluginId"] for item in registry()["plugins"]
    }
    for decision in decisions:
        assert decision["decisionAuthority"] == "producer_plugin_applicability_only"
        assert decision["pluginOutputAuthority"] == "producer_side_evidence_only"
        assert set(decision["evidencePaths"]).issubset(set(report["staticEvidence"]["paths"]))

    assert selected["spec_harvester.generic.parser_profile.v0"]["reasonCodes"] == [
        "required_static_evidence_available"
    ]
    assert blocked["spec_harvester.generic.package_topology.v0"]["missingEvidenceKinds"] == [
        "manifest_summary"
    ]
    assert blocked["spec_harvester.generic.review_surface.v0"]["missingEvidenceKinds"] == [
        "manifest_summary",
        "package_topology_hint",
    ]

    diagnostic_codes = {item["code"] for item in report["diagnostics"]}
    assert diagnostic_codes == {
        "plugin_selected",
        "plugin_blocked_required_evidence_missing",
    }
    assert report["sidecarBoundary"] == {
        "appliedToDrafting": False,
        "registryAuthority": False,
        "evaluatorExecution": "deterministic_static_metadata_only",
    }
    assert "does_not_execute_plugins" in report["nonAuthorityStatements"]
    assert "does_not_read_repository_source_files" in report["nonAuthorityStatements"]
    assert "does_not_treat_plugin_decisions_as_registry_truth" in report["nonAuthorityStatements"]
    assert report["followUp"]["cliReportTask"] == "P39-T4"


def test_missing_required_evidence_uses_declared_fallback_behavior() -> None:
    envelope = copy.deepcopy(static_evidence())
    envelope["evidenceKinds"].remove("operator_label")
    envelope["evidence"] = [
        item for item in envelope["evidence"] if item["kind"] != "operator_label"
    ]

    report = evaluate_repository_plugin_applicability(registry(), envelope)

    fallback = {item["pluginId"]: item for item in report["fallbackPlugins"]}
    selected = {item["pluginId"]: item for item in report["selectedPlugins"]}
    assert set(fallback) == {"spec_harvester.generic.parser_profile.v0"}
    assert fallback["spec_harvester.generic.parser_profile.v0"]["missingEvidenceKinds"] == [
        "operator_label"
    ]
    assert fallback["spec_harvester.generic.parser_profile.v0"]["reasonCodes"] == [
        "missing_required_evidence",
        "conservative_default_path_classification",
    ]
    assert "spec_harvester.generic.repository_profile.v0" in selected
    assert report["summary"]["fallbackCount"] == 1
    assert "plugin_fallback" in {item["code"] for item in report["diagnostics"]}


def test_missing_required_evidence_with_skip_blocks_plugin() -> None:
    envelope = copy.deepcopy(static_evidence())
    envelope["evidenceKinds"].remove("workspace_inventory")
    envelope["evidence"] = [
        item for item in envelope["evidence"] if item["kind"] != "workspace_inventory"
    ]

    report = evaluate_repository_plugin_applicability(registry(), envelope)

    blocked = {item["pluginId"]: item for item in report["blockedPlugins"]}
    assert "spec_harvester.generic.manifest_summary.v0" in blocked
    assert blocked["spec_harvester.generic.manifest_summary.v0"]["missingEvidenceKinds"] == [
        "workspace_inventory"
    ]
    assert blocked["spec_harvester.generic.manifest_summary.v0"]["reasonCodes"] == [
        "missing_required_evidence",
        "missing_manifest_evidence",
    ]
    assert report["summary"]["blockedCount"] >= 2
    assert "plugin_blocked_required_evidence_missing" in {
        item["code"] for item in report["diagnostics"]
    }


def test_evaluator_rejects_unsafe_evidence_paths_and_invalid_digests() -> None:
    unsafe = copy.deepcopy(static_evidence())
    unsafe["evidence"][0]["path"] = "../inputs/repositories.yml"
    with pytest.raises(ValueError, match="unsafe static evidence path"):
        evaluate_repository_plugin_applicability(registry(), unsafe)

    bad_digest = copy.deepcopy(static_evidence())
    bad_digest["evidence"][0]["digest"] = "sha256:not-a-real-digest"
    with pytest.raises(ValueError, match="static evidence digest"):
        evaluate_repository_plugin_applicability(registry(), bad_digest)
