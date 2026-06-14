# P30-T4 Candidate-Layer Triage Report

## Objective

Produce a machine-readable and operator-facing triage report for the P30
limited popular-library candidate layer.

The report must classify each generated preview package and each P30-T3 model
or generator finding before any selected SpecPM handoff dry run is prepared.

## Background

P30-T2 recorded a deterministic baseline for six repositories:

```text
tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json
```

P30-T3 recorded the matching live LM Studio run:

```text
tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json
```

The live run produced:

- `6` processed repositories;
- `9` generated preview candidates;
- `3` relation proposals;
- `6` passed preflights;
- AI draft statuses: `2 completed`, `4 warning`;
- AI enrichment statuses: `5 completed`, `1 warning`;
- JSON repair: `0 needed`, `0 exhausted`;
- product verdict: `ready_for_candidate_layer_triage`.

## Deliverables

- Add a machine-readable P30-T4 triage fixture that records:
  - corpus identity and source fixture links;
  - all generated preview package ids;
  - per-candidate triage classification;
  - per-finding classification;
  - selected candidates eligible for P30-T5 dry-run handoff;
  - candidates or findings that require regeneration before handoff;
  - non-authority boundaries.
- Add GitHub docs and DocC coverage for the triage report.
- Link the triage report from README, roadmap, corpus plan, deterministic
  batch docs, and live LM Studio batch docs.
- Add regression tests for the fixture shape and docs coverage.
- Archive Flow artifacts and set the next task to P30-T5.

## Triage States

- `candidate_layer_review_required`: valid starter package can proceed to
  author or maintainer review; not accepted registry truth.
- `needs_regeneration`: producer output should be regenerated or corrected
  before handoff because the finding points to package identity, summary, or
  model-output structure drift.
- `blocked`: required input is missing or a hard gate failed.
- `not_for_intake`: useful generator calibration evidence, but should not be
  handed to SpecPM.

## Initial Classification Policy

- Candidates with passed deterministic preflight, author-ready status, and no
  repository-level blocker are `candidate_layer_review_required`.
- Findings are classified independently from candidate readiness.
- `excluded_package_unknown` is model-output noise unless it changes generated
  candidate ids; it should not block a deterministic candidate.
- `package_set_id_missing` indicates AI draft structure drift and should be
  regenerated before AI-draft evidence is used for handoff.
- `refined_summary_missing` indicates AI enrichment quality drift and should be
  regenerated before AI-enrichment evidence is used for handoff.
- `package_id_hint_mismatch` for NavigationSplitView is a generator or manifest
  naming-policy issue and should be corrected or explicitly approved before
  selected handoff.

## Acceptance Criteria

- Every P30 generated preview package is represented exactly once in the
  triage fixture.
- The fixture includes all P30-T3 finding codes:
  - `excluded_package_unknown`;
  - `package_set_id_missing`;
  - `refined_summary_missing`;
  - `package_id_hint_mismatch`.
- The fixture records aggregate counts for candidate classifications and
  finding classifications.
- The product verdict says whether P30 can proceed to selected handoff dry run.
- The non-authority boundary explicitly says the triage report cannot accept
  packages, accept relations, seed baselines, remove `preview_only`, or publish
  registry metadata.
- Regression tests verify docs links, fixture identity, classification counts,
  selected candidates, and blocked/non-blocking findings.

## Non-Goals

- No repository clone/fetch.
- No new deterministic or live LM Studio run.
- No package content curation.
- No SpecPM handoff artifact generation.
- No SpecPM registry update, accepted-source proposal, relation acceptance, or
  baseline seeding.
- No automatic use of AI output as accepted `SpecPackage`, `BoundarySpec`, or
  relation truth.

---
**Archived:** 2026-06-13
**Verdict:** PASS
