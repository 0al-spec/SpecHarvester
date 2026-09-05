from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from spec_harvester.investigative_authoring_io import (
    AuthoringEvidence,
    AuthoringIOError,
    CandidateOutput,
    EvidenceLimits,
)


def evidence(tmp_path: Path, text: str = "abcdef", **limits: int) -> AuthoringEvidence:
    root = tmp_path / "source"
    root.mkdir()
    (root / "README.md").write_text(text)
    return AuthoringEvidence(
        root,
        {"README.md": hashlib.sha256(text.encode()).hexdigest()},
        EvidenceLimits(**limits),
    )


def test_overlapping_reads_charge_union_but_each_request_counts(tmp_path: Path) -> None:
    source = evidence(tmp_path)
    first = source.read("README.md", 0, 4)
    second = source.read("README.md", 2, 6)
    assert first["text"] == "abcd"
    assert second["text"] == "cdef"
    assert source.summary() == {
        "readCalls": 2,
        "sourceBytes": 6,
        "generatedBytes": 0,
        "exhausted": False,
    }
    assert [row["sequence"] for row in source.ledger()] == [1, 2]
    assert all(row["endedMonotonic"] >= row["startedMonotonic"] for row in source.ledger())


def test_utf8_ranges_are_explicit_and_never_split_a_character(tmp_path: Path) -> None:
    source = evidence(tmp_path, "a\u20ac\U0001f600z")
    result = source.read("README.md", 2, 8)
    assert result["text"] == "\U0001f600"
    assert result["requestedRange"] == [2, 8]
    assert result["returnedRange"] == [4, 8]
    assert result["truncated"] is True
    assert source.summary()["sourceBytes"] == 4


@pytest.mark.parametrize(
    "path",
    ["../secret", "/etc/passwd", "a/../README.md", "a\\b", "./README.md", "a//b", "", "a\x00b"],
)
def test_unsafe_paths_are_denied_without_leaking_them(tmp_path: Path, path: str) -> None:
    source = evidence(tmp_path)
    with pytest.raises(AuthoringIOError, match="invalid_path"):
        source.read(path, 0, 2)
    assert source.ledger()[0]["path"] is None
    assert source.summary()["readCalls"] == 1


def test_unlisted_file_and_source_drift_fail_before_return(tmp_path: Path) -> None:
    source = evidence(tmp_path)
    with pytest.raises(AuthoringIOError, match="source_not_allowlisted"):
        source.read("answers.json", 0, 1)
    (tmp_path / "source/README.md").write_text("changed")
    with pytest.raises(AuthoringIOError, match="source_digest_mismatch"):
        source.read("README.md", 0, 2)
    assert source.summary()["sourceBytes"] == 0


@pytest.mark.parametrize("kind", ["file", "parent", "root", "hardlink"])
def test_linked_inputs_are_rejected(tmp_path: Path, kind: str) -> None:
    source = evidence(tmp_path)
    root = tmp_path / "source"
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "README.md").write_text("abcdef")
    if kind == "root":
        (root / "README.md").unlink()
        root.rmdir()
        root.symlink_to(outside, target_is_directory=True)
    elif kind == "parent":
        (root / "docs").symlink_to(outside, target_is_directory=True)
        source = AuthoringEvidence(root, {"docs/README.md": hashlib.sha256(b"abcdef").hexdigest()})
    else:
        (root / "README.md").unlink()
        if kind == "file":
            (root / "README.md").symlink_to(outside / "README.md")
        else:
            import os

            os.link(outside / "README.md", root / "README.md")
    with pytest.raises(AuthoringIOError, match="unsafe_source"):
        source.read("docs/README.md" if kind == "parent" else "README.md", 0, 6)


@pytest.mark.parametrize("limit", [{"calls": 1}, {"source_file_bytes": 3}, {"evidence_bytes": 3}])
def test_caps_are_sticky_and_do_not_return_excess_bytes(tmp_path: Path, limit: dict) -> None:
    source = evidence(tmp_path, **limit)
    source.read("README.md", 0, 2)
    with pytest.raises(AuthoringIOError, match="budget_exhausted"):
        source.read("README.md", 2, 4)
    with pytest.raises(AuthoringIOError, match="budget_exhausted"):
        source.read("README.md", 0, 1)
    assert source.summary()["sourceBytes"] == 2
    assert source.summary()["exhausted"] is True


def test_generated_evidence_shares_cap_and_counts_unique_item_bytes(tmp_path: Path) -> None:
    source = evidence(tmp_path, evidence_bytes=8)
    source.read("README.md", 0, 3)
    source.generated("one", "ab")
    source.generated("one", "ab")
    source.generated("two", "ab")
    assert source.summary()["generatedBytes"] == 4
    with pytest.raises(AuthoringIOError, match="generated_item_changed"):
        source.generated("one", "different")
    with pytest.raises(AuthoringIOError, match="budget_exhausted"):
        source.generated("three", "ab")


@pytest.mark.parametrize("start,end", [(-1, 2), (3, 2), (0, 100000), (True, 2)])
def test_invalid_or_oversized_range_is_not_silently_clipped(
    tmp_path: Path, start: int, end: int
) -> None:
    source = evidence(tmp_path)
    with pytest.raises(AuthoringIOError, match="invalid_range"):
        source.read("README.md", start, end)


def test_eof_is_recorded_and_ledger_is_defensively_copied(tmp_path: Path) -> None:
    source = evidence(tmp_path)
    result = source.read("README.md", 4, 10)
    assert result["text"] == "ef"
    assert result["returnedRange"] == [4, 6]
    assert result["truncated"]
    source.ledger()[0]["returnedRange"][0] = 100
    assert source.ledger()[0]["returnedRange"] == [4, 6]


def test_candidate_output_is_bounded_new_and_portable(tmp_path: Path) -> None:
    sink = CandidateOutput(tmp_path / "candidate", max_bytes=100)
    files = {"specpm.yaml": "preview_only: true\n", "specs/root.spec.yaml": "status: draft\n"}
    receipt = sink.write(files)
    assert receipt["bytes"] == sum(len(text.encode()) for text in files.values())
    assert set(receipt["files"]) == set(files)
    assert (tmp_path / "candidate/specpm.yaml").read_text() == files["specpm.yaml"]
    with pytest.raises(AuthoringIOError, match="output_exists"):
        sink.write(files)


@pytest.mark.parametrize(
    "files", [{"../escape": "x"}, {"specpm.yaml": "x" * 11}, {"a": "x", "a/b": "y"}, {}]
)
def test_candidate_rejected_before_creating_output(tmp_path: Path, files: dict) -> None:
    with pytest.raises(AuthoringIOError):
        CandidateOutput(tmp_path / "candidate", max_bytes=10).write(files)
    assert not (tmp_path / "candidate").exists()


def test_allowlist_is_copied_and_bad_digest_rejected(tmp_path: Path) -> None:
    with pytest.raises(AuthoringIOError, match="invalid_digest"):
        AuthoringEvidence(tmp_path, {"README.md": "wrong"})
    for limits in [EvidenceLimits(calls=0), EvidenceLimits(evidence_bytes=-1)]:
        with pytest.raises(AuthoringIOError, match="invalid_limits"):
            AuthoringEvidence(tmp_path, {}, limits)
