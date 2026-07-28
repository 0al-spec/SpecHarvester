from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from spec_harvester.p53_campaign_quality_triage import (
    P53CampaignQualityTriageOptions,
    build_p53_campaign_quality_triage,
    classify_outcome,
    effective_outcome,
)


def write_json(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def corrective_evidence(tmp_path: Path, repository_id: str, *, duration_ms: int = 500) -> Path:
    artifact_names = {
        "followUpReport": "corrective-outcome.json",
        "correctedProposal": "corrected-proposal.json",
        "targetedStaticReport": "targeted-static-report.json",
    }
    artifacts = {}
    for name, filename in artifact_names.items():
        artifact_path = write_json(tmp_path / filename, {"artifact": name})
        artifacts[name] = {
            "path": filename,
            "sha256": sha256(artifact_path.read_bytes()).hexdigest(),
        }
    proposal_digest = artifacts["correctedProposal"]["sha256"]
    return write_json(
        tmp_path / "correction.json",
        {
            "apiVersion": "spec-harvester.p53-targeted-correction/v0",
            "kind": "SpecHarvesterP53TargetedCorrection",
            "schemaVersion": 1,
            "phase": "P53",
            "task": "P53-T13",
            "status": "passed",
            "authority": "producer_targeted_correction_evidence_only",
            "correctionDisposition": {
                "repositoryId": repository_id,
                "originalOutcome": "unsupported_relation_claim",
                "replacementEvidence": "revision_verified_targeted_rerun",
                "effectiveOutcome": "schema_valid_repository_specific_zero_unsupported_claims",
                "artifacts": artifacts,
            },
            "effectiveRecord": {
                "id": repository_id,
                "status": "completed",
                "schemaValid": True,
                "repositorySpecific": True,
                "unsupportedClaimCount": 0,
                "diagnosticCodes": [],
                "proposal": {
                    "status": "completed",
                    "path": f"codex-spark/{repository_id}/proposal.json",
                    "digest": {"algorithm": "sha256", "value": proposal_digest},
                },
                "receipt": {
                    "durationMs": duration_ms,
                    "rawPromptPersisted": False,
                    "rawResponsePersisted": False,
                    "chainOfThoughtPersisted": False,
                },
            },
        },
    )


def campaign_inputs(tmp_path: Path) -> P53CampaignQualityTriageOptions:
    repositories = [
        {
            "id": f"repo-{position:03d}",
            "position": position,
            "wave": f"wave-{((position - 1) // 25) + 1}",
        }
        for position in range(1, 101)
    ]
    metadata = write_json(
        tmp_path / "metadata.json",
        {
            "apiVersion": "spec-harvester.mass-corpus-selection-metadata/v0",
            "kind": "SpecHarvesterMassCorpusSelectionMetadata",
            "phase": "P53",
            "task": "P53-T3",
            "repositories": repositories,
        },
    )
    plan = write_json(
        tmp_path / "plan.json",
        {
            "apiVersion": "spec-harvester.mass-repository-campaign-plan/v0",
            "kind": "SpecHarvesterMassRepositoryCampaignPlan",
            "phase": "P53",
            "task": "P53-T1",
            "authority": "producer_planning_evidence_only",
            "worker": {
                "model": "gpt-5.3-codex-spark",
                "invocationSurface": "codex_exec",
                "proposalOnly": True,
            },
            "qualityMetrics": {
                "staticCompletionRateMinimum": 0.98,
                "codexCompletionRateMinimum": 0.95,
                "schemaValidRateMinimum": 0.99,
                "repositorySpecificRateMinimum": 0.9,
                "unsupportedClaimRateMaximum": 0.02,
            },
            "budgetPolicy": {
                "campaignMaxTokens": 2_000_000,
                "perRepositoryMaxTokens": 20_000,
            },
        },
    )
    wave_reports = []
    tasks = ("P53-T6", "P53-T8", "P53-T10", "P53-T12")
    for wave_number, task in enumerate(tasks, start=1):
        selected = repositories[(wave_number - 1) * 25 : wave_number * 25]
        records = []
        for item in selected:
            records.append(
                {
                    "id": item["id"],
                    "status": "completed",
                    "schemaValid": True,
                    "repositorySpecific": True,
                    "unsupportedClaimCount": 0,
                    "diagnosticCodes": [],
                    "proposal": {
                        "status": "completed",
                        "path": f"codex-spark/{item['id']}/proposal.json",
                        "digest": {"algorithm": "sha256", "value": "a" * 64},
                    },
                    "receipt": {
                        "durationMs": 1000,
                        "schemaValid": True,
                        "rawPromptPersisted": False,
                        "rawResponsePersisted": False,
                        "chainOfThoughtPersisted": False,
                    },
                }
            )
        wave_reports.append(
            write_json(
                tmp_path / f"wave-{wave_number}.json",
                {
                    "apiVersion": "spec-harvester.p53-codex-spark-wave/v0",
                    "kind": "SpecHarvesterP53CodexSparkWaveReport",
                    "phase": "P53",
                    "task": task,
                    "status": "passed",
                    "wave": f"wave-{wave_number}",
                    "sourceIds": [item["id"] for item in selected],
                    "static": {"status": "passed"},
                    "codexSpark": {
                        "model": "gpt-5.3-codex-spark",
                        "authority": "proposal_only_not_registry_acceptance",
                        "repositories": records,
                    },
                    "checkpointSummary": {
                        "completed": 25,
                        "terminalFailed": 0,
                        "stop": None,
                    },
                    "privacy": {
                        "rawPromptsPersisted": False,
                        "rawModelResponsesPersisted": False,
                        "chainOfThoughtPersisted": False,
                        "secretsIncluded": False,
                    },
                    "authority": "producer_wave_evidence_only",
                },
            )
        )
    return P53CampaignQualityTriageOptions(
        metadata=metadata,
        campaign_plan=plan,
        wave_reports=tuple(wave_reports),
        corrections=(),
        output=tmp_path / "triage.json",
    )


def test_campaign_triage_accounts_for_all_repositories_once(tmp_path: Path) -> None:
    options = campaign_inputs(tmp_path)

    result = build_p53_campaign_quality_triage(options)

    assert result["status"] == "passed"
    assert result["summary"]["repositoryCount"] == 100
    assert result["summary"]["dispositionCounts"] == {
        "selectedForAuthorReview": 100,
        "deferred": 0,
        "doNotPromote": 0,
    }
    assert result["quality"]["metrics"] == {
        "staticCompletionRate": 1.0,
        "codexCompletionRate": 1.0,
        "schemaValidRate": 1.0,
        "repositorySpecificRate": 1.0,
        "unsupportedClaimRate": 0.0,
    }
    assert result["usage"]["aggregateDurationMs"] == 100_000
    assert result["usage"]["actualTokenUsage"]["status"] == "not_reported_by_worker_receipts"
    assert len(result["repositories"]) == 100
    assert options.output.read_text(encoding="utf-8").endswith("\n")


def test_campaign_triage_rejects_wave_source_drift(tmp_path: Path) -> None:
    options = campaign_inputs(tmp_path)
    report = json.loads(options.wave_reports[0].read_text(encoding="utf-8"))
    report["sourceIds"][-1] = "substituted-repository"
    write_json(options.wave_reports[0], report)

    with pytest.raises(ValueError, match="does not match frozen source positions"):
        build_p53_campaign_quality_triage(options)


def test_campaign_triage_applies_explicit_corrective_evidence(tmp_path: Path) -> None:
    options = campaign_inputs(tmp_path)
    report = json.loads(options.wave_reports[1].read_text(encoding="utf-8"))
    record = report["codexSpark"]["repositories"][0]
    record["repositorySpecific"] = False
    record["unsupportedClaimCount"] = 1
    corrected_id = record["id"]
    report["status"] = "failed"
    report["checkpointSummary"]["completed"] = 24
    report["checkpointSummary"]["terminalFailed"] = 1
    write_json(options.wave_reports[1], report)
    correction = corrective_evidence(tmp_path, corrected_id)
    options = P53CampaignQualityTriageOptions(
        metadata=options.metadata,
        campaign_plan=options.campaign_plan,
        wave_reports=options.wave_reports,
        corrections=(correction,),
        output=options.output,
    )

    result = build_p53_campaign_quality_triage(options)
    corrected = next(item for item in result["repositories"] if item["id"] == corrected_id)

    assert corrected["disposition"] == "selected_for_author_review"
    assert corrected["correction"]["task"] == "P53-T13"
    assert corrected["originalOutcome"]["unsupportedClaimCount"] == 1
    assert result["summary"]["correctedRepositoryCount"] == 1
    assert result["usage"]["aggregateDurationMs"] == 100_500


@pytest.mark.parametrize(
    ("outcome", "expected"),
    [
        (
            {"status": "failed", "failure": "codex_timeout"},
            ("deferred", ["codex_timeout"]),
        ),
        (
            {"status": "failed", "failure": "source_policy_drift"},
            ("do_not_promote", ["source_policy_drift"]),
        ),
        (
            {"status": "completed", "schemaValid": False},
            ("do_not_promote", ["schema_invalid"]),
        ),
        (
            {
                "status": "completed",
                "schemaValid": True,
                "unsupportedClaimCount": 1,
            },
            ("do_not_promote", ["unsupported_claim"]),
        ),
        (
            {
                "status": "completed",
                "schemaValid": True,
                "unsupportedClaimCount": 0,
                "repositorySpecific": False,
            },
            ("deferred", ["repository_specificity_not_established"]),
        ),
        (
            {
                "status": "completed",
                "schemaValid": True,
                "unsupportedClaimCount": 0,
                "repositorySpecific": True,
                "proposal": {"status": "failed"},
            },
            ("deferred", ["proposal_artifact_incomplete"]),
        ),
        (
            {
                "status": "completed",
                "schemaValid": True,
                "unsupportedClaimCount": 0,
                "repositorySpecific": True,
                "proposal": {
                    "status": "completed",
                    "path": "proposal.json",
                    "digest": {"algorithm": "sha256", "value": "invalid"},
                },
            },
            ("deferred", ["proposal_artifact_invalid"]),
        ),
    ],
)
def test_classify_outcome_preserves_failure_dispositions(
    outcome: dict[str, object], expected: tuple[str, list[str]]
) -> None:
    assert classify_outcome(outcome) == expected


def test_campaign_triage_rejects_invalid_correction_digest(tmp_path: Path) -> None:
    options = campaign_inputs(tmp_path)
    correction = corrective_evidence(tmp_path, "repo-001")
    payload = json.loads(correction.read_text(encoding="utf-8"))
    payload["correctionDisposition"]["artifacts"]["followUpReport"]["sha256"] = "0" * 64
    write_json(correction, payload)
    options = P53CampaignQualityTriageOptions(
        metadata=options.metadata,
        campaign_plan=options.campaign_plan,
        wave_reports=options.wave_reports,
        corrections=(correction,),
        output=options.output,
    )

    with pytest.raises(ValueError, match="correction artifact digest mismatch"):
        build_p53_campaign_quality_triage(options)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("apiVersion", "unrelated/v0"),
        ("kind", "UnrelatedEvidence"),
        ("task", "P53-T9"),
        ("authority", "registry_authority"),
    ],
)
def test_campaign_triage_rejects_invalid_correction_authority(
    tmp_path: Path, field: str, value: str
) -> None:
    options = campaign_inputs(tmp_path)
    correction = corrective_evidence(tmp_path, "repo-001")
    payload = json.loads(correction.read_text(encoding="utf-8"))
    payload[field] = value
    write_json(correction, payload)
    options = P53CampaignQualityTriageOptions(
        metadata=options.metadata,
        campaign_plan=options.campaign_plan,
        wave_reports=options.wave_reports,
        corrections=(correction,),
        output=options.output,
    )

    with pytest.raises(ValueError, match="correction evidence is invalid"):
        build_p53_campaign_quality_triage(options)


