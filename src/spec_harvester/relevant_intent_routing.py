from __future__ import annotations

import hashlib
import json
import re
from importlib.resources import files
from pathlib import Path
from typing import Any

from spec_harvester.experimental_intent_policy import GENERIC_OBSERVED_INTENT_IDS
from spec_harvester.semantic_product_profile import validate_semantic_product_profile

SNAPSHOT_FILENAME = "specpm-observed-intent-snapshot-v0.json"
SNAPSHOT_SOURCE_PATH = (
    "tests/fixtures/relevant_intent_routing/p55-t10f-specpm-observed-intent-snapshot.example.json"
)
SNAPSHOT_API_VERSION = "spec-harvester.specpm-observed-intent-snapshot/v0"
SNAPSHOT_KIND = "SpecHarvesterSpecPMObservedIntentSnapshot"
ROUTING_API_VERSION = "spec-harvester.relevant-observed-intent-routing/v0"
ROUTING_KIND = "SpecHarvesterRelevantObservedIntentRouting"
DEFAULT_MAX_OBSERVED_INTENTS = 16
MAX_PRODUCT_TERMS = 64
MAX_PRODUCT_TERM_LENGTH = 80
MINIMUM_RELEVANT_INTENT_TERM_MATCHES = 2
MINIMUM_SPECIFIC_PURPOSE_TERM_MATCHES = 2
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
INTENT_ID_PATTERN = re.compile(r"^intent\.[a-z0-9][a-z0-9._-]*$")
PRODUCT_STOP_WORDS = frozenset(
    {
        "and",
        "are",
        "based",
        "com",
        "core",
        "demo",
        "framework",
        "from",
        "functions",
        "github",
        "https",
        "into",
        "intent",
        "javascript",
        "library",
        "locally",
        "metadata",
        "npm",
        "package",
        "pnpm",
        "provides",
        "public",
        "repository",
        "runs",
        "software",
        "that",
        "the",
        "tool",
        "toolkit",
        "using",
        "workspace",
        "your",
    }
)
EXPECTED_SOURCE = {
    "repository": "https://github.com/0al-spec/SpecPM",
    "revision": "8a5ce3dece3d18bf8f601a5a599520bd520c7839",
    "sourcePath": ".specpm/public-index/v0/intents/index.json",
    "sha256": "5ab3e55940faac03f341cb9b24f8db37924acec636179aa5eb17352ac2364f4e",
}
EXPECTED_SNAPSHOT_SHA256 = "ed03e772f9e634a4bd5de1343a0bd1d847513d66996c0770fcf61d3c3907781d"


def load_specpm_observed_intent_snapshot() -> dict[str, Any]:
    try:
        raw = (
            files("spec_harvester")
            .joinpath("routing", SNAPSHOT_FILENAME)
            .read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        source = Path(__file__).resolve().parents[2] / SNAPSHOT_SOURCE_PATH
        try:
            raw = source.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"cannot read SpecPM observed intent snapshot: {exc}") from exc
    try:
        snapshot = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"cannot read SpecPM observed intent snapshot: {exc}") from exc
    validate_specpm_observed_intent_snapshot(snapshot)
    return snapshot


def validate_specpm_observed_intent_snapshot(snapshot: dict[str, Any]) -> None:
    if (
        not isinstance(snapshot, dict)
        or snapshot.get("apiVersion") != SNAPSHOT_API_VERSION
        or snapshot.get("kind") != SNAPSHOT_KIND
        or snapshot.get("schemaVersion") != 1
        or snapshot.get("authority") != "observed_metadata_only"
        or snapshot.get("canonical") is not False
        or snapshot.get("source") != EXPECTED_SOURCE
    ):
        raise ValueError("SpecPM observed intent snapshot identity is invalid")
    if snapshot.get("snapshotSha256") != _digest_without(snapshot, "snapshotSha256"):
        raise ValueError("SpecPM observed intent snapshot digest is stale")
    intents = snapshot.get("intents")
    if not isinstance(intents, list) or not 1 <= len(intents) <= 64:
        raise ValueError("SpecPM observed intent snapshot items are malformed")
    seen: set[str] = set()
    for item in intents:
        if not isinstance(item, dict):
            raise ValueError("SpecPM observed intent snapshot item is malformed")
        intent_id = item.get("intentId")
        capabilities = item.get("capabilities")
        package_ids = item.get("packageIds")
        if (
            not isinstance(intent_id, str)
            or INTENT_ID_PATTERN.fullmatch(intent_id) is None
            or not _bounded_strings(capabilities)
            or not _bounded_strings(package_ids)
        ):
            raise ValueError("SpecPM observed intent snapshot item is malformed")
        if intent_id in seen:
            raise ValueError("SpecPM observed intent snapshot has duplicate intent ID")
        seen.add(intent_id)
    if snapshot["snapshotSha256"] != EXPECTED_SNAPSHOT_SHA256:
        raise ValueError("SpecPM observed intent snapshot identity is invalid")


