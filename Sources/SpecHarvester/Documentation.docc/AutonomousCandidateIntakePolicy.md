# Autonomous Candidate Intake Policy

Status: SpecPM-facing producer policy

This policy describes how SpecPM maintainers can review autonomous candidate
batch output without turning SpecHarvester producer evidence into accepted
registry truth.

It applies to:

- `SpecHarvesterAutonomousCandidateBatchReport`;
- package-set preview bundles;
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
- `blocked`: required deterministic evidence is missing or failed.
- `not_for_intake`: the repository is intentionally excluded from SpecPM intake.

These states are producer-side review guidance only. They are not SpecPM
acceptance decisions.

## Required Maintainer Checks

Before any SpecPM-side proposal, a maintainer should verify:

- identity: `apiVersion`, `kind`, `schemaVersion`, repository id, and package id
  hints;
- source provenance: public repository URL, exact source revision, and
  operator-provided local checkout path;
- deterministic evidence: `harvest.json`, `workspace-inventory.json`,
  `public-interface-index.json`, `batch-validation-report.json`, and collection
  status;
- candidate shape: candidate count, relation count, package-set draft status,
  `bundle-set-preflight.json`, and member evidence links;
- AI proposal evidence: provider receipts, privacy flags, unsupported evidence
  path diagnostics, `SpecHarvesterPackageSetAIDraftProposal`, and
  `SpecHarvesterPackageSetAIEnrichmentProposal`;
- author-ready state: `authorReadyDraftSummary.decision`, `stop_for_author_review`,
  `continue_generation`, `blocked_until_inputs_change`, author action items,
  and evidence gaps.

## Authority Boundary

Autonomous candidate output is `producer_preview_evidence_only`.

It cannot accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, grant namespace ownership, replace
SpecPM validation, replace maintainer review, or treat AI output as accepted
package truth.

SpecPM remains the validation, acceptance, relation, baseline, and registry
authority.

## Candidate-Layer Review Flow

```text
local public checkout
  -> autonomous-candidate-batch
  -> candidate-layer review
  -> optional regeneration or author edits
  -> SpecPM proposal/preflight
  -> maintainer acceptance decision
```

Candidate-layer review asks whether deterministic evidence is present, producer
preflight passed, candidate counts and relation counts are plausible, AI
proposals are privacy-safe, and output is ready for author review or
regeneration. It does not decide registry acceptance.

## Known Corpus Follow-Up Work

The first mixed corpus run identified two known gaps. Both now have producer-side
mitigation paths, but the mixed corpus still needs a post-fallback quality gate
before broad scraping:

- `single_package_fallback_needed`: mitigated by the deterministic
  single-package candidate fallback for repositories such as Flask and Gin.
- `ai_json_repair_needed`: mitigated by bounded local
  LM Studio/OpenAI-compatible JSON repair diagnostics.

Those gaps are tracked in <doc:AutonomousCandidateTechDebtPlan>. Until the
post-mitigation corpus quality gate passes, maintainers should treat affected
repositories as candidate-layer evidence, not as accepted packages.

The first durable Flask/Gin/xyflow baseline is recorded in
<doc:AutonomousCandidateCorpusBaseline>.
