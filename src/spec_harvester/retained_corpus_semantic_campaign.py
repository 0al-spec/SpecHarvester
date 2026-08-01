from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.9/3.10
    import tomli as tomllib

from spec_harvester.controlled_calibration import git_dirty_status, git_head
from spec_harvester.experimental_intent_policy import (
    GENERIC_OBSERVED_INTENT_IDS as GENERIC_INTENT_IDS,
)
from spec_harvester.portable_semantic_proposal import build_portable_semantic_proposal
from spec_harvester.relevant_intent_routing import (
    build_relevant_intent_catalog,
    load_specpm_observed_intent_snapshot,
)
from spec_harvester.semantic_author_input_pack import (
    SemanticAuthorInputPackOptions,
    build_semantic_author_input_pack,
)
from spec_harvester.semantic_author_pass import (
    CodexSparkSemanticAuthorProvider,
    SemanticAuthorPassError,
    SemanticAuthorPassOptions,
    run_semantic_author_pass,
)
from spec_harvester.semantic_product_profile import (
    PROFILE_FILENAME,
    build_semantic_product_profile,
    write_semantic_product_profile,
)
from spec_harvester.semantic_proposal_quality import evaluate_semantic_proposal_quality
from spec_harvester.source_manifest import read_repository_source_manifests

CAMPAIGN_API_VERSION = "spec-harvester.retained-corpus-semantic-campaign/v0"
CAMPAIGN_KIND = "SpecHarvesterRetainedCorpusSemanticCampaign"
RECORD_API_VERSION = "spec-harvester.retained-corpus-semantic-record/v0"
RECORD_KIND = "SpecHarvesterRetainedCorpusSemanticRecord"
EXPECTED_REPOSITORY_COUNT = 100
CODEX_SPARK_MODEL = "gpt-5.3-codex-spark"
CODEX_LUNA_MODEL = "gpt-5.6-luna"


@dataclass(frozen=True)
class CampaignTarget:
    repository_id: str
    revision: str
    wave: str
    packet_sha256: str
    candidate_id: str
    candidate_dir: Path
    source_dir: Path

    def binding(self) -> dict[str, str]:
        return {
            "repositoryId": self.repository_id,
            "revision": self.revision,
            "wave": self.wave,
            "packetSha256": self.packet_sha256,
            "candidateId": self.candidate_id,
        }


@dataclass(frozen=True)
class CampaignRunOptions:
    timeout_seconds: float = 300.0
    json_repair_max_attempts: int = 1
    provider_max_attempts: int = 2
    max_output_bytes: int = 256 * 1024


def load_campaign_scope(
    *,
    source_manifest_dir: Path,
    source_root: Path,
    handoff_root: Path,
    readiness_evidence: Path,
) -> tuple[dict[str, Any], list[CampaignTarget]]:
    sources = read_repository_source_manifests(source_manifest_dir)
    if len(sources) != EXPECTED_REPOSITORY_COUNT:
        raise ValueError("Retained corpus must contain exactly 100 repositories")
    repository_ids = [item["id"] for item in sources]
    if len(set(repository_ids)) != EXPECTED_REPOSITORY_COUNT:
        raise ValueError("Retained corpus repository IDs must be unique")

    aggregate_path = handoff_root / "aggregate-handoff.json"
    aggregate = _read_json(aggregate_path)
    selected = aggregate.get("selectedCandidates")
    packet_bindings = _aggregate_packet_bindings(selected)
    if set(packet_bindings) != set(repository_ids):
        raise ValueError("P53-T14 handoff does not match the retained corpus")

    readiness = _read_json(readiness_evidence)
    if readiness.get("decision") != {
        "p55T10Unblocked": True,
        "thresholdsRedefined": False,
    } or any(
        readiness.get("providers", {}).get(provider, {}).get("summary", {}).get("passed")
        is not True
        for provider in ("codex_spark", "lm_studio")
    ):
        raise ValueError("P55-T9A readiness evidence does not unblock P55-T10")

    intent_snapshot = load_specpm_observed_intent_snapshot()
    targets = [
        _load_target(
            source,
            source_root=source_root,
            handoff_root=handoff_root,
            expected_packet_sha256=packet_bindings[source["id"]],
        )
        for source in sources
    ]
    scope = {
        "apiVersion": CAMPAIGN_API_VERSION,
        "kind": CAMPAIGN_KIND,
        "schemaVersion": 1,
        "authority": "semantic_campaign_proposal_only",
        "provider": {
            "id": CODEX_SPARK_MODEL,
            "kind": "codex_exec",
        },
        "repositoryCount": EXPECTED_REPOSITORY_COUNT,
        "sourceManifestSha256": _directory_digest(source_manifest_dir, "*.yml"),
        "handoffAggregateSha256": sha256_file(aggregate_path),
        "p55T9AReadinessSha256": sha256_file(readiness_evidence),
        "specpmObservedIntentSnapshotSha256": intent_snapshot["snapshotSha256"],
        "inputProjection": {
            "id": "principal_candidate_semantic_projection_v1",
            "manifest": "exact",
            "boundaryFields": [
                "apiVersion",
                "kind",
                "metadata",
                "intent",
                "scope",
                "provides",
                "requires",
                "interfaces",
                "effects",
                "constraints",
            ],
            "publicInterfaceIndex": "omitted_packet_digest_bound",
            "interfaces": "id_kind_summary_language_max_32_per_direction",
            "documentation": "pinned_git_object_utf8_max_24_kib",
            "observedIntents": "specpm_observed_positive_lexical_matches_max_16",
        },
        "targets": [target.binding() for target in targets],
        "executionBoundary": _execution_boundary(),
    }
    scope["campaignInputSha256"] = digest(scope)
    return scope, targets


