# Trusted Local Adapter Sandbox Preflight Report Fixture

`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` is the P42-T3
machine-readable preflight fixture for the P42 trusted local adapter sandbox
contract. It validates the P42-T2
`SpecHarvesterTrustedLocalAdapterSandboxContract` shape before any sandbox
runner implementation exists.

The fixture is located at:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-preflight-report.example.json
```

## Boundary

The sandbox preflight report is not execution permission. It is producer-side
review evidence for future sandbox runner validation.

```text
sandbox contract fixture
  -> sandbox preflight report
  -> disabled sandbox runner validation
  -> explicitly approved synthetic adapter run
  -> real local adapter run only after review
```

P42-T3 does not implement a sandbox runner, does not load third-party adapter
code, and does not spawn adapter processes.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.trusted-local-adapter-sandbox-preflight/v0",
  "kind": "SpecHarvesterTrustedLocalAdapterSandboxPreflightReport",
  "schemaVersion": 1,
  "authority": "producer_trusted_local_adapter_sandbox_preflight_only"
}
```

The authority label is intentionally narrow. It means the document can be used
as producer-side review evidence and as input to future disabled sandbox runner
validation. It is not registry authority, package acceptance, relation
acceptance, baseline approval, or adapter execution permission.

## Sandbox Contract Reference

The report references the P42-T2 sandbox contract fixture by safe relative path
and `sha256:` digest:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json
```

The report validates:

- `SpecHarvesterTrustedLocalAdapterSandboxContract` identity;
- sandbox contract authority;
- digest linkage;
- sandbox policy id;
- operator approval requirements;
- no-execution boundary.

## Accepted Checks

The fixture records accepted checks for:

- sandbox contract identity;
- sandbox contract digest linkage;
- adapter package identity and digest pinning;
- sandbox policy identity;
- operator approval requirements;
- bounded process policy;
- safe relative filesystem policy;
- sealed environment policy;
- dependency-deny policy;
- network-deny-by-default policy;
- output verification requirements;
- replayable audit requirements;
- no-execution execution boundary;
- non-authority statements.

## Rejected Checks

The fixture records unsafe shapes that a future preflight implementation must
reject:

- parent paths;
- absolute paths;
- backslash paths;
- network paths;
- missing or mismatched sandbox contract digests;
- mutable adapter refs;
- missing operator approval requirements;
- contracts that self-provide operator approval;
- allowed adapter process execution;
- unbounded process trees;
- inherited environment;
- secrets access;
- dependency installation;
- package manager invocation;
- network access;
- missing output digest requirements;
- missing replayable audit requirements;
- registry authority;
- adapter output treated as registry truth.

## Blocked Runtime Checks

The fixture blocks:

- sandbox runner execution before P42-T4;
- third-party adapter code loading;
- adapter process spawning;
- synthetic approved adapter runs;
- real local adapter runs;
- registry authority requests.

## No-Execution State

The fixture keeps:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeImplemented: false
sandboxRunnerImplemented: false
sandboxPreflightIsExecutionPermission: false
operatorApprovalProvided: false
registryAuthority: false
```

Passing sandbox preflight is review evidence only. It does not grant permission
to run adapters.

## Non-Authority Statements

The fixture records explicit non-authority statements:

- sandbox preflight is not execution permission;
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
- does not treat adapter output as registry truth;
- does not treat sandbox contract as registry truth;
- does not treat sandbox preflight as registry truth.

## Follow-Up

P42-T3 only defines the sandbox preflight report fixture. P42-T4 adds
[`SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`](TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md)
as disabled sandbox runner validation that checks the sandbox contract and
preflight report linkage while still keeping adapter execution disabled. The
next runtime-adjacent step is an explicitly approved synthetic adapter run
fixture, not a real adapter process.