def build_relevant_intent_catalog(
    product_profile: dict[str, Any],
    *,
    current_intent_ids: list[str],
    snapshot: dict[str, Any] | None = None,
    max_observed_intents: int = DEFAULT_MAX_OBSERVED_INTENTS,
) -> dict[str, Any]:
    validate_semantic_product_profile(product_profile)
    snapshot = snapshot or load_specpm_observed_intent_snapshot()
    validate_specpm_observed_intent_snapshot(snapshot)
    if not 1 <= max_observed_intents <= DEFAULT_MAX_OBSERVED_INTENTS:
        raise ValueError("relevant observed intent budget is invalid")
    if not isinstance(current_intent_ids, list) or not all(
        isinstance(item, str) for item in current_intent_ids
    ):
        raise ValueError("current observed intent IDs are malformed")

    query_terms = _product_terms(product_profile)
    source_by_id = {item["intentId"]: item for item in snapshot["intents"]}
    current = sorted(set(current_intent_ids) & set(source_by_id))
    selected = _selected_records(snapshot, query_terms, current, max_observed_intents)
    selected_ids = [item["intentId"] for item in selected]
    routing: dict[str, Any] = {
        "apiVersion": ROUTING_API_VERSION,
        "kind": ROUTING_KIND,
        "schemaVersion": 1,
        "authority": "observed_metadata_routing_only",
        "canonical": False,
        "snapshotSha256": snapshot["snapshotSha256"],
        "productProfileSha256": product_profile["profileSha256"],
        "queryTerms": sorted(query_terms),
        "specificProductTerms": sorted(query_terms),
        "currentObservedIntentIds": current,
        "selectedIntentIds": selected_ids,
        "genericObservedIntentIds": sorted(GENERIC_OBSERVED_INTENT_IDS),
        "maxObservedIntents": max_observed_intents,
        "minimumRelevantIntentTermMatches": MINIMUM_RELEVANT_INTENT_TERM_MATCHES,
        "minimumSpecificPurposeTermMatches": MINIMUM_SPECIFIC_PURPOSE_TERM_MATCHES,
        "zeroScoreIntentsExcluded": True,
    }
    routing["routingSha256"] = _digest_without(routing, "routingSha256")
    content = {
        "sourcePath": "generated/specpm-relevant-observed-intents.json",
        "snapshotSource": snapshot["source"],
        "snapshotSha256": snapshot["snapshotSha256"],
        "routing": routing,
        "intents": selected,
    }
    return {**content, "sha256": _digest(content)}


