from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.accepted_candidate_impact import build_accepted_candidate_impact_report
from spec_harvester.cli import main


def test_build_accepted_candidate_impact_report_classifies_changed_candidate(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"

    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.write"],
        intents=["intent.package.utility"],
        summary="Old package",
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidates_root / "demo" / "1.1.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.workflow"],
        summary="New package",
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        extra_metadata={"licenseEvidence": "license.txt"},
    )

    report = build_accepted_candidate_impact_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["kind"] == "SpecHarvesterAcceptedCandidateImpactClassificationReport"
    assert report["status"] == "ok"
    assert report["summary"]["recordCount"] == 1
    assert report["summary"]["changedCount"] == 1
    assert report["summary"]["metadataImpactCount"] == 1
    assert report["summary"]["licenseImpactCount"] == 1
    assert report["summary"]["provenanceImpactCount"] == 1

    comparison = report["comparisons"][0]
    assert comparison["packageId"] == "demo.core"
    assert comparison["status"] == "changed"
    assert comparison["impact"]["metadata"]["changed"] is True
    assert comparison["impact"]["capability"]["changed"] is True
    assert comparison["impact"]["capability"]["added"] == ["demo.stream"]
    assert comparison["impact"]["capability"]["removed"] == ["demo.write"]
    assert comparison["impact"]["intent"]["added"] == ["intent.package.workflow"]
    assert comparison["impact"]["intent"]["removed"] == ["intent.package.utility"]
    assert comparison["impact"]["interface"]["added"] == [
        "capability:demo.stream",
        "intent:intent.package.workflow",
    ]
    assert comparison["impact"]["interface"]["removed"] == [
        "capability:demo.write",
        "intent:intent.package.utility",
    ]
    assert comparison["impact"]["provenance"]["changed"] is True
    assert comparison["impact"]["provenance"]["added"] == [
        {
            "id": "upstream_repository",
            "uri": "https://github.com/example/demo",
            "revision": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        }
    ]
    assert comparison["impact"]["provenance"]["removed"] == [
        {
            "id": "upstream_repository",
            "uri": "https://github.com/example/demo",
            "revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        }
    ]
    assert "licenseEvidence" in comparison["impact"]["metadata"]["items"]
    assert set(comparison["impact"]["license"]["items"]) == {"licenseEvidence"}
    assert comparison["changedClaims"] == [
        "capability:demo.stream",
        "capability:demo.write",
        "intent:intent.package.utility",
        "intent:intent.package.workflow",
    ]


def test_build_accepted_candidate_impact_report_marks_new_package(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    accepted_root.mkdir()
    write_manifest(
        candidates_root / "fresh" / "0.1.0" / "specpm.yaml",
        package_id="fresh.core",
        version="0.1.0",
        capabilities=["fresh.read"],
        intents=["intent.package.fresh"],
    )

    report = build_accepted_candidate_impact_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["summary"]["newPackageCount"] == 1
    comparison = report["comparisons"][0]
    assert comparison["status"] == "new_package"
    assert comparison["accepted"] is None
    assert comparison["impact"]["metadata"]["changed"] is True
    assert comparison["impact"]["interface"]["changed"] is True
    assert comparison["impact"]["interface"]["added"] == [
        "capability:fresh.read",
        "intent:intent.package.fresh",
    ]
    assert comparison["impact"]["capability"]["added"] == ["fresh.read"]
    assert comparison["impact"]["intent"]["added"] == ["intent.package.fresh"]
    assert comparison["impact"]["metadata"]["items"] == [
        "id",
        "license",
        "name",
        "summary",
        "version",
    ]
    assert comparison["impact"]["license"]["items"] == ["license"]
    assert comparison["impact"]["provenance"]["changed"] is True
    assert comparison["changedClaims"] == [
        "capability:fresh.read",
        "intent:intent.package.fresh",
    ]


def test_build_accepted_candidate_impact_report_marks_unchanged_candidate(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )
    write_manifest(
        candidates_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )

    report = build_accepted_candidate_impact_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["summary"]["unchangedCount"] == 1
    comparison = report["comparisons"][0]
    assert comparison["status"] == "unchanged"
    assert comparison["impact"]["metadata"]["changed"] is False
    assert comparison["impact"]["interface"]["changed"] is False
    assert comparison["impact"]["capability"]["changed"] is False
    assert comparison["impact"]["intent"]["changed"] is False
    assert comparison["impact"]["provenance"]["changed"] is False
    assert comparison["changedClaims"] == []


def test_build_accepted_candidate_impact_report_handles_invalid_manifest_as_partial(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    (accepted_root / "broken" / "1.0.0").mkdir(parents=True, exist_ok=True)
    (accepted_root / "broken" / "1.0.0" / "specpm.yaml").write_text(
        "kind: SpecPackage\n",
        encoding="utf-8",
    )
    write_manifest(
        candidates_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )

    report = build_accepted_candidate_impact_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["status"] == "partial"
    assert report["summary"]["issueCount"] == 1
    issue_codes = {item["code"] for item in report["issues"]}
    assert issue_codes == {"invalid_specpm_manifest"}


def test_cli_accepted_candidate_impact_report_writes_output(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    output = tmp_path / "impact.json"
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )
    write_manifest(
        candidates_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=["intent.package.utility"],
    )

    exit_code = main(
        [
            "accepted-candidate-impact-classification-report",
            "--accepted-root",
            str(accepted_root),
            "--candidates-root",
            str(candidates_root),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["summary"]["unchangedCount"] == 1
    assert report["kind"] == "SpecHarvesterAcceptedCandidateImpactClassificationReport"


def write_manifest(
    path: Path,
    *,
    package_id: str,
    version: str,
    capabilities: list[str],
    intents: list[str],
    name: str = "Demo",
    summary: str = "Demo package",
    license_name: str = "MIT",
    upstream_revision: str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    extra_metadata: dict[str, str] | None = None,
) -> None:
    metadata_lines = ""
    if extra_metadata:
        metadata_lines = "".join(f"  {key}: {value}\n" for key, value in extra_metadata.items())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            f"  id: {package_id}\n"
            f"  name: {name}\n"
            f"  version: {version}\n"
            f"  summary: {summary}\n"
            f"  license: {license_name}\n"
            f"{metadata_lines}"
            "index:\n"
            "  provides:\n"
            "    capabilities:\n"
            + "".join(f"      - {capability}\n" for capability in capabilities)
            + "  intents:\n"
            + "".join(f"    - {intent}\n" for intent in intents)
            + "foreignArtifacts:\n"
            "  - id: upstream_repository\n"
            "    uri: https://github.com/example/demo\n"
            f"    revision: {upstream_revision}\n"
        ),
        encoding="utf-8",
    )
