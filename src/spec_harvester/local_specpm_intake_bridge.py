from __future__ import annotations

import hashlib
import json
import os
import resource
import shlex
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import yaml  # type: ignore[import-untyped]

from spec_harvester.local_candidate_review_catalog import (
    LocalCandidateReviewCatalogOptions,
    _catalog_item,
    _json_object,
    _preflight_statuses,
    _read_archive,
)
from spec_harvester.local_candidate_review_details import _catalog_bindings
from spec_harvester.local_review_decision_service import LocalReviewDecisionStore

INTAKE_API_VERSION = "spec-harvester.local-specpm-intake-proposal/v0"
INTAKE_KIND = "SpecHarvesterLocalSpecPMIntakeProposal"
MAX_SPECPM_REPORT_BYTES = 2 * 1024 * 1024
DEFAULT_SPECPM_TIMEOUT_SECONDS = 60

NON_AUTHORITY = [
    "This record is read-only SpecPM intake proposal evidence.",
    "It is not SpecPM registry acceptance.",
    "It does not accept packages or relations.",
    "It does not remove preview_only.",
    "It does not mutate accepted sources or public index metadata.",
    "It does not create or merge a SpecPM pull request.",
    "It does not replace SpecPM maintainer review.",
]


@dataclass(frozen=True)
class LocalSpecPMIntakeBridgeOptions:
    archive: Path
    expected_archive_sha256: str
    catalog: Path
    review_workspace: Path
    output: Path
    specpm_command: str = "specpm"
    specpm_pythonpath: str | None = None
    specpm_timeout_seconds: int = DEFAULT_SPECPM_TIMEOUT_SECONDS
    max_specpm_report_bytes: int = MAX_SPECPM_REPORT_BYTES


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} path is invalid")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"{label} path is unsafe: {value}")
    return value


def _reconstruct_candidate(
    candidate_id: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
    root: Path,
) -> list[Path]:
    candidate = packet["candidate"]
    for record in candidate["files"]:
        relative_name = _safe_relative_path(record.get("path"), f"Candidate {candidate_id}")
        relative = PurePosixPath(relative_name)
        if relative.parts[0] != "candidate":
            raise ValueError(
                f"Candidate file is outside the candidate package root: "
                f"{candidate_id}/{relative_name}"
            )
        archive_name = str(PurePosixPath("packets", candidate_id, relative_name))
        payload = members.get(archive_name)
        if payload is None:
            raise ValueError(f"Candidate file is missing from portable handoff: {archive_name}")
        target = root.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    manifests = sorted(root.glob("candidate/**/specpm.yaml"))
    if not manifests:
        raise ValueError(f"Approved candidate has no SpecPM package manifest: {candidate_id}")
    return [manifest.parent for manifest in manifests]


def _read_bounded(path: Path, limit: int, label: str) -> bytes:
    try:
        with path.open("rb") as source:
            payload = source.read(limit + 1)
    except OSError as exc:
        raise ValueError(f"Cannot read {label}: {exc}") from exc
    if len(payload) > limit:
        raise ValueError(f"{label} exceeds the configured byte limit")
    return payload


def _limit_process_output(max_report_bytes: int) -> Any:
    def apply_limit() -> None:
        # Leave one sentinel byte so the parent can distinguish an exact-size
        # valid report from output that attempted to exceed the bound.
        limit = max_report_bytes + 1
        resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))

    return apply_limit


def _run_specpm_validation(
    candidate: Path,
    *,
    command: str,
    pythonpath: str | None,
    timeout_seconds: int,
    max_report_bytes: int,
) -> dict[str, Any]:
    argv = shlex.split(command)
    if not argv:
        raise ValueError("SpecPM validation command is empty")
    argv.extend(["validate", str(candidate), "--json"])
    env = os.environ.copy()
    if pythonpath:
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = pythonpath if not existing else f"{pythonpath}{os.pathsep}{existing}"
    with tempfile.TemporaryDirectory(prefix="spec-harvester-specpm-report-") as temp:
        stdout_path = Path(temp) / "stdout.json"
        stderr_path = Path(temp) / "stderr.txt"
        try:
            with stdout_path.open("wb") as stdout_file, stderr_path.open("wb") as stderr_file:
                completed = subprocess.run(  # noqa: S603
                    argv,
                    check=False,
                    env=env,
                    stdout=stdout_file,
                    stderr=stderr_file,
                    timeout=timeout_seconds,
                    preexec_fn=_limit_process_output(max_report_bytes),
                )
        except FileNotFoundError as exc:
            raise ValueError(f"SpecPM command was not found: {argv[0]}") from exc
        except subprocess.TimeoutExpired as exc:
            raise ValueError(f"SpecPM validation exceeded {timeout_seconds} seconds") from exc
        stdout_payload = _read_bounded(stdout_path, max_report_bytes, "SpecPM validation output")
        stderr_payload = _read_bounded(
            stderr_path, max_report_bytes, "SpecPM validation diagnostics"
        )
    try:
        report = json.loads(stdout_payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(
            "SpecPM validation did not return JSON. "
            f"exit={completed.returncode}, "
            f"stderr={stderr_payload.decode(errors='replace').strip()}"
        ) from exc
    if not isinstance(report, dict):
        raise ValueError("SpecPM validation report must be an object")
    if completed.returncode != 0 and report.get("status") != "invalid":
        raise ValueError(
            "SpecPM validation command failed unexpectedly. "
            f"exit={completed.returncode}, "
            f"stderr={stderr_payload.decode(errors='replace').strip()}"
        )
    return report


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"SpecPM validation {label} is invalid")
    return value


