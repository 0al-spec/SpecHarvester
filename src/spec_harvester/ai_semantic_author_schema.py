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
    if proposal["sourceBundleSha256"] != source_bundle_digest:
        raise ValueError("proposal source bundle digest is stale")

    for claim in proposal["claims"]:
        for evidence in claim["evidence"]:
            if evidence["sourceBundleSha256"] != source_bundle_digest:
                raise ValueError("claim evidence source bundle digest is stale")

    proposed_intent_ids = [
        record["intentId"]
        for record in proposal["intentDecisions"]
        if record["state"] == "proposed_experimental"
    ]
    if len(proposed_intent_ids) != len(set(proposed_intent_ids)):
        raise ValueError("duplicate proposed experimental intent ID")

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
    if materialization["decision"] not in {"accepted", "edited"}:
        raise ValueError("materialization decision requires accepted or edited reviewer decision")
