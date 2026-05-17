from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.collector import (
    HarvestOptions,
    classify_file,
    collect_local_repository,
    markdown_headings,
    parse_package_json,
)
from spec_harvester.drafter import DraftOptions, draft_spec_package, render_scalar
from spec_harvester.interface_index import (
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    render_public_interface_index_json,
)
from spec_harvester.promoter import (
    PromoteOptions,
    append_local_manifest_entry,
    infer_manifest_entry_path,
    promote_candidate,
    validate_with_specpm,
)


def test_collect_local_repository_extracts_safe_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n\n## Usage\n\ncontent\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/demo",
                "version": "1.2.3",
                "description": "Demo package",
                "license": "MIT",
                "scripts": {"build": "vite build", "test": "vitest"},
                "dependencies": {"react": "^19.0.0"},
                "peerDependencies": {"react-dom": "^19.0.0"},
                "exports": {".": "./dist/index.js"},
            }
        ),
        encoding="utf-8",
    )
    package_dir = repo / "packages" / "core"
    package_dir.mkdir(parents=True)
    (package_dir / "package.json").write_text(
        json.dumps({"name": "@example/core", "version": "0.1.0"}),
        encoding="utf-8",
    )

    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/demo",
            revision="abc123",
        )
    )

    assert snapshot["kind"] == "SpecHarvesterEvidenceSnapshot"
    assert snapshot["source"]["repository"] == "https://github.com/example/demo"
    assert snapshot["source"]["revision"] == "abc123"
    assert snapshot["source"]["label"] == "demo"
    assert "path" not in snapshot["source"]
    assert "generatedAt" not in snapshot
    assert snapshot["policy"]["execution"] == "none"
    assert snapshot["analyzerPolicy"] == {
        "schemaVersion": 1,
        "inputAuthority": "untrusted_repository_content",
        "outputAuthority": "untrusted_analyzer_metadata",
        "allowedExecutions": ["none"],
        "networkAccess": "none",
        "packageScripts": "not_run",
        "allowedConfidence": ["high", "medium", "low"],
        "requiresAnalyzerId": True,
        "requiresAnalyzerVersion": True,
        "requiresSourceRevision": True,
        "requiresSourceDigests": True,
    }
    assert snapshot["summary"]["fileCount"] == 4
    assert snapshot["summary"]["packageManifestCount"] == 2

    by_path = {item["path"]: item for item in snapshot["files"]}
    assert by_path["README.md"]["headings"] == ["Demo", "Usage"]
    assert by_path["package.json"]["package"]["name"] == "@example/demo"
    assert by_path["package.json"]["package"]["scripts"] == ["build", "test"]
    assert by_path["package.json"]["package"]["dependencies"] == ["react"]
    assert by_path["package.json"]["package"]["peerDependencies"] == ["react-dom"]
    assert by_path["package.json"]["package"]["exports"] == ["."]


