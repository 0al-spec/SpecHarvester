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
| `P41-T2` | Add `SpecHarvesterTrustedLocalAdapterRunRequest` as a machine-readable request fixture. |
| `P41-T3` | Add a trusted local adapter run preflight report fixture that rejects unsafe requests before execution. |
| `P41-T4` | Add a disabled-by-default runner skeleton that validates requests and emits a no-execution report. |
| `P41-T5` | Connect trusted local adapter run reports to `autonomous-candidate-batch` as review-only producer evidence. |
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

## Runner Boundary

The first runner task must stay disabled-by-default. It may validate a request
and emit a no-execution report. It must not load third-party adapter code or
launch adapter processes until a later task explicitly introduces that mode.

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
