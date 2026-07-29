from __future__ import annotations

import hashlib
import hmac
import json
import os
import stat
import tempfile
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from jsonschema import Draft202012Validator, FormatChecker

try:
    import fcntl
except ImportError:  # pragma: no cover - service reports unsupported platform
    fcntl = None  # type: ignore[assignment]

from spec_harvester.candidate_review_schema import load_candidate_review_schema
from spec_harvester.local_candidate_review_browser import (
    load_local_candidate_review_catalog,
)

MAX_DECISION_BYTES = 16 * 1024
MAX_EXCHANGE_BYTES = 2 * 1024 * 1024
LOOPBACK_HOST = "127.0.0.1"

REVIEW_REASONS: dict[str, dict[str, str]] = {
    "accept_for_intake": {
        "evidence_verified": "Evidence verified",
    },
    "request_revision": {
        "evidence_revision_required": "Evidence needs revision",
    },
    "defer": {
        "review_deferred": "Review deferred",
    },
    "do_not_promote": {
        "promotion_not_suitable": "Not suitable for promotion",
    },
}


@dataclass(frozen=True)
class LocalReviewDecisionServiceOptions:
    workspace: Path
    catalog: Path
    csrf_token: str
    allowed_origin: str
    host: str = LOOPBACK_HOST
    port: int = 8765
    max_request_bytes: int = MAX_EXCHANGE_BYTES


def _json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def decision_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _is_rfc3339(value: Any) -> bool:
    if not isinstance(value, str) or "T" not in value:
        return False
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.tzinfo is not None


