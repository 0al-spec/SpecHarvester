from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.accepted_diff import (
    AcceptedCandidateDiffReport,
    AcceptedCandidateDiffReportWriter,
    AcceptedPackageVersions,
    CandidateComparison,
    PackageDiffSource,
    PackageRecordDiff,
    build_accepted_candidate_diff_report,
    collect_package_diff_records,
    parse_specpm_diff_record,
    semver_sort_key,
)
from spec_harvester.cli import main


def test_build_accepted_candidate_diff_report_detects_changed_candidate(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        name="Demo",
        summary="Old summary",
        license_name="MIT",
        capabilities=["demo.read", "demo.write"],
        intents=["intent.package.utility"],
        upstream_revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    )
    write_manifest(
        candidates_root / "demo" / "1.1.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        name="Demo",
        summary="New summary",
        license_name="Apache-2.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility", "intent.package.workflow"],
        upstream_revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        extra_metadata={"licenseEvidence": "evidence.txt"},
    )

    report = build_accepted_candidate_diff_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["kind"] == "SpecHarvesterAcceptedCandidateDiffReport"
    assert report["status"] == "ok"
    assert report["summary"]["acceptedRecords"] == 1
    assert report["summary"]["candidateRecords"] == 1
    assert report["summary"]["changedCount"] == 1

    comparison = report["comparisons"][0]
    assert comparison["status"] == "changed"
    assert comparison["oldPackageVersion"] == "1.0.0"
    assert comparison["newPackageVersion"] == "1.1.0"
    assert comparison["changes"]["capabilities"] == {
        "added": ["demo.stream"],
        "removed": ["demo.write"],
    }
    assert comparison["changes"]["intents"] == {
        "added": ["intent.package.workflow"],
        "removed": [],
    }
    assert {item["field"] for item in comparison["changes"]["metadata"]} == {
        "version",
        "licenseEvidence",
        "summary",
        "license",
    }
    assert comparison["changes"]["upstreamArtifacts"]["changed"] is True


def test_accepted_candidate_diff_report_object_matches_public_wrapper(
    tmp_path: Path,
) -> None:
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
        candidates_root / "demo" / "1.1.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.utility"],
    )

    object_report = AcceptedCandidateDiffReport(accepted_root, candidates_root).report()
    wrapper_report = build_accepted_candidate_diff_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert object_report == wrapper_report
    assert object_report["summary"]["changedCount"] == 1


def test_build_accepted_candidate_diff_report_reports_new_and_unchanged_candidates(
    tmp_path: Path,
) -> None:
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
    write_manifest(
        candidates_root / "fresh" / "0.1.0" / "specpm.yaml",
        package_id="fresh.core",
        version="0.1.0",
        capabilities=["fresh.read"],
        intents=["intent.package.fresh"],
    )

    report = build_accepted_candidate_diff_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["summary"]["unchangedCount"] == 1
    assert report["summary"]["newPackageCount"] == 1
    by_package = {item["packageId"]: item for item in report["comparisons"]}
    assert by_package["demo.core"]["status"] == "unchanged"
    assert by_package["fresh.core"]["status"] == "new_package"
    assert by_package["fresh.core"]["accepted"] is None
    assert by_package["fresh.core"]["changes"]["capabilities"]["added"] == ["fresh.read"]


def test_build_accepted_candidate_diff_report_uses_latest_accepted_semver(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.old"],
        intents=[],
    )
    write_manifest(
        accepted_root / "demo" / "1.2.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.2.0",
        capabilities=["demo.latest"],
        intents=[],
    )
    write_manifest(
        candidates_root / "demo" / "1.3.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.3.0",
        capabilities=["demo.latest"],
        intents=[],
    )

    report = build_accepted_candidate_diff_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    comparison = report["comparisons"][0]
    assert comparison["accepted"]["packageVersion"] == "1.2.0"
    assert comparison["changes"]["capabilities"]["removed"] == []


