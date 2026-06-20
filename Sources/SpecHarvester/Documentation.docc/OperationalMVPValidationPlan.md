# Operational MVP Validation Plan

Status: Phase 43 plan.

## Motivation

SpecHarvester now has repository profile selection, repository plugin
applicability evidence, adapter manifests and preflight reports, trusted local
adapter readiness, and trusted local adapter sandbox review boundaries.

Phase 43 validates whether that pipeline is operationally useful for authors:

```text
pinned local repository checkout
  -> bounded evidence
  -> valid starter SpecPackage or package-set
  -> optional proposal-only AI improvement
  -> author-ready quality report
  -> reviewable SpecPM handoff decision
```

## Goal

Answer whether SpecHarvester can produce a valid, repository-specific starter
package that an author would reasonably edit toward final quality.

The target is not a 100% final specification. The target is a strong valid
starter package with evidence, quality dimensions, and author action items.

## Machine-Readable Plan

P43-T2 records this plan as <doc:OperationalMVPValidationPlanFixture> and the
`SpecHarvesterOperationalMVPValidationPlan` fixture at:

```text
tests/fixtures/operational_mvp_validation/p43-t2-operational-mvp-validation-plan.example.json
```

The fixture is producer-side evidence only. It captures selected corpus
requirements, pinned local checkout policy, `static_only` and
`ai_enabled_proposal` run modes, quality dimensions, shared stop policy, and the
non-authority boundary before any real corpus run starts.

P43-T3 records the companion report shape as
<doc:OperationalMVPValidationReportFixture> and the
`SpecHarvesterOperationalMVPValidationReport` fixture. The report fixture
captures per-repository draft status, static-only result, AI-enabled result,
author-ready verdict, evidence precision notes, stop-policy outcome, and SpecPM
handoff readiness without claiming that a real corpus has run.

P43-T4 records the first real static-only baseline as
<doc:OperationalMVPStaticOnlyBaseline> and the
`SpecHarvesterOperationalMVPStaticOnlyBaseline` fixture. The baseline uses
operator-provided pinned local xyflow, FastAPI, and Gin checkouts and records
passed preflight, author-ready preview candidates, quality dimensions, SpecPM
handoff readiness, and the remaining non-authority boundary.

P43-T5 records the AI-enabled comparison gate as
<doc:OperationalMVPAIEnabledComparison> and the
`SpecHarvesterOperationalMVPAIEnabledComparison` fixture. The comparison uses
the same pinned corpus and records live local LM Studio proposal-only AI draft
and enrichment sidecars without accepting AI output as registry truth.

## Corpus

The corpus is operator-selected and pinned. SpecHarvester must not clone or
fetch repositories implicitly.

Minimum target shape:

| Ecosystem | Example candidate | Expected shape |
| --- | --- | --- |
| JavaScript/TypeScript | `xyflow` | package-set / monorepo |
| Python | `FastAPI` or `FastMCP` | framework/library package |
| Go | `gin` | single-package framework |
| Additional ecosystem | local pinned checkout when available | one more repository shape |

Each corpus record should include repository URL, local checkout path, exact
revision, ecosystem/language family, expected package-family shape, enabled run
modes, and stop conditions.

## Run Modes

Static-only mode uses deterministic collection, profile selection, plugin
applicability evidence, drafting, validation, preflight, quality report, and
viewer output. It must not invoke AI, execute adapter code, install
dependencies, invoke package managers, or use network discovery.

AI-enabled mode may use a local OpenAI-compatible provider such as LM Studio.
AI output remains proposal-only: provider receipts are provenance, generated
proposals remain schema-checked, and accepted registry output still requires
maintainer review.

## Quality Dimensions

Operational validation records:

- `validity`
- `repositorySpecificity`
- `evidencePrecision`
- `packageTopology`
- `claimConservatism`
- `authorActionability`
- `SpecPMHandoffReadiness`

## Stop Policy

The run should stop or downgrade the verdict when a checkout is missing or not
pinned, generated artifacts fail validation or preflight, evidence over-capture
makes the starter package misleading, AI output attempts to claim authority, or
the repository requires real adapter execution.

## Exit Decision

P43 should end with one of three decisions:

- `ready_for_bounded_autonomous_scraping`
- `needs_quality_hardening`
- `blocked_until_adapter_execution`

## Phase Tasks

- `P43-T1`: document this operational MVP validation plan.
- `P43-T2`: add a machine-readable operational validation plan fixture.
- `P43-T3`: add an operational validation report fixture.
- `P43-T4`: record a static-only multi-repository quality baseline.
- `P43-T5`: record an AI-enabled comparison over the same pinned corpus when a
  local provider is available.
- `P43-T6`: add author handoff summaries for operational MVP runs.
- `P43-T7`: record the exit decision.

## Non-Authority Boundary

Operational MVP validation is producer-side evidence. It does not accept
packages, does not accept relations, does not seed baselines, does not publish
registry metadata, does not remove `preview_only`, does not treat AI output as
registry truth, does not treat adapter output as registry truth, and does not
enable trusted local adapter execution.

## References

- `docs/OPERATIONAL_MVP_VALIDATION_PLAN.md`
- <doc:OperationalMVPValidationPlanFixture>
- <doc:OperationalMVPValidationReportFixture>
- <doc:OperationalMVPStaticOnlyBaseline>
- <doc:OperationalMVPAIEnabledComparison>
- <doc:AutonomousCandidateBatch>
- <doc:AuthorReadyDraftQualityBar>
- <doc:AuthorReadyDraftQualityReport>
- <doc:PackageSetAIDraftProposal>
- <doc:TrustedLocalAdapterRuntimeSandboxPlan>
