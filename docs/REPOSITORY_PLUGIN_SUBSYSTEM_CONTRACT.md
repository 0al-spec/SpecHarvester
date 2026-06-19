# Repository Plugin Subsystem Contract

Status: Phase 38 contract plan.

SpecHarvester already has two related mechanisms:

- repository parsing profiles from Phase 36, which classify source paths before
  public-interface indexing;
- repository profile detection from Phase 37, which selects generic repository
  shapes before path classification and drafting.

The repository plugin subsystem is the broader contract that should eventually
unify those mechanisms without making any language, framework, package
manager, or repository shape normative.

```text
register plugins
  -> collect bounded static evidence
  -> evaluate applicability
  -> select, fallback, or block deterministically
  -> emit producer-side evidence
  -> let downstream review decide what to trust
```

## Goals

- Define plugin identity and versioning before adding more plugin-like
  mechanisms.
- Define plugin roles that cover parser profiles, repository profiles, static
  evidence producers, topology helpers, and review surfaces.
- Define registration metadata, input evidence, output artifact categories,
  diagnostics, and deterministic selection boundaries.
- Preserve a language- and framework-agnostic core. Python, JavaScript,
  FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle, and other
  ecosystems are examples only.
- Keep plugin output as producer-side evidence, not registry truth.

## Non-Goals

This contract does not implement plugin loading, execute plugin code, run real
repositories, or add the machine-readable registry fixture. Those follow in
later Phase 38 tasks.

Plugins must not:

- clone or fetch repositories;
- install dependencies;
- execute harvested code;
- invoke package managers;
- run builds or tests from harvested projects;
- run AI;
- accept packages;
- accept relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- treat plugin output as registry truth;
- treat AI output as registry truth.

## Plugin Identity

Every plugin declaration needs a stable identity:

| Field | Requirement |
| --- | --- |
| `pluginId` | Stable reverse-domain or namespaced id, for example `spec_harvester.generic.repository_profile.v0`. |
| `version` | Plugin contract version, independent from the repository or generated SpecPM package version. |
| `role` | One of the role categories below. |
| `title` | Human-readable label for docs and review reports. |
| `summary` | Short statement of what evidence or applicability signal the plugin provides. |
| `authority` | Producer-side authority string, never registry authority. |

Plugin ids should be stable across implementation rewrites. If semantics
change incompatibly, introduce a new versioned id instead of silently changing
the meaning of an existing plugin.

## Plugin Roles

| Role | Purpose | Existing/Future mapping |
| --- | --- | --- |
| `parser_profile` | Classifies repository paths into public interface, semantic usage, documentation, tests, generated files, tooling, internal files, or ignored files. | Phase 36 repository parsing profiles. |
| `repository_profile` | Classifies repository shape and emits advisory hints such as package-set root, member package, example package, or evidence-only source. | Phase 37 repository profile detection. |
| `evidence_producer` | Emits bounded static evidence artifacts such as public-interface indexes, manifest summaries, source graphs, or license summaries. | Future analyzer/evidence plugins. |
| `topology_helper` | Proposes package-set membership or relation candidates from static evidence. | Future package-set helper plugins. |
| `review_surface` | Renders or summarizes evidence for humans without changing generated package truth. | Future viewer/report helpers. |

A plugin can declare multiple roles only when each role has separate input
requirements, output artifacts, diagnostics, and authority statements.

## Registration Metadata

The future machine-readable registry fixture is planned as
`SpecHarvesterRepositoryPluginRegistry`.

P38-T2 records the first fixture in
[`REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`](REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md)
and
`tests/fixtures/repository_plugins/generic-registry.example.json`.

```json
{
  "apiVersion": "spec-harvester.repository-plugins/v0",
  "kind": "SpecHarvesterRepositoryPluginRegistry",
  "schemaVersion": 1,
  "authority": "producer_plugin_registry_only",
  "plugins": [
    {
      "pluginId": "spec_harvester.generic.repository_profile.v0",
      "version": "0.1.0",
      "role": "repository_profile",
      "authority": "producer_side_evidence_only",
      "inputEvidenceKinds": ["workspace_inventory", "harvest_manifest_paths"],
      "outputArtifactKinds": ["repository_profile_detection"],
      "safety": {
        "execution": "none",
        "networkAccess": "none",
        "packageManagers": "not_invoked"
      },
      "applicabilitySignals": ["root_manifest", "workspace_manifest", "member_manifest"],
      "fallbackBehavior": "fallback_to_generic_repository_profile"
    }
  ]
}
```

