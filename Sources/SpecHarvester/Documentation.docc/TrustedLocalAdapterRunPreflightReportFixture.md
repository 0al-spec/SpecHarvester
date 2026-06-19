# Trusted Local Adapter Run Preflight Report Fixture

`SpecHarvesterTrustedLocalAdapterRunPreflightReport` is the P41-T3
machine-readable preflight report fixture for
`SpecHarvesterTrustedLocalAdapterRunRequest`.

The fixture is located at:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json
```

## Boundary

Preflight is a review gate before any future runner. Passing preflight is not
execution permission, not registry acceptance, and not adapter output truth.

```text
run request -> preflight report -> disabled no-execution runner skeleton
```

The P41-T3 fixture does not implement a preflight CLI, does not load
third-party adapter code, and does not run adapter processes. P41-T4 consumes
this fixture through <doc:TrustedLocalAdapterRunnerSkeleton> without enabling
real adapter execution.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.trusted-local-adapter-run-preflight/v0",
  "kind": "SpecHarvesterTrustedLocalAdapterRunPreflightReport",
  "schemaVersion": 1,
  "authority": "producer_trusted_local_adapter_run_preflight_only"
}
```

The fixture references the P41-T2 request:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json
```

The request reference is digest-pinned with `sha256:` so review tooling can
detect stale or mismatched preflight evidence.

## Accepted Checks

The report records accepted checks for:

- request identity;
- explicit operator opt-in;
- adapter manifest/preflight references;
- declared input artifacts;
- safe relative path policy;
- read allowlists;
- output policy;
- resource budgets;
- environment policy;
- network policy;
- dependency policy;
- package manager policy;
- process policy;
- execution boundary;
- non-authority statements.

The passing result keeps:

```text
adapterExecution: not_run
adapterCodeLoaded: false
executedAdapterCount: 0
requestIsExecutionPermission: false
preflightPassIsExecutionPermission: false
registryAuthority: false
```

## Rejected Checks

The fixture shows request shapes that must be rejected:

- unsafe parent paths;
- absolute paths;
- backslash paths;
- network paths;
- missing explicit operator opt-in;
- missing digests;
- mismatched digests;
- undeclared input artifacts;
- undeclared output paths;
- network access;
- dependency installation;
- package manager invocation;
- harvested code execution;
- AI execution;
- unbounded process execution;
- unbounded outputs.

## Blocked Checks

The fixture also records blocked cases that require future explicit work:

- adapter execution requested;
- third-party adapter code loading requested;
- registry authority requested.

These are blocked because Phase 41 has not introduced runtime execution.

## Warning Checks

The fixture includes warning checks for review-only semantics.

Warnings document review semantics:

- preflight pass is review evidence only;
- P41-T4 adds a disabled no-execution runner skeleton that can consume this
  report without treating it as execution permission.

## Non-Authority Statements

The report states that it:

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

P41-T3 only defines the preflight report shape. Related and next tasks are:

- `P41-T4`: disabled-by-default no-execution runner skeleton and
  `SpecHarvesterTrustedLocalAdapterRunReport`;
- `P41-T5`: review-only batch evidence handoff;
- `P41-T6`: real local readiness validation.
