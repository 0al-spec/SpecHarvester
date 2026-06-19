# Repository Plugin Static Evidence Envelope Fixture

Status: Phase 39 fixture contract.

`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` is the
machine-readable fixture shape for declaring the bounded static evidence that
a future repository plugin applicability evaluator may read.

Fixture path:

```text
tests/fixtures/repository_plugins/static-evidence-envelope.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.repository-plugin-static-evidence/v0",
  "kind": "SpecHarvesterRepositoryPluginStaticEvidenceEnvelope",
  "schemaVersion": 1,
  "authority": "producer_plugin_static_evidence_only",
  "inputAuthority": "static_local_evidence_only"
}
```

The envelope authority means:

```text
static evidence envelope = producer-side evidence catalog
static evidence envelope != plugin execution
static evidence envelope != evaluator execution
static evidence envelope != accepted package truth
static evidence envelope != registry authority
```

## Relationship to Registry and Applicability

The fixture references the P38
`SpecHarvesterRepositoryPluginRegistry` fixture:

```text
tests/fixtures/repository_plugins/generic-registry.example.json
```

It also declares that the next consumer is a future
`SpecHarvesterRepositoryPluginApplicabilityReport` with
`apiVersion: spec-harvester.repository-plugin-applicability/v0` and
`authority: producer_plugin_applicability_only`.

The shape is:

```text
SpecHarvesterRepositoryPluginRegistry
  + SpecHarvesterRepositoryPluginStaticEvidenceEnvelope
  -> future deterministic evaluator
  -> SpecHarvesterRepositoryPluginApplicabilityReport
```

P39-T2 defines the envelope only. P39-T3 owns evaluator helper logic. P39-T4
owns `repository-plugin-applicability-detect`. P39-T5 owns opt-in
`autonomous-candidate-batch` integration. P39-T6 owns real multi-repository
validation.

## Evidence Kinds

The fixture includes `evidenceKinds[]`: the same bounded evidence kinds
declared by the generic plugin registry:

- `source_manifest`;
- `harvest_snapshot`;
- `workspace_inventory`;
- `public_interface_index`;
- `repository_profile_detection`;
- `repository_parsing_profile_decision`;
- `operator_label`.

These are static local evidence kinds. They do not require network discovery,
package registry queries, dependency installation, package manager execution,
imported package execution, build outputs, or live AI calls.

## Evidence Records

Every `evidence[]` record includes:

- `kind`;
- `path`;
- `digest`;
- `authority`;
- `requiredFor[]`.

Paths must be normalized POSIX-style relative paths. Absolute paths, parent
segments, backslashes, and network paths are not allowed. Digests use
`sha256:<64 hex chars>`.

The example records cover source manifest metadata, `harvest.json`,
`workspace-inventory.json`, `repository-profile-detection.json`,
public-interface indexes, parser profile decisions, and operator labels.

## Advisory Signals

The fixture records advisory signals that a future deterministic evaluator may
use when comparing plugin `inputEvidenceKinds[]` with available evidence:

- `root_manifest`;
- `workspace_manifest`;
- `member_manifest`;
- `public_interface_index_present`;
- `repository_profile_selected`;
- `parser_profile_available`;
- `operator_label_present`.

Advisory signals do not select plugins by themselves. They are reviewable
producer-side evidence.

## Sidecar Boundary

The fixture preserves the current sidecar boundary:

```json
{
  "appliedToDrafting": false,
  "registryAuthority": false,
  "evaluatorExecution": "not_run"
}
```

That means the envelope is not applied to drafting, is not registry authority,
and does not claim the future evaluator has run.

Review summaries should continue to say `appliedToDrafting: false`,
`registryAuthority: false`, and `evaluatorExecution: not_run`.

## Non-Authority Boundary

The static evidence envelope fixture does not load third-party plugin code,
execute plugins, run plugin code, clone or fetch repositories, install
dependencies, execute harvested code, invoke package managers, run AI,
implement evaluator logic, add a CLI, change autonomous batch behavior, accept
packages, accept relations, publish registry metadata, seed baselines, remove
`preview_only`, treat plugin evidence as registry truth, or treat plugin
decisions as registry truth.
