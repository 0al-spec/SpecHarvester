# Trusted Local Adapter Disabled Explicit Real Local Sandbox Runtime Invocation Skeleton

`SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport`
is the P42-T14 machine-readable disabled invocation skeleton for the explicit
real local sandbox path.

The fixture lives at:

```text
tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runtime-invocation.example.json
```

## Boundary

The disabled invocation skeleton follows the P42-T13 approval binding:

```text
explicit real local sandbox operator approval binding
  -> disabled explicit real local sandbox runtime invocation skeleton
  -> future real runtime implementation only after review
```

It validates the bounded approval scope. It is not execution permission, not
registry authority, not approval consumption by a real runtime, and not adapter
output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.disabled-explicit-real-local-trusted-adapter-sandbox-runtime-invocation/v0",
  "kind": "SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport",
  "schemaVersion": 1,
  "authority": "producer_disabled_explicit_real_local_trusted_adapter_sandbox_runtime_invocation_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
invocationIsExecutionPermission: false
invocationIsRegistryAuthority: false
invocationConsumesApproval: false
```

## Input Approval Binding

The skeleton references the P42-T13 operator approval binding:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-operator-approval-binding.example.json
sha256:c1d60ef17d878ca0a6119d28d51a61898828f0d34f77460ba16b912d76386b95
```

The approval binding validation requires:

```text
approvalBindingDigestAgreement: true
approvalStatusAccepted: true
bindingStatusAccepted: true
bindingModeAccepted: true
approvalScopeAccepted: true
approvalReusable: false
approvalConsumedByRuntime: false
approvalBindingIsExecutionPermission: false
approvalBindingIsRegistryAuthority: false
approvalBindingRuntimeInvoked: false
approvalBindingRuntimeImplemented: false
approvalBindingAdapterOutputAccepted: false
```

## Validated Approval Scope

The skeleton validates:

- adapter package identity;
- target repository revision;
- input artifact digests;
- output directory;
- runtime budgets;
- network policy;
- dependency policy;
- audit requirements.

The disabled invocation state remains:

```text
runtimeInvocationAllowed: false
operatorApprovalConsumed: false
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
runtimeInvoked: false
runtimeImplemented: false
networkAccess: none
registryAuthority: false
adapterOutputAccepted: false
```

## Accepted Checks

The skeleton accepts only shapes that preserve:

- P42-T13 approval binding artifact identity and SHA-256 digest;
- approval status `approval_bound_review_only`;
- binding status `approval_bound_runtime_still_blocked`;
- bounded approval scope;
- adapter package identity validation;
- target repository revision validation;
- input artifact digest validation;
- output directory validation;
- runtime budget validation;
- network policy validation;
- dependency policy validation;
- audit requirement validation;
- approval binding is not execution permission;
- approval binding has no registry authority;
- approval is not consumed by a runtime;
- no runtime side effects.

## Rejected And Blocked Shapes

The skeleton rejects missing approval binding input, approval binding digest
mismatch, non-accepted binding status, unscoped approval, reusable approval,
missing adapter identity, missing target revision, missing input digest binding,
missing output directory binding, invocation execution permission, invocation
registry authority, adapter code loading, adapter import, adapter process
spawning, dependency installation, package manager invocation, network access,
runtime invocation, and adapter output as registry truth.

The skeleton blocks any drift toward:

- adapter code loading;
- adapter import;
- adapter process spawning;
- real runtime invocation;
- approval consumption;
- dependency installation;
- package manager invocation;
- network access;
- harvested-code execution;
- AI execution;
- package acceptance;
- relation acceptance;
- baseline seeding;
- `preview_only` removal;
- adapter output truth.

## Execution Boundary

The disabled invocation skeleton preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
invocationIsExecutionPermission: false
invocationIsRegistryAuthority: false
approvalConsumedByRuntime: false
registryAuthority: false
adapterOutputAccepted: false
```

It does not load third-party adapter code, does not import adapter code, does
not execute real adapters, does not run adapter processes, does not install
dependencies, does not invoke package managers, does not execute harvested
repository code, does not run AI, does not use network access, does not accept
packages or relations, does not seed baselines, does not publish registry
metadata, does not remove `preview_only`, does not treat adapter output as
registry truth, and does not treat the disabled invocation skeleton as
execution permission.

## Relationship To Phase 42

- P42-T13 defines
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md).
- P42-T14 adds this disabled runtime invocation skeleton.
- P42-T15 adds
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_EVIDENCE_HANDOFF.md)
  before any real runtime implementation review can consume these artifacts.
