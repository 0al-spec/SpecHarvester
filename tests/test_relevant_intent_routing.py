from __future__ import annotations

import copy
import hashlib
import json

import pytest

from spec_harvester.relevant_intent_routing import (
    build_relevant_intent_catalog,
    has_specific_purpose_generic_only_contradiction,
    load_specpm_observed_intent_snapshot,
    validate_relevant_intent_catalog,
    validate_relevant_intent_routing,
    validate_specpm_observed_intent_snapshot,
)
from spec_harvester.semantic_product_profile import build_semantic_product_profile


def product_profile(
    *,
    repository: str = "https://github.com/xyflow/xyflow",
    description: str = "Node-based editor and flow diagramming toolkit",
    keywords: list[str] | None = None,
) -> dict:
    readme = b"Build node-based editors and flow diagrams."
    return build_semantic_product_profile(
        repository_id=repository.removeprefix("https://github.com/").replace("/", "-"),
        candidate_id="demo.package",
        harvest={
            "source": {
                "repository": repository,
                "revision": "a" * 40,
                "target": {"kind": "folder", "path": ".", "label": "package"},
            },
            "projectProfile": {
                "languages": [{"id": "javascript", "confidence": "high"}],
                "ecosystems": [{"id": "npm", "packageManager": "pnpm"}],
                "manifests": [{"path": "package.json"}],
                "analyzerPlan": [],
            },
            "files": [
                {
                    "path": "package.json",
                    "package": {"name": "demo-package", "description": description},
                }
            ],
        },
        root_document={
            "evidencePath": "README.md",
            "sourcePath": "README.md",
            "sha256": hashlib.sha256(readme).hexdigest(),
            "byteCount": len(readme),
            "harvestSha256": "f" * 64,
        },
        manifest_metadata={
            "sourcePath": "package.json",
            "sha256": "b" * 64,
            "name": "demo-package",
            "description": description,
            "keywords": keywords or ["node editor", "diagramming"],
        },
    )


def test_loads_digest_bound_noncanonical_specpm_snapshot() -> None:
    snapshot = load_specpm_observed_intent_snapshot()

    validate_specpm_observed_intent_snapshot(snapshot)
    assert snapshot["authority"] == "observed_metadata_only"
    assert snapshot["canonical"] is False
    assert snapshot["source"]["revision"] == "8a5ce3dece3d18bf8f601a5a599520bd520c7839"
    assert len(snapshot["intents"]) == 26


def test_routes_current_generic_and_positive_nearby_intents() -> None:
    catalog = build_relevant_intent_catalog(
        product_profile(),
        current_intent_ids=["intent.package.javascript_library"],
    )

    selected = {item["intentId"]: item for item in catalog["intents"]}
    assert "intent.package.javascript_library" in selected
    assert selected["intent.package.javascript_library"]["selectionReason"] == (
        "current_observed_generic"
    )
    assert {
        "intent.ui.diagramming",
        "intent.ui.flow_diagramming",
        "intent.ui.node_based_editor",
    } <= set(selected)
    assert "intent.llm.local_provider_discovery" not in selected
    assert catalog["routing"]["selectedIntentIds"] == sorted(selected)
    assert len(selected) <= 16
    assert catalog["sha256"] == digest_without(catalog, "sha256")


def test_routing_excludes_zero_score_intents_and_honors_limit() -> None:
    catalog = build_relevant_intent_catalog(
        product_profile(
            repository="https://github.com/openai/codex",
            description="Coding agent that works in a terminal",
            keywords=["coding agent", "terminal"],
        ),
        current_intent_ids=["intent.package.javascript_library"],
        max_observed_intents=2,
    )

    assert len(catalog["intents"]) <= 2
    assert catalog["routing"]["maxObservedIntents"] == 2
    assert "intent.package.javascript_library" in catalog["routing"]["selectedIntentIds"]
    assert "intent.ui.diagramming" not in catalog["routing"]["selectedIntentIds"]


@pytest.mark.parametrize(
    ("repository", "description", "keywords"),
    [
        (
            "https://github.com/axios/axios",
            "Promise based HTTP client for the browser and node.js",
            ["http", "client", "node"],
        ),
        (
            "https://github.com/openai/codex",
            "Coding agent that works in a terminal",
            ["coding agent", "terminal"],
        ),
    ],
)
def test_routing_rejects_ambiguous_single_term_matches(
    repository: str, description: str, keywords: list[str]
) -> None:
    catalog = build_relevant_intent_catalog(
        product_profile(
            repository=repository,
            description=description,
            keywords=keywords,
        ),
        current_intent_ids=["intent.package.javascript_library"],
    )

    assert catalog["routing"]["selectedIntentIds"] == ["intent.package.javascript_library"]
    assert catalog["routing"]["minimumRelevantIntentTermMatches"] == 2


