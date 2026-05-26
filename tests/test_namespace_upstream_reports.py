from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.namespace_reports import (
    build_namespace_upstream_report,
    parse_upstream_repository_reference,
)


def test_build_namespace_upstream_report_detects_duplicates_and_mismatches(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    candidates_root = tmp_path / "candidates"
    accepted_root.mkdir(parents=True)
    candidates_root.mkdir(parents=True)

    write_manifest(
        accepted_root / "alpha" / "0.1.0" / "specpm.yaml",
        "xyflow.core",
        "0.1.0",
        upstream_uri="https://github.com/xyflow/xyflow",
    )
    write_manifest(
        accepted_root / "beta" / "0.2.0" / "specpm.yaml",
        "xyflow.utils",
        "0.2.0",
        upstream_uri="https://github.com/other/xyflow-utils",
    )
    write_manifest(
        candidates_root / "gamma" / "1.0.0" / "specpm.yaml",
        "other.core",
        "1.0.0",
        upstream_uri="https://github.com/other/other",
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
    )

    assert report["summary"]["records"] == 3
    assert report["summary"]["duplicateNamespaceCount"] == 1
    assert report["summary"]["missingUpstreamCount"] == 0
    assert report["summary"]["upstreamMismatchCount"] == 1
    assert report["summary"]["issueCount"] == 1

    namespace_dup = report["duplicates"]["namespace"][0]
    assert namespace_dup["namespace"] == "xyflow"
    assert namespace_dup["count"] == 2
    assert {item["packageId"] for item in namespace_dup["claimants"]} == {
        "xyflow.core",
        "xyflow.utils",
    }

    mismatch = [
        issue for issue in report["issues"] if issue["code"] == "upstream_namespace_mismatch"
    ]
    assert len(mismatch) == 1
    assert mismatch[0]["packageId"] == "xyflow.utils"


def test_build_namespace_upstream_report_ignores_owner_case(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    write_manifest(
        accepted_root / "case" / "1.0.0" / "specpm.yaml",
        "SoundBlaster.core",
        "1.0.0",
        upstream_uri="https://github.com/soundblaster/soundblaster",
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=None,
    )

    mismatch = [
        issue for issue in report["issues"] if issue["code"] == "upstream_namespace_mismatch"
    ]
    assert report["summary"]["records"] == 1
    assert report["summary"]["upstreamMismatchCount"] == 0
    assert mismatch == []


def test_build_namespace_upstream_report_accepts_repository_name_match(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    write_manifest(
        accepted_root / "xyflow" / "1.0.0" / "specpm.yaml",
        "xyflow.core",
        "1.0.0",
        upstream_uri="https://github.com/SoundBlaster/xyflow",
    )
    write_manifest(
        accepted_root / "docc2context" / "1.0.0" / "specpm.yaml",
        "docc2context.core",
        "1.0.0",
        upstream_uri="git@github.com:SoundBlaster/docc2context.git",
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=None,
    )

    assert report["summary"]["records"] == 2
    assert report["summary"]["upstreamMismatchCount"] == 0
    assert report["issues"] == []


def test_build_namespace_upstream_report_accepts_separator_variants(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    write_manifest(
        accepted_root / "navigation" / "1.0.0" / "specpm.yaml",
        "navigation_split_view.core",
        "1.0.0",
        upstream_uri="https://github.com/example/NavigationSplitView",
    )
    write_manifest(
        accepted_root / "page-index" / "1.0.0" / "specpm.yaml",
        "page_index_instance.core",
        "1.0.0",
        upstream_uri="https://github.com/example/page-index-instance",
    )
    write_manifest(
        accepted_root / "nested" / "1.0.0" / "specpm.yaml",
        "nested-swiftui-a11y.core",
        "1.0.0",
        upstream_uri="https://github.com/example/NestedSwiftUIA11y",
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=None,
    )

    assert report["summary"]["records"] == 3
    assert report["summary"]["upstreamMismatchCount"] == 0
    assert report["issues"] == []


def test_build_namespace_upstream_report_keeps_true_mismatch(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    write_manifest(
        accepted_root / "navigation" / "1.0.0" / "specpm.yaml",
        "navigation_split_view.core",
        "1.0.0",
        upstream_uri="https://github.com/example/OtherNavigation",
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=None,
    )

    assert report["summary"]["upstreamMismatchCount"] == 1
    assert report["issues"][0]["code"] == "upstream_namespace_mismatch"


def test_parse_upstream_repository_reference_supports_github_url_forms() -> None:
    https = parse_upstream_repository_reference("https://github.com/SoundBlaster/xyflow.git")
    ssh = parse_upstream_repository_reference("git@github.com:SoundBlaster/docc2context.git")

    assert https is not None
    assert https.owner == "SoundBlaster"
    assert https.name == "xyflow"
    assert ssh is not None
    assert ssh.owner == "SoundBlaster"
    assert ssh.name == "docc2context"


def test_parse_upstream_repository_reference_rejects_empty_repository_name() -> None:
    assert parse_upstream_repository_reference("https://github.com/SoundBlaster/.git") is None
    assert parse_upstream_repository_reference("git@github.com:SoundBlaster/.git") is None


def test_build_namespace_upstream_report_reports_missing_upstream(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        "demo.core",
        "1.0.0",
        upstream_uri=None,
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=None,
    )

    assert report["summary"]["missingUpstreamCount"] == 1
    assert report["issues"][0]["code"] == "missing_upstream_repository"
    assert report["issues"][0]["packageId"] == "demo.core"


def test_namespace_upstream_report_preserves_artifact_before_next_top_level_block(
    tmp_path: Path,
) -> None:
    accepted_root = tmp_path / "accepted"
    accepted_root.mkdir(parents=True)
    manifest = accepted_root / "demo" / "1.0.0" / "specpm.yaml"
    write_manifest(
        manifest,
        "demo.core",
        "1.0.0",
        upstream_uri="https://github.com/demo/demo",
        trailing_keywords=True,
    )

    report = build_namespace_upstream_report(
        accepted_root=accepted_root,
        candidates_root=None,
    )

    assert report["summary"]["records"] == 1
    assert report["summary"]["missingUpstreamCount"] == 0
    assert report["issues"] == []
    assert report["records"][0]["upstreamArtifacts"][0]["uri"] == "https://github.com/demo/demo"


def test_cli_namespace_upstream_report_emits_json(tmp_path: Path) -> None:
    candidates_root = tmp_path / "candidates"
    accepted_root = tmp_path / "accepted"
    candidates_root.mkdir()
    accepted_root.mkdir()
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        "demo.core",
        "1.0.0",
        upstream_uri="https://github.com/demo/demo",
    )

    exit_code = main(
        [
            "governance-upstream-report",
            "--candidates-root",
            str(candidates_root),
            "--accepted-root",
            str(accepted_root),
        ]
    )

    assert exit_code == 0


def test_cli_namespace_upstream_report_writes_output_file(tmp_path: Path) -> None:
    accepted_root = tmp_path / "accepted"
    output = tmp_path / "namespace-upstream.json"
    accepted_root.mkdir()
    write_manifest(
        accepted_root / "demo" / "1.0.0" / "specpm.yaml",
        "demo.core",
        "1.0.0",
        upstream_uri="https://github.com/demo/demo",
    )

    exit_code = main(
        [
            "governance-upstream-report",
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
    upstream_uri: str | None,
    trailing_keywords: bool = False,
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
    path.write_text(
        (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            "metadata:\n"
            f"  id: {package_id}\n"
            "  name: Demo package\n"
            f"  version: {version}\n"
            "index:\n"
            "  provides:\n"
            "    capabilities: []\n"
            "  intents: []\n"
            f"{upstream_block}" + ("keywords:\n  - demo\n" if trailing_keywords else "")
        ),
        encoding="utf-8",
    )