def test_collect_local_repository_snapshot_is_deterministic(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")

    options = HarvestOptions(
        source=repo,
        repository="https://github.com/example/demo",
        revision="abc123",
    )

    assert collect_local_repository(options) == collect_local_repository(options)


def test_collect_local_repository_rejects_missing_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        collect_local_repository(HarvestOptions(source=tmp_path / "missing"))


def test_collect_local_repository_skips_paths_outside_source(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "package.json").write_text(
        json.dumps({"name": "@outside/secret", "version": "1.0.0"}),
        encoding="utf-8",
    )
    packages = repo / "packages"
    packages.mkdir()
    (packages / "core").symlink_to(outside, target_is_directory=True)

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["summary"]["fileCount"] == 0
    assert snapshot["summary"]["skippedFileCount"] == 1
    assert snapshot["skippedFiles"] == [
        {
            "path": "packages/core/package.json",
            "reason": "path_outside_source",
        }
    ]


def test_collect_local_repository_logs_internal_symlink_skips(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    target = repo / "real-package.json"
    target.write_text(
        json.dumps({"name": "@example/real", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (repo / "package.json").symlink_to(target)

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert snapshot["summary"]["fileCount"] == 0
    assert snapshot["summary"]["skippedFileCount"] == 1
    assert snapshot["skippedFiles"] == [
        {
            "path": "package.json",
            "reason": "symlink_unsupported",
        }
    ]


def test_collect_local_repository_sorts_skipped_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    target = repo / "real-package.json"
    target.write_text(
        json.dumps({"name": "@example/real", "version": "1.0.0"}),
        encoding="utf-8",
    )
    z_path = repo / "z-package.json"
    a_path = repo / "a-package.json"
    z_path.symlink_to(target)
    a_path.symlink_to(target)
    monkeypatch.setattr(
        "spec_harvester.collector.candidate_files",
        lambda _root: [z_path, a_path],
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    assert [item["path"] for item in snapshot["skippedFiles"]] == [
        "a-package.json",
        "z-package.json",
    ]


def test_collect_local_repository_logs_non_file_and_large_file_skips(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    package_dir = repo / "package.json"
    package_dir.mkdir()
    readme = repo / "README.md"
    readme.write_text("# Demo\ncontent\n", encoding="utf-8")
    monkeypatch.setattr(
        "spec_harvester.collector.candidate_files",
        lambda _root: [package_dir, readme],
    )

    snapshot = collect_local_repository(HarvestOptions(source=repo, max_file_bytes=4))

    assert snapshot["summary"]["fileCount"] == 0
    assert snapshot["skippedFiles"] == [
        {"path": "README.md", "reason": "file_too_large", "size": 15, "maxFileBytes": 4},
        {"path": "package.json", "reason": "not_regular_file"},
    ]


def test_collect_local_repository_records_binary_file_without_text_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    package_dir = repo / "packages" / "core" / "src"
    package_dir.mkdir(parents=True)
    entrypoint = package_dir / "index.js"
    entrypoint.write_bytes(b"\xff\xfe\x00")

    snapshot = collect_local_repository(HarvestOptions(source=repo))

    record = snapshot["files"][0]
    assert record["path"] == "packages/core/src/index.js"
    assert record["kind"] == "source_entrypoint"
    assert "package" not in record
    assert "headings" not in record


def test_metadata_helpers_cover_static_file_variants(tmp_path: Path) -> None:
    workflow = tmp_path / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True)
    workflow.touch()

    assert classify_file(workflow) == "workflow"
    assert classify_file(tmp_path / "pnpm-workspace.yaml") == "workspace_manifest"
    assert classify_file(tmp_path / "index.ts") == "source_entrypoint"
    assert classify_file(tmp_path / "notes.txt") == "metadata"
    assert markdown_headings("# One\n## Two\n### Three\n", limit=2) == ["One", "Two"]
    assert parse_package_json("{") is None
    assert parse_package_json("[]") is None
    assert parse_package_json('{"exports":"./dist/index.js"}') == {"exports": ["."]}


def test_cli_writes_harvest_snapshot(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n", encoding="utf-8")
    out = tmp_path / "out"

    result = main(["collect-local", str(repo), "--out", str(out)])

    assert result == 0
    snapshot = json.loads((out / "harvest.json").read_text(encoding="utf-8"))
    assert snapshot["summary"]["fileCount"] == 1
    assert json.loads(capsys.readouterr().out)["status"] == "ok"


def test_draft_spec_package_writes_candidate_files(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/react-flow",
                "version": "1.0.0",
                "description": "React library for building node-based editors.",
                "license": "MIT",
                "peerDependencies": {"react": "^19.0.0"},
            }
        ),
        encoding="utf-8",
    )
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/react-flow",
            revision="abc123",
        )
    )
    candidate = tmp_path / "candidate"
    (candidate / "harvest.json").parent.mkdir(parents=True)
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.react_flow",
        )
    )

    assert result["status"] == "ok"
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: example.react_flow" in manifest
    assert "preview_only: true" in manifest
    assert "example.react_flow.react_flow" in spec
    assert "intent.javascript.react_library" in spec
    assert "intent.ui.node_based_editor" in spec
    assert "path: harvest.json" in spec


def test_draft_spec_package_keeps_interfaces_matched_to_valid_packages(tmp_path: Path) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"version": "1.0.0", "description": "Root package without a name."}),
        encoding="utf-8",
    )
    package_dir = repo / "packages" / "core"
    package_dir.mkdir(parents=True)
    (package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/core",
                "version": "1.0.0",
                "description": "Core package.",
                "license": "MIT",
            }
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="example.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: package.core" in spec
    assert "Observed import surface for @example/core." in spec


