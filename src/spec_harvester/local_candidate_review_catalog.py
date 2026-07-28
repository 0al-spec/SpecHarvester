from __future__ import annotations

import hashlib
import json
import tarfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

CATALOG_API_VERSION = "spec-harvester.candidate-review-catalog/v0"
PACKET_API_VERSION = "spec-harvester.p53-portable-author-handoff-packet/v0"
PACKET_KIND = "SpecHarvesterP53PortableAuthorHandoffPacket"
PACKET_AUTHORITY = "producer_portable_handoff_evidence_only"
AGGREGATE_MEMBER = "aggregate-handoff.json"


@dataclass(frozen=True)
class LocalCandidateReviewCatalogOptions:
    archive: Path
    expected_archive_sha256: str
    expected_packet_count: int = 100
    max_archive_bytes: int = 512 * 1024 * 1024
    max_member_bytes: int = 32 * 1024 * 1024
    max_members: int = 10_000
    max_total_member_bytes: int = 512 * 1024 * 1024


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_archive(options: LocalCandidateReviewCatalogOptions) -> tuple[str, dict[str, bytes]]:
    try:
        archive_bytes = options.archive.read_bytes()
    except OSError as exc:
        raise ValueError(f"Cannot read portable handoff archive: {exc}") from exc
    if len(archive_bytes) > options.max_archive_bytes:
        raise ValueError("Portable handoff archive exceeds the configured byte limit")

    archive_sha256 = _sha256(archive_bytes)
    if archive_sha256 != options.expected_archive_sha256:
        raise ValueError("Portable handoff archive SHA-256 does not match the expected digest")

    members: dict[str, bytes] = {}
    total_bytes = 0
    try:
        with tarfile.open(options.archive, mode="r:gz") as archive:
            infos = archive.getmembers()
            if len(infos) > options.max_members:
                raise ValueError("Portable handoff archive exceeds the configured member limit")
            for info in infos:
                path = PurePosixPath(info.name)
                if path.is_absolute() or ".." in path.parts or not path.parts:
                    raise ValueError(f"Unsafe portable handoff member path: {info.name}")
                if info.isdir():
                    continue
                if not info.isfile():
                    raise ValueError(f"Unsupported portable handoff member type: {info.name}")
                if info.name in members:
                    raise ValueError(f"Duplicate portable handoff member: {info.name}")
                if info.size > options.max_member_bytes:
                    raise ValueError(f"Portable handoff member exceeds byte limit: {info.name}")
                total_bytes += info.size
                if total_bytes > options.max_total_member_bytes:
                    raise ValueError(
                        "Portable handoff payload exceeds the configured total byte limit"
                    )
                reader = archive.extractfile(info)
                if reader is None:
                    raise ValueError(f"Cannot read portable handoff member: {info.name}")
                payload = reader.read(options.max_member_bytes + 1)
                if len(payload) != info.size:
                    raise ValueError(f"Portable handoff member size mismatch: {info.name}")
                members[info.name] = payload
    except (OSError, tarfile.TarError) as exc:
        raise ValueError(f"Invalid portable handoff archive: {exc}") from exc
    return archive_sha256, members


