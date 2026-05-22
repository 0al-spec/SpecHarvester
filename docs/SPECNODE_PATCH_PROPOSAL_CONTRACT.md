# SpecNode Patch Proposal Contract

Status: Phase 11 contract

This document defines the schema-validated output contract for future
SpecNode-assisted candidate refinement.

The model may propose candidate metadata changes only as data. It cannot write
files, run commands, publish packages, bypass SpecPM validation, or make its
output accepted registry truth.

## Contract Names

- `SpecNodeCandidatePatchProposal`: schema-validated proposal containing
  candidate metadata edits.
- `candidatePatchProposal`: output kind requested by `SpecNodeRefinementJob`.
- `SpecNodeCandidatePatchOperation`: one structured operation against an
  allowed candidate file.
- `SpecNodeProposalProvenance`: provenance binding the proposal to the job,
  preview plan, source artifacts, provider receipt, and model policy.
- `SpecNodeProposalUsageReceipt`: top-level proposal receipt that embeds or
  references `SpecNodeProviderUsageReceipt`.
- `SpecNodeRejectionReason`: schema-validated refusal or inability reason.
- `reviewNotes`: optional structured notes for human review.
- `usageReceipt`: required runtime and policy receipt returned with every
  successful proposal or rejection.

## Relationship to Existing Contracts

The output contract is the last boundary before any generated change can be
applied:

```text
SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementJob
  -> SpecNodeOpenAICompatibleProviderAdapter
  -> SpecNodeCandidatePatchProposal | SpecNodeRejectionReason
  -> SpecHarvester schema validation
  -> human review
  -> optional local edit
  -> SpecPM validation
```