def test_parse_specpm_diff_record_rejects_missing_metadata(tmp_path: Path) -> None:
    manifest = tmp_path / "specpm.yaml"
    manifest.write_text("kind: SpecPackage\nindex: {}\n", encoding="utf-8")

    try:
        parse_specpm_diff_record(manifest, "candidate")
    except ValueError as exc:
        assert "metadata.id and metadata.version" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing metadata.")


def test_collect_package_diff_records_reports_symlink_and_invalid_manifest(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    root.mkdir()
    invalid = root / "invalid" / "specpm.yaml"
    invalid.parent.mkdir()
    invalid.write_text("kind: SpecPackage\n", encoding="utf-8")
    target = tmp_path / "target-specpm.yaml"
    target.write_text("metadata:\n  id: linked.core\n  version: 1.0.0\n", encoding="utf-8")
    symlink = root / "linked" / "specpm.yaml"
    symlink.parent.mkdir()
    symlink.symlink_to(target)

    records, issues = collect_package_diff_records(root, "candidate")

    assert records == []
    assert {issue["code"] for issue in issues} == {
        "invalid_specpm_manifest",
        "specpm_symlink",
    }


def test_package_diff_source_object_reports_symlink_and_invalid_manifest(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    root.mkdir()
    invalid = root / "invalid" / "specpm.yaml"
    invalid.parent.mkdir()
    invalid.write_text("kind: SpecPackage\n", encoding="utf-8")
    target = tmp_path / "target-specpm.yaml"
    target.write_text("metadata:\n  id: linked.core\n  version: 1.0.0\n", encoding="utf-8")
    symlink = root / "linked" / "specpm.yaml"
    symlink.parent.mkdir()
    symlink.symlink_to(target)

    records, issues = PackageDiffSource(root, "candidate").records_and_issues()

    assert records == []
    assert [issue["code"] for issue in sorted(issues, key=lambda item: item["code"])] == [
        "invalid_specpm_manifest",
        "specpm_symlink",
    ]


def test_collect_package_diff_records_rejects_missing_root(tmp_path: Path) -> None:
    try:
        collect_package_diff_records(tmp_path / "missing", "candidate")
    except ValueError as exc:
        assert "does not exist or is not a directory" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing source root.")


def test_parse_specpm_diff_record_reads_nested_intents_and_artifact_role(
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "specpm.yaml"
    manifest.write_text(
        (
            "metadata:\n"
            "  id: demo.core\n"
            "  version: 1.0.0\n"
            "index:\n"
            "  provides:\n"
            "    capabilities:\n"
            "      - demo.read\n"
            "    intents:\n"
            "      - intent.package.workflow\n"
            "foreignArtifacts:\n"
            "  - id: upstream_repository\n"
            "    uri: https://github.com/example/demo\n"
            "    role: source\n"
            "keywords:\n"
            "  - demo\n"
        ),
        encoding="utf-8",
    )

    record = parse_specpm_diff_record(manifest, "candidate")

    assert record.intents == ("intent.package.workflow",)
    assert record.capabilities == ("demo.read",)
    assert record.upstream_artifacts == (
        {
            "id": "upstream_repository",
            "role": "source",
            "uri": "https://github.com/example/demo",
        },
    )


def test_accepted_candidate_diff_normalizes_nested_license_evidence_metadata(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    write_nested_license_evidence_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        license_evidence_lines=[
            "    source: collected_license_file",
            "    confidence: high",
            "    paths:",
            "      - LICENSE",
        ],
    )
    write_nested_license_evidence_manifest(
        candidates_root / "demo" / "1.0.0" / "specpm.yaml",
        license_evidence_lines=[
            "    paths:",
            "      - LICENSE",
            "    confidence: high",
            "    source: collected_license_file",
        ],
    )

    report = build_accepted_candidate_diff_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    comparison = report["comparisons"][0]
    assert comparison["status"] == "unchanged"
    assert comparison["changes"]["metadata"] == []


def test_candidate_comparison_and_record_diff_objects_preserve_delta_shape(
    tmp_path: Path,
) -> None:
    accepted_manifest = tmp_path / "accepted" / "specpm.yaml"
    candidate_manifest = tmp_path / "candidate" / "specpm.yaml"
    write_manifest(
        accepted_manifest,
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read", "demo.write"],
        intents=["intent.package.utility"],
    )
    write_manifest(
        candidate_manifest,
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read", "demo.stream"],
        intents=["intent.package.workflow"],
    )
    accepted = parse_specpm_diff_record(accepted_manifest, "accepted")
    candidate = parse_specpm_diff_record(candidate_manifest, "candidate")

    changes = PackageRecordDiff(accepted, candidate).changes()
    comparison = CandidateComparison(candidate, accepted).as_dict()

    assert changes == comparison["changes"]
    assert comparison["status"] == "changed"
    assert comparison["changes"]["capabilities"] == {
        "added": ["demo.stream"],
        "removed": ["demo.write"],
    }
    assert comparison["changes"]["intents"] == {
        "added": ["intent.package.workflow"],
        "removed": ["intent.package.utility"],
    }


def test_accepted_package_versions_object_selects_latest_semver(tmp_path: Path) -> None:
    old_manifest = tmp_path / "old" / "specpm.yaml"
    new_manifest = tmp_path / "new" / "specpm.yaml"
    prerelease_manifest = tmp_path / "pre" / "specpm.yaml"
    write_manifest(
        old_manifest, package_id="demo.core", version="1.0.0", capabilities=[], intents=[]
    )
    write_manifest(
        new_manifest, package_id="demo.core", version="1.2.0", capabilities=[], intents=[]
    )
    write_manifest(
        prerelease_manifest,
        package_id="demo.core",
        version="1.2.0-rc.1",
        capabilities=[],
        intents=[],
    )
    records = [
        parse_specpm_diff_record(old_manifest, "accepted"),
        parse_specpm_diff_record(new_manifest, "accepted"),
        parse_specpm_diff_record(prerelease_manifest, "accepted"),
    ]

    latest = AcceptedPackageVersions(tuple(records)).latest_by_package_id()

    assert latest["demo.core"].package_version == "1.2.0"


def test_accepted_candidate_diff_report_writer_creates_parent_directory(
    tmp_path: Path,
) -> None:
    path = tmp_path / "nested" / "diff.json"
    report = {"kind": "SpecHarvesterAcceptedCandidateDiffReport", "summary": {"issueCount": 0}}

    AcceptedCandidateDiffReportWriter(path, report).write()

    assert json.loads(path.read_text(encoding="utf-8")) == report


def test_semver_sort_key_orders_prerelease_and_handles_invalid_versions() -> None:
    assert semver_sort_key("1.0.0") > semver_sort_key("1.0.0-rc.1")
    assert semver_sort_key("1.0.0-rc.2") > semver_sort_key("1.0.0-rc.1")
    assert semver_sort_key("not-semver") < semver_sort_key("0.1.0")


def test_cli_accepted_candidate_diff_report_writes_output(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    output = tmp_path / "diff.json"
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.0.0",
        capabilities=["demo.read"],
        intents=[],
    )
    write_manifest(
        candidates_root / "demo" / "1.1.0" / "specpm.yaml",
        package_id="demo.core",
        version="1.1.0",
        capabilities=["demo.read"],
        intents=[],
    )

    exit_code = main(
        [
            "accepted-candidate-diff-report",
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
    assert report["summary"]["comparedCount"] == 1


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


def write_nested_license_evidence_manifest(
    path: Path,
    *,
    license_evidence_lines: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            "  id: demo.core\n"
            "  name: Demo\n"
            "  version: 1.0.0\n"
            "  summary: Demo package\n"
            "  license: MIT\n"
            "  licenseEvidence:\n" + "\n".join(license_evidence_lines) + "\n"
            "index:\n"
            "  provides:\n"
            "    capabilities:\n"
            "      - demo.read\n"
        ),
        encoding="utf-8",
    )
