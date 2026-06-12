from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.fresh_candidate_refresh_run import (
    FRESH_CANDIDATE_REFRESH_RUN_API_VERSION,
    FRESH_CANDIDATE_REFRESH_RUN_KIND,
    FRESH_GENERATED_ROOT_LAYOUT,
    FreshCandidateRefreshRunOptions,
    build_fresh_candidate_refresh_run,
)
from spec_harvester.xyflow_package_set_smoke import (
    XyflowPackageSetSmokeOptions,
    run_xyflow_package_set_smoke,
)


def test_fresh_candidate_refresh_run_exports_specpm_generated_root(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    fresh_root = tmp_path / "fresh-generated"

    report = build_fresh_candidate_refresh_run(
        FreshCandidateRefreshRunOptions(
            bundle_set=smoke / "package-set",
            fresh_generated_root=fresh_root,
        )
    )

    assert report["apiVersion"] == FRESH_CANDIDATE_REFRESH_RUN_API_VERSION
    assert report["kind"] == FRESH_CANDIDATE_REFRESH_RUN_KIND
    assert report["status"] == "prepared"
    assert report["source"]["repository"] == "https://github.com/xyflow/xyflow"
    assert report["source"]["revision"] == "abc123"
    assert report["packageSet"] == {
        "id": "xyflow.workspace",
        "candidateCount": 4,
        "memberPackageIds": [
            "xyflow.workspace",
            "xyflow.react",
            "xyflow.svelte",
            "xyflow.system",
        ],
    }
    assert report["freshGeneratedRoot"]["layout"] == FRESH_GENERATED_ROOT_LAYOUT
    assert report["freshGeneratedRoot"]["packagePathTemplate"] == "<package_id>/<version>"
    assert report["authority"] == {
        "producerEvidenceAuthority": "evidence_only",
        "registryAuthority": "SpecPM maintainer review",
        "noRegistryMutation": True,
    }
    package_paths = {item["packageId"]: item["artifactPath"] for item in report["packages"]}
    assert package_paths == {
        "xyflow.react": "xyflow.react/0.1.0",
        "xyflow.svelte": "xyflow.svelte/0.1.0",
        "xyflow.system": "xyflow.system/0.1.0",
        "xyflow.workspace": "xyflow.workspace/0.1.0",
    }
    for artifact_path in package_paths.values():
        assert (fresh_root / artifact_path / "specpm.yaml").is_file()
        assert list((fresh_root / artifact_path / "specs").glob("*.spec.yaml"))

    react = next(item for item in report["packages"] if item["packageId"] == "xyflow.react")
    assert react["manifestPath"] == "xyflow.react/0.1.0/specpm.yaml"
    assert {item["role"] for item in react["contractFiles"]} == {
        "manifest",
        "boundary_spec",
    }
    for contract_file in react["contractFiles"]:
        assert contract_file["path"].startswith("xyflow.react/0.1.0/")
        assert contract_file["digest"]["algorithm"] == "sha256"
        assert len(contract_file["digest"]["value"]) == 64

    consumer = report["specpmConsumer"]
    assert consumer["command"] == "specpm producer-bundle prepare-refresh-decision"
    assert consumer["arguments"]["packageId"] == "xyflow.workspace"
    assert consumer["arguments"]["version"] == "0.1.0"
    assert consumer["arguments"]["packages"] == [
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
    ]
    assert consumer["expectedArtifacts"] == [
        "refresh-decision.json",
        "prepare-report.json",
        "preflight-report.json",
    ]


def test_fresh_candidate_refresh_run_cli_writes_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    fresh_root = tmp_path / "fresh-generated"
    output = tmp_path / "refresh" / "fresh-candidate-refresh-run.json"

    exit_code = main(
        [
            "fresh-candidate-refresh-run",
            "--bundle-set",
            str(smoke / "package-set"),
            "--fresh-generated-root",
            str(fresh_root),
            "--run-label",
            "xyflow-refresh-evaluation",
            "--output",
            str(output),
        ]
    )

    printed = json.loads(capsys.readouterr().out)
    written = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert printed == written
    assert written["runLabel"] == "xyflow-refresh-evaluation"
    assert written["kind"] == FRESH_CANDIDATE_REFRESH_RUN_KIND
    assert (fresh_root / "xyflow.workspace" / "0.1.0" / "specpm.yaml").is_file()


def test_fresh_candidate_refresh_run_rejects_unsafe_candidate_path(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    draft_path = smoke / "package-set" / "package-set-draft.json"
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    draft["candidates"][0]["candidatePath"] = "../outside"
    draft_path.write_text(json.dumps(draft, indent=2, sort_keys=True), encoding="utf-8")

    with pytest.raises(ValueError, match="escapes bundle root"):
        build_fresh_candidate_refresh_run(
            FreshCandidateRefreshRunOptions(
                bundle_set=smoke / "package-set",
                fresh_generated_root=tmp_path / "fresh-generated",
            )
        )


def test_fresh_candidate_refresh_run_rejects_fresh_root_inside_candidate_source(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)

    with pytest.raises(ValueError, match="must not overlap package-set candidate source"):
        build_fresh_candidate_refresh_run(
            FreshCandidateRefreshRunOptions(
                bundle_set=smoke / "package-set",
                fresh_generated_root=smoke / "package-set" / "xyflow.react",
            )
        )


def test_fresh_candidate_refresh_run_rejects_candidate_symlink(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    outside = tmp_path / "outside-secret.txt"
    outside.write_text("outside", encoding="utf-8")
    (smoke / "package-set" / "xyflow.react" / "leak.txt").symlink_to(outside)

    with pytest.raises(ValueError, match="contains symlink"):
        build_fresh_candidate_refresh_run(
            FreshCandidateRefreshRunOptions(
                bundle_set=smoke / "package-set",
                fresh_generated_root=tmp_path / "fresh-generated",
            )
        )


def write_xyflow_smoke(tmp_path: Path) -> Path:
    smoke = tmp_path / "xyflow-smoke"
    report = run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=smoke))
    assert report["status"] == "passed"
    return smoke
