from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.collector import HarvestOptions, collect_local_repository
from spec_harvester.drafter import DraftOptions, draft_spec_package
from spec_harvester.promoter import PromoteOptions, promote_candidate


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
