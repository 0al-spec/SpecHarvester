# Trusted Local Adapter Runner Skeleton

`SpecHarvesterTrustedLocalAdapterRunReport` is the P41-T4 no-execution report
emitted by the disabled trusted local adapter runner skeleton.

The skeleton is available through:

```bash
PYTHONPATH=src python -m spec_harvester trusted-local-adapter-runner-skeleton \
  --request tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json \
  --preflight tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json \
  --output /tmp/trusted-local-adapter-run-report.json
```

## Boundary

The skeleton is disabled by default and has no execution mode. It validates
`SpecHarvesterTrustedLocalAdapterRunRequest` and
`SpecHarvesterTrustedLocalAdapterRunPreflightReport`, verifies the request
digest recorded by preflight, and emits a deterministic no-execution report.

It does not load third-party adapter code, does not execute adapters, and does
not run adapter processes.

```text
run request -> preflight report -> disabled runner skeleton -> no-execution report
```

Passing preflight is not execution permission. Emitting the runner report is
also not execution permission, not registry acceptance, and not adapter output
truth.

## Identity

The runner report uses:

```json
{
  "apiVersion": "spec-harvester.trusted-local-adapter-run/v0",
  "kind": "SpecHarvesterTrustedLocalAdapterRunReport",
  "schemaVersion": 1,
  "authority": "producer_trusted_local_adapter_run_report_only"
}
```

The report references:

- `SpecHarvesterTrustedLocalAdapterRunRequest`;
- `SpecHarvesterTrustedLocalAdapterRunPreflightReport`.

Both references are SHA-256 digest-backed. The skeleton rejects request identity
failure, preflight identity failure, non-passing preflight status, mismatched
request digest, and preflight references that do not point at the supplied
request artifact.

## Runner State

The report records:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeImplemented: false
requestIsExecutionPermission: false
preflightPassIsExecutionPermission: false
runnerReportIsExecutionPermission: false
appliedToDrafting: false
registryAuthority: false
```

The runner also records:

- `dependencyInstallation: not_allowed`;
- `packageManagers: not_invoked`;
- `harvestedCodeExecution: not_allowed`;
- `aiExecution: not_run`;
- `networkAccess: none`.

## Validation Checks

The report accepts only the disabled no-execution path:

- request identity valid;
- request boundary remains no-execution;
- preflight identity valid;
- preflight status is passed but review-only;
- preflight request digest matches the supplied request artifact bytes;
- runner disabled no-execution boundary preserved;
- non-authority boundary preserved.

Any mismatch is an error. The CLI prints `status: error`, returns exit code `2`,
and does not write a pass-like report.

## Non-Authority Statements

The runner report states that it:

- is not execution permission;
- does not load third-party adapter code;
- does not execute adapters;
- does not run adapter processes;
- does not clone or fetch repositories;
- does not install dependencies;
- does not invoke package managers;
- does not execute harvested code;
- does not run AI;
- does not accept packages or relations;
- does not seed baselines;
- does not publish registry metadata;
- does not remove `preview_only`;
- does not treat adapter output as registry truth.

## Relationship to Other Phase 41 Artifacts

- P41-T2 defines
  <doc:TrustedLocalAdapterRunRequestFixture>.
- P41-T3 defines
  <doc:TrustedLocalAdapterRunPreflightReportFixture>.
- P41-T4 adds this disabled no-execution runner skeleton.
- P41-T5 will connect trusted local adapter run reports to
  `autonomous-candidate-batch` as review-only producer evidence.
- P41-T6 will run real local readiness validation over pinned checkouts while
  proving no adapter process, package manager, dependency installer, network
  discovery, harvested code, or AI execution occurred.
