# AI Enrichment Candidate Patch

Status: P34-T1 AI-enabled review helper.

`apply-ai-enrichment-proposal` turns a clean
`SpecHarvesterPackageSetAIEnrichmentProposal` into a copied, reviewable
candidate bundle with the proposed summary, capabilities, and interface
summaries applied.

It is the first deterministic step after local LM Studio/OpenAI-compatible
enrichment:

```text
candidate bundle
  + package-set-ai-enrichment-proposal.json
  -> apply-ai-enrichment-proposal
  -> enriched preview candidate copy
  -> ai-enrichment-candidate-patch.json
  -> producer/SpecPM validation and maintainer review
```

## Command

```bash
python3 -m spec_harvester apply-ai-enrichment-proposal \
  --proposal .smoke/fastapi/package-sets/fastapi/ai/package-set-ai-enrichment-proposal.json \
  --candidate .smoke/fastapi/package-sets/fastapi/fastapi.core \
  --package-id fastapi.core \
  --output .smoke/fastapi/enriched/fastapi.core
```

Use `--report` to write the patch report outside the enriched candidate
directory:

```bash
python3 -m spec_harvester apply-ai-enrichment-proposal \
  --proposal .smoke/fastapi/package-sets/fastapi/ai/package-set-ai-enrichment-proposal.json \
  --candidate .smoke/fastapi/package-sets/fastapi/fastapi.core \
  --package-id fastapi.core \
  --output .smoke/fastapi/enriched/fastapi.core \
  --report .smoke/fastapi/reports/ai-enrichment-candidate-patch.json
```

## Input Contract

The helper requires:

- `apiVersion: spec-harvester.package-set-ai-enrichment/v0`;
- `kind: SpecHarvesterPackageSetAIEnrichmentProposal`;
- `status: completed`;
- `authority: proposal_only_not_registry_acceptance`;
- selected proposal `status: proposed`;
- selected proposal `packageId` matching the candidate;
- `refinedSummary`;
- at least one proposed capability;
- no unresolved diagnostics for the selected package.

Warning-bearing proposals are rejected by default. Operators should regenerate
or review the proposal instead of silently applying it.

## Applied Fields

Applied changes are intentionally narrow:

- `specpm.yaml` `metadata.summary`;
- BoundarySpec `intent.summary`;
- primary capability summary;
- additive model-proposed capabilities;
- additive or updated inbound interface summaries;
- producer receipt output digests for changed bundle files.

The helper writes `ai-enrichment-candidate-patch.json` with:

- source candidate and enriched candidate paths;
- proposal digest;
- before/after candidate digests;
- applied and skipped changes;
- provider/model provenance copied from the proposal;
- non-authority boundary statements.

## Boundaries

The source candidate bundle is not mutated.

The enriched copy remains `preview_only: true`. The patch report is producer
review evidence only. It is not registry truth and does not:

- does not accept packages;
- does not accept relations;
- seed baselines;
- does not remove `preview_only`;
- publish registry metadata;
- replace SpecPM validation;
- replace maintainer review;
- persist raw prompts, raw model responses, secrets, or chain-of-thought.

## FastAPI Motivation

The FastAPI live LM Studio smoke showed the gap this helper closes:

- deterministic draft: valid starter package with a broad web-framework
  summary;
- AI enrichment: better repository-specific proposal, including HTTP routing,
  middleware, request/response context, and OpenAPI generation capabilities;
- before P34-T1: improvements stayed sidecar-only in JSON;
- after P34-T1: clean improvements can become a reviewable enriched candidate
  copy while preserving all authority boundaries.

Short form:

```text
AI output becomes reviewable candidate diff, not registry truth.
```
