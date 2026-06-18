from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.repository_profile_detection import (
    GENERIC_FALLBACK_PROFILE_ID,
    PACKAGE_SET_PROFILE_ID,
    SINGLE_PACKAGE_PROFILE_ID,
    RepositoryIdentity,
    RepositoryProfileDetectionOptions,
    build_repository_profile_detection,
)
from spec_harvester.repository_profile_hints import (
    GENERIC_REPOSITORY_PROFILE_HINT_IDS,
    build_repository_profile_hint_vocabulary,
    validate_repository_profile_hint,
)

FIXTURES = Path(__file__).parent / "fixtures" / "repository_profile_detection"

CROSS_ECOSYSTEM_SCENARIOS = {
    "cross-ecosystem-workspace.example.json": {
        "repository_id": "example.cross-ecosystem-workspace",
        "repository_url": "https://example.invalid/cross-ecosystem/workspace",
        "revision": "1" * 40,
        "evidence_paths": (
            "pnpm-workspace.yaml",
            "packages/ui/package.json",
            "packages/core/package.json",
            "docs/guide.md",
        ),
    },
    "cross-ecosystem-single-package.example.json": {
        "repository_id": "example.cross-ecosystem-single-package",
        "repository_url": "https://example.invalid/cross-ecosystem/single-package",
        "revision": "2" * 40,
        "evidence_paths": (
            "pyproject.toml",
            "README.md",
            "docs/index.md",
        ),
    },
    "cross-ecosystem-nested-package.example.json": {
        "repository_id": "example.cross-ecosystem-nested-package",
        "repository_url": "https://example.invalid/cross-ecosystem/nested-package",
        "revision": "3" * 40,
        "evidence_paths": (
            "modules/core/go.mod",
            "modules/plugin/go.mod",
            "docs/usage.md",
        ),
    },
    "cross-ecosystem-ambiguous-multi-signal.example.json": {
        "repository_id": "example.cross-ecosystem-ambiguous-multi-signal",
        "repository_url": "https://example.invalid/cross-ecosystem/ambiguous-multi-signal",
        "revision": "4" * 40,
        "evidence_paths": (
            "pnpm-workspace.yaml",
            "packages/core/package.json",
            "docs/index.md",
        ),
    },
}


def test_repository_profile_hint_vocabulary_fixture_matches_builder() -> None:
    payload = json.loads((FIXTURES / "generic-hint-vocabulary.example.json").read_text())

    assert payload == build_repository_profile_hint_vocabulary()
    assert payload["apiVersion"] == "spec-harvester.repository-profile-hints/v0"
    assert payload["kind"] == "SpecHarvesterRepositoryProfileHintVocabulary"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_profile_hint_vocabulary_only"
    assert payload["summary"] == {
        "hintCount": 13,
        "defaultConsumerBehavior": "review_only",
        "registryAuthority": False,
    }
    assert [item["hint"] for item in payload["hints"]] == [
        "package_set_root",
        "member_package",
        "meta_package",
        "primary_package",
        "cli_package",
        "bridge_package",
        "plugin_package",
        "example_package",
        "test_package",
        "documentation_source",
        "generated_artifact",
        "internal_utility",
        "evidence_only",
    ]
    for item in payload["hints"]:
        assert item["hint"] in GENERIC_REPOSITORY_PROFILE_HINT_IDS
        assert item["title"]
        assert item["pathSubject"]
        assert item["summary"]
        assert item["consumerAction"]
        assert "does_not_treat_profile_hints_as_registry_truth" in item["nonAuthorityStatements"]


def test_repository_profile_hint_validation_rejects_unknown_hint() -> None:
    assert validate_repository_profile_hint("member_package") == "member_package"

    with pytest.raises(ValueError, match="Unknown generic repository profile hint"):
        validate_repository_profile_hint("custom_unknown_hint")


