# SpecPM Handoff Guide

This guide explains how to hand a generated SpecHarvester candidate bundle to
SpecPM review without treating generated output as accepted registry truth.

SpecHarvester produces an evidence-rich candidate. SpecPM validates package
shape and registry policy. A maintainer approves acceptance. The public index
publishes only reviewed sources.

It is not:

```text
SpecHarvester generates package -> SpecPM accepts automatically
```

## Required Bundle

A generated candidate intended for public SpecPM review must contain:

```text
candidate/
  specpm.yaml
  specs/*.spec.yaml
  producer-receipt.json
  validation-report.json
  diagnostics.json
```

The bundle is machine-verifiable evidence. `producer-receipt.json` records
producer identity, source inputs, configuration digest, output file hashes,
validation status, diagnostics status, privacy/security caveats, and human
review status. `validation-report.json` and `diagnostics.json` remain separate
artifacts so future tools can verify their hashes and inspect them without
trusting receipt prose.

## Operator Flow

1. Collect deterministic evidence from a pinned checkout:

   ```bash
   spec-harvester collect-local /path/to/repo \
     --repository https://github.com/example/project \
     --revision <commit-sha> \
     --out .specharvester/snapshots/project
   ```

2. Draft a candidate bundle:

   ```bash
   spec-harvester draft .specharvester/snapshots/project \
     --out .specharvester/candidates/example.project \
     --package-id example.project
   ```

3. Run producer-side handoff preflight:

   ```bash
   spec-harvester preflight-candidate-bundle \
     .specharvester/candidates/example.project
   ```

4. Render a static review site:

   ```bash
   spec-harvester render-spec-site \
     --candidate .specharvester/candidates/example.project \
     --output .specharvester/previews/example.project
   ```

5. Review the generated bundle before any SpecPM proposal:

   - inspect `producer-receipt.json` for producer identity, input provenance,
     configuration digest, `outputs[]` SHA-256 digests, validation references,
     diagnostics references, privacy notes, and `humanReview.status`;
   - inspect `validation-report.json` for validation status and error/warning
     counts;
   - inspect `diagnostics.json` for warnings, evidence gaps, unstable generated
     IDs, namespace/version overlap signals, privacy caveats, and security
     caveats;
   - inspect `author-ready-draft-quality-report.json` for
     `authorReadyDraft.status`, hard gates, dimensions, and author action items;
   - inspect the static viewer for a human-readable summary of the same
     evidence;
   - decide whether the candidate should be accepted, rejected, corrected, or
     regenerated.

6. When using SpecPM proposal automation, verify that the generated pull
   request body links the same evidence:

   - accepted source bundle path in the SpecPM diff;
   - `specpm.yaml`;
   - `producer-receipt.json`;
   - `validation-report.json`;
   - `diagnostics.json`;
   - `author-ready-draft-quality-report.json`;
   - producer preflight report artifact or command output;
   - static viewer artifact, when available;
   - accepted-source diff in the pull request.

   The links are review evidence. They do not replace SpecPM validation or the
   maintainer acceptance decision.

   If SpecPM adds an optional CI preflight gate for producer bundles, it should
   consume the same evidence layout and stable roles described in
   [`SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md`](SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md).
   The CI result can support review, but acceptance still requires maintainer
   approval or an explicit override outside generated receipts.

  Registry acceptance decision records are described in
  [`SPECPM_REGISTRY_ACCEPTANCE_DECISION.md`](SPECPM_REGISTRY_ACCEPTANCE_DECISION.md).
  SpecHarvester handoff artifacts may reference the external record, but must
  not write maintainer approval into `producer-receipt.json`.

## Package-Set Handoff

For generated package-set bundles, create a package-set handoff proposal before
any future SpecPM PR:

```bash
spec-harvester package-set-handoff-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --viewer .smoke/xyflow-package-set/viewer \
  --output .smoke/xyflow-package-set/handoff/proposal.json \
  --proposal-body .smoke/xyflow-package-set/handoff/proposal.md
```

The proposal links `package-set-draft.json`,
`package-relation-proposals.json`, `bundle-set-preflight.json`, package-set
viewer output, member candidate bundles, and relation summary evidence. It
uses `registryAcceptanceDecision.status: external_required` for both
`public_index_acceptance` and `package_relation_acceptance`.

This package-set proposal is still review evidence. It does not accept
packages, accept relations, publish registry metadata, or replace SpecPM
maintainer review. See
[`PACKAGE_SET_HANDOFF_PROPOSAL.md`](PACKAGE_SET_HANDOFF_PROPOSAL.md).

## Autonomous Candidate Batch Intake

