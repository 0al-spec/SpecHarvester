# Static Repository Plugin Applicability Evaluator

Status: Phase 39 plan.

P39-T1 defines a deterministic static evaluator that can derive
`SpecHarvesterRepositoryPluginApplicabilityReport` from collected producer
evidence. It builds on the Phase 38 registry, applicability fixtures,
autonomous batch sidecar path, cross-ecosystem examples, and real FastMCP run.

The evaluator is not a plugin runtime. It does not load third-party plugin
code, execute plugins, run package managers, install dependencies, execute
harvested code, invoke AI, or use network discovery.

```text
plugin registry
  + static evidence envelope
  -> deterministic applicability evaluation
  -> SpecHarvesterRepositoryPluginApplicabilityReport
  -> optional autonomous batch sidecar evidence
```

## Inputs

Allowed static inputs include:

- `SpecHarvesterRepositoryPluginRegistry`;
- source manifest metadata;
- `harvest.json`;
- `workspace-inventory.json`;
- `repository-profile-detection.json`;
- public-interface indexes;
- optional parser profile decisions;
- operator labels or explicit source-manifest declarations.

P39-T2 will define the machine-readable static evidence envelope that records
repository identity, evidence paths, digests, available `evidenceKinds[]`,
advisory signals, and authority statements.
The P39-T2 fixture is documented in
<doc:RepositoryPluginStaticEvidenceEnvelopeFixture>.

The static evidence envelope uses source manifest metadata, `harvest.json`,
`workspace-inventory.json`, `repository-profile-detection.json`,
public-interface indexes, and operator labels as bounded producer-side
evidence. It is not registry truth and does not prove package acceptance.

## Decision Model

For each declared plugin in the registry, the evaluator should emit exactly one
decision: `selected`, `rejected`, `fallback`, or `blocked`.

The output report remains
`SpecHarvesterRepositoryPluginApplicabilityReport` and records
`selectedPlugins[]`, `rejectedPlugins[]`, `fallbackPlugins[]`,
`blockedPlugins[]`, and `diagnostics[]`.

Missing required input evidence must never silently select a plugin. Missing or
unsafe inputs produce `blocked`, `fallback`, or `rejected` decisions with
diagnostics.

Stable diagnostic codes include `plugin_selected`,
`plugin_rejected_low_confidence`, `plugin_fallback`, and
`plugin_blocked_required_evidence_missing`.

## Precedence

Autonomous batch should use:

1. explicit operator-supplied `--repository-plugin-applicability` sidecar;
2. future opt-in static evaluator output;
3. documented generic fallback behavior.

The explicit sidecar path from P38-T4 remains valid and takes precedence over
auto-generated applicability evidence.

Sidecar metadata must keep `appliedToDrafting: false` and
`registryAuthority: false` until a later task explicitly changes how drafting
consumes evaluator output.

## Follow-Up Tasks

- `P39-T2`: define the static plugin evidence envelope fixture.
- `P39-T3`: implement the deterministic evaluator helper.
- `P39-T4`: expose the evaluator through
  `repository-plugin-applicability-detect`.
- `P39-T5`: integrate evaluator output into `autonomous-candidate-batch` as an
  opt-in auto sidecar path.
- `P39-T6`: run real multi-repository validation over existing local checkouts.

## Boundary

The static evaluator must not load third-party plugin code, execute plugins,
run plugin code, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, run AI, change parser profile
behavior, change repository profile scoring, accept packages, accept
relations, publish registry metadata, remove `preview_only`, or treat plugin
decisions as registry truth.
