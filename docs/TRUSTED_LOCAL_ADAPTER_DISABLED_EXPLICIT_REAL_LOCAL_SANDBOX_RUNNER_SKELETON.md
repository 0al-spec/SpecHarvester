# Trusted Local Adapter Disabled Explicit Real Local Sandbox Runner Skeleton

`SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport` is
the P42-T10 machine-readable disabled runner skeleton for the explicit real
local sandbox path.

The fixture lives at:

```text
tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runner.example.json
```

## Boundary

The disabled runner skeleton follows the P42-T8 request and P42-T9 preflight:

```text
explicit real local sandbox run request fixture
  -> explicit real local sandbox run request preflight fixture
  -> disabled explicit real local sandbox runner skeleton
  -> future runtime only after review
```

It validates request/preflight linkage only. It is review evidence, not
execution permission, not operator approval, not registry authority, not package
or relation acceptance, and not adapter output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.disabled-explicit-real-local-trusted-adapter-sandbox-runner/v0",
  "kind": "SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport",
  "schemaVersion": 1,
  "authority": "producer_disabled_explicit_real_local_trusted_adapter_sandbox_runner_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
runnerIsExecutionPermission: false
runnerIsOperatorApproval: false
runnerIsRegistryAuthority: false
```

## Inputs

The skeleton references the P42-T8 request fixture:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request.example.json
sha256:a48dae0107ced92e8266ca788ff49e15246651503fd49a550e983aa9f9f33cd3
```

It also references the P42-T9 preflight fixture:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json
sha256:402145bb2e068de9bffa698b682014c6688829d1edb8debb7ac08949639f4e1c
```

The linkage validation requires:

```text
requestDigestAgreement: true
preflightReferencesRequest: true
preflightRequestDigest: sha256:a48dae0107ced92e8266ca788ff49e15246651503fd49a550e983aa9f9f33cd3
requestIdentityMatchesPreflightValidatedRequest: true
preflightResultStatusAccepted: true
preflightDecisionAccepted: true
requestExecutionPermissionGranted: false
preflightExecutionPermissionGranted: false
runnerExecutionPermissionGranted: false
operatorApprovalConsumed: false
operatorApprovalProvidedByRunner: false
```

## Accepted Checks

The skeleton accepts only shapes that preserve:

- P42-T8 request identity and SHA-256 digest;
- P42-T9 preflight identity and SHA-256 digest;
- preflight request-digest agreement;
- `preflight_passed_review_only` result semantics;
- request/preflight no-execution boundary;
- no operator approval consumed or provided by the runner;
- adapter execution disabled;
- adapter code loading disabled;
- process spawning disabled;
- runtime side effects disabled;
- registry authority disabled;
- adapter output acceptance disabled.

## Rejected And Blocked Shapes

The skeleton rejects missing request/preflight inputs, request digest mismatch,
preflight digest mismatch, preflight/request digest mismatch, non-passed
preflight status, non-review-only preflight decision, request execution
permission, preflight execution permission, runner execution permission,
operator approval consumption, network access, dependency installation,
package manager invocation, registry authority, and adapter output as registry
truth.

The skeleton blocks any drift toward:

- adapter code loading;
- adapter import;
- adapter process spawning;
- real runtime invocation;
- dependency installation;
- network access;
- harvested-code execution;
- AI execution;
- package acceptance;
- relation acceptance;
- baseline seeding;
- `preview_only` removal;
- adapter output truth.

## Execution Boundary

The disabled runner skeleton preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
requestIsExecutionPermission: false
preflightPassIsExecutionPermission: false
runnerIsExecutionPermission: false
runnerIsOperatorApproval: false
registryAuthority: false
adapterOutputAccepted: false
```

It does not load third-party adapter code, does not import adapter code, does
not run adapter processes, does not spawn real adapter processes, does not
install dependencies, does not invoke package managers, does not execute
harvested repository code, does not run AI, does not use network access, does
not accept packages or relations, does not seed baselines, does not publish
registry metadata, does not remove `preview_only`, does not treat adapter output
as registry truth, and does not treat the disabled runner skeleton as execution
permission.

## Relationship To Phase 42

- P42-T8 defines
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_FIXTURE.md).
- P42-T9 defines
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_PREFLIGHT_FIXTURE.md).
- P42-T10 adds this disabled runner skeleton.