def validate_relevant_intent_routing(routing: dict[str, Any]) -> None:
    query_terms = routing.get("queryTerms") if isinstance(routing, dict) else None
    specific_terms = routing.get("specificProductTerms") if isinstance(routing, dict) else None
    current_ids = routing.get("currentObservedIntentIds") if isinstance(routing, dict) else None
    selected_ids = routing.get("selectedIntentIds") if isinstance(routing, dict) else None
    if (
        not isinstance(routing, dict)
        or routing.get("apiVersion") != ROUTING_API_VERSION
        or routing.get("kind") != ROUTING_KIND
        or routing.get("schemaVersion") != 1
        or routing.get("authority") != "observed_metadata_routing_only"
        or routing.get("canonical") is not False
        or routing.get("snapshotSha256") != EXPECTED_SNAPSHOT_SHA256
        or not _sha256(routing.get("productProfileSha256"))
        or routing.get("genericObservedIntentIds") != sorted(GENERIC_OBSERVED_INTENT_IDS)
        or routing.get("minimumRelevantIntentTermMatches") != MINIMUM_RELEVANT_INTENT_TERM_MATCHES
        or routing.get("minimumSpecificPurposeTermMatches") != MINIMUM_SPECIFIC_PURPOSE_TERM_MATCHES
        or routing.get("zeroScoreIntentsExcluded") is not True
        or not isinstance(routing.get("maxObservedIntents"), int)
        or not 1 <= routing["maxObservedIntents"] <= DEFAULT_MAX_OBSERVED_INTENTS
        or not _bounded_strings(query_terms)
        or not _bounded_strings(specific_terms)
        or not _bounded_strings(current_ids)
        or not _bounded_strings(selected_ids)
        or query_terms != sorted(set(query_terms))
        or specific_terms != query_terms
        or any(
            TOKEN_PATTERN.fullmatch(term) is None or len(term) < 3 or term in PRODUCT_STOP_WORDS
            for term in query_terms
        )
        or current_ids != sorted(set(current_ids))
        or selected_ids != sorted(set(selected_ids))
        or any(INTENT_ID_PATTERN.fullmatch(intent_id) is None for intent_id in current_ids)
        or any(INTENT_ID_PATTERN.fullmatch(intent_id) is None for intent_id in selected_ids)
        or len(selected_ids) > routing.get("maxObservedIntents", 0)
        or (set(current_ids) & GENERIC_OBSERVED_INTENT_IDS) - set(selected_ids)
    ):
        raise ValueError("relevant observed intent routing is malformed")
    if routing.get("routingSha256") != _digest_without(routing, "routingSha256"):
        raise ValueError("relevant observed intent routing digest is stale")


def validate_relevant_intent_catalog(
    catalog: dict[str, Any], product_profile: dict[str, Any]
) -> None:
    if (
        not isinstance(catalog, dict)
        or catalog.get("sourcePath") != "generated/specpm-relevant-observed-intents.json"
        or catalog.get("snapshotSource") != EXPECTED_SOURCE
        or catalog.get("snapshotSha256") != EXPECTED_SNAPSHOT_SHA256
        or not isinstance(catalog.get("routing"), dict)
        or not isinstance(catalog.get("intents"), list)
        or catalog.get("sha256") != _digest_without(catalog, "sha256")
    ):
        raise ValueError("relevant observed intent catalog is malformed")
    routing = catalog["routing"]
    validate_relevant_intent_routing(routing)
    validate_semantic_product_profile(product_profile)
    expected_terms = sorted(_product_terms(product_profile))
    if (
        routing["productProfileSha256"] != product_profile["profileSha256"]
        or routing["queryTerms"] != expected_terms
        or routing["specificProductTerms"] != expected_terms
    ):
        raise ValueError("relevant observed intent catalog product profile binding is stale")
    snapshot = load_specpm_observed_intent_snapshot()
    if set(routing["currentObservedIntentIds"]) - {
        item["intentId"] for item in snapshot["intents"]
    }:
        raise ValueError("relevant observed intent catalog selection is stale")
    expected = _selected_records(
        snapshot,
        set(routing["queryTerms"]),
        routing["currentObservedIntentIds"],
        routing["maxObservedIntents"],
    )
    if catalog["intents"] != expected:
        raise ValueError("relevant observed intent catalog item is stale")
    if routing["selectedIntentIds"] != [item["intentId"] for item in expected]:
        raise ValueError("relevant observed intent catalog selection is stale")


