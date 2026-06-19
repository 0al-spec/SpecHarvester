# Trusted Local Adapter Explicit Real Local Sandbox Run Request Preflight Fixture

`SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`
is the P42-T9 machine-readable preflight fixture for the P42-T8 explicit real
local sandbox run request.

The fixture lives at:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json
```

## Boundary

The request preflight fixture follows the P42-T8 request fixture:

```text
synthetic sandbox run verifier
  -> real local sandbox run readiness gate
  -> explicit real local sandbox run request fixture
  -> explicit real local sandbox run request preflight fixture
  -> future runtime only after review
```

It validates request shape and safety requirements. It is review evidence only:
passing request preflight is not execution permission, not operator approval,
not registry authority, not package or relation acceptance, and not adapter
output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.explicit-real-local-trusted-adapter-sandbox-run-request-preflight/v0",
  "kind": "SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport",
  "schemaVersion": 1,
  "authority": "producer_explicit_real_local_trusted_adapter_sandbox_run_request_preflight_only"
}
```

The contract keeps:

```text
defaultExecution: disabled
preflightPassIsExecutionPermission: false
preflightPassIsOperatorApproval: false
preflightPassIsRegistryAuthority: false
```

## Request Reference

The preflight report references the P42-T8 request fixture:

```text
tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request.example.json
sha256:a48dae0107ced92e8266ca788ff49e15246651503fd49a550e983aa9f9f33cd3
```

The request digest is verified by the fixture. The validated request remains:

```text
requestIsExecutionPermission: false
requestIsOperatorApproval: false
requestIsRegistryAuthority: false
adapterExecution: not_run
readyForExecution: false
```

## Accepted Checks

The preflight fixture accepts only request shapes that preserve:

- request identity and digest;
- P42-T6 `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport`
  requirements;
- P42-T7 `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport`
  requirements;
- scoped operator approval binding;
- no request self-approval;
- digest-pinned adapter package identity;
- pinned target repository identity and revision;
- sandbox policy identity;
- runtime policy declared but not invoked;
- POSIX relative filesystem/output policy;
- replayable audit policy;
- rollback/review boundary;
- review-only execution boundary;
- non-authority statements.

## Rejected And Blocked Shapes

The fixture rejects unsafe parent paths, absolute paths, backslash paths,
network paths, missing request digests, digest mismatches, missing P42-T6/P42-T7
evidence requirements, wrong verifier/readiness status requirements, missing
review-time digests, reusable approval, request self-approval, mutable adapter
references, network access, dependency installation, package manager
invocation, missing output digest requirements, adapter output as registry
truth, and missing audit requirements.

The fixture blocks any drift toward:

- preflight pass as execution permission;
- request as execution permission;
- preflight-provided operator approval;
- adapter code loading;
- adapter process spawning;
- harvested-code execution;
- AI execution;
- registry authority;
- adapter output acceptance.

## Execution Boundary

The preflight fixture preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
runtimeImplemented: false
requestIsExecutionPermission: false
preflightPassIsExecutionPermission: false
preflightPassIsOperatorApproval: false
registryAuthority: false
adapterOutputAccepted: false
```

It does not load third-party adapter code, does not run adapter processes, does
not spawn real adapter processes, does not install dependencies, does not
invoke package managers, does not execute harvested repository code, does not
run AI, does not use network access, does not accept packages or relations,
does not seed baselines, does not publish registry metadata, does not remove
`preview_only`, does not treat adapter output as registry truth, and does not
treat preflight as execution permission.

## Relationship To Phase 42

- P42-T6 defines
  <doc:TrustedLocalAdapterSyntheticSandboxRunVerifier>.
- P42-T7 defines
  <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness>.
- P42-T8 defines
  <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture>.
- P42-T9 adds this request preflight fixture.
