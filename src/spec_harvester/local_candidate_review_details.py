# ruff: noqa: E501

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from spec_harvester.candidate_review_schema import load_candidate_review_schema
from spec_harvester.local_candidate_review_catalog import (
    LocalCandidateReviewCatalogOptions,
    _catalog_item,
    _json_object,
    _preflight_statuses,
    _read_archive,
)
from spec_harvester.portable_semantic_proposal import (
    MAX_PORTABLE_SEMANTIC_RECORD_BYTES,
    validate_portable_semantic_proposal,
)

MAX_DETAIL_DOCUMENT_BYTES = 128 * 1024
DETAIL_API_VERSION = "spec-harvester.candidate-review-detail-set/v0"


@dataclass(frozen=True)
class LocalCandidateReviewDetailsOptions:
    archive: Path
    expected_archive_sha256: str
    catalog: Path
    output: Path
    semantic_campaign_archive: Path | None = None
    expected_semantic_campaign_sha256: str | None = None
    semantic_follow_up_archive: Path | None = None
    expected_semantic_follow_up_sha256: str | None = None
    semantic_recovery_archive: Path | None = None
    expected_semantic_recovery_sha256: str | None = None


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


def _section(section_id: str, content_type: str, content: str) -> dict[str, str]:
    return {"id": section_id, "contentType": content_type, "content": content}


def _json_section(section_id: str, value: Any) -> dict[str, str]:
    return _section(section_id, "application/json", json.dumps(value, indent=2, sort_keys=True))


def _detail_sections(
    candidate_id: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
    campaign_record: dict[str, Any] | None = None,
    campaign_source: str | None = None,
) -> list[dict[str, str]]:
    candidate = packet["candidate"]
    packet_member = str(Path("packets") / candidate_id / "packet.json")
    try:
        packet_content = members[packet_member].decode("utf-8")
    except (KeyError, UnicodeDecodeError) as exc:
        raise ValueError(f"Packet binding content is invalid: {candidate_id}") from exc
    sections = [
        _section("packet-binding.json", "application/json", packet_content),
        _json_section("source-provenance", packet["repository"]),
        _json_section(
            "package-topology",
            {key: candidate[key] for key in ("fileCount", "manifestCount", "status")},
        ),
        _json_section("static-evidence-inventory", candidate["files"]),
        _json_section("triage-and-diagnostics", packet["triage"]),
    ]
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
            sections.append(_section(path, "text/plain", "[omitted: bounded detail limit]"))
            continue
        sections.append(
            _section(
                path,
                "application/json" if path.endswith(".json") else "application/yaml",
                payload.decode("utf-8", errors="replace"),
            )
        )
    semantic = _semantic_record(candidate_id, packet, members, campaign_record)
    if semantic is not None:
        sections.append(_json_section("semantic-proposal-record", semantic))
    if campaign_record is not None:
        sections.append(
            _json_section(
                "semantic-campaign-provenance",
                {
                    "source": campaign_source,
                    "campaignInputSha256": campaign_record["campaignInputSha256"],
                    "recordSha256": campaign_record["recordSha256"],
                },
            )
        )
        sections.append(_json_section("semantic-campaign-record", campaign_record))
    return sections