def test_draft_spec_package_keeps_interface_ids_unique_for_scoped_name_collisions(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    first_package_dir = repo / "packages" / "scope-a"
    second_package_dir = repo / "packages" / "scope-b"
    first_package_dir.mkdir(parents=True)
    second_package_dir.mkdir(parents=True)
    (first_package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@scope-a/core",
                "version": "1.0.0",
                "description": "First scoped core package.",
            }
        ),
        encoding="utf-8",
    )
    (second_package_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "@scope-b/core",
                "version": "1.0.0",
                "description": "Second scoped core package.",
            }
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="example.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: package.core\n" in spec
    assert "id: package.core_2\n" in spec
    assert "Observed import surface for @scope-a/core." in spec
    assert "Observed import surface for @scope-b/core." in spec


def test_draft_spec_package_enriches_interfaces_from_public_interface_index(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/core",
                "version": "1.0.0",
                "description": "Core package.",
                "license": "MIT",
                "exports": {".": "./src/index.ts"},
            }
        ),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(
        HarvestOptions(source=repo, repository="https://github.com/example/core", revision="abc123")
    )
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    interface_index_path = tmp_path / "public-api.json"
    interface_index_path.write_text(
        render_public_interface_index_json(public_interface_index_fixture()),
        encoding="utf-8",
    )

    result = draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.core",
            interface_index=interface_index_path,
        )
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    copied_index = candidate / "public-interface-index.json"
    assert copied_index.exists()
    assert result["interfaceIndex"] == str(copied_index)
    assert "id: public_interface_index" in spec
    assert "path: public-interface-index.json" in spec
    assert "interfaces.inbound.package.core" in spec
    assert "Observed public interface for @example/core from PublicInterfaceIndex." in spec
    assert "name: public_symbols" in spec
    assert "application/vnd.spec-harvester.public-interface-index+json" in spec
    assert 'packageId: "@example/core"' in spec
    assert "path: src/index.ts" in spec
    assert "symbolCount: 2" in spec
    assert "name: createGraph" in spec
    assert 'signature: "createGraph(options)"' in spec
    assert "sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" in spec


def test_draft_spec_package_auto_detects_colocated_public_interface_index(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "source": {"label": "demo", "revision": "abc123"},
        "policy": {"execution": "none"},
        "files": [],
    }
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    (candidate / "public-interface-index.json").write_text(
        render_public_interface_index_json(public_interface_index_fixture()),
        encoding="utf-8",
    )

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert result["interfaceIndex"] == str(candidate / "public-interface-index.json")
    assert "id: package.core" in spec
    assert "source: public_interface_index" in spec


