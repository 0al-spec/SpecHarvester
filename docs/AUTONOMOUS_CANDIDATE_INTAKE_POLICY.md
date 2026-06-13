# Autonomous Candidate Intake Policy

Status: SpecPM-facing producer policy

This policy describes how SpecPM maintainers can review autonomous candidate
batch output without turning SpecHarvester producer evidence into accepted
registry truth.

The policy applies to output from `autonomous-candidate-batch`, especially:

- `SpecHarvesterAutonomousCandidateBatchReport`;
- package-set preview bundles under `package-sets/<repository-id>/`;
- `bundle-set-preflight.json`;
- `SpecHarvesterPackageSetAIDraftProposal`;
- `SpecHarvesterPackageSetAIEnrichmentProposal`;
- author-ready stop-policy summaries such as `authorReadyDraftSummary` and
  `stopPolicySummary`;
- generated candidate artifacts that remain `preview_only`.

## Intake States

SpecHarvester recommends one candidate-layer intake state per repository:

- `candidate_layer_review_required`: deterministic evidence and producer
  preflight are present, and a maintainer can review whether the preview
  candidate deserves handoff work.
- `needs_regeneration`: the batch output is structurally present but has model,
  evidence, or author-ready gaps that should be regenerated before maintainer
  review.
- `blocked`: required deterministic evidence is missing or failed, so the
  repository is not reviewable until inputs change.
- `not_for_intake`: the repository is intentionally excluded from SpecPM intake,
  for example because it is private, disabled, a fixture-only target, or outside
  the operator's selected scope.

These states are producer-side review guidance only. They are not SpecPM
acceptance decisions.

## Required Maintainer Checks

Before any SpecPM-side proposal, a maintainer should verify:

1. Identity:
   - report `apiVersion`;
   - report `kind: SpecHarvesterAutonomousCandidateBatchReport`;
   - `schemaVersion`;
   - repository id and package id hints.
2. Source provenance:
   - public repository URL;
   - exact source revision;
   - operator-provided local checkout path;
   - no claim that SpecHarvester cloned or fetched the repository.
3. Deterministic producer evidence:
   - `harvest.json`;
   - `workspace-inventory.json`;
   - `public-interface-index.json` when available;
   - `batch-validation-report.json`;
   - deterministic collection status.
4. Candidate shape:
   - candidate count;
   - relation count;
   - package-set draft status;
   - `bundle-set-preflight.json` status;
   - member candidate evidence links.
5. AI proposal evidence:
   - `SpecHarvesterPackageSetAIDraftProposal` status;
   - `SpecHarvesterPackageSetAIEnrichmentProposal` status;
   - provider receipts;
   - privacy flags: no raw prompts, raw responses, secrets, or chain-of-thought
     persisted;
   - unsupported evidence path diagnostics.
6. Author-ready state:
   - `authorReadyDraftSummary.decision`;
   - `stop_for_author_review`, `continue_generation`, or
     `blocked_until_inputs_change`;
   - author action items and evidence gaps.

## Authority Boundary

Autonomous candidate output is `producer_preview_evidence_only`.

It cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- grant namespace ownership;
- replace SpecPM validation;
- replace maintainer review;
- treat AI output as accepted package truth.

SpecPM remains the validation, acceptance, relation, baseline, and registry
authority.

## Candidate-Layer Review Flow

The intended flow is:

```text
local public checkout
  -> autonomous-candidate-batch
  -> candidate-layer review
  -> optional regeneration or author edits
  -> SpecPM proposal/preflight
  -> maintainer acceptance decision
```

Candidate-layer review should answer only:

- Is there enough deterministic evidence to review this repository?
- Did producer preflight pass?
- Are candidate counts and relation counts plausible for the repository shape?
- Are AI proposals clean, bounded, and privacy-safe?
- Is the output ready for author review, regeneration, or rejection?

It should not answer:

- Is this package accepted into SpecPM?
- Are these relations accepted into the registry?
- Should public index metadata be published?
- Should a missing baseline be seeded automatically?

## Known Corpus Follow-Up Work

The first mixed corpus run identified two known gaps that do not invalidate
this policy. Both now have producer-side mitigation paths, but the mixed corpus
still needs a post-fallback quality gate before broad scraping:

- `single_package_fallback_needed`: mitigated by the deterministic
  single-package candidate fallback for repositories such as Flask and Gin.
- `ai_json_repair_needed`: mitigated by bounded local
  LM Studio/OpenAI-compatible JSON repair diagnostics.

Those gaps are tracked in
[`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md).
The first durable Flask/Gin/xyflow baseline is recorded in
[`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md).
Until the post-mitigation corpus quality gate passes, maintainers should treat
affected repositories as candidate-layer evidence, not as accepted packages.

## SpecPM Handoff

SpecHarvester can provide review evidence and candidate-layer guidance.
SpecPM should own any consumer-side preflight that turns this evidence into a
registry proposal gate.

A future SpecPM gate may consume this same evidence, but a passing gate should
still mean "review evidence is internally consistent", not "registry acceptance
is granted".
