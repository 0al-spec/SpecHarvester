from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.xyflow_package_set_smoke import (
    EXPECTED_PACKAGE_IDS,
    EXPECTED_RELATIONS,
    XYFLOW_PACKAGE_SET_SMOKE_API_VERSION,
    XYFLOW_PACKAGE_SET_SMOKE_KIND,
    XyflowPackageSetSmokeOptions,
    run_xyflow_package_set_smoke,
)


def test_xyflow_package_set_smoke_runs_end_to_end(tmp_path: Path) -> None:
    output = tmp_path / "xyflow-smoke"

    report = run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=output))

    assert report["apiVersion"] == XYFLOW_PACKAGE_SET_SMOKE_API_VERSION
    assert report["kind"] == XYFLOW_PACKAGE_SET_SMOKE_KIND
    assert report["status"] == "passed"
    assert report["source"] == {
        "fixture": "synthetic_local_checkout",
        "repository": "https://github.com/xyflow/xyflow",
        "revision": "abc123",
    }
    assert report["packageSet"] == {
        "candidateCount": 4,
        "id": "xyflow.workspace",
        "packageIds": sorted(EXPECTED_PACKAGE_IDS),
        "skippedPackageIds": [
            "xyflow.cli",
            "xyflow.e2e",
            "xyflow.react_examples",
            "xyflow.svelte_examples",
        ],
    }
    assert relation_tuples(report) == set(EXPECTED_RELATIONS)
    assert all(item["reviewStatus"] == "producer_observed" for item in report["relations"])
    assert report["preflight"]["status"] == "passed"
    assert report["preflight"]["summary"]["candidatePreflightPassedCount"] == 4
    assert report["viewer"]["status"] == "ok"
    assert report["viewer"]["packageSetId"] == "xyflow.workspace"
    assert report["viewer"]["payloadKind"] == "SpecHarvesterStaticPackageSet"
    assert "package-set.json" in report["viewer"]["written"]
    assert report["executionBoundary"] == {
        "builds": "not_run",
        "network": "none",
        "packageManagers": "not_run",
        "packageScripts": "not_run",
        "prompts": "not_run",
        "tests": "not_run",
    }

    assert (output / "candidates/xyflow/workspace-inventory.json").is_file()
    assert (output / "package-set/package-set-draft.json").is_file()
    assert (output / "package-set/package-relation-proposals.json").is_file()
    assert (output / "package-set/bundle-set-preflight.json").is_file()
    assert (output / "viewer/package-set.json").is_file()
    assert (output / "viewer/index.html").is_file()
    written_report = json.loads(
        (output / "xyflow-package-set-smoke.json").read_text(encoding="utf-8")
    )
    assert written_report == report

    viewer_payload = json.loads((output / "viewer/package-set.json").read_text(encoding="utf-8"))
    assert viewer_payload["packageSet"]["id"] == "xyflow.workspace"
    assert [member["packageId"] for member in viewer_payload["members"]] == [
        "xyflow.workspace",
        "xyflow.react",
        "xyflow.svelte",
        "xyflow.system",
    ]


def test_xyflow_package_set_smoke_cli_writes_summary(tmp_path: Path, capsys) -> None:
    output = tmp_path / "xyflow-smoke"

    exit_code = main(["xyflow-package-set-smoke", "--output", str(output)])

    printed = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert printed["status"] == "passed"
    assert printed["packageSet"]["packageIds"] == sorted(EXPECTED_PACKAGE_IDS)
    assert relation_tuples(printed) == set(EXPECTED_RELATIONS)
    assert printed["viewer"]["status"] == "ok"


def test_xyflow_package_set_smoke_rejects_existing_file_output(tmp_path: Path) -> None:
    output = tmp_path / "not-a-directory"
    output.write_text("file", encoding="utf-8")

    with pytest.raises(ValueError, match="not a directory"):
        run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=output))


def relation_tuples(report: dict[str, object]) -> set[tuple[str, str, str]]:
    relations = report["relations"]
    assert isinstance(relations, list)
    return {
        (str(item["source"]), str(item["type"]), str(item["target"]))
        for item in relations
        if isinstance(item, dict)
    }
