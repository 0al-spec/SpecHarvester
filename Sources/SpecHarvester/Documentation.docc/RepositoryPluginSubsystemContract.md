# Repository Plugin Subsystem Contract

Phase 38 defines the broader repository plugin subsystem contract that should
eventually unify repository parsing profiles from Phase 36 and repository
profile detection from Phase 37.

The subsystem is language- and framework-agnostic. Python, JavaScript,
FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle, and other ecosystems
are examples only, not normative plugin rules.

```text
register plugins
  -> collect bounded static evidence
  -> evaluate applicability
  -> select, fallback, or block deterministically
  -> emit producer-side evidence
  -> let downstream review decide what to trust
```

## Goals

- Define plugin identity and versioning.
- Define plugin roles.
- Define registration metadata.
- Define static input evidence.
- Define applicability checks.
- Define deterministic selection boundaries.
- Define output artifact categories.
- Define diagnostics, authority, and trust boundaries.

## Non-Goals

This contract does not implement plugin loading or plugin execution.

Plugins must not clone or fetch repositories, install dependencies, execute
harvested code, invoke package managers, run builds or tests, run AI, accept
packages, accept relations, publish registry metadata, seed baselines, remove
`preview_only`, treat plugin output as registry truth, or treat AI output as
registry truth.

## Plugin Identity

Each plugin declaration should include:

| Field | Requirement |
| --- | --- |
| `pluginId` | Stable namespaced id. |
| `version` | Plugin contract version. |
| `role` | Plugin role category. |
| `title` | Human-readable label. |
| `summary` | Short statement of provided evidence or applicability signal. |
| `authority` | Producer-side authority string, never registry authority. |

## Plugin Roles

| Role | Purpose |
| --- | --- |
| `parser_profile` | Classifies paths for public interface, semantic usage, documentation, examples, tests, generated files, tooling, internal files, or ignored files. |
| `repository_profile` | Classifies repository shape and emits advisory hints such as package-set root, member package, example package, or evidence-only source. |
| `evidence_producer` | Emits bounded static evidence artifacts such as public-interface indexes, manifest summaries, source graphs, or license summaries. |
| `topology_helper` | Proposes package-set membership or relation candidates from static evidence. |
| `review_surface` | Renders or summarizes evidence for human review without changing generated package truth. |

## Registration Metadata

The future machine-readable registry fixture is planned as
`SpecHarvesterRepositoryPluginRegistry`:

P38-T2 records the first fixture in <doc:RepositoryPluginRegistryFixture> and
`tests/fixtures/repository_plugins/generic-registry.example.json`.

```json
{
  "apiVersion": "spec-harvester.repository-plugins/v0",
  "kind": "SpecHarvesterRepositoryPluginRegistry",
  "schemaVersion": 1,
  "authority": "producer_plugin_registry_only",
  "plugins": []
}
```

Registration metadata should cover plugin ids, versions, roles, producer-side
authority, input evidence kinds, output artifact kinds, safety constraints,
applicability signals, conflicts, fallback behavior, diagnostics, and
non-authority statements.

## Static Evidence Inputs

Applicability checks must use bounded static evidence:

- repository source manifest metadata;
- `harvest.json`;
- `workspace-inventory.json`;
- public-interface indexes;
- parser profile decisions;
- repository profile detections;
- allowlisted manifest and lockfile paths;
- package metadata extracted from local files;
- operator-provided labels or explicit profile ids.

Applicability must not depend on network discovery, package registry queries,
dependency installation, imported package execution, build outputs, or live
model calls.

## Applicability Report

P38-T3 records the first fixture in
<doc:RepositoryPluginApplicabilityReportFixture> and
`tests/fixtures/repository_plugins/generic-applicability-report.example.json`.

The selection report shape is
`SpecHarvesterRepositoryPluginApplicabilityReport`:

```json
{
  "apiVersion": "spec-harvester.repository-plugin-applicability/v0",
  "kind": "SpecHarvesterRepositoryPluginApplicabilityReport",
  "schemaVersion": 1,
  "authority": "producer_plugin_applicability_only",
  "mode": "auto",
  "selectedPlugins": [],
  "rejectedPlugins": [],
  "fallbackPlugins": [],
  "blockedPlugins": [],
  "diagnostics": []
}
```

The report explains why a plugin was selected, rejected, blocked, or why the
system fell back to generic behavior. Each decision carries
`decisionAuthority: producer_plugin_applicability_only` and
`pluginOutputAuthority: producer_side_evidence_only`.

## Deterministic Selection Boundaries

Selection precedence should be deterministic:

1. explicit operator or source-manifest override;
2. high-confidence plugin applicability with no conflicts;
3. documented fallback plugin or generic behavior;
4. blocked decision with diagnostics when evidence is unsafe or ambiguous.

Ambiguous, missing, conflicting, or low-confidence signals must not silently
select technology-specific plugins.

## Output Artifact Categories

Plugins may produce or reference bounded artifacts such as
`repository_profile_detection`, `repository_parsing_profile_decision`,
`public_interface_index`, `workspace_inventory`, `manifest_summary`,
`package_topology_hint`, `candidate_quality_signal`, or `review_panel_data`.

Each output category should declare whether it is candidate-generation
evidence, author review evidence, SpecPM handoff evidence, or viewer/report
only evidence. No plugin output category is accepted package truth.

## Diagnostics

Diagnostics should include `severity`, `code`, `message`, `evidencePaths`, and
`pluginId`. Stable reason codes should distinguish selected, rejected,
fallback, blocked, low-confidence, conflict, and unsafe-input cases.

## Relationship to Existing Phases

Phase 36 parser profiles map to `parser_profile`. Phase 37 repository profiles
map to `repository_profile`.

Phase 38 does not rewrite either mechanism. It defines the common vocabulary
for registration, applicability, sidecar evidence, and review boundaries.

## Trust Boundary

Repository plugins are producer-side evidence producers and applicability
helpers. They can improve candidate generation and review, but they do not
replace SpecPM validation, maintainer acceptance, package relation acceptance,
or registry publication.

```text
plugin output = review evidence
SpecPM acceptance = maintainer-controlled registry decision
```
