from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from spec_harvester.final_corpus_checkout_readiness import (
    FinalCorpusCheckoutReadiness,
    FinalCorpusCheckoutReadinessOptions,
    read_metadata,
    tracked_file_bytes,
    validate_corpus_structure,
)
from spec_harvester.source_manifest import read_repository_source_manifests


def test_fifty_source_readiness_passes_and_unlocks_p52_t6(tmp_path: Path) -> None:
    inputs, revisions, metadata = write_inputs(tmp_path)
    readiness = FinalCorpusCheckoutReadiness(
        FinalCorpusCheckoutReadinessOptions(
            inputs=inputs,
            metadata=metadata,
            output=tmp_path / "report.json",
        ),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: "",
        size_reader=lambda _checkout: 1024,
    )

    report = readiness.run()

    assert report["status"] == "passed"
    assert report["summary"]["repositoryCount"] == 50
    assert report["summary"]["readyCount"] == 50
    assert report["decision"]["p52T6Unlocked"] is True
    assert all(value is False for value in report["executionBoundary"].values())


def test_dirty_checkout_blocks_p52_t6(tmp_path: Path) -> None:
    inputs, revisions, metadata = write_inputs(tmp_path)
    readiness = FinalCorpusCheckoutReadiness(
        FinalCorpusCheckoutReadinessOptions(
            inputs=inputs,
            metadata=metadata,
            output=tmp_path / "report.json",
        ),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda checkout: " M source.txt\n" if checkout.name == "repo-00" else "",
        size_reader=lambda _checkout: 1024,
    )

    report = readiness.run()

    assert report["status"] == "failed"
    assert report["decision"]["p52T6Unlocked"] is False
    assert report["repositories"][0]["failures"] == ["checkout_dirty"]