@pytest.mark.parametrize("fixture_name", sorted(CROSS_ECOSYSTEM_SCENARIOS))
def test_cross_ecosystem_profile_fixture_matches_builder(fixture_name: str) -> None:
    payload = json.loads((FIXTURES / fixture_name).read_text())

    assert payload == cross_ecosystem_payload(fixture_name)
    assert payload["apiVersion"] == "spec-harvester.repository-profile-detection/v0"
    assert payload["kind"] == "SpecHarvesterRepositoryProfileDetection"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_profile_selection_only"
    assert payload["selection"]["mode"] == "auto"
    assert payload["selection"]["fallbackProfileId"] == GENERIC_FALLBACK_PROFILE_ID
    assert "does_not_accept_packages" in payload["nonAuthorityStatements"]
    assert "does_not_treat_plugin_decisions_as_registry_truth" in payload["nonAuthorityStatements"]


def test_cross_ecosystem_profile_fixtures_cover_expected_selection_outcomes() -> None:
    workspace = cross_ecosystem_fixture("cross-ecosystem-workspace.example.json")
    assert workspace["selection"]["selectedProfileId"] == PACKAGE_SET_PROFILE_ID
    assert workspace["selection"]["confidence"] == "high"
    assert workspace["selection"]["decision"] == "selected"
    assert workspace["selection"]["reasonCodes"] == [
        "workspace_manifest_present",
        "multiple_member_manifests_present",
    ]
    assert {(hint["hint"], hint["path"]) for hint in workspace["advisoryDownstreamHints"]} == {
        ("documentation_source", "docs"),
        ("member_package", "packages/core"),
        ("member_package", "packages/ui"),
        ("package_set_root", "."),
    }

    single_package = cross_ecosystem_fixture("cross-ecosystem-single-package.example.json")
    assert single_package["selection"]["selectedProfileId"] == SINGLE_PACKAGE_PROFILE_ID
    assert single_package["selection"]["confidence"] == "high"
    assert single_package["selection"]["decision"] == "selected"
    assert single_package["selection"]["reasonCodes"] == ["root_manifest_present"]
    assert single_package["advisoryDownstreamHints"] == []

    nested_package = cross_ecosystem_fixture("cross-ecosystem-nested-package.example.json")
    assert nested_package["selection"]["selectedProfileId"] is None
    assert nested_package["selection"]["decision"] == "fallback"
    assert nested_package["selection"]["reasonCodes"] == [
        "insufficient_high_confidence_profile_evidence"
    ]
    assert {
        candidate["profileId"]: candidate["confidence"]
        for candidate in nested_package["candidateProfiles"]
    } == {
        PACKAGE_SET_PROFILE_ID: "medium",
        SINGLE_PACKAGE_PROFILE_ID: "low",
        "generic.documentation_site.v0": "medium",
    }

    ambiguous = cross_ecosystem_fixture("cross-ecosystem-ambiguous-multi-signal.example.json")
    assert ambiguous["selection"]["selectedProfileId"] is None
    assert ambiguous["selection"]["decision"] == "fallback"
    assert ambiguous["selection"]["reasonCodes"] == [
        "insufficient_high_confidence_profile_evidence"
    ]
    candidates = {candidate["profileId"]: candidate for candidate in ambiguous["candidateProfiles"]}
    assert candidates[PACKAGE_SET_PROFILE_ID]["confidence"] == "medium"
    assert candidates[PACKAGE_SET_PROFILE_ID]["evidencePaths"] == [
        "pnpm-workspace.yaml",
        "packages/core/package.json",
    ]
    assert candidates["generic.documentation_site.v0"]["confidence"] == "medium"


def cross_ecosystem_fixture(fixture_name: str) -> dict:
    return json.loads((FIXTURES / fixture_name).read_text())


def cross_ecosystem_payload(fixture_name: str) -> dict:
    scenario = CROSS_ECOSYSTEM_SCENARIOS[fixture_name]
    return build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=RepositoryIdentity(
                scenario["repository_id"],
                scenario["repository_url"],
                "main",
                scenario["revision"],
            ),
            selection="auto",
            evidence_paths=scenario["evidence_paths"],
        )
    )


