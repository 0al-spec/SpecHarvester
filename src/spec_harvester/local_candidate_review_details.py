# ruff: noqa: E501

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.local_candidate_review_catalog import (
    LocalCandidateReviewCatalogOptions,
    _catalog_item,
    _json_object,
    _preflight_statuses,
    _read_archive,
)

MAX_DETAIL_DOCUMENT_BYTES = 128 * 1024
DETAIL_API_VERSION = "spec-harvester.candidate-review-detail-set/v0"


@dataclass(frozen=True)
class LocalCandidateReviewDetailsOptions:
    archive: Path
    expected_archive_sha256: str
    catalog: Path
    output: Path


def _catalog_bindings(path: Path) -> dict[str, str]:
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read local review catalog: {exc}") from exc
    items = catalog.get("items") if isinstance(catalog, dict) else None
    if not isinstance(items, list):
        raise ValueError("Local review catalog items are invalid")
    bindings = {
        item.get("candidateId"): item.get("packetSha256")
        for item in items
        if isinstance(item, dict)
    }
    if len(bindings) != len(items) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in bindings.items()
    ):
        raise ValueError("Local review catalog bindings are invalid")
    return bindings


def _detail_documents(
    candidate_id: str, packet: dict[str, Any], members: dict[str, bytes]
) -> list[dict[str, str]]:
    candidate = packet["candidate"]
    documents: list[dict[str, str]] = []
    suffixes = (
        "specpm.yaml",
        ".spec.yaml",
        "diagnostics.json",
        "package-relation-proposals.json",
        "validation-report.json",
    )
    for record in candidate["files"]:
        path = record["path"]
        if not path.endswith(suffixes):
            continue
        payload = members[str(Path("packets") / candidate_id / path)]
        if len(payload) > MAX_DETAIL_DOCUMENT_BYTES:
            documents.append(
                {
                    "path": path,
                    "contentType": "text/plain",
                    "content": "[omitted: bounded detail limit]",
                }
            )
            continue
        documents.append(
            {
                "path": path,
                "contentType": "application/json" if path.endswith(".json") else "application/yaml",
                "content": payload.decode("utf-8", errors="replace"),
            }
        )
    return documents


def build_local_candidate_review_details(
    options: LocalCandidateReviewDetailsOptions,
) -> dict[str, Any]:
    archive_sha256, members = _read_archive(
        LocalCandidateReviewCatalogOptions(
            archive=options.archive,
            expected_archive_sha256=options.expected_archive_sha256,
        )
    )
    aggregate = _json_object(members["aggregate-handoff.json"], "aggregate-handoff.json")
    expectations = _preflight_statuses(aggregate)
    bindings = _catalog_bindings(options.catalog)
    details: list[dict[str, Any]] = []
    for name in sorted(
        name for name in members if name.startswith("packets/") and name.endswith("/packet.json")
    ):
        packet_bytes = members[name]
        _, catalog_item = _catalog_item(name, packet_bytes, expectations, members)
        candidate_id = catalog_item["candidateId"]
        if bindings.get(candidate_id) != catalog_item["packetSha256"]:
            raise ValueError(f"Detail packet binding differs from catalog: {candidate_id}")
        packet = _json_object(packet_bytes, name)
        details.append(
            {
                "apiVersion": "spec-harvester.candidate-review-detail/v0",
                "kind": "SpecHarvesterCandidateReviewDetail",
                "authority": "local_review_detail_evidence_only",
                "binding": {
                    "candidateId": candidate_id,
                    "packetSha256": catalog_item["packetSha256"],
                },
                "previewOnly": True,
                "repository": packet["repository"],
                "candidate": {
                    key: packet["candidate"][key]
                    for key in ("fileCount", "manifestCount", "status")
                },
                "aiProposal": packet["aiProposal"],
                "triage": packet["triage"],
                "documents": _detail_documents(candidate_id, packet, members),
            }
        )
    if set(bindings) != {detail["binding"]["candidateId"] for detail in details}:
        raise ValueError("Detail candidate set differs from catalog")
    payload = {
        "apiVersion": DETAIL_API_VERSION,
        "kind": "SpecHarvesterCandidateReviewDetailSet",
        "authority": "local_review_detail_evidence_only",
        "sourceBundleSha256": archive_sha256,
        "details": details,
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {"status": "passed", "detailCount": len(details), "output": str(options.output)}
