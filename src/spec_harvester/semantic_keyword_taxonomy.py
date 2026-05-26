from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticDomainRule:
    cluster_id: str
    intent_id: str
    label: str
    terms: tuple[str, ...]
    required_context: str | None = None
    minimum_score: int = 2


@dataclass(frozen=True)
class SemanticKeywordTaxonomy:
    rules: tuple[SemanticDomainRule, ...]
    hint_terms: tuple[str, ...]

    def domain_rules(self) -> tuple[SemanticDomainRule, ...]:
        return self.rules

    def markdown_hint_terms(self) -> tuple[str, ...]:
        return self.hint_terms


def ordered_unique_terms(*groups: tuple[str, ...]) -> tuple[str, ...]:
    terms: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for term in group:
            if term in seen:
                continue
            seen.add(term)
            terms.append(term)
    return tuple(terms)


WEB_FRAMEWORK_SURFACE_TERMS = (
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
)
WEB_HTTP_ROUTING_TERMS = (
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
)
WEB_MIDDLEWARE_PIPELINE_TERMS = (
    "middleware",
    "middlewares",
    "handler chain",
    "handlers chain",
    "before request",
    "after request",
    "request hook",
    "response pipeline",
)
WEB_REQUEST_RESPONSE_CONTEXT_TERMS = (
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
)
API_CONTRACT_SURFACE_TERMS = (
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
)
METADATA_SCHEMA_VALIDATION_TERMS = (
    "metadata",
    "schema",
    "validation",
    "validator",
    "manifest",
    "configuration",
    "config",
    "json schema",
)
WORKFLOW_AUTOMATION_PIPELINE_TERMS = (
    "workflow",
    "automation",
    "pipeline",
    "task",
    "validation",
    "command",
    "commands",
)
DEVELOPER_TOOLING_SURFACE_TERMS = (
    "cli",
    "command",
    "commands",
    "developer tool",
    "tooling",
    "plugin",
    "extension",
    "sdk",
    "configuration",
)
DOCUMENTATION_KNOWLEDGE_BASE_TERMS = (
    "documentation",
    "guide",
    "reference",
    "tutorial",
    "manual",
)
SWIFT_SPECIFICATION_PATTERN_TERMS = (
    "specification",
    "specifications",
    "specificationkit",
    "satisfies",
    "conditional satisfies",
)
SWIFT_PREDICATE_COMPOSITION_TERMS = (
    "predicate",
    "predicates",
    "composable business logic",
    "composition and reusability",
    "composite specification",
    "firstmatchspec",
)
SWIFT_CONTEXT_DRIVEN_DECISIONING_TERMS = (
    "context provider",
    "context providers",
    "compositecontextprovider",
    "networkcontextprovider",
    "persistentcontextprovider",
    "platform-specific context providers",
    "decision making",
)
SWIFT_FEATURE_GATING_TERMS = (
    "feature gating",
    "feature flag",
    "feature flags",
    "conditional",
    "thresholdspec",
    "weightedspec",
)
SWIFT_REACTIVE_SPECIFICATION_EVALUATION_TERMS = (
    "reactive wrappers",
    "reactive integration",
    "observedsatisfies",
    "observedmaybe",
    "swiftui integration",
    "combine",
    "observation",
)
SWIFT_SPECIFICATION_TRACING_TERMS = (
    "specificationtracer",
    "tracing",
    "trace",
    "debugging",
    "performance analysis",
    "dot graph",
)

MARKDOWN_SEMANTIC_HINT_TERMS = ordered_unique_terms(
    ("api contract", "json schema"),
    API_CONTRACT_SURFACE_TERMS,
    ("validation", "validator"),
    ("metadata", "manifest", "configuration", "config"),
    ("workflow", "automation", "pipeline", "task"),
    DEVELOPER_TOOLING_SURFACE_TERMS,
    DOCUMENTATION_KNOWLEDGE_BASE_TERMS,
    (
        "web framework",
        "http framework",
        "microframework",
        "wsgi",
        "asgi",
        "http server",
        "route",
        "routes",
        "routing",
        "router",
        "middleware",
        "middlewares",
        "handler",
        "handlers",
        "request context",
        "application context",
        "blueprint",
        "template",
        "templates",
        "json",
        "session",
        "cookie",
        "cookies",
    ),
)

