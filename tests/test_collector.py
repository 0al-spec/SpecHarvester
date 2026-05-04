from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.collector import HarvestOptions, collect_local_repository


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
