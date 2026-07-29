from __future__ import annotations

import http.client
import json
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import patch

from spec_harvester.local_candidate_review_browser import (
    LocalCandidateReviewBrowserOptions,
    render_local_candidate_review_browser,
)
from spec_harvester.local_candidate_review_catalog import (
    LocalCandidateReviewCatalogOptions,
    _catalog_item,
    _json_object,
    _preflight_statuses,
    _read_archive,
)
from spec_harvester.local_review_decision_service import (
    LocalReviewDecisionServiceOptions,
    LocalReviewDecisionStore,
    build_local_review_decision_server,
)
from spec_harvester.local_specpm_intake_bridge import (
    LocalSpecPMIntakeBridgeOptions,
    build_local_specpm_intake_proposal,
)

E2E_API_VERSION = "spec-harvester.local-candidate-review-workbench-e2e/v0"
E2E_KIND = "SpecHarvesterLocalCandidateReviewWorkbenchE2E"
HOSTILE_MARKER = "<script>globalThis.__candidateExecuted=true</script>"
CSRF_TOKEN = "p54-t9-e2e-csrf-token-with-at-least-32-characters"
REVIEW_ORIGIN = "http://127.0.0.1:8017"


@dataclass(frozen=True)
class LocalCandidateReviewWorkbenchE2EOptions:
    archive: Path
    expected_archive_sha256: str
    catalog: Path
    details: Path
    output: Path
    specpm_command: str = "specpm"
    specpm_pythonpath: str | None = None


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _wave_records(details: dict[str, Any]) -> tuple[dict[str, int], dict[str, str]]:
    counts: dict[str, int] = {}
    representatives: dict[str, str] = {}
    records = details.get("details")
    if not isinstance(records, list):
        raise ValueError("Candidate detail records are invalid")
    for record in records:
        try:
            candidate_id = record["binding"]["candidateId"]
            section = next(item for item in record["sections"] if item["id"] == "source-provenance")
            wave = json.loads(section["content"])["wave"]
        except (KeyError, StopIteration, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Candidate wave provenance is invalid") from exc
        if wave not in {"wave-1", "wave-2", "wave-3", "wave-4"}:
            raise ValueError(f"Candidate wave provenance is unknown: {wave}")
        counts[wave] = counts.get(wave, 0) + 1
        representatives.setdefault(wave, candidate_id)
    if counts != {f"wave-{index}": 25 for index in range(1, 5)}:
        raise ValueError(f"Candidate wave coverage is incomplete: {counts}")
    return counts, representatives


def _decision(
    item: dict[str, Any],
    disposition: str,
    index: int,
) -> dict[str, Any]:
    reasons = {
        "accept_for_intake": "evidence_verified",
        "request_revision": "evidence_revision_required",
        "defer": "review_deferred",
        "do_not_promote": "promotion_not_suitable",
    }
    return {
        "apiVersion": "spec-harvester.candidate-review-decision/v0",
        "kind": "SpecHarvesterCandidateReviewDecision",
        "authority": "local_review_decision_evidence_only",
        "binding": {
            "candidateId": item["candidateId"],
            "packetSha256": item["packetSha256"],
        },
        "disposition": disposition,
        "reviewer": "p54-t9-maintainer",
        "recordedAt": f"2026-07-29T15:00:0{index}Z",
        "reasonCode": reasons[disposition],
        "notes": f"P54-T9 representative {disposition} review.",
        "priorDecisionSha256": None,
    }


def _expect_value_error(action: Any, label: str) -> None:
    try:
        action()
    except ValueError:
        return
    raise ValueError(f"{label} did not fail closed")


def _exercise_packet_failures(members: dict[str, bytes], aggregate: dict[str, Any]) -> list[str]:
    expectations = _preflight_statuses(aggregate)
    packet_name = sorted(
        name for name in members if name.startswith("packets/") and name.endswith("/packet.json")
    )[0]
    packet = _json_object(members[packet_name], packet_name)

    malformed = json.loads(json.dumps(packet))
    del malformed["candidate"]
    _expect_value_error(
        lambda: _catalog_item(
            packet_name,
            (json.dumps(malformed, sort_keys=True) + "\n").encode(),
            expectations,
            members,
        ),
        "Malformed packet",
    )

    traversing = json.loads(json.dumps(packet))
    traversing["candidate"]["files"][0]["path"] = "../workspace-escape"
    _expect_value_error(
        lambda: _catalog_item(
            packet_name,
            (json.dumps(traversing, sort_keys=True) + "\n").encode(),
            expectations,
            members,
        ),
        "Traversing packet",
    )
    return ["malformed_packet_rejected", "path_traversal_rejected"]


def _exercise_hostile_browser(
    catalog: Path,
    details: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    hostile = json.loads(json.dumps(details))
    hostile["details"][0]["sections"].append(
        {
            "id": "hostile-candidate-content.json",
            "contentType": "application/json",
            "content": json.dumps({"candidateText": HOSTILE_MARKER}),
        }
    )
    hostile_path = root / "hostile-details.json"
    hostile_path.write_text(json.dumps(hostile, indent=2, sort_keys=True) + "\n")
    browser = root / "browser"
    rendered = render_local_candidate_review_browser(
        LocalCandidateReviewBrowserOptions(catalog, browser, hostile_path)
    )
    index = (browser / "index.html").read_text()
    script = (browser / "workbench.js").read_text()
    presentations = (browser / "presentations.json").read_text()
    if HOSTILE_MARKER not in presentations or HOSTILE_MARKER in index or HOSTILE_MARKER in script:
        raise ValueError("Hostile candidate marker crossed the inert presentation boundary")
    required_csp = (
        "default-src 'self'",
        "script-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "frame-ancestors 'none'",
    )
    if not all(value in index for value in required_csp):
        raise ValueError("Workbench Content Security Policy is incomplete")
    if "innerHTML" in script or "eval(" in script or CSRF_TOKEN in index + script:
        raise ValueError("Workbench browser rendering boundary is unsafe")
    return {
        "candidateCount": rendered["candidateCount"],
        "detailCount": rendered["detailCount"],
        "hostileMarkerPersistedAsInertText": True,
        "hostileMarkerPresentInExecutableAssets": False,
        "candidateRenderingPrimitive": "textContent",
        "inlineScriptAllowed": False,
        "csrfTokenPersisted": False,
        "contentSecurityPolicy": list(required_csp),
    }


def _exercise_decisions(
    catalog_path: Path,
    catalog: dict[str, Any],
    representatives: dict[str, str],
    root: Path,
) -> tuple[Path, list[dict[str, str]], dict[str, Any]]:
    workspace = root / "review"
    items = {item["candidateId"]: item for item in catalog["items"]}
    dispositions = [
        "accept_for_intake",
        "request_revision",
        "defer",
        "do_not_promote",
    ]
    store = LocalReviewDecisionStore(workspace, catalog_path)
    reviewed = []
    for index, (wave, disposition) in enumerate(
        zip(sorted(representatives), dispositions, strict=True)
    ):
        candidate_id = representatives[wave]
        store.write(_decision(items[candidate_id], disposition, index))
        reviewed.append(
            {
                "wave": wave,
                "candidateId": candidate_id,
                "disposition": disposition,
            }
        )
    before_restart = store.current_decisions()
    summary = store.summary()
    restarted = LocalReviewDecisionStore(workspace, catalog_path)
    if restarted.current_decisions() != before_restart or restarted.summary() != summary:
        raise ValueError("Review decisions did not survive restart")
    exchange = restarted.export()
    imported = LocalReviewDecisionStore(root / "imported-review", catalog_path)
    imported.import_exchange(exchange)
    if imported.export() != exchange:
        raise ValueError("Portable decision exchange did not round-trip")

    stale_workspace = root / "stale-review"
    stale = LocalReviewDecisionStore(stale_workspace, catalog_path)
    stale_record = stale.write(_decision(items[representatives["wave-1"]], "defer", 4))
    current_path = stale_workspace / "decisions" / f"{stale_record['candidateId']}.json"
    current = json.loads(current_path.read_text())
    current["binding"]["packetSha256"] = "0" * 64
    current_path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
    _expect_value_error(
        lambda: LocalReviewDecisionStore(stale_workspace, catalog_path).current(
            stale_record["candidateId"]
        ),
        "Stale decision",
    )

    interrupted_workspace = root / "interrupted-review"
    interrupted = LocalReviewDecisionStore(interrupted_workspace, catalog_path)
    with patch(
        "spec_harvester.local_review_decision_service.os.replace",
        side_effect=OSError("simulated interrupted replace"),
    ):
        _expect_value_error(
            lambda: interrupted.write(_decision(items[representatives["wave-2"]], "defer", 5)),
            "Interrupted write",
        )
    temporary_files = [
        path
        for path in interrupted_workspace.rglob(".decision-*")
        if path.name != ".decision-write.lock"
    ]
    if interrupted.current(representatives["wave-2"]) is not None or temporary_files:
        raise ValueError("Interrupted decision write left partial state")
    return workspace, reviewed, summary


def _request(
    port: int,
    action: dict[str, Any],
    *,
    origin: str,
    csrf: str,
) -> int:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    connection.request(
        "POST",
        "/v0/actions",
        body=json.dumps(action),
        headers={
            "Content-Type": "application/json",
            "Origin": origin,
            "X-CSRF-Token": csrf,
        },
    )
    response = connection.getresponse()
    response.read()
    connection.close()
    return response.status


def _exercise_service_security(
    catalog_path: Path,
    catalog: dict[str, Any],
    root: Path,
) -> dict[str, Any]:
    item = catalog["items"][10]
    action = {
        "candidateId": item["candidateId"],
        "disposition": "defer",
        "reviewer": "p54-t9-maintainer",
        "reasonCode": "review_deferred",
        "notes": "HTTP boundary validation.",
        "priorDecisionSha256": None,
    }
    server = build_local_review_decision_server(
        LocalReviewDecisionServiceOptions(
            workspace=root / "http-review",
            catalog=catalog_path,
            csrf_token=CSRF_TOKEN,
            allowed_origin=REVIEW_ORIGIN,
            port=0,
        )
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        attacker_status = _request(port, action, origin="http://candidate.invalid", csrf=CSRF_TOKEN)
        csrf_status = _request(port, action, origin=REVIEW_ORIGIN, csrf="invalid")
        allowed_status = _request(port, action, origin=REVIEW_ORIGIN, csrf=CSRF_TOKEN)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    if (attacker_status, csrf_status, allowed_status) != (403, 403, 201):
        raise ValueError("Decision service Origin/CSRF boundary failed")
    return {
        "candidateOriginStatus": attacker_status,
        "invalidCsrfStatus": csrf_status,
        "reviewerOriginStatus": allowed_status,
    }


def build_local_candidate_review_workbench_e2e(
    options: LocalCandidateReviewWorkbenchE2EOptions,
) -> dict[str, Any]:
    archive_sha256, members = _read_archive(
        LocalCandidateReviewCatalogOptions(
            archive=options.archive,
            expected_archive_sha256=options.expected_archive_sha256,
        )
    )
    aggregate = _json_object(members["aggregate-handoff.json"], "aggregate-handoff.json")
    catalog = _read_json(options.catalog, "candidate review catalog")
    details = _read_json(options.details, "candidate review detail set")
    if catalog.get("sourceBundleSha256") != archive_sha256:
        raise ValueError("Candidate catalog source bundle digest is stale")
    if details.get("sourceBundleSha256") != archive_sha256:
        raise ValueError("Candidate detail source bundle digest is stale")
    wave_counts, representatives = _wave_records(details)

    with tempfile.TemporaryDirectory(prefix="spec-harvester-workbench-e2e-") as temporary:
        root = Path(temporary)
        browser = _exercise_hostile_browser(options.catalog, details, root)
        negative_checks = _exercise_packet_failures(members, aggregate)

        drifted = json.loads(json.dumps(details))
        drifted["details"][0]["binding"]["packetSha256"] = "0" * 64
        drifted_path = root / "drifted-details.json"
        drifted_path.write_text(json.dumps(drifted))
        _expect_value_error(
            lambda: render_local_candidate_review_browser(
                LocalCandidateReviewBrowserOptions(
                    options.catalog, root / "drifted-browser", drifted_path
                )
            ),
            "Detail digest drift",
        )
        negative_checks.append("detail_digest_drift_rejected")

        workspace, reviewed, progress = _exercise_decisions(
            options.catalog, catalog, representatives, root
        )
        service_security = _exercise_service_security(options.catalog, catalog, root)
        intake_path = root / "specpm-intake.json"
        intake_result = build_local_specpm_intake_proposal(
            LocalSpecPMIntakeBridgeOptions(
                archive=options.archive,
                expected_archive_sha256=options.expected_archive_sha256,
                catalog=options.catalog,
                review_workspace=workspace,
                output=intake_path,
                specpm_command=options.specpm_command,
                specpm_pythonpath=options.specpm_pythonpath,
            )
        )
        intake = _read_json(intake_path, "SpecPM intake proposal")
        if intake_result["specpmPreflightFailedCount"] or intake["registryMutationCount"]:
            raise ValueError("Read-only SpecPM intake E2E validation failed")

    payload = {
        "apiVersion": E2E_API_VERSION,
        "kind": E2E_KIND,
        "authority": "local_workbench_validation_evidence_only",
        "status": "passed",
        "sourceBundleSha256": archive_sha256,
        "corpus": {
            "candidateCount": len(catalog["items"]),
            "detailCount": len(details["details"]),
            "comparisonCount": len(details["comparisons"]),
            "waveCounts": dict(sorted(wave_counts.items())),
        },
        "representativeReviews": reviewed,
        "decisionLifecycle": {
            "reviewedCount": progress["reviewedCount"],
            "unreviewedCount": progress["unreviewedCount"],
            "dispositionCounts": progress["dispositionCounts"],
            "restartHydrationPassed": True,
            "portableExchangeRoundTripPassed": True,
            "staleDecisionRejected": True,
            "interruptedWriteLeftPartialState": False,
        },
        "browserSecurity": browser,
        "serviceSecurity": service_security,
        "negativeChecks": sorted(
            [
                *negative_checks,
                "archive_digest_revalidated",
                "catalog_digest_revalidated",
                "interrupted_write_rejected",
                "stale_decision_rejected",
            ]
        ),
        "specpmIntake": {
            "approvedCandidateCount": intake_result["approvedCandidateCount"],
            "packageCount": intake_result["packageCount"],
            "failedCount": intake_result["specpmPreflightFailedCount"],
            "registryMutationCount": intake["registryMutationCount"],
            "previewOnlyPreserved": True,
        },
        "notExecuted": [
            "package manager",
            "harvested repository code",
            "trusted adapter",
            "AI provider",
            "registry acceptance",
            "public index publication",
        ],
        "privacy": {
            "rawPromptPersisted": False,
            "rawResponsePersisted": False,
            "chainOfThoughtPersisted": False,
        },
        "registryMutationCount": 0,
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return {
        "status": "passed",
        "candidateCount": payload["corpus"]["candidateCount"],
        "representativeReviewCount": len(reviewed),
        "specpmPreflightFailedCount": intake_result["specpmPreflightFailedCount"],
        "output": str(options.output),
    }
