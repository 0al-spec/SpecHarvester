from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from spec_harvester.ai_semantic_author_schema import load_ai_semantic_author_schema
from spec_harvester.semantic_proposal_quality import evaluate_semantic_proposal_quality

PORTABLE_SEMANTIC_API_VERSION = "spec-harvester.portable-semantic-proposal/v0"
PORTABLE_SEMANTIC_KIND = "SpecHarvesterPortableSemanticProposal"
SEMANTIC_INPUT_FILES = ("input-pack.json", "semantic-pass.json", "quality-report.json")
RECEIPT_KEYS = {
    "providerKind",
    "providerName",
    "providerId",
    "durationMs",
    "jsonRepairNeeded",
    "jsonRepairAttemptCount",
    "jsonRepairStatus",
    "rawPromptPersisted",
    "rawResponsePersisted",
    "chainOfThoughtPersisted",
    "modelId",
    "baseUrl",
    "endpoint",
    "usage",
    "receiptSha256",
}
REQUIRED_RECEIPT_KEYS = {
    "providerKind",
    "providerName",
    "providerId",
    "durationMs",
    "jsonRepairNeeded",
    "jsonRepairAttemptCount",
    "jsonRepairStatus",
    "rawPromptPersisted",
    "rawResponsePersisted",
    "chainOfThoughtPersisted",
    "receiptSha256",
}
MACHINE_LOCAL_PREFIXES = ("/Users/", "/home/", "/tmp/", "/private/var/")
PORTABLE_RECORD_KEYS = {
    "apiVersion",
    "kind",
    "schemaVersion",
    "authority",
    "candidateId",
    "sourceBundleSha256",
    "proposalSha256",
    "providerReceiptSha256",
    "qualityReportSha256",
    "qualityStatus",
    "proposal",
    "qualityReport",
    "providerReceipt",
    "privacy",
    "executionBoundary",
    "recordSha256",
}
QUALITY_REPORT_KEYS = {
    "apiVersion",
    "kind",
    "schemaVersion",
    "authority",
    "candidateId",
    "sourceBundleSha256",
    "proposalSha256",
    "policy",
    "status",
    "eligibleForCalibration",
    "summary",
    "metrics",
    "diagnostics",
    "executionBoundary",
}


def build_portable_semantic_proposal(
    input_pack: dict[str, Any],
    semantic_pass: dict[str, Any],
    quality_report: dict[str, Any],
) -> dict[str, Any]:
    """Build a self-contained proposal-only record from validated P55 artifacts."""
    candidate_id = input_pack.get("candidateId")
    source_digest = input_pack.get("sourceBundleSha256")
    if (
        input_pack.get("kind") != "SpecHarvesterAISemanticAuthorInputPack"
        or semantic_pass.get("kind") != "SpecHarvesterSemanticAuthorPass"
        or quality_report.get("kind") != "SpecHarvesterSemanticProposalQualityReport"
        or not isinstance(candidate_id, str)
        or not isinstance(source_digest, str)
    ):
        raise ValueError("portable semantic proposal inputs are malformed")

    expected_quality = evaluate_semantic_proposal_quality(input_pack, semantic_pass)
    if quality_report != expected_quality:
        raise ValueError("portable semantic proposal quality report is stale")
    if quality_report.get("status") == "rejected":
        raise ValueError("rejected semantic proposal cannot become portable")

    proposal = semantic_pass.get("proposal")
    receipt = semantic_pass.get("providerReceipt")
    if not isinstance(proposal, dict) or not isinstance(receipt, dict):
        raise ValueError("portable semantic proposal pass records are malformed")
    _validate_receipt(receipt)
    receipt_digest = _digest_without(receipt, "receiptSha256")
    proposal_digest = _digest_without(proposal, "proposalSha256")
    if (
        receipt.get("receiptSha256") != receipt_digest
        or proposal.get("proposalSha256") != proposal_digest
        or proposal.get("provider", {}).get("receiptSha256") != receipt_digest
    ):
        raise ValueError("portable semantic proposal digest binding is stale")
    if any(
        record.get("candidateId") != candidate_id
        or record.get("sourceBundleSha256") != source_digest
        for record in (semantic_pass, proposal, quality_report)
    ):
        raise ValueError("portable semantic proposal candidate or source binding is stale")

    record = {
        "apiVersion": PORTABLE_SEMANTIC_API_VERSION,
        "kind": PORTABLE_SEMANTIC_KIND,
        "schemaVersion": 1,
        "authority": "portable_semantic_proposal_evidence_only",
        "candidateId": candidate_id,
        "sourceBundleSha256": source_digest,
        "proposalSha256": proposal_digest,
        "providerReceiptSha256": receipt_digest,
        "qualityReportSha256": _digest(quality_report),
        "qualityStatus": quality_report["status"],
        "proposal": proposal,
        "qualityReport": quality_report,
        "providerReceipt": receipt,
        "privacy": {
            "rawPromptsPersisted": False,
            "rawProviderResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "credentialsPersisted": False,
            "providerLocalPathsPersisted": False,
        },
        "executionBoundary": {
            "providerInvokedDuringPortability": False,
            "materializationPerformed": False,
            "specpmMutated": False,
            "registryMutated": False,
            "publicationPerformed": False,
        },
    }
    record["recordSha256"] = _digest(record)
    validate_portable_semantic_proposal(record)
    return record


