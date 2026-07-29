from __future__ import annotations

import http.client
import json
import multiprocessing
import threading
from pathlib import Path
from typing import Any

import pytest

from spec_harvester.local_review_decision_service import (
    LocalReviewDecisionServiceOptions,
    LocalReviewDecisionStore,
    build_local_review_decision_server,
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json"
CSRF_TOKEN = "p54-t6-test-token-with-at-least-32-characters"
ORIGIN = "http://127.0.0.1:8000"


def _write_replacement_process(
    workspace: str,
    replacement: dict[str, object],
    barrier: Any,
    results: Any,
) -> None:
    store = LocalReviewDecisionStore(Path(workspace), CATALOG)
    barrier.wait()
    try:
        recorded = store.write(replacement)
    except ValueError as exc:
        results.put(("error", str(exc)))
    else:
        results.put(("recorded", recorded["decisionSha256"]))


def decision(
    catalog: dict[str, object],
    *,
    prior: str | None = None,
    disposition: str = "defer",
) -> dict[str, object]:
    item = catalog["items"][0]  # type: ignore[index]
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
            "candidateId": item["candidateId"],  # type: ignore[index]
            "packetSha256": item["packetSha256"],  # type: ignore[index]
        },
        "disposition": disposition,
        "reviewer": "maintainer@example",
        "recordedAt": "2026-07-29T08:00:00Z",
        "reasonCode": reasons[disposition],
        "notes": "Bounded local review evidence.",
        "priorDecisionSha256": prior,
    }


def catalog_payload() -> dict[str, object]:
    return json.loads(CATALOG.read_text())


def test_store_records_atomic_history_and_survives_restart(tmp_path: Path) -> None:
    payload = catalog_payload()
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    first = store.write(decision(payload))
    candidate_id = first["candidateId"]

    current = store.current(candidate_id)
    assert current is not None
    assert current["decisionSha256"] == first["decisionSha256"]
    assert (
        tmp_path / "workspace" / "history" / candidate_id / f"{first['decisionSha256']}.json"
    ).is_file()

    restarted = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    assert restarted.current(candidate_id) == current


def test_store_requires_exact_prior_and_preserves_replacement_history(tmp_path: Path) -> None:
    payload = catalog_payload()
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    first = store.write(decision(payload))

    with pytest.raises(ValueError, match="prior digest is stale"):
        store.write(decision(payload, prior="0" * 64, disposition="request_revision"))

    second = store.write(
        decision(payload, prior=first["decisionSha256"], disposition="request_revision")
    )
    history = list((tmp_path / "workspace" / "history" / first["candidateId"]).glob("*.json"))
    assert len(history) == 2
    assert second["priorDecisionSha256"] == first["decisionSha256"]


@pytest.mark.parametrize(
    ("disposition", "reason_code"),
    [
        ("accept_for_intake", "evidence_verified"),
        ("request_revision", "evidence_revision_required"),
        ("defer", "review_deferred"),
        ("do_not_promote", "promotion_not_suitable"),
    ],
)
def test_store_records_each_bounded_reviewer_action(
    tmp_path: Path, disposition: str, reason_code: str
) -> None:
    payload = catalog_payload()
    item = payload["items"][0]  # type: ignore[index]
    store = LocalReviewDecisionStore(tmp_path / disposition, CATALOG)

    result = store.record_action(
        {
            "candidateId": item["candidateId"],  # type: ignore[index]
            "disposition": disposition,
            "reviewer": "maintainer@example",
            "reasonCode": reason_code,
            "notes": "Reviewed locally.",
            "priorDecisionSha256": None,
        }
    )

    assert result["status"] == "recorded"
    assert store.current(result["candidateId"])["decision"]["disposition"] == disposition  # type: ignore[index]


def test_store_rejects_reason_for_different_disposition(tmp_path: Path) -> None:
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    invalid = decision(catalog_payload())
    invalid["reasonCode"] = "evidence_verified"

    with pytest.raises(ValueError, match="reason is not allowed"):
        store.write(invalid)


