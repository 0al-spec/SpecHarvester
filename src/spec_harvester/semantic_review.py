from __future__ import annotations

import hashlib
import json
from typing import Any

from jsonschema import Draft202012Validator

from spec_harvester.ai_semantic_author_schema import load_ai_semantic_author_schema
from spec_harvester.portable_semantic_proposal import validate_portable_semantic_proposal

MAX_EDITED_CLAIM_TEXT_BYTES = 16 * 1024


def _digest(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def reviewer_edit_sha256(value: dict[str, Any]) -> str:
    return _digest({key: item for key, item in value.items() if key != "reviewerEditSha256"})


def validate_semantic_reviewer_edit(reviewer_edit: dict[str, Any], record: dict[str, Any]) -> None:
    validate_portable_semantic_proposal(record)
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": "#/$defs/reviewerEdit",
        "$defs": load_ai_semantic_author_schema()["$defs"],
    }
    errors = list(Draft202012Validator(schema).iter_errors(reviewer_edit))
    if errors:
        raise ValueError(f"Semantic reviewer edit schema is invalid: {errors[0].message}")
    expected = {
        "proposalSha256": record["proposalSha256"],
        "sourceBundleSha256": record["sourceBundleSha256"],
        "semanticRecordSha256": record["recordSha256"],
    }
    if any(reviewer_edit.get(key) != value for key, value in expected.items()):
        raise ValueError("Semantic reviewer edit digest binding is stale")
    if reviewer_edit["reviewerEditSha256"] != reviewer_edit_sha256(reviewer_edit):
        raise ValueError("Semantic reviewer edit digest is invalid")

    claim_ids = {claim["id"] for claim in record["proposal"]["claims"]}
    accepted = reviewer_edit["acceptedOrEditedClaimIds"]
    if not set(accepted).issubset(claim_ids):
        raise ValueError("Semantic reviewer edit references an unknown claim")
    edits = reviewer_edit.get("editedClaims", [])
    edited_ids = [item["claimId"] for item in edits]
    if len(edited_ids) != len(set(edited_ids)):
        raise ValueError("Semantic reviewer edit contains duplicate edited claims")
    if not set(edited_ids).issubset(set(accepted)):
        raise ValueError("Edited semantic claim is not selected by the reviewer")
    if sum(len(item["text"].encode()) for item in edits) > MAX_EDITED_CLAIM_TEXT_BYTES:
        raise ValueError("Semantic reviewer edit text exceeds byte limit")

    decision = reviewer_edit["decision"]
    if decision in {"accepted", "edited"} and not accepted:
        raise ValueError("Accepted or edited semantic review requires selected claims")
    if decision == "edited" and not edits:
        raise ValueError("Edited semantic review requires edited claim text")
    if decision != "edited" and edits:
        raise ValueError("Only an edited semantic review may contain edited claim text")
    if decision in {"rejected", "deferred"} and accepted:
        raise ValueError("Rejected or deferred semantic review cannot select claims")


def build_semantic_reviewer_edit(
    action: dict[str, Any], record: dict[str, Any], reviewer: str
) -> dict[str, Any]:
    allowed = {
        "decision",
        "acceptedOrEditedClaimIds",
        "editedClaims",
        "proposalSha256",
        "sourceBundleSha256",
        "semanticRecordSha256",
    }
    if set(action) != allowed:
        raise ValueError("Semantic review action shape is invalid")
    reviewer_edit = {
        "apiVersion": "spec-harvester.ai-semantic-reviewer-edit/v0",
        "kind": "SpecHarvesterAISemanticReviewerEdit",
        "schemaVersion": 1,
        "authority": "reviewer_semantic_decision_evidence_only",
        "proposalSha256": action["proposalSha256"],
        "reviewerEditSha256": "0" * 64,
        "sourceBundleSha256": action["sourceBundleSha256"],
        "semanticRecordSha256": action["semanticRecordSha256"],
        "reviewer": reviewer,
        "decision": action["decision"],
        "acceptedOrEditedClaimIds": action["acceptedOrEditedClaimIds"],
    }
    if action["editedClaims"]:
        reviewer_edit["editedClaims"] = action["editedClaims"]
    reviewer_edit["reviewerEditSha256"] = reviewer_edit_sha256(reviewer_edit)
    validate_semantic_reviewer_edit(reviewer_edit, record)
    return reviewer_edit