class LocalReviewDecisionStore:
    def __init__(self, workspace: Path, catalog: Path) -> None:
        if workspace.is_symlink():
            raise ValueError("Review workspace must not be a symlink")
        workspace.mkdir(parents=True, exist_ok=True)
        self._root = workspace.resolve()
        if not self._root.is_dir():
            raise ValueError("Review workspace must be a directory")
        self._catalog = load_local_candidate_review_catalog(catalog)
        self._bindings = {
            item["candidateId"]: item["packetSha256"] for item in self._catalog["items"]
        }
        schema = load_candidate_review_schema()
        self._validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self._lock = threading.Lock()

    @property
    def source_bundle_sha256(self) -> str:
        return str(self._catalog["sourceBundleSha256"])

    def reasons(self) -> dict[str, Any]:
        return {
            "apiVersion": "spec-harvester.candidate-review-reasons/v0",
            "kind": "SpecHarvesterCandidateReviewReasons",
            "codes": [
                {
                    "code": code,
                    "allowedDispositions": [disposition],
                    "label": label,
                }
                for disposition, codes in REVIEW_REASONS.items()
                for code, label in codes.items()
            ],
        }

    def _path(self, *parts: str) -> Path:
        if any(not part or part in {".", ".."} or "/" in part or "\\" in part for part in parts):
            raise ValueError("Review workspace path component is unsafe")
        target = self._root.joinpath(*parts)
        current = self._root
        for part in parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("Review workspace path must not contain symlinks")
        resolved = target.resolve(strict=False)
        try:
            resolved.relative_to(self._root)
        except ValueError as exc:
            raise ValueError("Review workspace path escapes configured root") from exc
        return target

    def _validate(self, decision: dict[str, Any]) -> tuple[str, str]:
        errors = list(self._validator.iter_errors(decision))
        if errors:
            raise ValueError(f"Review decision schema is invalid: {errors[0].message}")
        if decision.get("kind") != "SpecHarvesterCandidateReviewDecision":
            raise ValueError("Submitted record is not a review decision")
        if not _is_rfc3339(decision["recordedAt"]):
            raise ValueError("Review decision schema is invalid: recordedAt is not RFC 3339")
        binding = decision["binding"]
        candidate_id = binding["candidateId"]
        expected_digest = self._bindings.get(candidate_id)
        if expected_digest is None:
            raise ValueError(f"Unknown review candidate: {candidate_id}")
        if binding["packetSha256"] != expected_digest:
            raise ValueError(f"Review decision packet digest is stale: {candidate_id}")
        disposition = decision["disposition"]
        if decision["reasonCode"] not in REVIEW_REASONS[disposition]:
            raise ValueError(f"Review reason is not allowed for disposition: {disposition}")
        return candidate_id, expected_digest

    def _read_path(self, path: Path) -> tuple[dict[str, Any], bytes]:
        try:
            with path.open("rb") as source:
                payload = source.read(MAX_DECISION_BYTES + 1)
        except OSError as exc:
            raise ValueError(f"Cannot read persisted review decision: {exc}") from exc
        if len(payload) > MAX_DECISION_BYTES:
            raise ValueError("Persisted review decision exceeds byte limit")
        try:
            value = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Persisted review decision is invalid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError("Persisted review decision must be an object")
        self._validate(value)
        if payload != _json_bytes(value):
            raise ValueError("Persisted review decision is not canonical")
        return value, payload

    def current(self, candidate_id: str) -> dict[str, Any] | None:
        expected_digest = self._bindings.get(candidate_id)
        if expected_digest is None:
            raise ValueError(f"Unknown review candidate: {candidate_id}")
        path = self._path("decisions", f"{candidate_id}.json")
        if not path.exists():
            return None
        value, payload = self._read_path(path)
        binding = value["binding"]
        if binding["candidateId"] != candidate_id or binding["packetSha256"] != expected_digest:
            raise ValueError("Persisted review decision binding differs from storage path")
        digest = hashlib.sha256(payload).hexdigest()
        history_path = self._path("history", candidate_id, f"{digest}.json")
        if not history_path.exists():
            raise ValueError("Persisted review decision is missing immutable history")
        _, history_payload = self._read_path(history_path)
        if history_payload != payload:
            raise ValueError("Persisted review decision differs from immutable history")
        return {
            "decision": value,
            "decisionSha256": digest,
            "packetSha256": expected_digest,
        }

    def _atomic_write(self, path: Path, payload: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path(*path.relative_to(self._root).parts)
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=path.parent, prefix=".decision-", delete=False
            ) as output:
                temporary = Path(output.name)
                output.write(payload)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, path)
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError as exc:
            raise ValueError(f"Cannot persist review decision atomically: {exc}") from exc
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()

    @contextmanager
    def _workspace_write_lock(self) -> Iterator[None]:
        if fcntl is None:
            raise ValueError("Review workspace process locking is unavailable on this platform")
        path = self._path(".decision-write.lock")
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(path, flags, 0o600)
        except OSError as exc:
            raise ValueError(f"Cannot open review workspace write lock: {exc}") from exc
        locked = False
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise ValueError("Review workspace write lock must be a regular file")
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            locked = True
            yield
        except OSError as exc:
            raise ValueError(f"Cannot lock review workspace writes: {exc}") from exc
        finally:
            if locked:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def write(self, decision: dict[str, Any]) -> dict[str, Any]:
        candidate_id, packet_sha256 = self._validate(decision)
        payload = _json_bytes(decision)
        if len(payload) > MAX_DECISION_BYTES:
            raise ValueError("Review decision exceeds byte limit")
        digest = hashlib.sha256(payload).hexdigest()
        with self._lock, self._workspace_write_lock():
            current = self.current(candidate_id)
            prior = decision["priorDecisionSha256"]
            if current is None and prior is not None:
                raise ValueError("First review decision must have a null prior digest")
            if current is not None and prior != current["decisionSha256"]:
                raise ValueError("Review decision prior digest is stale")
            history = self._path("history", candidate_id, f"{digest}.json")
            if history.exists():
                _, history_payload = self._read_path(history)
                if history_payload != payload:
                    raise ValueError("Review decision history digest collision")
            else:
                self._atomic_write(history, payload)
            self._atomic_write(self._path("decisions", f"{candidate_id}.json"), payload)
        return {
            "status": "recorded",
            "candidateId": candidate_id,
            "packetSha256": packet_sha256,
            "decisionSha256": digest,
            "priorDecisionSha256": prior,
            "authority": "local_review_decision_evidence_only",
        }

    def record_action(self, action: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "candidateId",
            "disposition",
            "reviewer",
            "reasonCode",
            "notes",
            "priorDecisionSha256",
        }
        if set(action) - allowed:
            raise ValueError("Review action contains unsupported fields")
        required = allowed - {"notes"}
        if not required.issubset(action):
            raise ValueError("Review action is missing required fields")
        candidate_id = action["candidateId"]
        if not isinstance(candidate_id, str) or candidate_id not in self._bindings:
            raise ValueError(f"Unknown review candidate: {candidate_id}")
        decision = {
            "apiVersion": "spec-harvester.candidate-review-decision/v0",
            "kind": "SpecHarvesterCandidateReviewDecision",
            "authority": "local_review_decision_evidence_only",
            "binding": {
                "candidateId": candidate_id,
                "packetSha256": self._bindings[candidate_id],
            },
            "disposition": action["disposition"],
            "reviewer": action["reviewer"],
            "recordedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "reasonCode": action["reasonCode"],
            "priorDecisionSha256": action["priorDecisionSha256"],
        }
        if "notes" in action and action["notes"]:
            decision["notes"] = action["notes"]
        return self.write(decision)

    def _history(self, candidate_id: str) -> list[dict[str, Any]]:
        current = self.current(candidate_id)
        if current is None:
            return []
        directory = self._path("history", candidate_id)
        records: dict[str, dict[str, Any]] = {}
        for path in directory.glob("*.json"):
            value, payload = self._read_path(path)
            digest = hashlib.sha256(payload).hexdigest()
            if path.name != f"{digest}.json":
                raise ValueError("Review decision history filename is not its digest")
            if value["binding"]["candidateId"] != candidate_id:
                raise ValueError("Review decision history candidate binding is invalid")
            records[digest] = value
        chain: list[dict[str, Any]] = []
        current_digest: str | None = current["decisionSha256"]
        visited: set[str] = set()
        while current_digest is not None:
            if current_digest in visited or current_digest not in records:
                raise ValueError("Review decision history chain is invalid")
            visited.add(current_digest)
            value = records[current_digest]
            chain.append(value)
            current_digest = value["priorDecisionSha256"]
        if visited != set(records):
            raise ValueError("Review decision history contains orphan records")
        return list(reversed(chain))

    def summary(self) -> dict[str, Any]:
        counts = {disposition: 0 for disposition in REVIEW_REASONS}
        reviewed = 0
        for candidate_id in sorted(self._bindings):
            current = self.current(candidate_id)
            if current is not None:
                reviewed += 1
                counts[current["decision"]["disposition"]] += 1
        total = len(self._bindings)
        return {
            "status": "ok",
            "candidateCount": total,
            "reviewedCount": reviewed,
            "unreviewedCount": total - reviewed,
            "dispositionCounts": counts,
            "sourceBundleSha256": self.source_bundle_sha256,
            "authority": "local_review_decision_evidence_only",
        }

    def current_decisions(self) -> dict[str, Any]:
        records = [
            current
            for candidate_id in sorted(self._bindings)
            if (current := self.current(candidate_id)) is not None
        ]
        return {
            "status": "ok",
            "decisions": records,
            "sourceBundleSha256": self.source_bundle_sha256,
            "authority": "local_review_decision_evidence_only",
        }

    def export(self) -> dict[str, Any]:
        decisions = [
            decision
            for candidate_id in sorted(self._bindings)
            for decision in self._history(candidate_id)
        ]
        return {
            "apiVersion": "spec-harvester.candidate-review-export/v0",
            "kind": "SpecHarvesterCandidateReviewExport",
            "authority": "portable_local_review_evidence_only",
            "sourceBundleSha256": self.source_bundle_sha256,
            "decisions": decisions,
            "registryMutationCount": 0,
        }

    def import_exchange(self, exchange: dict[str, Any]) -> dict[str, Any]:
        errors = list(self._validator.iter_errors(exchange))
        if errors or exchange.get("kind") != "SpecHarvesterCandidateReviewExport":
            message = errors[0].message if errors else "record is not a review export"
            raise ValueError(f"Portable review export schema is invalid: {message}")
        if exchange["sourceBundleSha256"] != self.source_bundle_sha256:
            raise ValueError("Portable review export source bundle digest is stale")
        simulated = {
            candidate_id: (
                current["decisionSha256"] if (current := self.current(candidate_id)) else None
            )
            for candidate_id in self._bindings
        }
        validated: list[dict[str, Any]] = []
        for decision in exchange["decisions"]:
            candidate_id, _ = self._validate(decision)
            expected_prior = simulated[candidate_id]
            if decision["priorDecisionSha256"] != expected_prior:
                raise ValueError(
                    f"Portable review export history is stale or out of order: {candidate_id}"
                )
            simulated[candidate_id] = decision_sha256(decision)
            validated.append(decision)
        for decision in validated:
            self.write(decision)
        return {
            "status": "imported",
            "decisionCount": len(validated),
            "sourceBundleSha256": self.source_bundle_sha256,
            "registryMutationCount": 0,
        }


