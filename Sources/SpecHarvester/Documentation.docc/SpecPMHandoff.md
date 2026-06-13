# SpecPM Handoff

This page mirrors `docs/SPECPM_HANDOFF.md` and explains how to hand a generated
SpecHarvester candidate bundle to SpecPM review without treating generated
output as accepted registry truth.

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

`producer-receipt.json` records producer identity, source inputs,
configuration digest, output file hashes, validation status, diagnostics
status, privacy/security caveats, and human review status. The separate
`validation-report.json` and `diagnostics.json` artifacts remain
machine-readable evidence for reviewers and future verification tools.

## Operator Flow

Collect deterministic evidence from a pinned checkout:

```bash
spec-harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out .specharvester/snapshots/project
```

Draft a candidate bundle:

```bash
spec-harvester draft .specharvester/snapshots/project \
  --out .specharvester/candidates/example.project \
  --package-id example.project
```

Run producer-side handoff preflight:

```bash
spec-harvester preflight-candidate-bundle \
  .specharvester/candidates/example.project
```

Render a static review site:

```bash
spec-harvester render-spec-site \
  --candidate .specharvester/candidates/example.project \
  --output .specharvester/previews/example.project
```

Review `producer-receipt.json`, `validation-report.json`, `diagnostics.json`,
`author-ready-draft-quality-report.json`, and the static viewer before any
SpecPM proposal. The reviewer decides whether the candidate should be accepted,
rejected, corrected, or regenerated.

When proposal automation opens a SpecPM pull request, the PR body should link
the same evidence: accepted source bundle path, `specpm.yaml`,
`producer-receipt.json`, `validation-report.json`, `diagnostics.json`,
`author-ready-draft-quality-report.json`, producer preflight report artifact or
command output, static viewer artifact when available, and the accepted-source diff.
These links are review evidence; they do not replace SpecPM validation or
maintainer acceptance.

If SpecPM adds an optional CI preflight gate for producer bundles, it should
consume the same evidence layout and stable roles described in
<doc:SpecPMCiPreflightGateSupport>. The CI result can support review, but
acceptance still requires maintainer approval or an explicit override outside
generated receipts.

Registry acceptance decision records are described in
<doc:SpecPMRegistryAcceptanceDecision>. SpecHarvester handoff artifacts may
reference the external record, but must not write maintainer approval into
`producer-receipt.json`.

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

This package-set proposal is review evidence. It does not accept packages,
accept relations, publish registry metadata, or replace SpecPM maintainer
review. See <doc:PackageSetHandoffProposal>.

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

See <doc:AutonomousCandidateIntakePolicy>.

The P30 limited popular-library selected handoff dry run records this boundary
for `flask.core`, `gin.core`, and `docc2context.core` in
<doc:LimitedPopularLibrarySelectedHandoffDryRun>. It includes producer
preflight reports, static viewer digests, required bundle file digests, and
`registryAcceptanceDecision.status: external_required` without creating a
SpecPM pull request or accepting packages.

For portable selected-candidate review evidence, use
<doc:SelectedCandidateHandoffProposal>. It records selected candidates,
deferred candidates, required evidence roles, producer preflight status, static
viewer status, and the same external acceptance boundary. It still cannot
accept packages, accept relations, seed baselines, remove `preview_only`,
publish registry metadata, or create a SpecPM pull request.

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
and <doc:SelectedCandidateHandoffProposalP31T3>. This is still producer
preview evidence only, not SpecPM acceptance.

P31-T4 records downstream SpecPM-side preflight expectations for this artifact
in <doc:SelectedCandidateHandoffPreflightExpectations>. The expected future
gate checks identity, candidate sets, evidence roles, digests, producer
preflight status, static viewer status, registry acceptance decision
boundaries, and non-authority statements. Passing that future preflight still
does not accept packages.

P31-T5 records the regeneration requirements for the six deferred P30
candidates in <doc:DeferredSelectedCandidateRegenerationRequirements>. Those
requirements cover package-set identity regeneration, warning-bearing
enrichment regeneration, and identity-drift resolution before any deferred
candidate can enter selected handoff.

## Fresh Candidate Refresh Run

Use <doc:FreshCandidateRefreshRun> when a generated package-set output should
be compared against current SpecPM generated artifacts. The
`fresh-candidate-refresh-run` command writes
`SpecHarvesterFreshCandidateRefreshRun`, copies candidates into the
`<package_id>/<version>/specpm.yaml` and `specs/*.spec.yaml` layout, records
contract-file digests, and points operators at
`specpm producer-bundle prepare-refresh-decision`.

The refresh run is producer evidence only. It records
`producerEvidenceAuthority: evidence_only` and `noRegistryMutation: true`.

## Baseline Submission Handoff

Use <doc:BaselineSubmissionHandoff> when SpecPM `prepare-report.json` contains
`refresh_decision_prepare_current_contract_files_missing`. That state means the
repository has no current generated baseline to compare against, so the next
review step is first submission, seeded baseline, or rejection rather than a
normal refresh decision.

The `baseline-submission-handoff` command writes
`SpecHarvesterBaselineSubmissionHandoff`, records
`first_submission_required`, maintainer actions such as
`first_submission_review`, `seed_baseline`, and
`reject_or_request_regeneration`, and preserves `notRefreshDecision: true`.
It does not seed SpecPM automatically, accept packages, publish registry
metadata, or replace maintainer review.

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

## Report Examples

`validation-report.json` records producer-side shape evidence:

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

`diagnostics.json` records privacy, security, and review caveats:

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

Reject or regenerate the candidate when preflight or review finds missing
required bundle files, unsupported receipt identity fields, output hash
mismatch, `producer-receipt.json` in `outputs[]`, validation or diagnostics
digest mismatch, missing input evidence, bundle-local input path escapes,
unstable generated IDs, generated claims without evidence, privacy-sensitive
content, or namespace and `packageId@version` overlap without maintainer review.

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
SpecPM maintainer review. See <doc:PackageSetAIEnrichment>.

## Shared Fixture Policy

When examples or tests demonstrate the SpecPM producer bundle contract, keep
them aligned through <doc:SpecPMSharedFixturePolicy>. The fixture policy
requires exact SpecPM commit SHAs, generated fixture provenance, and explicit
drift handling instead of relying on mutable refs or silent example updates.

Future optional SpecPM CI preflight support should consume the same evidence
layout and stable roles described in <doc:SpecPMCiPreflightGateSupport>.
