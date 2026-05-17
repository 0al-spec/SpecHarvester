from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from spec_harvester.batch_collection import BatchCollectOptions, collect_batch_snapshots
from spec_harvester.cli import main


def test_collect_batch_snapshots_writes_deterministic_candidate_paths(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    checkouts = tmp_path / "checkouts"
    out = tmp_path / "candidates"
    inputs.mkdir()
    alpha = make_checkout(checkouts / "alpha", "# Alpha\n")
    beta = make_checkout(checkouts / "beta", "# Beta\n")
    (inputs / "a.yml").write_text(
        f"""
repositories:
  - id: alpha
    repository: https://github.com/example/alpha
    revision: aaa
    checkout: {relative_to(alpha, inputs)}
""",
        encoding="utf-8",
    )
    (inputs / "z.yml").write_text(
        f"""
repositories:
  - id: beta
    repository: https://github.com/example/beta
    revision: bbb
    checkout: {relative_to(beta, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(
            inputs=inputs,
            out=out,
            selected_ids=("beta", "alpha"),
        )
    )

    assert [item["id"] for item in result["collected"]] == ["alpha", "beta"]
    assert result["skipped"] == []
    assert (out / "alpha" / "harvest.json").is_file()
    assert (out / "beta" / "harvest.json").is_file()
    alpha_snapshot = json.loads((out / "alpha" / "harvest.json").read_text(encoding="utf-8"))
    assert alpha_snapshot["source"]["repository"] == "https://github.com/example/alpha"
    assert alpha_snapshot["source"]["revision"] == "aaa"
    assert alpha_snapshot["summary"]["fileCount"] == 1


def test_collect_batch_snapshots_records_unselected_repositories(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    checkouts = tmp_path / "checkouts"
    out = tmp_path / "candidates"
    inputs.mkdir()
    alpha = make_checkout(checkouts / "alpha", "# Alpha\n")
    beta = make_checkout(checkouts / "beta", "# Beta\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: alpha
    repository: https://github.com/example/alpha
    revision: aaa
    checkout: {relative_to(alpha, inputs)}
  - id: beta
    repository: https://github.com/example/beta
    revision: bbb
    checkout: {relative_to(beta, inputs)}
""",
        encoding="utf-8",
    )

    result = collect_batch_snapshots(
        BatchCollectOptions(inputs=inputs, out=out, selected_ids=("alpha",))
    )

    assert [item["id"] for item in result["collected"]] == ["alpha"]
    assert result["skipped"] == [{"id": "beta", "reason": "not_selected"}]
    assert (out / "alpha" / "harvest.json").is_file()
    assert not (out / "beta").exists()


def test_collect_batch_snapshots_rejects_unknown_selected_ids(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unknown selected repository id"):
        collect_batch_snapshots(
            BatchCollectOptions(inputs=inputs, out=out, selected_ids=("missing",))
        )


def test_collect_batch_snapshots_rejects_duplicate_selected_ids(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate selected repository id"):
        collect_batch_snapshots(
            BatchCollectOptions(inputs=inputs, out=out, selected_ids=("demo", "demo"))
        )


def test_collect_batch_snapshots_requires_checkout_field(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="requires checkout"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))


def test_collect_batch_snapshots_rejects_missing_checkout_directory(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    (inputs / "repos.yml").write_text(
        """
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: ../missing
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="checkout does not exist"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))


def test_collect_batch_snapshots_does_not_write_partial_outputs_on_validation_failure(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: valid
    repository: https://github.com/example/valid
    revision: abc
    checkout: {relative_to(checkout, inputs)}
  - id: missing
    repository: https://github.com/example/missing
    revision: def
    checkout: ../missing
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="checkout does not exist"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))

    assert not (out / "valid").exists()


def test_collect_batch_snapshots_rejects_unsafe_candidate_directory_ids(
    tmp_path: Path,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: ../escape
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unsafe repository id"):
        collect_batch_snapshots(BatchCollectOptions(inputs=inputs, out=out))


def test_cli_collect_batch_prints_summary_and_writes_harvest_json(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(["collect-batch", str(inputs), "--out", str(out), "--select", "demo"])

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["status"] == "ok"
    assert summary["collectedCount"] == 1
    assert summary["collected"][0]["id"] == "demo"
    assert (out / "demo" / "harvest.json").is_file()


def test_cli_collect_batch_writes_validation_report(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = tmp_path / "inputs"
    out = tmp_path / "candidates"
    report_path = out / "batch-validation.json"
    inputs.mkdir()
    checkout = make_checkout(tmp_path / "checkout", "# Demo\n")
    (checkout / "package.json").write_text(
        json.dumps({"name": "@example/demo", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (inputs / "repos.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: abc
    checkout: {relative_to(checkout, inputs)}
""",
        encoding="utf-8",
    )

    result = main(
        [
            "collect-batch",
            str(inputs),
            "--out",
            str(out),
            "--report",
            str(report_path),
        ]
    )

    assert result == 0
    summary = json.loads(capsys.readouterr().out)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert summary["validationReport"] == str(report_path)
    assert report["summary"]["collectedCount"] == 1
    assert report["summary"]["highConfidenceCount"] == 1
    assert report["records"][0]["id"] == "demo"


def make_checkout(path: Path, readme: str) -> Path:
    path.mkdir(parents=True)
    (path / "README.md").write_text(readme, encoding="utf-8")
    return path


def relative_to(path: Path, root: Path) -> str:
    return Path(os.path.relpath(path, root)).as_posix()
