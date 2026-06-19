# Trusted Local Adapter Synthetic Sandbox Run Fixture

`SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun` is the P42-T5
machine-readable fixture for an explicitly approved synthetic trusted local
adapter sandbox run.

The fixture is located at:

```text
tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json
```

## Boundary

The fixture records approval, output, digest, and audit shape without running a
real adapter process.

```text
sandbox contract
  -> sandbox preflight
  -> disabled sandbox runner validation
  -> explicitly approved synthetic sandbox run fixture
  -> real local adapter run only after review
```

It is producer-side review evidence only. It is not real adapter execution, not
operator approval for arbitrary runs, not registry acceptance, and not adapter
output truth.

## Identity

The fixture uses:

```json
{
  "apiVersion": "spec-harvester.synthetic-trusted-local-adapter-sandbox-run/v0",
  "kind": "SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun",
  "schemaVersion": 1,
  "authority": "producer_synthetic_trusted_local_adapter_sandbox_run_only"
}
```

The authority label is intentionally narrow. It records a synthetic approved
run shape and cannot be used as permission to execute a real adapter process.

## Linked Artifacts

The fixture references these artifacts by safe relative path and `sha256:`
digest:

- `SpecHarvesterTrustedLocalAdapterSandboxContract`;
- `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`;
- `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`.

The runner validation input is:

```text
tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-runner-validation-report.example.json
```

## Operator Approval Binding

The synthetic approval is scoped to:

- one adapter id;
- one adapter digest;
- one repository id and revision;
- one sandbox policy id/version;
- one sandbox runner validation digest;
- one declared output root;
- the declared synthetic output candidate digests.

The fixture records:

```text
approvalProvidedByFixture: true
approvedForRealAdapterExecution: false
approvalIsExecutionPermission: false
approvalIsRegistryAcceptance: false
approvalIsReusableAcrossRepositories: false
```

## Synthetic Outputs

The fixture declares three synthetic output candidates:

- `trusted_local_adapter_output`;
- `trusted_local_adapter_diagnostics`;
- `trusted_local_adapter_audit_record`.

Each output candidate records:

- safe relative path;
- byte size;
- SHA-256 digest;
- producer run id;
- adapter id and digest;
- source input digests;
- diagnostics status;
- `outputIsRegistryTruth: false`.

## Execution Boundary

The fixture keeps:

```text
adapterExecution: synthetic_fixture_only
realAdapterProcessSpawned: false
thirdPartyAdapterCodeLoaded: false
adapterCodeImportAttempted: false
executedAdapterCount: 0
dependencyInstallation: not_allowed
packageManagers: not_invoked
harvestedCodeExecution: not_allowed
aiExecution: not_run
networkAccess: none
registryAuthority: false
```

The synthetic fixture does not load third-party adapter code, spawn real
adapter processes, install dependencies, invoke package managers, use network
access, execute harvested repository code, or run AI because of adapter
execution.

## Non-Authority Statements

The fixture states that it:

- is not real execution permission;
- does not execute real adapters;
- does not run real adapter processes;
- does not accept packages or relations;
- does not seed baselines;
- does not publish registry metadata;
- does not remove `preview_only`;
- does not treat synthetic adapter output as registry truth;
- does not treat sandbox runner validation as execution permission.

## Relationship to Phase 42

- P42-T1 defines the
  [trusted local adapter runtime sandbox plan](TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md).
- P42-T2 defines
  [`SpecHarvesterTrustedLocalAdapterSandboxContract`](TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_FIXTURE.md).
- P42-T3 defines
  [`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`](TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_REPORT_FIXTURE.md).
- P42-T4 defines
  [`SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`](TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md).
- P42-T5 adds this explicitly approved synthetic sandbox run fixture.
