# Trusted Local Adapter Explicit Real Local Sandbox Runner Evidence Handoff

`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff` is
the P42-T11 machine-readable evidence handoff for the explicit real local
sandbox path.

The fixture lives at:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff.example.json
```

## Boundary

The evidence handoff packages the P42-T8 request, P42-T9 preflight, and P42-T10
disabled runner skeleton:

```text
explicit real local sandbox run request fixture
  -> explicit real local sandbox run request preflight fixture
  -> disabled explicit real local sandbox runner skeleton
  -> explicit real local sandbox runner evidence handoff
  -> future runtime only after review
```

It carries review evidence only. It is not execution permission, not operator
approval, not registry authority, not package or relation acceptance, and not
adapter output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.explicit-real-local-trusted-adapter-sandbox-runner-evidence-handoff/v0",
  "kind": "SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff",
  "schemaVersion": 1,
  "authority": "producer_explicit_real_local_trusted_adapter_sandbox_runner_evidence_handoff_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
handoffIsExecutionPermission: false
handoffIsOperatorApproval: false
handoffIsRegistryAuthority: false
```

## Artifacts

The handoff references the P42-T8 request fixture:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request.example.json
sha256:a48dae0107ced92e8266ca788ff49e15246651503fd49a550e983aa9f9f33cd3
```

It references the P42-T9 preflight fixture:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json
sha256:402145bb2e068de9bffa698b682014c6688829d1edb8debb7ac08949639f4e1c
```

It references the P42-T10 disabled runner skeleton fixture:

```text
tests/fixtures/repository_plugins/disabled-explicit-real-local-trusted-adapter-sandbox-runner.example.json
sha256:f88f68f66b833d5f362d2301574dc4b8a4e9de9478cde6d2cffa938e9756e25a
```

The linkage validation requires:

```text
requestDigestAgreement: true
preflightReferencesRequest: true
disabledRunnerReferencesRequest: true
disabledRunnerReferencesPreflight: true
allDigestsVerified: true
preflightResultStatusAccepted: true
preflightDecisionAccepted: true
disabledRunnerStatusAccepted: true
artifactSetIsExecutionPermission: false
artifactSetIsOperatorApproval: false
artifactSetIsRegistryAuthority: false
adapterOutputAccepted: false
```

## Accepted Checks

The handoff accepts only shapes that preserve:

- P42-T8 request artifact identity and SHA-256 digest;
- P42-T9 preflight artifact identity and SHA-256 digest;
- P42-T10 disabled runner skeleton identity and SHA-256 digest;
- request/preflight linkage;
- preflight/disabled-runner linkage;
- review-only artifact set semantics;
- no execution permission from the handoff;
- no operator approval from the handoff;
- no registry authority from the handoff;
- no runtime side effects;
- no adapter output truth;
- explicit non-authority statements.

## Rejected And Blocked Shapes

The handoff rejects missing request, preflight, or disabled-runner artifacts,
digest mismatches, preflight/request digest mismatch, disabled-runner/request
digest mismatch, disabled-runner/preflight digest mismatch, handoff execution
permission, operator approval in the handoff, registry authority, network
access, dependency installation, and adapter output as registry truth.

The handoff blocks any drift toward:

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
- `preview_only` removal.

## Execution Boundary

The evidence handoff preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
handoffIsExecutionPermission: false
handoffIsOperatorApproval: false
handoffIsRegistryAuthority: false
registryAuthority: false
adapterOutputAccepted: false
```

It does not load third-party adapter code, does not import adapter code, does
not execute real adapters, does not run adapter processes, does not install
dependencies, does not invoke package managers, does not execute harvested
repository code, does not run AI, does not use network access, does not accept
packages or relations, does not seed baselines, does not publish registry
metadata, does not remove `preview_only`, does not treat adapter output as
registry truth, and does not treat the evidence handoff as execution
permission.

## Relationship To Phase 42

- P42-T8 defines
  <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture>.
- P42-T9 defines
  <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestPreflightFixture>.
- P42-T10 defines
  <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRunnerSkeleton>.
- P42-T11 adds this evidence handoff.
- P42-T12 validates this handoff through
  <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewGate>
  before any future runtime implementation task.
