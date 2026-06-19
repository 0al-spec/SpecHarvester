# Static Repository Plugin Applicability Evaluator

Status: Phase 39 helper and CLI implemented; batch integration planned.

Phase 38 proved the repository plugin applicability contract with fixtures,
autonomous batch sidecar recording, cross-ecosystem examples, and one real
FastMCP run. P39-T1 defines the next layer: a deterministic static evaluator
that can derive `SpecHarvesterRepositoryPluginApplicabilityReport` from
collected producer evidence.

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

## Goal

The evaluator should answer:

```text
Which declared plugin roles are applicable to this repository evidence?
```

It should answer that question from declared plugin metadata and bounded
static artifacts, not from hidden ecosystem heuristics or executable adapter
code.

P39-T3 implements the deterministic helper as
`spec_harvester.repository_plugin_applicability.evaluate_repository_plugin_applicability`.
The helper accepts already-loaded
`SpecHarvesterRepositoryPluginRegistry` and
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` JSON objects, compares
declared `inputEvidenceKinds[]` with available `evidenceKinds[]`, and returns a
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

## Inputs

Allowed static inputs:

- `SpecHarvesterRepositoryPluginRegistry`;
- source manifest metadata;
- `harvest.json`;
- `workspace-inventory.json`;
- `repository-profile-detection.json`;
- public-interface indexes;
- optional parser profile decisions;
- operator labels or explicit source-manifest declarations.

P39-T2 defines the machine-readable static evidence envelope. The fixture is
documented in
[`REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`](REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md).

The envelope should record:

- repository identity and revision;
- evidence paths and digests;
- available `evidenceKinds[]`;
- advisory signals such as `root_manifest`, `workspace_manifest`,
  `member_manifest`, `public_interface_index_present`, and
  `repository_profile_selected`;
- authority statements for each evidence source.

The envelope remains producer-side evidence. It is not registry truth and does
not prove package acceptance.

## Decision Model

For each declared plugin in the registry, the evaluator should emit exactly
one decision:

| Decision | Meaning |
| --- | --- |
| `selected` | All required input evidence is present, no conflict blocks the plugin, and confidence is sufficient. |
| `rejected` | Evidence exists but the plugin does not fit this repository shape. |
| `fallback` | Evidence is incomplete or ambiguous, and the declared fallback behavior should be used. |
| `blocked` | Required evidence is missing or unsafe; the plugin must not be selected. |

The output report remains:

```json
{
  "apiVersion": "spec-harvester.repository-plugin-applicability/v0",
  "kind": "SpecHarvesterRepositoryPluginApplicabilityReport",
  "authority": "producer_plugin_applicability_only",
  "selectedPlugins": [],
  "rejectedPlugins": [],
  "fallbackPlugins": [],
  "blockedPlugins": [],
  "diagnostics": []
}
```

The future report should preserve the existing sidecar boundary:

```json
{
  "appliedToDrafting": false,
  "registryAuthority": false
}
```

Decision arrays are named `selectedPlugins[]`, `rejectedPlugins[]`,
`fallbackPlugins[]`, and `blockedPlugins[]`.
Sidecar summaries should continue to say `appliedToDrafting: false` and
`registryAuthority: false`.

When `autonomous-candidate-batch` receives an explicit
`--repository-plugin-applicability` report, that operator-supplied report wins
over auto-detected evaluator output.

## Selection Rules

Initial deterministic rules:

1. Read only declared plugin metadata from the registry.
2. Build the evidence-kind set from static collected artifacts.
3. For every plugin, compare `inputEvidenceKinds[]` with available
   `evidenceKinds[]`.
4. If required input evidence is missing, emit `blocked` or `fallback`; do not
   select the plugin.
5. If evidence contradicts the plugin role, emit `rejected`.
6. If all required evidence is present and no conflict applies, emit
   `selected`.
7. Emit diagnostics for every non-selected plugin and for every selected
   plugin whose confidence depends on advisory evidence.

Missing input evidence must never silently select a plugin.

P39-T3 implements this first deterministic rule set:

- if all declared `inputEvidenceKinds[]` are available, emit `selected`;
- if required input evidence is missing and `fallbackBehavior.decision` is
  `fallback`, emit `fallback`;
- if required input evidence is missing and fallback behavior is `skip`, emit
  `blocked`;
- if a plugin conflicts with a previously selected plugin, emit `rejected`;
- preserve only safe relative evidence paths and SHA-256 digest-backed
  references from the static evidence envelope.

## Precedence

Autonomous batch should use this precedence after P39-T5:

1. Explicit operator-supplied `--repository-plugin-applicability` sidecar.
2. Future opt-in static evaluator CLI output.
3. Documented generic fallback behavior.

The explicit sidecar path from P38-T4 remains valid and takes precedence over
auto-generated applicability evidence. That preserves operator control and
keeps generated evidence reviewable.

## Diagnostics

The evaluator should reuse stable diagnostic code families:

- `plugin_selected`;
- `plugin_rejected_low_confidence`;
- `plugin_fallback`;
- `plugin_blocked_required_evidence_missing`;
- `plugin_blocked_conflicting_evidence`;
- `plugin_registry_contract_unsupported`.

Diagnostics should include:

- plugin id;
- severity;
- reason codes;
- evidence paths;
- human-readable review message.

## Follow-Up Tasks

- `P39-T2`: define the static plugin evidence envelope fixture.
- `P39-T3`: implement the deterministic evaluator helper.
- `P39-T4`: expose the evaluator through
  `repository-plugin-applicability-detect`.
- `P39-T5`: integrate evaluator output into `autonomous-candidate-batch` as an
  opt-in auto sidecar path.
- `P39-T6`: run real multi-repository validation over existing local checkouts.

## Boundary

The static evaluator must not:

- load third-party plugin code;
- execute plugins;
- run plugin code;
- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- read repository source files;
- auto-attach generated reports to autonomous batch output;
- run AI;
- change parser profile behavior;
- change repository profile scoring;
- accept packages;
- accept relations;
- publish registry metadata;
- remove `preview_only`;
- treat plugin decisions as registry truth.
