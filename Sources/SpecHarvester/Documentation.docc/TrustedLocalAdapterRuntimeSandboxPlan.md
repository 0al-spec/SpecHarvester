# Trusted Local Adapter Runtime Sandbox Plan

Status: P42-T1 sandbox planning contract.

P42 defines the sandbox boundary that must exist before SpecHarvester can run a
trusted local adapter process. It builds on Phase 41 readiness evidence, but it
does not enable adapter execution.

Current state remains:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterProcessSpawned: false
executedAdapterCount: 0
registryAuthority: false
```

## Why This Exists

Phase 41 proves that SpecHarvester can validate a run request, preflight it,
emit a disabled runner report, copy that report into autonomous batch output,
and validate the path over real pinned checkouts. That is not enough to run
adapter code.

A future trusted local adapter runtime must define the sandbox first. Otherwise
language-specific precision could accidentally become unbounded local
execution, dependency installation, package manager invocation, network
discovery, or harvested code execution.

## Required Sandbox Layers

### Operator Approval

Every real adapter run must require explicit local operator approval. Approval
must be scoped to:

- adapter package identity;
- adapter version, revision, or digest;
- target repository id and checkout revision;
- declared input artifact paths and digests;
- declared output directories;
- runtime budgets;
- network, dependency, and package-manager policy;
- expected output artifact kinds.

Approval is not registry acceptance. It only authorizes one bounded local
producer-side run.

### Adapter Package Identity

The runtime must know exactly which adapter package is being run. A future
machine-readable contract should require:

- adapter id;
- adapter kind and supported repository roles;
- adapter package source;
- pinned revision or content digest;
- signature or digest verification status;
- declared entrypoint;
- declared required evidence;
- declared output artifact kinds;
- non-authority statements.

Mutable adapter labels such as `main` or `latest` are not enough for a trusted
run unless resolved to an immutable revision or digest before approval.

### Process Isolation

Adapter execution must be isolated from the host and from harvested repository
code. The runtime plan requires:

- a bounded process tree;
- timeout and CPU budgets;
- memory budgets;
- no inherited shell session;
- no ambient credentials;
- no uncontrolled child processes;
- deterministic working directory;
- stdout/stderr size limits.

The first implementation may choose a conservative local isolation mechanism,
but the contract must record the chosen mechanism and its limits.

### Filesystem Policy

Adapters must read only declared producer evidence paths. A future run contract
must keep the Phase 41 path policy:

```text
pathFormat: posix_relative
parentSegmentsAllowed: false
absolutePathsAllowed: false
backslashAllowed: false
networkPathsAllowed: false
```

Writable paths must be limited to declared output directories. Outputs must be
replaced per run or written into a fresh run directory.

### Environment Sealing

The default environment must be sealed:

- do not inherit host environment variables;
- deny secrets by default;
- require explicit allowlists for any variable;
- record all allowed variables in the run receipt;
- do not expose GitHub, SSH, cloud, package registry, or model-provider tokens
  by default.

### Dependency Isolation

Dependency installation is denied by default. A future runtime may support
prebuilt adapter environments, but a run must not invoke package managers or
install repository dependencies unless a later policy explicitly permits a
bounded mode.

The safe default remains:

```text
dependencyInstallation: not_allowed
packageManagers: not_invoked
```

### Network Policy

Network access is denied by default:

```text
networkAccess: none
dnsAllowed: false
remoteFetchAllowed: false
```

If a future adapter needs network access, that must be a separate policy task
with a clear reason, target allowlist, audit trail, and operator approval. It
must not be silently enabled by repository or adapter metadata.

### Output Verification

Every output file must have:

- declared output kind;
- declared authority;
- safe relative path;
- byte size;
- SHA-256 digest;
- producer run id;
- adapter id and digest;
- source input digests;
- diagnostics status.

Adapter output is candidate evidence. It is not accepted package truth.

### Audit and Replay

Every real adapter run must emit a replayable audit record that includes:

- request digest;
- preflight digest;
- operator approval digest;
- adapter package identity;
- sandbox policy identity;
- input artifact digests;
- output artifact digests;
- runtime counters;
- diagnostics;
- non-authority statements.

The audit record should let a reviewer verify what was approved, what ran, what
was read, what was written, and why the output remains non-authoritative.

## Runtime Authority

Trusted local adapter runtime output is producer-side review evidence. It does
not:

- accept packages;
- accept relations;
- seed baselines;
- publish registry metadata;
- remove `preview_only`;
- replace SpecPM validation;
- replace maintainer review;
- treat adapter output, runner reports, sandbox plans, or AI output as registry
  truth.

## Machine-Readable Contract Fixture

P42-T2 adds <doc:TrustedLocalAdapterSandboxContractFixture> as the first
machine-readable `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture. It
records the sandbox layers above before any task implements real adapter
process execution.

The implementation sequence should remain:

```text
sandbox contract fixture
  -> sandbox preflight report
  -> disabled sandbox runner validation
  -> one explicitly approved synthetic adapter run
  -> synthetic sandbox run verifier
  -> real local sandbox run readiness gate
  -> explicit real local sandbox run request fixture
  -> real local adapter run only after review
```

P42-T3 adds <doc:TrustedLocalAdapterSandboxPreflightReportFixture> as the
review-only sandbox preflight report fixture. This ordering keeps the future
runtime incremental and auditable.
P42-T4 adds <doc:TrustedLocalAdapterSandboxRunnerValidation> as disabled
no-execution validation over the sandbox contract and preflight report while
preserving `adapterExecution: not_run`, `adapterCodeLoaded: false`,
`adapterProcessSpawned: false`, `executedAdapterCount: 0`, and
`registryAuthority: false`.
P42-T5 adds <doc:TrustedLocalAdapterSyntheticSandboxRunFixture> as an
explicitly approved synthetic run fixture. It records approval binding,
synthetic output candidates, output digests, audit records, and review-only
non-authority statements without running a real adapter process.
P42-T6 adds <doc:TrustedLocalAdapterSyntheticSandboxRunVerifier> as a
deterministic verifier for fixture identity, linked artifact digests, approval
binding, synthetic output byte sizes/digests, audit references, and
no-real-execution boundaries without enabling real adapter execution.
P42-T7 adds <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness> as a
readiness gate for explicit future real-run review prerequisites while still
refusing adapter code loading, process spawning, dependency installation,
package manager invocation, network access, and registry authority.
P42-T8 adds <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture>
as a request-only fixture for future real local sandbox run review. It requires
P42-T6 verifier and P42-T7 readiness evidence, declares scoped approval plus
runtime/output/audit policy, and still keeps `adapterExecution: not_run`,
`runtimeInvoked: false`, `requestIsExecutionPermission: false`, and
`registryAuthority: false`.
