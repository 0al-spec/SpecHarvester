# Trusted Local Adapter Run Request Fixture

`SpecHarvesterTrustedLocalAdapterRunRequest` is the P41-T2
machine-readable request fixture for a future trusted local adapter runtime.
It records what an operator wants to preflight, which adapter contract evidence
the request is tied to, which local files may be read, which output directory
may be written, and which resource and execution policies apply.

The fixture is located at:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json
```

## Boundary

The request is not permission to run by itself. It is input to a future
trusted local adapter run preflight.

```text
run request -> future run preflight -> future disabled runner skeleton
```

The P41-T2 fixture does not implement preflight, does not implement a runner,
does not load third-party adapter code, and does not run adapter processes.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.trusted-local-adapter-run-request/v0",
  "kind": "SpecHarvesterTrustedLocalAdapterRunRequest",
  "schemaVersion": 1,
  "authority": "producer_trusted_local_adapter_run_request_only"
}
```

The authority label is intentionally narrow. It means the document can be used
as producer-side review evidence and as input to future preflight. It is not
registry authority, package acceptance, relation acceptance, or baseline
approval.

The request authority is `producer_local_operator_request_only`; it records
local operator intent for review and preflight, not permission to execute.

## Required Inputs

The request references the Phase 40 adapter artifacts and records declared
input artifacts:

- `SpecHarvesterRepositoryPluginAdapterManifest` from
  `tests/fixtures/repository_plugins/adapter-manifest.example.json`;
- `SpecHarvesterRepositoryPluginAdapterPreflightReport` from
  `tests/fixtures/repository_plugins/adapter-preflight-report.example.json`.

Both references include `sha256:` digests. The request also declares every
static input artifact it wants to read:

- adapter manifest;
- adapter preflight report;
- static evidence envelope;
- repository plugin registry.

Every declared input path is POSIX relative. Parent segments, absolute paths,
backslashes, and network paths are not allowed.

## Operator Opt-In

The request has explicit operator opt-in:

```json
{
  "operatorOptIn": {
    "required": true,
    "provided": true,
    "scope": "trusted_local_adapter_run_preflight_fixture_only"
  }
}
```

This opt-in is scoped to future preflight. It does not load adapter code and
does not launch adapter processes.

## Read and Write Policy

The read allowlist is `declared_artifact_paths_only`. Future tooling should
reject any request that attempts to read undeclared paths or unsafe paths.

The output policy is limited to a declared run directory:

```text
artifacts/trusted-local-adapter-runs/example-workspace
```

Outputs must be declared, bounded by `maxBytes`, and digestable. Undeclared
output paths are outside the request contract.

## Resource and Execution Policy

The fixture records resource budgets:

- `timeoutMs`;
- `adapterStartupTimeoutMs`;
- `maxOutputBytes`;
- `maxOutputFiles`;
- `maxDiagnostics`;
- `maxProcessCount`.

It also denies unsafe execution surfaces:

- `networkAccess: none`;
- `dependencyInstallation: not_allowed`;
- `packageManagers: not_invoked`;
- `adapterProcessExecution: not_allowed_in_request_fixture`;
- `harvestedCodeExecution: not_allowed`;
- `aiExecution: not_run`.

The fixture keeps:

```text
adapterExecution: not_run
adapterCodeLoaded: false
appliedToDrafting: false
registryAuthority: false
requestIsExecutionPermission: false
```

## Non-Authority Statements

The fixture records explicit non-authority statements:

- request is not execution permission;
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

## Follow-Up

P41-T2 only defines the request shape. The next tasks are:

- `P41-T3`: trusted local adapter run preflight report fixture;
- `P41-T4`: disabled-by-default no-execution runner skeleton;
- `P41-T5`: review-only batch evidence handoff;
- `P41-T6`: real local readiness validation.

P41-T3 records
[`SpecHarvesterTrustedLocalAdapterRunPreflightReport`](TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md)
as the first review-only preflight fixture over this request shape. Passing
preflight is not execution permission.
