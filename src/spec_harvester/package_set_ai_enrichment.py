from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from spec_harvester.model_json_repair import (
    DEFAULT_JSON_REPAIR_MAX_ATTEMPTS,
    ModelJsonFailure,
    ModelJsonParseError,
    complete_json_with_repair,
)
from spec_harvester.model_json_repair import (
    parse_model_json_object as parse_model_json_object_shared,
)
from spec_harvester.package_set_drafter import (
    PACKAGE_RELATION_PROPOSALS_FILENAME,
    PACKAGE_SET_DRAFT_FILENAME,
)
from spec_harvester.producer_receipt import digest_record, sha256_file
from spec_harvester.producer_reports import stop_policy_summary_from_diagnostics

PACKAGE_SET_AI_ENRICHMENT_API_VERSION = "spec-harvester.package-set-ai-enrichment/v0"
PACKAGE_SET_AI_ENRICHMENT_KIND = "SpecHarvesterPackageSetAIEnrichmentProposal"
PACKAGE_SET_AI_ENRICHMENT_SCHEMA_VERSION = 1
MAX_EVIDENCE_TEXT_CHARS = 12_000
DEFAULT_TIMEOUT_SECONDS = 120.0
DEFAULT_MAX_OUTPUT_TOKENS = 2_200
DEFAULT_TEMPERATURE = 0.0
LOCAL_PROVIDER_HOSTS = {"localhost", "127.0.0.1", "::1"}

TRUST_BOUNDARY_NOTES = [
    "AI enrichment output is proposal evidence only.",
    "Model output cannot accept packages, accept relations, or publish registry metadata.",
    "SpecPM remains the validation, acceptance, relation, and registry authority.",
    "Evidence paths must refer to supplied deterministic package-set or allowlisted source files.",
    "Raw prompts, raw provider responses, secrets, and model chain-of-thought are not persisted.",
]


@dataclass(frozen=True)
class PackageSetAIEnrichmentOptions:
    bundle_set: Path
    source_checkout: Path | None = None
    provider_base_url: str | None = None
    provider_name: str = "lm_studio"
    model: str | None = None
    model_output: Path | None = None
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    json_repair_max_attempts: int = DEFAULT_JSON_REPAIR_MAX_ATTEMPTS


class PackageSetAIEnrichmentError(RuntimeError):
    """Raised when package-set AI enrichment cannot be completed."""


class OpenAICompatibleProvider:
    def __init__(
        self,
        *,
        base_url: str,
        provider_name: str,
        model: str,
        timeout_seconds: float,
        max_output_tokens: int,
        temperature: float,
        json_repair_max_attempts: int,
    ) -> None:
        self.base_url = normalize_local_provider_base_url(base_url)
        self.provider_name = provider_name
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.json_repair_max_attempts = json_repair_max_attempts

    def complete_json(self, request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        started = time.monotonic()
        system_prompt = (
            "Return exactly one valid JSON object and no prose. "
            "Do not invent facts not supported by evidence paths."
        )
        result = complete_json_with_repair(
            request=request,
            system_prompt=system_prompt,
            send_messages=self.send_messages,
            max_repair_attempts=self.json_repair_max_attempts,
        )
        raw_content = result.raw_content
        response_payload = result.response_payload
        receipt = {
            "providerKind": "openai_compatible",
            "providerName": self.provider_name,
            "baseUrl": self.base_url,
            "endpoint": "/v1/chat/completions",
            "modelId": str(response_payload.get("model") or self.model),
            "requestId": f"package-set-ai-enrichment-{request['packageId']}",
            "startedAt": utc_now(),
            "durationMs": int((time.monotonic() - started) * 1000),
            "temperature": self.temperature,
            "maxOutputTokens": self.max_output_tokens,
            "usage": result.usage,
            "jsonRepairNeeded": result.repair_needed,
            "jsonRepairAttemptCount": result.repair_attempt_count,
            "jsonRepairStatus": result.repair_status,
            "rawPromptPersisted": False,
            "rawResponsePersisted": False,
            "chainOfThoughtPersisted": False,
        }
        if isinstance(result, ModelJsonFailure):
            return {}, receipt
        receipt["responseDigest"] = sha256_text(raw_content)
        return result.payload, receipt

    def send_messages(self, messages: list[dict[str, str]]) -> tuple[str, dict[str, Any]]:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_output_tokens,
            "messages": messages,
        }
        http_request = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                http_request,
                timeout=self.timeout_seconds,
            ) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            raise PackageSetAIEnrichmentError(f"Provider request failed: {exc}") from exc

        try:
            choice = response_payload["choices"][0]
            raw_content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise PackageSetAIEnrichmentError("Provider response has unexpected shape") from exc
        if not isinstance(raw_content, str):
            raise PackageSetAIEnrichmentError("Provider response content must be a string")
        return raw_content, response_payload


