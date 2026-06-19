# Trusted Local Adapter Sandbox Contract Fixture

`SpecHarvesterTrustedLocalAdapterSandboxContract` is the P42-T2
machine-readable fixture for the trusted local adapter runtime sandbox
boundary. It turns the P42-T1 sandbox plan into reviewable data before any real
adapter process can run.

The fixture is located at:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json
```

## Boundary

The sandbox contract is not execution permission. It is producer-side review
evidence for a future sandbox preflight.

```text
sandbox contract fixture
  -> sandbox preflight report
  -> disabled sandbox runner validation
  -> explicitly approved synthetic adapter run
  -> real local adapter run only after review
```

P42-T2 does not implement preflight, does not implement a sandbox runner, does
not load third-party adapter code, and does not spawn adapter processes.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.trusted-local-adapter-sandbox-contract/v0",
  "kind": "SpecHarvesterTrustedLocalAdapterSandboxContract",
  "schemaVersion": 1,
  "authority": "producer_trusted_local_adapter_sandbox_contract_only"
}
```

The authority label is intentionally narrow. It means the document can be used
as producer-side review evidence and as input to a future sandbox preflight. It
is not registry authority, package acceptance, relation acceptance, baseline
approval, or adapter execution permission.

## Input Contract References

The fixture references the Phase 41 trusted local adapter artifacts by safe
relative path and `sha256:` digest:

- `SpecHarvesterTrustedLocalAdapterRunRequest`;
- `SpecHarvesterTrustedLocalAdapterRunPreflightReport`;
- `SpecHarvesterTrustedLocalAdapterRealLocalReadinessValidation`.

It also declares the adapter manifest, adapter preflight report, static
evidence envelope, and plugin registry as input artifacts. Every input path is
POSIX relative. Parent segments, absolute paths, backslashes, and network paths
are not allowed.

## Adapter Package Identity

The fixture records the adapter package identity required before future runtime:

- adapter id;
- adapter kind;
- supported repository roles;
- adapter package source path and digest;
- pinned revision or digest requirement;
- signature or digest verification requirement;
- declared entrypoint;
- declared required evidence;
- declared output artifact kinds.

Mutable labels such as `main` or `latest` are not enough for a trusted run
unless a future preflight resolves them to an immutable revision or digest.

## Sandbox Policy Identity

The sandbox policy identity records:

- policy id;
- policy version;
- source task;
- source document;
- policy authority;
- immutable policy requirement;
- requirement that a real runtime records the policy digest.

The policy identity lets future run evidence prove which sandbox contract was
approved and applied.

## Operator Approval Requirements

The `operatorApprovalRequirements` section records the operator approval
requirements that a future sandbox preflight must validate before runtime.

The fixture requires explicit local operator approval before runtime:

```json
{
  "requiredBeforeRuntime": true,
  "providedByFixture": false,
  "approvalScope": "single_adapter_single_repository_single_run"
}
```

The fixture does not provide approval itself. A future approval must bind the
adapter id and digest, sandbox policy id/version, target repository revision,
input digests, output directories, process budgets, network policy, dependency
policy, and expected output kinds.

Approval is not registry acceptance and is not reusable across repositories.

## Runtime Policies

The fixture records the sandbox defaults:

```text
adapterProcessExecution: not_allowed_in_contract_fixture
pathFormat: posix_relative
inheritEnvironment: false
secretsAccess: not_allowed
dependencyInstallation: not_allowed
packageManagers: not_invoked
networkAccess: none
dnsAllowed: false
remoteFetchAllowed: false
```

The process policy requires a bounded process tree, deterministic working
directory, no inherited shell session, no ambient credentials, bounded stdout
and stderr, timeout and CPU budgets, and memory budgets.

## Output Verification

Every future adapter output must be verifiable:

- declared output kind;
- safe relative path;
- byte size;
- SHA-256 digest;
- producer run id;
- adapter id and digest;
- source input digests;
- diagnostics status.

Adapter output remains candidate evidence. It is not accepted package truth.

## Audit Requirements

The fixture requires a replayable audit record with:

- request digest;
- preflight digest;
- operator approval digest;
- adapter package identity;
- sandbox policy identity;
- input artifact digests;
- output artifact digests;
- runtime counters;
- diagnostics;
- non-authority statements.

The audit record should let a reviewer answer what was approved, what ran, what
was read, what was written, and why the output remains non-authoritative.

## No-Execution State

The fixture keeps:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeImplemented: false
sandboxPreflightImplemented: false
registryAuthority: false
```

## Non-Authority Statements

The fixture records explicit non-authority statements:

- sandbox contract is not execution permission;
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
- does not treat sandbox contract as registry truth.

## Follow-Up

P42-T2 only defines the sandbox contract fixture. The next task is `P42-T3`,
the trusted local adapter sandbox preflight report fixture. That task should
validate this contract shape before any sandbox runner implementation exists.
