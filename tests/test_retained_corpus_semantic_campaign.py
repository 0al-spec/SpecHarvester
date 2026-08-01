from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from spec_harvester.retained_corpus_semantic_campaign import (
    EXPECTED_REPOSITORY_COUNT,
    CampaignRunOptions,
    _read_json,
    _safe_child,
    _validate_run_options,
    campaign_summary,
    finalize_campaign,
    initialize_campaign,
    load_campaign_scope,
    prepare_workspace,
    read_pinned_manifest_metadata,
    read_pinned_package_readme,
    read_pinned_readme,
    read_pinned_repository_document,
    run_campaign_target,
    select_principal_candidate,
    sha256_file,
    validate_campaign_record,
    validate_source_checkout,
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
            if claim["kind"] == "purpose":
                claim["text"] = request["outcomePurposeAnchors"]["anchors"][0]["phrase"]
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
    assert scope["specpmObservedIntentSnapshotSha256"] == (
        "ed03e772f9e634a4bd5de1343a0bd1d847513d66996c0770fcf61d3c3907781d"
    )
    assert targets[0].candidate_id == "repo_000.core"

    work_root = tmp_path / "work"
    initialize_campaign(work_root, scope)
    initialize_campaign(work_root, scope)
    monkeypatch.setattr(
        "spec_harvester.retained_corpus_semantic_campaign.validate_source_checkout",
        lambda *_args: None,
    )
    monkeypatch.setattr(
        "spec_harvester.retained_corpus_semantic_campaign.read_pinned_repository_document",
        lambda *_args: ("README.md", b"# Pinned README\nSearch files for users.\n"),
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
    assert records[0]["routedObservedIntentIds"] == ["intent.package.javascript_library"]
    assert records[0]["intentRouting"]["selectedIntentIds"] == records[0]["routedObservedIntentIds"]

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
    assert report["semanticQuality"]["purposeClaimCoverageRate"] == 0.99
    assert report["semanticQuality"]["routedObservedIntentReferenceCount"] == 99
    assert report["semanticQuality"]["specificPurposeGenericOnlyContradictionCount"] == 0
    assert report["semanticQuality"]["reviewerEditBurden"] == {
        "status": "unavailable_without_reviewer_decision_evidence",
        "reviewedRecordCount": 0,
    }
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
    stale_routing = copy.deepcopy(records[0])
    stale_routing["intentRouting"]["specificProductTerms"] = ["substituted", "terms"]
    stale_routing["intentRouting"]["routingSha256"] = hashlib.sha256(
        json.dumps(
            {
                key: value
                for key, value in stale_routing["intentRouting"].items()
                if key != "routingSha256"
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    stale_routing["recordSha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in stale_routing.items() if key != "recordSha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    with pytest.raises(ValueError, match="intent routing is stale"):
        validate_campaign_record(stale_routing, scope, targets[0])
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


def test_rejects_invalid_budgets_paths_and_json(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="budgets are invalid"):
        _validate_run_options(CampaignRunOptions(provider_max_attempts=3))
    with pytest.raises(ValueError, match="budgets are invalid"):
        _validate_run_options(CampaignRunOptions(json_repair_max_attempts=2))
    with pytest.raises(ValueError, match="must be relative"):
        _safe_child(tmp_path, "/absolute")
    with pytest.raises(ValueError, match="escapes its root"):
        _safe_child(tmp_path, "../escape")

    malformed = tmp_path / "malformed.json"
    malformed.write_text("{")
    with pytest.raises(ValueError, match="Cannot read campaign JSON"):
        _read_json(malformed)
    array = tmp_path / "array.json"
    array.write_text("[]")
    with pytest.raises(ValueError, match="must be an object"):
        _read_json(array)


def test_reads_documentation_from_pinned_git_object(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repository, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repository, check=True)
    (repository / "docs").mkdir()
    (repository / "docs" / "readme.rst").write_text("Pinned purpose\n")
    subprocess.run(["git", "add", "."], cwd=repository, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repository, check=True)
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    validate_source_checkout(repository, revision)
    assert read_pinned_readme(repository, revision) == b"Pinned purpose\n"
    assert read_pinned_repository_document(repository, revision) == (
        "docs/readme.rst",
        b"Pinned purpose\n",
    )
    with pytest.raises(ValueError, match="revision mismatch"):
        validate_source_checkout(repository, "0" * 40)
    with pytest.raises(ValueError, match="unavailable"):
        validate_source_checkout(tmp_path / "missing", revision)


def test_prepares_nested_package_semantic_profile_from_pinned_objects(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    package = repository / "packages/agents"
    package.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repository, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repository, check=True)
    (repository / "README.md").write_text("Workflow automation platform\n")
    (package / "README.md").write_text("Build code-first AI agents\n")
    (package / "package.json").write_text(
        json.dumps(
            {
                "name": "@demo/agents",
                "description": "AI agent SDK",
                "keywords": ["agents", "workflow"],
            }
        )
    )
    (package / "pyproject.toml").write_text(
        '[project]\nname = "demo-agents"\ndescription = "Python AI agent SDK"\n'
        'keywords = ["agents", "workflow"]\n'
    )
    subprocess.run(["git", "add", "."], cwd=repository, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repository, check=True)
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    candidate = tmp_path / "candidate"
    (candidate / "specs").mkdir(parents=True)
    (candidate / "specpm.yaml").write_text(
        "kind: SpecPackage\nmetadata:\n  id: demo.agents\npreview_only: true\n"
    )
    (candidate / "specs/core.spec.yaml").write_text("kind: BoundarySpec\n")
    harvest = {
        "source": {
            "repository": "https://github.com/demo/workspace",
            "revision": revision,
            "target": {"kind": "folder", "path": "packages/agents", "label": "agents"},
        },
        "projectProfile": {
            "languages": [{"id": "javascript", "confidence": "high"}],
            "ecosystems": [{"id": "npm", "packageManager": "pnpm"}],
            "manifests": [{"path": "packages/agents/package.json"}],
            "analyzerPlan": [],
        },
        "files": [
            {
                "path": "packages/agents/package.json",
                "package": {"name": "@demo/agents", "description": "AI agent SDK"},
            }
        ],
    }
    (candidate / "harvest.json").write_text(json.dumps(harvest))
    output_root = tmp_path / "output"
    output_root.mkdir()

    workspace_path = prepare_workspace(
        candidate,
        repository,
        revision,
        output_root,
        repository_id="demo-workspace",
    )

    profile = json.loads((workspace_path / "semantic-product-profile.json").read_text())
    assert (workspace_path / "PACKAGE_README.md").read_text() == "Build code-first AI agents\n"
    assert profile["repository"]["owner"] == "demo"
    assert profile["documents"][0]["sourcePath"] == "README.md"
    assert profile["package"]["targetPath"] == "packages/agents"
    assert profile["package"]["description"] == "AI agent SDK"
    assert profile["package"]["keywords"] == ["agents", "workflow"]
    assert read_pinned_package_readme(repository, revision, harvest) is not None
    assert read_pinned_manifest_metadata(repository, revision, harvest)["name"] == "@demo/agents"
    python_harvest = copy.deepcopy(harvest)
    python_harvest["projectProfile"]["manifests"][0]["path"] = "packages/agents/pyproject.toml"
    assert read_pinned_manifest_metadata(repository, revision, python_harvest) == {
        "sourcePath": "packages/agents/pyproject.toml",
        "sha256": hashlib.sha256((package / "pyproject.toml").read_bytes()).hexdigest(),
        "name": "demo-agents",
        "description": "Python AI agent SDK",
        "keywords": ["agents", "workflow"],
    }
    missing_manifest = copy.deepcopy(harvest)
    missing_manifest["projectProfile"]["manifests"][0]["path"] = (
        "packages/agents/missing-package.json"
    )
    with pytest.raises(ValueError, match="Pinned package manifest is unavailable"):
        read_pinned_manifest_metadata(repository, revision, missing_manifest)


def test_rejects_packet_substitution_against_aggregate_binding(tmp_path: Path) -> None:
    source_manifest_dir, source_root, handoff_root, readiness = corpus(tmp_path)
    packet = handoff_root / "packets/repo-000/packet.json"
    value = json.loads(packet.read_text())
    value["substituted"] = True
    packet.write_text(json.dumps(value))

    with pytest.raises(ValueError, match="aggregate packet digest mismatch"):
        load_campaign_scope(
            source_manifest_dir=source_manifest_dir,
            source_root=source_root,
            handoff_root=handoff_root,
            readiness_evidence=readiness,
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
        selected.append(
            {
                "repositoryId": repository_id,
                "evidenceLinks": [
                    {
                        "role": "portable_packet",
                        "status": "present",
                        "path": f"handoff/packets/{repository_id}/packet.json",
                        "digest": f"sha256:{sha256_file(packet_dir / 'packet.json')}",
                    }
                ],
            }
        )

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
