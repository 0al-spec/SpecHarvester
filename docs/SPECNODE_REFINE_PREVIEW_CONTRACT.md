# SpecNode Refine Preview Contract

Status: Phase 11 contract

This document defines the deterministic `refine-preview` planning contract for
future SpecNode-assisted candidate refinement.

`refine-preview` is a planning step, not model execution. It converts a
reviewable `SpecHarvesterSpecNodeArtifactBundle` into a compact model input
plan that can later be embedded in a `SpecNodeRefinementJob`.

## Contract Names

- `SpecHarvesterRefinePreviewPlan`: deterministic preview plan produced by
  SpecHarvester before any SpecNode provider is called.
- `compactModelInput`: bounded, serialized model context derived from
  deterministic artifacts.
- `promptBudget`: hard size and truncation policy for weak-model input.
- `artifactDigests`: digest records tying every compact summary back to local
  candidate artifacts.

## Relationship to SpecNode Integration

`SpecHarvesterRefinePreviewPlan` is built on top of the
`SpecHarvesterSpecNodeArtifactBundle` defined in
[`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md).

The flow is:

```text
candidate workspace
  -> SpecHarvesterSpecNodeArtifactBundle
  -> SpecHarvesterRefinePreviewPlan
  -> SpecNodeRefinementJob, future
  -> candidatePatchProposal, future
```

SpecHarvester still owns deterministic evidence production and preview planning.
SpecNode owns provider discovery and model execution in later tasks.
The OpenAI-compatible provider adapter boundary is defined in
[`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md).
That later boundary names `SpecNodeOpenAICompatibleProviderAdapter`, but this
preview contract still does not contact providers.