def build_portable_semantic_proposal_from_directory(source: Path) -> dict[str, Any]:
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f"portable semantic proposal source is unavailable: {source}")
    records = [_read_json_object(source / name) for name in SEMANTIC_INPUT_FILES]
    return build_portable_semantic_proposal(*records)


def validate_portable_semantic_proposal(record: dict[str, Any]) -> None:
    if set(record) != PORTABLE_RECORD_KEYS or (
        record.get("apiVersion") != PORTABLE_SEMANTIC_API_VERSION
        or record.get("kind") != PORTABLE_SEMANTIC_KIND
        or record.get("schemaVersion") != 1
        or record.get("authority") != "portable_semantic_proposal_evidence_only"
    ):
        raise ValueError("portable semantic proposal identity is invalid")
    candidate_id = record.get("candidateId")
    source_digest = record.get("sourceBundleSha256")
    proposal = record.get("proposal")
    quality = record.get("qualityReport")
    receipt = record.get("providerReceipt")
    if not all(isinstance(item, dict) for item in (proposal, quality, receipt)):
        raise ValueError("portable semantic proposal embedded records are malformed")
    if set(quality) != QUALITY_REPORT_KEYS:
        raise ValueError("portable semantic proposal quality report shape is invalid")
    proposal_schema = {
        "$ref": "#/$defs/proposal",
        "$defs": load_ai_semantic_author_schema()["$defs"],
    }
    proposal_errors = list(
        Draft202012Validator(proposal_schema, format_checker=FormatChecker()).iter_errors(proposal)
    )
    if proposal_errors:
        raise ValueError("portable semantic proposal embedded proposal shape is invalid")
    _validate_receipt(receipt)
    if (
        record.get("recordSha256") != _digest_without(record, "recordSha256")
        or record.get("proposalSha256") != _digest_without(proposal, "proposalSha256")
        or record.get("providerReceiptSha256") != _digest_without(receipt, "receiptSha256")
        or record.get("qualityReportSha256") != _digest(quality)
    ):
        raise ValueError("portable semantic proposal record digest is stale")
    if (
        proposal.get("proposalSha256") != record.get("proposalSha256")
        or receipt.get("receiptSha256") != record.get("providerReceiptSha256")
        or proposal.get("provider", {}).get("receiptSha256") != record.get("providerReceiptSha256")
        or quality.get("proposalSha256") != record.get("proposalSha256")
        or quality.get("status") != record.get("qualityStatus")
        or quality.get("status") == "rejected"
    ):
        raise ValueError("portable semantic proposal embedded digest binding is stale")
    if any(
        embedded.get("candidateId") != candidate_id
        or embedded.get("sourceBundleSha256") != source_digest
        for embedded in (proposal, quality)
    ):
        raise ValueError("portable semantic proposal embedded source binding is stale")
    expected_privacy = {
        "rawPromptsPersisted": False,
        "rawProviderResponsesPersisted": False,
        "chainOfThoughtPersisted": False,
        "credentialsPersisted": False,
        "providerLocalPathsPersisted": False,
    }
    if record.get("privacy") != expected_privacy:
        raise ValueError("portable semantic proposal privacy boundary is invalid")
    if record.get("executionBoundary") != {
        "providerInvokedDuringPortability": False,
        "materializationPerformed": False,
        "specpmMutated": False,
        "registryMutated": False,
        "publicationPerformed": False,
    }:
        raise ValueError("portable semantic proposal execution boundary is invalid")


def _validate_receipt(receipt: dict[str, Any]) -> None:
    if set(receipt) - RECEIPT_KEYS or not REQUIRED_RECEIPT_KEYS <= set(receipt):
        raise ValueError("portable semantic proposal receipt fields are invalid")
    if any(
        receipt.get(key) is not False
        for key in ("rawPromptPersisted", "rawResponsePersisted", "chainOfThoughtPersisted")
    ):
        raise ValueError("portable semantic proposal receipt violates privacy boundary")
    if _contains_machine_local_path(receipt):
        raise ValueError("portable semantic proposal receipt contains a provider-local path")


def _contains_machine_local_path(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_machine_local_path(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_machine_local_path(item) for item in value)
    return isinstance(value, str) and any(
        value.startswith(prefix) for prefix in MACHINE_LOCAL_PREFIXES
    )


def _read_json_object(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise ValueError(f"portable semantic proposal input cannot be a symlink: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read portable semantic proposal input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"portable semantic proposal input must be an object: {path}")
    return value


def _digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _digest_without(value: dict[str, Any], key: str) -> str:
    return _digest({name: item for name, item in value.items() if name != key})