def _load_target(
    source: dict[str, Any],
    *,
    source_root: Path,
    handoff_root: Path,
    expected_packet_sha256: str,
) -> CampaignTarget:
    repository_id = source["id"]
    revision = source.get("revision")
    if not isinstance(revision, str):
        raise ValueError(f"Retained source revision is not pinned: {repository_id}")
    packet_dir = handoff_root / "packets" / repository_id
    packet_path = packet_dir / "packet.json"
    if sha256_file(packet_path) != expected_packet_sha256:
        raise ValueError(f"P53-T14 aggregate packet digest mismatch: {repository_id}")
    packet = _read_json(packet_path)
    if packet.get("repository", {}).get("id") != repository_id:
        raise ValueError(f"P53-T14 packet identity mismatch: {repository_id}")
    _verify_packet_files(packet_dir, packet)
    candidate_relative = select_principal_candidate(
        _read_json(packet_dir / "candidate" / "package-set-draft.json")
    )
    candidate_dir = _safe_child(packet_dir / "candidate", candidate_relative)
    manifest = yaml.safe_load((candidate_dir / "specpm.yaml").read_text(encoding="utf-8"))
    candidate_id = manifest.get("metadata", {}).get("id") if isinstance(manifest, dict) else None
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError(f"Principal candidate identity is invalid: {repository_id}")
    wave = packet.get("repository", {}).get("wave")
    if not isinstance(wave, str) or not wave:
        raise ValueError(f"P53-T14 packet wave is invalid: {repository_id}")
    return CampaignTarget(
        repository_id=repository_id,
        revision=revision,
        wave=wave,
        packet_sha256=sha256_file(packet_path),
        candidate_id=candidate_id,
        candidate_dir=candidate_dir,
        source_dir=source_root / repository_id,
    )


def _aggregate_packet_bindings(selected: Any) -> dict[str, str]:
    if not isinstance(selected, list):
        raise ValueError("P53-T14 handoff selected candidates are invalid")
    bindings: dict[str, str] = {}
    for item in selected:
        if not isinstance(item, dict) or not isinstance(item.get("repositoryId"), str):
            raise ValueError("P53-T14 selected candidate identity is invalid")
        repository_id = item["repositoryId"]
        links = item.get("evidenceLinks")
        portable = (
            [
                link
                for link in links
                if isinstance(link, dict)
                and link.get("role") == "portable_packet"
                and link.get("status") == "present"
            ]
            if isinstance(links, list)
            else []
        )
        if len(portable) != 1:
            raise ValueError(f"P53-T14 portable packet binding is invalid: {repository_id}")
        digest_value = portable[0].get("digest")
        path_value = portable[0].get("path")
        path = PurePosixPath(path_value) if isinstance(path_value, str) else None
        if (
            repository_id in bindings
            or not isinstance(digest_value, str)
            or not digest_value.startswith("sha256:")
            or len(digest_value) != 71
            or any(character not in "0123456789abcdef" for character in digest_value[7:])
            or path is None
            or path.is_absolute()
            or ".." in path.parts
            or tuple(path.parts[-3:]) != ("packets", repository_id, "packet.json")
        ):
            raise ValueError(f"P53-T14 portable packet binding is invalid: {repository_id}")
        bindings[repository_id] = digest_value[7:]
    return bindings


