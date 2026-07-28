from __future__ import annotations

import hashlib
import io
import json
import tarfile
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from spec_harvester.cli import main
from spec_harvester.local_candidate_review_catalog import (
    LocalCandidateReviewCatalogOptions,
    build_local_candidate_review_catalog,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/local-candidate-review-workbench-v0.schema.json"
VALID_FIXTURE = (
    ROOT / "tests/fixtures/local_candidate_review_workbench_schemas/p54-t2-valid.example.json"
)


def packet(candidate_id: str, position: int, *, corrected: bool = False) -> dict[str, Any]:
    candidate_payload = f"candidate:{candidate_id}".encode()
    ai_payload = f"ai:{candidate_id}".encode()
    triage: dict[str, Any] = {
        "id": candidate_id,
        "proposal": {"summary": {"warningCount": position - 1}},
    }
    if corrected:
        triage["correction"] = {"task": "P53-T13"}
    return {
        "apiVersion": "spec-harvester.p53-portable-author-handoff-packet/v0",
        "kind": "SpecHarvesterP53PortableAuthorHandoffPacket",
        "authority": "producer_portable_handoff_evidence_only",
        "previewOnly": True,
        "status": "ready_for_author_review",
        "repository": {
            "id": candidate_id,
            "position": position,
            "ecosystem": "python",
            "repositoryShape": "single_package",
        },
        "candidate": {
            "previewOnly": True,
            "fileCount": 1,
            "files": [
                {
                    "path": "candidate/specpm.yaml",
                    "sha256": hashlib.sha256(candidate_payload).hexdigest(),
                }
            ],
        },
        "aiProposal": {
            "path": "ai-proposal.json",
            "sha256": hashlib.sha256(ai_payload).hexdigest(),
            "status": "portable",
        },
        "triage": triage,
    }


def archive_payload(
    packets: list[dict[str, Any]],
    *,
    extra_members: list[tuple[tarfile.TarInfo, bytes]] | None = None,
    aggregate_packet_digest_overrides: dict[str, str] | None = None,
) -> bytes:
    packet_payloads = {
        item["repository"]["id"]: json.dumps(item, sort_keys=True).encode() for item in packets
    }
    aggregate = {
        "selectedCandidates": [
            {
                "id": item["repository"]["id"],
                "producerPreflight": {"status": "passed"},
                "evidenceLinks": [
                    {
                        "role": "portable_packet",
                        "status": "present",
                        "digest": "sha256:"
                        + (aggregate_packet_digest_overrides or {}).get(
                            item["repository"]["id"],
                            hashlib.sha256(packet_payloads[item["repository"]["id"]]).hexdigest(),
                        ),
                    }
                ],
            }
            for item in packets
        ]
    }
    members = [
        ("aggregate-handoff.json", json.dumps(aggregate).encode()),
        *[
            (
                f"packets/{item['repository']['id']}/packet.json",
                packet_payloads[item["repository"]["id"]],
            )
            for item in packets
        ],
        *[
            (
                f"packets/{item['repository']['id']}/candidate/specpm.yaml",
                f"candidate:{item['repository']['id']}".encode(),
            )
            for item in packets
        ],
        *[
            (
                f"packets/{item['repository']['id']}/ai-proposal.json",
                f"ai:{item['repository']['id']}".encode(),
            )
            for item in packets
        ],
    ]
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:gz") as archive:
        for name, payload in members:
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            info.mtime = 0
            archive.addfile(info, io.BytesIO(payload))
        for info, payload in extra_members or []:
            archive.addfile(info, io.BytesIO(payload) if info.isfile() else None)
    return output.getvalue()


def build(tmp_path: Path, payload: bytes, **overrides: Any) -> dict[str, Any]:
    archive = tmp_path / "handoff.tar.gz"
    archive.write_bytes(payload)
    values = {
        "archive": archive,
        "expected_archive_sha256": hashlib.sha256(payload).hexdigest(),
        "expected_packet_count": 2,
    }
    values.update(overrides)
    return build_local_candidate_review_catalog(LocalCandidateReviewCatalogOptions(**values))


def test_catalog_is_deterministic_schema_valid_and_position_ordered(tmp_path: Path) -> None:
    payload = archive_payload([packet("second", 2, corrected=True), packet("first", 1)])

    first = build(tmp_path, payload)
    second = build(tmp_path, payload)

    assert first == second
    assert [item["candidateId"] for item in first["items"]] == ["first", "second"]
    assert first["items"][1]["corrected"] is True
    assert first["items"][1]["warningCount"] == 1
    fixture = json.loads(VALID_FIXTURE.read_text())
    fixture["catalog"] = first
    Draft202012Validator(json.loads(SCHEMA.read_text())).validate(fixture)


def test_catalog_rejects_archive_digest_drift(tmp_path: Path) -> None:
    payload = archive_payload([packet("first", 1), packet("second", 2)])
    with pytest.raises(ValueError, match="SHA-256"):
        build(tmp_path, payload, expected_archive_sha256="0" * 64)


def test_catalog_rejects_missing_archive(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Cannot read portable handoff archive"):
        build_local_candidate_review_catalog(
            LocalCandidateReviewCatalogOptions(
                archive=tmp_path / "missing.tar.gz",
                expected_archive_sha256="0" * 64,
                expected_packet_count=2,
            )
        )


@pytest.mark.parametrize(
    ("member_name", "member_type"),
    [
        ("../outside", tarfile.REGTYPE),
        ("packets/link", tarfile.SYMTYPE),
    ],
)
def test_catalog_rejects_unsafe_paths_and_links(
    tmp_path: Path, member_name: str, member_type: bytes
) -> None:
    info = tarfile.TarInfo(member_name)
    info.type = member_type
    info.size = 1 if member_type == tarfile.REGTYPE else 0
    if member_type == tarfile.SYMTYPE:
        info.linkname = "aggregate-handoff.json"
    payload = archive_payload(
        [packet("first", 1), packet("second", 2)],
        extra_members=[(info, b"x")],
    )

    with pytest.raises(ValueError, match="Unsafe|Unsupported"):
        build(tmp_path, payload)


def test_catalog_rejects_packet_count_and_member_size_limits(tmp_path: Path) -> None:
    payload = archive_payload([packet("first", 1), packet("second", 2)])
    with pytest.raises(ValueError, match="packet count mismatch"):
        build(tmp_path, payload, expected_packet_count=3)
    with pytest.raises(ValueError, match="member exceeds byte limit"):
        build(tmp_path, payload, max_member_bytes=8)
    with pytest.raises(ValueError, match="archive exceeds the configured byte limit"):
        build(tmp_path, payload, max_archive_bytes=len(payload) - 1)
    with pytest.raises(ValueError, match="member limit"):
        build(tmp_path, payload, max_members=1)
    with pytest.raises(ValueError, match="total byte limit"):
        build(tmp_path, payload, max_total_member_bytes=1)


def test_catalog_rejects_packet_identity_path_mismatch(tmp_path: Path) -> None:
    first = packet("first", 1)
    second = packet("second", 2)
    second["triage"]["id"] = "first"
    payload = archive_payload([first, second])

    with pytest.raises(ValueError, match="triage identity mismatch"):
        build(tmp_path, payload)


def test_catalog_rejects_referenced_file_digest_mismatch(tmp_path: Path) -> None:
    first = packet("first", 1)
    first["candidate"]["files"][0]["sha256"] = "0" * 64
    payload = archive_payload([first, packet("second", 2)])

    with pytest.raises(ValueError, match="file SHA-256 mismatch"):
        build(tmp_path, payload)


def test_catalog_rejects_packet_digest_that_does_not_match_aggregate(tmp_path: Path) -> None:
    payload = archive_payload(
        [packet("first", 1), packet("second", 2)],
        aggregate_packet_digest_overrides={"first": "0" * 64},
    )

    with pytest.raises(ValueError, match="does not match aggregate evidence"):
        build(tmp_path, payload)


def test_catalog_rejects_malformed_packet_contracts(tmp_path: Path) -> None:
    cases: list[tuple[dict[str, Any], str]] = []

    bad_contract = packet("first", 1)
    bad_contract["previewOnly"] = False
    cases.append((bad_contract, "contract mismatch"))

    bad_candidate = packet("first", 1)
    bad_candidate["candidate"]["previewOnly"] = False
    cases.append((bad_candidate, "candidate metadata"))

    bad_inventory = packet("first", 1)
    bad_inventory["candidate"]["fileCount"] = 2
    cases.append((bad_inventory, "file inventory"))

    bad_record = packet("first", 1)
    bad_record["candidate"]["files"] = [None]
    cases.append((bad_record, "file record"))

    bad_ai_status = packet("first", 1)
    bad_ai_status["aiProposal"]["status"] = "unknown"
    cases.append((bad_ai_status, "AI proposal status"))

    unsafe_reference = packet("first", 1)
    unsafe_reference["candidate"]["files"][0]["path"] = "../outside"
    cases.append((unsafe_reference, "file path is unsafe"))

    for index, (first, message) in enumerate(cases):
        payload = archive_payload([first, packet("second", 2)])
        case_path = tmp_path / str(index)
        case_path.mkdir()
        with pytest.raises(ValueError, match=message):
            build(case_path, payload)


def test_catalog_rejects_invalid_facets_and_duplicate_positions(tmp_path: Path) -> None:
    cases: list[tuple[dict[str, Any], str]] = []

    bad_readiness = packet("first", 1)
    bad_readiness["status"] = "published"
    cases.append((bad_readiness, "readiness"))

    bad_metadata = packet("first", 1)
    bad_metadata["repository"]["ecosystem"] = ""
    cases.append((bad_metadata, "catalog metadata"))

    bad_warning = packet("first", 1)
    bad_warning["triage"]["proposal"]["summary"]["warningCount"] = -1
    cases.append((bad_warning, "warning count"))

    for index, (first, message) in enumerate(cases):
        payload = archive_payload([first, packet("second", 2)])
        case_path = tmp_path / str(index)
        case_path.mkdir()
        with pytest.raises(ValueError, match=message):
            build(case_path, payload)

    payload = archive_payload([packet("first", 1), packet("second", 1)])
    duplicate_path = tmp_path / "duplicate"
    duplicate_path.mkdir()
    with pytest.raises(ValueError, match="duplicate repository positions"):
        build(duplicate_path, payload)


def test_catalog_rejects_candidate_identity_outside_schema_pattern(tmp_path: Path) -> None:
    payload = archive_payload([packet("bad id", 1), packet("second", 2)])

    with pytest.raises(ValueError, match="candidate identity is invalid"):
        build(tmp_path, payload)


def test_cli_writes_catalog(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = archive_payload([packet("first", 1), packet("second", 2)])
    archive = tmp_path / "handoff.tar.gz"
    output = tmp_path / "catalog.json"
    archive.write_bytes(payload)

    result = main(
        [
            "local-candidate-review-catalog",
            str(archive),
            "--expected-sha256",
            hashlib.sha256(payload).hexdigest(),
            "--expected-packet-count",
            "2",
            "--output",
            str(output),
        ]
    )

    assert result == 0
    assert json.loads(output.read_text())["items"][0]["candidateId"] == "first"
    assert json.loads(capsys.readouterr().out)["candidateCount"] == 2


def test_retained_p53_handoff_builds_schema_valid_100_candidate_catalog() -> None:
    catalog = build_local_candidate_review_catalog(
        LocalCandidateReviewCatalogOptions(
            archive=ROOT / "SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz",
            expected_archive_sha256=(
                "db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63"
            ),
        )
    )

    fixture = json.loads(VALID_FIXTURE.read_text())
    fixture["catalog"] = catalog
    Draft202012Validator(json.loads(SCHEMA.read_text())).validate(fixture)
    assert len(catalog["items"]) == 100
    assert sum(item["corrected"] for item in catalog["items"]) == 2
    assert {item["preflightStatus"] for item in catalog["items"]} == {"passed"}
