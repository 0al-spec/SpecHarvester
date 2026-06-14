# AI Enrichment Candidate Patch

Status: P34-T1 AI-enabled review helper.

`apply-ai-enrichment-proposal` turns a clean
`SpecHarvesterPackageSetAIEnrichmentProposal` into a copied, reviewable
candidate bundle with proposed summary, capabilities, and interface summaries
applied.

```text
candidate bundle
  + package-set-ai-enrichment-proposal.json
  -> apply-ai-enrichment-proposal
  -> enriched preview candidate copy
  -> ai-enrichment-candidate-patch.json
  -> producer/SpecPM validation and maintainer review
```

## Input Contract

The helper requires a completed package-set AI enrichment proposal, a selected
proposal with `status: proposed`, a matching package id, a `refinedSummary`, at
least one proposed capability, and no unresolved diagnostics for that package.

Warning-bearing proposals are rejected by default.

## Applied Fields

Applied changes are limited to:

- `specpm.yaml` `metadata.summary`;
- BoundarySpec `intent.summary`;
- primary capability summary;
- additive model-proposed capabilities;
- additive or updated inbound interface summaries;
- producer receipt output digests for changed bundle files.

The helper writes `ai-enrichment-candidate-patch.json` with input digests,
before/after candidate digests, applied changes, skipped changes,
provider/model provenance, and non-authority statements.

## Boundary

The source candidate bundle is not mutated. The enriched copy remains
`preview_only: true`. The patch report is producer review evidence only and is
not registry truth. It does not accept packages, does not accept relations,
does not seed baselines, does not remove `preview_only`, does not publish
registry metadata, does not replace SpecPM validation, and does not replace
maintainer review.

Short form:

```text
AI output becomes reviewable candidate diff, not registry truth.
```
