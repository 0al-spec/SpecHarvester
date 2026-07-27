from __future__ import annotations

import json
from pathlib import Path

import pytest

import spec_harvester.mass_corpus_checkout_readiness as readiness_module
from spec_harvester.mass_corpus_checkout_readiness import (
    MassCorpusCheckoutReadiness,
    MassCorpusCheckoutReadinessOptions,
    _canonical_origin,
    _metadata_by_id,
    _validate_structure,
    git_origin,
    root_license_files,
)


def test_one_hundred_clean_checkouts_unlock_p53_t5(tmp_path: Path) -> None:
    inputs, metadata, revisions = write_inputs(tmp_path)
    readiness = build_readiness(inputs, metadata, revisions, tmp_path / "report.json")

    report = readiness.run()

    assert report["status"] == "passed"
    assert report["summary"]["repositoryCount"] == 100
    assert report["summary"]["readyCount"] == 100
    assert report["summary"]["waveDistribution"] == {
        "wave-1": 25,
        "wave-2": 25,
        "wave-3": 25,
        "wave-4": 25,
    }
    assert report["decision"]["p53T5Unlocked"] is True
    assert all(value is False for value in report["executionBoundary"].values())


def test_missing_checkout_blocks_p53_t5_and_records_every_failure(tmp_path: Path) -> None:
    inputs, metadata, revisions = write_inputs(tmp_path)
    (inputs / "checkouts/repo-000").rmdir()
    readiness = build_readiness(inputs, metadata, revisions, tmp_path / "report.json")

    report = readiness.run()

    assert report["status"] == "failed"
    assert report["decision"]["p53T5Unlocked"] is False
    assert report["summary"]["blockedCount"] == 1
    assert set(report["repositories"][0]["failures"]) == {
        "checkout_missing",
        "checkout_revision_mismatch",
        "checkout_status_unavailable",
        "checkout_origin_mismatch",
        "tracked_size_unavailable",
        "license_evidence_unavailable",
    }


def test_origin_and_license_failures_block_p53_t5(tmp_path: Path) -> None:
    inputs, metadata, revisions = write_inputs(tmp_path)
    readiness = MassCorpusCheckoutReadiness(
        MassCorpusCheckoutReadinessOptions(inputs, metadata, tmp_path / "report.json"),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: "",
        origin_reader=lambda checkout: (
            "https://github.com/example/wrong" if checkout.name == "repo-000" else origin(checkout)
        ),
        size_reader=lambda _checkout: 1024,
        license_reader=lambda _checkout: [],
    )

    report = readiness.run()

    assert report["status"] == "failed"
    assert "checkout_origin_mismatch" in report["repositories"][0]["failures"]
    assert report["summary"]["failureCounts"]["license_evidence_unavailable"] == 100


def test_ssh_origin_with_git_suffix_matches_canonical_https_source(tmp_path: Path) -> None:
    inputs, metadata, revisions = write_inputs(tmp_path)
    readiness = MassCorpusCheckoutReadiness(
        MassCorpusCheckoutReadinessOptions(inputs, metadata, tmp_path / "report.json"),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: "",
        origin_reader=lambda checkout: f"git@github.com:example/{checkout.name}.git",
        size_reader=lambda _checkout: 1024,
        license_reader=lambda _checkout: ["LICENSE"],
    )

    report = readiness.run()

    assert report["status"] == "passed"


