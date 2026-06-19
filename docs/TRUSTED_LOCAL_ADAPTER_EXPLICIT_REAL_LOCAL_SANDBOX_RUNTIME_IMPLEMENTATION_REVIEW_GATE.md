# Trusted Local Adapter Explicit Real Local Sandbox Runtime Implementation Review Gate

`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate`
is the P42-T12 machine-readable review gate for future real local sandbox
runtime implementation.

The fixture lives at:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate.example.json
```

## Boundary

The review gate follows the P42-T11 evidence handoff:

```text
explicit real local sandbox runner evidence handoff
  -> explicit real local sandbox runtime implementation review gate
  -> future operator approval binding
  -> future runtime implementation only after review
```

It records prerequisites only. It is not execution permission, not operator
approval, not registry authority, not package or relation acceptance, and not
adapter output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.explicit-real-local-trusted-adapter-sandbox-runtime-implementation-review-gate/v0",
  "kind": "SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate",
  "schemaVersion": 1,
  "authority": "producer_explicit_real_local_trusted_adapter_sandbox_runtime_implementation_review_gate_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
gateIsExecutionPermission: false
gateIsOperatorApproval: false
gateIsRegistryAuthority: false
```

## Input Handoff

The gate references the P42-T11 evidence handoff fixture:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff.example.json
sha256:ca141fb24d383a4bef98e4bc9e601990bcbd6c0e7d71a1bae9f663b8ed577504
```

The handoff validation requires:

```text
handoffDigestAgreement: true
handoffStatusAccepted: true
handoffModeAccepted: true
handoffReviewOnly: true
handoffIsExecutionPermission: false
handoffIsOperatorApproval: false
handoffIsRegistryAuthority: false
handoffRuntimeInvoked: false
handoffRuntimeImplemented: false
handoffAdapterOutputAccepted: false
```

## Runtime Prerequisites

The gate records these runtime implementation prerequisites, but it does not
satisfy them:

- explicit operator approval;
- adapter package identity;
- process isolation;
- safe input allowlists;
- sealed environment;
- dependency isolation;
- network-deny-by-default policy;
- output digests;
- audit records;
- rollback policy;
- review-only authority.

`providedRuntimePrerequisiteCount` remains `0`. A later task must bind explicit
operator approval before a runtime can execute adapters.

## Accepted Checks

The gate accepts only shapes that preserve:

- P42-T11 handoff artifact identity and SHA-256 digest;
- handoff status `ready_for_review`;
- handoff review-only semantics;
- no execution permission from the handoff;
- no operator approval from the handoff;
- no registry authority from the handoff;
- no adapter output truth from the handoff;
- recorded runtime prerequisites;
- explicit operator approval prerequisite;
- process isolation prerequisite;
- network-deny-by-default prerequisite;
- output digest and audit prerequisites;
- no runtime side effects.

## Rejected And Blocked Shapes

The gate rejects missing handoff input, handoff digest mismatch, non-ready
handoff status, handoff execution permission, handoff operator approval,
handoff registry authority, gate execution permission, gate operator approval,
gate registry authority, adapter code loading, adapter process spawning,
dependency installation, package manager invocation, network access, runtime
invocation, and adapter output as registry truth.

The gate blocks any drift toward:

- adapter code loading;
- adapter import;
- adapter process spawning;
- real runtime invocation;
- missing operator approval binding;
- dependency installation;
- package manager invocation;
- network access;
- harvested-code execution;
- AI execution;
- package acceptance;
- relation acceptance;
- baseline seeding;
- `preview_only` removal.

## Execution Boundary

The review gate preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
gateIsExecutionPermission: false
gateIsOperatorApproval: false
gateIsRegistryAuthority: false
operatorApprovalConsumed: false
operatorApprovalProvided: false
registryAuthority: false
adapterOutputAccepted: false
```

It does not load third-party adapter code, does not import adapter code, does
not execute real adapters, does not run adapter processes, does not install
dependencies, does not invoke package managers, does not execute harvested
repository code, does not run AI, does not use network access, does not accept
packages or relations, does not seed baselines, does not publish registry
metadata, does not remove `preview_only`, does not treat adapter output as
registry truth, and does not treat the runtime review gate as execution
permission.

## Relationship To Phase 42

- P42-T11 defines
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_EVIDENCE_HANDOFF.md).
- P42-T12 adds this runtime implementation review gate.
- P42-T13 adds
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md)
  before any runtime implementation task can execute adapters.
