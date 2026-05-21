from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from spec_harvester.interface_index import (
    PUBLIC_INTERFACE_INDEX_KIND,
    render_public_interface_index_json,
    validate_public_interface_index,
)

SPEC_API_VERSION = "specpm.dev/v0.1"
DEFAULT_SPEC_VERSION = "0.1.0"
DEFAULT_AUTHOR = "SpecHarvester"
PUBLIC_INTERFACE_INDEX_OUTPUT = "public-interface-index.json"
PUBLIC_INTERFACE_INDEX_DISCOVERY_NAMES = (
    PUBLIC_INTERFACE_INDEX_OUTPUT,
    "public_interface_index.json",
)
PUBLIC_INTERFACE_INDEX_MEDIA_TYPE = "application/vnd.spec-harvester.public-interface-index+json"
YAML_RESERVED_SCALARS = {"true", "false", "null", "yes", "no", "on", "off", "~"}
PUBLIC_INTERFACE_SEMANTIC_TERM_LIMIT = 2_000
PUBLIC_INTERFACE_SEMANTIC_TEXT_CHAR_LIMIT = 60_000
PUBLIC_INTERFACE_SEMANTIC_IDENTIFIER_CHAR_LIMIT = 160


@dataclass(frozen=True)
class DraftOptions:
    snapshot: Path
    out: Path
    package_id: str | None = None
    name: str | None = None
    version: str = DEFAULT_SPEC_VERSION
    author: str = DEFAULT_AUTHOR
    interface_index: Path | None = None


@dataclass(frozen=True)
class LicenseInference:
    name: str
    evidence: dict[str, Any]


@dataclass(frozen=True)
class SemanticIntentProfile:
    summary: str
    intent_ids: list[str]
    evidence_paths: list[str]
    clusters: list[dict[str, Any]]


@dataclass(frozen=True)
class SemanticDomainRule:
    cluster_id: str
    intent_id: str
    label: str
    terms: tuple[str, ...]
    required_context: str | None = None
    minimum_score: int = 2


SEMANTIC_DOMAIN_RULES = (
    SemanticDomainRule(
        cluster_id="web.framework_surface",
        intent_id="intent.web.framework_surface",
        label="Web Framework Surface",
        terms=(
            "web framework",
            "http framework",
            "microframework",
            "wsgi",
            "asgi",
            "flask",
            "gin",
            "blueprint",
            "route",
            "routes",
            "routing",
            "router",
            "router group",
            "middleware",
            "handler",
            "handlers",
            "request context",
            "application context",
        ),
        minimum_score=4,
    ),
    SemanticDomainRule(
        cluster_id="web.http_routing",
        intent_id="intent.web.http_routing",
        label="HTTP Routing Surface",
        terms=(
            "route",
            "routes",
            "routing",
            "router",
            "router group",
            "url rule",
            "url map",
            "url for",
            "endpoint",
            "handler",
            "handlers",
            "handle",
        ),
        minimum_score=3,
    ),
    SemanticDomainRule(
        cluster_id="web.middleware_pipeline",
        intent_id="intent.web.middleware_pipeline",
        label="Middleware Pipeline",
        terms=(
            "middleware",
            "middlewares",
            "handler chain",
            "handlers chain",
            "before request",
            "after request",
            "request hook",
            "response pipeline",
        ),
    ),
    SemanticDomainRule(
        cluster_id="web.request_response_context",
        intent_id="intent.web.request_response_context",
        label="Request/Response Context",
        terms=(
            "request",
            "response",
            "context",
            "request context",
            "application context",
            "session",
            "cookie",
            "cookies",
            "json",
            "jsonify",
            "bind json",
            "render template",
            "template",
            "templates",
        ),
        minimum_score=4,
    ),
    SemanticDomainRule(
        cluster_id="api.contract_surface",
        intent_id="intent.api.contract_surface",
        label="API Contract Surface",
        terms=(
            "api contract",
            "api",
            "contract",
            "schema",
            "openapi",
            "endpoint",
            "request",
            "response",
            "webhook",
            "graphql",
        ),
    ),
    SemanticDomainRule(
        cluster_id="metadata.schema_validation",
        intent_id="intent.metadata.schema_validation",
        label="Metadata Schema Validation",
        terms=(
            "metadata",
            "schema",
            "validation",
            "validator",
            "manifest",
            "configuration",
            "config",
            "json schema",
        ),
    ),
    SemanticDomainRule(
        cluster_id="workflow.automation_pipeline",
        intent_id="intent.workflow.automation_pipeline",
        label="Workflow Automation Pipeline",
        terms=(
            "workflow",
            "automation",
            "pipeline",
            "task",
            "validation",
            "command",
            "commands",
        ),
    ),
    SemanticDomainRule(
        cluster_id="developer.tooling_surface",
        intent_id="intent.developer.tooling_surface",
        label="Developer Tooling Surface",
        terms=(
            "cli",
            "command",
            "commands",
            "developer tool",
            "tooling",
            "plugin",
            "extension",
            "sdk",
            "configuration",
        ),
    ),
    SemanticDomainRule(
        cluster_id="documentation.knowledge_base",
        intent_id="intent.documentation.knowledge_base",
        label="Documentation Knowledge Base",
        terms=(
            "documentation",
            "guide",
            "reference",
            "tutorial",
            "manual",
        ),
    ),
    SemanticDomainRule(
        cluster_id="swift.specification_pattern",
        intent_id="intent.swift.specification_pattern",
        label="Swift Specification Pattern",
        terms=(
            "specification",
            "specifications",
            "specificationkit",
            "satisfies",
            "conditional satisfies",
        ),
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.predicate_composition",
        intent_id="intent.swift.predicate_composition",
        label="Predicate Composition",
        terms=(
            "predicate",
            "predicates",
            "composable business logic",
            "composition and reusability",
            "composite specification",
            "firstmatchspec",
        ),
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.context_driven_decisioning",
        intent_id="intent.swift.context_driven_decisioning",
        label="Context-Driven Decisioning",
        terms=(
            "context provider",
            "context providers",
            "compositecontextprovider",
            "networkcontextprovider",
            "persistentcontextprovider",
            "platform-specific context providers",
            "decision making",
        ),
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.feature_gating",
        intent_id="intent.swift.feature_gating",
        label="Feature Gating",
        terms=(
            "feature gating",
            "feature flag",
            "feature flags",
            "conditional",
            "thresholdspec",
            "weightedspec",
        ),
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.reactive_specification_evaluation",
        intent_id="intent.swift.reactive_specification_evaluation",
        label="Reactive Specification Evaluation",
        terms=(
            "reactive wrappers",
            "reactive integration",
            "observedsatisfies",
            "observedmaybe",
            "swiftui integration",
            "combine",
            "observation",
        ),
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.specification_tracing",
        intent_id="intent.swift.specification_tracing",
        label="Specification Tracing",
        terms=(
            "specificationtracer",
            "tracing",
            "trace",
            "debugging",
            "performance analysis",
            "dot graph",
        ),
        required_context="swift",
    ),
)


