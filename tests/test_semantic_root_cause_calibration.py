from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import spec_harvester.semantic_root_cause_calibration as calibration
from spec_harvester.retained_corpus_semantic_campaign import CampaignTarget, digest
from spec_harvester.semantic_root_cause_calibration import (
    TARGET_IDS,
    _report,
    _root_cause,
    _validate_purpose_assessment,
    validate_calibration_plan,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "SPECS/EVIDENCE/P55-T10G"


def test_build_plan_binds_current_scope_and_immutable_baseline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    targets = [
        CampaignTarget(
            repository_id=repository_id,
            revision=f"{index + 1:040x}",
            wave="wave-1",
            packet_sha256=f"{index + 1:064x}",
            candidate_id=f"candidate.{index}",
            candidate_dir=tmp_path / "candidate",
            source_dir=tmp_path / "source",
        )
        for index, repository_id in enumerate(TARGET_IDS)
    ]
    base_scope = {
        "sourceManifestSha256": "1" * 64,
        "handoffAggregateSha256": "2" * 64,
        "p55T9AReadinessSha256": "3" * 64,
        "specpmObservedIntentSnapshotSha256": "4" * 64,
    }
    archived_scope = {"taskId": "P55-T10C"}
    archived_scope["campaignInputSha256"] = digest(archived_scope)
    members = {"campaign-input.json": json.dumps(archived_scope).encode()}
    for index, target in enumerate(targets):
        record = {
            "campaignInputSha256": archived_scope["campaignInputSha256"],
            **target.binding(),
            "status": "completed",
            "proposalReuseIntentIds": ["intent.package.javascript_library"],
            "semanticPass": {"providerReceipt": {"jsonRepairNeeded": index == 0}},
        }
        record["recordSha256"] = digest(record)
        members[f"records/{target.repository_id}/campaign-record.json"] = json.dumps(
            record
        ).encode()
    report = {"archive": {"sha256": "5" * 64}}
    report["reportSha256"] = digest(report)

    monkeypatch.setattr(calibration, "load_campaign_scope", lambda **_kwargs: (base_scope, targets))
    monkeypatch.setattr(calibration, "_read_json", lambda _path: report)
    monkeypatch.setattr(calibration, "sha256_file", lambda _path: "5" * 64)
    monkeypatch.setattr(calibration, "_read_archive", lambda _options: ({}, members))
    monkeypatch.setattr(
        calibration,
        "load_semantic_author_quality_policy",
        lambda: {"policySha256": "6" * 64},
    )

    plan, returned_scope, selected, baseline = calibration.build_calibration_plan(
        source_manifest_dir=tmp_path,
        source_root=tmp_path,
        handoff_root=tmp_path,
        readiness_evidence=tmp_path / "readiness.json",
        baseline_report_path=tmp_path / "report.json",
        baseline_archive_path=tmp_path / "records.tar.gz",
    )

    assert returned_scope == base_scope
    assert selected == targets
    assert set(baseline) == set(TARGET_IDS)
    assert plan["targets"][0]["baselineJsonRepairNeeded"] is True
    assert plan["targets"][0]["baselineGenericIntentIds"] == ["intent.package.javascript_library"]
    validate_calibration_plan(plan)


def test_load_scope_and_finalize_use_frozen_plan_and_terminal_records(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    plan = json.loads((EVIDENCE / "P55-T10G_Frozen_Plan.json").read_text())
    targets = [
        CampaignTarget(
            repository_id=repository_id,
            revision="a" * 40,
            wave="wave-1",
            packet_sha256="b" * 64,
            candidate_id=f"candidate.{index}",
            candidate_dir=tmp_path,
            source_dir=tmp_path,
        )
        for index, repository_id in enumerate(TARGET_IDS)
    ]
    base_scope = {
        "provider": {"id": "gpt-5.3-codex-spark", "kind": "codex_exec"},
        "sourceManifestSha256": "1" * 64,
        "handoffAggregateSha256": "2" * 64,
        "p55T9AReadinessSha256": "3" * 64,
        "specpmObservedIntentSnapshotSha256": "4" * 64,
    }
    baseline = {repository_id: {} for repository_id in TARGET_IDS}
    monkeypatch.setattr(calibration, "_read_json", lambda _path: plan)
    monkeypatch.setattr(
        calibration,
        "build_calibration_plan",
        lambda **_kwargs: (plan, base_scope, targets, baseline),
    )

    scope, selected, returned_baseline, returned_plan = calibration.load_calibration_scope(
        plan_path=tmp_path / "plan.json"
    )

    assert selected == targets
    assert returned_baseline == baseline
    assert returned_plan == plan
    assert scope["repositoryCount"] == 10
    assert scope["taskId"] == "P55-T10G"
    records_by_path = {}
    for target in targets:
        path = tmp_path / "work" / "records" / target.repository_id / "campaign-record.json"
        path.parent.mkdir(parents=True)
        path.write_text("{}")
        records_by_path[path] = {"repositoryId": target.repository_id}
    assessment_path = tmp_path / "assessment.json"
    assessment_path.write_text("{}")
    monkeypatch.setattr(calibration, "_read_json", lambda path: records_by_path.get(path, {}))
    monkeypatch.setattr(calibration, "validate_campaign_record", lambda *_args: None)
    monkeypatch.setattr(calibration, "write_deterministic_archive", lambda *_args: "c" * 64)
    monkeypatch.setattr(calibration, "_validate_purpose_assessment", lambda *_args: None)
    monkeypatch.setattr(
        calibration,
        "_report",
        lambda *_args: {"summary": {"passed": False}},
    )
    written = {}
    monkeypatch.setattr(
        calibration, "_write_json", lambda path, value: written.update({path: value})
    )

    report = calibration.finalize_calibration(
        scope=scope,
        targets=targets,
        baseline_records=baseline,
        plan=plan,
        work_root=tmp_path / "work",
        output_path=tmp_path / "report.json",
        archive_path=tmp_path / "archive.tar.gz",
        purpose_assessment_path=assessment_path,
    )

    assert report["archive"]["recordCount"] == 10
    assert len(report["reportSha256"]) == 64
    assert written[tmp_path / "report.json"] == report


def test_frozen_plan_is_valid_and_has_exact_ordered_scope() -> None:
    plan = json.loads((EVIDENCE / "P55-T10G_Frozen_Plan.json").read_text())

    validate_calibration_plan(plan)

    assert [item["repositoryId"] for item in plan["targets"]] == list(TARGET_IDS)
    assert plan["provider"]["modelId"] == "gpt-5.3-codex-spark"
    assert plan["successCriteria"]["purposeAccuracyRate"]["threshold"] == 0.85


def test_frozen_plan_rejects_rehashed_target_substitution() -> None:
    plan = json.loads((EVIDENCE / "P55-T10G_Frozen_Plan.json").read_text())
    plan["targets"][0]["repositoryId"] = "substituted-repository"

    with pytest.raises(ValueError, match="calibration plan is invalid"):
        validate_calibration_plan(plan)


def test_purpose_assessment_binds_every_terminal_record() -> None:
    assessment = json.loads((EVIDENCE / "P55-T10G_Purpose_Assessment.json").read_text())
    records = [
        {
            "repositoryId": item["repositoryId"],
            "recordSha256": item["recordSha256"],
        }
        for item in assessment["assessments"]
    ]

    _validate_purpose_assessment(assessment, records)

    stale = copy.deepcopy(assessment)
    stale["assessments"][0]["recordSha256"] = "0" * 64
    with pytest.raises(ValueError, match="purpose assessment is invalid"):
        _validate_purpose_assessment(stale, records)


@pytest.mark.parametrize(
    ("failure_code", "expected"),
    [
        (
            "provider JSON repair exhausted: specific semantic purpose cannot use only a "
            "generic observed intent",
            "generic_only_contradiction",
        ),
        (
            "provider JSON repair exhausted: experimental intent identifier leaks candidate "
            "namespace",
            "experimental_intent_namespace",
        ),
    ],
)
def test_failed_records_have_actionable_root_causes(failure_code: str, expected: str) -> None:
    record = {
        "status": "failed",
        "attempts": [{"status": "failed", "failureCode": failure_code}],
    }

    assert _root_cause(record) == expected


def test_report_accounts_for_failures_and_supervisor_purpose_assessment() -> None:
    baseline_records = {}
    records = []
    assessments = []
    for index, repository_id in enumerate(TARGET_IDS):
        baseline_records[repository_id] = {
            "repositoryId": repository_id,
            "status": "completed",
            "recordSha256": f"{index + 1:064x}",
            "proposalReuseIntentIds": ["intent.package.javascript_library"],
            "semanticPass": {"providerReceipt": {"jsonRepairNeeded": index == 0}},
        }
        assessments.append({"repositoryId": repository_id, "purposeAccurate": index < 6})
        if index >= 8:
            records.append(
                {
                    "repositoryId": repository_id,
                    "status": "failed",
                    "recordSha256": f"{index + 20:064x}",
                    "attempts": [
                        {
                            "status": "failed",
                            "failureCode": "specific semantic purpose cannot use only a "
                            "generic observed intent",
                        }
                    ],
                }
            )
            continue
        records.append(
            {
                "repositoryId": repository_id,
                "status": "completed",
                "recordSha256": f"{index + 20:064x}",
                "attempts": [{"status": "completed"}],
                "proposalReuseIntentIds": [],
                "experimentalIntentIds": [f"intent.experimental.purpose_{index}.deadbeef"],
                "semanticPass": {"providerReceipt": {"jsonRepairNeeded": index == 0}},
                "qualityReport": {
                    "status": "eligible_for_calibration",
                    "metrics": {
                        "purposeClaimCount": 1,
                        "evidenceSupportRate": 1.0,
                        "schemaValid": True,
                    },
                    "diagnostics": [],
                },
            }
        )
    plan = json.loads((EVIDENCE / "P55-T10G_Frozen_Plan.json").read_text())

    report = _report(
        {"campaignInputSha256": "a" * 64},
        plan,
        records,
        baseline_records,
        {"assessmentSha256": "b" * 64, "assessments": assessments},
    )

    assert report["summary"]["completedCount"] == 8
    assert report["summary"]["genericIntentReductionCount"] == 10
    assert report["summary"]["metrics"] == {
        "purposeAccuracyRate": 0.6,
        "evidenceSupportedClaimRate": 0.8,
        "schemaValidProposalRate": 0.8,
        "reviewerEditBurdenRate": 0.4,
    }
    assert report["summary"]["passed"] is False
    assert report["summary"]["p55T10HUnblocked"] is False
    assert report["comparisons"][-1]["rootCause"] == "generic_only_contradiction"
