from __future__ import annotations

import json

from spec_harvester.model_json_repair import (
    MAX_REPAIR_INPUT_CHARS,
    ModelJsonCompletion,
    ModelJsonFailure,
    ModelJsonSemanticViolation,
    complete_json_with_repair,
    repair_messages,
)


def semantic_request() -> dict:
    return {
        "request": {
            "candidateId": "axios_axios.axios",
            "evidence": [
                {
                    "id": "evidence_readme",
                    "class": "allowlisted_source_documentation",
                    "sourcePath": "README.md",
                    "sha256": "a" * 64,
                    "sourceBundleSha256": "b" * 64,
                }
            ],
        },
        "evidence": [
            {
                "id": "evidence_readme",
                "sourcePath": "README.md",
                "content": "Promise based HTTP client for the browser and node.js",
            }
        ],
        "observedIntents": [
            {
                "intentId": "intent.package.javascript_library",
                "observedIntentSha256": "c" * 64,
            }
        ],
        "experimentalIntentDecisionPolicy": {"authority": "maintainer_bounded_proposal_policy"},
        "requiredJsonShape": {"type": "object"},
        "allowedEvidencePaths": ["README.md"],
    }


def test_repair_messages_preserve_original_semantic_context_and_roles() -> None:
    request = semantic_request()
    system_prompt = "Describe the concrete user outcome before implementation shape."
    invalid_output = "x" * (MAX_REPAIR_INPUT_CHARS + 100)

    messages = repair_messages(
        request,
        invalid_output,
        1,
        system_prompt=system_prompt,
        validation_error="generic reuse lacks comparison",
    )

    assert [message["role"] for message in messages] == [
        "system",
        "user",
        "assistant",
        "user",
    ]
    assert messages[0]["content"] == system_prompt
    assert json.loads(messages[1]["content"]) == request
    assert "Promise based HTTP client" in messages[1]["content"]
    assert messages[2]["content"] == invalid_output[:MAX_REPAIR_INPUT_CHARS]
    repair = json.loads(messages[3]["content"])
    assert repair["attempt"] == 1
    assert repair["validationError"] == "generic reuse lacks comparison"
    assert repair["truncatedInvalidModelOutput"] is True
    assert "invalidModelOutput" not in repair
    assert "requiredJsonShape" not in repair
    assert json.loads(messages[1]["content"])["requiredJsonShape"] == {"type": "object"}


def test_successful_repair_continues_original_request_context() -> None:
    request = semantic_request()
    calls: list[list[dict[str, str]]] = []

    def send_messages(messages: list[dict[str, str]]) -> tuple[str, dict]:
        calls.append(messages)
        if len(calls) == 1:
            return '{"status":"wrong"}', {"usage": {"total_tokens": 3}}
        return '{"status":"complete"}', {"usage": {"total_tokens": 5}}

    result = complete_json_with_repair(
        request=request,
        system_prompt="semantic system prompt",
        send_messages=send_messages,
        max_repair_attempts=1,
        validate_payload=lambda payload: (
            None
            if payload.get("status") == "complete"
            else (_ for _ in ()).throw(ValueError("status must be complete"))
        ),
    )

    assert isinstance(result, ModelJsonCompletion)
    assert result.repair_needed is True
    assert result.usage == {"total_tokens": 8}
    assert json.loads(calls[1][1]["content"])["evidence"] == request["evidence"]
    assert calls[1][2] == {"role": "assistant", "content": '{"status":"wrong"}'}


def test_exhausted_repair_retains_failure_without_persisting_context() -> None:
    request = semantic_request()

    result = complete_json_with_repair(
        request=request,
        system_prompt="semantic system prompt",
        send_messages=lambda _messages: ("not-json", {}),
        max_repair_attempts=1,
    )

    assert isinstance(result, ModelJsonFailure)
    assert result.raw_content == "not-json"
    assert result.repair_attempt_count == 1
    assert result.repair_status == "exhausted"
    assert "Promise based HTTP client" not in result.raw_content


def test_repair_carries_structured_semantic_violation_guidance() -> None:
    request = semantic_request()
    calls: list[list[dict[str, str]]] = []

    def send_messages(messages: list[dict[str, str]]) -> tuple[str, dict]:
        calls.append(messages)
        return '{"intentId":"intent.package.javascript_library"}', {}

    def reject_generic(_payload: dict) -> None:
        raise ModelJsonSemanticViolation(
            "specific_purpose_generic_only_contradiction",
            "specific purpose cannot use only a generic intent",
            prohibited_values=["intent.package.javascript_library"],
            replacement_constraints={"removeGenericOnlyReuse": True},
        )

    result = complete_json_with_repair(
        request=request,
        system_prompt="semantic system prompt",
        send_messages=send_messages,
        max_repair_attempts=3,
        validate_payload=reject_generic,
    )

    assert isinstance(result, ModelJsonFailure)
    assert len(calls) == 2
    assert result.repair_attempt_count == 1
    assert result.repair_status == "unchanged_semantic_violation"
    assert result.violation_code == "specific_purpose_generic_only_contradiction"
    assert result.unchanged_semantic_violation is True
    repair = json.loads(calls[1][-1]["content"])
    assert repair["semanticViolation"] == {
        "code": "specific_purpose_generic_only_contradiction",
        "prohibitedValues": ["intent.package.javascript_library"],
        "replacementConstraints": {"removeGenericOnlyReuse": True},
    }


def test_semantic_violation_rejects_unstable_code() -> None:
    try:
        ModelJsonSemanticViolation("INVALID-CODE", "bad")
    except ValueError as exc:
        assert str(exc) == "semantic violation code is invalid"
    else:
        raise AssertionError("invalid semantic violation code was accepted")
