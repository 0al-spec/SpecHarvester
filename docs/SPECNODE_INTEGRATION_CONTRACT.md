# SpecNode Integration Contract

Status: Phase 11 contract

This document defines the boundary between SpecHarvester and SpecNode for future
model-assisted candidate refinement.

SpecHarvester remains the deterministic evidence producer. SpecNode owns local
provider discovery, model execution, typed job policy, provenance, and usage
receipt generation. Model output is untrusted proposal metadata until
SpecHarvester validates it and a human reviewer accepts it.

## Contract Names

- `SpecHarvesterSpecNodeArtifactBundle`: the deterministic artifact bundle
  produced by SpecHarvester for one candidate refinement job.
- `SpecNodeRefinementJob`: the typed job envelope sent to SpecNode.
- `candidatePatchProposal`: a future schema-validated model output containing
  proposed candidate changes.
- `SpecNodeSemanticReviewJob`: the clean-context review job for a generated
  `SpecNodeRefinementResult`.
- `SpecNodeSemanticReviewResult`: typed semantic verdict and findings emitted
  after structural proposal validation.
- `usageReceipt`: a future SpecNode output containing provider/model identity,
  token usage, timing, and policy metadata.

## Ownership Split

SpecHarvester owns:

- collecting static evidence;
- drafting `specpm.yaml` and `specs/*.spec.yaml`;
- producing `harvest.json`, `ProjectProfile`, optional
  `PublicInterfaceIndex`, validation reports, governance reports, and smoke
  triage reports;
- building the `SpecHarvesterSpecNodeArtifactBundle`;
- validating returned proposal metadata before any local file mutation;
- keeping SpecPM validation and human review as required gates.

SpecNode owns:

- provider discovery and health checks;
- model execution;
- model timeout, retry, token-budget, temperature, and provider policy;
- provenance and `usageReceipt` generation;
- returning typed proposal output to SpecHarvester.

The model owns no authority. It cannot run shell commands, mutate files, read
secrets, read raw repository source, install dependencies, run package scripts,
or expand network access.

Explicitly: the model cannot read secrets or read raw repository source outside
the typed artifact bundle.

## Artifact Bundle