def _json_object(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid JSON in {label}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return value


def _preflight_statuses(aggregate: dict[str, Any]) -> dict[str, str]:
    selected = aggregate.get("selectedCandidates")
    if not isinstance(selected, list):
        raise ValueError("Aggregate handoff selectedCandidates must be an array")
    statuses: dict[str, str] = {}
    for record in selected:
        if not isinstance(record, dict):
            raise ValueError("Aggregate handoff candidate must be an object")
        candidate_id = record.get("id")
        preflight = record.get("producerPreflight")
        status = preflight.get("status") if isinstance(preflight, dict) else None
        if not isinstance(candidate_id, str) or status not in {"passed", "warning", "error"}:
            raise ValueError("Aggregate handoff candidate has invalid preflight metadata")
        if candidate_id in statuses:
            raise ValueError(f"Duplicate aggregate handoff candidate: {candidate_id}")
        statuses[candidate_id] = status
    return statuses


def _validate_digest(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError(f"Invalid SHA-256 for {label}")
    return value


def _validate_packet_files(
    candidate_id: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
) -> None:
    candidate = packet.get("candidate")
    if not isinstance(candidate, dict) or candidate.get("previewOnly") is not True:
        raise ValueError(f"Packet candidate metadata is invalid: {candidate_id}")
    files = candidate.get("files")
    if not isinstance(files, list) or candidate.get("fileCount") != len(files):
        raise ValueError(f"Packet candidate file inventory is invalid: {candidate_id}")

    references: list[tuple[Any, Any]] = []
    for record in files:
        if not isinstance(record, dict):
            raise ValueError(f"Packet candidate file record is invalid: {candidate_id}")
        references.append((record.get("path"), record.get("sha256")))
    ai_proposal = packet.get("aiProposal")
    if not isinstance(ai_proposal, dict):
        raise ValueError(f"Packet AI proposal metadata is invalid: {candidate_id}")
    ai_status = ai_proposal.get("status")
    if ai_status == "portable":
        references.append((ai_proposal.get("path"), ai_proposal.get("sha256")))
    elif ai_status == "summary_only_not_portable":
        _validate_digest(ai_proposal.get("expectedSha256"), f"{candidate_id} expected AI proposal")
    else:
        raise ValueError(f"Packet AI proposal status is invalid: {candidate_id}")

    seen_paths: set[str] = set()
    for relative_name, digest in references:
        if not isinstance(relative_name, str):
            raise ValueError(f"Packet file path is invalid: {candidate_id}")
        relative_path = PurePosixPath(relative_name)
        if relative_path.is_absolute() or ".." in relative_path.parts or not relative_path.parts:
            raise ValueError(f"Packet file path is unsafe: {candidate_id}/{relative_name}")
        if relative_name in seen_paths:
            raise ValueError(f"Packet file path is duplicated: {candidate_id}/{relative_name}")
        seen_paths.add(relative_name)
        archive_name = str(PurePosixPath("packets", candidate_id, relative_name))
        payload = members.get(archive_name)
        if payload is None:
            raise ValueError(f"Packet file is missing: {archive_name}")
        if _sha256(payload) != _validate_digest(digest, archive_name):
            raise ValueError(f"Packet file SHA-256 mismatch: {archive_name}")


def _catalog_item(
    member_name: str,
    packet_bytes: bytes,
    preflight_statuses: dict[str, str],
    members: dict[str, bytes],
) -> tuple[int, dict[str, Any]]:
    packet = _json_object(packet_bytes, member_name)
    if (
        packet.get("apiVersion") != PACKET_API_VERSION
        or packet.get("kind") != PACKET_KIND
        or packet.get("authority") != PACKET_AUTHORITY
        or packet.get("previewOnly") is not True
    ):
        raise ValueError(f"Packet contract mismatch: {member_name}")

    repository = packet.get("repository")
    triage = packet.get("triage")
    if not isinstance(repository, dict) or not isinstance(triage, dict):
        raise ValueError(f"Packet repository or triage metadata is invalid: {member_name}")
    candidate_id = repository.get("id")
    expected_parts = ("packets", candidate_id, "packet.json")
    if not isinstance(candidate_id, str) or PurePosixPath(member_name).parts != expected_parts:
        raise ValueError(f"Packet identity does not match its archive path: {member_name}")
    if triage.get("id") != candidate_id:
        raise ValueError(f"Packet triage identity mismatch: {member_name}")
    _validate_packet_files(candidate_id, packet, members)

    readiness = packet.get("status")
    if readiness not in {"ready_for_author_review", "blocked"}:
        raise ValueError(f"Packet readiness is invalid: {member_name}")
    ecosystem = repository.get("ecosystem")
    package_shape = repository.get("repositoryShape")
    position = repository.get("position")
    if (
        not isinstance(ecosystem, str)
        or not ecosystem
        or not isinstance(package_shape, str)
        or not package_shape
        or not isinstance(position, int)
        or isinstance(position, bool)
        or position < 1
    ):
        raise ValueError(f"Packet catalog metadata is invalid: {member_name}")

    proposal = triage.get("proposal")
    summary = proposal.get("summary") if isinstance(proposal, dict) else None
    warning_count = summary.get("warningCount") if isinstance(summary, dict) else None
    if not isinstance(warning_count, int) or isinstance(warning_count, bool) or warning_count < 0:
        raise ValueError(f"Packet warning count is invalid: {member_name}")
    if candidate_id not in preflight_statuses:
        raise ValueError(f"Packet is missing aggregate preflight metadata: {member_name}")

    return position, {
        "candidateId": candidate_id,
        "packetSha256": _sha256(packet_bytes),
        "reviewState": "unreviewed",
        "readiness": readiness,
        "ecosystem": ecosystem,
        "packageShape": package_shape,
        "warningCount": warning_count,
        "corrected": "correction" in triage,
        "preflightStatus": preflight_statuses[candidate_id],
    }


def build_local_candidate_review_catalog(
    options: LocalCandidateReviewCatalogOptions,
) -> dict[str, Any]:
    archive_sha256, members = _read_archive(options)
    aggregate_bytes = members.get(AGGREGATE_MEMBER)
    if aggregate_bytes is None:
        raise ValueError(f"Portable handoff archive is missing {AGGREGATE_MEMBER}")
    preflight_statuses = _preflight_statuses(_json_object(aggregate_bytes, AGGREGATE_MEMBER))

    packet_names = sorted(
        name
        for name in members
        if len(PurePosixPath(name).parts) == 3
        and PurePosixPath(name).parts[0] == "packets"
        and PurePosixPath(name).name == "packet.json"
    )
    if len(packet_names) != options.expected_packet_count:
        raise ValueError(
            "Portable handoff packet count mismatch: "
            f"expected {options.expected_packet_count}, found {len(packet_names)}"
        )

    positioned_items = [
        _catalog_item(name, members[name], preflight_statuses, members) for name in packet_names
    ]
    positions = [position for position, _ in positioned_items]
    candidate_ids = [item["candidateId"] for _, item in positioned_items]
    if len(set(positions)) != len(positions):
        raise ValueError("Portable handoff packets contain duplicate repository positions")
    if len(set(candidate_ids)) != len(candidate_ids):
        raise ValueError("Portable handoff packets contain duplicate candidate identities")
    if set(candidate_ids) != set(preflight_statuses):
        raise ValueError("Packet and aggregate handoff candidate sets do not match")

    return {
        "apiVersion": CATALOG_API_VERSION,
        "kind": "SpecHarvesterCandidateReviewCatalog",
        "authority": "local_review_catalog_evidence_only",
        "sourceBundleSha256": archive_sha256,
        "items": [item for _, item in sorted(positioned_items, key=lambda pair: pair[0])],
    }


def write_local_candidate_review_catalog(path: Path, catalog: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n", encoding="utf-8")
