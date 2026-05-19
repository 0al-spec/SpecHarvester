from __future__ import annotations

from spec_harvester.classifier_registry import (
    CLASSIFIER_STATUSES,
    classifier_registry,
    default_classifier_policy,
)
from spec_harvester.collector import HarvestOptions, collect_local_repository


def test_classifier_registry_records_supported_statuses_and_tool_decisions() -> None:
    registry = classifier_registry()
    tools = {tool["id"]: tool for tool in registry["tools"]}

    assert registry["schemaVersion"] == 1
    assert registry["statusValues"] == list(CLASSIFIER_STATUSES)
    assert set(tools) == {
        "github-linguist",
        "go-enry",
        "syft",
        "scancode-toolkit",
        "universal-ctags",
        "tree-sitter",
    }
    assert tools["go-enry"]["status"] == "approved_optional"
    assert tools["syft"]["status"] == "approved_optional"
    assert tools["scancode-toolkit"]["status"] == "deferred"
    assert tools["universal-ctags"]["status"] == "deferred"
    assert tools["tree-sitter"]["status"] == "deferred"


def test_classifier_registry_entries_have_trust_and_fallback_contracts() -> None:
    registry = classifier_registry()

    for tool in registry["tools"]:
        assert tool["status"] in CLASSIFIER_STATUSES
        assert tool["license"]["spdx"]
        assert tool["source"].startswith("https://")
        assert tool["deterministicUse"]
        assert tool["execution"] == "optional_local_tool_only"
        assert tool["networkAccess"] == "none"
        assert tool["packageScripts"] == "not_run"
        assert tool["outputAuthority"] == "advisory_untrusted_metadata"
        assert tool["fallback"]
        assert tool["trustBoundary"]["manifestEvidencePrecedence"] == "manifest_first"
        assert tool["trustBoundary"]["requiresPinnedToolVersion"] is True
        assert tool["trustBoundary"]["requiresSourceDigests"] is True


def test_default_classifier_policy_is_disabled_and_manifest_first() -> None:
    policy = default_classifier_policy()

    assert policy["defaultMode"] == "disabled"
    assert policy["allowedExecutions"] == ["none"]
    assert policy["networkAccess"] == "none"
    assert policy["packageScripts"] == "not_run"
    assert policy["outputAuthority"] == "advisory_untrusted_metadata"
    assert policy["manifestEvidencePrecedence"] == "manifest_first"
    assert policy["requiresPinnedToolVersion"] is True
    assert policy["adapterContract"]["mergeRule"].endswith(
        "must not override manifest-first ProjectProfile evidence."
    )
    assert "observations" in policy["adapterContract"]["requiredFields"]
    assert "license" not in policy["registry"]["tools"][0]
    assert "deterministicUse" not in policy["registry"]["tools"][0]


def test_default_harvest_includes_classifier_policy_without_external_tools(tmp_path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")

    snapshot = collect_local_repository(HarvestOptions(source=repo))
    policy = snapshot["classifierPolicy"]

    assert policy["defaultMode"] == "disabled"
    assert policy["allowedExecutions"] == ["none"]
    assert policy["registry"]["tools"][0]["id"] == "github-linguist"
    assert snapshot["projectProfile"]["languages"][0]["id"] == "python"
    assert snapshot["projectProfile"]["languages"][0]["confidence"] == "high"
