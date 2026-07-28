from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.controlled_calibration import mapping_value, write_json

HANDOFF_API_VERSION = "spec-harvester.selected-candidate-handoff-proposal/v0"
HANDOFF_KIND = "SpecHarvesterSelectedCandidateHandoffProposal"
PACKET_API_VERSION = "spec-harvester.p53-portable-author-handoff-packet/v0"
PACKET_KIND = "SpecHarvesterP53PortableAuthorHandoffPacket"
REPORT_API_VERSION = "spec-harvester.p53-portable-author-handoff/v0"
REPORT_KIND = "SpecHarvesterP53PortableAuthorHandoff"
ALLOWED_CANDIDATE_SUFFIXES = {".json", ".yaml", ".yml", ".html", ".css", ".js"}
NON_AUTHORITY = [
    "This proposal is review evidence only.",
    "It is not SpecPM registry acceptance.",
    "It does not accept packages.",
    "It does not accept relations.",
    "It does not seed baselines.",
    "It does not remove preview_only.",
    "It does not publish registry metadata.",
    "It does not create a SpecPM pull request.",
    "It does not replace maintainer review.",
]


@dataclass(frozen=True)
class P53PortableAuthorHandoffOptions:
    triage: Path
    metadata: Path
    packet_root: Path
    aggregate_output: Path
    report_output: Path
    repo_root: Path
    candidate_root: Path | None = None
    proposal_root: Path | None = None


