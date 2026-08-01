from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import spec_harvester.retained_generic_intent_follow_up as follow_up
from spec_harvester.retained_corpus_semantic_campaign import CampaignTarget, digest
from spec_harvester.retained_generic_intent_follow_up import (
    EXPECTED_GENERIC_REFERENCE_COUNT,
    EXPECTED_TARGET_COUNT,
    _is_codex_quota_failure,
    build_follow_up_plan,
    build_representative_review_sample,
    compare_follow_up,
    finalize_follow_up,
    finalize_quota_recovery,
    load_quota_recovery_scope,
    validate_follow_up_plan,
)


def test_quota_recovery_selector_accepts_only_codex_nonzero_attempts() -> None:
    quota_failure = {
        "status": "failed",
        "attempts": [
            {"status": "failed", "failureCode": "codex_nonzero_exit"},
            {"status": "failed", "failureCode": "codex_nonzero_exit"},
        ],
    }
    semantic_failure = {
        "status": "failed",
        "attempts": [
            {
                "status": "failed",
                "failureCode": "provider JSON repair exhausted: policy violation",
            }
        ],
    }

    assert _is_codex_quota_failure(quota_failure) is True
    assert _is_codex_quota_failure(semantic_failure) is False


@pytest.mark.parametrize("payload", ("not-json", "[]"))
def test_follow_up_json_reader_rejects_malformed_records(tmp_path: Path, payload: str) -> None:
    path = tmp_path / "record.json"
    path.write_text(payload)

    with pytest.raises(ValueError, match="P55-T10C JSON"):
        follow_up._read_json(path)


def test_quota_recovery_scope_is_limited_to_verified_spark_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    targets = [
        CampaignTarget(
            repository_id=repository_id,
            revision="a" * 40,
            wave="wave-1",
            packet_sha256=f"{index + 1:064x}",
            candidate_id=repository_id,
            candidate_dir=tmp_path,
            source_dir=tmp_path,
        )
        for index, repository_id in enumerate(follow_up.EXPECTED_LUNA_RECOVERY_IDS)
    ]
    initial_scope = {
        "campaignInputSha256": "b" * 64,
        "attemptBudget": {"providerMaxAttempts": 2},
    }
    baseline_records = {
        target.repository_id: {"proposalReuseIntentIds": [GENERIC]} for target in targets
    }
    initial_records = {
        target.repository_id: {
            **target.binding(),
            "repositoryId": target.repository_id,
            "candidateId": target.candidate_id,
            "status": "failed",
            "attempts": [{"status": "failed", "failureCode": "codex_nonzero_exit"}],
            "recordSha256": f"{index + 10:064x}",
        }
        for index, target in enumerate(targets)
    }
    archive_path = tmp_path / "initial.tar.gz"
    archive_path.write_bytes(b"initial archive")
    report = {
        "campaignInputSha256": initial_scope["campaignInputSha256"],
        "archive": {
            "recordCount": follow_up.EXPECTED_TARGET_COUNT,
            "sha256": follow_up.sha256_file(archive_path),
        },
    }
    report["reportSha256"] = digest(report)
    report_path = tmp_path / "initial.json"
    report_path.write_text(json.dumps(report))
    members = {"campaign-input.json": json.dumps(initial_scope).encode()}
    members.update(
        {
            f"records/{repository_id}/campaign-record.json": json.dumps(record).encode()
            for repository_id, record in initial_records.items()
        }
    )

    monkeypatch.setattr(
        follow_up,
        "load_follow_up_scope",
        lambda **_kwargs: (initial_scope, targets, baseline_records),
    )
    monkeypatch.setattr(follow_up, "_read_archive", lambda _options: ("ignored", members))
    monkeypatch.setattr(follow_up, "validate_campaign_record", lambda *_args: None)

    scope, selected, loaded_baseline, loaded_initial = load_quota_recovery_scope(
        initial_report_path=report_path,
        initial_archive_path=archive_path,
        plan_path=tmp_path / "plan.json",
        source_manifest_dir=tmp_path,
        source_root=tmp_path,
        handoff_root=tmp_path,
        readiness_evidence=tmp_path / "readiness.json",
        baseline_report_path=tmp_path / "baseline.json",
        baseline_archive_path=tmp_path / "baseline.tar.gz",
    )

    assert [target.repository_id for target in selected] == list(
        follow_up.EXPECTED_LUNA_RECOVERY_IDS
    )
    assert scope["provider"] == {
        "id": follow_up.CODEX_LUNA_MODEL,
        "kind": "codex_exec",
        "reasoningEffort": "low",
    }
    assert scope["targetCount"] == 3
    assert loaded_baseline == baseline_records
    assert loaded_initial == initial_records


