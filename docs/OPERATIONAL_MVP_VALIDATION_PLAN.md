# Operational MVP Validation Plan

Status: Phase 43 plan.

## Motivation

SpecHarvester has accumulated the safety and review plumbing needed for a
serious producer pipeline:

- repository profile selection;
- repository plugin applicability evidence;
- adapter manifests and preflight reports;
- trusted local adapter no-execution readiness;
- trusted local adapter sandbox review boundaries.

Those layers are useful only if the product loop is still strong:

```text
pinned local repository checkout
  -> bounded evidence
  -> valid starter SpecPackage or package-set
  -> optional proposal-only AI improvement
  -> author-ready quality report
  -> reviewable SpecPM handoff decision
```

Phase 43 validates that loop before broader autonomous scraping or any real
adapter execution work.

## Goal

Operational MVP validation should answer one question:

```text
Can SpecHarvester produce a valid, repository-specific starter package that an
author would reasonably edit toward final quality?
```

The target is not a 100% final specification. The target is a strong valid
starter package with clear evidence, quality dimensions, and author action
items.

## Machine-Readable Plan

P43-T2 records this plan as
[`OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md)
and the `SpecHarvesterOperationalMVPValidationPlan` fixture at:

```text
tests/fixtures/operational_mvp_validation/p43-t2-operational-mvp-validation-plan.example.json
```

The fixture is producer-side evidence only. It captures selected corpus
requirements, pinned local checkout policy, `static_only` and
`ai_enabled_proposal` run modes, quality dimensions, shared stop policy, and the
non-authority boundary before any real corpus run starts.

P43-T3 records the companion report shape as
[`OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md)
and the `SpecHarvesterOperationalMVPValidationReport` fixture. The report
fixture captures per-repository draft status, static-only result, AI-enabled
result, author-ready verdict, evidence precision notes, stop-policy outcome,
and SpecPM handoff readiness without claiming that a real corpus has run.

P43-T4 records the first real static-only baseline as
[`OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`](OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md)
and the `SpecHarvesterOperationalMVPStaticOnlyBaseline` fixture. The baseline
uses operator-provided pinned local xyflow, FastAPI, and Gin checkouts and
records passed preflight, author-ready preview candidates, quality dimensions,
SpecPM handoff readiness, and the remaining non-authority boundary.

P43-T5 records the AI-enabled comparison gate as
[`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
and the `SpecHarvesterOperationalMVPAIEnabledComparison` fixture. The
comparison uses the same pinned corpus and records live local LM Studio
proposal-only AI draft and enrichment sidecars without accepting AI output as
registry truth.

P43-T6 records author handoff summaries as
[`OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md`](OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md)
and the `SpecHarvesterOperationalMVPAuthorHandoffSummaries` fixture. The
handoff shows authors what is valid, reviewable, needs manual correction, and
must not be promoted.

## Corpus

The corpus is operator-selected and pinned. SpecHarvester must not clone or
fetch repositories implicitly for this phase.

Minimum target shape:

| Ecosystem | Example candidate | Expected shape |
| --- | --- | --- |
| JavaScript/TypeScript | `xyflow` | package-set / monorepo |
| Python | `FastAPI` or `FastMCP` | framework/library package |
| Go | `gin` | single-package framework |
| Additional ecosystem | local pinned checkout when available | one more repository shape |

Each corpus record should include:

- repository URL;
- local checkout path;
- exact revision;
- ecosystem/language family;
- expected package-family shape;
- enabled run modes;
- stop conditions.

## Run Modes

Phase 43 compares two modes.

### Static-only

Static-only mode uses existing deterministic collection, profile selection,
plugin applicability evidence, drafting, validation, preflight, quality report,
and viewer output.

It must not:

- invoke AI;
- execute adapter code;
- install dependencies;
- invoke package managers;
- use network discovery.

### AI-enabled

AI-enabled mode may use a local OpenAI-compatible provider such as LM Studio.

AI output remains proposal-only:

- provider receipts are provenance, not authority;
- raw prompt/response content must not become registry truth;
- generated proposals must remain schema-checked;
- accepted registry output still requires maintainer review.

## Quality Dimensions

Operational validation should record:

- `validity`: generated artifacts validate and pass relevant preflight.
- `repositorySpecificity`: summary, intent, capabilities, and evidence are
  specific to the repository.
- `evidencePrecision`: public interface evidence is not dominated by docs,
  examples, tests, generated files, or internal tooling.
- `packageTopology`: package-set/member structure is useful for monorepos.
- `claimConservatism`: claims are supported by observed evidence.
- `authorActionability`: the author can see what to keep, revise, reject, or
  enrich.
- `SpecPMHandoffReadiness`: output is ready for reviewable handoff, not
  automatic acceptance.

## Stop Policy

The operational run should stop or downgrade the verdict when:

- a local checkout is missing or not pinned;
- generated artifacts fail validation or preflight;
- evidence over-capture makes the starter package misleading;
- AI output attempts to claim registry authority;
- the repository needs real adapter execution, which remains disabled;
- package/relation acceptance would require maintainer decision.

## Exit Decision

P43 should end with one of three decisions:

- `ready_for_bounded_autonomous_scraping`: the current pipeline is good enough
  for a curated popular-library batch.
- `needs_quality_hardening`: the pipeline works, but specific evidence or
  draft-quality gaps should be fixed first.
- `blocked_until_adapter_execution`: useful output requires a future explicitly
  approved adapter runtime.

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

Operational MVP validation is producer-side evidence. It does not:

- does not accept packages;
- does not accept relations;
- does not seed baselines;
- does not publish registry metadata;
- does not remove `preview_only`;
- does not treat AI output as registry truth;
- does not treat adapter output as registry truth;
- does not enable trusted local adapter execution.

## References

- [`SPECS/Workplan.md`](../SPECS/Workplan.md)
- [`OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md)
- [`OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md)
- [`OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`](OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md)
- [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
- [`OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md`](OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
- [`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md)
- [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md)
- [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md)
- [`TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md`](TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md)