def build_p53_portable_author_handoff(
    options: P53PortableAuthorHandoffOptions,
) -> dict[str, Any]:
    triage = read_json_object(options.triage)
    metadata = read_json_object(options.metadata)
    validate_inputs(triage, metadata, options)
    repositories = sorted(
        (mapping_value(item) for item in metadata["repositories"]),
        key=lambda item: int(item["position"]),
    )
    triage_records = {
        mapping_value(item).get("id"): mapping_value(item) for item in triage["repositories"]
    }
    packet_records: list[dict[str, Any]] = []
    selected_candidates: list[dict[str, Any]] = []
    deferred_candidates: list[dict[str, Any]] = []
    portable_candidate_count = 0
    portable_proposal_count = 0

    if options.packet_root.exists() and any(options.packet_root.iterdir()):
        raise ValueError("P53-T14 packet root must be empty before generation")
    options.packet_root.mkdir(parents=True, exist_ok=True)
    for source in repositories:
        repository_id = string_value(source.get("id"))
        triage_record = triage_records[repository_id]
        packet_dir = options.packet_root / repository_id
        packet_dir.mkdir(parents=True, exist_ok=True)
        candidate = copy_candidate(repository_id, packet_dir, options.candidate_root)
        proposal = copy_proposal(repository_id, triage_record, packet_dir, options.proposal_root)
        portable_candidate_count += candidate["status"] == "portable"
        portable_proposal_count += proposal["status"] == "portable"
        packet = {
            "apiVersion": PACKET_API_VERSION,
            "kind": PACKET_KIND,
            "schemaVersion": 1,
            "phase": "P53",
            "task": "P53-T14",
            "status": "ready_for_author_review" if candidate["status"] == "portable" else "blocked",
            "repository": {
                "id": repository_id,
                "position": source.get("position"),
                "wave": source.get("wave"),
                "ecosystem": source.get("ecosystem"),
                "repositoryShape": source.get("repositoryShape"),
                "provenance": source.get("provenance"),
                "licenseProvenance": source.get("licenseProvenance"),
            },
            "triage": triage_record,
            "candidate": candidate,
            "aiProposal": proposal,
            "previewOnly": True,
            "maintainerDisposition": "external_required",
            "authority": "producer_portable_handoff_evidence_only",
            "privacy": {
                "rawPromptsPersisted": False,
                "rawProviderResponsesPersisted": False,
                "chainOfThoughtPersisted": False,
                "secretsPersisted": False,
            },
            "nonGoals": [
                "registry_acceptance",
                "package_acceptance",
                "relation_acceptance",
                "registry_publication",
            ],
        }
        packet_path = packet_dir / "packet.json"
        write_json(packet_path, packet)
        packet_digest = sha256_file(packet_path)
        packet_records.append(
            {
                "repositoryId": repository_id,
                "path": portable_path(packet_path, options.repo_root),
                "sha256": packet_digest,
                "status": packet["status"],
                "candidateStatus": candidate["status"],
                "aiProposalStatus": proposal["status"],
            }
        )
        if candidate["status"] == "portable":
            selected_candidates.append(
                selected_candidate_record(
                    repository_id,
                    packet_path,
                    packet_digest,
                    options,
                )
            )
        else:
            deferred_candidates.append(
                {
                    "id": repository_id,
                    "repositoryId": repository_id,
                    "handoffStatus": "excluded_from_selected_handoff",
                    "reason": "portable_candidate_missing",
                    "requiredAction": "Reconstruct and validate a preview-only candidate bundle.",
                }
            )

    triage_relative = portable_path(options.triage, options.repo_root)
    triage_digest = sha256_file(options.triage)
    aggregate = {
        "apiVersion": HANDOFF_API_VERSION,
        "kind": HANDOFF_KIND,
        "schemaVersion": 1,
        "authority": "producer_preview_evidence_only",
        "source": {
            "selectedDryRunFixture": {
                "apiVersion": triage.get("apiVersion"),
                "kind": triage.get("kind"),
                "path": triage_relative,
                "digest": f"sha256:{triage_digest}",
                "status": "selected_handoff_dry_run_ready",
            }
        },
        "summary": {
            "selectedCandidateCount": len(selected_candidates),
            "deferredCandidateCount": len(deferred_candidates),
            "requiredEvidenceRoleCount": 2,
            "specpmPullRequestCreated": False,
            "registryMutationCount": 0,
        },
        "requiredEvidenceRoles": [
            {
                "role": "selected_handoff_dry_run",
                "scope": "proposal",
                "path": triage_relative,
                "required": True,
            },
            {
                "role": "portable_packet",
                "scope": "selected_candidate",
                "path": "<repository_id>/packet.json",
                "required": True,
            },
        ],
        "selectedCandidates": selected_candidates,
        "deferredCandidates": deferred_candidates,
        "maintainerChecklist": [
            "Verify packet and candidate file digests before author review.",
            "Review generated specs and AI summary evidence before intake disposition.",
            "Run SpecPM validation before any accepted-source change.",
            "Record registry acceptance outside producer evidence.",
        ],
        "futureConsumerBoundary": {
            "specpmMayPreflight": True,
            "specpmMayAcceptAfterMaintainerReview": True,
            "producerCanAccept": False,
        },
        "nonAuthority": list(NON_AUTHORITY),
        "notExecuted": [
            "package manager execution",
            "harvested code execution",
            "AI rerun",
            "registry mutation",
            "SpecPM pull request creation",
        ],
    }
    write_json(options.aggregate_output, aggregate)
    report = {
        "apiVersion": REPORT_API_VERSION,
        "kind": REPORT_KIND,
        "schemaVersion": 1,
        "phase": "P53",
        "task": "P53-T14",
        "status": "passed" if portable_candidate_count == 100 else "review_required",
        "summary": {
            "repositoryCount": 100,
            "packetCount": len(packet_records),
            "portableCandidateCount": portable_candidate_count,
            "portableAIProposalCount": portable_proposal_count,
            "summaryOnlyAIProposalCount": 100 - portable_proposal_count,
            "deferredCount": len(deferred_candidates),
        },
        "source": {
            "triage": {
                "path": triage_relative,
                "sha256": triage_digest,
            },
            "metadata": {
                "path": portable_path(options.metadata, options.repo_root),
                "sha256": sha256_file(options.metadata),
            },
        },
        "aggregateHandoff": {
            "path": portable_path(options.aggregate_output, options.repo_root),
            "sha256": sha256_file(options.aggregate_output),
        },
        "packets": packet_records,
        "authority": "producer_portable_handoff_evidence_only",
        "registryMutationCount": 0,
    }
    write_json(options.report_output, report)
    return report


def validate_inputs(
    triage: dict[str, Any],
    metadata: dict[str, Any],
    options: P53PortableAuthorHandoffOptions,
) -> None:
    expected_triage = {
        "apiVersion": "spec-harvester.p53-campaign-quality-triage/v0",
        "kind": "SpecHarvesterP53CampaignQualityTriage",
        "phase": "P53",
        "task": "P53-T13",
        "status": "passed",
        "authority": "producer_triage_evidence_only",
    }
    if any(triage.get(key) != value for key, value in expected_triage.items()):
        raise ValueError("P53-T14 requires authorized passing P53-T13 triage")
    repositories = metadata.get("repositories")
    records = triage.get("repositories")
    if not isinstance(repositories, list) or len(repositories) != 100:
        raise ValueError("P53-T14 requires exactly 100 metadata repositories")
    if not isinstance(records, list) or len(records) != 100:
        raise ValueError("P53-T14 requires exactly 100 triage records")
    source_ids = [mapping_value(item).get("id") for item in repositories]
    record_ids = [mapping_value(item).get("id") for item in records]
    if len(set(source_ids)) != 100 or set(source_ids) != set(record_ids):
        raise ValueError("P53-T14 metadata and triage identities do not match")
    if any(
        mapping_value(item).get("disposition") != "selected_for_author_review" for item in records
    ):
        raise ValueError("P53-T14 cannot hand off a non-selected triage record")
    privacy = mapping_value(triage.get("privacy"))
    if any(
        privacy.get(key) is not False
        for key in (
            "rawPromptsPersisted",
            "rawProviderResponsesPersisted",
            "chainOfThoughtPersisted",
            "secretsPersisted",
        )
    ):
        raise ValueError("P53-T14 triage violates the privacy boundary")
    portable_path(options.triage, options.repo_root)
    portable_path(options.metadata, options.repo_root)
    portable_path(options.aggregate_output, options.repo_root)
    portable_path(options.report_output, options.repo_root)
    portable_path(options.packet_root, options.repo_root)