def test_campaign_triage_rejects_correction_without_effective_record(tmp_path: Path) -> None:
    options = campaign_inputs(tmp_path)
    correction = corrective_evidence(tmp_path, "repo-001")
    payload = json.loads(correction.read_text(encoding="utf-8"))
    payload.pop("effectiveRecord")
    write_json(correction, payload)
    options = P53CampaignQualityTriageOptions(
        metadata=options.metadata,
        campaign_plan=options.campaign_plan,
        wave_reports=options.wave_reports,
        corrections=(correction,),
        output=options.output,
    )

    with pytest.raises(ValueError, match="correction evidence is invalid"):
        build_p53_campaign_quality_triage(options)


def test_effective_outcome_rejects_unbound_replacement_digest() -> None:
    original = {"id": "repo-001"}
    correction = {
        "disposition": {
            "artifacts": {"correctedProposal": {"sha256": "a" * 64}},
        },
        "effectiveRecord": {
            "id": "repo-001",
            "status": "completed",
            "schemaValid": True,
            "repositorySpecific": True,
            "unsupportedClaimCount": 0,
            "proposal": {
                "digest": {"algorithm": "sha256", "value": "b" * 64},
            },
            "receipt": {
                "rawPromptPersisted": False,
                "rawResponsePersisted": False,
                "chainOfThoughtPersisted": False,
            },
        },
    }

    with pytest.raises(ValueError, match="effective record is invalid"):
        effective_outcome(original, correction)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("authority", "not authorized wave evidence"),
        ("status", "no terminal status"),
        ("static", "static evidence did not pass"),
        ("model", "violates the Codex Spark authority boundary"),
        ("record_count", "must contain exactly 25 outcomes"),
        ("record_identity", "outcomes do not match frozen source identities"),
        ("privacy", "violates the privacy boundary"),
        ("receipt_privacy", "outcome receipt violates the privacy boundary"),
    ],
)
def test_campaign_triage_rejects_invalid_wave_boundaries(
    tmp_path: Path, mutation: str, message: str
) -> None:
    options = campaign_inputs(tmp_path)
    report = json.loads(options.wave_reports[0].read_text(encoding="utf-8"))
    if mutation == "authority":
        report["authority"] = "registry_authority"
    elif mutation == "status":
        report["status"] = "running"
    elif mutation == "static":
        report["static"]["status"] = "failed"
    elif mutation == "model":
        report["codexSpark"]["model"] = "alternate-model"
    elif mutation == "record_count":
        report["codexSpark"]["repositories"].pop()
    elif mutation == "record_identity":
        report["codexSpark"]["repositories"][0]["id"] = "unknown-repository"
    elif mutation == "receipt_privacy":
        report["codexSpark"]["repositories"][0]["receipt"]["rawPromptPersisted"] = True
    else:
        report["privacy"]["rawPromptsPersisted"] = True
    write_json(options.wave_reports[0], report)

    with pytest.raises(ValueError, match=message):
        build_p53_campaign_quality_triage(options)


@pytest.mark.parametrize("mutation", ["count", "positions", "identity"])
def test_campaign_triage_rejects_invalid_frozen_metadata(tmp_path: Path, mutation: str) -> None:
    options = campaign_inputs(tmp_path)
    metadata = json.loads(options.metadata.read_text(encoding="utf-8"))
    if mutation == "count":
        metadata["repositories"].pop()
        message = "exactly 100"
    elif mutation == "positions":
        metadata["repositories"][0]["position"] = 101
        message = "positions 1 through 100"
    else:
        metadata["repositories"][0]["id"] = None
        message = "invalid source identity"
    write_json(options.metadata, metadata)

    with pytest.raises(ValueError, match=message):
        build_p53_campaign_quality_triage(options)
