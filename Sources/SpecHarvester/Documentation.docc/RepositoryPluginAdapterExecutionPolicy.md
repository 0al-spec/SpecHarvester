# Repository Plugin Adapter Execution Policy

Status: Phase 40 policy contract.

P40-T4 defines the execution policy for future repository plugin adapters. It
does not implement adapter loading, adapter execution, sandbox launch, batch
integration, or registry publication.

The policy is disabled-by-default: no adapter code may run unless a future
task implements and verifies an explicit runtime boundary.

The policy boundary is:

```text
adapter manifest
  -> adapter preflight report
  -> explicit operator opt-in
  -> future bounded local adapter execution
  -> review-only adapter output evidence
```

The current implementation stops before adapter execution.

## Policy Goals

- Keep all adapter execution disabled by default.
- Keep `static_only` as the only current safe mode.
- Define `trusted_local_tool` as a future mode that requires explicit operator
  opt-in, passing preflight, path allowlists, bounded resources, and denied
  ambient capabilities.
- Block unsafe modes before adapter code can load.
- Keep adapter output as producer-side review evidence only.

## Execution Modes

| Mode | Status | Meaning |
| --- | --- | --- |
| `disabled` | Current default | No adapter code is loaded or run. Manifest and preflight metadata may be reviewed. |
| `static_only` | Current safe mode | Reads declared static local evidence artifacts only. No third-party adapter code is loaded. |
| `trusted_local_tool` | Future explicit opt-in only | Runs a bounded local tool chosen by the operator after passing preflight and sandbox policy checks. |
| `blocked` | Current denial state | Manifest, evidence, requested capability, or execution request is unsafe, unsupported, ambiguous, or missing required evidence. |

`disabled` and `static_only` are the only modes that can be represented by
current fixtures. `trusted_local_tool` is policy vocabulary for later work, not
an implemented runtime.

## Default Deny Rules

Every adapter starts from deny-by-default capabilities:

| Capability | Default |
| --- | --- |
| Filesystem read | Declared evidence paths only. |
| Filesystem write | Not allowed. |
| Network | Not allowed. |
| Dependency installation | Not allowed. |
| Package manager invocation | Not allowed. |
| Process execution | Not allowed. |
| Environment access | Not allowed. |
| Harvested code execution | Not allowed. |
| AI/model execution | Not allowed. |
| Registry write | Not allowed. |

Any undeclared, ambiguous, or unsupported capability request must become
`blocked`.

## Static-Only Mode

`static_only` can only read already collected evidence:

- `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`;
- adapter manifest files;
- adapter preflight reports;
- `harvest.json`;
- `workspace-inventory.json`;
- `repository-profile-detection.json`;
- `repository-parsing-profile-decision.json`;
- public-interface indexes;
- operator-supplied labels.

All paths must be safe relative paths. Absolute paths, parent segments,
backslashes, network paths, symlink escapes, and missing digests are blocked.

`static_only` does not execute adapter code. It only describes what a future
adapter could consume or what review tooling can infer from existing static
evidence.

## Trusted Local Tool Mode

`trusted_local_tool` is future-only and requires all of the following before it
can be considered:

- an adapter manifest with stable adapter id and version;
- a passing adapter preflight report;
- explicit operator opt-in for that adapter id and exact version;
- read path allowlist scoped to declared evidence artifacts;
- write path allowlist scoped to a dedicated output directory;
- no network discovery;
- no dependency installation;
- no package manager invocation;
- no harvested repository code execution;
- timeout;
- maximum output size;
- deterministic output file paths;
- output digests;
- diagnostics for every denied capability;
- a record that output authority is `producer_adapter_output_only`.

The mode remains blocked until a future task implements a sandbox and verifier
that can prove these requirements.

## Blocked Conditions

Adapter execution must be `blocked` when any of these are true:

- required evidence is missing;
- required digest is missing or mismatched;
- path policy is violated;
- requested role or output kind is unknown;
- requested authority claims package acceptance, relation acceptance, baseline
  seeding, registry publication, or registry truth;
- network access is requested;
- dependency installation is requested;
- package manager invocation is requested;
- harvested code execution is requested;
- unbounded process execution is requested;
- environment access is requested without an explicit allowlist;
- AI/model execution is requested without a separate proposal-only AI policy;
- operator opt-in is absent for any non-static mode.

## Output Authority

Adapter output remains producer-side evidence:

```text
adapter output = review evidence
adapter output != accepted package truth
adapter output != accepted relation truth
adapter output != baseline authority
adapter output != registry publication
adapter output != permission to remove preview_only
```

Future adapter output can only enter candidate workflows as review-only
evidence after digest recording, validation, and explicit operator selection.

## Relationship to Other Phase 40 Tasks

- P40-T1 defines the adapter contract.
- P40-T2 adds the adapter manifest fixture.
- P40-T3 adds the adapter preflight report fixture.
- P40-T4 defines this execution policy.
- P40-T5 connects manifest and preflight output to
  `autonomous-candidate-batch` as `repositoryPluginAdapterEvidence`
  review-only producer evidence through explicit operator-supplied sidecars.
- P40-T6 records <doc:RepositoryPluginAdapterCrossEcosystemFixtureMatrix> as
  cross-ecosystem adapter contract fixtures.
- P40-T7 should record real local adapter-contract validation over existing
  pinned checkouts.

P40-T4 intentionally does not enable adapter runtime.
