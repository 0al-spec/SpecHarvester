"""Frozen preparation checkpoint, not a validator for future human decisions."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SPECS/EVIDENCE"


def _read(path):
    return json.loads(path.read_text())


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_checkpoint_binds_all_original_comparison_inputs():
    review = _read(EVIDENCE / "P56-T6/human-review.json")
    report = _read(EVIDENCE / "P56-T4/generation-report.json")
    lock = _read(EVIDENCE / "P56-T4/baseline-lock.json")
    comparison = _read(EVIDENCE / "P56-T5/comparison.json")
    assert review["protocol"] == report["protocol"] == comparison["protocol"]
    assert review["sourceBindings"] == {
        "generationReportSha256": _sha(EVIDENCE / "P56-T4/generation-report.json"),
        "baselineLockSha256": _sha(EVIDENCE / "P56-T4/baseline-lock.json"),
        "comparisonSha256": _sha(EVIDENCE / "P56-T5/comparison.json"),
    }
    assert len(review["repositories"]) == 5
    originals = {row["repositoryId"]: row for row in report["repositories"]}
    assert {row["repositoryId"] for row in review["repositories"]} == set(originals)
    for row in review["repositories"]:
        key = row["repositoryId"]
        assert row["candidateSha256"] == originals[key]["candidateSha256"]
        assert row["sourceRevision"] == originals[key]["revision"]
        assert row["retainedSetSha256"] == lock["repositories"][key]["candidateSetSha256"]
        assert row["semanticRecordSha256"] == lock["repositories"][key]["semanticRecordSha256"]


def test_preparation_does_not_fabricate_human_findings():
    review = _read(EVIDENCE / "P56-T6/human-review.json")
    assert review["humanReview"] == "pending"
    assert review["authority"] == "maintainer_review_pending"
    assert review["reviewer"] is None
    for row in review["repositories"]:
        for field in ("humanDisposition", "reviewMinutes", "editMinutes"):
            assert row[field] is None
        for field in ("usefulInformation", "materialMistakes", "missingGuidance", "proposedEdits"):
            assert row[field] == []
        assert set(row["surfaces"]) == {
            "new_candidate",
            "pinned_readme",
            "retained_packages",
            "semantic_proposal",
        }
        for surface in row["surfaces"].values():
            assert surface["status"] == "not_reviewed"
            assert surface["sourceLookups"] == []
            assert len(surface["answers"]) == 5
            assert len({answer["question"] for answer in surface["answers"]}) == 5
            for answer in surface["answers"]:
                assert answer["answer"] is None
                assert answer["verdict"] is None
                assert answer["reason"] is None


def test_assistance_is_labeled_bounded_and_portable():
    candidate = (EVIDENCE / "P56-T6/candidate-assistance.md").read_text()
    reference = (EVIDENCE / "P56-T6/reference-assistance.md").read_text()
    assert "AI assistance, maintainer confirmation pending" in candidate
    assert "corrected four initial quick-start omissions" in candidate
    assert "AI assistance only" in reference
    assert "not exhaustively reviewed" in reference
    assert "not retained YAML, acceptance, or verified behavior" in reference
    for path in (EVIDENCE / "P56-T6").iterdir():
        assert "/Users/" not in path.read_text()