SpecHarvester must validate this output before any local file mutation.
SpecNode output remains untrusted proposal metadata.
The prompt that asks for this output is governed by
[`SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`](SPECNODE_REFINEMENT_PROMPT_CONTRACT.md),
including evidence-reference, negative-claim, and confidence-calibration rules.
After this structural output validates, clean-context semantic review is
governed by
[`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md).
The reviewer emits `SpecNodeSemanticReviewResult` findings only and cannot add
`candidatePatchProposal`, `operations`, retry directives, or direct file
writes.

## Output Envelope

SpecNode returns exactly one successful proposal or one rejection reason, plus a
usage receipt.

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeRefinementResult",
  "job": {
    "kind": "SpecNodeRefinementJob",
    "jobId": "01HY0000000000000000000000",
    "digest": "sha256:64-hex-digest"
  },
  "result": {
    "kind": "candidatePatchProposal",
    "proposal": {
      "kind": "SpecNodeCandidatePatchProposal",
      "proposalId": "01HY0000000000000000000001",
      "candidateId": "flask.core",
      "candidateVersion": "0.1.0",
      "baseCandidateDigest": "sha256:64-hex-digest",
      "sourceJobDigest": "sha256:64-hex-digest",
      "sourcePreviewPlanDigest": "sha256:64-hex-digest",
      "sourceArtifactDigests": [
        {
          "id": "boundary_spec",
          "path": "specs/flask.spec.yaml",
          "sha256": "64-hex-digest"
        }
      ],
      "operations": [],
      "provenance": {
        "kind": "SpecNodeProposalProvenance",
        "sourceJobDigest": "sha256:64-hex-digest",
        "sourceBundleDigest": "sha256:64-hex-digest",
        "sourcePreviewPlanDigest": "sha256:64-hex-digest",
        "sourceArtifactDigests": [],
        "baseCandidateDigest": "sha256:64-hex-digest",
        "providerReceiptDigest": "sha256:64-hex-digest",
        "modelId": "local-model-id",
        "createdAt": "2026-05-21T00:00:00Z",
        "policyDigest": "sha256:64-hex-digest",
        "promptBudget": {},
        "redactionPolicy": "path_digest_and_summary_only",
        "schemaVersion": 1
      },
      "validationExpectations": {
        "requiresSchemaValidation": true,
        "requiresHumanReview": true,
        "requiresSpecPMValidationAfterApply": true
      }
    }
  },
  "reviewNotes": [],
  "usageReceipt": {
    "kind": "SpecNodeProposalUsageReceipt",
    "providerReceipt": {
      "kind": "SpecNodeProviderUsageReceipt",
      "modelId": "local-model-id"
    }
  }
}
```

If no safe proposal can be produced, `result.kind` must be `rejectionReason`
and `result.rejection` must contain `SpecNodeRejectionReason`.

## Candidate Patch Proposal

`SpecNodeCandidatePatchProposal` contains structured edits only.

Required fields:

- `kind: SpecNodeCandidatePatchProposal`
- `proposalId`
- `candidateId`
- `candidateVersion`
- `baseCandidateDigest`
- `sourceJobDigest`
- `sourcePreviewPlanDigest`
- `sourceArtifactDigests`
- `operations`
- `provenance`
- `validationExpectations`

The proposal must not include raw repository source, raw documentation bodies,
provider logs, secrets, shell commands, Git commands, package manager commands,
or full-file replacement text.

## Patch Operation Shape

Each `SpecNodeCandidatePatchOperation` is one candidate metadata operation.

```json
{
  "operationId": "op-001",
  "op": "replace_field",
  "targetFile": "specs/flask.spec.yaml",
  "targetPointer": "/provides/capabilities/0/summary",
  "expectedCurrentValueSha256": "sha256:64-hex-digest",
  "value": "Bounded candidate summary",
  "rationale": "Clarifies the capability from compact evidence.",
  "evidenceRefs": ["harvest_snapshot", "semantic_evidence_index"],
  "confidence": 0.72
}
```

Allowed operations:

- `add_field`
- `replace_field`
- `remove_field`
- `append_unique`
- `replace_list_item_by_id`
- `remove_list_item_by_id`

Allowed target files:

- `specpm.yaml`
- `specs/*.spec.yaml`

Allowed target pointer classes:

- package metadata fields;
- BoundarySpec identity and summary fields;
- `provides.capabilities` metadata;
- `provides.interfaces` metadata;
- intent and capability evidence references;
- provenance metadata already present in the candidate;
- review notes stored as candidate metadata when a future implementation
  explicitly allows them.

Rejected operation shapes:

- `rawUnifiedDiff`
- `fullFileReplacement`
- `shellCommand`
- `gitCommand`
- `networkFetch`
- `providerCall`
- `packageManagerCommand`
- `testRunnerCommand`
- `buildToolCommand`
- direct file writes;
- operations targeting files outside `specpm.yaml` or `specs/*.spec.yaml`;
- operations without `expectedCurrentValueSha256`;
- operations without `rationale` and `evidenceRefs`.

## Provenance

`SpecNodeProposalProvenance` must bind the proposal to deterministic inputs and
runtime policy.

Required fields:

- `sourceJobDigest`
- `sourceBundleDigest`
- `sourcePreviewPlanDigest`
- `sourceArtifactDigests`
- `baseCandidateDigest`
- `providerReceiptDigest`
- `modelId`
- `createdAt`
- `policyDigest`
- `promptBudget`
- `redactionPolicy`
- `schemaVersion`

The provenance must not rely on model assertions. It must point to digests and
runtime receipts produced by SpecNode and deterministic artifacts produced by
SpecHarvester.

## Usage Receipt

`SpecNodeProposalUsageReceipt` is required for both successful proposals and
rejections.

Required fields:

- `kind: SpecNodeProposalUsageReceipt`
- `jobId`
- `proposalId`, when a proposal exists;
- `rejectionId`, when a rejection exists;
- `providerReceipt`
- `providerReceiptDigest`
- `modelId`
- `inputTokens`
- `outputTokens`
- `totalTokens`
- `finishReason`
- `attempts`
- `startedAt`
- `completedAt`
- `durationMs`
- `timeoutPolicy`
- `retryPolicy`
- `temperature`
- `maxOutputTokens`
- `promptBudget`
- `responseSha256`
- `redactionPolicy`

The receipt may reference `SpecNodeProviderUsageReceipt` from the provider
adapter contract. It must not persist raw prompts, raw responses, secrets, or
provider logs unless a later contract defines a bounded redacted artifact.

## Rejection Reason

`SpecNodeRejectionReason` is returned when SpecNode cannot safely produce a
proposal.

Allowed rejection codes:

- `insufficient_evidence`
- `prompt_budget_exceeded`
- `provider_unavailable`
- `model_output_invalid`
- `policy_violation`
- `unsupported_candidate_shape`
- `schema_validation_failed`
- `safety_boundary_triggered`

Required fields:

- `kind: SpecNodeRejectionReason`
- `rejectionId`
- `code`
- `message`
- `sourceJobDigest`
- `sourcePreviewPlanDigest`
- `evidenceRefs`
- `usageReceipt`

Rejections are not failures of deterministic harvesting. They are safe model
non-output states that keep the original candidate unchanged.

## Review Notes

`reviewNotes` are optional structured notes for humans.

Allowed fields:

- `noteId`
- `severity`
- `message`
- `evidenceRefs`
- `operationIds`
- `confidence`

Review notes cannot command the host, request shell execution, request network
fetches, or instruct SpecHarvester to bypass schema validation, human review,
or SpecPM validation.

## Validation Before Apply

SpecHarvester must reject model output before any local edit when:

- output is not valid JSON-compatible data;
- `kind` is not `SpecNodeRefinementResult`;
- neither `candidatePatchProposal` nor `rejectionReason` is present;
- both proposal and rejection are present;
- `usageReceipt` is missing;
- required provenance fields are missing;
- digests do not match the job, preview plan, artifact bundle, or base
  candidate;
- any operation targets a forbidden file or pointer;
- any operation lacks `expectedCurrentValueSha256`;
- any operation asks for shell, filesystem, Git, provider, package manager,
  test, build, or network behavior;
- raw repository source, raw documentation bodies, secrets, provider logs, or
  full-file replacement text appear in the output.

After a human accepts a proposal and SpecHarvester applies the corresponding
local edit, SpecHarvester must rerun SpecPM validation before any promotion or
accepted-source proposal.

## Non-Goals

P11-T4 does not implement JSON Schema validators, model execution, provider
calls, local patch application, or accepted-source mutation. It defines the
output boundary that later implementation must enforce.
P11-T5 adds structural smoke validation for local provider-stub output in
[`SPECNODE_PROVIDER_SMOKE_COVERAGE.md`](SPECNODE_PROVIDER_SMOKE_COVERAGE.md);
that validation is a smoke gate, not accepted registry truth.

## Review Rule

A model-generated candidate change is safe to present for review only when it
is structured, schema-validated, digest-bound, provenance-linked, receipted, and
free of authority-expanding instructions. It is never accepted registry truth
until validated and reviewed through the normal SpecPM process.