def test_finalize_quota_recovery_combines_initial_and_recovered_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    targets = [
        CampaignTarget(
            repository_id=repository_id,
            revision="a" * 40,
            wave="wave-1",
            packet_sha256=f"{index + 1:064x}",
            candidate_id=repository_id,
            candidate_dir=tmp_path,
            source_dir=tmp_path,
        )
        for index, repository_id in enumerate(follow_up.EXPECTED_LUNA_RECOVERY_IDS)
    ]
    recovered = [
        _record(targets[0].repository_id, experimental=["intent.experimental.web.11111111"]),
        _record(targets[1].repository_id, quality_status="rejected"),
        _record(targets[2].repository_id, failed=True),
    ]
    for index, record in enumerate(recovered):
        record.setdefault("recordSha256", f"{index + 20:064x}")
    work_root = tmp_path / "work"
    for record in recovered:
        path = work_root / "records" / record["repositoryId"] / "campaign-record.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record))
    baseline_records = {
        target.repository_id: {"proposalReuseIntentIds": [GENERIC]} for target in targets
    }
    initial_records = {
        target.repository_id: _record(target.repository_id, failed=True) for target in targets
    }
    scope = {
        "campaignInputSha256": "c" * 64,
        "provider": {"id": follow_up.CODEX_LUNA_MODEL},
        "baseline": {"archiveSha256": "d" * 64},
    }
    monkeypatch.setattr(follow_up, "validate_campaign_record", lambda *_args: None)
    monkeypatch.setattr(follow_up, "write_deterministic_archive", lambda *_args: "e" * 64)

    report = finalize_quota_recovery(
        scope=scope,
        targets=targets,
        baseline_records=baseline_records,
        initial_records=initial_records,
        work_root=work_root,
        output_path=tmp_path / "report.json",
        archive_path=tmp_path / "recovery.tar.gz",
    )

    assert report["summary"]["completedCount"] == 2
    assert report["summary"]["failedCount"] == 1
    assert report["effectiveFollowUpSummary"]["completedCount"] == 2
    assert report["archive"]["sha256"] == "e" * 64
    assert report["reportSha256"] == digest(
        {key: value for key, value in report.items() if key != "reportSha256"}
    )