def has_specific_purpose_generic_only_contradiction(
    routing: dict[str, Any], proposal: dict[str, Any]
) -> bool:
    validate_relevant_intent_routing(routing)
    decisions = proposal.get("intentDecisions") if isinstance(proposal, dict) else None
    if not isinstance(decisions, list) or not decisions:
        return False
    if any(
        not isinstance(item, dict)
        or item.get("state") != "proposed_reuse"
        or item.get("intentId") not in GENERIC_OBSERVED_INTENT_IDS
        for item in decisions
    ):
        return False
    purpose = " ".join(
        item.get("text", "")
        for item in proposal.get("claims", [])
        if isinstance(item, dict) and item.get("kind") == "purpose"
    )
    purpose_terms = _tokens(purpose)
    matched = purpose_terms & set(routing["specificProductTerms"])
    return len(matched) >= routing["minimumSpecificPurposeTermMatches"]


def _selection(item: dict[str, Any], query_terms: set[str], reason: str) -> dict[str, Any]:
    intent_terms = _tokens(item["intentId"])
    capability_terms = _tokens(" ".join(item["capabilities"]))
    package_terms = _tokens(" ".join(item["packageIds"]))
    matched_intent = query_terms & intent_terms
    matched_capability = query_terms & capability_terms
    matched_package = query_terms & package_terms
    matched = matched_intent | matched_capability | matched_package
    return {
        "intentId": item["intentId"],
        "sha256": _digest(item),
        "relevanceScore": (
            4 * len(matched_intent) + 2 * len(matched_capability) + len(matched_package)
        ),
        "matchedTerms": sorted(matched),
        "selectionReason": reason,
        "capabilities": item["capabilities"],
        "packageIds": item["packageIds"],
    }


def _selected_records(
    snapshot: dict[str, Any],
    query_terms: set[str],
    current_intent_ids: list[str],
    max_observed_intents: int,
) -> list[dict[str, Any]]:
    source_by_id = {item["intentId"]: item for item in snapshot["intents"]}
    mandatory = [
        _selection(source_by_id[intent_id], query_terms, "current_observed_generic")
        for intent_id in current_intent_ids
        if intent_id in GENERIC_OBSERVED_INTENT_IDS
    ]
    mandatory_ids = {item["intentId"] for item in mandatory}
    ranked = []
    for item in snapshot["intents"]:
        if item["intentId"] in mandatory_ids:
            continue
        selection = _selection(item, query_terms, "relevant_lexical_match")
        if len(selection["matchedTerms"]) >= MINIMUM_RELEVANT_INTENT_TERM_MATCHES:
            ranked.append(selection)
    ranked.sort(key=lambda item: (-item["relevanceScore"], item["intentId"]))
    selected = mandatory[:max_observed_intents]
    selected.extend(ranked[: max_observed_intents - len(selected)])
    if not selected:
        comparisons = [
            _selection(item, query_terms, "fallback_comparison_only")
            for item in snapshot["intents"]
        ]
        comparisons.sort(
            key=lambda item: (
                -item["relevanceScore"],
                item["intentId"] not in GENERIC_OBSERVED_INTENT_IDS,
                item["intentId"],
            )
        )
        selected = comparisons[:1]
    return sorted(selected, key=lambda item: item["intentId"])


def _product_terms(profile: dict[str, Any]) -> set[str]:
    repository = profile["repository"]
    package = profile["package"]
    technology = profile["technology"]
    values = [
        repository.get("name", ""),
        package.get("name", ""),
        package.get("description", ""),
        package.get("targetLabel", ""),
        *package.get("keywords", []),
        *(item.get("id", "") for item in technology.get("languages", [])),
        *(item.get("id", "") for item in technology.get("ecosystems", [])),
        *technology.get("analyzerSignals", []),
    ]
    terms = {
        token
        for token in _tokens(" ".join(str(item) for item in values))
        if 3 <= len(token) <= MAX_PRODUCT_TERM_LENGTH and token not in PRODUCT_STOP_WORDS
    }
    return set(sorted(terms)[:MAX_PRODUCT_TERMS])


def _tokens(value: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(value.casefold()))


def _bounded_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) <= 64
        and all(isinstance(item, str) and 0 < len(item) <= 200 for item in value)
    )


def _sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _digest_without(value: dict[str, Any], key: str) -> str:
    return _digest({name: item for name, item in value.items() if name != key})
