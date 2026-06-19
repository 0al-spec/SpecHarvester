# Trusted Local Adapter Runtime Readiness

Status: Phase 41 readiness plan.

P41-T1 defines the readiness path from the Phase 40 repository plugin adapter
contract toward a future trusted local adapter runtime. It does not enable
adapter execution. It defines the next artifacts and gates needed before any
adapter process can be launched.

## Why This Exists

Phase 40 established:

- a language- and framework-agnostic adapter contract;
- `SpecHarvesterRepositoryPluginAdapterManifest`;
- `SpecHarvesterRepositoryPluginAdapterPreflightReport`;
- disabled-by-default execution policy;
- autonomous batch adapter evidence handoff;
- a cross-ecosystem adapter fixture matrix;
- real local adapter-contract validation.

That is enough to describe future adapters as review evidence, but it is not
enough to run adapters. A trusted local runtime needs a separate request,
preflight, runner, evidence handoff, and real validation sequence.

## Phase 41 Tasks

| Task | Purpose |
| --- | --- |
| `P41-T1` | Document this readiness plan and add the next-task scaffold. |
| `P41-T2` | Add [`SpecHarvesterTrustedLocalAdapterRunRequest`](TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md) as a machine-readable request fixture. |
| `P41-T3` | Add [`SpecHarvesterTrustedLocalAdapterRunPreflightReport`](TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md) as a machine-readable preflight report fixture that rejects unsafe requests before execution. |
| `P41-T4` | Add [`SpecHarvesterTrustedLocalAdapterRunReport`](TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md) through a disabled-by-default runner skeleton that validates request/preflight linkage and emits a no-execution report. |
| `P41-T5` | Connect trusted local adapter run reports to `autonomous-candidate-batch` as review-only producer evidence through `--trusted-local-adapter-run-report`. |
| `P41-T6` | Validate the readiness path against FastMCP, FastAPI, xyflow, and Gin pinned local checkouts without executing adapters. |

## Required Request Boundary

`SpecHarvesterTrustedLocalAdapterRunRequest` should record:

- explicit operator opt-in;
- adapter manifest and adapter preflight references;
- declared input artifacts with SHA-256 digests;
- safe relative read path allowlists;
- output directory policy;
- maximum output sizes;
- timeout budgets;
- environment variable policy;
- network policy;
- dependency policy;
- package manager policy;
- process execution policy;
- non-authority statements.

The request is not permission to run by itself. It is input to preflight.

P41-T2 records the first request fixture at
`tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json`.
It references the P40-T2 adapter manifest and P40-T3 adapter preflight report
with SHA-256 digests, records explicit operator opt-in, declares safe input
artifacts, and keeps `requestIsExecutionPermission: false`.

## Required Preflight Boundary

Trusted local adapter run preflight should reject or block:

- missing explicit operator opt-in;
- unsafe paths, absolute paths, parent segments, backslashes, and network paths;
- missing or mismatched digests;
- undeclared input artifacts;
- undeclared output paths;
- network access;
- dependency installation;
- package manager invocation;
- harvested code execution;
- AI execution;
- unbounded process execution;
- missing timeout or output-size budgets.

Preflight pass is not registry acceptance. It only says a future local adapter
request is internally consistent enough for an explicitly trusted local run.

P41-T3 records the first trusted local adapter run preflight report fixture at
`tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json`.
It references the P41-T2 run request with a SHA-256 digest, records accepted,
rejected, blocked, and warning checks, and keeps
`preflightPassIsExecutionPermission: false`.

## Runner Boundary

The first runner task stays disabled-by-default. P41-T4 adds
[`trusted-local-adapter-runner-skeleton`](TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md),
which validates a request and preflight report, verifies the request digest
recorded by preflight, and emits a deterministic no-execution report. It does
not load third-party adapter code or launch adapter processes.

The runner report keeps:

```text
adapterExecution: not_run
adapterCodeLoaded: false
adapterCodeImportAttempted: false
adapterProcessSpawned: false
executedAdapterCount: 0
runtimeImplemented: false
runnerReportIsExecutionPermission: false
appliedToDrafting: false
registryAuthority: false
```

The skeleton returns `status: error` for request identity failure, preflight
identity failure, non-passing preflight status, request digest mismatch, or a
preflight request reference that does not point at the supplied request
artifact.

Any runner in this phase must not load third-party adapter code or launch
adapter processes until a later task explicitly introduces that mode.

## Batch Evidence Handoff

P41-T5 adds an explicit `autonomous-candidate-batch
--trusted-local-adapter-run-report` input. The batch accepts only a
`SpecHarvesterTrustedLocalAdapterRunReport` with the disabled no-execution
runner identity, copies it to
`reports/trusted-local-adapter-run-evidence/trusted-local-adapter-run-report.json`,
and records `trustedLocalAdapterRunEvidence`.

The handoff records source and copied SHA-256 digests, report identity,
diagnostic codes, runner status, and the no-execution boundary. It keeps
`adapterExecution: not_run`, `adapterCodeLoaded: false`,
`adapterProcessSpawned: false`, `executedAdapterCount: 0`,
`appliedToDrafting: false`, and `registryAuthority: false`.

This does not enable adapter execution, load adapter code, run adapter
processes, install dependencies, invoke package managers, execute harvested
code, run AI, change static plugin applicability behavior, accept packages,
accept relations, seed baselines, remove `preview_only`, publish registry
metadata, or treat a runner report as adapter output truth.

Any future execution mode must preserve:

- explicit operator opt-in;
- path allowlists;
- no network discovery by default;
- no dependency installation;
- no package manager invocation;
- no harvested repository code execution;
- bounded timeout and output size;
- output digests;
- producer-side review-only authority.

## Non-Authority Boundary

Trusted local adapter artifacts are producer-side review evidence. They do not
accept packages, accept relations, seed baselines, publish registry metadata,
remove `preview_only`, or treat adapter output as registry truth.

The default state remains:

```text
adapterExecution: not_run
adapterCodeLoaded: false
registryAuthority: false
appliedToDrafting: false
```

## Relationship to Phase 40

Phase 40 remains the adapter contract source. Phase 41 is the readiness layer
for future trusted local execution. It should build on
[`REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`](REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md),
[`REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md),
and
[`REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`](REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md)
without weakening their no-runtime and non-authority guarantees.