def select_principal_candidate(draft: dict[str, Any]) -> str:
    candidates = draft.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Package-set draft has no candidates")
    eligible = [
        item
        for item in candidates
        if isinstance(item, dict)
        and item.get("status") == "ok"
        and isinstance(item.get("candidatePath"), str)
    ]
    if not eligible:
        raise ValueError("Package-set draft has no eligible candidates")
    selected = next(
        (item for item in eligible if item.get("role") == "member_package"), eligible[0]
    )
    return selected["candidatePath"]


def initialize_campaign(work_root: Path, scope: dict[str, Any]) -> None:
    work_root.mkdir(parents=True, exist_ok=True)
    scope_path = work_root / "campaign-input.json"
    if scope_path.exists():
        existing = _read_json(scope_path)
        if existing != scope:
            raise ValueError("Resumed campaign input binding is stale")
    else:
        _atomic_write_json(scope_path, scope)
    (work_root / "records").mkdir(exist_ok=True)


def run_campaign_target(
    target: CampaignTarget,
    *,
    scope: dict[str, Any],
    work_root: Path,
    provider: CodexSparkSemanticAuthorProvider,
    options: CampaignRunOptions,
) -> dict[str, Any]:
    _validate_run_options(options)
    record_path = _record_path(work_root, target.repository_id)
    if record_path.exists():
        record = _read_json(record_path)
        validate_campaign_record(record, scope, target)
        return record

    validate_source_checkout(target.source_dir, target.revision)
    attempt_records: list[dict[str, Any]] = []
    terminal: dict[str, Any] | None = None
    try:
        with tempfile.TemporaryDirectory(prefix="p55-t10-") as temporary:
            workspace = prepare_workspace(
                target.candidate_dir,
                target.source_dir,
                target.revision,
                Path(temporary),
                repository_id=target.repository_id,
            )
            manifest = yaml.safe_load((workspace / "specpm.yaml").read_text(encoding="utf-8"))
            static_intent_ids = manifest_intent_ids(manifest)
            product_profile = _read_json(workspace / PROFILE_FILENAME)
            intent_catalog = observed_catalog(manifest, product_profile)
            if intent_catalog["snapshotSha256"] != scope["specpmObservedIntentSnapshotSha256"]:
                raise ValueError("SpecPM observed intent snapshot binding is stale")
            pack = build_semantic_author_input_pack(
                workspace,
                intent_catalog,
                options=SemanticAuthorInputPackOptions(
                    document_paths=tuple(
                        path
                        for path in ("README.md", "PACKAGE_README.md")
                        if (workspace / path).exists()
                    )
                ),
            )
    except (ValueError, OSError) as exc:
        terminal = {
            "apiVersion": RECORD_API_VERSION,
            "kind": RECORD_KIND,
            "schemaVersion": 1,
            "authority": "semantic_campaign_proposal_only",
            "campaignInputSha256": scope["campaignInputSha256"],
            **target.binding(),
            "status": "failed",
            "failureStage": "input_pack",
            "failureCode": str(exc)[:500],
            "attempts": [],
            "executionBoundary": _execution_boundary(),
        }
    for attempt in range(1, options.provider_max_attempts + 1):
        if terminal is not None:
            break
        started = time.monotonic()
        try:
            semantic_pass = run_semantic_author_pass(
                pack,
                provider,
                options=SemanticAuthorPassOptions(
                    timeout_seconds=options.timeout_seconds,
                    max_output_bytes=options.max_output_bytes,
                    json_repair_max_attempts=options.json_repair_max_attempts,
                ),
            )
            quality = evaluate_semantic_proposal_quality(pack, semantic_pass)
            portable = (
                build_portable_semantic_proposal(pack, semantic_pass, quality)
                if quality["status"] != "rejected"
                else None
            )
            terminal = _completed_record(
                target,
                scope=scope,
                attempt=attempt,
                attempt_records=attempt_records,
                pack=pack,
                semantic_pass=semantic_pass,
                quality=quality,
                portable=portable,
                static_intent_ids=static_intent_ids,
            )
            attempt_records.append(
                _attempt_record(attempt, "completed", started, semantic_pass=semantic_pass)
            )
            terminal["attempts"] = attempt_records
            break
        except (SemanticAuthorPassError, ValueError, OSError) as exc:
            attempt_records.append(_attempt_record(attempt, "failed", started, error=exc))

    if terminal is None:
        terminal = {
            "apiVersion": RECORD_API_VERSION,
            "kind": RECORD_KIND,
            "schemaVersion": 1,
            "authority": "semantic_campaign_proposal_only",
            "campaignInputSha256": scope["campaignInputSha256"],
            **target.binding(),
            "status": "failed",
            "attempts": attempt_records,
            "executionBoundary": _execution_boundary(),
        }
    terminal["recordSha256"] = digest(terminal)
    validate_campaign_record(terminal, scope, target)
    record_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(record_path, terminal)
    portable = terminal.get("portableProposal")
    if isinstance(portable, dict):
        _atomic_write_json(record_path.parent / "semantic-proposal-record.json", portable)
    return terminal