def build_package_set_ai_enrichment_proposal(
    options: PackageSetAIEnrichmentOptions,
) -> dict[str, Any]:
    if options.json_repair_max_attempts < 0:
        raise ValueError("json_repair_max_attempts must be zero or greater")
    bundle_set = options.bundle_set.resolve()
    if not bundle_set.is_dir():
        raise ValueError(f"Package-set directory does not exist: {bundle_set}")
    if options.model_output is not None and (options.provider_base_url or options.model):
        raise ValueError("--model-output cannot be combined with provider execution options")

    draft = read_json_object(bundle_set / PACKAGE_SET_DRAFT_FILENAME)
    relations = read_json_object(bundle_set / PACKAGE_RELATION_PROPOSALS_FILENAME)
    members = member_records(draft)
    package_set_id = package_set_id_from_members(members)
    requests = [
        enrichment_request(
            bundle_set=bundle_set,
            member=member,
            source_checkout=options.source_checkout,
        )
        for member in members
    ]

    model_outputs: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    provider_record: dict[str, Any]
    if options.model_output is not None:
        model_outputs = model_outputs_from_file(options.model_output)
        provider_record = {
            "kind": "external_model_output",
            "name": "external",
            "model": None,
            "baseUrl": None,
            "execution": "not_run_by_spec_harvester",
        }
    else:
        if not options.provider_base_url or not options.model:
            raise ValueError("provider execution requires --provider-base-url and --model")
        provider = OpenAICompatibleProvider(
            base_url=options.provider_base_url,
            provider_name=options.provider_name,
            model=options.model,
            timeout_seconds=options.timeout_seconds,
            max_output_tokens=options.max_output_tokens,
            temperature=options.temperature,
            json_repair_max_attempts=options.json_repair_max_attempts,
        )
        provider_record = {
            "kind": "openai_compatible",
            "name": options.provider_name,
            "model": options.model,
            "baseUrl": provider.base_url,
            "execution": "operator_opt_in_local",
        }
        for request in requests:
            output, receipt = provider.complete_json(request)
            reported_package_id = string_value(output.get("packageId"))
            output = dict(output)
            output["packageId"] = request["packageId"]
            receipt["reportedPackageId"] = reported_package_id
            model_outputs[request["packageId"]] = (output, receipt)

    diagnostics: list[dict[str, Any]] = []
    proposals = []
    for request in requests:
        package_id = request["packageId"]
        model_output, provider_receipt = model_outputs.get(package_id, ({}, {}))
        reported_package_id = string_value(provider_receipt.get("reportedPackageId"))
        if reported_package_id and reported_package_id != package_id:
            diagnostics.append(
                diagnostic(
                    "warning",
                    "model_package_id_mismatch",
                    f"Model reported {reported_package_id}, but request package is {package_id}.",
                    package_id,
                    {"reportedPackageId": reported_package_id},
                )
            )
        proposals.append(
            package_proposal(
                package_id=package_id,
                request=request,
                model_output=model_output,
                provider_receipt=provider_receipt,
                diagnostics=diagnostics,
            )
        )

    error_count = sum(1 for item in diagnostics if item["severity"] == "error")
    warning_count = sum(1 for item in diagnostics if item["severity"] == "warning")
    status = "failed" if error_count else ("warning" if warning_count else "completed")
    return {
        "apiVersion": PACKAGE_SET_AI_ENRICHMENT_API_VERSION,
        "kind": PACKAGE_SET_AI_ENRICHMENT_KIND,
        "schemaVersion": PACKAGE_SET_AI_ENRICHMENT_SCHEMA_VERSION,
        "status": status,
        "authority": "proposal_only_not_registry_acceptance",
        "packageSet": {
            "id": package_set_id,
            "candidateCount": len(members),
            "relationCount": len(list_value(relations.get("relations"))),
        },
        "provider": provider_record,
        "inputs": input_records(bundle_set, options.source_checkout, requests),
        "proposals": proposals,
        "diagnostics": diagnostics,
        "summary": {
            "proposalCount": len(proposals),
            "errorCount": error_count,
            "warningCount": warning_count,
            "providerTotalTokens": sum_provider_usage(proposals, "total_tokens"),
            "providerPromptTokens": sum_provider_usage(proposals, "prompt_tokens"),
            "providerCompletionTokens": sum_provider_usage(proposals, "completion_tokens"),
        },
        "stopPolicySummary": stop_policy_summary_from_diagnostics(
            source_status=status,
            error_count=error_count,
            warning_count=warning_count,
            subject_count=len(proposals),
        ),
        "privacy": {
            "rawPromptsPersisted": False,
            "rawModelResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "secretsIncluded": False,
        },
        "trustBoundary": TRUST_BOUNDARY_NOTES,
        "nonGoals": [
            "specpm_acceptance",
            "package_acceptance",
            "relation_acceptance",
            "registry_publication",
            "model_authored_file_mutation",
        ],
    }