def draft_spec_package(options: DraftOptions) -> dict[str, Any]:
    snapshot_path = resolve_snapshot_path(options.snapshot)
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if snapshot.get("kind") != "SpecHarvesterEvidenceSnapshot":
        raise ValueError(f"Unsupported harvest snapshot kind: {snapshot.get('kind')!r}")
    public_interface_index = load_public_interface_index(
        options.interface_index,
        snapshot_path=snapshot_path,
    )

    source = snapshot.get("source")
    if not isinstance(source, dict):
        source = {}

    repository_name = infer_repository_name(source)
    package_id = options.package_id or f"{repository_name}.core"
    package_id = slug_id(package_id)
    bounded_context = slug_id(repository_name)
    spec_path = f"specs/{bounded_context}.spec.yaml"

    package_records = package_manifest_records(snapshot)
    license_records = license_file_records(snapshot)
    documentation_records = documentation_file_records(snapshot)
    primary_package_records = capability_source_records(package_records)
    semantic_profile = infer_semantic_intent_profile(
        repository_name,
        package_records,
        documentation_records,
        public_interface_index,
    )
    capability_entries = build_capability_entries(
        package_id,
        primary_package_records,
        semantic_profile,
    )
    semantic_profile_for_summary = (
        semantic_profile
        if semantic_profile is not None
        and (
            semantic_profile_applies_to_manifest_capabilities(semantic_profile)
            or not capability_entries
        )
        else None
    )
    if not capability_entries:
        fallback_summary = (
            semantic_profile.summary
            if semantic_profile is not None
            else (f"Describe observed public package metadata for {display_name(repository_name)}.")
        )
        fallback_intents = (
            semantic_profile.intent_ids
            if semantic_profile is not None
            else ["intent.package.public_repository_metadata"]
        )
        capability_entries = [
            {
                "id": package_id,
                "role": "primary",
                "summary": fallback_summary,
                "intentIds": fallback_intents,
            }
        ]

    manifest_capabilities = [entry["id"] for entry in capability_entries]
    manifest_intents = sorted(
        {intent_id for entry in capability_entries for intent_id in entry.get("intentIds", [])}
    )
    license_inference = infer_license_with_evidence(package_records, license_records)
    license_name = license_inference.name
    package_name = options.name or display_name(repository_name)
    package_summary = (
        f"Unofficial generated SpecPackage for {package_name} public package metadata."
    )

    manifest = {
        "apiVersion": SPEC_API_VERSION,
        "kind": "SpecPackage",
        "metadata": {
            "id": package_id,
            "name": package_name,
            "version": options.version,
            "summary": package_summary,
            "license": license_name,
            "licenseEvidence": license_inference.evidence,
            "authors": [{"name": options.author}],
        },
        "preview_only": True,
        "specs": [{"path": spec_path}],
        "index": {
            "provides": {
                "capabilities": manifest_capabilities,
                "intents": manifest_intents,
            },
            "requires": {"capabilities": []},
        },
        "compatibility": infer_compatibility(package_records, snapshot, manifest_intents),
        "foreignArtifacts": [foreign_repository_artifact(source)],
        "keywords": ["generated", "specharvester", bounded_context],
    }

    inbound_interfaces = build_interfaces(
        interface_source_records(package_records),
        public_interface_index,
    )
    evidence = build_evidence(
        manifest_capabilities,
        inbound_interfaces,
        public_interface_index,
        semantic_profile,
    )
    provenance = {
        "sourceConfidence": {
            "intent": "medium",
            "boundary": "medium",
            "behavior": "low",
        },
        "generatedBy": "SpecHarvester deterministic draft generator",
        "sourceRepository": source.get("repository"),
        "sourceRevision": source.get("revision"),
        "harvestPolicy": snapshot.get("policy"),
    }
    if public_interface_index is not None:
        provenance["publicInterfaceIndex"] = public_interface_provenance(public_interface_index)

    boundary_spec = {
        "apiVersion": SPEC_API_VERSION,
        "kind": "BoundarySpec",
        "metadata": {
            "id": package_id,
            "title": f"{package_name} Generated Public Package Boundary",
            "version": options.version,
            "status": "draft",
            "authors": [{"name": options.author}],
        },
        "intent": {
            "summary": (
                semantic_profile_for_summary.summary
                if semantic_profile_for_summary is not None
                else infer_intent_summary(package_name, primary_package_records)
            )
        },
        "scope": {
            "boundedContext": bounded_context,
            "includes": [
                "Describe observed public package metadata from an allowlisted harvest snapshot.",
                "Declare package capabilities and intent IDs inferred from static manifests.",
                "Preserve source repository provenance and harvest policy metadata.",
            ],
            "excludes": [
                "Upstream maintainer endorsement.",
                "Runtime behavior not evidenced by static harvested metadata.",
                "Package script execution, dependency installation, or network probing.",
                "Automatic acceptance into a public SpecPM registry.",
            ],
        },
        "provides": {"capabilities": capability_entries},
        "requires": {"capabilities": []},
        "interfaces": {
            "inbound": inbound_interfaces,
            "outbound": [],
        },
        "effects": {"sideEffects": []},
        "constraints": [
            {
                "id": "generated_candidate_review_required",
                "level": "MUST",
                "statement": (
                    "This generated candidate must be reviewed before it is treated as "
                    "accepted registry metadata."
                ),
            },
            {
                "id": "no_package_execution",
                "level": "MUST",
                "statement": (
                    "SpecHarvester must not execute package scripts, install dependencies, "
                    "or treat package content as host instructions."
                ),
            },
        ],
        "evidence": evidence,
        "provenance": provenance,
        "foreignArtifacts": [foreign_repository_artifact(source)],
        "keywords": ["generated", "specharvester", bounded_context],
    }

    options.out.mkdir(parents=True, exist_ok=True)
    specs_dir = options.out / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    interface_index_output: Path | None = None
    if public_interface_index is not None:
        interface_index_output = options.out / PUBLIC_INTERFACE_INDEX_OUTPUT
        interface_index_output.write_text(
            render_public_interface_index_json(public_interface_index),
            encoding="utf-8",
        )
    (options.out / "specpm.yaml").write_text(render_yaml(manifest), encoding="utf-8")
    (options.out / spec_path).write_text(render_yaml(boundary_spec), encoding="utf-8")

    result = {
        "status": "ok",
        "output": str(options.out),
        "manifest": str(options.out / "specpm.yaml"),
        "spec": str(options.out / spec_path),
        "packageId": package_id,
        "capabilityCount": len(manifest_capabilities),
        "intentCount": len(manifest_intents),
    }
    if interface_index_output is not None:
        result["interfaceIndex"] = str(interface_index_output)
    return result