def _completed_record(
    target: CampaignTarget,
    *,
    scope: dict[str, Any],
    attempt: int,
    attempt_records: list[dict[str, Any]],
    pack: dict[str, Any],
    semantic_pass: dict[str, Any],
    quality: dict[str, Any],
    portable: dict[str, Any] | None,
    static_intent_ids: list[str],
) -> dict[str, Any]:
    proposal = semantic_pass["proposal"]
    intent_decisions = proposal["intentDecisions"]
    record: dict[str, Any] = {
        "apiVersion": RECORD_API_VERSION,
        "kind": RECORD_KIND,
        "schemaVersion": 1,
        "authority": "semantic_campaign_proposal_only",
        "campaignInputSha256": scope["campaignInputSha256"],
        **target.binding(),
        "status": "completed",
        "providerAttemptCount": attempt,
        "attempts": attempt_records,
        "sourceBundleSha256": pack["sourceBundleSha256"],
        "staticObservedIntentIds": static_intent_ids,
        "routedObservedIntentIds": [item["intentId"] for item in pack["observedIntents"]],
        "intentRouting": pack["intentRouting"],
        "proposalReuseIntentIds": sorted(
            item["intentId"] for item in intent_decisions if item["state"] == "proposed_reuse"
        ),
        "experimentalIntentIds": sorted(
            item["intentId"]
            for item in intent_decisions
            if item["state"] == "proposed_experimental"
        ),
        "semanticPass": semantic_pass,
        "qualityReport": quality,
        "portableProposal": portable,
        "executionBoundary": _execution_boundary(),
    }
    return record


def validate_campaign_record(
    record: dict[str, Any], scope: dict[str, Any], target: CampaignTarget
) -> None:
    if (
        record.get("apiVersion") != RECORD_API_VERSION
        or record.get("kind") != RECORD_KIND
        or record.get("authority") != "semantic_campaign_proposal_only"
        or record.get("campaignInputSha256") != scope.get("campaignInputSha256")
        or any(record.get(key) != value for key, value in target.binding().items())
        or record.get("status") not in {"completed", "failed"}
        or record.get("executionBoundary") != _execution_boundary()
        or record.get("recordSha256") != _digest_without(record, "recordSha256")
    ):
        raise ValueError(f"Campaign record binding is stale: {target.repository_id}")
    attempts = record.get("attempts")
    if not isinstance(attempts, list) or len(attempts) > 2:
        raise ValueError(f"Campaign record attempt accounting is invalid: {target.repository_id}")
    if record["status"] == "completed":
        if not attempts:
            raise ValueError(
                f"Completed campaign record has no provider attempt: {target.repository_id}"
            )
        if not all(
            isinstance(record.get(key), expected)
            for key, expected in (
                ("semanticPass", dict),
                ("qualityReport", dict),
                ("staticObservedIntentIds", list),
                ("routedObservedIntentIds", list),
                ("intentRouting", dict),
                ("proposalReuseIntentIds", list),
                ("experimentalIntentIds", list),
            )
        ):
            raise ValueError(f"Completed campaign record is incomplete: {target.repository_id}")
        if (
            record["intentRouting"].get("snapshotSha256")
            != scope.get("specpmObservedIntentSnapshotSha256")
            or record["intentRouting"].get("selectedIntentIds") != record["routedObservedIntentIds"]
        ):
            raise ValueError(f"Campaign record intent routing is stale: {target.repository_id}")


