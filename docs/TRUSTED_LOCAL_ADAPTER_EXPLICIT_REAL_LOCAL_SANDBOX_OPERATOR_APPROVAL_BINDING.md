# Trusted Local Adapter Explicit Real Local Sandbox Operator Approval Binding

`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding` is
the P42-T13 machine-readable approval binding fixture for the explicit real
local sandbox path.

The fixture lives at:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-operator-approval-binding.example.json
```

## Boundary

The approval binding follows the P42-T12 runtime implementation review gate:

```text
explicit real local sandbox runtime implementation review gate
  -> explicit real local sandbox operator approval binding
  -> future runtime implementation only after review
```

It records a bounded approval scope. It is not execution permission by itself,
not registry authority, not package or relation acceptance, and not adapter
output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.explicit-real-local-trusted-adapter-sandbox-operator-approval-binding/v0",
  "kind": "SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding",
  "schemaVersion": 1,
  "authority": "producer_explicit_real_local_trusted_adapter_sandbox_operator_approval_binding_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
bindingIsExecutionPermission: false
bindingIsRegistryAuthority: false
bindingIsReusableApproval: false
```

## Input Review Gate

The binding references the P42-T12 runtime implementation review gate:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate.example.json
sha256:0195ad160fddd7039d89e8f18033f5c9aafbcecf799bbfde7dd507c409cc0bf3
```

The review gate validation requires:

```text
reviewGateDigestAgreement: true
reviewGateStatusAccepted: true
reviewGateModeAccepted: true
reviewGateRequiresApprovalBinding: true
reviewGateIsExecutionPermission: false
reviewGateIsOperatorApproval: false
reviewGateIsRegistryAuthority: false
reviewGateRuntimeInvoked: false
reviewGateRuntimeImplemented: false
reviewGateAdapterOutputAccepted: false
```

## Approval Scope

The binding records:

- adapter package identity;
- target repository revision;
- input artifact digests;
- output directory;
- runtime budgets;
- network policy;
- dependency policy;
- audit requirements.

The binding state remains:

```text
approvalRecorded: true
approvalConsumedByRuntime: false
approvalReusable: false
```

## Accepted Checks

The binding accepts only shapes that preserve:

- P42-T12 review gate artifact identity and SHA-256 digest;
- review gate status `blocked_until_future_runtime_review`;
- bounded approval scope;
- adapter package identity binding;
- target repository revision binding;
- input artifact digest binding;
- output directory binding;
- runtime budget binding;
- network policy binding;
- dependency policy binding;
- audit requirement binding;
- approval binding is not execution permission;
- approval binding has no registry authority;
- no runtime side effects.

## Rejected And Blocked Shapes

The binding rejects missing review gate input, review gate digest mismatch,
non-blocked review gate status, unscoped approval, reusable approval, binding
execution permission, binding registry authority, adapter code loading, adapter
process spawning, dependency installation, package manager invocation, network
access, runtime invocation, missing input digest binding, missing output
directory binding, and adapter output as registry truth.

The binding blocks any drift toward:

- adapter code loading;
- adapter import;
- adapter process spawning;
- real runtime invocation;
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

The approval binding preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
bindingIsExecutionPermission: false
bindingIsRegistryAuthority: false
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
registry truth, and does not treat the approval binding as execution
permission.

## Relationship To Phase 42

- P42-T12 defines
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_GATE.md).
- P42-T13 adds this operator approval binding fixture.