def test_build_repository_profile_detection_selects_package_set_from_static_evidence() -> None:
    payload = build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=repository_identity(),
            selection="auto",
            evidence_paths=(
                "workspace.yaml",
                "packages/core/package.json",
                "packages/adapter/package.json",
                "docs/index.md",
            ),
        )
    )

    assert payload["apiVersion"] == "spec-harvester.repository-profile-detection/v0"
    assert payload["kind"] == "SpecHarvesterRepositoryProfileDetection"
    assert payload["schemaVersion"] == 1
    assert payload["authority"] == "producer_profile_selection_only"
    assert payload["selection"] == {
        "mode": "auto",
        "overrideSource": "none",
        "selectedProfileId": PACKAGE_SET_PROFILE_ID,
        "fallbackProfileId": GENERIC_FALLBACK_PROFILE_ID,
        "confidence": "high",
        "decision": "selected",
        "reasonCodes": [
            "workspace_manifest_present",
            "multiple_member_manifests_present",
        ],
    }

    candidates = {candidate["profileId"]: candidate for candidate in payload["candidateProfiles"]}
    assert candidates[PACKAGE_SET_PROFILE_ID]["recommendedAction"] == "select"
    assert candidates[PACKAGE_SET_PROFILE_ID]["confidence"] == "high"
    assert candidates[PACKAGE_SET_PROFILE_ID]["evidencePaths"] == [
        "workspace.yaml",
        "packages/adapter/package.json",
        "packages/core/package.json",
    ]
    assert {profile["profileId"] for profile in payload["rejectedProfiles"]} == {
        "generic.single_package.v0",
        "generic.documentation_site.v0",
    }
    assert {(hint["hint"], hint["path"]) for hint in payload["advisoryDownstreamHints"]} == {
        ("documentation_source", "docs"),
        ("member_package", "packages/adapter"),
        ("member_package", "packages/core"),
        ("package_set_root", "."),
    }
    assert "does_not_run_ai" in payload["nonAuthorityStatements"]
    assert "does_not_draft_packages" in payload["nonAuthorityStatements"]
    assert "does_not_publish_registry_metadata" in payload["nonAuthorityStatements"]


def test_build_repository_profile_detection_none_mode_records_disabled_decision() -> None:
    payload = build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=repository_identity(),
            selection="none",
            evidence_paths=("workspace.yaml",),
        )
    )

    assert payload["selection"]["mode"] == "none"
    assert payload["selection"]["overrideSource"] == "operator_disabled"
    assert payload["selection"]["selectedProfileId"] is None
    assert payload["selection"]["fallbackProfileId"] == GENERIC_FALLBACK_PROFILE_ID
    assert payload["selection"]["decision"] == "disabled"
    assert payload["diagnostics"][0]["code"] == "repository_profile_selection_disabled"


def test_build_repository_profile_detection_explicit_profile_records_cli_override() -> None:
    payload = build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=repository_identity(),
            selection="custom.vendor_profile.v0",
            evidence_paths=("custom.profile.yml",),
        )
    )

    assert payload["selection"]["mode"] == "custom.vendor_profile.v0"
    assert payload["selection"]["overrideSource"] == "cli"
    assert payload["selection"]["selectedProfileId"] == "custom.vendor_profile.v0"
    assert payload["selection"]["reasonCodes"] == ["explicit_cli_profile_override"]
    assert payload["candidateProfiles"][0]["profileId"] == "custom.vendor_profile.v0"
    assert payload["diagnostics"][0]["code"] == "repository_profile_cli_override"