def finalize_campaign(
    *,
    scope: dict[str, Any],
    targets: list[CampaignTarget],
    work_root: Path,
    output_path: Path,
    archive_path: Path,
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for target in targets:
        path = _record_path(work_root, target.repository_id)
        if not path.is_file():
            raise ValueError(f"Campaign is incomplete: {target.repository_id}")
        record = _read_json(path)
        validate_campaign_record(record, scope, target)
        records.append(record)

    archive_sha256 = write_deterministic_archive(work_root, archive_path)
    report = campaign_summary(scope, records)
    report["archive"] = {
        "path": archive_path.name,
        "sha256": archive_sha256,
        "recordCount": len(records),
    }
    report["reportSha256"] = digest(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(output_path, report)
    return report


def campaign_summary(scope: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    if len(records) != EXPECTED_REPOSITORY_COUNT:
        raise ValueError("Full campaign summary requires exactly 100 records")
    completed = [record for record in records if record["status"] == "completed"]
    failed = [record for record in records if record["status"] == "failed"]
    quality_counts = Counter(record["qualityReport"]["status"] for record in completed)
    diagnostics = Counter(
        item["code"] for record in completed for item in record["qualityReport"]["diagnostics"]
    )
    static_generic = sum(
        intent_id in GENERIC_INTENT_IDS
        for record in completed
        for intent_id in record["staticObservedIntentIds"]
    )
    proposed_generic = sum(
        intent_id in GENERIC_INTENT_IDS
        for record in completed
        for intent_id in record["proposalReuseIntentIds"]
    )
    experimental = Counter(
        intent_id for record in completed for intent_id in record["experimentalIntentIds"]
    )
    duration_ms = sum(attempt["durationMs"] for record in records for attempt in record["attempts"])
    usage: Counter[str] = Counter()
    for record in completed:
        usage.update(
            {
                key: value
                for key, value in record["semanticPass"]["providerReceipt"].get("usage", {}).items()
                if isinstance(value, int)
            }
        )
    repair_count = sum(
        record["semanticPass"]["providerReceipt"]["jsonRepairNeeded"] for record in completed
    )
    return {
        "apiVersion": CAMPAIGN_API_VERSION,
        "kind": CAMPAIGN_KIND,
        "schemaVersion": 1,
        "authority": "semantic_campaign_proposal_only",
        "campaignInputSha256": scope["campaignInputSha256"],
        "bindings": {
            key: scope[key]
            for key in (
                "sourceManifestSha256",
                "handoffAggregateSha256",
                "p55T9AReadinessSha256",
                "specpmObservedIntentSnapshotSha256",
            )
        },
        "provider": scope["provider"],
        "summary": {
            "repositoryCount": len(records),
            "completedCount": len(completed),
            "failedCount": len(failed),
            "portableProposalCount": sum(
                isinstance(record.get("portableProposal"), dict) for record in completed
            ),
            "qualityStatusCounts": dict(sorted(quality_counts.items())),
        },
        "semanticQuality": {
            "purposeClaimCoverageRate": _rate(
                sum(
                    record["qualityReport"]["metrics"]["purposeClaimCount"] > 0
                    for record in completed
                ),
                len(records),
            ),
            "evidenceSupportedProposalRate": _rate(
                sum(
                    record["qualityReport"]["metrics"]["evidenceSupportRate"] == 1.0
                    for record in completed
                ),
                len(records),
            ),
            "schemaValidProposalRate": _rate(
                sum(
                    record["qualityReport"]["metrics"]["schemaValid"] is True
                    for record in completed
                ),
                len(records),
            ),
            "staticGenericIntentReferenceCount": static_generic,
            "proposedGenericIntentReuseCount": proposed_generic,
            "genericIntentReductionCount": static_generic - proposed_generic,
            "routedObservedIntentReferenceCount": sum(
                len(record["routedObservedIntentIds"]) for record in completed
            ),
            "specificPurposeGenericOnlyContradictionCount": diagnostics.get(
                "specific_purpose_generic_only_contradiction", 0
            ),
            "diagnosticCounts": dict(sorted(diagnostics.items())),
            "duplicateExperimentalIntentIds": {
                key: count for key, count in sorted(experimental.items()) if count > 1
            },
            "reviewerEditBurden": {
                "status": "unavailable_without_reviewer_decision_evidence",
                "reviewedRecordCount": 0,
            },
        },
        "reviewerDecisions": {
            "acceptedCount": 0,
            "editedCount": 0,
            "rejectedCount": 0,
            "deferredCount": 0,
            "unreviewedCount": len(records),
            "source": "no_reviewer_decision_evidence_supplied",
        },
        "budgets": {
            "providerAttemptCount": sum(len(record["attempts"]) for record in records),
            "failedProviderAttemptCount": sum(
                attempt["status"] == "failed"
                for record in records
                for attempt in record["attempts"]
            ),
            "jsonRepairRecordCount": repair_count,
            "durationMs": duration_ms,
            "tokenUsage": dict(sorted(usage.items())),
            "cost": {"status": "unavailable_from_codex_exec_receipts"},
        },
        "privacy": {
            "rawPromptsPersisted": False,
            "rawResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "credentialsPersisted": False,
            "machineLocalPathsPersisted": False,
        },
        "executionBoundary": _execution_boundary(),
        "recordIndex": [
            {
                "repositoryId": record["repositoryId"],
                "candidateId": record["candidateId"],
                "status": record["status"],
                "recordSha256": record["recordSha256"],
            }
            for record in records
        ],
    }


def write_deterministic_archive(work_root: Path, archive_path: Path) -> str:
    paths = [work_root / "campaign-input.json", *sorted((work_root / "records").rglob("*.json"))]
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as archive:
        for path in paths:
            if path.is_symlink() or not path.is_file():
                raise ValueError("Campaign archive input must be a regular file")
            relative = path.relative_to(work_root).as_posix()
            data = path.read_bytes()
            info = tarfile.TarInfo(relative)
            info.size = len(data)
            info.mode = 0o644
            info.mtime = 0
            archive.addfile(info, io.BytesIO(data))
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with archive_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            compressed.write(tar_buffer.getvalue())
    return sha256_file(archive_path)


def prepare_workspace(
    candidate: Path,
    source: Path,
    revision: str,
    root: Path,
    *,
    repository_id: str,
) -> Path:
    workspace = root / "workspace"
    workspace.mkdir()
    shutil.copy2(candidate / "specpm.yaml", workspace / "specpm.yaml")
    (workspace / "specs").mkdir()
    for source_spec in sorted((candidate / "specs").glob("*.spec.yaml")):
        value = yaml.safe_load(source_spec.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"BoundarySpec projection source is invalid: {source_spec.name}")
        projected = {
            key: value[key]
            for key in (
                "apiVersion",
                "kind",
                "metadata",
                "intent",
                "scope",
                "provides",
                "requires",
                "interfaces",
                "effects",
                "constraints",
            )
            if key in value
        }
        if isinstance(value.get("interfaces"), dict):
            projected["interfaces"] = {
                direction: [
                    {
                        key: interface[key]
                        for key in ("id", "kind", "summary", "language")
                        if key in interface
                    }
                    for interface in value["interfaces"].get(direction, [])[:32]
                    if isinstance(interface, dict)
                ]
                for direction in ("inbound", "outbound")
            }
        (workspace / "specs" / source_spec.name).write_text(
            yaml.safe_dump(projected, sort_keys=False), encoding="utf-8"
        )
    harvest_path = candidate / "harvest.json"
    shutil.copy2(harvest_path, workspace / "harvest.json")
    harvest = json.loads(harvest_path.read_text(encoding="utf-8"))
    if not isinstance(harvest, dict):
        raise ValueError("Candidate harvest.json must be an object")
    repository_source_path, root_readme = read_pinned_repository_document(source, revision)
    (workspace / "README.md").write_bytes(root_readme)
    package_readme = read_pinned_package_readme(source, revision, harvest)
    package_document = None
    if package_readme is not None:
        package_source_path, package_readme_bytes = package_readme
        (workspace / "PACKAGE_README.md").write_bytes(package_readme_bytes)
        package_document = _document_record(
            "PACKAGE_README.md", package_source_path, package_readme_bytes
        )
    candidate_manifest = yaml.safe_load((candidate / "specpm.yaml").read_text(encoding="utf-8"))
    candidate_id = candidate_manifest.get("metadata", {}).get("id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("Candidate specpm.yaml metadata.id must be non-empty")
    profile = build_semantic_product_profile(
        repository_id=repository_id,
        candidate_id=candidate_id,
        harvest=harvest,
        root_document={
            **_document_record("README.md", repository_source_path, root_readme),
            "harvestSha256": sha256_file(harvest_path),
        },
        package_document=package_document,
        manifest_metadata=read_pinned_manifest_metadata(source, revision, harvest),
    )
    write_semantic_product_profile(workspace / PROFILE_FILENAME, profile)
    return workspace


def validate_source_checkout(source: Path, expected_revision: str) -> None:
    if not source.is_dir() or source.is_symlink():
        raise ValueError(f"Retained source checkout is unavailable: {source.name}")
    if git_head(source) != expected_revision:
        raise ValueError(f"Retained source revision mismatch: {source.name}")
    if git_dirty_status(source) is None:
        raise ValueError(f"Retained source status is unavailable: {source.name}")


def read_pinned_readme(source: Path, revision: str) -> bytes:
    return read_pinned_repository_document(source, revision)[1]


def read_pinned_repository_document(source: Path, revision: str) -> tuple[str, bytes]:
    allowed_names = {
        "readme",
        "readme.adoc",
        "readme.md",
        "readme.markdown",
        "readme.rst",
        "readme.txt",
    }
    listing = subprocess.run(  # noqa: S603
        ["git", "ls-tree", "--name-only", revision],
        cwd=source,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=30,
        text=True,
    )
    names = ["README.md", "README.markdown", "README"]
    if listing.returncode == 0:
        names.extend(
            name for name in listing.stdout.splitlines() if name.casefold() in allowed_names
        )
    if not any(name.casefold() in allowed_names for name in listing.stdout.splitlines()):
        recursive = subprocess.run(  # noqa: S603
            ["git", "ls-tree", "-r", "--name-only", revision],
            cwd=source,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=30,
            text=True,
        )
        if recursive.returncode == 0:
            nested = [
                name
                for name in recursive.stdout.splitlines()
                if Path(name).name.casefold() in allowed_names
            ]
            names.extend(sorted(nested, key=lambda name: (name.count("/"), name)))
    for name in dict.fromkeys(names):
        completed = subprocess.run(  # noqa: S603
            ["git", "show", f"{revision}:{name}"],
            cwd=source,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=30,
        )
        if completed.returncode == 0:
            text = completed.stdout.decode("utf-8", errors="strict")
            while len(text.encode("utf-8")) > 24 * 1024:
                text = text[: int(len(text) * 0.9)]
            return name, text.encode("utf-8")
    raise ValueError(f"Pinned README evidence is unavailable: {source.name}")


def read_pinned_package_readme(
    source: Path, revision: str, harvest: dict[str, Any]
) -> tuple[str, bytes] | None:
    source_record = harvest.get("source") if isinstance(harvest.get("source"), dict) else {}
    target = source_record.get("target") if isinstance(source_record.get("target"), dict) else {}
    target_path = str(target.get("path") or ".")
    if target_path == ".":
        return None
    relative = PurePosixPath(target_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Package target path is unsafe")
    directories = [relative, *relative.parents]
    for directory in directories:
        if directory.as_posix() == ".":
            continue
        for filename in (
            "README.md",
            "README.markdown",
            "README.rst",
            "README.adoc",
            "README.txt",
            "README",
        ):
            path = (directory / filename).as_posix()
            raw = _git_show_bounded(source, revision, path, 24 * 1024)
            if raw is not None:
                return path, raw
    return None


def read_pinned_manifest_metadata(
    source: Path, revision: str, harvest: dict[str, Any]
) -> dict[str, Any] | None:
    project = (
        harvest.get("projectProfile") if isinstance(harvest.get("projectProfile"), dict) else {}
    )
    manifests = project.get("manifests") if isinstance(project.get("manifests"), list) else []
    path = next(
        (
            str(item["path"])
            for item in manifests
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        ),
        "",
    )
    if not path:
        return None
    relative = PurePosixPath(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Package manifest path is unsafe")
    raw = _git_show_bounded(source, revision, path, 64 * 1024)
    if raw is None:
        raise ValueError(f"Pinned package manifest is unavailable: {path}")
    payload = _parse_manifest_metadata(path, raw)
    if not isinstance(payload, dict):
        payload = {}
    package = payload.get("package") if isinstance(payload.get("package"), dict) else {}
    project = payload.get("project") if isinstance(payload.get("project"), dict) else {}
    tool = payload.get("tool") if isinstance(payload.get("tool"), dict) else {}
    poetry = tool.get("poetry") if isinstance(tool.get("poetry"), dict) else {}
    metadata = next((item for item in (project, package, poetry, payload) if item), {})
    return {
        "sourcePath": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "name": metadata.get("name", ""),
        "description": metadata.get("description", ""),
        "keywords": metadata.get("keywords", []),
    }


def _parse_manifest_metadata(path: str, raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
        if PurePosixPath(path).suffix == ".json":
            value = json.loads(text)
        elif PurePosixPath(path).suffix == ".toml":
            value = tomllib.loads(text)
        else:
            return {}
    except (UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _git_show_bounded(source: Path, revision: str, path: str, maximum_bytes: int) -> bytes | None:
    completed = subprocess.run(  # noqa: S603
        ["git", "show", f"{revision}:{path}"],
        cwd=source,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        return None
    text = completed.stdout.decode("utf-8", errors="strict")
    while len(text.encode("utf-8")) > maximum_bytes:
        text = text[: int(len(text) * 0.9)]
    return text.encode("utf-8")


def _document_record(evidence_path: str, source_path: str, raw: bytes) -> dict[str, Any]:
    return {
        "evidencePath": evidence_path,
        "sourcePath": source_path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "byteCount": len(raw),
    }


def observed_catalog(manifest: dict[str, Any], product_profile: dict[str, Any]) -> dict[str, Any]:
    return build_relevant_intent_catalog(
        product_profile,
        current_intent_ids=manifest_intent_ids(manifest),
    )


def manifest_intent_ids(manifest: dict[str, Any]) -> list[str]:
    provides = manifest.get("index", {}).get("provides", {})
    return sorted({item for item in provides.get("intents", []) if isinstance(item, str)})


def _verify_packet_files(packet_dir: Path, packet: dict[str, Any]) -> None:
    files = packet.get("candidate", {}).get("files")
    if not isinstance(files, list) or not files:
        raise ValueError(f"P53-T14 packet has no candidate files: {packet_dir.name}")
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError(f"P53-T14 packet file binding is invalid: {packet_dir.name}")
        path = _safe_child(packet_dir, item["path"])
        if path.is_symlink() or not path.is_file() or sha256_file(path) != item.get("sha256"):
            raise ValueError(f"P53-T14 packet file binding is stale: {packet_dir.name}")


def _safe_child(root: Path, relative: str) -> Path:
    if Path(relative).is_absolute():
        raise ValueError("Campaign path must be relative")
    root_resolved = root.resolve()
    path = (root / relative).resolve()
    if path == root_resolved or root_resolved not in path.parents:
        raise ValueError("Campaign path escapes its root")
    return path


def _attempt_record(
    attempt: int,
    status: str,
    started: float,
    *,
    semantic_pass: dict[str, Any] | None = None,
    error: Exception | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "attempt": attempt,
        "status": status,
        "durationMs": int((time.monotonic() - started) * 1000),
    }
    if semantic_pass is not None:
        receipt = semantic_pass["providerReceipt"]
        record.update(
            {
                "jsonRepairNeeded": receipt["jsonRepairNeeded"],
                "jsonRepairAttemptCount": receipt["jsonRepairAttemptCount"],
            }
        )
    if error is not None:
        record["failureCode"] = str(error)[:500]
    return record


def _validate_run_options(options: CampaignRunOptions) -> None:
    if (
        options.timeout_seconds <= 0
        or options.max_output_bytes <= 0
        or not 0 <= options.json_repair_max_attempts <= 1
        or not 1 <= options.provider_max_attempts <= 2
    ):
        raise ValueError("Semantic campaign budgets are invalid")


def _execution_boundary() -> dict[str, bool]:
    return {
        "repositoryCodeExecuted": False,
        "packageManagerInvoked": False,
        "reviewerDecisionCreated": False,
        "materializationPerformed": False,
        "specpmMutated": False,
        "registryMutated": False,
        "publicationPerformed": False,
    }


def _record_path(work_root: Path, repository_id: str) -> Path:
    return work_root / "records" / repository_id / "campaign-record.json"


def _directory_digest(root: Path, pattern: str) -> str:
    records = [
        {"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path)}
        for path in sorted(root.glob(pattern))
    ]
    return digest(records)


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read campaign JSON: {path.name}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Campaign JSON must be an object: {path.name}")
    return value


def _atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _digest_without(value: dict[str, Any], key: str) -> str:
    return digest({name: item for name, item in value.items() if name != key})
