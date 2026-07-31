from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.retained_corpus_semantic_campaign import (
    EXPECTED_REPOSITORY_COUNT,
    CampaignRunOptions,
    campaign_summary,
    finalize_campaign,
    initialize_campaign,
    load_campaign_scope,
    run_campaign_target,
    select_principal_candidate,
    sha256_file,
    validate_campaign_record,
    write_deterministic_archive,
)
from spec_harvester.semantic_author_pass import (
    ProviderCompletion,
    SemanticAuthorPassError,
)

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_FIXTURE = ROOT / "tests/fixtures/ai_semantic_author_schemas/p55-t2-valid.example.json"


class FakeProvider:
    provider_id = "gpt-5.3-codex-spark"

    def complete(self, request: dict, _options: object) -> ProviderCompletion:
        candidate_id = request["request"]["candidateId"]
        if candidate_id.endswith("099.core"):
            raise SemanticAuthorPassError("synthetic_provider_failure")
        proposal = copy.deepcopy(json.loads(PROPOSAL_FIXTURE.read_text())["proposal"])
        proposal.pop("proposalSha256")
        proposal.pop("provider")
        proposal["candidateId"] = candidate_id
        proposal["sourceBundleSha256"] = request["request"]["sourceBundleSha256"]
        evidence = request["request"]["evidence"][0]
        for claim in proposal["claims"]:
            claim["evidence"] = [dict(evidence)]
        reuse = proposal["intentDecisions"][0]
        observed = request["observedIntents"][0]
        reuse["intentId"] = observed["intentId"]
        reuse["observedIntentSha256"] = observed["observedIntentSha256"]
        proposal["intentDecisions"] = [reuse]
        return ProviderCompletion(
            payload=proposal,
            receipt={
                "providerKind": "codex_exec",
                "providerName": self.provider_id,
                "modelId": self.provider_id,
                "durationMs": 1,
                "usage": {},
                "jsonRepairNeeded": False,
                "jsonRepairAttemptCount": 0,
                "jsonRepairStatus": "not_needed",
                "rawPromptPersisted": False,
                "rawResponsePersisted": False,
                "chainOfThoughtPersisted": False,
            },
        )


def test_selects_first_member_package_before_workspace() -> None:
    draft = {
        "candidates": [
            {"candidatePath": "workspace", "role": "workspace", "status": "ok"},
            {"candidatePath": "cli", "role": "member_package", "status": "ok"},
            {"candidatePath": "sdk", "role": "member_package", "status": "ok"},
        ]
    }

    assert select_principal_candidate(draft) == "cli"
    assert (
        select_principal_candidate(
            {"candidates": [{"candidatePath": "workspace", "role": "workspace", "status": "ok"}]}
        )
        == "workspace"
    )
    with pytest.raises(ValueError, match="no eligible"):
        select_principal_candidate(
            {"candidates": [{"candidatePath": "bad", "role": "member_package"}]}
        )


