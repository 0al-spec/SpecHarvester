# Repository Plugin Adapter Preflight Report Fixture

Status: Phase 40 fixture contract.

`SpecHarvesterRepositoryPluginAdapterPreflightReport` is the
machine-readable fixture shape for checking adapter manifests against static
evidence before any adapter code can be loaded or run.

Fixture path:

```text
tests/fixtures/repository_plugins/adapter-preflight-report.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.repository-plugin-adapter-preflight/v0",
  "kind": "SpecHarvesterRepositoryPluginAdapterPreflightReport",
  "schemaVersion": 1,
  "authority": "producer_plugin_adapter_preflight_only"
}
```

The preflight authority means:

```text
adapter preflight = producer-side safety and evidence check
adapter preflight != adapter execution permission
adapter preflight != accepted SpecPM package truth
adapter preflight != accepted relation truth
adapter preflight != registry authority
```

## Inputs

The fixture references the P40-T2 adapter manifest and the Phase 39 static
evidence envelope:

```text
tests/fixtures/repository_plugins/adapter-manifest.example.json
tests/fixtures/repository_plugins/static-evidence-envelope.example.json
```

Both references use safe relative paths and SHA-256 digests. The report records
`inputAuthority: static_local_evidence_only`, so missing evidence or unsafe
paths must become diagnostics or blocked decisions instead of hidden runtime
work.

## Decision Categories

The report records four decision arrays:

| Field | Meaning |
| --- | --- |
| `allowedAdapters[]` | Declared adapters whose required static evidence is available and whose manifest stays within static-only policy. |
| `rejectedAdapters[]` | Unsafe or undeclared adapter requests, such as network, process, or adapter code loading requirements. |
| `fallbackAdapters[]` | Lower-fidelity static outcomes when optional evidence is unavailable. |
| `blockedAdapters[]` | Adapter requests that cannot proceed because required evidence or policy is missing. |

The fixture allows the three P40-T2 generic static adapters:

- `spec_harvester.adapters.generic.parser_profile_summary.v0`;
- `spec_harvester.adapters.generic.manifest_summary.v0`;
- `spec_harvester.adapters.generic.package_topology_hint.v0`.

It also includes explicit rejected, fallback, and blocked examples so future
tooling can test all branches without enabling adapter runtime.

## Execution Boundary

The required execution labels are:

```json
{
  "adapterCodeLoaded": false,
  "adapterExecution": "not_run",
  "executedAdapterCount": 0,
  "dependencyInstallation": "not_allowed",
  "packageManagers": "not_invoked",
  "networkAccess": "none",
  "harvestedCodeExecution": "not_allowed",
  "processExecution": "not_allowed",
  "ai": "not_run"
}
```

In prose, the fixture does not load third-party adapter code, execute
adapters, clone or fetch repositories, install dependencies, invoke package
managers, execute harvested code, run AI, accept packages, accept relations,
publish registry metadata, seed baselines, remove `preview_only`, or treat
adapter output as registry truth.

## Required Top-Level Fields

| Field | Purpose |
| --- | --- |
| `manifest` | Digest-pinned link to the adapter manifest fixture. |
| `staticEvidenceEnvelope` | Digest-pinned link to the static evidence envelope fixture. |
| `repository` | Repository identity copied from static evidence. |
| `pathPolicy` | Safe path policy used by the referenced inputs. |
| `evaluationMode` | States that this is fixture-only static preflight. |
| `adapterExecution` | Proves no adapter code was loaded or run. |
| `evidenceAvailability` | Records available and missing evidence kinds. |
| `allowedAdapters[]` | Safe declared adapter decisions. |
| `rejectedAdapters[]` | Unsafe or undeclared adapter decisions. |
| `fallbackAdapters[]` | Lower-fidelity fallback decisions. |
| `blockedAdapters[]` | Missing-required-evidence or unsupported-policy decisions. |
| `diagnostics[]` | Human-readable review diagnostics. |
| `summary` | Counts decision categories and executed adapters. |
| `sidecarBoundary` | Records review-only, non-registry authority status. |
| `nonAuthorityStatements[]` | Records trust and safety boundaries. |

## Relationship to Later Tasks

- `P40-T4` defines
  <doc:RepositoryPluginAdapterExecutionPolicy>.
- `P40-T5` connects adapter manifest and preflight output to
  `autonomous-candidate-batch` as review-only producer evidence.
- `P40-T6` records a cross-ecosystem adapter contract fixture matrix.
- `P40-T7` records real local adapter-contract validation over existing pinned
  checkouts.