def test_missing_license_evidence_blocks_p52_t6(tmp_path: Path) -> None:
    inputs, revisions, metadata_path = write_inputs(tmp_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["repositories"][0]["licenseProvenance"]["paths"] = []
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    readiness = FinalCorpusCheckoutReadiness(
        FinalCorpusCheckoutReadinessOptions(
            inputs=inputs,
            metadata=metadata_path,
            output=tmp_path / "report.json",
        ),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: "",
        size_reader=lambda _checkout: 1024,
    )

    report = readiness.run()

    assert report["status"] == "failed"
    assert report["repositories"][0]["failures"] == ["license_evidence_unavailable"]


def test_collapsed_corpus_coverage_blocks_p52_t6(tmp_path: Path) -> None:
    inputs, revisions, metadata_path = write_inputs(tmp_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for record in metadata["repositories"]:
        record["ecosystem"] = "python"
        record["repositoryShape"] = "single_package"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    readiness = FinalCorpusCheckoutReadiness(
        FinalCorpusCheckoutReadinessOptions(
            inputs=inputs,
            metadata=metadata_path,
            output=tmp_path / "report.json",
        ),
        head_reader=lambda checkout: revisions[checkout.name],
        dirty_reader=lambda _checkout: "",
        size_reader=lambda _checkout: 1024,
    )

    report = readiness.run()

    assert report["summary"]["readyCount"] == 50
    assert report["summary"]["coveragePolicy"]["status"] == "failed"
    assert report["gateFailures"] == ["corpus_coverage_insufficient"]
    assert report["decision"]["p52T6Unlocked"] is False


def test_durable_p52_t5_fixture_records_passing_fifty_source_gate() -> None:
    root = Path(__file__).resolve().parents[1]
    report = json.loads(
        (
            root / "tests/fixtures/final_corpus_checkout_readiness/"
            "p52-t5-final-corpus-checkout-readiness.example.json"
        ).read_text(encoding="utf-8")
    )

    assert report["status"] == "passed"
    assert report["summary"]["repositoryCount"] == 50
    assert report["summary"]["readyCount"] == 50
    assert report["decision"] == {
        "p52T6Unlocked": True,
        "selectedDecision": "unlock_p52_t6",
    }


def test_readiness_collects_all_source_policy_failures(tmp_path: Path) -> None:
    inputs, revisions, metadata_path = write_inputs(tmp_path)
    manifest_path = inputs / "repositories.yml"
    manifest_path.write_text(
        manifest_path.read_text(encoding="utf-8").replace(
            "https://github.com/example/repo-00",
            "https://github.com.evil/example/repo-00",
        ),
        encoding="utf-8",
    )
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["repositories"][0]["provenance"]["status"] = "unresolved"
    metadata["repositories"][0]["provenance"]["repository"] = "https://github.com/wrong/repo"
    metadata["repositories"][0]["licenseProvenance"]["status"] = "unresolved"
    metadata["repositories"][0]["stopPolicy"]["excludeOnDirtyCheckout"] = False
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    readiness = FinalCorpusCheckoutReadiness(
        FinalCorpusCheckoutReadinessOptions(
            inputs=inputs,
            metadata=metadata_path,
            output=tmp_path / "report.json",
        ),
        head_reader=lambda checkout: (
            "wrong-revision" if checkout.name == "repo-00" else revisions[checkout.name]
        ),
        dirty_reader=lambda checkout: None if checkout.name == "repo-00" else "",
        size_reader=lambda checkout: 4096 if checkout.name == "repo-00" else 1024,
    )

    report = readiness.run()

    assert set(report["repositories"][0]["failures"]) == {
        "repository_not_public_https_github",
        "checkout_revision_mismatch",
        "checkout_status_unavailable",
        "provenance_unresolved",
        "provenance_repository_mismatch",
        "license_provenance_unresolved",
        "stop_policy_incomplete",
        "tracked_size_mismatch",
        "size_budget_exceeded",
    }


def test_metadata_reader_rejects_unavailable_and_duplicate_records(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unavailable"):
        read_metadata(tmp_path / "missing.json")

    path = tmp_path / "metadata.json"
    path.write_text(json.dumps({"repositories": {}}))
    with pytest.raises(ValueError, match="must contain repositories"):
        read_metadata(path)

    path.write_text(json.dumps({"repositories": [{"name": "missing-id"}]}))
    with pytest.raises(ValueError, match="records are invalid"):
        read_metadata(path)

    path.write_text(json.dumps({"repositories": [{"id": "same"}, {"id": "same"}]}))
    with pytest.raises(ValueError, match="duplicate"):
        read_metadata(path)


def test_tracked_file_bytes_reads_only_git_tracked_files(tmp_path: Path) -> None:
    assert tracked_file_bytes(tmp_path / "not-a-checkout") is None

    checkout = tmp_path / "checkout"
    subprocess.run(["git", "init", "-q", str(checkout)], check=True)
    (checkout / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    (checkout / "untracked.txt").write_text("not-counted\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(checkout), "add", "tracked.txt"], check=True)

    assert tracked_file_bytes(checkout) == len("tracked\n")


def test_corpus_structure_rejects_invalid_nested_metadata(tmp_path: Path) -> None:
    inputs, _revisions, metadata_path = write_inputs(tmp_path)
    metadata = read_metadata(metadata_path)
    sources = read_repository_source_manifests(inputs)
    metadata["repo-00"]["sizeBudget"] = {"observedBytes": -1, "maximumBytes": 0}

    with pytest.raises(ValueError, match="size budget is invalid"):
        validate_corpus_structure(sources, metadata)


def test_corpus_structure_rejects_invalid_manifest_metadata_contract(tmp_path: Path) -> None:
    inputs, _revisions, metadata_path = write_inputs(tmp_path)
    sources = read_repository_source_manifests(inputs)
    metadata = read_metadata(metadata_path)

    with pytest.raises(ValueError, match="between 50 and 100"):
        validate_corpus_structure(sources[:-1], metadata)

    with pytest.raises(ValueError, match="ids must match"):
        validate_corpus_structure(
            sources, {key: value for key, value in metadata.items() if key != "repo-00"}
        )

    invalid_revision_sources = [dict(source) for source in sources]
    invalid_revision_sources[0]["revision"] = "short"
    with pytest.raises(ValueError, match="full pinned revision"):
        validate_corpus_structure(invalid_revision_sources, metadata)

    incomplete_metadata = {key: dict(value) for key, value in metadata.items()}
    incomplete_metadata["repo-00"].pop("stopPolicy")
    with pytest.raises(ValueError, match="metadata is incomplete"):
        validate_corpus_structure(sources, incomplete_metadata)


def write_inputs(tmp_path: Path) -> tuple[Path, dict[str, str], Path]:
    inputs = tmp_path / "inputs"
    checkouts = inputs / "checkouts"
    revisions = {f"repo-{index:02d}": f"{index:040x}" for index in range(50)}
    manifest = ["repositories:"]
    metadata_records = []
    for repository_id, revision in revisions.items():
        checkout = checkouts / repository_id
        checkout.mkdir(parents=True)
        (checkout / "LICENSE").write_text("test license\n", encoding="utf-8")
        index = int(repository_id.rsplit("-", maxsplit=1)[1])
        manifest.extend(
            [
                f"  - id: {repository_id}",
                f"    repository: https://github.com/example/{repository_id}",
                f"    revision: {revision}",
                f"    checkout: checkouts/{repository_id}",
            ]
        )
        metadata_records.append(
            {
                "id": repository_id,
                "ecosystem": "python" if index % 2 == 0 else "go",
                "repositoryShape": "single_package" if index % 2 == 0 else "workspace",
                "importanceSignals": ["test_fixture"],
                "provenance": {
                    "status": "resolved",
                    "repository": f"https://github.com/example/{repository_id}",
                },
                "licenseProvenance": {"status": "resolved", "paths": ["LICENSE"]},
                "sizeBudget": {"observedBytes": 1024, "maximumBytes": 2048},
                "selectionRationale": "test_fixture",
                "stopPolicy": {
                    "excludeOnRevisionMismatch": True,
                    "excludeOnDirtyCheckout": True,
                    "excludeOnUnresolvedProvenance": True,
                    "excludeOnSizeBudgetExceeded": True,
                },
            }
        )
    inputs.mkdir(exist_ok=True)
    (inputs / "repositories.yml").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    metadata = inputs / "selection-metadata.json"
    metadata.write_text(json.dumps({"repositories": metadata_records}), encoding="utf-8")
    return inputs, revisions, metadata
