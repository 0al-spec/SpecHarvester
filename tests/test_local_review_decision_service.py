from __future__ import annotations

import hashlib
import http.client
import json
import multiprocessing
import threading
from pathlib import Path
from typing import Any

import pytest

import spec_harvester.local_review_decision_service as decision_service
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


def test_store_rolls_back_history_when_current_replacement_is_interrupted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = catalog_payload()
    workspace = tmp_path / "workspace"
    store = LocalReviewDecisionStore(workspace, CATALOG)
    first = store.write(decision(payload))
    before = store.export()
    replacement = decision(
        payload,
        prior=first["decisionSha256"],
        disposition="request_revision",
    )
    original_replace = decision_service.os.replace
    replace_count = 0

    def interrupt_current_replace(source: Path, destination: Path) -> None:
        nonlocal replace_count
        replace_count += 1
        if replace_count == 2:
            raise OSError("simulated interrupted current-decision replace")
        original_replace(source, destination)

    monkeypatch.setattr(decision_service.os, "replace", interrupt_current_replace)
    with pytest.raises(ValueError, match="Cannot persist review decision atomically"):
        store.write(replacement)

    assert replace_count == 2
    assert store.current(first["candidateId"])["decisionSha256"] == first["decisionSha256"]  # type: ignore[index]
    assert store.export() == before
    assert len(list((workspace / "history" / first["candidateId"]).glob("*.json"))) == 1


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
    source.write(decision(payload, prior=first["decisionSha256"], disposition="request_revision"))

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


def test_store_never_creates_an_export_larger_than_import_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = catalog_payload()
    source = LocalReviewDecisionStore(tmp_path / "source", CATALOG)
    source.write(decision(payload))

    monkeypatch.setattr(decision_service, "MAX_EXCHANGE_BYTES", 100)
    with pytest.raises(ValueError, match="export exceeds byte limit"):
        source.export()
    with pytest.raises(ValueError, match="would exceed portable export byte limit"):
        LocalReviewDecisionStore(tmp_path / "target", CATALOG).write(decision(payload))


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

    with pytest.raises(ValueError, match="schema is invalid"):
        LocalReviewDecisionStore(tmp_path / "invalid", CATALOG).import_exchange({})


def test_store_rejects_invalid_action_shapes(tmp_path: Path) -> None:
    payload = catalog_payload()
    candidate_id = payload["items"][0]["candidateId"]  # type: ignore[index]
    store = LocalReviewDecisionStore(tmp_path / "workspace", CATALOG)
    base = {
        "candidateId": candidate_id,
        "disposition": "defer",
        "reviewer": "maintainer@example",
        "reasonCode": "review_deferred",
        "priorDecisionSha256": None,
    }
    with pytest.raises(ValueError, match="unsupported fields"):
        store.record_action({**base, "unexpected": True})
    with pytest.raises(ValueError, match="missing required"):
        store.record_action({"candidateId": candidate_id})
    with pytest.raises(ValueError, match="Unknown review candidate"):
        store.record_action({**base, "candidateId": "unknown"})


