from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

DEFAULT_JSON_REPAIR_MAX_ATTEMPTS = 1
MAX_REPAIR_INPUT_CHARS = 24_000
LM_STUDIO_JSON_SCHEMA_NAME = "spec_harvester_json_object"


@dataclass(frozen=True)
class ModelJsonCompletion:
    payload: dict[str, Any]
    raw_content: str
    response_payload: dict[str, Any]
    usage: dict[str, Any]
    repair_needed: bool
    repair_attempt_count: int
    repair_status: str


@dataclass(frozen=True)
class ModelJsonFailure:
    raw_content: str
    response_payload: dict[str, Any]
    usage: dict[str, Any]
    repair_needed: bool
    repair_attempt_count: int
    repair_status: str
    failure_reason: str
    violation_code: str | None = None
    unchanged_semantic_violation: bool = False


class ModelJsonParseError(ValueError):
    """Raised when model output cannot be parsed as a JSON object."""


class ModelJsonConformanceError(ValueError):
    """Raised when parsed model JSON does not satisfy a caller contract."""


class ModelJsonSemanticViolation(ModelJsonConformanceError):
    """A stable semantic failure that can safely guide one bounded repair."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        prohibited_values: list[str] | None = None,
        replacement_constraints: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        if not re.fullmatch(r"[a-z][a-z0-9_]{2,79}", code):
            raise ValueError("semantic violation code is invalid")
        self.code = code
        self.prohibited_values = sorted(set(prohibited_values or []))[:64]
        self.replacement_constraints = dict(replacement_constraints or {})

    def repair_guidance(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "prohibitedValues": self.prohibited_values,
            "replacementConstraints": self.replacement_constraints,
        }


def openai_compatible_json_response_format(provider_name: str) -> dict[str, Any] | None:
    """Return LM Studio's request-side JSON-object constraint when applicable."""
    normalized_name = re.sub(r"[\s-]+", "_", provider_name.strip().lower())
    if normalized_name != "lm_studio":
        return None
    return {
        "type": "json_schema",
        "json_schema": {
            "name": LM_STUDIO_JSON_SCHEMA_NAME,
            "schema": {
                "type": "object",
                "additionalProperties": True,
            },
        },
    }


def complete_json_with_repair(
    *,
    request: dict[str, Any],
    system_prompt: str,
    send_messages: Callable[[list[dict[str, str]]], tuple[str, dict[str, Any]]],
    max_repair_attempts: int,
    normalize_payload: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    validate_payload: Callable[[dict[str, Any]], None] | None = None,
) -> ModelJsonCompletion | ModelJsonFailure:
    repair_bound = max(0, max_repair_attempts)
    raw_content, response_payload = send_messages(initial_messages(system_prompt, request))
    responses = [(raw_content, response_payload)]
    try:
        payload = _normalize_and_validate(
            parse_model_json_object(raw_content),
            normalize_payload=normalize_payload,
            validate_payload=validate_payload,
        )
        return ModelJsonCompletion(
            payload=payload,
            raw_content=raw_content,
            response_payload=response_payload,
            usage=sum_usage(responses),
            repair_needed=False,
            repair_attempt_count=0,
            repair_status="not_needed",
        )
    except (ModelJsonParseError, ModelJsonConformanceError) as exc:
        validation_error = str(exc)
        semantic_violation = _semantic_violation(exc)

    latest_raw = raw_content
    latest_payload = response_payload
    for attempt in range(1, repair_bound + 1):
        latest_raw, latest_payload = send_messages(
            repair_messages(
                request,
                latest_raw,
                attempt,
                system_prompt=system_prompt,
                validation_error=validation_error,
                semantic_violation=semantic_violation,
            )
        )
        responses.append((latest_raw, latest_payload))
        try:
            payload = _normalize_and_validate(
                parse_model_json_object(latest_raw),
                normalize_payload=normalize_payload,
                validate_payload=validate_payload,
            )
            return ModelJsonCompletion(
                payload=payload,
                raw_content=latest_raw,
                response_payload=latest_payload,
                usage=sum_usage(responses),
                repair_needed=True,
                repair_attempt_count=attempt,
                repair_status="repaired",
            )
        except (ModelJsonParseError, ModelJsonConformanceError) as exc:
            validation_error = str(exc)
            next_violation = _semantic_violation(exc)
            if (
                semantic_violation is not None
                and next_violation is not None
                and next_violation["code"] == semantic_violation["code"]
            ):
                return ModelJsonFailure(
                    raw_content=latest_raw,
                    response_payload=latest_payload,
                    usage=sum_usage(responses),
                    repair_needed=True,
                    repair_attempt_count=attempt,
                    repair_status="unchanged_semantic_violation",
                    failure_reason=validation_error,
                    violation_code=next_violation["code"],
                    unchanged_semantic_violation=True,
                )
            semantic_violation = next_violation
            continue

    return ModelJsonFailure(
        raw_content=latest_raw,
        response_payload=latest_payload,
        usage=sum_usage(responses),
        repair_needed=True,
        repair_attempt_count=repair_bound,
        repair_status="exhausted",
        failure_reason=validation_error,
        violation_code=(semantic_violation or {}).get("code"),
    )