def _valid_origin(origin: str) -> bool:
    parsed = urlparse(origin)
    return (
        parsed.scheme == "http"
        and parsed.hostname in {"127.0.0.1", "localhost"}
        and parsed.username is None
        and parsed.password is None
        and parsed.path in {"", "/"}
        and not parsed.query
        and not parsed.fragment
    )


def build_local_review_decision_server(
    options: LocalReviewDecisionServiceOptions,
) -> ThreadingHTTPServer:
    if options.host != LOOPBACK_HOST:
        raise ValueError("Review decision service must bind to 127.0.0.1")
    if not 0 <= options.port <= 65535:
        raise ValueError("Review decision service port is invalid")
    if len(options.csrf_token) < 32:
        raise ValueError("Review decision service CSRF token must contain at least 32 characters")
    if not _valid_origin(options.allowed_origin):
        raise ValueError("Review decision service allowed origin must be local HTTP")
    if not 1 <= options.max_request_bytes <= MAX_EXCHANGE_BYTES:
        raise ValueError("Review decision service request byte limit is invalid")
    store = LocalReviewDecisionStore(options.workspace, options.catalog)

    class DecisionHandler(BaseHTTPRequestHandler):
        server_version = "SpecHarvesterLocalReview/0"

        def _cors(self) -> None:
            self.send_header("Access-Control-Allow-Origin", options.allowed_origin)
            self.send_header("Vary", "Origin")

        def _json(self, status: int, value: dict[str, Any]) -> None:
            payload = _json_bytes(value)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self._cors()
            self.end_headers()
            self.wfile.write(payload)

        def _origin_allowed(self) -> bool:
            return self.headers.get("Origin") == options.allowed_origin

        def do_OPTIONS(self) -> None:  # noqa: N802
            if not self._origin_allowed():
                self._json(403, {"status": "error", "message": "Origin is not allowed"})
                return
            self.send_response(204)
            self._cors()
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-CSRF-Token")
            self.send_header("Access-Control-Max-Age", "60")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/v0/reasons":
                self._json(200, store.reasons())
                return
            if self.path == "/v0/summary":
                try:
                    self._json(200, store.summary())
                except ValueError as exc:
                    self._json(409, {"status": "error", "message": str(exc)})
                return
            if self.path == "/v0/decisions":
                try:
                    self._json(200, store.current_decisions())
                except ValueError as exc:
                    self._json(409, {"status": "error", "message": str(exc)})
                return
            if self.path == "/v0/export":
                try:
                    self._json(200, store.export())
                except ValueError as exc:
                    self._json(409, {"status": "error", "message": str(exc)})
                return
            prefix = "/v0/decisions/"
            if not self.path.startswith(prefix):
                self._json(404, {"status": "error", "message": "Not found"})
                return
            candidate_id = unquote(self.path[len(prefix) :])
            try:
                current = store.current(candidate_id)
            except ValueError as exc:
                self._json(400, {"status": "error", "message": str(exc)})
                return
            if current is None:
                self._json(404, {"status": "not_found", "candidateId": candidate_id})
                return
            self._json(200, {"status": "found", **current})

        def do_POST(self) -> None:  # noqa: N802
            if self.path not in {"/v0/decisions", "/v0/actions", "/v0/import"}:
                self._json(404, {"status": "error", "message": "Not found"})
                return
            if not self._origin_allowed():
                self._json(403, {"status": "error", "message": "Origin is not allowed"})
                return
            supplied_token = self.headers.get("X-CSRF-Token", "")
            if not hmac.compare_digest(supplied_token, options.csrf_token):
                self._json(403, {"status": "error", "message": "CSRF token is invalid"})
                return
            if self.headers.get_content_type() != "application/json":
                self._json(
                    415, {"status": "error", "message": "Content-Type must be application/json"}
                )
                return
            try:
                length = int(self.headers.get("Content-Length", ""))
            except ValueError:
                length = -1
            if not 0 <= length <= options.max_request_bytes:
                self._json(413, {"status": "error", "message": "Request body exceeds byte limit"})
                return
            payload = self.rfile.read(length)
            try:
                submitted = json.loads(payload)
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._json(400, {"status": "error", "message": "Request body is invalid JSON"})
                return
            if not isinstance(submitted, dict):
                self._json(400, {"status": "error", "message": "Request body must be an object"})
                return
            try:
                if self.path == "/v0/actions":
                    result = store.record_action(submitted)
                elif self.path == "/v0/import":
                    result = store.import_exchange(submitted)
                else:
                    result = store.write(submitted)
            except ValueError as exc:
                self._json(409, {"status": "error", "message": str(exc)})
                return
            self._json(201, result)

        def log_message(self, _format: str, *args: object) -> None:
            return

    return ThreadingHTTPServer((options.host, options.port), DecisionHandler)


def serve_local_review_decisions(options: LocalReviewDecisionServiceOptions) -> None:
    server = build_local_review_decision_server(options)
    try:
        server.serve_forever()
    finally:
        server.server_close()