For autonomous popular-library runs, review the candidate layer before any
SpecPM proposal or refresh decision work. The batch report links deterministic
collection, package-set preview bundles, bundle-set preflight, AI
draft/enrichment proposals, and author-ready stop-policy summaries.

Candidate-layer review can classify a repository as
`candidate_layer_review_required`, `needs_regeneration`, `blocked`, or
`not_for_intake`. These states are review guidance only. They do not accept
packages, accept relations, seed baselines, remove `preview_only`, or publish
registry metadata.

See
[`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md).

The P30 limited popular-library selected handoff dry run records this boundary
for `flask.core`, `gin.core`, and `docc2context.core` in
[`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md).
It includes producer preflight reports, static viewer digests, required bundle
file digests, and `registryAcceptanceDecision.status: external_required`
without creating a SpecPM pull request or accepting packages.

For portable selected-candidate review evidence, use the
`SpecHarvesterSelectedCandidateHandoffProposal` contract described in
[`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md).
It records selected candidates, deferred candidates, required evidence roles,
producer preflight status, static viewer status, and the same external
acceptance boundary. It still cannot accept packages, accept relations, seed
baselines, remove `preview_only`, publish registry metadata, or create a
SpecPM pull request.

The producer helper writes both machine-readable and Markdown handoff artifacts:

```bash
spec-harvester selected-candidate-handoff-proposal \
  --selected-handoff-dry-run .smoke/selected-handoff/p30-t5-selected-handoff.json \
  --candidate-root .smoke/selected-handoff/selected \
  --preflight-root .smoke/selected-handoff/preflight \
  --viewer-root .smoke/selected-handoff/viewer \
  --output .smoke/selected-handoff/selected-candidate-handoff-proposal.json \
  --proposal-body .smoke/selected-handoff/selected-candidate-handoff-proposal.md
```

P31-T3 records a generated dry-run handoff proposal for the real P30 selected
candidates in
`tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`
and [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md).
This is still producer preview evidence only, not SpecPM acceptance.

## Fresh Candidate Refresh Run

When a package-set bundle is generated to evaluate whether current SpecPM
generated artifacts need an update, export it into the SpecPM refresh helper
layout:

```bash
spec-harvester fresh-candidate-refresh-run \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --fresh-generated-root .smoke/xyflow-package-set/fresh-generated \
  --output .smoke/xyflow-package-set/fresh-candidate-refresh-run.json
```

This writes `SpecHarvesterFreshCandidateRefreshRun` and copies member
candidates into:

```text
<package_id>/<version>/specpm.yaml
<package_id>/<version>/specs/*.spec.yaml
```

The report records package IDs, version, source revision, contract-file
digests, and the downstream
`specpm producer-bundle prepare-refresh-decision` command arguments. SpecPM
then produces `refresh-decision.json`, `prepare-report.json`, and
`preflight-report.json`.

This is still review evidence only. It records `producerEvidenceAuthority:
evidence_only` and `noRegistryMutation: true`; it does not update curated
accepted artifacts or publish registry metadata. See
[`FRESH_CANDIDATE_REFRESH_RUN.md`](FRESH_CANDIDATE_REFRESH_RUN.md).

## Baseline Submission Handoff

If SpecPM `prepare-report.json` contains
`refresh_decision_prepare_current_contract_files_missing`, the repository does
not yet have current generated artifacts to compare against. In that state,
emit a first-submission or seeded-baseline handoff instead of treating the run
as a normal refresh decision:

```bash
spec-harvester baseline-submission-handoff \
  --fresh-candidate-refresh-run .smoke/tanstack-query/fresh-candidate-refresh-run.json \
  --specpm-prepare-report .smoke/tanstack-query/prepare-report.json \
  --output .smoke/tanstack-query/baseline-submission-handoff.json
```

The output is `SpecHarvesterBaselineSubmissionHandoff`. It records
`first_submission_required`, maintainer actions such as
`first_submission_review`, `seed_baseline`, and
`reject_or_request_regeneration`, and the boundary
`notRefreshDecision: true`. It does not seed SpecPM automatically, accept
packages, publish registry metadata, or replace maintainer review. See
[`BASELINE_SUBMISSION_HANDOFF.md`](BASELINE_SUBMISSION_HANDOFF.md).

## Receipt Example

```json
{
  "apiVersion": "specpm.receipts/v0",
  "kind": "SpecPMProducerReceipt",
  "schemaVersion": 1,
  "receiptProfile": "generated_spec_package_v0",
  "producer": {
    "name": "SpecHarvester",
    "version": "0.1.0"
  },
  "subject": {
    "packageId": "example.project",
    "packageVersion": "0.1.0",
    "boundarySpecs": ["specs/example_project.spec.yaml"]
  },
  "outputs": [
    {
      "path": "specpm.yaml",
      "role": "manifest",
      "digest": {
        "algorithm": "sha256",
        "value": "<64 lowercase hex characters>"
      }
    }
  ],
  "validation": {
    "status": "passed",
    "reportPath": "validation-report.json",
    "reportDigest": {
      "algorithm": "sha256",
      "value": "<64 lowercase hex characters>"
    }
  },
  "diagnostics": {
    "status": "clean",
    "path": "diagnostics.json",
    "digest": {
      "algorithm": "sha256",
      "value": "<64 lowercase hex characters>"
    }
  },
  "humanReview": {
    "status": "required",
    "requiredFor": ["public_index_acceptance"]
  }
}
```

`producer-receipt.json` must not appear in `outputs[]`; receipt self-hashing is
handled outside the receipt body.

## Validation Report Example

```json
{
  "kind": "SpecHarvesterProducerValidationReport",
  "schemaVersion": 1,
  "status": "valid",
  "summary": {
    "errorCount": 0,
    "warningCount": 0
  },
  "authority": "producer_side_shape_check"
}
```

This report is producer-side evidence. It does not replace SpecPM validation.

## Diagnostics Example

```json
{
  "kind": "SpecHarvesterProducerDiagnosticsReport",
  "schemaVersion": 1,
  "status": "clean",
  "entries": [],
  "privacy": {
    "privatePromptsIncluded": false,
    "rawSourceIncluded": false,
    "secretsIncluded": false
  },
  "security": {
    "caveat": "Generated diagnostics are review evidence only."
  },
  "review": {
    "acceptanceAuthority": "maintainer_review",
    "requiredFor": ["public_index_acceptance"]
  }
}
```

## Rejection Signals

Reject or regenerate the candidate when preflight or review finds:

- missing `specpm.yaml`, `specs/*.spec.yaml`, `producer-receipt.json`,
  `validation-report.json`, `diagnostics.json`, or
  `author-ready-draft-quality-report.json`;
- unsupported receipt `apiVersion`, `kind`, `schemaVersion`, or
  `receiptProfile`;
- output hash mismatch;
- `producer-receipt.json` listed in `outputs[]`;
- validation or diagnostics report digest mismatch;
- author-ready quality report digest mismatch;
- missing source input evidence or bundle-local input path escapes;
- unstable generated IDs;
- generated claims without backing evidence;
- privacy-sensitive content, secrets, private prompts, or confidential raw
  source in public handoff artifacts;
- namespace or `packageId@version` overlap without explicit maintainer review.

## Acceptance Boundary

For public index handoff, `humanReview.status` should remain `required` or
`pending` until a maintainer reviews the candidate. Public index acceptance
requires `humanReview.status: approved` or an explicit maintainer override
recorded outside the generated bundle, normally in the accepted-source pull
request.

SpecHarvester evidence can support the decision. It cannot make the decision.

The external decision record is the handoff boundary for maintainer approval or
override. SpecHarvester proposal artifacts should use
`registryAcceptanceDecision.status: external_required` until SpecPM review
creates or records a `SpecPMRegistryAcceptanceDecision`.

## Package-Set AI Enrichment

After `draft-package-set` and `preflight-bundle-set`, operators may prepare
proposal-only semantic enrichment for generated package-set candidates:

```bash
spec-harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --provider-base-url http://127.0.0.1:1234 \
  --model openai/gpt-oss-20b \
  --request-output .smoke/xyflow-package-set/ai/requests.json \
  --output .smoke/xyflow-package-set/ai/ai-enrichment-proposals.json
```

The output is `SpecHarvesterPackageSetAIEnrichmentProposal` with
`apiVersion: spec-harvester.package-set-ai-enrichment/v0`. It records
`refinedSummary`, `capabilities`, `interfaces`, `evidencePaths`, confidence,
provider usage metadata, and diagnostics such as
`model_evidence_path_unsupported`.

The artifact is still review evidence. It does not mutate generated specs,
accept packages, accept relations, publish registry metadata, or replace
SpecPM maintainer review. See
[`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md).

## Shared Fixture Policy

When examples or tests are intended to demonstrate the SpecPM producer bundle
contract, keep them aligned through
[`SPECPM_SHARED_FIXTURE_POLICY.md`](SPECPM_SHARED_FIXTURE_POLICY.md). The
fixture policy requires exact SpecPM commit SHAs, generated fixture provenance,
and explicit drift handling instead of relying on mutable refs or silent
example updates.