def test_build_repository_profile_detection_explicit_builtin_override_updates_candidate() -> None:
    payload = build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=repository_identity(),
            selection=PACKAGE_SET_PROFILE_ID,
            evidence_paths=("README.md",),
        )
    )

    candidates = {candidate["profileId"]: candidate for candidate in payload["candidateProfiles"]}
    selected = candidates[PACKAGE_SET_PROFILE_ID]

    assert payload["selection"]["selectedProfileId"] == PACKAGE_SET_PROFILE_ID
    assert selected["confidence"] == "high"
    assert selected["score"] == 1.0
    assert selected["evidencePaths"] == ["README.md"]
    assert selected["reasonCodes"] == ["explicit_cli_profile_override"]
    assert selected["recommendedAction"] == "select"


def test_build_repository_profile_detection_derives_nested_workspace_root_hint() -> None:
    payload = build_repository_profile_detection(
        RepositoryProfileDetectionOptions(
            repository=repository_identity(),
            selection="auto",
            evidence_paths=(
                "examples/demo/pnpm-workspace.yaml",
                "examples/demo/packages/core/package.json",
                "examples/demo/packages/adapter/package.json",
            ),
        )
    )

    assert {"hint": "package_set_root", "path": "examples/demo"} in [
        {"hint": item["hint"], "path": item["path"]} for item in payload["advisoryDownstreamHints"]
    ]


def test_build_repository_profile_detection_rejects_unsafe_evidence_paths() -> None:
    with pytest.raises(ValueError, match="repository-relative"):
        build_repository_profile_detection(
            RepositoryProfileDetectionOptions(
                repository=repository_identity(),
                evidence_paths=("../package.json",),
            )
        )

    with pytest.raises(ValueError, match="forward slashes"):
        build_repository_profile_detection(
            RepositoryProfileDetectionOptions(
                repository=repository_identity(),
                evidence_paths=(r"packages\\core\\package.json",),
            )
        )


def test_repository_profile_detect_cli_writes_output_and_stdout(
    tmp_path: Path,
    capsys,
) -> None:
    output = tmp_path / "repository-profile-detection.json"

    result = main(
        [
            "repository-profile-detect",
            "--repository-id",
            "example.generic-package-set",
            "--repository-url",
            "https://example.invalid/generic-package-set",
            "--revision",
            "0000000000000000000000000000000000000000",
            "--selection",
            "auto",
            "--evidence-path",
            "workspace.yaml",
            "--evidence-path",
            "packages/core/package.json",
            "--evidence-path",
            "packages/adapter/package.json",
            "--output",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_payload == file_payload
    assert stdout_payload["selection"]["selectedProfileId"] == PACKAGE_SET_PROFILE_ID
    assert stdout_payload["repository"]["id"] == "example.generic-package-set"


def test_repository_profile_detect_cli_reads_source_manifest(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: example.generic-package-set
    repository: https://github.com/example/generic-package-set
    ref: main
""",
        encoding="utf-8",
    )

    result = main(
        [
            "repository-profile-detect",
            "--source-manifest",
            str(inputs),
            "--source-id",
            "example.generic-package-set",
            "--declared-repository-profile",
            "generic.package_set.v0",
            "--selection",
            "auto",
            "--evidence-path",
            "workspace.yaml",
            "--evidence-path",
            "packages/core/package.json",
            "--evidence-path",
            "packages/adapter/package.json",
        ]
    )

    assert result == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["repository"] == {
        "id": "example.generic-package-set",
        "name": "generic-package-set",
        "url": "https://github.com/example/generic-package-set",
        "ref": "main",
        "revision": None,
    }
    assert payload["sourceManifest"] == {
        "path": "repos.yml",
        "entryId": "example.generic-package-set",
        "declaredRepositoryProfile": "generic.package_set.v0",
    }
    assert payload["selection"]["selectedProfileId"] == PACKAGE_SET_PROFILE_ID


def repository_identity() -> RepositoryIdentity:
    return RepositoryIdentity(
        repository_id="example.generic-package-set",
        repository_url="https://example.invalid/generic-package-set",
        ref=None,
        revision="0000000000000000000000000000000000000000",
        source_manifest_path=None,
        source_manifest_entry_id="example.generic-package-set",
        declared_repository_profile=None,
    )
