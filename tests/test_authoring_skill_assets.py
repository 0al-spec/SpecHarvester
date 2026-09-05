from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/specpm-author-candidate"


def package_documents(package: Path) -> tuple[dict, list[dict]]:
    manifest = yaml.safe_load((package / "specpm.yaml").read_text())
    specs = [yaml.safe_load((package / item["path"]).read_text()) for item in manifest["specs"]]
    return manifest, specs


def test_skill_can_be_copied_without_sibling_or_personal_resources(tmp_path: Path) -> None:
    assert not any(path.is_symlink() for path in SKILL.rglob("*"))
    copied = Path(shutil.copytree(SKILL, tmp_path / SKILL.name))
    entry = (copied / "SKILL.md").read_text()
    metadata = yaml.safe_load(entry.split("---", 2)[1])
    assert metadata["name"] == copied.name
    assert metadata["description"]
    for document in copied.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            path = (document.parent / target).resolve()
            assert path.is_relative_to(copied)
            assert path.is_file()
    assert not any(path.is_symlink() for path in copied.rglob("*"))


@pytest.mark.parametrize("asset", ["template", "example"])
def test_assets_keep_complete_candidate_and_source_bindings(asset: str) -> None:
    package = SKILL / "assets" / asset
    manifest, specs = package_documents(package)
    assert manifest["preview_only"] is True
    assert manifest["kind"] == "SpecPackage"
    provided = {
        capability["id"] for spec in specs for capability in spec["provides"]["capabilities"]
    }
    assert set(manifest["index"]["provides"]["capabilities"]) == provided
    for spec in specs:
        assert spec["metadata"]["status"] == "draft"
        assert isinstance(spec["effects"], dict)
        assert spec["scope"]["includes"] and spec["scope"]["excludes"]
        assert spec["interfaces"]["inbound"]
        assert spec["constraints"]
        supports = {target for evidence in spec["evidence"] for target in evidence["supports"]}
        for capability in spec["provides"]["capabilities"]:
            assert f"provides.capabilities.{capability['id']}" in supports
        for evidence in spec["evidence"]:
            path = (package / evidence["path"]).resolve()
            assert path.is_relative_to(package.resolve())
            assert path.is_file()
        assert spec["provenance"]["sourceConfidence"]["behavior"] in {"low", "unknown"}


@pytest.mark.parametrize("asset", ["template", "example"])
def test_assets_pass_independent_specpm_validation(asset: str) -> None:
    core = pytest.importorskip("specpm.core", reason="Run in the SpecPM integration job")
    report = core.validate_package(SKILL / "assets" / asset)
    assert report["errors"] == []
    assert [item["code"] for item in report["warnings"]] == ["preview_only_package"]


@pytest.mark.parametrize("damage", ["missing_source", "unbound_capability", "unknown_target"])
def test_independent_validation_detects_broken_asset_bindings(tmp_path: Path, damage: str) -> None:
    core = pytest.importorskip("specpm.core", reason="Run in the SpecPM integration job")
    package = Path(shutil.copytree(SKILL / "assets/example", tmp_path / "candidate"))
    if damage == "missing_source":
        (package / "evidence/command.md").unlink()
    elif damage == "unbound_capability":
        manifest_path = package / "specpm.yaml"
        manifest = yaml.safe_load(manifest_path.read_text())
        manifest["index"]["provides"]["capabilities"].append("example.rowpick.unimplemented")
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    else:
        spec_path = package / "specs/main.spec.yaml"
        spec = yaml.safe_load(spec_path.read_text())
        spec["evidence"][0]["supports"].append("constraints.nonexistent")
        spec_path.write_text(yaml.safe_dump(spec, sort_keys=False))
    report = core.validate_package(package)
    codes = {issue["code"] for issue in report["errors"] + report["warnings"]}
    expected = {
        "missing_source": "evidence_path_missing",
        "unbound_capability": "manifest_capability_not_declared",
        "unknown_target": "evidence_support_target_unknown",
    }
    assert expected[damage] in codes
