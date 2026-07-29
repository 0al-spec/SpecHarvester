from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_NAME = "ai-semantic-author-v0.schema.json"


def load_ai_semantic_author_schema() -> dict[str, Any]:
    """Load the packaged P55 semantic-author JSON Schema bundle."""
    try:
        payload = (
            files("spec_harvester").joinpath("schemas", SCHEMA_NAME).read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        source_path = Path(__file__).resolve().parents[2] / "schemas" / SCHEMA_NAME
        try:
            payload = source_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"Cannot read AI semantic-author schema: {exc}") from exc
    try:
        schema = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Cannot read AI semantic-author schema: {exc}") from exc
    if not isinstance(schema, dict):
        raise ValueError("AI semantic-author schema must be an object")
    return schema


def validate_semantic_author_fixture(payload: dict[str, Any]) -> None:
    """Validate record shape and P55-T2 cross-record evidence invariants."""
    schema = load_ai_semantic_author_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.absolute_path))
    if errors:
        raise ValueError(errors[0].message)

    request = payload["request"]
    proposal = payload["proposal"]
    source_bundle_digest = request["sourceBundleSha256"]
    request_evidence = {
        (
            evidence["id"],
            evidence["class"],
            evidence["sourcePath"],
            evidence["sha256"],
            evidence["sourceBundleSha256"],
        )
        for evidence in request["evidence"]
    }
    if any(evidence[4] != source_bundle_digest for evidence in request_evidence):
        raise ValueError("request evidence source bundle digest is stale")
    if proposal["candidateId"] != request["candidateId"]:
        raise ValueError("proposal candidate ID does not match request")
    if proposal["sourceBundleSha256"] != source_bundle_digest:
        raise ValueError("proposal source bundle digest is stale")

    for claim in proposal["claims"]:
        for evidence in claim["evidence"]:
            if evidence["sourceBundleSha256"] != source_bundle_digest:
                raise ValueError("claim evidence source bundle digest is stale")
            binding = (
                evidence["id"],
                evidence["class"],
                evidence["sourcePath"],
                evidence["sha256"],
                evidence["sourceBundleSha256"],
            )
            if binding not in request_evidence:
                raise ValueError("claim evidence is not in request allowlist")

    proposed_intent_ids = [
        record["intentId"]
        for record in proposal["intentDecisions"]
        if record["state"] == "proposed_experimental"
    ]
    if len(proposed_intent_ids) != len(set(proposed_intent_ids)):
        raise ValueError("duplicate proposed experimental intent ID")

    claim_ids = {claim["id"] for claim in proposal["claims"]}
    referenced_claim_ids = set()
    for record in proposal["intentDecisions"]:
        if record["state"] == "proposed_reuse":
            referenced_claim_ids.add(record["rationaleClaimId"])
        else:
            referenced_claim_ids.add(record["userNeedClaimId"])
            referenced_claim_ids.update(record["nonGoalClaimIds"])

    nearby_intent_analysis = payload["nearbyIntentAnalysis"]
    if nearby_intent_analysis["proposalSha256"] != proposal["proposalSha256"]:
        raise ValueError("nearby intent analysis proposal digest is stale")
    referenced_claim_ids.update(
        entry["differenceClaimId"] for entry in nearby_intent_analysis["entries"]
    )

    reviewer_edit = payload["reviewerEdit"]
    materialization = payload["materializationDecision"]
    for record, name in (
        (reviewer_edit, "reviewer edit"),
        (materialization, "materialization decision"),
    ):
        if record["sourceBundleSha256"] != source_bundle_digest:
            raise ValueError(f"{name} source bundle digest is stale")
        if record["proposalSha256"] != proposal["proposalSha256"]:
            raise ValueError(f"{name} proposal digest is stale")

    if materialization["reviewerEditSha256"] != reviewer_edit["reviewerEditSha256"]:
        raise ValueError("materialization decision reviewer edit digest is stale")
    if reviewer_edit["decision"] not in {"accepted", "edited"}:
        raise ValueError("materialization requires an accepted or edited reviewer decision")
    if materialization["decision"] not in {"accepted", "edited"}:
        raise ValueError("materialization decision requires accepted or edited reviewer decision")
    if materialization["decision"] != reviewer_edit["decision"]:
        raise ValueError("materialization decision does not match reviewer decision")
    if materialization["candidateId"] != request["candidateId"]:
        raise ValueError("materialization decision candidate ID does not match request")

    referenced_claim_ids.update(reviewer_edit["acceptedOrEditedClaimIds"])
    referenced_claim_ids.update(materialization["materializedClaimIds"])
    unknown_claim_ids = sorted(referenced_claim_ids - claim_ids)
    if unknown_claim_ids:
        raise ValueError(f"referenced claim ID is not present in proposal: {unknown_claim_ids[0]}")
    unapproved_materialized_claim_ids = sorted(
        set(materialization["materializedClaimIds"])
        - set(reviewer_edit["acceptedOrEditedClaimIds"])
    )
    if unapproved_materialized_claim_ids:
        raise ValueError(
            "materialized claim ID is not accepted or edited by reviewer: "
            f"{unapproved_materialized_claim_ids[0]}"
        )
