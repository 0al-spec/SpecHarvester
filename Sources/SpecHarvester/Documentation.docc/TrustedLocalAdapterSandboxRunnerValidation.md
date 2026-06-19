# Trusted Local Adapter Sandbox Runner Validation

`SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport` is the P42-T4
no-execution validation report emitted by the disabled trusted local adapter
sandbox runner validation command.

The validation is available through:

```bash
PYTHONPATH=src python -m spec_harvester trusted-local-adapter-sandbox-runner-validation \
  --contract tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json \
  --preflight tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-preflight-report.example.json \
  --output /tmp/trusted-local-adapter-sandbox-runner-validation-report.json
```

## Boundary

The validation is disabled by default and has no execution mode. It validates
`SpecHarvesterTrustedLocalAdapterSandboxContract` and
`SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`, verifies the sandbox
contract digest recorded by the preflight report, and emits a deterministic
no-execution validation report.

It does not load third-party adapter code, does not execute adapters, does not
run adapter processes, does not install dependencies, does not invoke package
managers, does not use network access, and does not run AI.

```text
sandbox contract -> sandbox preflight -> disabled sandbox runner validation -> no-execution report
```

Passing sandbox preflight is not execution permission. Emitting the sandbox
runner validation report is also not execution permission, not operator
approval, not registry acceptance, and not adapter output truth.
It is producer-side review evidence only.

## Identity

The validation report uses:

```json
{
  "apiVersion": "spec-harvester.trusted-local-adapter-sandbox-runner-validation/v0",
  "kind": "SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport",
  "schemaVersion": 1,
  "authority": "producer_trusted_local_adapter_sandbox_runner_validation_only"
}
```

The report references:

- `SpecHarvesterTrustedLocalAdapterSandboxContract`;
- `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`.

Both references are SHA-256 digest-backed. The command rejects sandbox contract
identity failure, sandbox preflight identity failure, non-passing preflight
status, mismatched sandbox contract digest, and preflight references that do
not point at the supplied contract artifact.

## Runner State

The report records:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeImplemented: false
sandboxRunnerImplemented: false
sandboxContractIsExecutionPermission: false
sandboxPreflightIsExecutionPermission: false
runnerValidationIsExecutionPermission: false
operatorApprovalProvided: false
appliedToDrafting: false
registryAuthority: false
```

The runner validation also records:

- `dependencyInstallation: not_allowed`;
- `packageManagers: not_invoked`;
- `harvestedCodeExecution: not_allowed`;
- `aiExecution: not_run`;
- `networkAccess: none`.

## Validation Checks

The report accepts only the disabled no-execution path:

- sandbox contract identity valid;
- sandbox contract boundary remains no-execution;
- sandbox preflight identity valid;
- sandbox preflight status is passed but review-only;
- sandbox preflight contract digest matches the supplied contract artifact
  bytes;
- sandbox runner validation disabled no-execution boundary preserved;
- non-authority boundary preserved.

Any mismatch is an error. The CLI prints `status: error`, returns exit code `2`,
and does not write a pass-like report.

## Non-Authority Statements

The sandbox runner validation report states that it:

- is not execution permission;
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
- does not treat sandbox contract as registry truth;
- does not treat sandbox preflight as registry truth.

## Relationship to Other Phase 42 Artifacts

- P42-T1 defines <doc:TrustedLocalAdapterRuntimeSandboxPlan>.
- P42-T2 defines <doc:TrustedLocalAdapterSandboxContractFixture>.
- P42-T3 defines <doc:TrustedLocalAdapterSandboxPreflightReportFixture>.
- P42-T4 adds this disabled no-execution sandbox runner validation.
- P42-T5 should add an explicitly approved synthetic adapter run fixture only
  after the disabled validation boundary is stable.