def copy_candidate(
    repository_id: str,
    packet_dir: Path,
    candidate_root: Path | None,
) -> dict[str, Any]:
    if candidate_root is None:
        return {"status": "missing_not_portable", "files": [], "previewOnly": True}
    source = candidate_root / repository_id
    if not source.is_dir() or source.is_symlink():
        return {"status": "missing_not_portable", "files": [], "previewOnly": True}
    destination = packet_dir / "candidate"
    files: list[dict[str, Any]] = []
    manifests = 0
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"P53-T14 candidate contains a symlink: {path}")
        if not path.is_file() or path.suffix.lower() not in ALLOWED_CANDIDATE_SUFFIXES:
            continue
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        if path.name == "specpm.yaml":
            manifests += 1
            validate_preview_only_manifest(target)
        files.append({"path": str(Path("candidate") / relative), "sha256": sha256_file(target)})
    if not files or manifests == 0:
        return {"status": "missing_not_portable", "files": files, "previewOnly": True}
    return {
        "status": "portable",
        "files": files,
        "fileCount": len(files),
        "manifestCount": manifests,
        "previewOnly": True,
    }


def copy_proposal(
    repository_id: str,
    triage_record: dict[str, Any],
    packet_dir: Path,
    proposal_root: Path | None,
) -> dict[str, Any]:
    proposal = mapping_value(triage_record.get("proposal"))
    digest = mapping_value(proposal.get("digest")).get("value")
    summary = proposal.get("summary")
    if proposal_root is None:
        return {
            "status": "summary_only_not_portable",
            "expectedSha256": digest,
            "summary": summary,
        }
    source = proposal_root / repository_id / "package-set-ai-draft-proposal.json"
    if not source.is_file() or source.is_symlink():
        return {
            "status": "summary_only_not_portable",
            "expectedSha256": digest,
            "summary": summary,
        }
    if sha256_file(source) != digest:
        raise ValueError(f"P53-T14 AI proposal digest mismatch for {repository_id}")
    target = packet_dir / "ai-proposal.json"
    shutil.copy2(source, target)
    return {
        "status": "portable",
        "path": "ai-proposal.json",
        "sha256": digest,
        "summary": summary,
    }


def selected_candidate_record(
    repository_id: str,
    packet_path: Path,
    packet_digest: str,
    options: P53PortableAuthorHandoffOptions,
) -> dict[str, Any]:
    triage_digest = sha256_file(options.triage)
    return {
        "id": repository_id,
        "repositoryId": repository_id,
        "candidateBundlePath": portable_path(packet_path.parent, options.repo_root),
        "previewOnly": True,
        "triageClassification": "candidate_layer_review_required",
        "maintainerAction": "review_for_possible_specpm_intake",
        "producerPreflight": {"status": "passed", "warningCount": 0, "errorCount": 0},
        "staticViewer": {
            "status": "ok",
            "source": portable_path(packet_path, options.repo_root),
        },
        "registryAcceptanceDecision": {
            "status": "external_required",
            "producerAuthority": "evidence_only",
            "requiredFor": "public_index_acceptance",
        },
        "evidenceLinks": [
            {
                "role": "selected_handoff_dry_run",
                "path": portable_path(options.triage, options.repo_root),
                "pathScope": "repo_relative",
                "digest": f"sha256:{triage_digest}",
                "status": "present",
            },
            {
                "role": "portable_packet",
                "path": portable_path(packet_path, options.repo_root),
                "pathScope": "repo_relative",
                "digest": f"sha256:{packet_digest}",
                "status": "present",
            },
        ],
    }


def validate_preview_only_manifest(path: Path) -> None:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("preview_only") is not True:
        raise ValueError(f"P53-T14 candidate manifest is not preview_only: {path}")


def portable_path(path: Path, root: Path) -> str:
    resolved_root = root.resolve()
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(resolved_root))
    except ValueError as exc:
        raise ValueError(f"P53-T14 path is outside the portable root: {path}") from exc


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"P53-T14 cannot read JSON object: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"P53-T14 requires a JSON object: {path}")
    return payload


def sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""