## Plan Shape

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterRefinePreviewPlan",
  "command": "refine-preview",
  "sourceBundle": {
    "kind": "SpecHarvesterSpecNodeArtifactBundle",
    "digest": "sha256:64-hex-digest"
  },
  "candidate": {
    "packageId": "flask.core",
    "packageVersion": "0.1.0",
    "workspaceRoot": ".",
    "specPaths": ["specs/flask.spec.yaml"]
  },
  "artifactDigests": [
    {
      "id": "harvest_snapshot",
      "path": "harvest.json",
      "sha256": "64-hex-digest"
    },
    {
      "id": "spec_package_manifest",
      "path": "specpm.yaml",
      "sha256": "64-hex-digest"
    }
  ],
  "compactModelInput": {
    "harvestSummary": {},
    "projectProfile": {},
    "publicInterfaceSummary": {},
    "semanticEvidenceIndex": {},
    "validationSummaries": {},
    "draftCandidateMetadata": {}
  },
  "promptBudget": {
    "maxPromptBytes": 60000,
    "maxPromptTokens": 8192,
    "maxPublicSymbols": 200,
    "maxSemanticClusters": 50,
    "truncationPolicy": "deterministic_priority_order",
    "redactionPolicy": "path_digest_and_summary_only"
  },
  "excludedContent": {
    "rawRepositorySource": "excluded",
    "documentationBodies": "excluded",
    "dependencyDirectories": "excluded",
    "providerLogs": "excluded",
    "secrets": "excluded",
    "arbitraryPrompts": "excluded"
  },
  "policy": {
    "modelFilesystemAccess": "none",
    "modelShellAccess": "none",
    "rawSourceAccess": "none",
    "secretAccess": "none",
    "candidateMutation": "proposal_only"
  }
}
```

The exact JSON schema can be implemented later. P11-T2 fixes the contract
meaning and required fields.

## Required Inputs

`refine-preview` planning requires these candidate workspace artifacts:

- `harvest.json`
- `specpm.yaml`
- every referenced `specs/*.spec.yaml`

The planner must verify every required artifact by relative path and SHA-256
digest before producing `SpecHarvesterRefinePreviewPlan`.

## Optional Inputs

The planner may include compact summaries from:

- `public-interface-index.json`
- `batch-validation.json`
- `governance-claims.json`
- `namespace-upstream.json`
- `license-provenance.json`
- `smoke-triage.json`
- accepted-candidate diff reports
- accepted-candidate impact classification reports
- accepted package update proposal metadata

Optional inputs must still be represented in `artifactDigests` when used.

## Compact Model Input Sections

### harvestSummary

`harvestSummary` contains source repository metadata, pinned revision, collector
policy, file counts, skipped-file counts, package-manifest counts, license-file
counts, and allowlisted file evidence references.

It does not include raw file contents.

### projectProfile

`projectProfile` contains the deterministic `ProjectProfile` subset from
`harvest.json`: languages, ecosystems, manifest paths, analyzer plan IDs,
analyzer plan statuses, confidence, evidence paths, and diagnostics.

It is the primary package-type and language signal for weak-model refinement.

### publicInterfaceSummary

`publicInterfaceSummary` is derived from optional `PublicInterfaceIndex`.

It may include analyzer metadata, summary counts, package IDs, entrypoint paths,
selected public symbol names, symbol kinds, signatures when already present in
the index, diagnostics, and evidence digests.

It must not include source bodies or private implementation text.

### semanticEvidenceIndex

`semanticEvidenceIndex` includes deterministic semantic clusters already present
in candidate BoundarySpec evidence. It may include cluster IDs, intent IDs,
labels, matched terms, evidence paths, evidence kinds, scores, and support
targets.

It must keep `documentationBodies: excluded`. Matched terms and headings are
allowed only when already present in bounded static evidence.

### validationSummaries

`validationSummaries` includes compact status, warning, error, and issue counts
from available reports:

- SpecPM validation status, when present;
- batch validation report summary;
- duplicate claim report summary;
- namespace/upstream report summary;
- license/provenance report summary;
- smoke triage summary;
- accepted-candidate diff and impact summaries.

It must not include full generated report bodies unless they fit the
`promptBudget` and are explicitly allowlisted by future implementation.

### draftCandidateMetadata

`draftCandidateMetadata` includes candidate package ID, version, name, summary,
license, license evidence source, spec paths, provided capabilities, provided
intents, inbound interface IDs, evidence IDs, provenance source revision, and
foreign artifact references.

It is candidate metadata, not accepted registry truth.

## Prompt Budget and Deterministic Truncation

`promptBudget` is mandatory. It bounds weak-model input before SpecNode receives
the job.

Required fields:

- `maxPromptBytes`
- `maxPromptTokens`
- `maxPublicSymbols`
- `maxSemanticClusters`
- `truncationPolicy`
- `redactionPolicy`

When data exceeds the budget, the planner must truncate in deterministic
priority order:

1. keep candidate identity, source revision, policy, and validation status;
2. keep package languages, ecosystems, manifests, and analyzer plan statuses;
3. keep capability and intent IDs;
4. keep public interface summary counts and highest-priority symbols;
5. keep semantic clusters by score and stable ID order;
6. omit lower-priority diagnostics and long report details.

Truncation must be visible in the plan through a `truncationNotes` field when
implementation is added.

## Excluded Content

The plan must declare:

- `rawRepositorySource: excluded`
- `documentationBodies: excluded`
- `dependencyDirectories: excluded`
- `providerLogs: excluded`
- `secrets: excluded`
- `arbitraryPrompts: excluded`

The planner must not include raw repository source, raw documentation bodies,
dependency directories, package manager caches, `.git/` content, environment
dumps, local credentials, SSH keys, access tokens, provider logs, or arbitrary
operator prompts outside the typed contract.

## Authority Policy

The plan repeats the authority boundary required by the parent SpecNode
contract:

- `modelFilesystemAccess: none`
- `modelShellAccess: none`
- `rawSourceAccess: none`
- `secretAccess: none`
- `candidateMutation: proposal_only`

`refine-preview` planning does not execute models, run shell commands, mutate
candidate files, call package managers, run tests, run build tools, contact
model providers, or perform network fetches. It is a deterministic local planning step.

## Rejection Conditions

SpecHarvester must reject the plan when:

- required artifacts are missing;
- artifact paths are absolute, symlinked, or outside the candidate workspace;
- artifact digests do not match local bytes;
- `harvest.json` is not a `SpecHarvesterEvidenceSnapshot`;
- `specpm.yaml` or referenced specs are missing;
- required `compactModelInput` sections are missing;
- excluded content appears in the plan;
- authority policy is weaker than `none` or `proposal_only`;
- prompt budget fields are missing;
- truncation would remove candidate identity, source revision, or validation
  status.

## Non-Goals

P11-T2 does not implement the `refine-preview` command. It does not execute
SpecNode, call LM Studio, discover models, invoke OpenAI-compatible providers,
define the final `candidatePatchProposal` schema, or apply generated changes.
P11-T3 defines the future provider adapter boundary separately.

## Review Rule

A `SpecHarvesterRefinePreviewPlan` is safe to hand to SpecNode only when it is
derived from deterministic artifacts, budgeted, digest-linked, and free of
excluded content. Model output remains untrusted proposal metadata and still
requires schema validation, SpecPM validation after accepted edits, and human
review.
