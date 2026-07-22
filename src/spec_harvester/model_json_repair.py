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


class ModelJsonParseError(ValueError):
    """Raised when model output cannot be parsed as a JSON object."""


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
) -> ModelJsonCompletion | ModelJsonFailure:
    repair_bound = max(0, max_repair_attempts)
    raw_content, response_payload = send_messages(initial_messages(system_prompt, request))
    responses = [(raw_content, response_payload)]
    try:
        return ModelJsonCompletion(
            payload=parse_model_json_object(raw_content),
            raw_content=raw_content,
            response_payload=response_payload,
            usage=sum_usage(responses),
            repair_needed=False,
            repair_attempt_count=0,
            repair_status="not_needed",
        )
    except ModelJsonParseError:
        pass

    latest_raw = raw_content
    latest_payload = response_payload
    for attempt in range(1, repair_bound + 1):
        latest_raw, latest_payload = send_messages(repair_messages(request, latest_raw, attempt))
        responses.append((latest_raw, latest_payload))
        try:
            return ModelJsonCompletion(
                payload=parse_model_json_object(latest_raw),
                raw_content=latest_raw,
                response_payload=latest_payload,
                usage=sum_usage(responses),
                repair_needed=True,
                repair_attempt_count=attempt,
                repair_status="repaired",
            )
        except ModelJsonParseError:
            continue

    return ModelJsonFailure(
        raw_content=latest_raw,
        response_payload=latest_payload,
        usage=sum_usage(responses),
        repair_needed=True,
        repair_attempt_count=repair_bound,
        repair_status="exhausted",
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
) -> list[dict[str, str]]:
    payload = {
        "task": "repair_invalid_json_model_output",
        "attempt": attempt,
        "instructions": [
            "Return exactly one valid JSON object.",
            "Preserve only claims supported by the supplied evidence paths.",
            "Do not add prose, markdown fences, comments, or chain-of-thought.",
            "Do not claim package acceptance, relation acceptance, or registry publication.",
        ],
        "requiredJsonShape": request.get("requiredJsonShape"),
        "allowedEvidencePaths": request.get("allowedEvidencePaths", []),
        "invalidModelOutput": invalid_output[:MAX_REPAIR_INPUT_CHARS],
        "truncatedInvalidModelOutput": len(invalid_output) > MAX_REPAIR_INPUT_CHARS,
    }
    return [
        {
            "role": "system",
            "content": "Repair malformed model output into valid JSON only.",
        },
        {"role": "user", "content": json.dumps(payload, sort_keys=True)},
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