def write_package_set_ai_enrichment_proposal(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read JSON artifact {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON artifact {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return payload


def model_outputs_from_file(path: Path) -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    payload = read_json_object(path)
    raw_proposals = list_value(payload.get("proposals"))
    if not raw_proposals and payload.get("packageId"):
        raw_proposals = [payload]
    outputs = {}
    for item in raw_proposals:
        if isinstance(item, dict) and isinstance(item.get("packageId"), str):
            outputs[item["packageId"]] = (item, {"source": str(path), "execution": "external"})
    return outputs


def member_records(draft: dict[str, Any]) -> list[dict[str, Any]]:
    records = [item for item in list_value(draft.get("candidates")) if isinstance(item, dict)]
    return sorted(records, key=lambda item: str(item.get("packageId") or ""))


def package_set_id_from_members(members: list[dict[str, Any]]) -> str:
    for member in members:
        if member.get("role") == "workspace" and isinstance(member.get("packageId"), str):
            return member["packageId"]
    for member in members:
        if isinstance(member.get("packageId"), str):
            return member["packageId"]
    return "package-set"


def enrichment_request(
    *,
    bundle_set: Path,
    member: dict[str, Any],
    source_checkout: Path | None,
) -> dict[str, Any]:
    package_id = string_value(member.get("packageId"))
    candidate_path = string_value(member.get("candidatePath"))
    candidate_root = safe_bundle_path(bundle_set, candidate_path)
    evidence = candidate_evidence(candidate_root, member)
    if source_checkout is not None:
        evidence.extend(source_checkout_evidence(source_checkout, member))
    evidence_paths = [item["path"] for item in evidence]
    return {
        "task": "Create evidence-grounded SpecPM semantic enrichment proposal.",
        "packageId": package_id,
        "role": string_value(member.get("role")),
        "candidatePath": candidate_path,
        "requiredJsonShape": {
            "packageId": package_id,
            "refinedSummary": "one sentence",
            "capabilities": [
                {
                    "id": "stable capability id under package namespace",
                    "summary": "capability summary",
                    "intentIds": ["intent.*"],
                    "evidencePaths": ["path"],
                    "confidence": "high|medium|low",
                }
            ],
            "interfaces": [
                {
                    "id": "stable interface id",
                    "kind": "library|component|hook|utility|style_asset",
                    "summary": "interface summary",
                    "evidencePaths": ["path"],
                    "confidence": "high|medium|low",
                }
            ],
            "evidenceGaps": ["missing deterministic evidence"],
            "overallConfidence": "high|medium|low",
        },
        "constraints": [
            "Return proposal evidence only; do not claim registry acceptance.",
            "Use only supplied evidence paths.",
            "Prefer concrete product/API capabilities over generic labels.",
            (
                "Do not merely repeat current generated capability ids when they only "
                "restate the framework or package name."
            ),
            (
                "When evidence supports it, propose 2 to 6 distinct capabilities for "
                "product/API behavior."
            ),
            (
                "Use capability ids such as '<package>.flow_canvas' or "
                "'<package>.viewport_controls' instead of '<package>.react' or "
                "'<package>.system'."
            ),
            "Every capability and interface must include evidencePaths.",
        ],
        "allowedEvidencePaths": evidence_paths,
        "evidence": evidence,
    }


def candidate_evidence(candidate_root: Path | None, member: dict[str, Any]) -> list[dict[str, Any]]:
    if candidate_root is None:
        return []
    evidence = []
    for role, relative in (
        ("manifest", "specpm.yaml"),
        ("harvest_snapshot", "harvest.json"),
        ("boundary_spec", first_spec_path(candidate_root)),
    ):
        if not relative:
            continue
        record = evidence_record(
            root=candidate_root,
            relative=relative,
            role=role,
            path=f"{string_value(member.get('candidatePath'))}/{relative}",
        )
        if record is not None:
            evidence.append(record)
    return evidence


def first_spec_path(candidate_root: Path) -> str:
    specs = sorted((candidate_root / "specs").glob("*.spec.yaml"))
    if not specs:
        return ""
    return specs[0].relative_to(candidate_root).as_posix()


def source_checkout_evidence(source_checkout: Path, member: dict[str, Any]) -> list[dict[str, Any]]:
    root = source_checkout.resolve()
    source_target = string_value(member.get("sourceTargetPath")) or "."
    candidates = source_evidence_candidates(root, source_target)
    evidence = []
    seen: set[str] = set()
    for relative in candidates:
        if relative in seen:
            continue
        seen.add(relative)
        record = evidence_record(root=root, relative=relative, role=source_role(relative))
        if record is not None:
            evidence.append(record)
    return evidence


def source_evidence_candidates(root: Path, source_target: str) -> list[str]:
    target = "" if source_target == "." else source_target.strip("/")
    prefixes = [""] if not target else ["", target]
    candidates = []
    for prefix in prefixes:
        for name in ("package.json", "README.md", "readme.md"):
            candidates.append(join_posix(prefix, name))
    package_manifest = root / join_posix(target, "package.json")
    source_value = package_source_entry(package_manifest)
    if source_value:
        candidates.append(join_posix(target, source_value))
    for entry in (
        "src/index.ts",
        "src/index.tsx",
        "src/index.js",
        "src/lib/index.ts",
        "src/lib/index.js",
        "src/types/index.ts",
        "src/utils/index.ts",
    ):
        candidates.append(join_posix(target, entry))
    return [candidate for candidate in candidates if candidate]


def package_source_entry(package_manifest: Path) -> str:
    try:
        payload = json.loads(package_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    if not isinstance(payload, dict):
        return ""
    source = payload.get("source")
    if not isinstance(source, str):
        return ""
    source_path = Path(source)
    if source_path.is_absolute() or ".." in source_path.parts or "\\" in source:
        return ""
    return source_path.as_posix()


def evidence_record(
    *,
    root: Path,
    relative: str,
    role: str,
    path: str | None = None,
) -> dict[str, Any] | None:
    resolved_root = root.resolve()
    artifact = (resolved_root / relative).resolve()
    if not artifact.is_file() or not artifact.is_relative_to(resolved_root):
        return None
    try:
        text = artifact.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    public_path = path or relative
    return {
        "role": role,
        "path": public_path,
        "digest": digest_record(sha256_file(artifact)),
        "text": text[:MAX_EVIDENCE_TEXT_CHARS],
        "truncated": len(text) > MAX_EVIDENCE_TEXT_CHARS,
    }


def package_proposal(
    *,
    package_id: str,
    request: dict[str, Any],
    model_output: dict[str, Any],
    provider_receipt: dict[str, Any],
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any]:
    diagnostics.extend(json_repair_diagnostics(provider_receipt, package_id))
    allowed_paths = set(request["allowedEvidencePaths"])
    proposal = {
        "packageId": package_id,
        "status": "proposed" if model_output else "missing_model_output",
        "refinedSummary": string_value(model_output.get("refinedSummary")),
        "capabilities": normalized_records(
            package_id=package_id,
            records=list_value(model_output.get("capabilities")),
            allowed_paths=allowed_paths,
            diagnostics=diagnostics,
            field="capabilities",
            preserve_kind=False,
        ),
        "interfaces": normalized_records(
            package_id=package_id,
            records=list_value(model_output.get("interfaces")),
            allowed_paths=allowed_paths,
            diagnostics=diagnostics,
            field="interfaces",
            preserve_kind=True,
        ),
        "evidenceGaps": [
            item for item in list_value(model_output.get("evidenceGaps")) if isinstance(item, str)
        ],
        "overallConfidence": confidence_value(model_output.get("overallConfidence")),
        "providerReceipt": provider_receipt,
    }
    if not model_output:
        diagnostics.append(
            diagnostic(
                "error",
                "model_output_missing",
                f"No model enrichment output was produced for {package_id}.",
                package_id,
            )
        )
    if not proposal["refinedSummary"]:
        diagnostics.append(
            diagnostic(
                "warning",
                "refined_summary_missing",
                f"Model output for {package_id} did not include refinedSummary.",
                package_id,
            )
        )
    return proposal


def normalized_records(
    *,
    package_id: str,
    records: list[Any],
    allowed_paths: set[str],
    diagnostics: list[dict[str, Any]],
    field: str,
    preserve_kind: bool,
) -> list[dict[str, Any]]:
    normalized = []
    for index, item in enumerate(records):
        if not isinstance(item, dict):
            diagnostics.append(
                diagnostic(
                    "warning",
                    "model_record_invalid",
                    f"{field}[{index}] for {package_id} is not an object.",
                    package_id,
                )
            )
            continue
        evidence_paths = [
            normalized_evidence_path(package_id, path.strip(), allowed_paths)
            for path in list_value(item.get("evidencePaths"))
            if isinstance(path, str) and path.strip()
        ]
        supported_evidence_paths = [path for path in evidence_paths if path in allowed_paths]
        unsupported = sorted(set(evidence_paths) - allowed_paths)
        if unsupported:
            diagnostics.append(
                diagnostic(
                    "warning",
                    "model_evidence_path_unsupported",
                    f"{field}[{index}] for {package_id} cites unsupported evidence paths.",
                    package_id,
                    {"paths": unsupported},
                )
            )
        record = {
            "id": string_value(item.get("id")),
            "summary": string_value(item.get("summary")),
            "evidencePaths": supported_evidence_paths,
            "confidence": confidence_value(item.get("confidence")),
        }
        if preserve_kind:
            record["kind"] = string_value(item.get("kind"))
        else:
            record["intentIds"] = [
                x for x in list_value(item.get("intentIds")) if isinstance(x, str)
            ]
        normalized.append(record)
    return normalized


def normalized_evidence_path(package_id: str, path: str, allowed_paths: set[str]) -> str:
    if path in allowed_paths:
        return path
    if not path.startswith("/") and not path.startswith(f"{package_id}/"):
        candidate_relative = f"{package_id}/{path}"
        if candidate_relative in allowed_paths:
            return candidate_relative
    return path


def input_records(
    bundle_set: Path,
    source_checkout: Path | None,
    requests: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    for role, filename in (
        ("package_set_draft", PACKAGE_SET_DRAFT_FILENAME),
        ("package_relation_proposals", PACKAGE_RELATION_PROPOSALS_FILENAME),
    ):
        path = bundle_set / filename
        if path.is_file():
            records.append(
                {
                    "role": role,
                    "path": filename,
                    "pathScope": "bundle_relative",
                    "digest": digest_record(sha256_file(path)),
                }
            )
    if source_checkout is not None:
        records.append(
            {
                "role": "source_checkout",
                "path": str(source_checkout),
                "pathScope": "local_path",
            }
        )
    evidence_paths = sorted(
        {
            evidence["path"]
            for request in requests
            for evidence in list_value(request.get("evidence"))
            if isinstance(evidence, dict) and isinstance(evidence.get("path"), str)
        }
    )
    records.append(
        {
            "role": "compact_model_input",
            "packageCount": len(requests),
            "evidencePathCount": len(evidence_paths),
            "evidencePaths": evidence_paths,
        }
    )
    return records


def model_request_records(options: PackageSetAIEnrichmentOptions) -> list[dict[str, Any]]:
    bundle_set = options.bundle_set.resolve()
    draft = read_json_object(bundle_set / PACKAGE_SET_DRAFT_FILENAME)
    return [
        enrichment_request(
            bundle_set=bundle_set,
            member=member,
            source_checkout=options.source_checkout,
        )
        for member in member_records(draft)
    ]


def write_model_request_records(path: Path, requests: list[dict[str, Any]]) -> None:
    payload = {
        "apiVersion": PACKAGE_SET_AI_ENRICHMENT_API_VERSION,
        "kind": "SpecHarvesterPackageSetAIEnrichmentRequests",
        "schemaVersion": PACKAGE_SET_AI_ENRICHMENT_SCHEMA_VERSION,
        "requests": requests,
        "privacy": {
            "rawPromptsPersisted": False,
            "rawModelResponsesPersisted": False,
            "chainOfThoughtPersisted": False,
            "secretsIncluded": False,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_model_json_object(raw_content: str) -> dict[str, Any]:
    try:
        return parse_model_json_object_shared(raw_content)
    except ModelJsonParseError as exc:
        raise PackageSetAIEnrichmentError(str(exc)) from exc


def json_repair_diagnostics(
    provider_receipt: dict[str, Any],
    package_id: str,
) -> list[dict[str, Any]]:
    if not provider_receipt.get("jsonRepairNeeded"):
        return []
    attempt_count = provider_receipt.get("jsonRepairAttemptCount")
    repair_status = string_value(provider_receipt.get("jsonRepairStatus"))
    diagnostics = [
        diagnostic(
            "warning",
            "ai_json_repair_needed",
            "Initial local model output was not a valid JSON object; bounded repair was attempted.",
            package_id,
            {
                "repairAttemptCount": attempt_count if isinstance(attempt_count, int) else 0,
                "jsonRepairStatus": repair_status,
            },
        )
    ]
    if repair_status == "exhausted":
        diagnostics.append(
            diagnostic(
                "error",
                "ai_json_repair_exhausted",
                "Local model output remained invalid JSON after bounded repair attempts.",
                package_id,
                {
                    "repairAttemptCount": attempt_count if isinstance(attempt_count, int) else 0,
                },
            )
        )
    return diagnostics


def normalize_local_provider_base_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value.strip().rstrip("/"))
    if parsed.scheme != "http" or parsed.hostname not in LOCAL_PROVIDER_HOSTS:
        raise ValueError("Provider base URL must be an explicit local http URL")
    if parsed.username or parsed.password:
        raise ValueError("Provider base URL must not include credentials")
    if (
        parsed.params
        or parsed.query
        or parsed.fragment
        or ";" in parsed.netloc
        or ";" in parsed.path
    ):
        raise ValueError("Provider base URL must not include params, query, or fragment")
    path = parsed.path.rstrip("/")
    if path == "/v1":
        path = ""
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def safe_bundle_path(root: Path, relative: str) -> Path | None:
    if not relative:
        return None
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        return None
    return candidate


def source_role(relative: str) -> str:
    name = Path(relative).name.lower()
    if name == "package.json":
        return "package_manifest"
    if name == "readme.md":
        return "readme"
    return "public_exports"


def join_posix(prefix: str, suffix: str) -> str:
    if not prefix:
        return suffix
    return f"{prefix.rstrip('/')}/{suffix.lstrip('/')}"


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def confidence_value(value: Any) -> str:
    return value if value in {"high", "medium", "low"} else "low"


def diagnostic(
    severity: str,
    code: str,
    message: str,
    package_id: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "severity": severity,
        "code": code,
        "message": message,
        "packageId": package_id,
    }
    if extra:
        payload.update(extra)
    return payload


def sum_provider_usage(proposals: list[dict[str, Any]], key: str) -> int:
    total = 0
    for proposal in proposals:
        receipt = proposal.get("providerReceipt")
        if not isinstance(receipt, dict):
            continue
        usage = receipt.get("usage")
        if not isinstance(usage, dict):
            continue
        value = usage.get(key)
        if isinstance(value, int):
            total += value
    return total


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