def test_draft_spec_package_rejects_invalid_public_interface_index(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "harvest.json").write_text(
        json.dumps({"kind": "SpecHarvesterEvidenceSnapshot", "files": []}),
        encoding="utf-8",
    )
    interface_index_path = tmp_path / "invalid-public-api.json"
    interface_index_path.write_text(json.dumps({"kind": "Wrong"}), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid PublicInterfaceIndex"):
        draft_spec_package(
            DraftOptions(
                snapshot=candidate,
                out=candidate,
                interface_index=interface_index_path,
            )
        )

    assert not (candidate / "specpm.yaml").exists()


def test_draft_spec_package_keeps_capability_ids_unique_for_slug_collisions(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"name": "@example/react-flow", "version": "1.0.0"}),
        encoding="utf-8",
    )
    package_dir = repo / "packages" / "react"
    package_dir.mkdir(parents=True)
    (package_dir / "package.json").write_text(
        json.dumps({"name": "@example/react_flow", "version": "1.0.0"}),
        encoding="utf-8",
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(
        DraftOptions(snapshot=candidate, out=candidate, package_id="example.core")
    )

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    assert "id: example.core.react_flow\n" in spec
    assert "id: example.core.react_flow_2\n" in spec


def test_draft_spec_package_uses_fallback_metadata_without_package_manifests(
    tmp_path: Path,
) -> None:
    snapshot = {
        "kind": "SpecHarvesterEvidenceSnapshot",
        "source": "unexpected",
        "policy": {"execution": "none"},
        "files": [],
    }
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = draft_spec_package(DraftOptions(snapshot=candidate, out=candidate))

    spec = Path(result["spec"]).read_text(encoding="utf-8")
    manifest = (candidate / "specpm.yaml").read_text(encoding="utf-8")
    assert "id: generated_package.core" in manifest
    assert "license: UNKNOWN" in manifest
    assert "intent.package.public_repository_metadata" in spec


def test_draft_spec_package_rejects_unsupported_snapshot_kind(tmp_path: Path) -> None:
    snapshot = tmp_path / "harvest.json"
    snapshot.write_text(json.dumps({"kind": "OtherSnapshot"}), encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported harvest snapshot kind"):
        draft_spec_package(DraftOptions(snapshot=snapshot, out=tmp_path / "candidate"))


def test_render_scalar_quotes_yaml_reserved_words() -> None:
    assert render_scalar("true") == '"true"'
    assert render_scalar("FALSE") == '"FALSE"'
    assert render_scalar("null") == '"null"'
    assert render_scalar("yes") == '"yes"'
    assert render_scalar("off") == '"off"'
    assert render_scalar("~") == '"~"'


def test_cli_draft_writes_candidate_files(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"name": "@example/system", "description": "Core system", "license": "MIT"}),
        encoding="utf-8",
    )
    out = tmp_path / "candidate"
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    out.mkdir()
    (out / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")

    result = main(["draft", str(out), "--out", str(out), "--package-id", "example.core"])

    assert result == 0
    assert (out / "specpm.yaml").exists()
    assert (out / "specs" / "demo.spec.yaml").exists()
    assert json.loads(capsys.readouterr().out)["packageId"] == "example.core"


def test_cli_draft_accepts_public_interface_index(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    repo = tmp_path / "demo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps({"name": "@example/core", "description": "Core system", "license": "MIT"}),
        encoding="utf-8",
    )
    out = tmp_path / "candidate"
    snapshot = collect_local_repository(HarvestOptions(source=repo))
    out.mkdir()
    (out / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    interface_index_path = tmp_path / "public-api.json"
    interface_index_path.write_text(
        render_public_interface_index_json(public_interface_index_fixture()),
        encoding="utf-8",
    )

    result = main(
        [
            "draft",
            str(out),
            "--out",
            str(out),
            "--package-id",
            "example.core",
            "--interface-index",
            str(interface_index_path),
        ]
    )

    cli_result = json.loads(capsys.readouterr().out)
    assert result == 0
    assert cli_result["interfaceIndex"] == str(out / "public-interface-index.json")
    assert "name: createGraph" in (out / "specs" / "demo.spec.yaml").read_text(encoding="utf-8")


def test_promote_candidate_copies_package_and_updates_manifest(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    validator = tmp_path / "specpm"
    validator.write_text('#!/bin/sh\nprintf \'{"status":"warning_only"}\\n\'\n', encoding="utf-8")
    validator.chmod(0o755)
    accepted_root = tmp_path / "accepted"
    manifest = tmp_path / "accepted-packages.yml"

    result = promote_candidate(
        PromoteOptions(
            candidate=candidate,
            accepted_root=accepted_root,
            manifest=manifest,
            manifest_entry_path="accepted/example.core/0.1.0",
            specpm_command=str(validator),
        )
    )

    destination = accepted_root / "example.core" / "0.1.0"
    assert result["status"] == "ok"
    assert result["validationStatus"] == "warning_only"
    assert (destination / "specpm.yaml").exists()
    assert (destination / "harvest.json").exists()
    assert (destination / "specs" / "demo.spec.yaml").exists()
    assert "  - path: accepted/example.core/0.1.0\n" in manifest.read_text(encoding="utf-8")


def test_promote_candidate_rejects_candidate_symlinks(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    (candidate / "evidence-link").symlink_to(outside)

    with pytest.raises(ValueError, match="unsupported symlink"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                skip_validation=True,
            )
        )


def test_promote_candidate_rejects_missing_candidate_and_manifest(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Candidate directory does not exist"):
        promote_candidate(
            PromoteOptions(
                candidate=tmp_path / "missing",
                accepted_root=tmp_path / "accepted",
                skip_validation=True,
            )
        )

    candidate = tmp_path / "candidate"
    candidate.mkdir()
    with pytest.raises(ValueError, match="missing specpm.yaml"):
        promote_candidate(PromoteOptions(candidate=candidate, accepted_root=tmp_path / "accepted"))


def test_promote_candidate_rejects_existing_destination_without_force(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    destination = tmp_path / "accepted" / "example.core" / "0.1.0"
    destination.mkdir(parents=True)

    with pytest.raises(ValueError, match="Destination already exists"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                skip_validation=True,
            )
        )


def test_promote_candidate_rejects_escaping_package_subdir(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)

    with pytest.raises(ValueError, match="escapes accepted root"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                package_subdir="../escape",
                skip_validation=True,
            )
        )


def test_promote_candidate_rejects_invalid_specpm_validation(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    validator = tmp_path / "specpm"
    validator.write_text('#!/bin/sh\nprintf \'{"status":"invalid"}\\n\'\n', encoding="utf-8")
    validator.chmod(0o755)

    with pytest.raises(ValueError, match="SpecPM validation failed"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                specpm_command=str(validator),
            )
        )


def test_validate_with_specpm_reports_tool_failures(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()

    with pytest.raises(ValueError, match="was not found"):
        validate_with_specpm(candidate, command=str(tmp_path / "missing-specpm"))

    non_json = tmp_path / "non-json-specpm"
    non_json.write_text("#!/bin/sh\necho nope\n", encoding="utf-8")
    non_json.chmod(0o755)
    with pytest.raises(ValueError, match="did not return JSON"):
        validate_with_specpm(candidate, command=str(non_json))

    failed = tmp_path / "failed-specpm"
    failed.write_text('#!/bin/sh\nprintf \'{"status":"error"}\\n\'\nexit 2\n', encoding="utf-8")
    failed.chmod(0o755)
    with pytest.raises(ValueError, match="failed unexpectedly"):
        validate_with_specpm(candidate, command=str(failed), pythonpath="src")


def test_promote_candidate_inserts_manifest_entry_inside_packages_block(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text(
        "schemaVersion: 1\n"
        "packages:\n"
        "  - path: existing/package\n"
        "# keep comment\n"
        "metadata:\n"
        "  owner: test\n",
        encoding="utf-8",
    )

    promote_candidate(
        PromoteOptions(
            candidate=candidate,
            accepted_root=tmp_path / "accepted",
            manifest=manifest,
            manifest_entry_path="accepted/example.core/0.1.0",
            skip_validation=True,
        )
    )

    text = manifest.read_text(encoding="utf-8")
    assert "  - path: accepted/example.core/0.1.0\n" in text
    assert text.index("  - path: accepted/example.core/0.1.0") < text.index("metadata:")


def test_promote_candidate_accepts_empty_packages_list_with_inline_comment(
    tmp_path: Path,
) -> None:
    candidate = draft_demo_candidate(tmp_path)
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text(
        "schemaVersion: 1\n"
        "packages: []  # generated packages are inserted here\n"
        "metadata:\n"
        "  owner: test\n",
        encoding="utf-8",
    )

    promote_candidate(
        PromoteOptions(
            candidate=candidate,
            accepted_root=tmp_path / "accepted",
            manifest=manifest,
            manifest_entry_path="accepted/example.core/0.1.0",
            skip_validation=True,
        )
    )

    text = manifest.read_text(encoding="utf-8")
    assert "packages:\n  - path: accepted/example.core/0.1.0\n" in text
    assert text.index("  - path: accepted/example.core/0.1.0") < text.index("metadata:")


def test_promote_candidate_rejects_unsafe_manifest_entry_path(tmp_path: Path) -> None:
    candidate = draft_demo_candidate(tmp_path)

    with pytest.raises(ValueError, match="relative|parent|newlines"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=tmp_path / "accepted",
                manifest=tmp_path / "accepted-packages.yml",
                manifest_entry_path="../accepted/example.core/0.1.0",
                skip_validation=True,
            )
        )


def test_append_local_manifest_entry_rejects_invalid_packages_field(tmp_path: Path) -> None:
    manifest = tmp_path / "accepted-packages.yml"
    manifest.write_text("schemaVersion: 1\npackages: wrong\n", encoding="utf-8")

    with pytest.raises(ValueError, match="block list or an empty list"):
        append_local_manifest_entry(manifest, "accepted/example.core/0.1.0")


def test_infer_manifest_entry_path_requires_relative_manifest_path(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest-root" / "accepted-packages.yml"
    destination = tmp_path / "accepted" / "example.core" / "0.1.0"
    manifest.parent.mkdir()
    destination.mkdir(parents=True)

    with pytest.raises(ValueError, match="manifest entry path"):
        infer_manifest_entry_path(manifest, destination)


def test_promote_candidate_force_preserves_destination_when_copy_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = draft_demo_candidate(tmp_path)
    accepted_root = tmp_path / "accepted"
    destination = accepted_root / "example.core" / "0.1.0"
    destination.mkdir(parents=True)
    existing_file = destination / "keep.txt"
    existing_file.write_text("keep", encoding="utf-8")

    def fail_copytree(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise OSError("copy failed")

    monkeypatch.setattr("spec_harvester.promoter.shutil.copytree", fail_copytree)

    with pytest.raises(OSError, match="copy failed"):
        promote_candidate(
            PromoteOptions(
                candidate=candidate,
                accepted_root=accepted_root,
                force=True,
                skip_validation=True,
            )
        )

    assert existing_file.read_text(encoding="utf-8") == "keep"


def test_cli_promote_writes_json_result(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    candidate = draft_demo_candidate(tmp_path)
    accepted_root = tmp_path / "accepted"

    result = main(
        [
            "promote",
            str(candidate),
            "--accepted-root",
            str(accepted_root),
            "--skip-validation",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert result == 0
    assert output["packageId"] == "example.core"
    assert output["validationStatus"] == "skipped"
    assert (accepted_root / "example.core" / "0.1.0" / "specpm.yaml").exists()


def draft_demo_candidate(tmp_path: Path) -> Path:
    repo = tmp_path / "demo"
    repo.mkdir(exist_ok=True)
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/demo",
                "version": "1.0.0",
                "description": "Demo package",
                "license": "MIT",
            }
        ),
        encoding="utf-8",
    )
    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/demo",
            revision="abc123",
        )
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir(exist_ok=True)
    (candidate / "harvest.json").write_text(json.dumps(snapshot), encoding="utf-8")
    draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.core",
        )
    )
    return candidate


def public_interface_index_fixture() -> dict:
    return new_public_interface_index(
        source_revision="abc123",
        analyzers=[
            analyzer_record(
                "js-ts-manifest-export-analyzer",
                "0.1.0",
                execution="none",
                confidence="medium",
            )
        ],
        packages=[
            {
                "id": "@example/core",
                "path": ".",
                "language": "javascript-typescript",
                "entrypoints": [
                    {
                        "path": "src/index.ts",
                        "symbols": [
                            {
                                "name": "GraphOptions",
                                "kind": "type",
                                "visibility": "public",
                                "evidence": evidence_record("src/index.ts", "a" * 64),
                            },
                            {
                                "name": "createGraph",
                                "kind": "function",
                                "visibility": "public",
                                "signature": "createGraph(options)",
                                "evidence": evidence_record("src/index.ts", "a" * 64),
                            },
                        ],
                    }
                ],
            }
        ],
    )