def _semantic_record(
    candidate_id: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
    campaign_record: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if campaign_record is not None:
        portable = campaign_record.get("portableProposal")
        if portable is None:
            return None
        if not isinstance(portable, dict):
            raise ValueError(f"Semantic campaign portable proposal is invalid: {candidate_id}")
        validate_portable_semantic_proposal(portable)
        return portable
    binding = packet.get("semanticProposal")
    if not isinstance(binding, dict) or binding.get("status") == "not_available":
        return None
    if binding.get("status") != "complete_portable" or binding.get("path") != (
        "semantic-proposal-record.json"
    ):
        raise ValueError(f"Semantic proposal binding is invalid: {candidate_id}")
    member_name = str(Path("packets") / candidate_id / binding["path"])
    payload = members.get(member_name)
    if payload is None or sha256(payload).hexdigest() != binding.get("sha256"):
        raise ValueError(f"Semantic proposal member digest differs from packet: {candidate_id}")
    if len(payload) > MAX_PORTABLE_SEMANTIC_RECORD_BYTES:
        raise ValueError(f"Semantic proposal exceeds bounded detail limit: {candidate_id}")
    record = _json_object(payload, member_name)
    validate_portable_semantic_proposal(record)
    expected = {
        "recordSha256": record["recordSha256"],
        "proposalSha256": record["proposalSha256"],
        "providerReceiptSha256": record["providerReceiptSha256"],
        "qualityReportSha256": record["qualityReportSha256"],
        "qualityStatus": record["qualityStatus"],
    }
    if any(binding.get(key) != value for key, value in expected.items()):
        raise ValueError(f"Semantic proposal record binding differs from packet: {candidate_id}")
    return record


def _static_semantics(
    candidate_id: str, packet: dict[str, Any], members: dict[str, bytes]
) -> dict[str, Any]:
    summaries: list[str] = []
    capabilities: list[dict[str, Any]] = []
    intents: set[str] = set()
    interfaces: list[str] = []
    evidence: list[str] = []
    for file_record in packet["candidate"]["files"]:
        path = file_record["path"]
        if not path.endswith(("specpm.yaml", ".spec.yaml")):
            continue
        member_name = str(Path("packets") / candidate_id / path)
        try:
            document = yaml.safe_load(members[member_name])
        except (KeyError, yaml.YAMLError) as exc:
            raise ValueError(f"Static semantic YAML is invalid: {candidate_id}/{path}") from exc
        if not isinstance(document, dict):
            raise ValueError(f"Static semantic YAML must be an object: {candidate_id}/{path}")
        metadata = document.get("metadata")
        if isinstance(metadata, dict) and isinstance(metadata.get("summary"), str):
            summaries.append(metadata["summary"])
        intent = document.get("intent")
        if isinstance(intent, dict) and isinstance(intent.get("summary"), str):
            summaries.append(intent["summary"])
        provides = document.get("provides")
        if not isinstance(provides, dict):
            index = document.get("index")
            provides = index.get("provides") if isinstance(index, dict) else None
        if isinstance(provides, dict):
            for intent_id in provides.get("intents", []):
                if isinstance(intent_id, str):
                    intents.add(intent_id)
            for capability in provides.get("capabilities", []):
                if isinstance(capability, str):
                    capabilities.append({"id": capability, "summary": "", "intentIds": []})
                    continue
                if not isinstance(capability, dict) or not isinstance(capability.get("id"), str):
                    continue
                intent_ids = [
                    item for item in capability.get("intentIds", []) if isinstance(item, str)
                ]
                intents.update(intent_ids)
                capabilities.append(
                    {
                        "id": capability["id"],
                        "summary": (
                            capability.get("summary")
                            if isinstance(capability.get("summary"), str)
                            else ""
                        ),
                        "intentIds": intent_ids,
                    }
                )
        for key in ("interfaces", "exposes"):
            values = document.get(key)
            if isinstance(values, dict):
                values = [
                    item
                    for direction in ("inbound", "outbound")
                    if isinstance(values.get(direction), list)
                    for item in values[direction]
                ]
            if isinstance(values, list):
                interfaces.extend(_interface_summary(value) for value in values)
        values = document.get("evidence")
        if isinstance(values, list):
            evidence.extend(
                str(item.get("path") or item.get("id") or item)
                if isinstance(item, dict)
                else str(item)
                for item in values
            )
    return {
        "summaries": summaries,
        "capabilities": capabilities,
        "intents": sorted(intents),
        "interfaces": interfaces,
        "evidence": evidence,
    }


def _interface_summary(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " · ".join(
            str(value[key])
            for key in ("id", "kind", "summary")
            if isinstance(value.get(key), str) and value[key]
        ) or json.dumps(value, sort_keys=True)
    return str(value)


def _semantic_comparison_projection(
    candidate_id: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
    record: dict[str, Any],
) -> dict[str, Any]:
    claims = record["proposal"]["claims"]
    by_kind = {
        kind: [
            {
                "id": claim["id"],
                "text": claim["text"],
                "evidence": [
                    {
                        "id": item["id"],
                        "sourcePath": item["sourcePath"],
                        "sha256": item["sha256"],
                    }
                    for item in claim["evidence"]
                ],
            }
            for claim in claims
            if claim["kind"] == kind
        ]
        for kind in ("purpose", "capability", "interface", "nearby_intent_difference", "non_goal")
    }
    reuse: list[dict[str, Any]] = []
    experimental: list[dict[str, Any]] = []
    for decision in record["proposal"]["intentDecisions"]:
        if decision["state"] == "proposed_reuse":
            reuse.append(
                {
                    "intentId": decision["intentId"],
                    "rationaleClaimId": decision["rationaleClaimId"],
                }
            )
        else:
            experimental.append(
                {
                    "intentId": decision["intentId"],
                    "userNeedClaimId": decision["userNeedClaimId"],
                    "nearbyIntentIds": decision["nearbyIntentIds"],
                    "nearbyIntentClaimIds": decision["nearbyIntentClaimIds"],
                    "nonGoalClaimIds": decision["nonGoalClaimIds"],
                }
            )
    return {
        "static": _static_semantics(candidate_id, packet, members),
        "ai": {
            "claims": by_kind,
            "observedIntentReuse": reuse,
            "experimentalIntents": experimental,
        },
        "binding": {
            "semanticRecordSha256": record["recordSha256"],
            "proposalSha256": record["proposalSha256"],
            "sourceBundleSha256": record["sourceBundleSha256"],
        },
    }


def _comparison(
    candidate_id: str,
    packet_sha256: str,
    packet: dict[str, Any],
    members: dict[str, bytes],
    campaign_record: dict[str, Any] | None = None,
    campaign_source: str | None = None,
) -> dict[str, Any]:
    proposal = packet["aiProposal"]
    ai: dict[str, Any] = {"status": proposal["status"]}
    summary = proposal.get("summary")
    if isinstance(summary, dict) and isinstance(summary.get("warningCount"), int):
        ai["warningCount"] = summary["warningCount"]
    if proposal["status"] == "portable":
        ai["proposalSha256"] = proposal["sha256"]
    semantic = _semantic_record(candidate_id, packet, members, campaign_record)
    if semantic is not None:
        ai = {
            "status": "complete_portable",
            "proposalSha256": semantic["proposalSha256"],
            "semanticRecordSha256": semantic["recordSha256"],
            "qualityReportSha256": semantic["qualityReportSha256"],
            "providerReceiptSha256": semantic["providerReceiptSha256"],
            "sourceBundleSha256": semantic["sourceBundleSha256"],
            "qualityStatus": semantic["qualityStatus"],
            "warningCount": semantic["qualityReport"]["summary"]["warningCount"],
            "campaignSource": campaign_source,
        }
    elif (
        campaign_record is not None
        and campaign_record.get("qualityReport", {}).get("status") == "rejected"
    ):
        quality = campaign_record["qualityReport"]
        ai = {
            "status": "campaign_rejected",
            "qualityStatus": "rejected",
            "warningCount": quality["summary"]["warningCount"],
            "campaignRecordSha256": campaign_record["recordSha256"],
            "campaignSource": campaign_source,
        }
    comparison = {
        "apiVersion": "spec-harvester.candidate-review-comparison/v0",
        "kind": "SpecHarvesterCandidateReviewComparison",
        "authority": "local_review_comparison_evidence_only",
        "binding": {"candidateId": candidate_id, "packetSha256": packet_sha256},
        "static": {"memberCount": packet["candidate"]["fileCount"]},
        "ai": ai,
    }
    if semantic is not None:
        comparison["semantic"] = _semantic_comparison_projection(
            candidate_id, packet, members, semantic
        )
    return comparison


def _digest_without_record_sha256(record: dict[str, Any]) -> str:
    value = {key: item for key, item in record.items() if key != "recordSha256"}
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _semantic_archive_records(
    archive: Path,
    expected: str,
    catalog_ids: set[str],
    *,
    require_full_catalog: bool,
) -> tuple[str, dict[str, Any], dict[str, dict[str, Any]]]:
    if archive is None or expected is None:
        raise ValueError("Semantic campaign archive and expected SHA-256 must be supplied together")
    archive_sha256, members = _read_archive(
        LocalCandidateReviewCatalogOptions(
            archive=archive,
            expected_archive_sha256=expected,
            expected_packet_count=len(catalog_ids),
        )
    )
    campaign_input = _json_object(members.get("campaign-input.json", b""), "campaign-input.json")
    input_sha256 = campaign_input.get("campaignInputSha256")
    targets = campaign_input.get("targets")
    if not isinstance(input_sha256, str) or not isinstance(targets, list):
        raise ValueError("Semantic campaign input binding is invalid")
    target_bindings = {
        target.get("repositoryId"): target.get("candidateId")
        for target in targets
        if isinstance(target, dict)
    }
    target_ids = set(target_bindings)
    if (
        not target_ids
        or not target_ids <= catalog_ids
        or len(target_bindings) != len(targets)
        or (require_full_catalog and target_ids != catalog_ids)
    ):
        raise ValueError("Semantic campaign target set differs from catalog")

    records: dict[str, dict[str, Any]] = {}
    for name, payload in members.items():
        parts = Path(name).parts
        if len(parts) != 3 or parts[0] != "records" or parts[2] != "campaign-record.json":
            continue
        repository_id = parts[1]
        record = _json_object(payload, name)
        if (
            repository_id in records
            or record.get("repositoryId") != repository_id
            or record.get("candidateId") != target_bindings.get(repository_id)
            or record.get("campaignInputSha256") != input_sha256
            or record.get("status") not in {"completed", "failed"}
            or not isinstance(record.get("attempts"), list)
            or len(record["attempts"]) > 2
            or record.get("recordSha256") != _digest_without_record_sha256(record)
        ):
            raise ValueError(f"Semantic campaign record binding is invalid: {repository_id}")
        portable = record.get("portableProposal")
        if portable is not None:
            if (
                not isinstance(portable, dict)
                or portable.get("candidateId") != record["candidateId"]
            ):
                raise ValueError(f"Semantic campaign portable binding is invalid: {repository_id}")
            validate_portable_semantic_proposal(portable)
            portable_member = members.get(
                str(Path("records") / repository_id / "semantic-proposal-record.json")
            )
            if portable_member is None or _json_object(portable_member, repository_id) != portable:
                raise ValueError(f"Semantic campaign portable member differs: {repository_id}")
        records[repository_id] = record
    if set(records) != target_ids:
        raise ValueError("Semantic campaign record set differs from catalog")
    return archive_sha256, campaign_input, records


def _semantic_campaign_records(
    options: LocalCandidateReviewDetailsOptions, catalog_ids: set[str]
) -> tuple[
    str | None,
    str | None,
    str | None,
    dict[str, dict[str, Any]],
    set[str],
    set[str],
]:
    archive = options.semantic_campaign_archive
    expected = options.expected_semantic_campaign_sha256
    follow_up_archive = options.semantic_follow_up_archive
    follow_up_expected = options.expected_semantic_follow_up_sha256
    recovery_archive = options.semantic_recovery_archive
    recovery_expected = options.expected_semantic_recovery_sha256
    if all(
        value is None
        for value in (
            archive,
            expected,
            follow_up_archive,
            follow_up_expected,
            recovery_archive,
            recovery_expected,
        )
    ):
        return None, None, None, {}, set(), set()
    if archive is None or expected is None:
        raise ValueError("Semantic campaign archive and expected SHA-256 must be supplied together")
    baseline_sha256, _baseline_input, records = _semantic_archive_records(
        archive, expected, catalog_ids, require_full_catalog=True
    )
    if follow_up_archive is None and follow_up_expected is None:
        if recovery_archive is not None or recovery_expected is not None:
            raise ValueError("Semantic recovery requires a semantic follow-up archive")
        return baseline_sha256, None, None, records, set(), set()
    if follow_up_archive is None or follow_up_expected is None:
        raise ValueError(
            "Semantic follow-up archive and expected SHA-256 must be supplied together"
        )
    follow_up_sha256, follow_up_input, follow_up_records = _semantic_archive_records(
        follow_up_archive,
        follow_up_expected,
        catalog_ids,
        require_full_catalog=False,
    )
    baseline = follow_up_input.get("baseline")
    if not isinstance(baseline, dict) or baseline.get("archiveSha256") != baseline_sha256:
        raise ValueError("Semantic follow-up baseline archive binding is stale")
    records.update(follow_up_records)
    if recovery_archive is None and recovery_expected is None:
        return baseline_sha256, follow_up_sha256, None, records, set(follow_up_records), set()
    if recovery_archive is None or recovery_expected is None:
        raise ValueError("Semantic recovery archive and expected SHA-256 must be supplied together")
    recovery_sha256, recovery_input, recovery_records = _semantic_archive_records(
        recovery_archive,
        recovery_expected,
        catalog_ids,
        require_full_catalog=False,
    )
    recovery_baseline = recovery_input.get("baseline")
    if (
        not isinstance(recovery_baseline, dict)
        or recovery_baseline.get("archiveSha256") != follow_up_sha256
    ):
        raise ValueError("Semantic recovery follow-up archive binding is stale")
    records.update(recovery_records)
    return (
        baseline_sha256,
        follow_up_sha256,
        recovery_sha256,
        records,
        set(follow_up_records),
        set(recovery_records),
    )


def _validate_record(record: dict[str, Any]) -> None:
    schema = load_candidate_review_schema()
    errors = list(Draft202012Validator(schema).iter_errors(record))
    if errors:
        raise ValueError(f"Candidate detail record schema is invalid: {errors[0].message}")


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
    (
        semantic_campaign_sha256,
        semantic_follow_up_sha256,
        semantic_recovery_sha256,
        campaign_records,
        follow_up_ids,
        recovery_ids,
    ) = _semantic_campaign_records(options, set(bindings))
    details: list[dict[str, Any]] = []
    comparisons: list[dict[str, Any]] = []
    for name in sorted(
        name for name in members if name.startswith("packets/") and name.endswith("/packet.json")
    ):
        packet_bytes = members[name]
        _, catalog_item = _catalog_item(name, packet_bytes, expectations, members)
        candidate_id = catalog_item["candidateId"]
        if bindings.get(candidate_id) != catalog_item["packetSha256"]:
            raise ValueError(f"Detail packet binding differs from catalog: {candidate_id}")
        packet = _json_object(packet_bytes, name)
        detail = {
            "apiVersion": "spec-harvester.candidate-review-detail/v0",
            "kind": "SpecHarvesterCandidateReviewDetail",
            "authority": "local_review_detail_evidence_only",
            "binding": {
                "candidateId": candidate_id,
                "packetSha256": catalog_item["packetSha256"],
            },
            "previewOnly": True,
            "sections": _detail_sections(
                candidate_id,
                packet,
                members,
                campaign_records.get(candidate_id),
                (
                    "recovery"
                    if candidate_id in recovery_ids
                    else "follow_up"
                    if candidate_id in follow_up_ids
                    else "baseline"
                ),
            ),
        }
        comparison = _comparison(
            candidate_id,
            catalog_item["packetSha256"],
            packet,
            members,
            campaign_records.get(candidate_id),
            (
                "recovery"
                if candidate_id in recovery_ids
                else "follow_up"
                if candidate_id in follow_up_ids
                else "baseline"
            ),
        )
        _validate_record(detail)
        _validate_record(comparison)
        details.append(detail)
        comparisons.append(comparison)
    if set(bindings) != {detail["binding"]["candidateId"] for detail in details}:
        raise ValueError("Detail candidate set differs from catalog")
    payload = {
        "apiVersion": DETAIL_API_VERSION,
        "kind": "SpecHarvesterCandidateReviewDetailSet",
        "authority": "local_review_detail_evidence_only",
        "sourceBundleSha256": archive_sha256,
        "semanticCampaignSha256": semantic_campaign_sha256,
        "semanticFollowUpSha256": semantic_follow_up_sha256,
        "semanticRecoverySha256": semantic_recovery_sha256,
        "details": details,
        "comparisons": comparisons,
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "status": "passed",
        "detailCount": len(details),
        "semanticPortableCount": sum(
            isinstance(record.get("portableProposal"), dict) for record in campaign_records.values()
        ),
        "semanticRejectedCount": sum(
            record.get("qualityReport", {}).get("status") == "rejected"
            for record in campaign_records.values()
        ),
        "semanticFollowUpCount": len(follow_up_ids),
        "semanticRecoveryCount": len(recovery_ids),
        "output": str(options.output),
    }
