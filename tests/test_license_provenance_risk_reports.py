from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.license_provenance_reports import (
    build_license_provenance_risk_report,
    parse_specpm_license_provenance,
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
        "MIT OR Apache-2.0",
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


def test_report_summary_counts_dynamic_issue_codes(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)

    malformed_manifest = accepted_root / "malformed" / "1.0.0" / "specpm.yaml"
    malformed_manifest.parent.mkdir(parents=True)
    malformed_manifest.write_text("{invalid: [\n", encoding="utf-8")

    target = accepted_root / "target.yaml"
    target.write_text("placeholder\n", encoding="utf-8")
    symlink = accepted_root / "linked" / "1.0.0" / "specpm.yaml"
    symlink.parent.mkdir(parents=True)
    symlink.symlink_to(target)

    report = build_license_provenance_risk_report(
        accepted_root=accepted_root,
    )

    issues_by_code = report["summary"]["issuesByCode"]
    assert "invalid_specpm_manifest" in issues_by_code
    assert "specpm_symlink" in issues_by_code
    assert issues_by_code["invalid_specpm_manifest"] == 1
    assert issues_by_code["specpm_symlink"] == 1


def test_license_provenance_report_accepts_upstream_repository_name_match(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    write_manifest(
        accepted_root / "xyflow" / "1.0.0" / "specpm.yaml",
        "xyflow.core",
        "1.0.0",
        "MIT",
        upstream_uri="https://github.com/SoundBlaster/xyflow",
    )

    report = build_license_provenance_risk_report(
        accepted_root=accepted_root,
    )

    assert report["summary"]["issueCount"] == 0
    assert "upstream_namespace_mismatch" not in report["summary"]["issuesByCode"]
    assert report["issues"] == []


def test_license_provenance_report_keeps_known_license_with_evidence_ok(
    tmp_path: Path,
) -> None:
    candidates_root = tmp_path / "candidates"
    candidates_root.mkdir(parents=True)
    write_manifest(
        candidates_root / "known" / "1.0.0" / "specpm.yaml",
        "known.core",
        "1.0.0",
        "MIT",
        upstream_uri="https://github.com/known/known",
        license_evidence={
            "source": "manifest",
            "confidence": "high",
            "paths": ["package.json"],
        },
    )

    report = build_license_provenance_risk_report(candidates_root=candidates_root)

    assert report["summary"]["issueCount"] == 0
    assert report["issues"] == []
    assert report["records"][0]["licenseEvidence"]["source"] == "manifest"


def test_license_provenance_report_distinguishes_unknown_evidence_classes(
    tmp_path: Path,
) -> None:
    candidates_root = tmp_path / "candidates"
    candidates_root.mkdir(parents=True)
    write_manifest(
        candidates_root / "absent" / "0.1.0" / "specpm.yaml",
        "absent.core",
        "0.1.0",
        "UNKNOWN",
        upstream_uri="https://github.com/absent/absent",
        license_evidence={"source": "absent", "confidence": "high", "paths": []},
    )
    write_manifest(
        candidates_root / "ambiguous" / "0.1.0" / "specpm.yaml",
        "ambiguous.core",
        "0.1.0",
        "UNKNOWN",
        upstream_uri="https://github.com/ambiguous/ambiguous",
        license_evidence={
            "source": "ambiguous_license_file",
            "confidence": "low",
            "paths": ["LICENSE.custom"],
        },
    )
    write_manifest(
        candidates_root / "collected" / "0.1.0" / "specpm.yaml",
        "collected.core",
        "0.1.0",
        "UNKNOWN",
        upstream_uri="https://github.com/collected/collected",
        license_evidence={
            "source": "ambiguous_license_file",
            "confidence": "low",
            "paths": ["LICENSE.txt"],
        },
    )
    write_manifest(
        candidates_root / "legacy" / "0.1.0" / "specpm.yaml",
        "legacy.core",
        "0.1.0",
        "UNKNOWN",
        upstream_uri="https://github.com/legacy/legacy",
    )

    report = build_license_provenance_risk_report(candidates_root=candidates_root)

    assert report["summary"]["issuesByCode"] == {
        "absent_license_evidence": 1,
        "ambiguous_unknown_license": 1,
        "collected_unknown_license_evidence": 1,
        "unknown_license": 1,
    }
    by_package = {record["packageId"]: record for record in report["records"]}
    assert by_package["absent.core"]["licenseEvidence"] == {
        "source": "absent",
        "confidence": "high",
        "paths": [],
    }
    assert by_package["ambiguous.core"]["licenseEvidence"] == {
        "source": "ambiguous_license_file",
        "confidence": "low",
        "paths": ["LICENSE.custom"],
    }
    assert by_package["collected.core"]["licenseEvidence"] == {
        "source": "ambiguous_license_file",
        "confidence": "low",
        "paths": ["LICENSE.txt"],
    }

    issue_by_package = {issue["packageId"]: issue for issue in report["issues"]}
    assert issue_by_package["absent.core"]["code"] == "absent_license_evidence"
    assert issue_by_package["ambiguous.core"]["code"] == "ambiguous_unknown_license"
    assert issue_by_package["collected.core"]["code"] == "collected_unknown_license_evidence"
    assert issue_by_package["collected.core"]["severity"] == "low"
    assert issue_by_package["legacy.core"]["code"] == "unknown_license"


def test_license_provenance_report_accepts_collected_license_path_variants(
    tmp_path: Path,
) -> None:
    candidates_root = tmp_path / "candidates"
    candidates_root.mkdir(parents=True)
    for index, license_path in enumerate(
        ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING", "COPYING.rst"),
        start=1,
    ):
        write_manifest(
            candidates_root / f"collected-{index}" / "0.1.0" / "specpm.yaml",
            f"collected-{index}.core",
            "0.1.0",
            "UNKNOWN",
            upstream_uri=f"https://github.com/collected-{index}/collected-{index}",
            license_evidence={
                "source": "ambiguous_license_file",
                "confidence": "low",
                "paths": [license_path],
            },
        )

    report = build_license_provenance_risk_report(candidates_root=candidates_root)

    assert report["summary"]["issuesByCode"] == {"collected_unknown_license_evidence": 5}
    assert {issue["severity"] for issue in report["issues"]} == {"low"}


def test_parse_license_evidence_accepts_inline_path_and_artifact_alias(
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "specpm.yaml"
    manifest.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            "  id: inline.core\n"
            "  name: Inline\n"
            "  version: 1.0.0\n"
            "  license: UNKNOWN\n"
            "  licenseEvidence:\n"
            "    source: ambiguous_license_file\n"
            "    confidence: low\n"
            "    paths: LICENSE\n"
            "foreignArtifacts:\n"
            "  - artifact: upstream_repository\n"
            "    uri: https://github.com/inline/inline\n"
        ),
        encoding="utf-8",
    )

    record = parse_specpm_license_provenance(manifest, "candidate")

    assert record.license_evidence == {
        "source": "ambiguous_license_file",
        "confidence": "low",
        "paths": ["LICENSE"],
    }
    assert record.upstream_artifacts[0].artifact_id == "upstream_repository"


def test_license_provenance_report_covers_upstream_edge_cases(tmp_path: Path) -> None:
    candidates_root = tmp_path / "candidates"
    candidates_root.mkdir(parents=True)
    write_manifest(
        candidates_root / "missing-upstream" / "1.0.0" / "specpm.yaml",
        "missing_upstream.core",
        "1.0.0",
        "MIT",
        upstream_uri=None,
    )
    write_manifest(
        candidates_root / "duplicate-upstream" / "1.0.0" / "specpm.yaml",
        "duplicate_upstream.core",
        "1.0.0",
        "MIT",
        upstream_uri="https://github.com/duplicate-upstream/duplicate-upstream",
        extra_upstream_uri="https://github.com/duplicate-upstream/duplicate-upstream.git",
    )
    write_manifest(
        candidates_root / "empty-upstream" / "1.0.0" / "specpm.yaml",
        "empty_upstream.core",
        "1.0.0",
        "MIT",
        upstream_uri="",
    )
    write_manifest(
        candidates_root / "bad-github-upstream" / "1.0.0" / "specpm.yaml",
        "bad_github_upstream.core",
        "1.0.0",
        "MIT",
        upstream_uri="https://github.com/",
    )

    report = build_license_provenance_risk_report(candidates_root=candidates_root)

    issues_by_code = report["summary"]["issuesByCode"]
    assert issues_by_code["missing_upstream_repository"] == 1
    assert issues_by_code["duplicate_upstream_repository_entries"] == 1
    assert issues_by_code["invalid_upstream_repository_uri"] == 2


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


def test_cli_license_provenance_report_writes_output_file(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    output = tmp_path / "license-provenance.json"
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
            "--accepted-root",
            str(accepted_root),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["summary"]["records"] == 1


def write_manifest(
    path: Path,
    package_id: str,
    version: str,
    license_name: str | None,
    upstream_uri: str | None,
    license_evidence: dict[str, object] | None = None,
    extra_upstream_uri: str | None = None,
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
        if extra_upstream_uri is not None:
            upstream_block += (
                "  - id: upstream_repository\n"
                f'    uri: "{extra_upstream_uri}"\n'
                "    role: secondary_intent_source\n"
            )

    license_block = ""
    if license_name is not None:
        license_block = f"  license: {license_name}\n"
    if license_evidence is not None:
        source = license_evidence["source"]
        confidence = license_evidence["confidence"]
        paths = license_evidence["paths"]
        paths_block = "    paths: []\n"
        if paths:
            paths_block = "    paths:\n" + "".join(f"      - {path}\n" for path in paths)
        license_block += (
            f"  licenseEvidence:\n    source: {source}\n    confidence: {confidence}\n{paths_block}"
        )

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