def test_runs_resumes_and_finalizes_complete_bound_campaign(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_manifest_dir, source_root, handoff_root, readiness = corpus(tmp_path)
    scope, targets = load_campaign_scope(
        source_manifest_dir=source_manifest_dir,
        source_root=source_root,
        handoff_root=handoff_root,
        readiness_evidence=readiness,
    )
    assert len(targets) == EXPECTED_REPOSITORY_COUNT
    assert scope["repositoryCount"] == EXPECTED_REPOSITORY_COUNT
    assert targets[0].candidate_id == "repo_000.core"

    work_root = tmp_path / "work"
    initialize_campaign(work_root, scope)
    initialize_campaign(work_root, scope)
    monkeypatch.setattr(
        "spec_harvester.retained_corpus_semantic_campaign.validate_source_checkout",
        lambda *_args: None,
    )
    monkeypatch.setattr(
        "spec_harvester.retained_corpus_semantic_campaign.read_pinned_readme",
        lambda *_args: b"# Pinned README\nSearch files for users.\n",
    )
    provider = FakeProvider()
    options = CampaignRunOptions(provider_max_attempts=2)
    records = [
        run_campaign_target(
            target,
            scope=scope,
            work_root=work_root,
            provider=provider,  # type: ignore[arg-type]
            options=options,
        )
        for target in targets
    ]
    assert (
        run_campaign_target(
            targets[0],
            scope=scope,
            work_root=work_root,
            provider=provider,  # type: ignore[arg-type]
            options=options,
        )
        == records[0]
    )
    assert sum(record["status"] == "completed" for record in records) == 99
    assert records[-1]["status"] == "failed"
    assert len(records[-1]["attempts"]) == 2

    output = tmp_path / "evidence" / "summary.json"
    archive = tmp_path / "evidence" / "records.tar.gz"
    report = finalize_campaign(
        scope=scope,
        targets=targets,
        work_root=work_root,
        output_path=output,
        archive_path=archive,
    )
    assert report["summary"]["repositoryCount"] == 100
    assert report["summary"]["completedCount"] == 99
    assert report["summary"]["failedCount"] == 1
    assert report["reviewerDecisions"]["unreviewedCount"] == 100
    assert report["budgets"]["providerAttemptCount"] == 101
    assert report["archive"]["sha256"] == sha256_file(archive)
    first_archive = archive.read_bytes()
    assert write_deterministic_archive(work_root, archive) == sha256_file(archive)
    assert archive.read_bytes() == first_archive

    stale = copy.deepcopy(records[0])
    stale["candidateId"] = "substituted.core"
    with pytest.raises(ValueError, match="binding is stale"):
        validate_campaign_record(stale, scope, targets[0])
    with pytest.raises(ValueError, match="exactly 100"):
        campaign_summary(scope, records[:-1])


def test_rejects_stale_resume_and_incomplete_finalization(tmp_path: Path) -> None:
    source_manifest_dir, source_root, handoff_root, readiness = corpus(tmp_path)
    scope, targets = load_campaign_scope(
        source_manifest_dir=source_manifest_dir,
        source_root=source_root,
        handoff_root=handoff_root,
        readiness_evidence=readiness,
    )
    work_root = tmp_path / "work"
    initialize_campaign(work_root, scope)
    stale = copy.deepcopy(scope)
    stale["campaignInputSha256"] = "f" * 64
    with pytest.raises(ValueError, match="input binding is stale"):
        initialize_campaign(work_root, stale)
    with pytest.raises(ValueError, match="Campaign is incomplete"):
        finalize_campaign(
            scope=scope,
            targets=targets,
            work_root=work_root,
            output_path=tmp_path / "summary.json",
            archive_path=tmp_path / "records.tar.gz",
        )


def corpus(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    source_manifest_dir = tmp_path / "inputs"
    source_root = tmp_path / "sources"
    handoff_root = tmp_path / "handoff"
    source_manifest_dir.mkdir()
    source_root.mkdir()
    (handoff_root / "packets").mkdir(parents=True)
    manifest_lines = ["repositories:"]
    selected = []
    for index in range(EXPECTED_REPOSITORY_COUNT):
        repository_id = f"repo-{index:03d}"
        candidate_id = f"repo_{index:03d}.core"
        revision = hashlib.sha1(repository_id.encode()).hexdigest()  # noqa: S324
        manifest_lines.extend(
            (
                f"  - id: {repository_id}",
                f"    repository: https://github.com/example/{repository_id}",
                f"    revision: {revision}",
                f"    checkout: ../../sources/{repository_id}",
                f"    packageId: {candidate_id}",
                "    labels: [wave_1]",
            )
        )
        selected.append({"repositoryId": repository_id})
        source = source_root / repository_id
        source.mkdir()
        (source / "README.md").write_text(f"# {repository_id}\nSearch files for users.\n")
        packet_dir = handoff_root / "packets" / repository_id
        candidate_root = packet_dir / "candidate"
        candidate = candidate_root / candidate_id
        (candidate / "specs").mkdir(parents=True)
        manifest = (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: SpecPackage\n"
            f"metadata:\n  id: {candidate_id}\n"
            "preview_only: true\n"
            "specs:\n  - path: specs/core.spec.yaml\n"
            "index:\n  provides:\n"
            f"    capabilities: [{candidate_id}]\n"
            "    intents: [intent.package.javascript_library]\n"
        )
        boundary = (
            "apiVersion: specpm.dev/v0.1\n"
            "kind: BoundarySpec\n"
            f"metadata:\n  id: {candidate_id}\n"
            "intent:\n  summary: Search files for users.\n"
            "provides:\n  capabilities:\n"
            f"    - id: {candidate_id}\n"
            "      intentIds: [intent.package.javascript_library]\n"
        )
        (candidate / "specpm.yaml").write_text(manifest)
        (candidate / "specs/core.spec.yaml").write_text(boundary)
        (candidate / "harvest.json").write_text("{}\n")
        draft = {
            "candidates": [
                {
                    "candidatePath": candidate_id,
                    "role": "member_package",
                    "status": "ok",
                }
            ]
        }
        draft_path = candidate_root / "package-set-draft.json"
        draft_path.write_text(json.dumps(draft))
        files = []
        for path in sorted(candidate_root.rglob("*")):
            if path.is_file():
                files.append(
                    {
                        "path": path.relative_to(packet_dir).as_posix(),
                        "sha256": sha256_file(path),
                    }
                )
        packet = {
            "repository": {"id": repository_id, "wave": f"wave-{index // 25 + 1}"},
            "candidate": {"files": files},
        }
        (packet_dir / "packet.json").write_text(json.dumps(packet))

    (source_manifest_dir / "repositories.yml").write_text("\n".join(manifest_lines) + "\n")
    (handoff_root / "aggregate-handoff.json").write_text(
        json.dumps({"selectedCandidates": selected})
    )
    readiness = tmp_path / "p55-t9a.json"
    readiness.write_text(
        json.dumps(
            {
                "decision": {"p55T10Unblocked": True, "thresholdsRedefined": False},
                "providers": {
                    "codex_spark": {"summary": {"passed": True}},
                    "lm_studio": {"summary": {"passed": True}},
                },
            }
        )
    )
    return source_manifest_dir, source_root, handoff_root, readiness