Required registration categories:

- plugin identity and versioning;
- plugin roles;
- input evidence kinds;
- output artifact kinds;
- safety constraints;
- applicability signals;
- conflict declarations;
- fallback behavior;
- diagnostics emitted by the plugin or selector;
- non-authority statements.

## Static Input Evidence

Applicability must be evaluated from bounded static evidence that SpecHarvester
already has or explicitly collected without execution:

- repository source manifest metadata;
- `harvest.json` file records and digests;
- `workspace-inventory.json`;
- public-interface indexes;
- parser profile decisions;
- repository profile detections;
- allowlisted manifest and lockfile paths;
- package metadata extracted from local files;
- operator-provided labels or explicit profile ids.

Plugin applicability must not depend on network discovery, package registry
queries, dependency installation, imported package execution, build outputs, or
live model calls.

## Applicability Report

P38-T3 records the first fixture in
[`REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md)
and
`tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
P38-T5 adds cross-ecosystem examples in
[`REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md)
and `tests/fixtures/repository_plugins/cross_ecosystem/`.
P38-T6 records a real FastMCP comparison in
[`REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`](REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md)
and
`tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.

The selection report shape is
`SpecHarvesterRepositoryPluginApplicabilityReport`.

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

Plugin decisions may influence candidate generation only through explicit
sidecar evidence. They must not rewrite accepted package state, mutate SpecPM
registry inputs, or remove review gates.

## Output Artifact Categories

Plugins may produce or reference bounded artifacts such as:

- `repository_profile_detection`;
- `repository_parsing_profile_decision`;
- `public_interface_index`;
- `workspace_inventory`;
- `manifest_summary`;
- `package_topology_hint`;
- `candidate_quality_signal`;
- `review_panel_data`.

Every output category must declare whether it is:

- candidate-generation evidence;
- author review evidence;
- SpecPM handoff evidence;
- viewer/report-only evidence.

No plugin output category is accepted package truth.

## Diagnostics

Diagnostics should be machine-readable and reviewable:

| Field | Purpose |
| --- | --- |
| `severity` | `info`, `warning`, or `error`. |
| `code` | Stable reason code. |
| `message` | Human-readable explanation. |
| `evidencePaths` | Static paths that informed the diagnostic. |
| `pluginId` | Plugin that emitted or caused the diagnostic. |

Examples:

- `plugin_selected_from_static_evidence`;
- `plugin_rejected_low_confidence`;
- `plugin_rejected_conflict`;
- `plugin_blocked_unsafe_input`;
- `plugin_fallback_generic_behavior`.

## Relationship to Phase 36 and Phase 37

Phase 36 parser profiles become the first `parser_profile` role family. They
answer:

```text
Which paths are public interface evidence, semantic usage evidence,
documentation, examples, tests, generated files, tooling, internal files, or
ignored files?
```

Phase 37 repository profiles become the first `repository_profile` role family.
They answer:

```text
What repository shape is visible from static evidence, and which advisory
hints should downstream drafting consider?
```

Phase 38 does not rewrite those mechanisms. It defines the common vocabulary
that future tasks can use to register them, evaluate applicability, emit
sidecar evidence, and review decisions consistently.

Phase 39 starts the static evaluator layer in
[`STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`](STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md).
That plan keeps the same registry/applicability vocabulary but moves from
operator-authored sidecars toward deterministic derivation from a static
evidence envelope.

P39-T2 records the static evidence envelope fixture in
[`REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`](REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md)
and
`tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.

## Trust Boundary

Repository plugins are producer-side evidence producers and applicability
helpers. They can improve candidate generation and review, but they do not
replace SpecPM validation, maintainer acceptance, package relation acceptance,
or registry publication.

The trust boundary is:

```text
plugin output = review evidence
SpecPM acceptance = maintainer-controlled registry decision
```
