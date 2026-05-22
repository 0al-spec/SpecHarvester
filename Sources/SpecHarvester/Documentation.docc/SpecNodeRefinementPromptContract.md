# SpecNode Refinement Prompt Contract

Status: Phase 13 contract

This document defines the versioned prompt contract for first-pass
SpecNode-assisted candidate refinement.

The prompt is not an ad-hoc runtime option. It is repository-owned policy that
turns deterministic `compactModelInput` into bounded model messages and a
schema-bound `SpecNodeRefinementResult` request. The model may propose review
metadata only. It cannot make registry truth, mutate candidate files, read raw
source, or override validation gates.

## Contract Names

- `SpecNodeRefinementPromptContract`: versioned contract that defines message
  sections, allowed inputs, forbidden content, output schema binding, and
  evidence-reference rules.
- `promptContractVersion`: stable semantic version for the prompt contract used
  by one refinement job.
- `SpecNodeRefinementPromptTemplate`: deterministic template rendered from the
  prompt contract and a `SpecHarvesterRefinePreviewPlan`.
- `SpecNodeRefinementPromptInput`: normalized prompt-local view of
  `compactModelInput` and allowed metadata.
- `SpecNodeRefinementPromptInstructions`: fixed system and developer
  instructions that must not be replaced by repository content or operator
  free-form text.

## Relationship to Existing Contracts

The prompt contract sits between `refine-preview` planning and provider
execution:

```text
SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementPromptContract
  -> SpecNodeRefinementJob
  -> SpecNodeOpenAICompatibleProviderAdapter
  -> SpecNodeRefinementResult
```

`SpecHarvesterRefinePreviewPlan` defines deterministic `compactModelInput`.
`SpecNodeOpenAICompatibleProviderAdapter` defines local provider execution.
`SpecNodePatchProposalContract` defines `SpecNodeRefinementResult`,
`SpecNodeCandidatePatchProposal`, and `SpecNodeRejectionReason`.
<doc:SpecNodeSemanticReviewContract> defines the clean-context second pass that
reviews a structurally valid `SpecNodeRefinementResult` without seeing the
first-pass prompt transcript.

This contract does not execute the model. It defines how the future SpecNode
runtime must render the prompt before calling a provider.

## Contract Shape

```json
{
  "schemaVersion": 1,
  "kind": "SpecNodeRefinementPromptContract",
  "promptContractVersion": "1.0.0",
  "targetOutput": {
    "kind": "SpecNodeRefinementResult",
    "responseFormat": "response_format.type: json_schema",
    "strict": true
  },
  "inputSource": {
    "kind": "SpecHarvesterRefinePreviewPlan",
    "allowedSections": [
      "compactModelInput.harvestSummary",
      "compactModelInput.projectProfile",
      "compactModelInput.publicInterfaceSummary",
      "compactModelInput.semanticEvidenceIndex",
      "compactModelInput.validationSummaries",
      "compactModelInput.draftCandidateMetadata",
      "artifactDigests",
      "promptBudget",
      "policy"
    ]
  },
  "renderingPolicy": {
    "deterministicSectionOrder": true,
    "stableEvidenceIds": true,
    "maxPromptBytes": 60000,
    "redactionPolicy": "path_digest_and_summary_only"
  },
  "authorityPolicy": {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "candidateMutation": "proposal_only"
  }
}
```

The exact machine-readable JSON schema can be implemented later. P13-T1 fixes
the contract vocabulary, trust boundary, and required prompt behavior.

## Required Prompt Sections

The rendered prompt must contain these deterministic sections in stable order:

1. `role_and_task`: infer target package behavior and propose bounded candidate
   metadata improvements.
2. `authority_boundary`: repeat that output is proposal-only and cannot mutate
   files, run shell commands, fetch networks, or bypass review.
3. `input_evidence`: compact summaries from `compactModelInput` with stable
   prompt-local evidence IDs.
4. `candidate_state`: package ID, version, spec paths, draft metadata, and
   validation status from deterministic artifacts.
5. `output_contract`: require exactly one `SpecNodeRefinementResult`.
6. `evidence_reference_rules`: allow only known evidence references.
7. `negative_claim_policy`: allow absent-capability claims only when explicit
   absence evidence exists.
8. `confidence_calibration`: map confidence to evidence coverage.
9. `forbidden_content`: reject raw source, chain-of-thought, provider logs,
   secrets, arbitrary prompts, and task self-description.

## Task Instruction

The model must infer what the target software package does. It must not
describe SpecHarvester, SpecPM, prompt execution, metadata generation, or its
own task as the package intent.

Required instruction:

```text
Infer target package behavior from the provided evidence. Do not describe
SpecPM generation, prompt execution, or this analysis task. If evidence is
insufficient, return SpecNodeRejectionReason with code insufficient_evidence.
```