def resolve_snapshot_path(path: Path) -> Path:
    if path.is_dir():
        path = path / "harvest.json"
    if not path.exists() or not path.is_file():
        raise ValueError(f"Harvest snapshot does not exist: {path}")
    return path


def resolve_public_interface_index_path(
    path: Path | None,
    *,
    snapshot_path: Path,
) -> Path | None:
    if path is not None:
        if path.is_dir():
            for name in PUBLIC_INTERFACE_INDEX_DISCOVERY_NAMES:
                candidate = path / name
                if candidate.exists():
                    path = candidate
                    break
        if not path.exists() or not path.is_file():
            raise ValueError(f"Public interface index does not exist: {path}")
        return path

    for name in PUBLIC_INTERFACE_INDEX_DISCOVERY_NAMES:
        candidate = snapshot_path.parent / name
        if candidate.exists():
            if not candidate.is_file():
                raise ValueError(f"Public interface index is not a file: {candidate}")
            return candidate
    return None


def load_public_interface_index(
    path: Path | None,
    *,
    snapshot_path: Path,
) -> dict[str, Any] | None:
    resolved = resolve_public_interface_index_path(path, snapshot_path=snapshot_path)
    if resolved is None:
        return None
    try:
        index = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid PublicInterfaceIndex JSON: {exc.msg}") from exc
    if not isinstance(index, dict):
        raise ValueError("Invalid PublicInterfaceIndex: index must be an object")
    validate_public_interface_index(index)
    return index


def infer_repository_name(source: dict[str, Any]) -> str:
    repository = source.get("repository")
    if isinstance(repository, str) and repository.strip():
        parsed = urlparse(repository)
        path = parsed.path.rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        name = path.rsplit("/", 1)[-1]
        if name:
            return slug_id(name)

    source_label = source.get("label")
    if isinstance(source_label, str) and source_label.strip():
        return slug_id(source_label)
    return "generated_package"


def package_manifest_records(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    files = snapshot.get("files")
    if not isinstance(files, list):
        return []
    records: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict) or item.get("kind") != "package_manifest":
            continue
        package = item.get("package")
        if not isinstance(package, dict):
            continue
        records.append({"path": item.get("path"), "package": package})
    return sorted(records, key=lambda item: str(item.get("path") or ""))


def license_file_records(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    files = snapshot.get("files")
    if not isinstance(files, list):
        return []
    records: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict) or item.get("kind") != "license":
            continue
        records.append(item)
    return sorted(records, key=lambda item: str(item.get("path") or ""))


def documentation_file_records(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    files = snapshot.get("files")
    if not isinstance(files, list):
        return []
    records: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict) or item.get("kind") != "documentation":
            continue
        records.append(item)
    return sorted(records, key=lambda item: str(item.get("path") or ""))