def test_finalize_follow_up_writes_bound_report_and_review_sample(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    targets = [
        CampaignTarget(
            repository_id=f"repo-{index:02d}",
            revision="a" * 40,
            wave="wave-1",
            packet_sha256=f"{index + 1:064x}",
            candidate_id=f"repo-{index:02d}",
            candidate_dir=tmp_path,
            source_dir=tmp_path,
        )
        for index in range(follow_up.EXPECTED_TARGET_COUNT)
    ]
    records = [_record(target.repository_id) for target in targets]
    work_root = tmp_path / "work"
    for record in records:
        path = work_root / "records" / record["repositoryId"] / "campaign-record.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record))
    baseline_records = {
        target.repository_id: {"proposalReuseIntentIds": [GENERIC]} for target in targets
    }
    scope = {
        "campaignInputSha256": "c" * 64,
        "baseline": {"archiveSha256": "d" * 64},
        "policies": {"quality": "e" * 64},
        "provider": {"id": follow_up.CODEX_SPARK_MODEL},
        "successCriteria": {
            "maximumFalseNoveltyCount": 0,
            "maximumDuplicateExperimentalIntentIdCount": 0,
            "maximumDuplicateExperimentalSemanticStemCount": 0,
            "minimumRepresentativeReviewSampleCount": 8,
        },
    }
    output_path = tmp_path / "report.json"
    review_path = tmp_path / "review.json"
    monkeypatch.setattr(follow_up, "validate_campaign_record", lambda *_args: None)
    monkeypatch.setattr(follow_up, "write_deterministic_archive", lambda *_args: "f" * 64)

    report = finalize_follow_up(
        scope=scope,
        targets=targets,
        baseline_records=baseline_records,
        work_root=work_root,
        output_path=output_path,
        archive_path=tmp_path / "follow-up.tar.gz",
        review_sample_path=review_path,
    )

    assert report["summary"]["targetCount"] == follow_up.EXPECTED_TARGET_COUNT
    assert report["review"]["sampleCount"] == 8
    assert report["decision"]["p55T11TechnicallyReady"] is True
    assert report["decision"]["p55T11Unblocked"] is False
    assert output_path.exists()
    assert review_path.exists()


ROOT = Path(__file__).resolve().parents[1]
PLAN = (
    ROOT / "tests/fixtures/retained_generic_intent_follow_up/p55-t10c-follow-up-plan.example.json"
)
GENERIC = "intent.package.javascript_library"


def _record(
    repository_id: str,
    *,
    reuse: list[str] | None = None,
    experimental: list[str] | None = None,
    quality_status: str = "review_required",
    diagnostics: list[str] | None = None,
    failed: bool = False,
    retry: bool = False,
) -> dict:
    attempts = [{"status": "failed", "durationMs": 2}] if retry else []
    if failed:
        return {
            "repositoryId": repository_id,
            "candidateId": repository_id,
            "status": "failed",
            "attempts": attempts or [{"status": "failed", "durationMs": 2}],
        }
    attempts.append({"status": "completed", "durationMs": 3})
    return {
        "repositoryId": repository_id,
        "candidateId": repository_id,
        "status": "completed",
        "attempts": attempts,
        "proposalReuseIntentIds": reuse or [],
        "experimentalIntentIds": experimental or [],
        "qualityReport": {
            "status": quality_status,
            "diagnostics": [{"code": code} for code in diagnostics or []],
            "metrics": {"schemaValid": True, "evidenceSupportRate": 1.0},
        },
        "semanticPass": {
            "providerReceipt": {
                "jsonRepairNeeded": False,
                "usage": {},
            }
        },
        "recordSha256": "a" * 64,
    }


def test_frozen_plan_binds_46_repositories_and_48_references() -> None:
    plan = json.loads(PLAN.read_text())

    validate_follow_up_plan(plan)

    assert len(plan["targets"]) == EXPECTED_TARGET_COUNT == 46
    assert plan["genericReferenceCount"] == EXPECTED_GENERIC_REFERENCE_COUNT == 48
    assert sum(len(item["baselineGenericIntentIds"]) for item in plan["targets"]) == 48
    assert plan["provider"]["modelId"] == "gpt-5.3-codex-spark"
    assert "/Users/" not in PLAN.read_text()


@pytest.mark.parametrize("field", ("planSha256", "authority", "genericReferenceCount"))
def test_frozen_plan_rejects_drift(field: str) -> None:
    plan = json.loads(PLAN.read_text())
    plan[field] = "f" * 64 if field != "genericReferenceCount" else 47

    with pytest.raises(ValueError):
        validate_follow_up_plan(plan)


def test_plan_derivation_counts_repositories_and_references(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    targets = [
        CampaignTarget(
            repository_id=f"repo-{index:03d}",
            revision="a" * 40,
            wave="wave-1",
            packet_sha256=f"{index:064x}",
            candidate_id=f"candidate-{index:03d}",
            candidate_dir=tmp_path,
            source_dir=tmp_path,
        )
        for index in range(100)
    ]
    baseline_scope = {
        "campaignInputSha256": "b" * 64,
        "provider": {"id": "gpt-5.3-codex-spark", "kind": "codex_exec"},
        "inputProjection": {},
        "targets": [target.binding() for target in targets],
    }
    records = {}
    members = {"campaign-input.json": json.dumps(baseline_scope).encode()}
    generic_ids = sorted(follow_up.GENERIC_OBSERVED_INTENT_IDS)
    for index, target in enumerate(targets):
        reuse = []
        if index < 46:
            reuse = [generic_ids[0]]
            if index < 2:
                reuse.append(generic_ids[1])
        record = {
            **target.binding(),
            "repositoryId": target.repository_id,
            "proposalReuseIntentIds": reuse,
            "recordSha256": f"{index + 100:064x}",
        }
        records[target.repository_id] = record
        members[f"records/{target.repository_id}/campaign-record.json"] = json.dumps(
            record
        ).encode()
    archive_path = tmp_path / "baseline.tar.gz"
    archive_path.write_bytes(b"archive")
    baseline_report = {
        "campaignInputSha256": baseline_scope["campaignInputSha256"],
        "archive": {
            "recordCount": 100,
            "sha256": follow_up.sha256_file(archive_path),
        },
    }
    baseline_report["reportSha256"] = digest(baseline_report)
    report_path = tmp_path / "baseline.json"
    report_path.write_text(json.dumps(baseline_report))

    monkeypatch.setattr(
        follow_up, "load_campaign_scope", lambda **_kwargs: (baseline_scope, targets)
    )
    monkeypatch.setattr(
        follow_up,
        "_read_archive",
        lambda _options: (follow_up.sha256_file(archive_path), members),
    )
    monkeypatch.setattr(follow_up, "validate_campaign_record", lambda *_args: None)

    plan, _scope, selected, derived_records = build_follow_up_plan(
        source_manifest_dir=tmp_path,
        source_root=tmp_path,
        handoff_root=tmp_path,
        readiness_evidence=tmp_path,
        baseline_report_path=report_path,
        baseline_archive_path=archive_path,
    )

    assert len(selected) == 46
    assert len(derived_records) == 100
    assert plan["genericReferenceCount"] == 48


def test_comparison_keeps_failures_and_generic_reuse_in_edit_denominator() -> None:
    completed = _record("one", experimental=["intent.experimental.context_search.11111111"])
    retained = _record("two", reuse=[GENERIC], quality_status="rejected")
    failed = _record("three", failed=True)
    baseline = {
        item["repositoryId"]: {"proposalReuseIntentIds": [GENERIC]}
        for item in (completed, retained, failed)
    }

    result = compare_follow_up(baseline, [completed, retained, failed])

    assert result["completedCount"] == 2
    assert result["failedCount"] == 1
    assert result["baselineGenericIntentReuseCount"] == 3
    assert result["followUpGenericIntentReuseCount"] == 2
    assert result["genericIntentReductionCount"] == 1
    assert result["evidenceSupportedExperimentalIntentCount"] == 1
    assert result["estimatedReviewerEditRequiredCount"] == 2


def test_comparison_detects_duplicate_ids_stems_and_false_novelty() -> None:
    first = _record(
        "one",
        experimental=["intent.experimental.context_search.11111111"],
        diagnostics=["experimental_intent_false_novelty_risk"],
    )
    second = _record("two", experimental=["intent.experimental.context_search.22222222"])
    third = _record("three", experimental=["intent.experimental.context_search.22222222"])
    baseline = {
        item["repositoryId"]: {"proposalReuseIntentIds": [GENERIC]}
        for item in (first, second, third)
    }

    result = compare_follow_up(baseline, [first, second, third])

    assert result["falseNoveltyCount"] == 1
    assert result["duplicateExperimentalIntentIdCount"] == 1
    assert result["duplicateExperimentalSemanticStemCount"] == 2


def test_representative_sample_is_deterministic_and_requires_maintainer() -> None:
    records = [
        _record("experimental", experimental=["intent.experimental.context_search.11111111"]),
        _record("generic", reuse=[GENERIC]),
        _record("rejected", quality_status="rejected"),
        _record("retry", retry=True),
        *[_record(f"fill-{index}") for index in range(8)],
    ]
    scope = {"campaignInputSha256": "b" * 64}

    first = build_representative_review_sample(scope, records)
    second = build_representative_review_sample(scope, copy.deepcopy(records))

    assert first == second
    assert len(first["items"]) == 8
    assert {item["stratum"] for item in first["items"]} >= {
        "experimental_proposal",
        "retained_generic_reuse",
        "quality_rejected",
        "recovered_provider_attempt",
    }
    assert all(
        item["reviewStatus"] == "awaiting_explicit_maintainer_review" for item in first["items"]
    )
    assert first["executionBoundary"]["reviewerDecisionCreated"] is False