def initial_messages(system_prompt: str, request: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(request, sort_keys=True)},
    ]


def repair_messages(
    request: dict[str, Any],
    invalid_output: str,
    attempt: int,
    *,
    system_prompt: str,
    validation_error: str | None = None,
    semantic_violation: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    bounded_output = invalid_output[:MAX_REPAIR_INPUT_CHARS]
    payload = {
        "task": "repair_invalid_json_model_output",
        "attempt": attempt,
        "instructions": [
            "Return exactly one valid JSON object.",
            "Preserve only claims supported by the supplied evidence paths.",
            "Do not add prose, markdown fences, comments, or chain-of-thought.",
            "Do not claim package acceptance, relation acceptance, or registry publication.",
        ],
        "allowedEvidencePaths": request.get("allowedEvidencePaths", []),
        "allowedEvidenceBindings": _repair_evidence_bindings(request),
        "observedIntentBindings": _repair_observed_intent_bindings(request),
        "validationError": validation_error,
        "semanticViolation": semantic_violation,
        "truncatedInvalidModelOutput": len(invalid_output) > MAX_REPAIR_INPUT_CHARS,
    }
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(request, sort_keys=True)},
        {"role": "assistant", "content": bounded_output},
        {"role": "user", "content": json.dumps(payload, sort_keys=True)},
    ]


def _normalize_and_validate(
    payload: dict[str, Any],
    *,
    normalize_payload: Callable[[dict[str, Any]], dict[str, Any]] | None,
    validate_payload: Callable[[dict[str, Any]], None] | None,
) -> dict[str, Any]:
    try:
        normalized = normalize_payload(payload) if normalize_payload else payload
    except ModelJsonSemanticViolation:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise ModelJsonConformanceError(str(exc)) from exc
    if not isinstance(normalized, dict):
        raise ModelJsonConformanceError("Model output normalization must return an object")
    if validate_payload:
        try:
            validate_payload(normalized)
        except ModelJsonSemanticViolation:
            raise
        except (KeyError, TypeError, ValueError) as exc:
            raise ModelJsonConformanceError(str(exc)) from exc
    return normalized


def _semantic_violation(exc: Exception) -> dict[str, Any] | None:
    return exc.repair_guidance() if isinstance(exc, ModelJsonSemanticViolation) else None


def _repair_evidence_bindings(request: dict[str, Any]) -> list[dict[str, Any]]:
    semantic_request = request.get("request")
    if not isinstance(semantic_request, dict):
        return []
    evidence = semantic_request.get("evidence")
    if not isinstance(evidence, list):
        return []
    fields = ("id", "class", "sourcePath", "sha256", "sourceBundleSha256")
    return [
        {field: item[field] for field in fields if field in item}
        for item in evidence
        if isinstance(item, dict)
    ]


def _repair_observed_intent_bindings(request: dict[str, Any]) -> list[dict[str, Any]]:
    observed = request.get("observedIntents")
    if not isinstance(observed, list):
        return []
    fields = ("intentId", "observedIntentSha256")
    return [
        {field: item[field] for field in fields if field in item}
        for item in observed
        if isinstance(item, dict)
    ]


def parse_model_json_object(raw_content: str) -> dict[str, Any]:
    text = raw_content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise ModelJsonParseError("Model output must be valid JSON") from exc
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError as fallback_exc:
            raise ModelJsonParseError("Model output must be valid JSON") from fallback_exc
    if not isinstance(payload, dict):
        raise ModelJsonParseError("Model output must be a JSON object")
    return payload


def sum_usage(responses: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    totals: dict[str, Any] = {}
    for _raw_content, response_payload in responses:
        usage = response_payload.get("usage")
        if not isinstance(usage, dict):
            continue
        for key, value in usage.items():
            if isinstance(value, int):
                totals[key] = int(totals.get(key, 0)) + value
    return totals