SEMANTIC_DOMAIN_RULES = (
    SemanticDomainRule(
        cluster_id="web.framework_surface",
        intent_id="intent.web.framework_surface",
        label="Web Framework Surface",
        terms=WEB_FRAMEWORK_SURFACE_TERMS,
        minimum_score=4,
    ),
    SemanticDomainRule(
        cluster_id="web.http_routing",
        intent_id="intent.web.http_routing",
        label="HTTP Routing Surface",
        terms=WEB_HTTP_ROUTING_TERMS,
        minimum_score=3,
    ),
    SemanticDomainRule(
        cluster_id="web.middleware_pipeline",
        intent_id="intent.web.middleware_pipeline",
        label="Middleware Pipeline",
        terms=WEB_MIDDLEWARE_PIPELINE_TERMS,
    ),
    SemanticDomainRule(
        cluster_id="web.request_response_context",
        intent_id="intent.web.request_response_context",
        label="Request/Response Context",
        terms=WEB_REQUEST_RESPONSE_CONTEXT_TERMS,
        minimum_score=4,
    ),
    SemanticDomainRule(
        cluster_id="api.contract_surface",
        intent_id="intent.api.contract_surface",
        label="API Contract Surface",
        terms=API_CONTRACT_SURFACE_TERMS,
    ),
    SemanticDomainRule(
        cluster_id="metadata.schema_validation",
        intent_id="intent.metadata.schema_validation",
        label="Metadata Schema Validation",
        terms=METADATA_SCHEMA_VALIDATION_TERMS,
    ),
    SemanticDomainRule(
        cluster_id="workflow.automation_pipeline",
        intent_id="intent.workflow.automation_pipeline",
        label="Workflow Automation Pipeline",
        terms=WORKFLOW_AUTOMATION_PIPELINE_TERMS,
    ),
    SemanticDomainRule(
        cluster_id="developer.tooling_surface",
        intent_id="intent.developer.tooling_surface",
        label="Developer Tooling Surface",
        terms=DEVELOPER_TOOLING_SURFACE_TERMS,
    ),
    SemanticDomainRule(
        cluster_id="documentation.knowledge_base",
        intent_id="intent.documentation.knowledge_base",
        label="Documentation Knowledge Base",
        terms=DOCUMENTATION_KNOWLEDGE_BASE_TERMS,
    ),
    SemanticDomainRule(
        cluster_id="swift.specification_pattern",
        intent_id="intent.swift.specification_pattern",
        label="Swift Specification Pattern",
        terms=SWIFT_SPECIFICATION_PATTERN_TERMS,
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.predicate_composition",
        intent_id="intent.swift.predicate_composition",
        label="Predicate Composition",
        terms=SWIFT_PREDICATE_COMPOSITION_TERMS,
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.context_driven_decisioning",
        intent_id="intent.swift.context_driven_decisioning",
        label="Context-Driven Decisioning",
        terms=SWIFT_CONTEXT_DRIVEN_DECISIONING_TERMS,
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.feature_gating",
        intent_id="intent.swift.feature_gating",
        label="Feature Gating",
        terms=SWIFT_FEATURE_GATING_TERMS,
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.reactive_specification_evaluation",
        intent_id="intent.swift.reactive_specification_evaluation",
        label="Reactive Specification Evaluation",
        terms=SWIFT_REACTIVE_SPECIFICATION_EVALUATION_TERMS,
        required_context="swift",
    ),
    SemanticDomainRule(
        cluster_id="swift.specification_tracing",
        intent_id="intent.swift.specification_tracing",
        label="Specification Tracing",
        terms=SWIFT_SPECIFICATION_TRACING_TERMS,
        required_context="swift",
    ),
)

SEMANTIC_KEYWORD_TAXONOMY = SemanticKeywordTaxonomy(
    rules=SEMANTIC_DOMAIN_RULES,
    hint_terms=MARKDOWN_SEMANTIC_HINT_TERMS,
)
