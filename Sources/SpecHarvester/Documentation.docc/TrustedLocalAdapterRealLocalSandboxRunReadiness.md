# Trusted Local Adapter Real Local Sandbox Run Readiness

`SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport` is the P42-T7
machine-readable readiness gate for future real local trusted adapter sandbox
runs.

The readiness command is:

```bash
PYTHONPATH=src python -m spec_harvester.cli \
  real-local-trusted-adapter-sandbox-run-readiness \
  --verifier-report /tmp/synthetic-sandbox-run-verifier-report.json \
  --output /tmp/real-local-sandbox-run-readiness-report.json
```

## Boundary

The readiness gate consumes a P42-T6
`SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` and checks
whether the evidence is ready for explicit real-run review.

```text
synthetic sandbox run fixture
  -> synthetic sandbox run verifier
  -> real local sandbox run readiness gate
  -> real local adapter run only after explicit review
```

It is producer-side review evidence only. It is not execution permission, not
operator approval for a real run, not registry acceptance, and not adapter
output truth.

## Identity

The readiness report uses:

```json
{
  "apiVersion": "spec-harvester.real-local-trusted-adapter-sandbox-run-readiness/v0",
  "kind": "SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport",
  "schemaVersion": 1,
  "authority": "producer_real_local_trusted_adapter_sandbox_run_readiness_only"
}
```

The report status is:

```text
ready_for_explicit_real_run_review
```

That means the evidence can be reviewed for a future real run. It does not mean
that SpecHarvester can run an adapter process.

## Verified Inputs

The readiness gate validates:

- P42-T6 verifier report API version, kind, schema version, status, and
  authority;
- verifier fixture and linked artifact digest verification summaries;
- verifier synthetic output byte-size/digest verification summaries;
- verifier audit record digest and replay requirements;
- verifier operator approval binding;
- verifier no-real-execution boundary;
- verifier non-authority statements.

## Real-Run Prerequisites

The readiness report declares prerequisites for later explicit review:

- explicit real-run operator approval is required;
- approval must bind adapter id/digest, target repository id/revision, sandbox
  policy id/version, output root, and audit record path;
- approval is not reusable across repositories;
- sandbox runtime requirements are declared but not invoked;
- process isolation, sealed environment, dependency isolation, and network
  deny-by-default policy are required;
- filesystem paths must remain bounded and output digests must be verified;
- replayable audit records, runtime counters, diagnostics, and non-authority
  statements are required.

## Execution Boundary

The readiness report preserves:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeInvoked: false
realRunImplementationPresent: false
readinessGateIsExecutionPermission: false
syntheticRunVerificationIsExecutionPermission: false
registryAuthority: false
adapterOutputAccepted: false
```

The readiness gate does not load third-party adapter code, spawn real adapter
processes, install dependencies, invoke package managers, use network access,
execute harvested repository code, or run AI because of adapter execution.

## Failure Cases

The readiness gate rejects:

- wrong verifier report identity or authority;
- non-passing verifier status;
- verifier output or audit summaries that are not verified;
- verifier operator approval drift toward execution permission;
- verifier drift toward real adapter process execution;
- missing verifier non-authority statements;
- any verifier claim that treats synthetic output as registry truth.

## Non-Authority Statements

The readiness report states that it:

- is not execution permission;
- does not execute real adapters;
- does not run real adapter processes;
- does not accept packages or relations;
- does not seed baselines;
- does not publish registry metadata;
- does not remove `preview_only`;
- does not treat synthetic adapter output as registry truth;
- does not treat readiness as execution permission;
- does not grant registry authority.

## Relationship to Phase 42

- P42-T5 defines <doc:TrustedLocalAdapterSyntheticSandboxRunFixture>.
- P42-T6 defines <doc:TrustedLocalAdapterSyntheticSandboxRunVerifier>.
- P42-T7 adds this readiness gate for explicit future real-run review.
