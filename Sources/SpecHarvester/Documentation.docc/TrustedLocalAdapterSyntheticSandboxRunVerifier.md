# Trusted Local Adapter Synthetic Sandbox Run Verifier

`SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` is the
P42-T6 machine-readable verifier for
`SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun`.

The verifier command is:

```bash
PYTHONPATH=src python -m spec_harvester.cli \
  synthetic-trusted-local-adapter-sandbox-run-verifier \
  --fixture tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json \
  --output /tmp/synthetic-sandbox-run-verifier-report.json
```

## Boundary

The verifier checks the P42-T5 synthetic fixture and linked files without
running a real adapter process.

```text
sandbox contract
  -> sandbox preflight
  -> disabled sandbox runner validation
  -> explicitly approved synthetic sandbox run fixture
  -> synthetic sandbox run verifier
  -> real local sandbox run readiness gate
  -> real local adapter run only after review
```

It is producer-side review evidence only. It is not execution permission, not
operator approval for arbitrary real runs, not registry acceptance, and not
adapter output truth.

P42-T7 adds <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness> as a
separate readiness gate for explicit future real-run review. Passing this
verifier remains necessary evidence, but it is still not execution permission.

## Identity

The verifier report uses:

```json
{
  "apiVersion": "spec-harvester.synthetic-trusted-local-adapter-sandbox-run-verifier/v0",
  "kind": "SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport",
  "schemaVersion": 1,
  "authority": "producer_synthetic_trusted_local_adapter_sandbox_run_verifier_only"
}
```

## Verified Inputs

The verifier validates:

- fixture API version, kind, schema version, and authority;
- linked artifact digests and safe relative paths;
- `SpecHarvesterTrustedLocalAdapterSandboxContract`;
- `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport`;
- `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`;
- operator approval binding to one adapter, one repository revision, one
  sandbox policy, one runner validation report, and one synthetic output root;
- synthetic output byte sizes/digests for each candidate artifact;
- audit references, including record path, digest, runtime counters, and
  reviewer questions;
- no-real-execution and non-authority statements.

## Execution Boundary

The verifier report preserves:

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
syntheticRunVerificationIsExecutionPermission: false
registryAuthority: false
adapterOutputAccepted: false
```

The verifier does not load third-party adapter code, spawn real adapter
processes, install dependencies, invoke package managers, use network access,
execute harvested repository code, or run AI because of adapter execution.

## Failure Cases

The verifier rejects:

- wrong fixture identity or authority;
- unsafe paths such as absolute paths, parent segments, backslashes, or URI
  paths;
- missing linked artifacts;
- linked artifact digest mismatch;
- synthetic output byte-size or digest mismatch;
- approval binding drift;
- audit record digest/reference drift;
- any fixture drift toward real adapter process execution.

## Non-Authority Statements

The verifier states that it:

- is not execution permission;
- does not execute real adapters;
- does not run real adapter processes;
- does not accept packages or relations;
- does not seed baselines;
- does not publish registry metadata;
- does not remove `preview_only`;
- does not treat adapter output as registry truth;
- does not treat synthetic run verification as execution permission.

## Relationship to Phase 42

- P42-T1 defines <doc:TrustedLocalAdapterRuntimeSandboxPlan>.
- P42-T2 defines <doc:TrustedLocalAdapterSandboxContractFixture>.
- P42-T3 defines <doc:TrustedLocalAdapterSandboxPreflightReportFixture>.
- P42-T4 defines <doc:TrustedLocalAdapterSandboxRunnerValidation>.
- P42-T5 defines <doc:TrustedLocalAdapterSyntheticSandboxRunFixture>.
- P42-T6 adds this verifier report and CLI gate.
- P42-T7 adds <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness>.
- P42-T8 adds
  <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture>.