def test_position_wave_drift_is_rejected_before_checkout_reading(tmp_path: Path) -> None:
    inputs, metadata_path, revisions = write_inputs(tmp_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["repositories"][0]["position"] = 26
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    readiness = build_readiness(inputs, metadata_path, revisions, tmp_path / "report.json")

    with pytest.raises(ValueError, match="wave does not match position"):
        readiness.run()


def test_dirty_checkout_and_excess_size_are_recorded(tmp_path: Path) -> None:
    inputs, metadata, revisions = write_inputs(tmp_path)
    readiness = MassCorpusCheckoutReadiness(
        MassCorpusCheckoutReadinessOptions(inputs, metadata, tmp_path / "report.json"),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: " M changed.py",
        origin_reader=origin,
        size_reader=lambda _checkout: 2049,
        license_reader=lambda _checkout: ["LICENSE"],
    )

    report = readiness.run()

    assert {"checkout_dirty", "size_budget_exceeded"} <= set(report["repositories"][0]["failures"])


def test_metadata_validation_rejects_invalid_shapes() -> None:
    with pytest.raises(ValueError, match="exactly 100"):
        _metadata_by_id({"repositories": []})
    with pytest.raises(ValueError, match="unique and valid"):
        _metadata_by_id({"repositories": [{"id": "same"}] * 100})

    source = {"id": "repo-000"}
    metadata = {
        "repo-000": {
            "position": 1,
            "wave": "wave-1",
            "ecosystem": "python",
            "repositoryShape": "single_package",
            "sizeBudget": {"maximumBytes": 1},
        }
    }
    with pytest.raises(ValueError, match="matching 100"):
        _validate_structure([source], metadata)


def test_git_and_license_helpers_handle_supported_and_unavailable_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / "LICENSE-APACHE").write_text("license", encoding="utf-8")
    (checkout / "notice.md").write_text("notice", encoding="utf-8")
    (checkout / "README.md").write_text("readme", encoding="utf-8")

    class Result:
        def __init__(self, returncode: int, stdout: str) -> None:
            self.returncode = returncode
            self.stdout = stdout

    monkeypatch.setattr(
        readiness_module.subprocess,
        "run",
        lambda *_args, **_kwargs: Result(0, "https://github.com/example/repo.git\n"),
    )
    assert git_origin(checkout) == "https://github.com/example/repo.git"
    monkeypatch.setattr(readiness_module.subprocess, "run", lambda *_args, **_kwargs: Result(1, ""))
    assert git_origin(checkout) is None
    assert root_license_files(checkout) == ["LICENSE-APACHE", "notice.md"]
    assert root_license_files(tmp_path / "missing") == []
    assert _canonical_origin("https://github.com/example/repo.git") == "example/repo"
    assert _canonical_origin("git@github.com:example/repo.git") == "example/repo"
    assert _canonical_origin("https://gitlab.com/example/repo") is None
    assert _canonical_origin("https://github.com/example/repo/extra") is None


def build_readiness(
    inputs: Path, metadata: Path, revisions: dict[str, str], output: Path
) -> MassCorpusCheckoutReadiness:
    return MassCorpusCheckoutReadiness(
        MassCorpusCheckoutReadinessOptions(inputs, metadata, output),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: "",
        origin_reader=origin,
        size_reader=lambda _checkout: 1024,
        license_reader=lambda _checkout: ["LICENSE"],
    )


def origin(checkout: Path) -> str:
    return f"https://github.com/example/{checkout.name}"


def write_inputs(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    inputs = tmp_path / "inputs"
    checkouts = inputs / "checkouts"
    manifest = ["repositories:"]
    metadata_records = []
    revisions = {}
    for index in range(100):
        repository_id = f"repo-{index:03d}"
        revision = f"{index:040x}"
        revisions[repository_id] = revision
        (checkouts / repository_id).mkdir(parents=True)
        manifest.extend(
            [
                f"  - id: {repository_id}",
                f"    repository: https://github.com/example/{repository_id}",
                f"    revision: {revision}",
                f"    checkout: checkouts/{repository_id}",
                f"    packageId: {repository_id}.core",
                "    labels: [p53_t4]",
            ]
        )
        metadata_records.append(
            {
                "id": repository_id,
                "position": index + 1,
                "wave": f"wave-{(index // 25) + 1}",
                "ecosystem": "python",
                "repositoryShape": "single_package",
                "sizeBudget": {"maximumBytes": 2048},
            }
        )
    inputs.mkdir(exist_ok=True)
    (inputs / "repositories.yml").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    metadata = inputs / "metadata.json"
    metadata.write_text(json.dumps({"repositories": metadata_records}), encoding="utf-8")
    return inputs, metadata, revisions
