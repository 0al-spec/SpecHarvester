from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from spec_harvester.ai_semantic_author_schema import (
    SCHEMA_NAME,
    load_ai_semantic_author_schema,
    validate_semantic_author_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / SCHEMA_NAME
VALID = ROOT / "tests/fixtures/ai_semantic_author_schemas/p55-t2-valid.example.json"
INVALID = ROOT / "tests/fixtures/ai_semantic_author_schemas/p55-t2-invalid.example.json"
SOURCE_CONTRACT = (
    ROOT / "tests/fixtures/ai_semantic_author_contract/"
    "p55-t1-ai-semantic-author-contract.example.json"
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def set_path(value: dict[str, Any], path: list[str | int], replacement: Any) -> None:
    target: Any = value
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = replacement


def test_schema_loader_returns_packaged_contract() -> None:
    schema = load_ai_semantic_author_schema()

    assert schema["$id"].endswith(SCHEMA_NAME)
    assert {
        "request",
        "proposal",
        "observedIntent",
        "reviewerEdit",
        "materializationDecision",
    } <= set(schema["$defs"])


def test_valid_fixture_covers_all_semantic_author_records() -> None:
    payload = load(VALID)

    Draft202012Validator.check_schema(load(SCHEMA))
    Draft202012Validator(load(SCHEMA), format_checker=FormatChecker()).validate(payload)
    validate_semantic_author_fixture(payload)

    assert (
        payload["sourceContract"]["sha256"]
        == hashlib.sha256(SOURCE_CONTRACT.read_bytes()).hexdigest()
    )
    assert payload["proposal"]["provider"]["id"] == "gpt-5.3-codex-spark"
    assert payload["observedIntents"][0]["state"] == "observed"
    assert payload["proposal"]["intentDecisions"][1]["intentId"].startswith("intent.experimental.")
    assert payload["materializationDecision"]["previewOnly"] is True
    assert payload["materializationDecision"]["isRegistryTruth"] is False


def test_invalid_fixtures_reject_shape_and_cross_record_drift() -> None:
    base = load(VALID)
    schema_validator = Draft202012Validator(load(SCHEMA), format_checker=FormatChecker())

    for case in load(INVALID):
        payload = copy.deepcopy(base)
        if case["kind"] == "duplicate_experimental_intent":
            payload["proposal"]["intentDecisions"].append(
                copy.deepcopy(payload["proposal"]["intentDecisions"][1])
            )
            with pytest.raises(ValueError, match="duplicate proposed experimental intent ID"):
                validate_semantic_author_fixture(payload)
            continue

        set_path(payload, case["path"], case["value"])
        if case["kind"] == "schema":
            assert list(schema_validator.iter_errors(payload)), case["case"]
        else:
            with pytest.raises(ValueError, match="source bundle digest is stale"):
                validate_semantic_author_fixture(payload)


@pytest.mark.parametrize(
    ("path", "message"),
    [
        (["proposal", "sourceBundleSha256"], "proposal source bundle digest is stale"),
        (
            ["proposal", "claims", 0, "evidence", 0, "sourceBundleSha256"],
            "claim evidence source bundle digest is stale",
        ),
        (["reviewerEdit", "proposalSha256"], "reviewer edit proposal digest is stale"),
        (
            ["materializationDecision", "reviewerEditSha256"],
            "materialization decision reviewer edit digest is stale",
        ),
        (
            ["nearbyIntentAnalysis", "proposalSha256"],
            "nearby intent analysis proposal digest is stale",
        ),
    ],
)
def test_cross_record_digest_drift_is_rejected(path: list[str | int], message: str) -> None:
    payload = copy.deepcopy(load(VALID))
    set_path(payload, path, "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

    with pytest.raises(ValueError, match=message):
        validate_semantic_author_fixture(payload)


@pytest.mark.parametrize(
    ("path", "message"),
    [
        (["proposal", "candidateId"], "proposal candidate ID does not match request"),
        (
            ["materializationDecision", "candidateId"],
            "materialization decision candidate ID does not match request",
        ),
        (
            ["nearbyIntentAnalysis", "entries", 0, "differenceClaimId"],
            "referenced claim ID is not present in proposal",
        ),
    ],
)
def test_cross_record_identity_and_claim_references_are_rejected(
    path: list[str | int], message: str
) -> None:
    payload = copy.deepcopy(load(VALID))
    set_path(payload, path, "missing_claim" if "claim" in message else "other-candidate")

    with pytest.raises(ValueError, match=message):
        validate_semantic_author_fixture(payload)


def test_schema_errors_are_reported_by_cross_record_validator() -> None:
    payload = copy.deepcopy(load(VALID))
    payload["request"]["evidence"][0]["class"] = "unsupported"

    with pytest.raises(ValueError, match="unsupported"):
        validate_semantic_author_fixture(payload)


def test_proposal_requires_complete_semantic_sections_and_an_intent_decision() -> None:
    payload = copy.deepcopy(load(VALID))
    schema_validator = Draft202012Validator(load(SCHEMA), format_checker=FormatChecker())
    payload["proposal"]["claims"] = [payload["proposal"]["claims"][0]]
    payload["proposal"]["intentDecisions"] = []

    assert list(schema_validator.iter_errors(payload))


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("request_evidence_stale", "request evidence source bundle digest is stale"),
        ("claim_evidence_fabricated", "claim evidence is not in request allowlist"),
        (
            "reviewer_rejected",
            "materialization requires an accepted or edited reviewer decision",
        ),
        ("reviewer_decision_mismatch", "materialization decision does not match reviewer decision"),
        (
            "unapproved_materialized_claim",
            "materialized claim ID is not accepted or edited by reviewer",
        ),
    ],
)
def test_allowlist_and_reviewer_authority_are_enforced(mutation: str, message: str) -> None:
    payload = copy.deepcopy(load(VALID))
    if mutation == "request_evidence_stale":
        payload["request"]["evidence"][0]["sourceBundleSha256"] = "e" * 64
    elif mutation == "claim_evidence_fabricated":
        payload["proposal"]["claims"][0]["evidence"][0]["sourcePath"] = "docs/forged.md"
    elif mutation == "reviewer_rejected":
        payload["reviewerEdit"]["decision"] = "rejected"
    elif mutation == "reviewer_decision_mismatch":
        payload["reviewerEdit"]["decision"] = "accepted"
    else:
        payload["reviewerEdit"]["acceptedOrEditedClaimIds"].remove("interface_cli")
        payload["materializationDecision"]["materializedClaimIds"] = ["interface_cli"]

    with pytest.raises(ValueError, match=message):
        validate_semantic_author_fixture(payload)


def test_schema_has_no_provider_prompt_or_registry_authority_fields() -> None:
    serialized = SCHEMA.read_text(encoding="utf-8")

    for forbidden in (
        "rawPrompt",
        "rawResponse",
        "hiddenReasoning",
        "credential",
        "privateMachinePath",
        "canonicalIntent",
        "registryMutation",
    ):
        assert forbidden not in serialized


def test_docs_describe_provider_neutral_proposal_only_schema_boundary() -> None:
    github_doc = (ROOT / "docs/AI_SEMANTIC_AUTHOR_SCHEMAS.md").read_text(encoding="utf-8")
    docc_doc = (
        ROOT / "Sources/SpecHarvester/Documentation.docc/AISemanticAuthorSchemas.md"
    ).read_text(encoding="utf-8")

    for text in (github_doc, docc_doc):
        normalized = " ".join(text.split())
        assert "provider-neutral" in normalized
        assert "intent.experimental.*" in normalized
        assert "P55-T1" in normalized
        assert "Codex 5.3 Spark" in normalized
        assert "LM Studio" in normalized
    assert "AI_SEMANTIC_AUTHOR_SCHEMAS.md" in (ROOT / "docs/CAPABILITIES.md").read_text(
        encoding="utf-8"
    )
    assert "<doc:AISemanticAuthorSchemas>" in (
        ROOT / "Sources/SpecHarvester/Documentation.docc/Capabilities.md"
    ).read_text(encoding="utf-8")
