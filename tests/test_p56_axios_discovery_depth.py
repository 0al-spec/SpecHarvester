"""Replay a bounded authoring artifact; not a semantic utility benchmark."""

import hashlib
import json
import tarfile
from pathlib import Path, PurePosixPath

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SPECS/EVIDENCE/P56-AXIOS-DISCOVERY"
AUTHOR = EVIDENCE / "author"
REVISION = "509719387e4993392ca40da03a49678269cdfb90"


def _read(path):
    return json.loads(path.read_text())


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def test_discovery_follow_up_is_bound_and_does_not_replace_originals():
    receipt = _read(EVIDENCE / "verification.json")
    baseline = _read(ROOT / "SPECS/EVIDENCE/P56-T4/generation-report.json")
    original = next(row for row in baseline["repositories"] if row["repositoryId"] == "axios-axios")
    assert receipt["experiment"] == "p56-axios-discovery-depth/v1"
    assert receipt["author"]["model"] == "gpt-5.6-sol"
    assert receipt["author"]["reasoningEffort"] == "high"
    assert receipt["author"]["usage"] is None
    assert receipt["source"]["revision"] == original["revision"] == REVISION
    assert receipt["originalCandidateSha256"] == original["candidateSha256"]
    original_copy = AUTHOR / "original"
    assert {
        str(path.relative_to(original_copy)): _sha(path.read_bytes())
        for path in original_copy.rglob("*")
        if path.is_file()
    } == original["files"]
    assert receipt["authority"] == {
        "humanReview": "pending",
        "publicationAuthorized": False,
        "runtimeExecuted": False,
        "t6Completed": False,
    }
    assert receipt["runtimeIsolationProven"] is False
    actual = {
        str(path.relative_to(AUTHOR)): _sha(path.read_bytes())
        for path in AUTHOR.rglob("*")
        if path.is_file()
    }
    assert actual == receipt["authorArtifacts"]
    assert not any(path.is_symlink() for path in AUTHOR.rglob("*"))
    for path in AUTHOR.rglob("*"):
        if path.is_file():
            assert b"/Users/" not in path.read_bytes()


def test_capability_map_binds_ranges_to_retained_source_bytes():
    receipt = _read(EVIDENCE / "verification.json")
    archive = EVIDENCE / "sources.tar.gz"
    assert _sha(archive.read_bytes()) == receipt["source"]["archiveSha256"]
    sources = {}
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            path = PurePosixPath(member.name)
            assert member.isfile() and not path.is_absolute() and ".." not in path.parts
            assert member.name not in sources
            sources[member.name] = tar.extractfile(member).read()
    assert {path: _sha(data) for path, data in sources.items()} == receipt["source"]["files"]
    coverage = _read(AUTHOR / "capability-map.json")
    assert coverage["revision"] == REVISION
    assert coverage["experiment"] == receipt["experiment"]
    ids = [item["id"] for item in coverage["items"]]
    assert ids and len(ids) == len(set(ids))
    for item in coverage["items"]:
        assert item["userNeed"] and item["summary"] and item["sources"]
        for reference in item["sources"]:
            data = sources[reference["path"]]
            assert reference["sha256"] == _sha(data)
            assert 1 <= reference["startLine"] <= reference["endLine"] <= len(data.splitlines())
        for stage in ("before", "after"):
            assert item[stage]["status"] in {"covered", "partial", "missing", "excluded", "unknown"}
            assert item[stage]["reason"]
    assert (AUTHOR / "inventory-initial.json").is_file()
    assert (AUTHOR / "review.ru.md").is_file()


def test_packaged_excerpts_preserve_exact_source_bytes_and_ranges():
    with tarfile.open(EVIDENCE / "sources.tar.gz") as tar:
        sources = {member.name: tar.extractfile(member).read() for member in tar.getmembers()}
    candidate = AUTHOR / "candidate"
    provenance = _read(candidate / "evidence/sources.json")
    assert provenance["revision"] == REVISION
    paths = [entry["path"] for entry in provenance["entries"]]
    assert paths and len(paths) == len(set(paths))
    for entry in provenance["entries"]:
        source = sources[entry["sourcePath"]]
        assert _sha(source) == entry["sourceSha256"]
        lines = source.splitlines(keepends=True)
        assert 1 <= entry["startLine"] <= entry["endLine"] <= len(lines)
        expected = b"".join(lines[entry["startLine"] - 1 : entry["endLine"]])
        path = (candidate / entry["path"]).resolve()
        assert path.is_relative_to(candidate.resolve())
        assert path.read_bytes() == expected
        assert _sha(expected) == entry["excerptSha256"]


def test_preview_keeps_draft_authority_and_explicit_capability_index():
    candidate = AUTHOR / "candidate"
    manifest = yaml.safe_load((candidate / "specpm.yaml").read_text())
    assert manifest["preview_only"] is True
    declared = set()
    for entry in manifest["specs"]:
        path = (candidate / entry["path"]).resolve()
        assert path.is_relative_to(candidate.resolve())
        spec = yaml.safe_load(path.read_text())
        assert spec["metadata"]["status"] == "draft"
        declared.update(item["id"] for item in spec["provides"]["capabilities"])
        for evidence in spec["evidence"]:
            path = (candidate / evidence["path"]).resolve()
            assert path.is_relative_to(candidate.resolve()) and path.is_file()
    assert declared == set(manifest["index"]["provides"]["capabilities"])
    assert not manifest["index"]["provides"].get("intents")


def test_preview_passes_current_specpm_without_omitting_evidence():
    core = pytest.importorskip("specpm.core", reason="Run in the SpecPM integration job")
    candidate = AUTHOR / "candidate"
    result = core.validate_package(candidate)
    assert result["errors"] == []
    assert [warning["code"] for warning in result["warnings"]] == ["preview_only_package"]
    manifest = yaml.safe_load((candidate / "specpm.yaml").read_text())
    errors = []
    collected = set(core.collect_package_files(candidate, manifest, errors))
    assert errors == []
    actual = {str(path.relative_to(candidate)) for path in candidate.rglob("*") if path.is_file()}
    assert collected == actual
