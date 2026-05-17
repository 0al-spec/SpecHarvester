from __future__ import annotations

from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.license_provenance_reports import (
    build_license_provenance_risk_report,
)


def test_build_license_provenance_risk_report_flags_license_and_provenance_issues(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    accepted_root.mkdir(parents=True)
    candidates_root.mkdir(parents=True)

    write_manifest(
        accepted_root / "good" / "1.0.0" / "specpm.yaml",
        "good.core",
        "1.0.0",
        "MIT",
        upstream_uri="https://github.com/good/good",
    )
    write_manifest(
        accepted_root / "missing" / "1.1.0" / "specpm.yaml",
        "missing.license",
        "1.1.0",
        None,
        upstream_uri="https://github.com/missing/missing",
    )
    write_manifest(
        candidates_root / "odd" / "2.0.0" / "specpm.yaml",
        "odd.core",
        "2.0.0",
        "MIT LICENSE",
        upstream_uri="https://gitlab.com/odd/odd",
    )

    report = build_license_provenance_risk_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["summary"]["records"] == 3
    assert report["summary"]["issueCount"] == 3
    assert report["summary"]["issuesByCode"]["missing_license"] == 1
    assert report["summary"]["issuesByCode"]["non_standard_license"] == 1
    assert report["summary"]["issuesByCode"]["non_github_upstream_repository"] == 1

    issues = report["issues"]
    assert {item["code"] for item in issues} >= {
        "missing_license",
        "non_standard_license",
    }

    missing = [item for item in issues if item["code"] == "non_standard_license"]
    assert len(missing) == 1
    assert missing[0]["packageId"] == "odd.core"


def test_cli_license_provenance_report_emits_json(tmp_path: Path) -> None:
    candidates_root = tmp_path / "candidates"
    accepted_root = tmp_path / "accepted"
    candidates_root.mkdir()
    accepted_root.mkdir()
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        "demo.core",
        "1.0.0",
        "MIT",
        upstream_uri="https://github.com/demo/demo",
    )

    exit_code = main(
        [
            "governance-license-provenance-report",
            "--candidates-root",
            str(candidates_root),
            "--accepted-root",
            str(accepted_root),
        ]
    )

    assert exit_code == 0


def write_manifest(
    path: Path,
    package_id: str,
    version: str,
    license_name: str | None,
    upstream_uri: str | None,
) -> None:
    path.parent.mkdir(parents=True)
    upstream_block = ""
    if upstream_uri is not None:
        upstream_block = (
            "foreignArtifacts:\n"
            "  - id: upstream_repository\n"
            f'    uri: "{upstream_uri}"\n'
            "    role: primary_intent_source\n"
        )

    license_block = ""
    if license_name is not None:
        license_block = f"  license: {license_name}\n"

    path.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            f"  id: {package_id}\n"
            "  name: Demo package\n"
            f"  version: {version}\n"
            f"{license_block}"
            "index:\n"
            "  provides:\n"
            "    capabilities: []\n"
            f"  intents: []\n"
            f"{upstream_block}"
        ),
        encoding="utf-8",
    )