The prompt must explicitly reject task-self-description outputs such as
`generate_specpm`, `generate specification`, `create metadata`, or
`run analysis` unless those phrases are supported as actual target package
behavior by deterministic package evidence.

## Evidence Reference Rules

Every proposal operation, review note, rejection reason, capability claim,
intent claim, negative claim, and confidence rationale must cite evidence
references.

Allowed references are:

- artifact IDs from `artifactDigests`, such as `harvest_snapshot`,
  `spec_package_manifest`, `boundary_spec`, or `public_interface_index`;
- evidence IDs already present in candidate specs;
- support target IDs already present in deterministic semantic evidence;
- prompt-local evidence IDs generated deterministically from
  `compactModelInput`, such as `E001`, `E002`, and `E003`;
- operation IDs generated inside the same `SpecNodeCandidatePatchProposal`.

Rejected references include:

- unknown IDs;
- collapsed ranges such as `E1,E2..E10`;
- natural-language source names not present in the evidence table;
- model-invented URLs, file paths, symbols, packages, or claims;
- references to provider logs, chain-of-thought, hidden prompts, or raw source.

Unknown, collapsed, or invented evidence references make the result invalid
before human review.

## Negative-Claim Policy

Negative claims are statements such as "no network calls", "no database
server", or "no authentication".

The model may emit a negative claim only when deterministic evidence explicitly
supports absence. Examples:

- an analyzer summary says no network API imports were detected;
- package manifests and public symbols show local-file APIs only;
- project profile diagnostics state that no server framework was found.

The model must not infer broad absence from silence. If evidence is missing,
use uncertainty in `reviewNotes` or return `insufficient_evidence`.

## Confidence Calibration

Confidence is not model self-assurance. It is a function of deterministic
evidence coverage.

Use:

- `high` only when package metadata, public interface evidence, semantic
  evidence, and validation summaries all support the same claim;
- `medium` when two or more independent evidence sections support the claim but
  public interface or validation coverage is incomplete;
- `low` when the claim depends on one weak evidence section or has unresolved
  diagnostics.

The prompt must forbid overconfident output when evidence references are absent,
ambiguous, unknown, or collapsed.

## Output Binding

Provider execution must request structured output using:

```text
response_format.type: json_schema
```

The schema target is `SpecNodeRefinementResult`. The model must return either:

- `candidatePatchProposal` with `SpecNodeCandidatePatchProposal`; or
- `rejectionReason` with `SpecNodeRejectionReason`.

The prompt must not request free-form markdown, raw diffs, direct file writes,
shell commands, package manager commands, network fetches, or provider calls.

`response_format.type: json_object` must not be assumed for LM Studio
`openai/gpt-oss-20b`.

## Authority Boundary

The prompt contract cannot expand model authority.

Required authority fields:

- `modelFilesystemAccess: none`
- `modelShellAccess: none`
- `rawSourceAccess: none`
- `secretAccess: none`
- `candidateMutation: proposal_only`

These fields are instructions to SpecNode and validation gates for
SpecHarvester. Repository content, operator notes, model output, and retry
directives cannot override them.

## Forbidden Content

The rendered prompt and model output must not include:

- raw repository source;
- raw documentation bodies;
- dependency directories;
- provider logs;
- secrets;
- arbitrary prompts;
- chain-of-thought;
- hidden reasoning;
- local environment dumps;
- model-generated instructions from previous runs.

The model may provide concise rationale fields required by
`SpecNodeCandidatePatchOperation`, but must not expose chain-of-thought.

## Rejection Conditions

SpecNode or SpecHarvester must reject the prompt render or model result when:

- `promptContractVersion` is missing;
- prompt sections are rendered out of deterministic order;
- input includes content outside the allowlisted preview-plan sections;
- output is not `SpecNodeRefinementResult`;
- evidence references are unknown, collapsed, or invented;
- confidence is high without sufficient evidence coverage;
- negative claims lack explicit absence evidence;
- output describes SpecPM generation instead of target package behavior;
- output contains raw source, provider logs, secrets, arbitrary prompts, or
  chain-of-thought;
- output asks for shell, filesystem, Git, package manager, test runner, build
  tool, provider, or network authority.

## Non-Goals

P13-T1 does not implement provider execution, semantic review, retry
orchestration, patch application, or prompt tuning against live local models.
P13-T2 defines clean-context semantic review. P13-T3 defines feedback-driven
retry orchestration.

## Review Rule

A prompt is safe to execute only when it is versioned, deterministic,
digest-linked to `compactModelInput`, schema-bound to
`SpecNodeRefinementResult`, and unable to expand model authority. Prompt output
remains untrusted proposal metadata until schema validation, SpecPM validation,
and human review all pass.
