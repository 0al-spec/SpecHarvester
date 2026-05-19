from __future__ import annotations

from copy import deepcopy
from typing import Any

CLASSIFIER_REGISTRY_SCHEMA_VERSION = 1
CLASSIFIER_POLICY_SCHEMA_VERSION = 1
CLASSIFIER_STATUSES = ("approved_optional", "deferred", "rejected")

_COMMON_TRUST_BOUNDARY = {
    "inputAuthority": "untrusted_repository_content",
    "outputAuthority": "advisory_untrusted_metadata",
    "execution": "optional_local_tool_only",
    "networkAccess": "none",
    "packageScripts": "not_run",
    "requiresPinnedToolVersion": True,
    "requiresSourceDigests": True,
    "manifestEvidencePrecedence": "manifest_first",
}

_REGISTRY: tuple[dict[str, Any], ...] = (
    {
        "id": "github-linguist",
        "name": "GitHub Linguist",
        "status": "approved_optional",
        "categories": [
            "language_classification",
            "vendored_filtering",
            "generated_filtering",
        ],
        "license": {
            "spdx": "MIT",
            "notes": (
                "Core repository is MIT; bundled grammars carry their own upstream licenses."
            ),
        },
        "source": "https://github.com/github-linguist/linguist",
        "deterministicUse": (
            "Pin gem version and revision, parse JSON output only, and treat "
            ".gitattributes overrides as repository-provided advisory input."
        ),
        "execution": "optional_local_tool_only",
        "networkAccess": "none",
        "packageScripts": "not_run",
        "outputAuthority": "advisory_untrusted_metadata",
        "trustBoundary": _COMMON_TRUST_BOUNDARY,
        "fallback": "Use manifest-first ProjectProfile evidence when unavailable.",
        "notes": (
            "Reference-compatible classifier for GitHub language statistics; not a "
            "source of SpecPM package authority."
        ),
    },
    {
        "id": "go-enry",
        "name": "go-enry",
        "status": "approved_optional",
        "categories": [
            "language_classification",
            "vendored_filtering",
            "generated_filtering",
        ],
        "license": {
            "spdx": "Apache-2.0",
            "notes": "Go port of Linguist semantics with CLI hosted separately.",
        },
        "source": "https://github.com/go-enry/go-enry",
        "deterministicUse": (
            "Pin module or CLI release, pass bounded file content from the already "
            "collected checkout, and record classifier version plus source digests."
        ),
        "execution": "optional_local_tool_only",
        "networkAccess": "none",
        "packageScripts": "not_run",
        "outputAuthority": "advisory_untrusted_metadata",
        "trustBoundary": _COMMON_TRUST_BOUNDARY,
        "fallback": "Use manifest-first ProjectProfile evidence when unavailable.",
        "notes": (
            "Preferred future Linguist-compatible adapter candidate because it can "
            "be embedded or invoked without Ruby dependency setup."
        ),
    },
    {
        "id": "syft",
        "name": "Syft",
        "status": "approved_optional",
        "categories": [
            "package_cataloging",
            "sbom_generation",
            "declared_dependency_evidence",
        ],
        "license": {
            "spdx": "Apache-2.0",
            "notes": "Single-binary CLI and Go library from Anchore.",
        },
        "source": "https://github.com/anchore/syft",
        "deterministicUse": (
            "Pin release, scan only a local directory source, disable networked "
            "targets, and retain package results as advisory dependency evidence."
        ),
        "execution": "optional_local_tool_only",
        "networkAccess": "none",
        "packageScripts": "not_run",
        "outputAuthority": "advisory_untrusted_metadata",
        "trustBoundary": _COMMON_TRUST_BOUNDARY,
        "fallback": "Skip SBOM enrichment and keep collected manifests as primary evidence.",
        "notes": (
            "Useful for package inventory enrichment, not for deciding repository "
            "language or SpecPM capability truth."
        ),
    },
    {
        "id": "scancode-toolkit",
        "name": "ScanCode Toolkit",
        "status": "deferred",
        "categories": [
            "license_detection",
            "copyright_detection",
            "package_metadata",
            "provenance_evidence",
        ],
        "license": {
            "spdx": "NOASSERTION",
            "notes": (
                "Repository includes Apache-2.0 and CC-BY-4.0 license materials; "
                "reference datasets and bundled third-party materials require "
                "secondary license review."
            ),
        },
        "source": "https://github.com/aboutcode-org/scancode-toolkit",
        "deterministicUse": (
            "Needs a pinned distribution, bounded scan scope, explicit output "
            "schema, and cost limits before it can be enabled."
        ),
        "execution": "optional_local_tool_only",
        "networkAccess": "none",
        "packageScripts": "not_run",
        "outputAuthority": "advisory_untrusted_metadata",
        "trustBoundary": _COMMON_TRUST_BOUNDARY,
        "fallback": "Use LICENSE file hints and manifest license fields already collected.",
        "notes": (
            "Deferred because license-data provenance and runtime cost need a "
            "dedicated adapter review."
        ),
    },
    {
        "id": "universal-ctags",
        "name": "Universal Ctags",
        "status": "deferred",
        "categories": [
            "symbol_extraction",
            "public_interface_indexing",
        ],
        "license": {
            "spdx": "GPL-2.0",
            "notes": "CLI integration requires license and distribution-boundary review.",
        },
        "source": "https://github.com/universal-ctags/ctags",
        "deterministicUse": (
            "Would require pinned executable, JSON Lines output, sorted paths, "
            "bounded file set, and stable field selection."
        ),
        "execution": "optional_local_tool_only",
        "networkAccess": "none",
        "packageScripts": "not_run",
        "outputAuthority": "advisory_untrusted_metadata",
        "trustBoundary": _COMMON_TRUST_BOUNDARY,
        "fallback": "Use language-specific static analyzers or manifest-only analyzer plan.",
        "notes": (
            "Deferred because the GPL CLI boundary and parser-specific output "
            "variance need review before adapter approval."
        ),
    },
    {
        "id": "tree-sitter",
        "name": "Tree-sitter",
        "status": "deferred",
        "categories": [
            "syntax_indexing",
            "ast_extraction",
            "public_interface_indexing",
        ],
        "license": {
            "spdx": "MIT",
            "notes": "Core runtime is MIT; each language grammar still needs license review.",
        },
        "source": "https://github.com/tree-sitter/tree-sitter",
        "deterministicUse": (
            "Future adapters must pin runtime and grammar versions, forbid grammar "
            "generation during harvest, and store parser plus source digests."
        ),
        "execution": "optional_local_tool_only",
        "networkAccess": "none",
        "packageScripts": "not_run",
        "outputAuthority": "advisory_untrusted_metadata",
        "trustBoundary": _COMMON_TRUST_BOUNDARY,
        "fallback": "Use existing Python ast and JS/TS export analyzers where available.",
        "notes": (
            "Deferred here because P10-T3 defines the trust contract; AST ingestion "
            "belongs to a later language-neutral analyzer task."
        ),
    },
)


