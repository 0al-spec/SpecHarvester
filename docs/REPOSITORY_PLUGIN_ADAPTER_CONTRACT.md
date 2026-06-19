# Repository Plugin Adapter Contract

Status: Phase 40 contract plan.

P40-T1 defines the language- and framework-agnostic contract for future
repository plugin adapters. It extends the Phase 38 repository plugin
subsystem and the Phase 39 static applicability evaluator without adding
adapter loading or execution.

```text
static evidence
  -> static applicability evaluation
  -> optional adapter manifest preflight
  -> disabled-by-default adapter execution policy
  -> review-only adapter output evidence
  -> downstream author/maintainer review
```

Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle,
and other ecosystems are examples only. No ecosystem is normative.

## Goals

- Define adapter identity and manifest versioning before implementation.
- Define declared input evidence and output artifact categories.
- Define execution modes and sandbox expectations before any runtime path.
- Define diagnostics and preflight decisions for missing or unsafe evidence.
- Preserve static applicability as the default safe path.
- Keep adapter output as producer-side evidence, not registry truth.

## Non-Goals

P40-T1 does not implement adapter manifests, adapter preflight, adapter loading,
or adapter execution.

Repository plugin adapters must not:

- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- run builds or tests from harvested projects;
- perform network discovery;
- run AI unless a future explicit AI policy allows proposal-only use;
- accept packages;
- accept relations;
- seed baselines;
- publish registry metadata;
- remove `preview_only`;
- treat adapter output as registry truth;
- treat AI output as registry truth.

## Relationship to Existing Plugin Evidence

The adapter contract does not replace the existing plugin subsystem:

| Layer | Artifact | Authority |
| --- | --- | --- |
| Plugin registry | `SpecHarvesterRepositoryPluginRegistry` | `producer_plugin_registry_only` |
| Static evidence envelope | `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` | `producer_plugin_static_evidence_only` |
| Applicability report | `SpecHarvesterRepositoryPluginApplicabilityReport` | `producer_plugin_applicability_only` |
| Adapter manifest | `SpecHarvesterRepositoryPluginAdapterManifest` | `producer_plugin_adapter_manifest_only` |
| Adapter preflight report | `SpecHarvesterRepositoryPluginAdapterPreflightReport` | `producer_plugin_adapter_preflight_only` |
| Adapter output evidence | Future adapter-specific artifacts | `producer_adapter_output_only` |

Static applicability answers whether a plugin role appears relevant from
bounded evidence. Adapter preflight answers whether a declared adapter is safe
and sufficiently evidenced to participate in a future adapter path. Adapter
output remains evidence for review; it is not accepted package truth.

## Adapter Identity

Every adapter manifest should declare stable identity:

| Field | Requirement |
| --- | --- |
| `adapterId` | Stable namespaced id, for example `spec_harvester.adapters.python.public_interface.v0`. |
| `schemaVersion` | Integer manifest schema version. |
| `contractVersion` | Version of the adapter contract implemented by the manifest. |
| `adapterVersion` | Version of the adapter implementation or declarative rule set. |
| `roles[]` | One or more roles such as `parser_profile`, `repository_profile`, `evidence_producer`, `topology_helper`, or `review_surface`. |
| `title` | Human-readable label. |
| `summary` | Short statement of what the adapter can produce. |
| `authority` | Producer-side authority string, never registry authority. |

Adapter ids should be immutable in meaning. Incompatible semantic changes need
a new versioned id instead of silently changing the existing contract.

## Manifest Shape

P40-T2 adds the first
[`SpecHarvesterRepositoryPluginAdapterManifest`](REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md)
fixture at:

```text
tests/fixtures/repository_plugins/adapter-manifest.example.json
```

The fixture shape is:

```json
{
  "apiVersion": "spec-harvester.repository-plugin-adapter/v0",
  "kind": "SpecHarvesterRepositoryPluginAdapterManifest",
  "schemaVersion": 1,
  "authority": "producer_plugin_adapter_manifest_only",
  "adapterId": "spec_harvester.adapters.example.static.v0",
  "contractVersion": "0.1.0",
  "adapterVersion": "0.1.0",
  "roles": ["evidence_producer"],
  "inputEvidence": {
    "requiredKinds": ["static_evidence_envelope"],
    "optionalKinds": ["public_interface_index"]
  },
  "outputs": [
    {
      "kind": "adapter_public_interface_summary",
      "role": "review_evidence",
      "authority": "producer_adapter_output_only"
    }
  ],
  "execution": {
    "mode": "static_only",
    "defaultEnabled": false,
    "requiresOperatorOptIn": true
  }
}
```