def test_store_summary_and_portable_exchange_round_trip(tmp_path: Path) -> None:
    payload = catalog_payload()
    source = LocalReviewDecisionStore(tmp_path / "source", CATALOG)
    first = source.write(decision(payload))
    source.write(
        decision(payload, prior=first["decisionSha256"], disposition="request_revision")
    )

    summary = source.summary()
    assert summary["candidateCount"] == 100
    assert summary["reviewedCount"] == 1
    assert summary["unreviewedCount"] == 99
    assert summary["dispositionCounts"]["request_revision"] == 1

    exchange = source.export()
    assert exchange["registryMutationCount"] == 0
    assert len(exchange["decisions"]) == 2
    target = LocalReviewDecisionStore(tmp_path / "target", CATALOG)
    imported = target.import_exchange(exchange)
    assert imported == {
        "status": "imported",
        "decisionCount": 2,
        "sourceBundleSha256": exchange["sourceBundleSha256"],
        "registryMutationCount": 0,
    }
    assert target.export() == exchange


def test_store_rejects_stale_or_broken_portable_exchange(tmp_path: Path) -> None:
    payload = catalog_payload()
    source = LocalReviewDecisionStore(tmp_path / "source", CATALOG)
    source.write(decision(payload))
    exchange = source.export()

    stale = {**exchange, "sourceBundleSha256": "0" * 64}
    with pytest.raises(ValueError, match="source bundle digest is stale"):
        LocalReviewDecisionStore(tmp_path / "stale", CATALOG).import_exchange(stale)

    broken = json.loads(json.dumps(exchange))
    broken["decisions"][0]["priorDecisionSha256"] = "0" * 64
    with pytest.raises(ValueError, match="history is stale or out of order"):
        LocalReviewDecisionStore(tmp_path / "broken", CATALOG).import_exchange(broken)


def test_store_serializes_optimistic_replacements_across_processes(tmp_path: Path) -> None:
    payload = catalog_payload()
    workspace = tmp_path / "workspace"
    first = LocalReviewDecisionStore(workspace, CATALOG).write(decision(payload))
    replacements = [
        decision(payload, prior=first["decisionSha256"], disposition="request_revision"),
        decision(payload, prior=first["decisionSha256"], disposition="do_not_promote"),
    ]
    replacements[1]["recordedAt"] = "2026-07-29T08:00:01Z"
    context = multiprocessing.get_context("spawn")
    barrier = context.Barrier(2)
    results = context.Queue()
    processes = [
        context.Process(
            target=_write_replacement_process,
            args=(str(workspace), replacement, barrier, results),
        )
        for replacement in replacements
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join(timeout=10)
        assert process.exitcode == 0

    outcomes = [results.get(timeout=2), results.get(timeout=2)]
    assert sorted(outcome[0] for outcome in outcomes) == ["error", "recorded"]
    assert "prior digest is stale" in next(
        outcome[1] for outcome in outcomes if outcome[0] == "error"
    )
    history = list((workspace / "history" / first["candidateId"]).glob("*.json"))
    assert len(history) == 2


def test_store_rejects_unknown_stale_and_malformed_decisions(tmp_path: Path) -> None:
    payload = catalog_payload()
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)

    unknown = decision(payload)
    unknown["binding"]["candidateId"] = "unknown-candidate"  # type: ignore[index]
    with pytest.raises(ValueError, match="Unknown review candidate"):
        store.write(unknown)

    stale = decision(payload)
    stale["binding"]["packetSha256"] = "0" * 64  # type: ignore[index]
    with pytest.raises(ValueError, match="packet digest is stale"):
        store.write(stale)

    malformed = decision(payload)
    malformed["recordedAt"] = "not-a-date"
    with pytest.raises(ValueError, match="schema is invalid"):
        store.write(malformed)