def classifier_registry() -> dict[str, Any]:
    return {
        "schemaVersion": CLASSIFIER_REGISTRY_SCHEMA_VERSION,
        "statusValues": list(CLASSIFIER_STATUSES),
        "tools": deepcopy(list(_REGISTRY)),
    }


def classifier_registry_summary() -> dict[str, Any]:
    return {
        "schemaVersion": CLASSIFIER_REGISTRY_SCHEMA_VERSION,
        "statusValues": list(CLASSIFIER_STATUSES),
        "tools": [
            {
                "id": tool["id"],
                "status": tool["status"],
                "categories": deepcopy(tool["categories"]),
                "outputAuthority": tool["outputAuthority"],
                "fallback": tool["fallback"],
            }
            for tool in _REGISTRY
        ],
    }


def default_classifier_policy() -> dict[str, Any]:
    return {
        "schemaVersion": CLASSIFIER_POLICY_SCHEMA_VERSION,
        "registrySchemaVersion": CLASSIFIER_REGISTRY_SCHEMA_VERSION,
        "inputAuthority": "untrusted_repository_content",
        "outputAuthority": "advisory_untrusted_metadata",
        "defaultMode": "disabled",
        "allowedExecutions": ["none"],
        "networkAccess": "none",
        "packageScripts": "not_run",
        "requiresClassifierId": True,
        "requiresClassifierVersion": True,
        "requiresSourceRevision": True,
        "requiresSourceDigests": True,
        "requiresPinnedToolVersion": True,
        "manifestEvidencePrecedence": "manifest_first",
        "registry": classifier_registry_summary(),
        "adapterContract": {
            "requiredFields": [
                "classifierId",
                "classifierVersion",
                "sourceRevision",
                "sourceDigest",
                "outputDigest",
                "observations",
            ],
            "allowedObservationKinds": [
                "language",
                "vendored_file",
                "generated_file",
                "package",
                "license",
                "symbol",
                "syntax_node",
            ],
            "mergeRule": (
                "External classifier observations can enrich review evidence but "
                "must not override manifest-first ProjectProfile evidence."
            ),
        },
    }
