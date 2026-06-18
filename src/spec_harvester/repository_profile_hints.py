from __future__ import annotations

import json
from pathlib import Path
from typing import Any

API_VERSION = "spec-harvester.repository-profile-hints/v0"
KIND = "SpecHarvesterRepositoryProfileHintVocabulary"
SCHEMA_VERSION = 1
AUTHORITY = "producer_profile_hint_vocabulary_only"

HINT_PACKAGE_SET_ROOT = "package_set_root"
HINT_MEMBER_PACKAGE = "member_package"
HINT_META_PACKAGE = "meta_package"
HINT_PRIMARY_PACKAGE = "primary_package"
HINT_CLI_PACKAGE = "cli_package"
HINT_BRIDGE_PACKAGE = "bridge_package"
HINT_PLUGIN_PACKAGE = "plugin_package"
HINT_EXAMPLE_PACKAGE = "example_package"
HINT_TEST_PACKAGE = "test_package"
HINT_DOCUMENTATION_SOURCE = "documentation_source"
HINT_GENERATED_ARTIFACT = "generated_artifact"
HINT_INTERNAL_UTILITY = "internal_utility"
HINT_EVIDENCE_ONLY = "evidence_only"

NON_AUTHORITY_STATEMENTS = [
    "does_not_accept_packages",
    "does_not_accept_relations",
    "does_not_publish_registry_metadata",
    "does_not_remove_preview_only",
    "does_not_treat_profile_hints_as_registry_truth",
]

GENERIC_PROFILE_DISCOVERY_HINTS = [
    {
        "hint": HINT_PACKAGE_SET_ROOT,
        "title": "Package-Set Root",
        "pathSubject": "workspace_root",
        "summary": "Path likely anchors an aggregate package-set candidate.",
        "consumerAction": "review_as_candidate_package_set_root",
    },
    {
        "hint": HINT_MEMBER_PACKAGE,
        "title": "Member Package",
        "pathSubject": "package_root",
        "summary": "Path likely contains a package that belongs to a package-set.",
        "consumerAction": "review_as_candidate_member_package",
    },
    {
        "hint": HINT_META_PACKAGE,
        "title": "Meta Package",
        "pathSubject": "package_root",
        "summary": "Path likely groups or re-exports other package surfaces.",
        "consumerAction": "review_as_meta_or_aggregate_package",
    },
    {
        "hint": HINT_PRIMARY_PACKAGE,
        "title": "Primary Package",
        "pathSubject": "package_root",
        "summary": "Path likely contains a primary public package surface.",
        "consumerAction": "review_as_primary_public_package",
    },
    {
        "hint": HINT_CLI_PACKAGE,
        "title": "CLI Package",
        "pathSubject": "package_root",
        "summary": "Path likely contains a command-line package or executable surface.",
        "consumerAction": "review_as_command_line_surface",
    },
    {
        "hint": HINT_BRIDGE_PACKAGE,
        "title": "Bridge Package",
        "pathSubject": "package_root",
        "summary": "Path likely adapts one runtime, framework, or ecosystem to another.",
        "consumerAction": "review_as_adapter_or_bridge_package",
    },
    {
        "hint": HINT_PLUGIN_PACKAGE,
        "title": "Plugin Package",
        "pathSubject": "package_root",
        "summary": "Path likely extends a host package or framework.",
        "consumerAction": "review_as_extension_surface",
    },
    {
        "hint": HINT_EXAMPLE_PACKAGE,
        "title": "Example Package",
        "pathSubject": "package_root",
        "summary": "Path likely exists to demonstrate usage rather than define a primary package.",
        "consumerAction": "exclude_from_primary_members_unless_operator_selected",
    },
    {
        "hint": HINT_TEST_PACKAGE,
        "title": "Test Package",
        "pathSubject": "package_root",
        "summary": "Path likely contains test fixtures or test-only packages.",
        "consumerAction": "exclude_from_public_interface_claims_by_default",
    },
    {
        "hint": HINT_DOCUMENTATION_SOURCE,
        "title": "Documentation Source",
        "pathSubject": "documentation_path",
        "summary": "Path likely provides documentation or semantic usage evidence.",
        "consumerAction": "use_as_semantic_usage_evidence",
    },
    {
        "hint": HINT_GENERATED_ARTIFACT,
        "title": "Generated Artifact",
        "pathSubject": "source_or_output_path",
        "summary": "Path likely contains generated source, build output, or checked-in artifacts.",
        "consumerAction": "treat_as_generated_or_build_output",
    },
    {
        "hint": HINT_INTERNAL_UTILITY,
        "title": "Internal Utility",
        "pathSubject": "package_or_source_path",
        "summary": (
            "Path likely supports the repository internally rather than defining public intent."
        ),
        "consumerAction": "exclude_from_primary_public_claims_by_default",
    },
    {
        "hint": HINT_EVIDENCE_ONLY,
        "title": "Evidence Only",
        "pathSubject": "evidence_path",
        "summary": (
            "Path should be retained as review evidence without becoming a package identity."
        ),
        "consumerAction": "retain_as_evidence_without_candidate_identity",
    },
]

GENERIC_REPOSITORY_PROFILE_HINT_IDS = frozenset(
    hint["hint"] for hint in GENERIC_PROFILE_DISCOVERY_HINTS
)


def build_repository_profile_hint_vocabulary() -> dict[str, Any]:
    return {
        "apiVersion": API_VERSION,
        "kind": KIND,
        "schemaVersion": SCHEMA_VERSION,
        "authority": AUTHORITY,
        "hints": [
            {
                **hint,
                "nonAuthorityStatements": list(NON_AUTHORITY_STATEMENTS),
            }
            for hint in GENERIC_PROFILE_DISCOVERY_HINTS
        ],
        "summary": {
            "hintCount": len(GENERIC_PROFILE_DISCOVERY_HINTS),
            "defaultConsumerBehavior": "review_only",
            "registryAuthority": False,
        },
        "nonAuthorityStatements": list(NON_AUTHORITY_STATEMENTS),
    }


def write_repository_profile_hint_vocabulary(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_repository_profile_hint(hint_id: str) -> str:
    if hint_id not in GENERIC_REPOSITORY_PROFILE_HINT_IDS:
        raise ValueError(f"Unknown generic repository profile hint: {hint_id}")
    return hint_id
