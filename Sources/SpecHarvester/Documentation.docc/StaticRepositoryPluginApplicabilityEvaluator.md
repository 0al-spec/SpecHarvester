# Static Repository Plugin Applicability Evaluator

Status: Phase 39 helper and CLI implemented; batch integration planned.

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

P39-T3 implements the deterministic helper as
`spec_harvester.repository_plugin_applicability.evaluate_repository_plugin_applicability`.
The helper accepts already-loaded registry and static evidence envelope JSON
objects, compares declared `inputEvidenceKinds[]` with available
`evidenceKinds[]`, and returns a
`SpecHarvesterRepositoryPluginApplicabilityReport`.

The helper does not read repository source files. It only reads metadata
objects that the caller already provided.

P39-T4 exposes the helper through
`repository-plugin-applicability-detect`:

```bash
PYTHONPATH=src python -m spec_harvester repository-plugin-applicability-detect \
  --registry tests/fixtures/repository_plugins/generic-registry.example.json \
  --static-evidence-envelope tests/fixtures/repository_plugins/static-evidence-envelope.example.json \
  --out /tmp/repository-plugin-applicability-report.json
```

The command writes the full
`SpecHarvesterRepositoryPluginApplicabilityReport` JSON to `--out` and prints
a compact JSON summary with selected, rejected, fallback, blocked, and
diagnostic counts. It reads only the explicit registry and static evidence
envelope files.

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

P39-T3 implements this first deterministic rule set:

- if all declared `inputEvidenceKinds[]` are available, emit `selected`;
- if required input evidence is missing and `fallbackBehavior.decision` is
  `fallback`, emit `fallback`;
- if required input evidence is missing and fallback behavior is `skip`, emit
  `blocked`;
- if a plugin conflicts with a previously selected plugin, emit `rejected`;
- preserve only safe relative evidence paths and SHA-256 digest-backed
  references from the static evidence envelope.

Stable diagnostic codes include `plugin_selected`,
`plugin_rejected_low_confidence`, `plugin_fallback`, and
`plugin_blocked_required_evidence_missing`.

## Precedence

Autonomous batch should use after P39-T5:

1. explicit operator-supplied `--repository-plugin-applicability` sidecar;
2. future opt-in static evaluator CLI output;
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
package managers, execute harvested code, read repository source files,
auto-attach generated reports to autonomous batch output, run AI, change
parser profile behavior, change repository profile scoring, accept packages,
accept relations, publish registry metadata, remove `preview_only`, or treat
plugin decisions as registry truth.
