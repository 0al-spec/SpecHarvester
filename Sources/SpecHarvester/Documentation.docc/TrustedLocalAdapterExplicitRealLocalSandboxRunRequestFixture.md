# Trusted Local Adapter Explicit Real Local Sandbox Run Request Fixture

`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` is the P42-T8
machine-readable request fixture for a future real local trusted adapter
sandbox run review.

The fixture lives at:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request.example.json
```

## Boundary

The request fixture follows the P42-T6 verifier and P42-T7 readiness gate:

```text
synthetic sandbox run fixture
  -> synthetic sandbox run verifier
  -> real local sandbox run readiness gate
  -> explicit real local sandbox run request fixture
  -> future preflight/runtime only after review
```

It records a future real-run review request. It is not execution permission,
not operator approval for an actual run, not registry acceptance, not package
or relation acceptance, and not adapter output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.explicit-real-local-trusted-adapter-sandbox-run-request/v0",
  "kind": "SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest",
  "schemaVersion": 1,
  "authority": "producer_explicit_real_local_trusted_adapter_sandbox_run_request_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
requestIsExecutionPermission: false
requestIsOperatorApproval: false
requestIsRegistryAuthority: false
```

## Required Evidence

The fixture requires review-time evidence from:

- `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` with
  `statusRequired: passed`;
- `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport` with
  `statusRequired: ready_for_explicit_real_run_review`;
- review-time paths and SHA-256 digests for both reports.

P42-T8 does not persist those generated reports as truth. It records that a
future reviewer or preflight must provide them and check their digests.

## Approval Scope

The request records the exact scope that later operator approval must bind:

- adapter id and adapter digest;
- target repository id and revision;
- sandbox policy id and version;
- verifier report digest;
- readiness report digest;
- output root;
- audit record path.

The fixture itself has:

```text
approvalProvidedByRequestFixture: false
approvedForRealAdapterExecution: false
approvalIsExecutionPermission: false
approvalIsRegistryAcceptance: false
approvalIsReusableAcrossRepositories: false
```

## Runtime And Output Policy

The fixture declares, but does not invoke:

- process isolation;
- sealed environment;
- dependency isolation;
- network deny-by-default;
- package managers not invoked;
- POSIX relative output paths;
- no parent segments, absolute paths, backslashes, or network paths;
- output digest verification;
- replayable audit record requirements.

Declared outputs remain producer-side evidence under:

```text
artifacts/trusted-local-adapter-sandbox-runs/example-workspace/real-run-request-001
```

## Execution Boundary

The request fixture preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
realRunImplementationPresent: false
requestIsExecutionPermission: false
requestIsOperatorApproval: false
readinessGateIsExecutionPermission: false
registryAuthority: false
adapterOutputAccepted: false
```

It does not load third-party adapter code, does not run adapter processes, does
not spawn real adapter processes, does not install dependencies, does not
invoke package managers, does not execute harvested repository code, does not
run AI, does not use network access, does not accept packages or relations,
does not seed baselines, does not publish registry metadata, does not remove
`preview_only`, and does not treat adapter output as registry truth.

## Relationship To Phase 42

- P42-T6 defines
  <doc:TrustedLocalAdapterSyntheticSandboxRunVerifier>.
- P42-T7 defines
  <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness>.
- P42-T8 adds this request fixture.
- P42-T9 is expected to add request preflight before any runtime can consume the
  request.
