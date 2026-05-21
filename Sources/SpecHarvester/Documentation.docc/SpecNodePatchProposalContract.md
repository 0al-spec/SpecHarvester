# SpecNode Patch Proposal Contract

This page mirrors the GitHub patch proposal output contract for future
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
  preview plan, artifact bundle, provider receipt, and model policy.
- `SpecNodeProposalUsageReceipt`: top-level proposal receipt that embeds or
  references `SpecNodeProviderUsageReceipt`.
- `SpecNodeRejectionReason`: schema-validated refusal or inability reason.
- `reviewNotes`: optional structured notes for human review.
- `usageReceipt`: required runtime and policy receipt returned with every
  successful proposal or rejection.

## Output Envelope

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
      "operations": []
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

Required fields are `kind: SpecNodeCandidatePatchProposal`, `proposalId`,
`candidateId`, `candidateVersion`, `baseCandidateDigest`, `sourceJobDigest`,
`sourcePreviewPlanDigest`, `sourceArtifactDigests`, `operations`,
`provenance`, and `validationExpectations`.

The proposal must not include raw repository source, raw documentation bodies,
provider logs, secrets, shell commands, Git commands, package manager commands,
or full-file replacement text.

## Patch Operations

Each `SpecNodeCandidatePatchOperation` targets only `specpm.yaml` or
`specs/*.spec.yaml`.

Allowed operations are `add_field`, `replace_field`, `remove_field`,
`append_unique`, `replace_list_item_by_id`, and `remove_list_item_by_id`.

Each operation must include `operationId`, `op`, `targetFile`,
`targetPointer`, `expectedCurrentValueSha256`, `value` when needed,
`rationale`, `evidenceRefs`, and `confidence`.

Rejected operation shapes include `rawUnifiedDiff`, `fullFileReplacement`,
`shellCommand`, `gitCommand`, `networkFetch`, `providerCall`,
`packageManagerCommand`, `testRunnerCommand`, `buildToolCommand`, direct file
writes, forbidden target files, operations without
`expectedCurrentValueSha256`, and operations without `rationale` or
`evidenceRefs`.

Explicitly, model output must not contain direct file writes.

## Provenance

`SpecNodeProposalProvenance` must include `sourceJobDigest`,
`sourceBundleDigest`, `sourcePreviewPlanDigest`, `sourceArtifactDigests`,
`baseCandidateDigest`, `providerReceiptDigest`, `modelId`, `createdAt`,
`policyDigest`, `promptBudget`, `redactionPolicy`, and `schemaVersion`.

Provenance must point to digests and receipts, not model assertions.

## Usage Receipt

`SpecNodeProposalUsageReceipt` is required for both successful proposals and
rejections. It records `jobId`, `proposalId` or `rejectionId`,
`providerReceipt`, `providerReceiptDigest`, `modelId`, `inputTokens`,
`outputTokens`, `totalTokens`, `finishReason`, `attempts`, `startedAt`,
`completedAt`, `durationMs`, `timeoutPolicy`, `retryPolicy`, `temperature`,
`maxOutputTokens`, `promptBudget`, `responseSha256`, and `redactionPolicy`.

It may reference `SpecNodeProviderUsageReceipt`, but it must not persist raw
prompts, raw responses, secrets, or provider logs unless a later contract
defines a bounded redacted artifact.

## Rejection Reason

`SpecNodeRejectionReason` is returned when SpecNode cannot safely produce a
proposal.

Allowed rejection codes are `insufficient_evidence`, `prompt_budget_exceeded`,
`provider_unavailable`, `model_output_invalid`, `policy_violation`,
`unsupported_candidate_shape`, `schema_validation_failed`, and
`safety_boundary_triggered`.

Required fields are `kind: SpecNodeRejectionReason`, `rejectionId`, `code`,
`message`, `sourceJobDigest`, `sourcePreviewPlanDigest`, `evidenceRefs`, and
`usageReceipt`.

## Validation Before Apply

SpecHarvester must reject output before any local edit when output is not valid
JSON-compatible data, `kind` is not `SpecNodeRefinementResult`, the result has
neither or both `candidatePatchProposal` and `rejectionReason`, `usageReceipt`
is missing, provenance is incomplete, digests do not match, operations target
forbidden files or pointers, operations lack `expectedCurrentValueSha256`, or
the output asks for shell, filesystem, Git, provider, package manager, test,
build, or network behavior.

After a human accepts a proposal and SpecHarvester applies the corresponding
local edit, SpecHarvester must rerun SpecPM validation before any promotion or
accepted-source proposal.

## References

- `docs/SPECNODE_PATCH_PROPOSAL_CONTRACT.md`
- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeRefinePreviewContract>
- <doc:SpecNodeProviderAdapterContract>
- <doc:Workflow>
- <doc:TrustBoundary>
