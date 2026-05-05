from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.collector import HarvestOptions, collect_local_repository
from spec_harvester.drafter import DraftOptions, draft_spec_package, render_scalar
from spec_harvester.promoter import PromoteOptions, infer_manifest_entry_path, promote_candidate


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