def build_capability_entries(
    package_id: str,
    package_records: list[dict[str, Any]],
    semantic_profile: SemanticIntentProfile | None = None,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    semantic_profile_for_manifest_capabilities = (
        semantic_profile
        if semantic_profile is not None
        and semantic_profile_applies_to_manifest_capabilities(semantic_profile)
        else None
    )
    for record in capability_source_records(package_records):
        package = record["package"]
        package_name = package.get("name")
        if not isinstance(package_name, str) or not package_name.strip():
            continue
        label = package_label(package_name)
        capability_id = unique_id(f"{package_id}.{label}", seen_ids)
        description = package.get("description")
        summary = capability_summary(
            package_name,
            description,
            semantic_profile_for_manifest_capabilities,
        )
        role = "secondary" if label in {"monorepo", "workspace", "root"} else "primary"
        entries.append(
            {
                "id": capability_id,
                "role": role,
                "summary": summary,
                "intentIds": (
                    semantic_profile_for_manifest_capabilities.intent_ids
                    if semantic_profile_for_manifest_capabilities is not None
                    else infer_intent_ids(package_name, summary, package)
                ),
            }
        )

    if entries and all(entry.get("role") != "primary" for entry in entries):
        entries[0]["role"] = "primary"
    return entries


def semantic_profile_applies_to_manifest_capabilities(
    semantic_profile: SemanticIntentProfile,
) -> bool:
    return any(
        intent_id.startswith(("intent.swift.", "intent.ios.", "intent.web."))
        for intent_id in semantic_profile.intent_ids
    )


def capability_summary(
    package_name: str,
    description: Any,
    semantic_profile: SemanticIntentProfile | None,
) -> str:
    if semantic_profile is not None:
        return semantic_profile.summary
    if isinstance(description, str) and description.strip():
        return description.strip()
    return f"Provide observed package metadata for {package_name}."


def capability_source_records(package_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    swift_records = [
        record
        for record in package_records
        if isinstance(record.get("package"), dict) and record["package"].get("ecosystem") == "swift"
    ]
    if not swift_records:
        return package_records

    non_swift_records = [
        record
        for record in package_records
        if not (
            isinstance(record.get("package"), dict)
            and record["package"].get("ecosystem") == "swift"
        )
    ]
    root_records = [record for record in swift_records if record.get("path") == "Package.swift"]
    if root_records:
        return [*non_swift_records, *root_records[:1]]

    reviewable_records = [
        record for record in swift_records if is_reviewable_swift_manifest(record)
    ]
    if reviewable_records:
        return [*non_swift_records, reviewable_records[0]]
    return [*non_swift_records, swift_records[0]]


def interface_source_records(package_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    swift_records = [
        record
        for record in package_records
        if isinstance(record.get("package"), dict) and record["package"].get("ecosystem") == "swift"
    ]
    if not swift_records:
        return package_records

    records: list[dict[str, Any]] = [
        record
        for record in package_records
        if not (
            isinstance(record.get("package"), dict)
            and record["package"].get("ecosystem") == "swift"
        )
    ]
    root_records = [record for record in swift_records if record.get("path") == "Package.swift"]
    records.extend(root_records[:1])
    records.extend(
        record
        for record in swift_records
        if record.get("path") != "Package.swift" and is_reviewable_swift_manifest(record)
    )
    if records:
        return records
    return swift_records[:1]


def is_reviewable_swift_manifest(record: dict[str, Any]) -> bool:
    path = str(record.get("path") or "")
    parts = set(path.split("/"))
    if {"SourcePackages", "checkouts"}.issubset(parts):
        return False
    ignored_parts = {"Derived", "DerivedData", "Fixtures", "CompileFixtures"}
    if parts.intersection(ignored_parts):
        return False
    return not (
        path.startswith("Derived/")
        or path.startswith("Tests/")
        or path.startswith("old_")
        or "/old_" in path
    )


def infer_semantic_intent_profile(
    repository_name: str,
    package_records: list[dict[str, Any]],
    documentation_records: list[dict[str, Any]],
    public_interface_index: dict[str, Any] | None,
) -> SemanticIntentProfile | None:
    semantic_entries = semantic_text_entries(
        repository_name,
        package_records,
        documentation_records,
        public_interface_index,
    )
    corpus = " ".join(entry["text"] for entry in semantic_entries).lower()
    enabled_contexts = (
        {"swift"}
        if has_swift_semantic_context(
            package_records,
            documentation_records,
            public_interface_index,
        )
        else set()
    )
    clusters = build_semantic_evidence_clusters(semantic_entries, enabled_contexts)
    evidence_paths: set[str] = {
        path
        for cluster in clusters
        for path in cluster.get("evidencePaths", [])
        if isinstance(path, str) and path
    }
    intents: set[str] = {
        str(cluster["intentId"]) for cluster in clusters if isinstance(cluster.get("intentId"), str)
    }

    has_screen = has_any(corpus, "screen", "screens")
    has_uikit = "uikit" in corpus or "ui kit" in corpus
    has_swiftui = "swiftui" in corpus or "swift ui" in corpus
    has_ios_evidence = has_uikit or has_swiftui
    has_migration = has_any(corpus, "migration", "migrating", "legacy", "incremental")
    has_collection = has_any(
        corpus,
        "collection",
        "collections",
        "list",
        "grid",
        "carousel",
        "waterfall",
    )
    has_state = has_any(corpus, "state", "binding", "bindings", "observation", "observable")

    if (
        has_ios_evidence
        and has_screen
        and has_any(corpus, "composition", "compose", "composable", "container")
    ):
        intents.add("intent.ios.screen_level_composition")
    if has_ios_evidence and has_screen and has_uikit and has_swiftui and has_migration:
        intents.add("intent.ios.uikit_swiftui_migration")
    if has_ios_evidence and has_screen and has_collection:
        intents.add("intent.ios.collection_layout_composition")
    if has_ios_evidence and has_screen and has_state:
        intents.add("intent.ios.screen_state_binding")
    if (
        has_ios_evidence
        and has_screen
        and has_any(corpus, "diagnostic", "diagnostics", "debug", "debugging")
    ):
        intents.add("intent.ios.screen_diagnostics")
    if "swift" in enabled_contexts and has_any(corpus, "macro", "macros", "#screen"):
        intents.add("intent.swift.macro_developer_experience")

    if not intents:
        return None

    summary = semantic_summary(repository_name, intents)
    return SemanticIntentProfile(
        summary=summary,
        intent_ids=sorted(intents),
        evidence_paths=sorted(evidence_paths or semantic_profile_paths(semantic_entries)),
        clusters=clusters,
    )


def semantic_text_entries(
    repository_name: str,
    package_records: list[dict[str, Any]],
    documentation_records: list[dict[str, Any]],
    public_interface_index: dict[str, Any] | None,
) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = [
        {"path": "repository", "kind": "repository", "text": repository_name}
    ]

    for record in capability_source_records(package_records):
        package = record.get("package")
        if not isinstance(package, dict):
            continue
        path = str(record.get("path") or "")
        parts: list[str] = []
        for key in ("name", "description", "ecosystem", "language"):
            value = package.get(key)
            if isinstance(value, str):
                parts.append(value)
        products = package.get("products")
        if isinstance(products, list):
            for product in products:
                if isinstance(product, dict) and isinstance(product.get("name"), str):
                    parts.append(product["name"])
        if parts:
            entries.append({"path": path, "kind": "package_manifest", "text": " ".join(parts)})

    for record in documentation_records:
        path = str(record.get("path") or "")
        if not is_semantic_documentation_path(path):
            continue
        parts = [path]
        headings = record.get("headings")
        if isinstance(headings, list):
            parts.extend(str(heading) for heading in headings if isinstance(heading, str))
        semantic_hints = record.get("semanticHints")
        if isinstance(semantic_hints, list):
            parts.extend(str(hint) for hint in semantic_hints if isinstance(hint, str))
        entries.append({"path": path, "kind": "documentation", "text": " ".join(parts)})

    if public_interface_index is not None:
        symbol_terms = public_interface_semantic_terms(public_interface_index)
        if symbol_terms:
            entries.append(
                {
                    "path": PUBLIC_INTERFACE_INDEX_OUTPUT,
                    "kind": "public_interface_index",
                    "text": " ".join(symbol_terms),
                }
            )

    return entries


def build_semantic_evidence_clusters(
    entries: list[dict[str, str]],
    enabled_contexts: set[str],
) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for rule in SEMANTIC_DOMAIN_RULES:
        if rule.required_context is not None and rule.required_context not in enabled_contexts:
            continue
        matched_terms: set[str] = set()
        evidence_paths: set[str] = set()
        evidence_kinds: set[str] = set()
        score = 0
        for entry in entries:
            text = entry["text"].lower()
            entry_matches = [term for term in rule.terms if semantic_rule_term_matches(text, term)]
            if not entry_matches:
                continue
            matched_terms.update(entry_matches)
            evidence_kind = entry.get("kind", "documentation")
            if evidence_kind != "repository":
                evidence_kinds.add(evidence_kind)
            if entry["path"] != "repository" and evidence_kind != "public_interface_index":
                evidence_paths.add(entry["path"])
            score += len(entry_matches)
        if score < rule.minimum_score:
            continue
        clusters.append(
            {
                "id": rule.cluster_id,
                "intentId": rule.intent_id,
                "label": rule.label,
                "score": score,
                "matchedTerms": sorted(matched_terms),
                "evidenceKinds": sorted(evidence_kinds),
                "evidencePaths": sorted(path for path in evidence_paths if path),
            }
        )
    return sorted(clusters, key=lambda item: (-int(item["score"]), str(item["id"])))


def semantic_rule_term_matches(text: str, term: str) -> bool:
    if " " in term or "-" in term:
        return term in text
    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def has_swift_semantic_context(
    package_records: list[dict[str, Any]],
    documentation_records: list[dict[str, Any]],
    public_interface_index: dict[str, Any] | None,
) -> bool:
    for record in package_records:
        path = str(record.get("path") or "").lower()
        package = record.get("package")
        if path.endswith("package.swift"):
            return True
        if not isinstance(package, dict):
            continue
        for key in ("ecosystem", "language"):
            value = package.get(key)
            if isinstance(value, str) and value.lower() == "swift":
                return True

    for record in documentation_records:
        path = str(record.get("path") or "").lower()
        if path.endswith("package.swift") or "/documentation.docc/" in path:
            return True
        headings = record.get("headings")
        if isinstance(headings, list) and any(
            isinstance(heading, str) and has_any(heading.lower(), "swift", "swiftui")
            for heading in headings
        ):
            return True

    if public_interface_index is None:
        return False
    packages = public_interface_index.get("packages")
    if not isinstance(packages, list):
        return False
    return any(
        isinstance(package, dict)
        and isinstance(package.get("language"), str)
        and package["language"].lower() == "swift"
        for package in packages
    )


def semantic_profile_paths(entries: list[dict[str, str]]) -> set[str]:
    return {
        entry["path"]
        for entry in entries
        if entry.get("path")
        and entry["path"] != "repository"
        and entry.get("kind") != "public_interface_index"
    }


def is_semantic_documentation_path(path: str) -> bool:
    if not path:
        return False
    lowered = path.lower()
    if any(part in lowered for part in ("/claude.md", "/agents.md", "/tasks_archive/")):
        return False
    return (
        lowered.startswith("readme")
        or lowered.startswith("docs/")
        or lowered.startswith("specs/prd/")
        or "/documentation.docc/" in lowered
    )


def public_interface_semantic_terms(public_interface_index: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()
    char_count = 0

    def add(
        value: Any,
        *,
        include_ngrams: bool = True,
        max_chars: int = PUBLIC_INTERFACE_SEMANTIC_IDENTIFIER_CHAR_LIMIT,
    ) -> None:
        nonlocal char_count
        if len(terms) >= PUBLIC_INTERFACE_SEMANTIC_TERM_LIMIT:
            return
        if not isinstance(value, str) or not value.strip():
            return
        for term in semantic_identifier_terms(
            value,
            include_ngrams=include_ngrams,
            max_chars=max_chars,
        ):
            if len(terms) >= PUBLIC_INTERFACE_SEMANTIC_TERM_LIMIT:
                break
            if term in seen:
                continue
            next_char_count = char_count + len(term) + 1
            if next_char_count > PUBLIC_INTERFACE_SEMANTIC_TEXT_CHAR_LIMIT:
                break
            seen.add(term)
            terms.append(term)
            char_count = next_char_count

    packages = public_interface_index.get("packages")
    if not isinstance(packages, list):
        return terms
    for package in packages:
        if not isinstance(package, dict):
            continue
        add(package.get("id"))
        add(package.get("path"))
        add(package.get("language"))
        entrypoints = package.get("entrypoints")
        if not isinstance(entrypoints, list):
            continue
        for entrypoint in entrypoints:
            if not isinstance(entrypoint, dict):
                continue
            add(entrypoint.get("path"))
            symbols = entrypoint.get("symbols")
            if not isinstance(symbols, list):
                continue
            for symbol in symbols:
                if not isinstance(symbol, dict):
                    continue
                add(symbol.get("name"))
                add(symbol.get("kind"))
    return terms


def semantic_identifier_terms(
    value: str,
    *,
    include_ngrams: bool = True,
    max_chars: int = PUBLIC_INTERFACE_SEMANTIC_IDENTIFIER_CHAR_LIMIT,
) -> list[str]:
    normalized = value.strip()[:max_chars]
    if not normalized:
        return []

    variants = {normalized.lower()}
    separated = re.sub(r"[_./:@#-]+", " ", normalized)
    separated = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", separated)
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", separated)
    separated = re.sub(r"\s+", " ", separated).strip().lower()
    if separated:
        variants.add(separated)

    tokens = [token for token in separated.split(" ") if token]
    variants.update(tokens)
    if include_ngrams:
        for size in (2, 3):
            for index in range(0, max(len(tokens) - size + 1, 0)):
                variants.add(" ".join(tokens[index : index + size]))

    return sorted(variant for variant in variants if variant)


def has_any(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def semantic_summary(repository_name: str, intents: set[str]) -> str:
    package_name = display_name(repository_name)
    if "intent.web.framework_surface" in intents:
        return (
            "Provide a statically evidenced web framework surface for HTTP routing, "
            f"middleware, handlers, and request/response context in {package_name}."
        )
    if "intent.swift.specification_pattern" in intents:
        return (
            "Provide a Swift Specification Pattern toolkit for composing reusable "
            "predicates, context-driven decisions, feature gates, reactive evaluation, "
            "and diagnostic tracing."
        )
    if "intent.ios.uikit_swiftui_migration" in intents:
        return (
            "Provide a screen-level composition framework for incrementally migrating "
            "UIKit-heavy iOS screens to mixed UIKit/SwiftUI surfaces."
        )
    if "intent.ios.screen_level_composition" in intents:
        return (
            "Provide a screen-level composition framework for declarative iOS screen "
            "state, layout, bindings, and lifecycle hooks."
        )
    if "intent.api.contract_surface" in intents:
        return (
            "Provide language-neutral API contract documentation and schema evidence "
            f"for {package_name}."
        )
    if "intent.metadata.schema_validation" in intents:
        return (
            "Provide language-neutral metadata schema validation and manifest evidence "
            f"for {package_name}."
        )
    if "intent.workflow.automation_pipeline" in intents:
        return (
            "Provide language-neutral workflow automation and validation pipeline evidence "
            f"for {package_name}."
        )
    if "intent.developer.tooling_surface" in intents:
        return (
            "Provide language-neutral developer tooling, CLI, and configuration evidence "
            f"for {package_name}."
        )
    if "intent.documentation.knowledge_base" in intents:
        return f"Provide language-neutral documentation knowledge-base evidence for {package_name}."
    return (
        "Provide deterministic public package metadata and semantic intent evidence "
        f"for {package_name}."
    )


def infer_intent_ids(
    package_name: str,
    summary: str,
    package: dict[str, Any] | None = None,
) -> list[str]:
    # Bootstrap-only baseline over package manifest name/description.
    # Other harvested files, including workflow files, are provenance evidence and do not
    # participate in intent inference.
    if package is not None and package.get("ecosystem") == "swift":
        return infer_swift_intent_ids(package_name, package)

    text = f"{package_name} {summary}".lower()
    intents = {"intent.package.javascript_library"}
    if "monorepo" in text or "workspace" in text:
        intents.add("intent.repository.package_workspace")
    if "react" in text:
        intents.add("intent.javascript.react_library")
    if "svelte" in text:
        intents.add("intent.javascript.svelte_library")
    if "node-based" in text or "node based" in text:
        intents.add("intent.ui.node_based_editor")
    if "flow chart" in text or "flow charts" in text or "workflow" in text:
        intents.add("intent.ui.flow_diagramming")
    if "diagram" in text or "diagrams" in text:
        intents.add("intent.ui.diagramming")
    if "core system" in text or package_name.endswith("/system"):
        intents.add("intent.ui.flow_system_utilities")
    return sorted(intents)


def infer_swift_intent_ids(package_name: str, package: dict[str, Any]) -> list[str]:
    products = package.get("products")
    product_names = (
        [
            product["name"]
            for product in products
            if isinstance(product, dict)
            and isinstance(product.get("name"), str)
            and product["name"].strip()
        ]
        if isinstance(products, list)
        else []
    )

    if product_names:
        return sorted(
            f"intent.swift.product.{package_label(product_name)}" for product_name in product_names
        )
    return [f"intent.swift.package.{package_label(package_name)}"]


def build_interfaces(
    package_records: list[dict[str, Any]],
    public_interface_index: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    interfaces_by_id: dict[str, dict[str, Any]] = {}
    interface_order: list[str] = []
    seen_interface_ids: set[str] = set()
    manifest_interface_ids_by_key: dict[tuple[str, str], str] = {}
    manifest_interface_ids_by_name: dict[str, list[str]] = {}
    for record in package_records:
        entry = manifest_interface_entry(record)
        if entry is None:
            continue
        interface_id = unique_id(entry["id"], seen_interface_ids)
        entry["id"] = interface_id
        interfaces_by_id[interface_id] = entry
        interface_order.append(interface_id)

        package_name = manifest_package_name(record)
        if package_name is not None:
            manifest_interface_ids_by_name.setdefault(package_name, []).append(interface_id)
            manifest_interface_ids_by_key[manifest_package_key(record)] = interface_id

    if public_interface_index is not None:
        enriched_manifest_ids: set[str] = set()
        packages = public_interface_index.get("packages", [])
        for package in sorted(packages, key=public_interface_package_sort_key):
            if not isinstance(package, dict):
                continue
            interface_id = matched_manifest_interface_id(
                package,
                manifest_interface_ids_by_key,
                manifest_interface_ids_by_name,
            )
            if interface_id is not None and interface_id in enriched_manifest_ids:
                interface_id = None

            base = interfaces_by_id.get(interface_id) if interface_id is not None else None
            if interface_id is None:
                interface_id = unique_id(public_interface_id(package), seen_interface_ids)
                interface_order.append(interface_id)
            else:
                enriched_manifest_ids.add(interface_id)
            interfaces_by_id[interface_id] = public_interface_entry(package, base, interface_id)

    return [interfaces_by_id[interface_id] for interface_id in interface_order]


def manifest_interface_entry(record: dict[str, Any]) -> dict[str, Any] | None:
    package = record["package"]
    package_name = package.get("name")
    if not isinstance(package_name, str) or not package_name.strip():
        return None
    outputs = [
        {
            "name": "package_manifest",
            "mediaTypes": ["application/json"],
        }
    ]
    if package.get("exports"):
        outputs.append(
            {
                "name": "package_exports",
                "mediaTypes": ["application/javascript", "text/css"],
            }
        )
    return {
        "id": slug_id(f"package.{package_label(package_name)}"),
        "kind": "library",
        "summary": f"Observed import surface for {package_name}.",
        "outputs": outputs,
    }


def public_interface_entry(
    package: dict[str, Any],
    base: dict[str, Any] | None,
    interface_id: str,
) -> dict[str, Any]:
    package_id = public_interface_package_name(package)
    entrypoints = public_interface_entrypoints(package)
    entrypoint_count = len(entrypoints)
    symbol_count = sum(entrypoint["symbolCount"] for entrypoint in entrypoints)
    entry = {
        "id": interface_id,
        "kind": "library",
        "summary": f"Observed public interface for {package_id} from PublicInterfaceIndex.",
        "source": "public_interface_index",
        "publicInterface": {
            "packageId": package_id,
            "packagePath": package.get("path"),
            "entrypointCount": entrypoint_count,
            "symbolCount": symbol_count,
        },
        "outputs": merge_interface_outputs(
            list(base.get("outputs", [])) if base is not None else [],
            [
                {
                    "name": "public_symbols",
                    "mediaTypes": [PUBLIC_INTERFACE_INDEX_MEDIA_TYPE],
                }
            ],
        ),
    }
    language = package.get("language")
    if isinstance(language, str) and language.strip():
        entry["language"] = language
    if entrypoints:
        entry["entrypoints"] = entrypoints
    return entry


def public_interface_entrypoints(package: dict[str, Any]) -> list[dict[str, Any]]:
    entrypoints = package.get("entrypoints")
    if not isinstance(entrypoints, list):
        return []

    summaries: list[dict[str, Any]] = []
    for entrypoint in sorted(entrypoints, key=entrypoint_sort_key):
        if not isinstance(entrypoint, dict):
            continue
        path = entrypoint.get("path")
        if not isinstance(path, str) or not path.strip():
            continue
        symbols = public_interface_symbols(entrypoint)
        summaries.append(
            {
                "path": path,
                "symbolCount": len(symbols),
                "symbols": symbols,
            }
        )
    return summaries


def public_interface_symbols(entrypoint: dict[str, Any]) -> list[dict[str, Any]]:
    symbols = entrypoint.get("symbols")
    if not isinstance(symbols, list):
        return []

    summaries: list[dict[str, Any]] = []
    for symbol in sorted(symbols, key=symbol_sort_key):
        if not isinstance(symbol, dict):
            continue
        name = symbol.get("name")
        kind = symbol.get("kind")
        if not isinstance(name, str) or not isinstance(kind, str):
            continue
        summary = {
            "name": name,
            "kind": kind,
        }
        signature = symbol.get("signature")
        if isinstance(signature, str) and signature.strip():
            summary["signature"] = signature
        evidence = symbol.get("evidence")
        if isinstance(evidence, dict):
            path = evidence.get("path")
            sha256 = evidence.get("sha256")
            if isinstance(path, str) and isinstance(sha256, str):
                summary["evidence"] = {"path": path, "sha256": sha256}
        summaries.append(summary)
    return summaries


def merge_interface_outputs(
    base_outputs: list[Any],
    extra_outputs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for output in [*base_outputs, *extra_outputs]:
        if not isinstance(output, dict):
            continue
        name = output.get("name")
        media_types = output.get("mediaTypes")
        if not isinstance(name, str) or not isinstance(media_types, list):
            continue
        normalized_media_types = tuple(str(media_type) for media_type in media_types)
        key = (name, normalized_media_types)
        if key in seen:
            continue
        seen.add(key)
        outputs.append({"name": name, "mediaTypes": list(normalized_media_types)})
    return outputs


def public_interface_id(package: dict[str, Any]) -> str:
    return slug_id(f"package.{package_label(public_interface_package_name(package))}")


def matched_manifest_interface_id(
    package: dict[str, Any],
    manifest_interface_ids_by_key: dict[tuple[str, str], str],
    manifest_interface_ids_by_name: dict[str, list[str]],
) -> str | None:
    package_name = public_interface_package_name(package)
    package_path = public_interface_package_path(package)
    interface_id = manifest_interface_ids_by_key.get((package_name, package_path))
    if interface_id is not None:
        return interface_id

    candidates = manifest_interface_ids_by_name.get(package_name, [])
    if len(candidates) == 1:
        return candidates[0]
    return None


def manifest_package_key(record: dict[str, Any]) -> tuple[str, str]:
    return (manifest_package_name(record) or "", manifest_package_root(record))


def manifest_package_name(record: dict[str, Any]) -> str | None:
    package = record.get("package")
    if not isinstance(package, dict):
        return None
    package_name = package.get("name")
    if not isinstance(package_name, str) or not package_name.strip():
        return None
    return package_name.strip()


def manifest_package_root(record: dict[str, Any]) -> str:
    path = record.get("path")
    if not isinstance(path, str) or not path.strip():
        return "."
    if path == "package.json":
        return "."
    if path.endswith("/package.json"):
        return path[: -len("/package.json")]
    return path


def public_interface_package_name(package: dict[str, Any]) -> str:
    package_id = package.get("id")
    if isinstance(package_id, str) and package_id.strip():
        return package_id.strip()
    package_path = package.get("path")
    if isinstance(package_path, str) and package_path.strip() and package_path != ".":
        return package_path.strip()
    return "public_interface"


def public_interface_package_path(package: dict[str, Any]) -> str:
    package_path = package.get("path")
    if not isinstance(package_path, str) or not package_path.strip():
        return "."
    return package_path.strip()


def public_interface_package_sort_key(package: Any) -> tuple[str, str]:
    if not isinstance(package, dict):
        return ("", "")
    return (str(package.get("path") or ""), str(package.get("id") or ""))


def entrypoint_sort_key(entrypoint: Any) -> str:
    if not isinstance(entrypoint, dict):
        return ""
    return str(entrypoint.get("path") or "")


def symbol_sort_key(symbol: Any) -> tuple[str, str, str]:
    if not isinstance(symbol, dict):
        return ("", "", "")
    return (
        str(symbol.get("name") or ""),
        str(symbol.get("kind") or ""),
        str(symbol.get("signature") or ""),
    )


def build_evidence(
    manifest_capabilities: list[str],
    inbound_interfaces: list[dict[str, Any]],
    public_interface_index: dict[str, Any] | None,
    semantic_profile: SemanticIntentProfile | None = None,
) -> list[dict[str, Any]]:
    evidence = [
        {
            "id": "harvest_snapshot",
            "kind": "package_manifest",
            "path": "harvest.json",
            "supports": ["intent.summary", "scope", "provides.capabilities"]
            + [f"provides.capabilities.{capability_id}" for capability_id in manifest_capabilities],
        }
    ]
    if semantic_profile is not None:
        evidence.append(
            {
                "id": "semantic_intent_static_evidence",
                "kind": "documentation",
                "paths": semantic_profile.evidence_paths,
                "semanticEvidenceIndex": {
                    "schemaVersion": 1,
                    "clusters": semantic_profile.clusters,
                },
                "supports": [
                    "intent.summary",
                    "provides.capabilities.intentIds",
                ],
            }
        )
    if public_interface_index is None:
        return evidence

    supported_interfaces = [
        f"interfaces.inbound.{interface['id']}"
        for interface in inbound_interfaces
        if interface.get("source") == "public_interface_index"
    ]
    evidence.append(
        {
            "id": "public_interface_index",
            "kind": "public_interface_index",
            "path": PUBLIC_INTERFACE_INDEX_OUTPUT,
            "artifactKind": PUBLIC_INTERFACE_INDEX_KIND,
            "mediaType": PUBLIC_INTERFACE_INDEX_MEDIA_TYPE,
            "schemaVersion": public_interface_index.get("schemaVersion"),
            "summary": public_interface_index.get("summary"),
            "supports": ["interfaces.inbound", *supported_interfaces],
        }
    )
    return evidence


def public_interface_provenance(index: dict[str, Any]) -> dict[str, Any]:
    analyzers = []
    for analyzer in index.get("analyzers", []):
        if not isinstance(analyzer, dict):
            continue
        analyzers.append(
            {
                "id": analyzer.get("id"),
                "version": analyzer.get("version"),
                "confidence": analyzer.get("confidence"),
                "execution": analyzer.get("execution"),
            }
        )
    return {
        "sourceRevision": index.get("sourceRevision"),
        "summary": index.get("summary"),
        "analyzers": analyzers,
    }


def infer_license(
    package_records: list[dict[str, Any]],
    license_records: list[dict[str, Any]],
) -> str:
    return infer_license_with_evidence(package_records, license_records).name


def infer_license_with_evidence(
    package_records: list[dict[str, Any]],
    license_records: list[dict[str, Any]],
) -> LicenseInference:
    licenses = [
        (record.get("path"), record["package"]["license"])
        for record in package_records
        if isinstance(record["package"].get("license"), str)
        and record["package"]["license"].strip()
    ]
    if licenses:
        path, license_name = licenses[0]
        return LicenseInference(
            name=license_name,
            evidence={
                "source": "manifest",
                "confidence": "high",
                "paths": [path] if isinstance(path, str) and path else [],
            },
        )

    license_hints = [
        (record.get("path"), record.get("licenseHint"))
        for record in license_records
        if isinstance(record.get("licenseHint"), str) and record["licenseHint"].strip()
    ]
    if license_hints:
        path, hint = license_hints[0]
        return LicenseInference(
            name=hint,
            evidence={
                "source": "license_file_hint",
                "confidence": "medium",
                "paths": [path] if isinstance(path, str) and path else [],
            },
        )

    license_paths = [
        path for path in (record.get("path") for record in license_records) if isinstance(path, str)
    ]
    if license_paths:
        return LicenseInference(
            name="UNKNOWN",
            evidence={
                "source": "ambiguous_license_file",
                "confidence": "low",
                "paths": license_paths,
            },
        )

    return LicenseInference(
        name="UNKNOWN",
        evidence={
            "source": "absent",
            "confidence": "high",
            "paths": [],
        },
    )


def infer_compatibility(
    package_records: list[dict[str, Any]],
    snapshot: dict[str, Any] | None = None,
    intent_ids: list[str] | None = None,
) -> dict[str, list[str]]:
    languages = compatibility_languages(package_records, snapshot)
    platforms = compatibility_platforms(languages, intent_ids or [])
    return {"platforms": platforms, "languages": languages}


def compatibility_languages(
    package_records: list[dict[str, Any]],
    snapshot: dict[str, Any] | None,
) -> list[str]:
    detected: set[str] = set()
    project_profile = snapshot.get("projectProfile") if isinstance(snapshot, dict) else None
    profile_languages = (
        project_profile.get("languages") if isinstance(project_profile, dict) else None
    )
    if isinstance(profile_languages, list):
        high_signal_languages = [
            item
            for item in profile_languages
            if isinstance(item, dict) and item.get("confidence") != "low"
        ]
        selected_profile_languages = high_signal_languages or profile_languages
        for item in profile_languages:
            if item not in selected_profile_languages:
                continue
            if not isinstance(item, dict):
                continue
            language_id = item.get("id")
            if isinstance(language_id, str) and language_id.strip():
                detected.update(compatibility_language_names(language_id))

    for record in package_records:
        package = record.get("package")
        if not isinstance(package, dict):
            continue
        for key in ("language", "ecosystem"):
            value = package.get(key)
            if isinstance(value, str) and value.strip():
                detected.update(compatibility_language_names(value))

    dependencies = {
        dependency
        for record in package_records
        for dependency in package_dependency_names(record["package"])
    }
    if dependencies & {"typescript", "tslib"} or (
        "javascript" in detected and any("typescript" in dependency for dependency in dependencies)
    ):
        detected.add("typescript")
    if not detected:
        return []
    ordered_languages = [
        language for language in COMPATIBILITY_LANGUAGE_ORDER if language in detected
    ]
    return ordered_languages + sorted(detected - set(COMPATIBILITY_LANGUAGE_ORDER))


COMPATIBILITY_LANGUAGE_ORDER = (
    "typescript",
    "javascript",
    "swift",
    "objective-c",
    "python",
    "java",
    "kotlin",
    "go",
    "php",
    "c",
    "c++",
    "ruby",
)


def compatibility_language_names(language_id: str) -> set[str]:
    normalized = language_id.strip().lower()
    if normalized in {"javascript-typescript", "javascript", "typescript", "npm", "pnpm"}:
        return {"javascript"}
    if normalized in {"swift", "swiftpm"}:
        return {"swift"}
    if normalized in {"objective-c", "objc", "xcode", "cocoapods"}:
        return {"objective-c"}
    if normalized in {"python", "pypi"}:
        return {"python"}
    if normalized == "java-kotlin":
        return {"java", "kotlin"}
    if normalized in {"java", "kotlin", "go", "php", "ruby"}:
        return {normalized}
    if normalized in {"c-cpp", "cpp", "c++"}:
        return {"c", "c++"}
    if normalized == "c":
        return {"c"}
    return {normalized}


def compatibility_platforms(languages: list[str], intent_ids: list[str]) -> list[str]:
    platforms: set[str] = set()
    if any(intent_id.startswith("intent.ios.") for intent_id in intent_ids):
        platforms.update({"ios", "macos"})
    if any(intent_id.startswith("intent.web.") for intent_id in intent_ids):
        platforms.update({"web", "any"})
    if "javascript" in languages or "typescript" in languages:
        platforms.update({"web", "node"})
    apple_project = "objective-c" in languages
    if "swift" in languages and not apple_project and not platforms.intersection({"ios", "macos"}):
        platforms.update({"macos", "linux"})
    if "objective-c" in languages:
        platforms.update({"ios", "macos"})
    if {"java", "kotlin"} & set(languages):
        platforms.add("jvm")
    if any(language in languages for language in ("python", "go", "php", "ruby", "c", "c++")):
        platforms.add("any")
    if not platforms:
        return []
    ordered_platforms = [
        platform for platform in COMPATIBILITY_PLATFORM_ORDER if platform in platforms
    ]
    return ordered_platforms + sorted(platforms - set(COMPATIBILITY_PLATFORM_ORDER))


COMPATIBILITY_PLATFORM_ORDER = (
    "ios",
    "macos",
    "linux",
    "windows",
    "web",
    "node",
    "jvm",
    "any",
)


def package_dependency_names(package: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        value = package.get(key)
        if isinstance(value, list):
            names.extend(str(item) for item in value)
    return names


def infer_intent_summary(package_name: str, package_records: list[dict[str, Any]]) -> str:
    for record in package_records:
        description = record["package"].get("description")
        if isinstance(description, str) and description.strip():
            return (
                f"Capture observed public package intent for {package_name}: {description.strip()}"
            )
    return f"Capture observed public package intent for {package_name}."


def foreign_repository_artifact(source: dict[str, Any]) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "id": "upstream_repository",
        "role": "primary_intent_source",
    }
    repository = source.get("repository")
    if isinstance(repository, str):
        artifact["uri"] = repository
    revision = source.get("revision")
    if isinstance(revision, str):
        artifact["revision"] = revision
    return artifact


def package_label(package_name: str) -> str:
    name = package_name.strip()
    if "/" in name:
        name = name.rsplit("/", 1)[-1]
    if name.startswith("@"):
        name = name[1:]
    return slug_id(name)


def slug_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^@+", "", value)
    value = value.replace("/", ".")
    value = re.sub(r"[^a-z0-9.]+", "_", value)
    value = re.sub(r"[._]+", lambda match: "." if "." in match.group(0) else "_", value)
    value = value.strip("._-")
    if not value or not re.match(r"^[a-z]", value):
        value = f"generated_{value}" if value else "generated"
    return value


def unique_id(base: str, seen: set[str]) -> str:
    candidate = slug_id(base)
    if candidate not in seen:
        seen.add(candidate)
        return candidate
    index = 2
    while f"{candidate}_{index}" in seen:
        index += 1
    unique = f"{candidate}_{index}"
    seen.add(unique)
    return unique


def display_name(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[._-]+", value) if part) or value


def render_yaml(value: Any) -> str:
    return "\n".join(render_yaml_lines(value, 0)) + "\n"


def render_yaml_lines(value: Any, indent: int) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        if not value:
            return [f"{prefix}{{}}"]
        lines: list[str] = []
        for key, child in value.items():
            if is_inline(child):
                lines.append(f"{prefix}{key}: {render_inline(child)}")
            else:
                lines.append(f"{prefix}{key}:")
                lines.extend(render_yaml_lines(child, indent + 2))
        return lines
    if isinstance(value, list):
        if not value:
            return [f"{prefix}[]"]
        lines = []
        for item in value:
            if is_inline(item):
                lines.append(f"{prefix}- {render_inline(item)}")
            elif isinstance(item, dict):
                item_lines = render_yaml_lines(item, indent + 2)
                first_line = item_lines[0][indent + 2 :]
                lines.append(f"{prefix}- {first_line}")
                lines.extend(item_lines[1:])
            else:
                lines.append(f"{prefix}-")
                lines.extend(render_yaml_lines(item, indent + 2))
        return lines
    return [f"{prefix}{render_scalar(value)}"]


def is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def is_inline(value: Any) -> bool:
    return is_scalar(value) or value == [] or value == {}


def render_inline(value: Any) -> str:
    if value == []:
        return "[]"
    if value == {}:
        return "{}"
    return render_scalar(value)


def render_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    plain_safe = (
        re.match(r"^[a-zA-Z0-9][a-zA-Z0-9._/@+ -]*$", text)
        and text.strip() == text
        and ":" not in text
    )
    if plain_safe:
        if text.lower() in YAML_RESERVED_SCALARS:
            return json.dumps(text)
        return text
    return json.dumps(text)