def _issue_list(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError(f"SpecPM validation {label} is invalid")
    issues: list[dict[str, str]] = []
    allowed = ("severity", "code", "message", "file", "field")
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"SpecPM validation {label} entry is invalid")
        issue = {key: item[key] for key in allowed if isinstance(item.get(key), str) and item[key]}
        if "code" not in issue or "message" not in issue:
            raise ValueError(f"SpecPM validation {label} entry is incomplete")
        if "file" in issue:
            _safe_relative_path(issue["file"], f"SpecPM validation {label}")
        issues.append(issue)
    return issues


def _normalized_specpm_report(report: dict[str, Any]) -> dict[str, Any]:
    status = report.get("status")
    if status not in {"valid", "warning_only", "invalid"}:
        raise ValueError("SpecPM validation status is invalid")
    error_count = report.get("error_count")
    warning_count = report.get("warning_count")
    if (
        not isinstance(error_count, int)
        or isinstance(error_count, bool)
        or error_count < 0
        or not isinstance(warning_count, int)
        or isinstance(warning_count, bool)
        or warning_count < 0
    ):
        raise ValueError("SpecPM validation issue counts are invalid")
    errors = _issue_list(report.get("errors"), "errors")
    warnings = _issue_list(report.get("warnings"), "warnings")
    if len(errors) != error_count or len(warnings) != warning_count:
        raise ValueError("SpecPM validation issue counts do not match entries")
    if status in {"valid", "warning_only"} and error_count:
        raise ValueError("SpecPM validation status conflicts with explicit errors")
    identity = report.get("package_identity")
    if not isinstance(identity, dict):
        raise ValueError("SpecPM validation package identity is invalid")
    package_identity = {
        key: identity[key]
        for key in ("package_id", "name", "version")
        if isinstance(identity.get(key), str) and identity[key]
    }
    if set(package_identity) != {"package_id", "name", "version"}:
        raise ValueError("SpecPM validation package identity is incomplete")
    mappings = report.get("intent_mappings")
    if not isinstance(mappings, list):
        raise ValueError("SpecPM validation intent mappings are invalid")
    intent_mappings = []
    for mapping in mappings:
        if (
            not isinstance(mapping, dict)
            or not isinstance(mapping.get("capability_id"), str)
            or not isinstance(mapping.get("intent_id"), str)
        ):
            raise ValueError("SpecPM validation intent mapping is invalid")
        intent_mappings.append(
            {
                "capabilityId": mapping["capability_id"],
                "intentId": mapping["intent_id"],
            }
        )
    checked_files = _string_list(report.get("checked_files"), "checked files")
    for path in checked_files:
        _safe_relative_path(path, "SpecPM validation checked file")
    return {
        "status": status,
        "errorCount": error_count,
        "warningCount": warning_count,
        "packageIdentity": package_identity,
        "checkedFiles": checked_files,
        "capabilities": _string_list(report.get("capabilities"), "capabilities"),
        "intents": _string_list(report.get("intents"), "intents"),
        "intentMappings": intent_mappings,
        "errors": errors,
        "warnings": warnings,
    }


