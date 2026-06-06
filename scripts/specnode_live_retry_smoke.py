#!/usr/bin/env python3
"""Manual LM Studio live smoke for the SpecNode retry feedback loop."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from spec_harvester.specnode_refinement import (  # noqa: E402
    SPECNODE_SCHEMA_VERSION,
    SpecNodeModelJSONParseError,
    SpecNodeProviderUnavailable,
    SpecNodeRefinementRetryOptions,
    canonical_json_sha256_digest,
    parse_specnode_model_json_object,
    run_specnode_refinement_retry_orchestration,
    validate_specnode_refinement_retry_run,
)

RUN_FLAG_ENV = "SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE"
BASE_URL_ENV = "SPECHARVESTER_LM_STUDIO_BASE_URL"
MODEL_ENV = "SPECHARVESTER_SPECNODE_MODEL"
TIMEOUT_ENV = "SPECHARVESTER_LIVE_SMOKE_TIMEOUT_SECONDS"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_OUTPUT_TOKENS = 256
LOCAL_PROVIDER_HOSTS = {"localhost", "127.0.0.1", "::1"}


class LiveSmokeConfigError(ValueError):
    """Raised when live smoke configuration is incomplete."""


class LiveSmokeProviderError(RuntimeError):
    """Raised when the OpenAI-compatible endpoint cannot complete a smoke call."""


@dataclass(frozen=True)
class LiveSmokeConfig:
    base_url: str
    model: str
    timeout_seconds: float = 60.0
    temperature: float = DEFAULT_TEMPERATURE
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS

    @classmethod
    def from_env(
        cls,
        environ: dict[str, str] | None = None,
        *,
        require_run_flag: bool = False,
    ) -> LiveSmokeConfig:
        env = os.environ if environ is None else environ
        if require_run_flag and env.get(RUN_FLAG_ENV) != "1":
            raise LiveSmokeConfigError(f"set {RUN_FLAG_ENV}=1 to run live LM Studio smoke")
        base_url = env.get(BASE_URL_ENV, "").strip().rstrip("/")
        model = env.get(MODEL_ENV, "").strip()
        if not base_url:
            raise LiveSmokeConfigError(f"set {BASE_URL_ENV}, for example http://127.0.0.1:1234")
        if not model:
            raise LiveSmokeConfigError(f"set {MODEL_ENV}, for example openai/gpt-oss-20b")
        _validate_local_base_url(base_url)
        timeout = _parse_timeout_seconds(env.get(TIMEOUT_ENV, "60"))
        return cls(base_url=base_url, model=model, timeout_seconds=timeout)


@dataclass(frozen=True)
class ChatJSONResult:
    payload: dict[str, Any]
    raw_content: str
    model: str
    finish_reason: str | None
    usage: dict[str, Any]
    duration_ms: int


class OpenAICompatibleChatClient:
    def __init__(self, config: LiveSmokeConfig) -> None:
        self.config = config

    def chat_json(self, *, purpose: str, messages: list[dict[str, str]]) -> ChatJSONResult:
        started = time.monotonic()
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_output_tokens,
        }
        request = urllib.request.Request(
            f"{self.config.base_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise LiveSmokeProviderError(f"{purpose} request failed: {exc}") from exc

        try:
            choice = response_payload["choices"][0]
            raw_content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LiveSmokeProviderError(f"{purpose} response has unexpected shape") from exc
        if not isinstance(raw_content, str):
            raise LiveSmokeProviderError(f"{purpose} response content must be a string")

        try:
            parsed = parse_specnode_model_json_object(raw_content)
        except SpecNodeModelJSONParseError as exc:
            raise LiveSmokeProviderError(f"{purpose} response JSON parse failed: {exc}") from exc
        return ChatJSONResult(
            payload=parsed,
            raw_content=raw_content,
            model=str(response_payload.get("model") or self.config.model),
            finish_reason=choice.get("finish_reason"),
            usage=(
                response_payload.get("usage")
                if isinstance(response_payload.get("usage"), dict)
                else {}
            ),
            duration_ms=int((time.monotonic() - started) * 1000),
        )


class LMStudioRefinementProvider:
    def __init__(self, client: OpenAICompatibleChatClient) -> None:
        self.client = client
        self.calls: list[dict[str, Any]] = []

    def refine(
        self,
        *,
        job: dict[str, Any],
        preview_plan: dict[str, Any],
    ) -> dict[str, Any]:
        attempt_index = int(job.get("retryContext", {}).get("attemptIndex", 0))
        retry_context_present = "retryContext" in job
        messages = [
            {
                "role": "system",
                "content": "Return exactly one JSON object and no prose.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "task": "SpecNode live refinement smoke",
                        "attemptIndex": attempt_index,
                        "retryContextPresent": retry_context_present,
                        "candidate": preview_plan.get("candidate", {}),
                        "draftCandidateMetadata": preview_plan.get(
                            "compactModelInput", {}
                        ).get("draftCandidateMetadata", {}),
                        "requiredOutput": {
                            "decision": "propose",
                            "summary": "short target-package behavior summary",
                        },
                    },
                    sort_keys=True,
                ),
            },
        ]
        chat = self.client.chat_json(purpose="refinement", messages=messages)
        _require_payload_value(chat.payload, "decision", "propose", purpose="refinement")
        _require_payload_string(chat.payload, "summary", purpose="refinement")
        self.calls.append(
            {
                "attemptIndex": attempt_index,
                "retryContextPresent": retry_context_present,
                "payload": chat.payload,
                "usage": chat.usage,
            }
        )
        return build_live_refinement_result(
            job=job,
            preview_plan=preview_plan,
            chat=chat,
            config=self.client.config,
            endpoint="chat.completions/refine",
            attempt_index=attempt_index,
        )


class LMStudioSemanticReviewer:
    def __init__(self, client: OpenAICompatibleChatClient) -> None:
        self.client = client
        self.calls: list[dict[str, Any]] = []

    def review(
        self,
        *,
        review_job: dict[str, Any],
        preview_plan: dict[str, Any],
        refinement_result: dict[str, Any],
    ) -> dict[str, Any]:
        del preview_plan
        review_index = len(self.calls)
        expected_verdict = "needs_revision" if review_index == 0 else "approve"
        messages = [
            {
                "role": "system",
                "content": "Return exactly one JSON object and no prose.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "task": "SpecNode clean-context semantic review smoke",
                        "reviewIndex": review_index,
                        "expectedVerdict": expected_verdict,
                        "reviewedResultKind": refinement_result.get("result", {}).get("kind"),
                        "requiredOutput": {
                            "verdict": expected_verdict,
                            "summary": "short review summary",
                        },
                    },
                    sort_keys=True,
                ),
            },
        ]
        chat = self.client.chat_json(purpose="semantic-review", messages=messages)
        _require_payload_value(
            chat.payload,
            "verdict",
            expected_verdict,
            purpose="semantic-review",
        )
        _require_payload_string(chat.payload, "summary", purpose="semantic-review")
        self.calls.append(
            {
                "reviewIndex": review_index,
                "expectedVerdict": expected_verdict,
                "modelVerdict": chat.payload.get("verdict"),
                "usage": chat.usage,
            }
        )
        return build_live_semantic_review_result(
            review_job=review_job,
            refinement_result=refinement_result,
            chat=chat,
            verdict=expected_verdict,
            review_index=review_index,
        )


def run_live_retry_smoke(config: LiveSmokeConfig) -> dict[str, Any]:
    client = OpenAICompatibleChatClient(config)
    with tempfile.TemporaryDirectory(prefix="specharvester-live-smoke-") as tmp:
        candidate = create_live_smoke_candidate_workspace(Path(tmp))
        provider = LMStudioRefinementProvider(client)
        reviewer = LMStudioSemanticReviewer(client)
        run = run_specnode_refinement_retry_orchestration(
            SpecNodeRefinementRetryOptions(
                candidate_workspace=candidate,
                provider=provider,
                reviewer=reviewer,
                max_attempts=2,
            )
        )
        from spec_harvester.specnode_refinement import (  # noqa: PLC0415
            build_refine_preview_plan,
            build_specnode_artifact_bundle,
        )

        bundle = build_specnode_artifact_bundle(candidate)
        preview_plan = build_refine_preview_plan(bundle, candidate)
        validate_specnode_refinement_retry_run(run, bundle=bundle, preview_plan=preview_plan)

    return summarize_live_retry_run(
        run=run,
        provider_calls=provider.calls,
        review_calls=reviewer.calls,
        config=config,
    )


def summarize_live_retry_run(
    *,
    run: dict[str, Any],
    provider_calls: list[dict[str, Any]],
    review_calls: list[dict[str, Any]],
    config: LiveSmokeConfig,
) -> dict[str, Any]:
    attempts = run.get("attempts", [])
    return {
        "status": run.get("status"),
        "model": config.model,
        "baseUrl": config.base_url,
        "attemptCount": len(attempts) if isinstance(attempts, list) else 0,
        "attemptStatuses": [
            attempt.get("status") for attempt in attempts if isinstance(attempt, dict)
        ],
        "reviewVerdicts": [call["expectedVerdict"] for call in review_calls],
        "retryContextSeenByProvider": [
            call["retryContextPresent"] for call in provider_calls
        ],
        "tokenUsage": _sum_usage([*provider_calls, *review_calls]),
        "finalRefinementResultDigest": run.get("finalRefinementResultDigest"),
        "finalSemanticReviewResultDigest": run.get("finalSemanticReviewResultDigest"),
    }


def build_live_refinement_result(
    *,
    job: dict[str, Any],
    preview_plan: dict[str, Any],
    chat: ChatJSONResult,
    config: LiveSmokeConfig,
    endpoint: str,
    attempt_index: int,
) -> dict[str, Any]:
    job_digest = canonical_json_sha256_digest(job)
    preview_digest = canonical_json_sha256_digest(preview_plan)
    bundle_digest = preview_plan["sourceBundle"]["digest"]
    source_artifacts = preview_plan["artifactDigests"]
    candidate = preview_plan["candidate"]
    base_digest = canonical_json_sha256_digest(candidate)
    response_digest = canonical_json_sha256_digest(
        {"content": chat.raw_content, "payload": chat.payload}
    )
    proposal_id = f"proposal-live-smoke-{attempt_index + 1:03d}"
    operation_id = "op-001"
    provider_receipt = _provider_receipt(
        config=config,
        endpoint=endpoint,
        request_id=f"live-refine-{attempt_index + 1:03d}",
        chat=chat,
        response_digest=response_digest,
        prompt_budget=preview_plan["promptBudget"],
    )
    provider_receipt_digest = canonical_json_sha256_digest(provider_receipt)
    usage_receipt = _usage_receipt(
        job_id=str(job["jobId"]),
        result_id_field="proposalId",
        result_id=proposal_id,
        config=config,
        chat=chat,
        provider_receipt=provider_receipt,
        provider_receipt_digest=provider_receipt_digest,
        response_digest=response_digest,
        prompt_budget=preview_plan["promptBudget"],
    )
    summary = str(chat.payload.get("summary") or "LM Studio live smoke proposal.")
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeRefinementResult",
        "job": {
            "kind": "SpecNodeRefinementJob",
            "jobId": job["jobId"],
            "digest": job_digest,
        },
        "result": {
            "kind": "candidatePatchProposal",
            "proposal": {
                "kind": "SpecNodeCandidatePatchProposal",
                "proposalId": proposal_id,
                "candidateId": candidate["packageId"],
                "candidateVersion": candidate["packageVersion"],
                "baseCandidateDigest": base_digest,
                "sourceJobDigest": job_digest,
                "sourcePreviewPlanDigest": preview_digest,
                "sourceArtifactDigests": source_artifacts,
                "operations": [
                    {
                        "operationId": operation_id,
                        "op": "replace_field",
                        "targetFile": candidate["specPaths"][0],
                        "targetPointer": "/intent/summary",
                        "expectedCurrentValueSha256": canonical_json_sha256_digest(
                            {"current": "summary"}
                        ),
                        "value": summary[:240],
                        "rationale": "Live smoke proposal generated from compact evidence.",
                        "evidenceRefs": ["harvest_snapshot", "public_interface_index"],
                        "confidence": 0.5,
                    }
                ],
                "provenance": {
                    "kind": "SpecNodeProposalProvenance",
                    "sourceJobDigest": job_digest,
                    "sourceBundleDigest": bundle_digest,
                    "sourcePreviewPlanDigest": preview_digest,
                    "sourceArtifactDigests": source_artifacts,
                    "baseCandidateDigest": base_digest,
                    "providerReceiptDigest": provider_receipt_digest,
                    "modelId": config.model,
                    "createdAt": "2026-05-22T00:00:00Z",
                    "policyDigest": canonical_json_sha256_digest(job["policy"]),
                    "promptBudget": preview_plan["promptBudget"],
                    "redactionPolicy": "path_digest_and_summary_only",
                    "schemaVersion": SPECNODE_SCHEMA_VERSION,
                },
                "validationExpectations": {
                    "requiresSchemaValidation": True,
                    "requiresHumanReview": True,
                    "requiresSpecPMValidationAfterApply": True,
                },
            },
        },
        "reviewNotes": [
            {
                "noteId": f"live-note-{attempt_index + 1:03d}",
                "severity": "info",
                "message": "LM Studio live smoke returned compact JSON.",
                "evidenceRefs": ["harvest_snapshot"],
                "operationIds": [operation_id],
                "confidence": 0.5,
            }
        ],
        "usageReceipt": usage_receipt,
    }


def build_live_semantic_review_result(
    *,
    review_job: dict[str, Any],
    refinement_result: dict[str, Any],
    chat: ChatJSONResult,
    verdict: str,
    review_index: int,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    if verdict == "needs_revision":
        findings.append(
            {
                "kind": "SpecNodeSemanticReviewFinding",
                "findingId": "live-finding-001",
                "code": "unsupported_capability_claim",
                "severity": "warning",
                "message": "Live smoke intentionally requests one bounded retry.",
                "target": {
                    "kind": "candidate_patch_operation",
                    "operationId": "op-001",
                },
                "evidenceRefs": ["harvest_snapshot", "op-001"],
            }
        )
    return {
        "schemaVersion": SPECNODE_SCHEMA_VERSION,
        "kind": "SpecNodeSemanticReviewResult",
        "job": {
            "kind": "SpecNodeSemanticReviewJob",
            "jobId": review_job["jobId"],
            "digest": canonical_json_sha256_digest(review_job),
        },
        "reviewedRefinementResult": {
            "kind": "SpecNodeRefinementResult",
            "digest": canonical_json_sha256_digest(refinement_result),
        },
        "verdict": verdict,
        "findings": findings,
        "summary": str(
            chat.payload.get("summary")
            or f"LM Studio live semantic review smoke pass {review_index + 1}."
        )[:240],
    }


def create_live_smoke_candidate_workspace(root: Path) -> Path:
    candidate = root / "candidate"
    specs = candidate / "specs"
    specs.mkdir(parents=True)
    (candidate / "harvest.json").write_text(
        json.dumps(
            {
                "kind": "SpecHarvesterSnapshot",
                "source": {
                    "repository": "https://github.com/example/specnode-live-smoke",
                    "revision": "1" * 40,
                },
                "summary": {"fileCount": 3},
                "policy": {"mode": "manual-live-smoke"},
                "projectProfile": {
                    "kind": "ProjectProfile",
                    "languages": [{"name": "Python", "confidence": 0.9}],
                    "ecosystems": [{"name": "pypi", "confidence": 0.8}],
                    "evidencePaths": ["pyproject.toml", "src/specnode_live_smoke/app.py"],
                },
                "files": [
                    {
                        "path": "pyproject.toml",
                        "kind": "package_manifest",
                        "package": {
                            "ecosystem": "pypi",
                            "name": "specnode-live-smoke",
                            "version": "1.0.0",
                            "description": "Synthetic live smoke fixture.",
                        },
                        "semanticHints": ["routing", "middleware", "api"],
                    }
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (candidate / "specpm.yaml").write_text(
        "\n".join(
            [
                "metadata:",
                "  id: specnode_live_smoke.core",
                "  name: SpecNode Live Smoke",
                "  version: 1.0.0",
                "  summary: Synthetic package for live retry smoke.",
                "  license: MIT",
                "specs:",
                "  - path: specs/specnode_live_smoke.spec.yaml",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (specs / "specnode_live_smoke.spec.yaml").write_text(
        "\n".join(
            [
                "id: specnode-live-smoke-boundary",
                "intent:",
                "  summary: intent.web.routing_surface",
                "capabilities:",
                "  - id: specnode_live_smoke.core.routing",
                "evidence:",
                "  - id: semantic-routing-evidence",
                "    kind: documentation",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (candidate / "public-interface-index.json").write_text(
        json.dumps(
            {
                "kind": "PublicInterfaceIndex",
                "summary": {"symbolCount": 2},
                "analyzers": [{"name": "synthetic-live-smoke"}],
                "packages": [
                    {
                        "name": "specnode_live_smoke",
                        "symbols": [
                            {
                                "name": "DemoApp.route",
                                "kind": "method",
                                "signature": "route(path)",
                                "path": "src/specnode_live_smoke/app.py",
                            },
                            {
                                "name": "DemoApp.middleware",
                                "kind": "method",
                                "signature": "middleware(callback)",
                                "path": "src/specnode_live_smoke/app.py",
                            },
                        ],
                    }
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return candidate


def _provider_receipt(
    *,
    config: LiveSmokeConfig,
    endpoint: str,
    request_id: str,
    chat: ChatJSONResult,
    response_digest: str,
    prompt_budget: dict[str, Any],
) -> dict[str, Any]:
    return {
        "kind": "SpecNodeProviderUsageReceipt",
        "providerKind": "openai_compatible",
        "providerName": "lm_studio_live_smoke",
        "baseUrl": config.base_url,
        "endpoint": endpoint,
        "modelId": config.model,
        "requestId": request_id,
        "startedAt": "2026-05-22T00:00:00Z",
        "completedAt": "2026-05-22T00:00:00Z",
        "durationMs": chat.duration_ms,
        "status": "ok",
        "attempts": 1,
        "timeoutPolicy": {"totalTimeoutSeconds": config.timeout_seconds},
        "retryPolicy": {"maxAttempts": 1},
        "temperature": config.temperature,
        "maxOutputTokens": config.max_output_tokens,
        "promptBudget": prompt_budget,
        "inputTokens": int(chat.usage.get("prompt_tokens", 0)),
        "outputTokens": int(chat.usage.get("completion_tokens", 0)),
        "totalTokens": int(chat.usage.get("total_tokens", 0)),
        "finishReason": chat.finish_reason or "unknown",
        "responseSha256": response_digest,
        "redactionPolicy": "path_digest_and_summary_only",
    }


def _usage_receipt(
    *,
    job_id: str,
    result_id_field: str,
    result_id: str,
    config: LiveSmokeConfig,
    chat: ChatJSONResult,
    provider_receipt: dict[str, Any],
    provider_receipt_digest: str,
    response_digest: str,
    prompt_budget: dict[str, Any],
) -> dict[str, Any]:
    return {
        "kind": "SpecNodeProposalUsageReceipt",
        "jobId": job_id,
        result_id_field: result_id,
        "providerReceipt": provider_receipt,
        "providerReceiptDigest": provider_receipt_digest,
        "modelId": config.model,
        "inputTokens": int(chat.usage.get("prompt_tokens", 0)),
        "outputTokens": int(chat.usage.get("completion_tokens", 0)),
        "totalTokens": int(chat.usage.get("total_tokens", 0)),
        "finishReason": chat.finish_reason or "unknown",
        "attempts": 1,
        "startedAt": "2026-05-22T00:00:00Z",
        "completedAt": "2026-05-22T00:00:00Z",
        "durationMs": chat.duration_ms,
        "timeoutPolicy": {"totalTimeoutSeconds": config.timeout_seconds},
        "retryPolicy": {"maxAttempts": 1},
        "temperature": config.temperature,
        "maxOutputTokens": config.max_output_tokens,
        "promptBudget": prompt_budget,
        "responseSha256": response_digest,
        "redactionPolicy": "path_digest_and_summary_only",
    }


def _sum_usage(calls: list[dict[str, Any]]) -> dict[str, int]:
    totals = {"promptTokens": 0, "completionTokens": 0, "totalTokens": 0}
    for call in calls:
        usage = call.get("usage") if isinstance(call.get("usage"), dict) else {}
        totals["promptTokens"] += int(usage.get("prompt_tokens", 0))
        totals["completionTokens"] += int(usage.get("completion_tokens", 0))
        totals["totalTokens"] += int(usage.get("total_tokens", 0))
    return totals


def _validate_local_base_url(base_url: str) -> None:
    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in LOCAL_PROVIDER_HOSTS:
        raise LiveSmokeConfigError(
            f"{BASE_URL_ENV} must target a local provider host: "
            f"{', '.join(sorted(LOCAL_PROVIDER_HOSTS))}"
        )
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        raise LiveSmokeConfigError(f"{BASE_URL_ENV} must not include path, query, or fragment")


def _parse_timeout_seconds(value: str | float) -> float:
    try:
        timeout = float(value)
    except (TypeError, ValueError) as exc:
        raise LiveSmokeConfigError(f"{TIMEOUT_ENV} must be a number") from exc
    if timeout <= 0:
        raise LiveSmokeConfigError(f"{TIMEOUT_ENV} must be greater than zero")
    return timeout


def _require_payload_value(
    payload: dict[str, Any],
    field: str,
    expected: str,
    *,
    purpose: str,
) -> None:
    if payload.get(field) != expected:
        raise LiveSmokeProviderError(
            f"{purpose} response must include {field}={expected!r}, got {payload.get(field)!r}"
        )


def _require_payload_string(payload: dict[str, Any], field: str, *, purpose: str) -> None:
    if not isinstance(payload.get(field), str) or not payload[field].strip():
        raise LiveSmokeProviderError(f"{purpose} response must include non-empty {field}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=os.environ.get(BASE_URL_ENV, ""))
    parser.add_argument("--model", default=os.environ.get(MODEL_ENV, ""))
    parser.add_argument(
        "--timeout-seconds",
        default=os.environ.get(TIMEOUT_ENV, "60"),
    )
    args = parser.parse_args(argv)
    try:
        timeout_seconds = _parse_timeout_seconds(args.timeout_seconds)
        config = LiveSmokeConfig(
            base_url=args.base_url.strip().rstrip("/"),
            model=args.model.strip(),
            timeout_seconds=timeout_seconds,
        )
        if not config.base_url or not config.model:
            raise LiveSmokeConfigError(
                f"set {BASE_URL_ENV} and {MODEL_ENV}, or pass --base-url and --model"
            )
        _validate_local_base_url(config.base_url)
        summary = run_live_retry_smoke(config)
    except (LiveSmokeConfigError, LiveSmokeProviderError, SpecNodeProviderUnavailable) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