def test_snapshot_validation_rejects_stale_digest_and_duplicate_ids() -> None:
    stale = load_specpm_observed_intent_snapshot()
    stale["intents"][0]["capabilities"].append("changed")
    with pytest.raises(ValueError, match="snapshot digest is stale"):
        validate_specpm_observed_intent_snapshot(stale)

    duplicate = load_specpm_observed_intent_snapshot()
    duplicate["intents"].append(copy.deepcopy(duplicate["intents"][0]))
    duplicate["snapshotSha256"] = digest_without(duplicate, "snapshotSha256")
    with pytest.raises(ValueError, match="duplicate intent ID"):
        validate_specpm_observed_intent_snapshot(duplicate)


def test_snapshot_validation_rejects_rehashed_source_substitution() -> None:
    substituted = load_specpm_observed_intent_snapshot()
    substituted["intents"][0]["capabilities"] = ["substituted.capability"]
    substituted["snapshotSha256"] = digest_without(substituted, "snapshotSha256")

    with pytest.raises(ValueError, match="identity is invalid"):
        validate_specpm_observed_intent_snapshot(substituted)


def test_routing_and_catalog_reject_rehashed_semantic_substitution() -> None:
    profile = product_profile()
    catalog = build_relevant_intent_catalog(
        profile,
        current_intent_ids=["intent.package.javascript_library"],
    )
    substituted_routing = copy.deepcopy(catalog["routing"])
    substituted_routing["specificProductTerms"] = ["substituted", "terms"]
    substituted_routing["routingSha256"] = digest_without(substituted_routing, "routingSha256")
    with pytest.raises(ValueError, match="routing is malformed"):
        validate_relevant_intent_routing(substituted_routing)

    substituted_catalog = copy.deepcopy(catalog)
    substituted_catalog["intents"][0]["sha256"] = "a" * 64
    substituted_catalog["sha256"] = digest_without(substituted_catalog, "sha256")
    with pytest.raises(ValueError, match="catalog item is stale"):
        validate_relevant_intent_catalog(substituted_catalog, profile)


def test_catalog_rejects_rehashed_terms_not_derived_from_product_profile() -> None:
    profile = product_profile()
    catalog = build_relevant_intent_catalog(
        profile,
        current_intent_ids=["intent.package.javascript_library"],
    )
    catalog["routing"]["queryTerms"] = ["fabricated", "purpose"]
    catalog["routing"]["specificProductTerms"] = ["fabricated", "purpose"]
    catalog["routing"]["routingSha256"] = digest_without(catalog["routing"], "routingSha256")
    catalog["sha256"] = digest_without(catalog, "sha256")

    with pytest.raises(ValueError, match="product profile binding is stale"):
        validate_relevant_intent_catalog(catalog, profile)


def test_routing_keeps_one_observed_comparator_when_lexical_selection_is_empty() -> None:
    catalog = build_relevant_intent_catalog(
        product_profile(description="Quux zorb", keywords=["quux", "zorb"]),
        current_intent_ids=[],
    )

    assert len(catalog["intents"]) == 1
    assert catalog["intents"][0]["selectionReason"] == "fallback_comparison_only"
    assert catalog["routing"]["selectedIntentIds"] == [catalog["intents"][0]["intentId"]]


def test_product_terms_are_deterministically_bounded() -> None:
    keywords = [f"keyword{index} companion{index} " + "x" * 120 for index in range(40)]
    profile = product_profile(description="Bounded metadata projection", keywords=keywords)

    catalog = build_relevant_intent_catalog(profile, current_intent_ids=[])

    assert len(catalog["routing"]["queryTerms"]) <= 64
    assert all(len(term) <= 80 for term in catalog["routing"]["queryTerms"])
    validate_relevant_intent_catalog(catalog, profile)


def test_detects_specific_purpose_mapped_only_to_generic_intent() -> None:
    routing = build_relevant_intent_catalog(
        product_profile(description="Promise-based HTTP client", keywords=["http", "client"]),
        current_intent_ids=["intent.package.javascript_library"],
    )["routing"]
    proposal = {
        "claims": [
            {
                "id": "purpose",
                "kind": "purpose",
                "text": "Provide a Promise-based HTTP client for browser and server requests.",
            }
        ],
        "intentDecisions": [
            {
                "state": "proposed_reuse",
                "intentId": "intent.package.javascript_library",
            }
        ],
    }

    assert has_specific_purpose_generic_only_contradiction(routing, proposal) is True
    proposal["intentDecisions"].append(
        {"state": "proposed_reuse", "intentId": "intent.registry.intent_lookup"}
    )
    assert has_specific_purpose_generic_only_contradiction(routing, proposal) is False
    proposal["intentDecisions"] = [
        {"state": "proposed_reuse", "intentId": "intent.package.javascript_library"}
    ]
    proposal["claims"][0]["text"] = "Provide a JavaScript library package."
    assert has_specific_purpose_generic_only_contradiction(routing, proposal) is False


def digest_without(value: dict, key: str) -> str:
    return hashlib.sha256(
        json.dumps(
            {name: item for name, item in value.items() if name != key},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