`SpecHarvesterSpecNodeArtifactBundle` is a reviewable JSON-compatible envelope.
It references files by relative path inside a candidate workspace and records
content digests for every file included in the job.

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterSpecNodeArtifactBundle",
  "candidateId": "flask.core",
  "candidateVersion": "0.1.0",
  "workspaceRoot": ".",
  "source": {
    "repository": "https://github.com/pallets/flask",
    "revision": "0123456789abcdef0123456789abcdef01234567"
  },
  "artifacts": [
    {
      "id": "harvest_snapshot",
      "path": "harvest.json",
      "required": true,
      "sha256": "64-hex-digest"
    },
    {
      "id": "spec_package_manifest",
      "path": "specpm.yaml",
      "required": true,
      "sha256": "64-hex-digest"
    },
    {
      "id": "boundary_spec",
      "path": "specs/flask.spec.yaml",
      "required": true,
      "sha256": "64-hex-digest"
    }
  ],
  "policy": {
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "candidateMutation": "proposal_only"
  }
}
```

Required artifacts:

- `harvest.json`
- `specpm.yaml`
- every referenced `specs/*.spec.yaml`

Optional artifacts:

- `public-interface-index.json`
- `batch-validation.json`
- `governance-claims.json`
- `namespace-upstream.json`
- `license-provenance.json`
- `smoke-triage.json`
- accepted-candidate diff reports
- accepted-candidate impact classification reports
- accepted package update proposal metadata

Forbidden artifacts:

- raw repository source trees;
- `.git/` content;
- package manager caches;
- dependency directories such as `node_modules/`, `.build/`, `vendor/`, or
  virtual environments;
- local secrets, credentials, private configuration, SSH keys, tokens, and
  environment dumps;
- generated provider logs that contain prompt or secret material not selected by
  the typed job.

## Bundle Validation Rules

SpecHarvester must reject the bundle before handoff if any rule fails:

- every artifact path is relative;
- no artifact path escapes the candidate workspace;
- no artifact path is a symlink;
- every `sha256` is computed from the exact bytes sent to SpecNode;
- every required artifact exists;
- `harvest.json` has `kind: SpecHarvesterEvidenceSnapshot`;
- `specpm.yaml` is present for the candidate;
- `modelFilesystemAccess: none`;
- `modelShellAccess: none`;
- `candidateMutation: proposal_only`;
- `rawSourceAccess: none`;
- `secretAccess: none`.

These checks are deterministic and do not require a model provider.

## Typed Job Envelope

`SpecNodeRefinementJob` is the only message SpecHarvester sends to SpecNode for
candidate refinement.

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeRefinementJob",
  "jobId": "01HY0000000000000000000000",
  "createdAt": "2026-05-21T00:00:00Z",
  "producer": {
    "name": "SpecHarvester",
    "version": "0.1.0"
  },
  "bundle": {
    "kind": "SpecHarvesterSpecNodeArtifactBundle",
    "digest": "sha256:64-hex-digest"
  },
  "policy": {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "modelNetworkAccess": "provider_only",
    "allowedTools": [],
    "candidateMutation": "proposal_only",
    "temperature": 0.2,
    "tokenBudget": 8192,
    "timeoutSeconds": 120
  },
  "requestedOutputs": [
    "candidatePatchProposal",
    "reviewNotes",
    "rejectionReason",
    "usageReceipt"
  ]
}
```

Job policy rules:

- `modelFilesystemAccess: none` means the model receives serialized artifact
  content through SpecNode only; it never receives filesystem handles.
- `modelShellAccess: none` means the model cannot invoke shell commands,
  package managers, tests, build tools, or analyzers.
- `modelNetworkAccess: provider_only` means SpecNode may contact the configured
  model provider, but the model cannot request new network fetches or browse
  upstream repositories.
- `allowedTools: []` means no LLM tool calls are exposed for this job class.
- `candidateMutation: proposal_only` means SpecNode returns proposed edits as
  data. It cannot write candidate files directly.

## Output Authority

SpecNode may return only typed outputs requested by the job. P11-T1 names these
output kinds; later tasks define their final schemas.

Allowed output kinds:

- `candidatePatchProposal`
- `reviewNotes`
- `rejectionReason`
- `usageReceipt`

Forbidden output behavior:

- direct writes to `specpm.yaml` or `specs/*.spec.yaml`;
- direct promotion into accepted source;
- direct SpecPM publication;
- shell, Git, filesystem, package manager, test runner, build tool, or network
  actions requested by model text;
- treating model assertions as accepted registry truth.

SpecHarvester must validate proposed output, show it for review, and rerun
SpecPM validation before any accepted-source proposal.

## Handoff Sequence

1. SpecHarvester drafts a candidate from deterministic evidence.
2. SpecHarvester validates candidate structure and optional review reports.
3. SpecHarvester builds a `SpecHarvesterSpecNodeArtifactBundle`.
4. SpecHarvester creates a `SpecNodeRefinementJob` with explicit policy.
5. SpecNode executes the configured model under that policy.
6. SpecNode returns proposal metadata and `usageReceipt`.
7. SpecHarvester validates the proposal schema.
8. A human reviewer decides whether to apply, reject, or rewrite the proposal.
9. SpecHarvester reruns SpecPM validation after any accepted local edit.

## Rejection Conditions

SpecHarvester should reject a job or returned proposal when:

- bundle digests do not match;
- paths are absolute, symlinked, or outside the workspace;
- forbidden artifacts are present;
- policy does not declare `modelFilesystemAccess: none` and
  `modelShellAccess: none`;
- output contains file writes instead of a proposal;
- output references artifacts not present in the bundle;
- output asks to run commands, fetch dependencies, browse the network, or use
  secrets;
- output lacks a `usageReceipt` once SpecNode support is implemented.

## Compatibility With Later Phase 11 Tasks

This contract intentionally leaves implementation details to later tasks:

- `P11-T2` defines the concrete `refine-preview` planning contract in
  [`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md).
  It emits a deterministic `SpecHarvesterRefinePreviewPlan` with
  `compactModelInput` derived from trusted local artifacts before any provider
  adapter is contacted.
- `P11-T3` defines the OpenAI-compatible provider adapter and LM Studio
  discovery boundary in
  [`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md).
  It fixes `SpecNodeOpenAICompatibleProviderAdapter`,
  `SpecNodeProviderHealth`, `SpecNodeModelListing`,
  `SpecNodeGenerationPolicy`, `SpecNodeProviderUsageReceipt`,
  `timeoutPolicy`, `retryPolicy`, `temperature`, `maxOutputTokens`, and
  `promptBudget` without granting provider execution authority to
  SpecHarvester.
- `P11-T4` defines schema-validated patch proposal output in
  [`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md).
  It fixes `SpecNodeCandidatePatchProposal`,
  `SpecNodeCandidatePatchOperation`, `SpecNodeProposalProvenance`,
  `SpecNodeProposalUsageReceipt`, `SpecNodeRejectionReason`, `reviewNotes`,
  `usageReceipt`, and validation-before-apply rules.
- `P11-T5` adds integration smoke coverage with deterministic fallback in
  [`SPECNODE_PROVIDER_SMOKE_COVERAGE.md`](SPECNODE_PROVIDER_SMOKE_COVERAGE.md).
  It fixes `SpecNodeProviderSmokeRun`, local SpecNode-compatible provider stub
  coverage, structural `SpecNodeRefinementResult` validation, compact
  weak-model drafting input checks, and the `provider_unavailable` fallback.
- `P13-T2` defines clean-context semantic review in
  [`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md).
  It fixes `SpecNodeSemanticReviewJob`, `SpecNodeSemanticReviewRubric`,
  `SpecNodeSemanticReviewResult`, typed `SpecNodeSemanticReviewFinding`
  records, verdicts, evidence-reference rules, and review-only mutation
  boundaries.
- `P13-T3` defines feedback-driven retry orchestration in
  [`SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md`](SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md).
  It fixes `SpecNodeRefinementRetryRun`,
  `SpecNodeRefinementRetryPolicy`, `SpecNodeRefinementRetryAttempt`,
  `SpecNodeRetryDirectiveSet`, `SpecNodeRetryDirective`,
  `SpecNodeRetryContext`, immutable artifact reuse, max-attempt caps, and audit
  trail validation.

The compatibility rule is stable: model-assisted refinement consumes compact
deterministic artifacts instead of raw repository source dumps.

## Trust Boundary

SpecHarvester and SpecNode both preserve the same trust boundary:

- repository content is untrusted input;
- deterministic analyzer output is advisory untrusted evidence;
- model output is untrusted proposal metadata;
- SpecPM validation and human review remain required;
- package content can describe desired outputs, but package content cannot
  command the host.
