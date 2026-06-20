# Operational MVP Validation Report Fixture

`SpecHarvesterOperationalMVPValidationReport` is the machine-readable report
fixture for Phase 43 operational MVP validation. It records per-repository
draft status, static-only result, AI-enabled result, author-ready verdict,
evidence precision notes, stop-policy outcome, and SpecPM handoff readiness
without accepting packages or publishing registry metadata.

Fixture path:

```text
tests/fixtures/operational_mvp_validation/p43-t3-operational-mvp-validation-report.example.json
```

## Identity

```json
{
  "apiVersion": "spec-harvester.operational-mvp-validation-report/v0",
  "kind": "SpecHarvesterOperationalMVPValidationReport",
  "schemaVersion": 1,
  "authority": "producer_operational_mvp_validation_report_only"
}
```

```text
operational MVP validation report = producer-side evidence report
operational MVP validation report != real corpus run
operational MVP validation report != package acceptance
operational MVP validation report != registry authority
operational MVP validation report != adapter execution permission
```

## Plan Linkage

The report fixture references the P43-T2 plan fixture with a pinned SHA-256
digest:

```text
tests/fixtures/operational_mvp_validation/p43-t2-operational-mvp-validation-plan.example.json
sha256:a035b03fb66ba6bf56fc09dc8301ce611f144aa9e8dc342b82a8f9fbc052b772
```

That linkage keeps report fields aligned with
`SpecHarvesterOperationalMVPValidationPlan`, especially the shared quality
dimension vocabulary and `shared_operational_mvp_stop_policy`.

## Repository Results

Each `repositoryResults[]` record includes repository id and URL, ecosystem
family, expected package-family shape, pinned checkout state, draft status,
`staticOnlyResult`, `aiEnabledResult`, `qualityDimensions`, author-ready
verdict, evidence precision notes, stop-policy outcome, and SpecPM handoff
readiness.

The P43-T3 fixture is synthetic and placeholder-based. It records
`reportMode: synthetic_fixture_shape_only` and `realCorpusRunPerformed: false`.
The example repository results are blocked before generation with
`missing_pinned_local_checkout` and `unverified_exact_revision`; they do not
pretend that a static baseline or AI comparison has run.

## Run Result Fields

`staticOnlyResult` records `runMode: static_only`, `status: not_run`,
`adapterExecution: not_run`, `aiInvocation: not_run`, and `registryAuthority:
false`.

`aiEnabledResult` records `runMode: ai_enabled_proposal`, `status: not_run`,
`aiOutputAuthority: proposal_only`, `adapterExecution: not_run`, and
`registryAuthority: false`.

Both result blocks preserve the boundary that P43-T3 defines the report shape
only. P43-T4 owns static-only baseline results, and P43-T5 owns AI-enabled
comparison results.

P43-T4 records those static-only baseline results in
<doc:OperationalMVPStaticOnlyBaseline> and the
`SpecHarvesterOperationalMVPStaticOnlyBaseline` fixture.

## Quality Dimensions and Stop Policy

The report uses the same quality dimension ids as P43-T2: `validity`,
`repositorySpecificity`, `evidencePrecision`, `packageTopology`,
`claimConservatism`, `authorActionability`, and `SpecPMHandoffReadiness`.

The shared stop policy remains `shared_operational_mvp_stop_policy`. The
synthetic fixture observes `missing_pinned_local_checkout` and
`unverified_exact_revision`, with per-repository `stopPolicyOutcome.outcome:
blocked`.

## Handoff Readiness

`specpmHandoffReadiness` records whether a repository result is ready for
reviewable SpecPM handoff. In the P43-T3 fixture every repository has
`ready: false`, `reason: no_generated_candidate_available`, and
`registryAuthority: false`.

## Non-Authority Boundary

The report fixture is producer-side evidence only. It records
`reportIsRegistryAuthority: false`, `acceptsPackages: false`,
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

- `P43-T4`: static-only quality baseline over operator-provided pinned
  checkouts.
- `P43-T5`: AI-enabled comparison over the same pinned corpus when a local
  provider is available.
- `P43-T6`: author handoff summaries.
- `P43-T7`: operational MVP exit report.

## References

- `docs/OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`
- <doc:OperationalMVPValidationPlan>
- <doc:OperationalMVPValidationPlanFixture>
- <doc:OperationalMVPStaticOnlyBaseline>
- <doc:AuthorReadyDraftQualityReport>
- <doc:AutonomousCandidateBatch>