def test_store_rejects_noncanonical_and_orphan_history(tmp_path: Path) -> None:
    payload = catalog_payload()
    workspace = tmp_path / "workspace"
    store = LocalReviewDecisionStore(workspace, CATALOG)
    recorded = store.write(decision(payload))
    candidate_id = recorded["candidateId"]
    current = store.current(candidate_id)
    assert current is not None
    history_dir = workspace / "history" / candidate_id
    original = history_dir / f"{recorded['decisionSha256']}.json"

    noncanonical = json.loads(original.read_text())
    noncanonical["recordedAt"] = "2026-07-29T08:00:01Z"
    orphan_payload = (json.dumps(noncanonical, sort_keys=True) + "\n").encode()
    orphan_digest = hashlib.sha256(orphan_payload).hexdigest()
    (history_dir / f"{orphan_digest}.json").write_bytes(orphan_payload)
    with pytest.raises(ValueError, match="not canonical"):
        store.export()

    (history_dir / f"{orphan_digest}.json").write_text(
        json.dumps(noncanonical, indent=2, sort_keys=True) + "\n"
    )
    canonical_digest = hashlib.sha256(
        (json.dumps(noncanonical, indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest()
    (history_dir / f"{orphan_digest}.json").rename(history_dir / f"{canonical_digest}.json")
    with pytest.raises(ValueError, match="orphan records"):
        store.export()


def test_store_rejects_unsafe_workspace_and_corrupt_current_files(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    symlink = tmp_path / "symlink"
    symlink.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="must not be a symlink"):
        LocalReviewDecisionStore(symlink, CATALOG)

    payload = catalog_payload()
    candidate_id = payload["items"][0]["candidateId"]  # type: ignore[index]
    workspace = tmp_path / "workspace"
    store = LocalReviewDecisionStore(workspace, CATALOG)
    with pytest.raises(ValueError, match="component is unsafe"):
        store._path("..")  # noqa: SLF001

    decisions = workspace / "decisions"
    decisions.mkdir()
    current = decisions / f"{candidate_id}.json"
    current.write_text("{not-json")
    with pytest.raises(ValueError, match="invalid JSON"):
        store.current(candidate_id)

    current.write_text("[]")
    with pytest.raises(ValueError, match="must be an object"):
        store.current(candidate_id)

    current.write_bytes(b"x" * (16 * 1024 + 1))
    with pytest.raises(ValueError, match="exceeds byte limit"):
        store.current(candidate_id)

    current.unlink()
    current.mkdir()
    with pytest.raises(ValueError, match="Cannot read persisted"):
        store.current(candidate_id)

    first_with_prior = decision(payload, prior="0" * 64)
    with pytest.raises(ValueError, match="First review decision"):
        LocalReviewDecisionStore(tmp_path / "prior", CATALOG).write(first_with_prior)


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
    with pytest.raises(ValueError, match="port"):
        build_local_review_decision_server(
            LocalReviewDecisionServiceOptions(**{**base.__dict__, "port": -1})
        )
    with pytest.raises(ValueError, match="byte limit"):
        build_local_review_decision_server(
            LocalReviewDecisionServiceOptions(
                **{**base.__dict__, "max_request_bytes": 2 * 1024 * 1024 + 1}
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


def test_server_exposes_actions_progress_and_portable_exchange(tmp_path: Path) -> None:
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
    item = catalog_payload()["items"][0]  # type: ignore[index]

    def request(
        method: str,
        path: str,
        body: object | None = None,
        *,
        csrf: str = CSRF_TOKEN,
        origin: str = ORIGIN,
        content_type: str = "application/json",
    ) -> tuple[int, dict[str, Any]]:
        connection = http.client.HTTPConnection("127.0.0.1", port)
        encoded = None if body is None else json.dumps(body)
        headers = {"Origin": origin}
        if body is not None:
            headers.update(
                {
                    "Content-Type": content_type,
                    "X-CSRF-Token": csrf,
                }
            )
        connection.request(method, path, body=encoded, headers=headers)
        response = connection.getresponse()
        payload = json.loads(response.read())
        connection.close()
        return response.status, payload

    try:
        status, reasons = request("GET", "/v0/reasons")
        assert status == 200
        assert len(reasons["codes"]) == 4
        assert request("GET", "/v0/summary")[1]["unreviewedCount"] == 100
        assert request("GET", "/v0/decisions")[1]["decisions"] == []
        assert request("GET", "/v0/export")[1]["decisions"] == []
        assert request("GET", "/not-found")[0] == 404
        assert request("GET", "/v0/decisions/not-a-candidate")[0] == 400

        action = {
            "candidateId": item["candidateId"],  # type: ignore[index]
            "disposition": "accept_for_intake",
            "reviewer": "maintainer@example",
            "reasonCode": "evidence_verified",
            "notes": "Ready.",
            "priorDecisionSha256": None,
        }
        status, recorded = request("POST", "/v0/actions", action)
        assert status == 201
        assert recorded["status"] == "recorded"
        current = request("GET", "/v0/decisions")[1]["decisions"]
        assert current[0]["decision"]["disposition"] == "accept_for_intake"
        progress = request("GET", "/v0/summary")[1]
        assert progress["reviewedCount"] == 1
        assert progress["unreviewedCount"] == 99
        exported = request("GET", "/v0/export")[1]
        assert exported["decisions"][0]["reasonCode"] == "evidence_verified"
        assert exported["registryMutationCount"] == 0

        invalid = {**action, "reasonCode": "review_deferred"}
        assert request("POST", "/v0/actions", invalid)[0] == 409
        assert request("POST", "/missing", action)[0] == 404
        assert request("POST", "/v0/actions", action, csrf="wrong")[0] == 403
        assert request("POST", "/v0/actions", action, content_type="text/plain")[0] == 415
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_server_imports_valid_portable_exchange(tmp_path: Path) -> None:
    source = LocalReviewDecisionStore(tmp_path / "source", CATALOG)
    source.write(decision(catalog_payload()))
    exchange = source.export()
    server = build_local_review_decision_server(
        LocalReviewDecisionServiceOptions(
            workspace=tmp_path / "target",
            catalog=CATALOG,
            csrf_token=CSRF_TOKEN,
            allowed_origin=ORIGIN,
            port=0,
        )
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    try:
        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.request(
            "POST",
            "/v0/import",
            body=json.dumps(exchange),
            headers={
                "Content-Type": "application/json",
                "Origin": ORIGIN,
                "X-CSRF-Token": CSRF_TOKEN,
            },
        )
        response = connection.getresponse()
        imported = json.loads(response.read())
        assert response.status == 201
        assert imported["decisionCount"] == 1
        assert imported["registryMutationCount"] == 0
        connection.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_server_preflight_and_malformed_requests(tmp_path: Path) -> None:
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

    def raw(
        method: str,
        path: str,
        body: str = "",
        *,
        origin: str = ORIGIN,
    ) -> tuple[int, bytes]:
        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.request(
            method,
            path,
            body=body,
            headers={
                "Content-Type": "application/json",
                "Origin": origin,
                "X-CSRF-Token": CSRF_TOKEN,
            },
        )
        response = connection.getresponse()
        payload = response.read()
        status = response.status
        connection.close()
        return status, payload

    try:
        assert raw("OPTIONS", "/v0/actions")[0] == 204
        assert raw("OPTIONS", "/v0/actions", origin="http://attacker.invalid")[0] == 403
        assert raw("POST", "/v0/actions", "{not-json")[0] == 400
        assert raw("POST", "/v0/actions", "[]")[0] == 400
        second_id = catalog_payload()["items"][1]["candidateId"]  # type: ignore[index]
        assert raw("GET", f"/v0/decisions/{second_id}")[0] == 404
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_server_reports_corrupt_state_and_request_size_errors(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    server = build_local_review_decision_server(
        LocalReviewDecisionServiceOptions(
            workspace=workspace,
            catalog=CATALOG,
            csrf_token=CSRF_TOKEN,
            allowed_origin=ORIGIN,
            port=0,
            max_request_bytes=10,
        )
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    candidate_id = catalog_payload()["items"][0]["candidateId"]  # type: ignore[index]
    decisions = workspace / "decisions"
    decisions.mkdir()
    (decisions / f"{candidate_id}.json").write_text("{broken")
    try:
        for path in ("/v0/summary", "/v0/decisions", "/v0/export"):
            connection = http.client.HTTPConnection("127.0.0.1", port)
            connection.request("GET", path)
            assert connection.getresponse().status == 409
            connection.close()

        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.request(
            "POST",
            "/v0/actions",
            body="01234567890",
            headers={
                "Content-Type": "application/json",
                "Origin": ORIGIN,
                "X-CSRF-Token": CSRF_TOKEN,
            },
        )
        assert connection.getresponse().status == 413
        connection.close()

        connection = http.client.HTTPConnection("127.0.0.1", port)
        connection.putrequest("POST", "/v0/actions")
        connection.putheader("Content-Type", "application/json")
        connection.putheader("Origin", ORIGIN)
        connection.putheader("X-CSRF-Token", CSRF_TOKEN)
        connection.putheader("Content-Length", "invalid")
        connection.endheaders()
        assert connection.getresponse().status == 413
        connection.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
