# Trusted Local Adapter Real Local Readiness Validation

Status: P41-T6 real local validation fixture.

P41-T6 records a practical readiness run for the trusted local adapter path over
existing pinned local checkouts. It proves the request, preflight, disabled
runner report, and batch handoff can be exercised over real repository shapes
without executing adapters.

The durable fixture is:

```text
tests/fixtures/repository_plugins/trusted_local_adapter_real_runs/p41-t6-real-local-trusted-adapter-readiness-validation.example.json
```

## What Was Run

The local run used the P41 request and preflight fixtures, generated a disabled
`SpecHarvesterTrustedLocalAdapterRunReport`, and attached that report to
<doc:AutonomousCandidateBatch> through explicit operator input:

```bash
PYTHONPATH=src python3 -m spec_harvester trusted-local-adapter-runner-skeleton \
  --request tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json \
  --preflight tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json \
  --output /tmp/p41-t6/trusted-local-adapter-run-report.json

PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/p41-t6/inputs \
  --out /tmp/p41-t6/output \
  --skip-ai \
  --trusted-local-adapter-run-report /tmp/p41-t6/trusted-local-adapter-run-report.json
```

The source manifest itself is intentionally not committed because it contains
machine-local checkout paths. The fixture records its SHA-256 digest,
repository revisions, and relative checkout hints instead of absolute paths.

## Corpus

| Repository | Shape | Revision | Batch result |
| --- | --- | --- | --- |
| FastMCP | `nested_package_roots` | `3b8538e2422a1c43fdb69661c610de7985b785f2` | passed, 1 candidate |
| FastAPI | `documentation_heavy_repository` | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | passed, 1 candidate |
| xyflow | `workspace_or_multi_package` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | passed, 4 candidates, 3 relations |
| Gin | `manifest_backed_single_package` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | passed, 1 candidate |

All four checkouts were available and clean during the run. If a future rerun
cannot find a checkout, it should record an explicit skipped entry with the
reason instead of silently reducing corpus coverage.

## Boundary Proved

The run recorded:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
dependencyInstallation: not_allowed
packageManagers: not_invoked
networkAccess: none
harvestedCodeExecution: not_allowed
aiExecution: not_run
appliedToDrafting: false
registryAuthority: false
```

Aggregate counters are all zero for adapter processes, adapter code loading,
dependency installation, package manager invocation, network discovery,
harvested code execution, AI execution, drafting application, and registry
authority.

The batch recorded `trustedLocalAdapterRunEvidence` only because
`--trusted-local-adapter-run-report` was provided explicitly. It did not record
repository plugin applicability evidence, repository plugin adapter evidence,
or any accepted package truth.

## Non-Authority Boundary

This fixture is producer-side readiness evidence only. It does not:

- load third-party adapter code;
- execute adapters;
- run adapter processes;
- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- run AI because of the adapter sidecar;
- change static plugin applicability evaluation;
- change autonomous batch behavior;
- accept packages or relations;
- seed baselines;
- publish registry metadata;
- remove `preview_only`;
- treat adapter output, adapter preflight, AI output, or runner reports as
  registry truth.

## Remaining Runtime Gap

P41-T6 does not implement real adapter execution. A later phase must still
define sandboxed process execution, adapter package distribution, dependency
isolation, output verification, and explicit operator approval before any
adapter can run.

That gap is intentional. The point of P41-T6 is to prove the review evidence
path is practical before introducing a runtime.