def test_store_rejects_symlink_workspace_escape(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    workspace.mkdir()
    outside.mkdir()
    (workspace / "decisions").symlink_to(outside, target_is_directory=True)
    store = LocalReviewDecisionStore(workspace, CATALOG)

    with pytest.raises(ValueError, match="symlinks"):
        store.write(decision(catalog_payload()))
    assert not list(outside.iterdir())


def test_store_rejects_valid_decision_under_wrong_candidate_path(tmp_path: Path) -> None:
    payload = catalog_payload()
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    first_item = payload["items"][0]  # type: ignore[index]
    second_item = payload["items"][1]  # type: ignore[index]
    recorded = decision(payload)
    recorded["binding"] = {
        "candidateId": second_item["candidateId"],  # type: ignore[index]
        "packetSha256": second_item["packetSha256"],  # type: ignore[index]
    }
    decisions = tmp_path / "workspace" / "decisions"
    decisions.mkdir()
    (decisions / f"{first_item['candidateId']}.json").write_text(  # type: ignore[index]
        json.dumps(recorded, indent=2, sort_keys=True) + "\n"
    )

    with pytest.raises(ValueError, match="differs from storage path"):
        store.current(first_item["candidateId"])  # type: ignore[index]


def test_store_rejects_current_decision_without_immutable_history(tmp_path: Path) -> None:
    payload = catalog_payload()
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    recorded = store.write(decision(payload))
    history = (
        tmp_path
        / "workspace"
        / "history"
        / recorded["candidateId"]
        / f"{recorded['decisionSha256']}.json"
    )
    history.unlink()

    with pytest.raises(ValueError, match="missing immutable history"):
        store.current(recorded["candidateId"])


def test_server_rejects_non_loopback_and_unsafe_write_configuration(tmp_path: Path) -> None:
    base = LocalReviewDecisionServiceOptions(
        workspace=tmp_path / "workspace",
        catalog=CATALOG,
        csrf_token=CSRF_TOKEN,
        allowed_origin=ORIGIN,
    )
    with pytest.raises(ValueError, match="bind"):
        build_local_review_decision_server(
            LocalReviewDecisionServiceOptions(**{**base.__dict__, "host": "0.0.0.0"})
        )
    with pytest.raises(ValueError, match="CSRF"):
        build_local_review_decision_server(
            LocalReviewDecisionServiceOptions(**{**base.__dict__, "csrf_token": "short"})
        )
    with pytest.raises(ValueError, match="allowed origin"):
        build_local_review_decision_server(
            LocalReviewDecisionServiceOptions(
                **{**base.__dict__, "allowed_origin": "https://example.com"}
            )
        )


def test_server_enforces_origin_csrf_and_records_decision(tmp_path: Path) -> None:
    server = build_local_review_decision_server(
        LocalReviewDecisionServiceOptions(
            workspace=tmp_path / "workspace",
            catalog=CATALOG,
            csrf_token=CSRF_TOKEN,
            allowed_origin=ORIGIN,
            port=0,
        )
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    body = json.dumps(decision(catalog_payload()))
    try:
        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.request(
            "POST",
            "/v0/decisions",
            body=body,
            headers={
                "Content-Type": "application/json",
                "Origin": "http://attacker.invalid",
                "X-CSRF-Token": CSRF_TOKEN,
            },
        )
        assert connection.getresponse().status == 403
        connection.close()

        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.request(
            "POST",
            "/v0/decisions",
            body=body,
            headers={
                "Content-Type": "application/json",
                "Origin": ORIGIN,
                "X-CSRF-Token": CSRF_TOKEN,
            },
        )
        response = connection.getresponse()
        recorded = json.loads(response.read())
        assert response.status == 201
        assert recorded["status"] == "recorded"
        connection.close()

        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.request("GET", f"/v0/decisions/{recorded['candidateId']}")
        response = connection.getresponse()
        assert response.status == 200
        assert json.loads(response.read())["decisionSha256"] == recorded["decisionSha256"]
        connection.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