The manifest is a declaration. It does not grant permission to execute an
adapter.

## Input Evidence Requirements

Adapters may only consume declared evidence artifacts:

- safe relative paths;
- SHA-256 digests;
- evidence kind labels;
- authority labels;
- source repository revision;
- path policy stating that absolute paths, parent segments, backslashes, and
  network paths are not allowed.

Allowed evidence can include static evidence envelopes, `harvest.json`,
`workspace-inventory.json`, `repository-profile-detection.json`,
`repository-parsing-profile-decision.json`, public-interface indexes, source
manifest metadata, operator labels, and pre-existing analyzer artifacts.

Adapter input evidence must not be gathered through dependency installation,
package manager invocation, build output, imported package execution, network
discovery, or unbounded local tool execution.

## Execution Modes

P40-T4 defines the execution policy in
[`REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md).
Adapter execution is disabled until a future implementation explicitly enables
it under that policy.
The planned execution vocabulary is:

| Mode | Meaning |
| --- | --- |
| `disabled` | No execution. Manifest and preflight only. |
| `static_only` | Reads declared local evidence artifacts only. |
| `trusted_local_tool` | Future bounded local adapter mode requiring explicit operator opt-in, sandbox policy, and path allowlists. |
| `blocked` | Manifest or evidence is unsafe, ambiguous, or unsupported. |

The default mode is `disabled` or `static_only` with `defaultEnabled: false`.
Non-static modes require an explicit future execution policy, an operator
opt-in, and a passing preflight report.

## Sandbox Expectations

Future adapter execution policy must define:

- read path allowlists;
- write path allowlists;
- timeout limits;
- maximum output sizes;
- environment variable policy;
- network policy;
- dependency policy;
- package manager policy;
- process execution policy;
- diagnostics for every denied capability.

The default sandbox decision for undeclared or unsafe capabilities is
`blocked`.

## Adapter Preflight

P40-T3 adds the first
[`SpecHarvesterRepositoryPluginAdapterPreflightReport`](REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md)
fixture. It validates adapter manifests against static evidence before any
future runtime path.

Preflight decisions should include:

- `allowedAdapters[]`;
- `rejectedAdapters[]`;
- `fallbackAdapters[]`;
- `blockedAdapters[]`;
- `diagnostics[]`.

Preflight must block missing required evidence, unsafe paths, unsupported
execution modes, undeclared capabilities, unknown output roles, ambiguous
authority, and any manifest that claims registry authority.

The P40-T3 fixture records the three P40-T2 generic static adapters as
`allowedAdapters[]` and includes explicit rejected, fallback, and blocked
decision examples while keeping `adapterCodeLoaded: false`,
`adapterExecution: not_run`, and `executedAdapterCount: 0`.

## Output Artifact Categories

Adapters may produce proposal-only evidence such as:

- public-interface summaries;
- manifest summaries;
- package topology hints;
- source graph summaries;
- license or provenance summaries;
- documentation/usage summaries;
- review panel data;
- diagnostics.

No adapter output category is accepted package truth. Adapter output may become
candidate-layer evidence only after validation, digest recording, and human
review.

## Autonomous Batch Boundary

P40-T5 connects adapter manifest and preflight output to
`autonomous-candidate-batch` as sidecar producer evidence through
`--repository-plugin-adapter-manifest` and
`--repository-plugin-adapter-preflight`. That integration preserves existing
behavior unless an operator explicitly supplies adapter evidence. The batch
report field is `repositoryPluginAdapterEvidence`.

The batch path must record:

- adapter manifest path and digest;
- preflight path and digest;
- selected, rejected, fallback, and blocked adapter counts;
- diagnostic counts and diagnostic codes;
- `appliedToDrafting: false`;
- `registryAuthority: false`;
- `adapterExecution: not_run`.

## Planned Follow-Ups

- `P40-T2`: add the machine-readable adapter manifest fixture.
- `P40-T3`: add adapter preflight report fixture.
- `P40-T4`: define adapter execution policy.
- `P40-T5`: connect adapter evidence to autonomous candidate batch.
- `P40-T6`: add
  [`REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`](REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md)
  as the static cross-ecosystem adapter contract fixture matrix.
- `P40-T7`: record real local adapter-contract validation
  ([`REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`](REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md)).
