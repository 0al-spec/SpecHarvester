# Operational MVP Validation Plan Fixture

Status: Phase 43 fixture contract.

`SpecHarvesterOperationalMVPValidationPlan` is the machine-readable plan
fixture for Phase 43 operational MVP validation. It records selected corpus
requirements, pinned local checkout policy, run modes, quality dimensions, stop
policy, and non-authority boundaries before any real corpus run starts.

Fixture path:

```text
tests/fixtures/operational_mvp_validation/p43-t2-operational-mvp-validation-plan.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.operational-mvp-validation-plan/v0",
  "kind": "SpecHarvesterOperationalMVPValidationPlan",
  "schemaVersion": 1,
  "authority": "producer_operational_mvp_validation_plan_only"
}
```

The authority means:

```text
operational MVP validation plan = producer-side evidence plan
operational MVP validation plan != real corpus run
operational MVP validation plan != package acceptance
operational MVP validation plan != registry authority
operational MVP validation plan != adapter execution permission
```

## Corpus Requirements

The fixture is synthetic and placeholder-based. It does not require local
checkouts to exist in P43-T2.

Each corpus item records:

- repository URL;
- local checkout path placeholder;
- exact revision placeholder;
- ecosystem family;
- expected package-family shape;
- allowed run modes;
- stop conditions.

The example corpus covers `xyflow` as a JavaScript/TypeScript package-set
monorepo, `FastAPI` or `FastMCP` as a Python framework/library package, `gin`
as a Go single-package framework, and one additional operator-selected
ecosystem placeholder.

The input policy requires `operator_selected_pinned_local_checkouts`,
`localCheckoutRequired: true`, `exactRevisionRequired: true`,
`implicitCloneOrFetchAllowed: false`, `networkDiscoveryAllowed: false`, and
`mutableRevisionAccepted: false`.

## Run Modes

The fixture declares two run modes:

- `static_only` with `aiInvocation: not_run`, `adapterExecution: not_run`,
  `networkAccess: not_allowed`, `packageManagerInvocation: not_allowed`, and
  `dependencyInstallation: not_allowed`.
- `ai_enabled_proposal` with `providerPolicy:
  local_openai_compatible_optional`, `aiOutputAuthority: proposal_only`,
  `adapterExecution: not_run`, and `registryAuthority: false`.

Both modes use the same `qualityDimensions[]` and the same
`shared_operational_mvp_stop_policy`.

## Quality Dimensions

Operational MVP validation records:

- `validity`;
- `repositorySpecificity`;
- `evidencePrecision`;
- `packageTopology`;
- `claimConservatism`;
- `authorActionability`;
- `SpecPMHandoffReadiness`.

Each dimension is required for an author-ready draft. Later tasks can turn
these dimensions into per-repository result fields without inventing a new
quality vocabulary.

## Stop Policy

The shared stop policy includes:

- `missing_pinned_local_checkout`;
- `unverified_exact_revision`;
- `generated_artifacts_fail_validation`;
- `generated_artifacts_fail_preflight`;
- `ai_output_attempts_registry_authority`;
- `evidence_over_capture_makes_starter_misleading`;
- `requires_real_adapter_execution`;
- `package_or_relation_acceptance_requires_maintainer_decision`.

Allowed outcomes are `author_ready_draft`, `needs_quality_hardening`, and
`blocked`.

## Non-Authority Boundary

The fixture is producer-side evidence only. It records
`registryAuthority: false`, `acceptsPackages: false`,
`acceptsRelations: false`, `publishesRegistryMetadata: false`,
`seedsBaselines: false`, `removesPreviewOnly: false`,
`aiOutputAcceptedAsRegistryTruth: false`,
`adapterOutputAcceptedAsRegistryTruth: false`,
`trustedLocalAdapterExecutionEnabled: false`, `realCorpusRunPerformed: false`,
and `implicitRepositoryFetchAllowed: false`.

The fixture does not run the real corpus, clone or fetch repositories, accept
mutable repository state, execute harvested code, install dependencies, invoke
package managers, enable trusted local adapter execution, run adapter code, run
AI, accept packages, accept relations, publish registry metadata, seed
baselines, remove `preview_only`, treat AI output as registry truth, or treat
adapter output as registry truth.

## Follow-Up Tasks

- `P43-T3`: operational MVP validation report fixture.
- `P43-T4`: static-only quality baseline over operator-provided pinned
  checkouts.
- `P43-T5`: AI-enabled comparison over the same pinned corpus when a local
  provider is available.
- `P43-T6`: author handoff summaries.
- `P43-T7`: operational MVP exit report.

## References

- [`OPERATIONAL_MVP_VALIDATION_PLAN.md`](OPERATIONAL_MVP_VALIDATION_PLAN.md)
- [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
