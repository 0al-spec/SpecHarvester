# Trusted Local Adapter Explicit Real Local Sandbox Runtime Invocation Evidence Handoff

`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff`
is the P42-T15 portable review evidence handoff for the explicit real local
sandbox runtime invocation path.

The fixture lives at:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runtime-invocation-evidence-handoff.example.json
```

## Boundary

The handoff packages the two immediate prerequisites for a future real runtime
implementation review:

```text
explicit real local sandbox operator approval binding
  + disabled explicit real local sandbox runtime invocation skeleton
  -> explicit real local sandbox runtime invocation evidence handoff
  -> future real runtime implementation review
```

It is portable review evidence. It is not execution permission, not registry
authority, not approval consumption by a real runtime, and not adapter output
truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.explicit-real-local-trusted-adapter-sandbox-runtime-invocation-evidence-handoff/v0",
  "kind": "SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff",
  "schemaVersion": 1,
  "authority": "producer_explicit_real_local_trusted_adapter_sandbox_runtime_invocation_evidence_handoff_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
handoffIsExecutionPermission: false
handoffIsRegistryAuthority: false
handoffConsumesApproval: false
```

## Linked Artifacts

The handoff references:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-operator-approval-binding.example.json
sha256:c1d60ef17d878ca0a6119d28d51a61898828f0d34f77460ba16b912d76386b95

tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runtime-invocation.example.json
sha256:626e9b8affbf6a668e3da13b32b7b3df8b4976e643eb3ccd9fe33df65fa1237d
```

The artifact validation requires:

```text
approvalBindingDigestAgreement: true
disabledInvocationDigestAgreement: true
approvalBindingStatusAccepted: true
disabledInvocationStatusAccepted: true
approvalBindingIsExecutionPermission: false
disabledInvocationIsExecutionPermission: false
approvalConsumedByRuntime: false
runtimeInvoked: false
runtimeImplemented: false
adapterOutputAccepted: false
```

## Packaged Evidence

The handoff packages:

- approval binding evidence;
- disabled invocation evidence;
- linked artifact digests;
- approval scope summary;
- audit requirements;
- execution boundary;
- non-authority statements.

The handoff state remains:

```text
handoffArtifactCount: 2
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

The handoff accepts only shapes that preserve:

- P42-T13 approval binding artifact identity and SHA-256 digest;
- P42-T14 disabled invocation artifact identity and SHA-256 digest;
- linked digest set;
- approval binding status `approval_bound_runtime_still_blocked`;
- disabled invocation status `blocked_no_execution`;
- approval scope summary;
- audit requirements;
- non-authority statements;
- no execution permission from the handoff;
- no registry authority from the handoff;
- no approval consumption by a runtime;
- no runtime invocation;
- no runtime side effects.

## Rejected And Blocked Shapes

The handoff rejects missing approval binding artifact, missing disabled
invocation artifact, digest mismatch, non-accepted statuses, unscoped approval
summary, handoff execution permission, handoff registry authority, approval
consumption, adapter code loading, adapter import, adapter process spawning,
dependency installation, package manager invocation, network access, runtime
invocation, and adapter output as registry truth.

The handoff blocks any drift toward:

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

## Warning Checks

The warning checks deliberately keep the handoff review-only:

- handoff review-only;
- future runtime implementation required;
- approval is not consumed.

## Execution Boundary

The runtime invocation evidence handoff preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
handoffIsExecutionPermission: false
handoffIsRegistryAuthority: false
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
registry truth, and does not treat the handoff as execution permission.

## Relationship To Phase 42

- P42-T13 defines
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md).
- P42-T14 defines
  [`SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_SKELETON.md).
- P42-T15 adds this runtime invocation evidence handoff.
- P42-T16 adds
  [`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewPacket`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_PACKET.md)
  as the next review packet before any runtime implementation task.
