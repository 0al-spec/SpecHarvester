from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.repository_profile_detection import (
    GENERIC_FALLBACK_PROFILE_ID,
    PACKAGE_SET_PROFILE_ID,
    RepositoryIdentity,
    RepositoryProfileDetectionOptions,
    build_repository_profile_detection,
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