def _manifest_preview_only(candidate: Path) -> bool:
    try:
        manifest = yaml.safe_load((candidate / "specpm.yaml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"Cannot read reconstructed candidate manifest: {exc}") from exc
    return isinstance(manifest, dict) and manifest.get("preview_only") is True


def _approved_candidate_record(
    *,
    candidate_id: str,
    packet_sha256: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
    current: dict[str, Any],
    options: LocalSpecPMIntakeBridgeOptions,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="spec-harvester-intake-") as temporary:
        roots = _reconstruct_candidate(candidate_id, packet, members, Path(temporary))
        packages = []
        for root in roots:
            if not _manifest_preview_only(root):
                raise ValueError(
                    f"Approved candidate manifest is not preview_only: {candidate_id}/{root.name}"
                )
            report = _normalized_specpm_report(
                _run_specpm_validation(
                    root,
                    command=options.specpm_command,
                    pythonpath=options.specpm_pythonpath,
                    timeout_seconds=options.specpm_timeout_seconds,
                    max_report_bytes=options.max_specpm_report_bytes,
                )
            )
            report_bytes = _json_bytes(report)
            packages.append(
                {
                    "packageRoot": root.relative_to(Path(temporary)).as_posix(),
                    "preflightStatus": (
                        "passed" if report["status"] in {"valid", "warning_only"} else "failed"
                    ),
                    "specpmReportSha256": _sha256(report_bytes),
                    "specpmReport": report,
                }
            )
    decision = current["decision"]
    return {
        "candidateId": candidate_id,
        "packetSha256": packet_sha256,
        "decisionSha256": current["decisionSha256"],
        "reviewDecision": {
            "disposition": decision["disposition"],
            "reasonCode": decision["reasonCode"],
            "reviewer": decision["reviewer"],
            "recordedAt": decision["recordedAt"],
        },
        "status": (
            "specpm_preflight_passed"
            if all(package["preflightStatus"] == "passed" for package in packages)
            else "specpm_preflight_failed"
        ),
        "packages": packages,
    }


def build_local_specpm_intake_proposal(
    options: LocalSpecPMIntakeBridgeOptions,
) -> dict[str, Any]:
    if options.specpm_timeout_seconds < 1:
        raise ValueError("SpecPM validation timeout must be positive")
    if not 1 <= options.max_specpm_report_bytes <= MAX_SPECPM_REPORT_BYTES:
        raise ValueError("SpecPM validation report byte limit is invalid")
    archive_sha256, members = _read_archive(
        LocalCandidateReviewCatalogOptions(
            archive=options.archive,
            expected_archive_sha256=options.expected_archive_sha256,
        )
    )
    aggregate_bytes = members.get("aggregate-handoff.json")
    if aggregate_bytes is None:
        raise ValueError("Portable handoff is missing aggregate-handoff.json")
    aggregate = _json_object(aggregate_bytes, "aggregate-handoff.json")
    expectations = _preflight_statuses(aggregate)
    bindings = _catalog_bindings(options.catalog)
    store = LocalReviewDecisionStore(options.review_workspace, options.catalog)
    if store.source_bundle_sha256 != archive_sha256:
        raise ValueError("Review decisions and portable handoff archive digests differ")

    current_records = store.current_decisions()["decisions"]
    skipped = Counter(
        current["decision"]["disposition"]
        for current in current_records
        if current["decision"]["disposition"] != "accept_for_intake"
    )
    approved = {
        current["decision"]["binding"]["candidateId"]: current
        for current in current_records
        if current["decision"]["disposition"] == "accept_for_intake"
    }
    candidates = []
    for candidate_id in sorted(approved):
        current = approved[candidate_id]
        decision = current["decision"]
        if decision["reasonCode"] != "evidence_verified":
            raise ValueError(f"Approved candidate has an invalid intake reason: {candidate_id}")
        packet_name = f"packets/{candidate_id}/packet.json"
        packet_bytes = members.get(packet_name)
        if packet_bytes is None:
            raise ValueError(f"Approved candidate packet is missing: {candidate_id}")
        _, catalog_item = _catalog_item(packet_name, packet_bytes, expectations, members)
        packet_sha256 = catalog_item["packetSha256"]
        if (
            bindings.get(candidate_id) != packet_sha256
            or decision["binding"]["packetSha256"] != packet_sha256
            or current["packetSha256"] != packet_sha256
        ):
            raise ValueError(f"Approved candidate packet binding is stale: {candidate_id}")
        packet = _json_object(packet_bytes, packet_name)
        candidates.append(
            _approved_candidate_record(
                candidate_id=candidate_id,
                packet_sha256=packet_sha256,
                packet=packet,
                members=members,
                current=current,
                options=options,
            )
        )

    package_count = sum(len(candidate["packages"]) for candidate in candidates)
    passed_count = sum(
        package["preflightStatus"] == "passed"
        for candidate in candidates
        for package in candidate["packages"]
    )
    payload = {
        "apiVersion": INTAKE_API_VERSION,
        "kind": INTAKE_KIND,
        "authority": "local_review_specpm_intake_proposal_evidence_only",
        "sourceBundleSha256": archive_sha256,
        "summary": {
            "reviewedCandidateCount": len(current_records),
            "approvedCandidateCount": len(candidates),
            "skippedDecisionCount": sum(skipped.values()),
            "skippedDispositionCounts": dict(sorted(skipped.items())),
            "packageCount": package_count,
            "specpmPreflightPassedCount": passed_count,
            "specpmPreflightFailedCount": package_count - passed_count,
        },
        "candidates": candidates,
        "nonAuthority": list(NON_AUTHORITY),
        "notExecuted": [
            "repository checkout access",
            "package manager execution",
            "harvested code execution",
            "AI provider invocation",
            "SpecPM accepted-source mutation",
            "public index mutation",
            "SpecPM pull request creation",
        ],
        "registryMutationCount": 0,
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_bytes(_json_bytes(payload))
    return {
        "status": "passed",
        "approvedCandidateCount": len(candidates),
        "packageCount": package_count,
        "specpmPreflightFailedCount": package_count - passed_count,
        "output": str(options.output),
    }
