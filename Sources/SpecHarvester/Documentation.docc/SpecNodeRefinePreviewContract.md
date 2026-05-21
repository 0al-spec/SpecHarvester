# SpecNode Refine Preview Contract

`refine-preview` is the deterministic planning step that prepares compact model
input for future SpecNode-assisted candidate refinement.

It does not execute models. It converts a
`SpecHarvesterSpecNodeArtifactBundle` into a
`SpecHarvesterRefinePreviewPlan`, which can later be embedded in a
`SpecNodeRefinementJob`.

## Contract Names

- `SpecHarvesterRefinePreviewPlan`: deterministic preview plan produced before
  any provider is called.
- `compactModelInput`: bounded model context derived from deterministic
  artifacts.
- `promptBudget`: hard size and truncation policy for weak-model input.
- `artifactDigests`: digest records tying compact summaries back to candidate
  artifacts.

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

## Inputs

Required artifacts are `harvest.json`, `specpm.yaml`, every referenced
`specs/*.spec.yaml`, and the `ProjectProfile` captured in the harvest
snapshot. Optional artifacts include `public-interface-index.json`,
`batch-validation.json`,
`governance-claims.json`, `namespace-upstream.json`,
`license-provenance.json`, `smoke-triage.json`, accepted-candidate diff
reports, accepted-candidate impact classification reports, and accepted package
update proposal metadata.

Every used artifact must be recorded in `artifactDigests`.

The OpenAI-compatible provider adapter boundary is defined separately in
<doc:SpecNodeProviderAdapterContract>.
That later boundary names `SpecNodeOpenAICompatibleProviderAdapter`, but this
preview contract still does not contact providers.
Schema-validated model output is defined separately in
<doc:SpecNodePatchProposalContract>.

## Compact Model Input

`harvestSummary` includes source repository metadata, pinned revision, collector
policy, file counts, skipped-file counts, package-manifest counts,
license-file counts, and evidence references. It does not include raw file
contents.

`projectProfile` includes languages, ecosystems, manifest paths, analyzer plan
IDs, analyzer plan statuses, confidence, evidence paths, and diagnostics.

`publicInterfaceSummary` is derived from optional `PublicInterfaceIndex`. It may
include analyzer metadata, summary counts, package IDs, entrypoint paths,
selected public symbol names, symbol kinds, signatures when already present,
diagnostics, and evidence digests. It must not include source bodies.

`semanticEvidenceIndex` includes deterministic semantic clusters already present
in BoundarySpec evidence: cluster IDs, intent IDs, labels, matched terms,
evidence paths, evidence kinds, scores, and support targets. It must keep
`documentationBodies: excluded`.

`validationSummaries` includes compact status, warning, error, and issue counts
from SpecPM validation, batch validation, duplicate claim, namespace/upstream,
license/provenance, smoke triage, accepted-candidate diff, and impact reports.

`draftCandidateMetadata` includes package ID, version, name, summary, license,
license evidence source, spec paths, provided capabilities, provided intents,
inbound interface IDs, evidence IDs, provenance source revision, and foreign
artifact references.

## Budget And Exclusions

`promptBudget` requires `maxPromptBytes`, `maxPromptTokens`,
`maxPublicSymbols`, `maxSemanticClusters`, `truncationPolicy`, and
`redactionPolicy`.

The planner must truncate in deterministic priority order and report
`truncationNotes` when implementation is added.

The plan must declare `rawRepositorySource: excluded`,
`documentationBodies: excluded`, `dependencyDirectories: excluded`,
`providerLogs: excluded`, `secrets: excluded`, and
`arbitraryPrompts: excluded`.

The planner must not include raw repository source, raw documentation bodies,
dependency directories, package manager caches, `.git/` content, environment
dumps, local credentials, SSH keys, access tokens, provider logs, or arbitrary
operator prompts outside the typed contract.

## Authority Policy

The plan repeats the parent SpecNode boundary:

- `modelFilesystemAccess: none`
- `modelShellAccess: none`
- `rawSourceAccess: none`
- `secretAccess: none`
- `candidateMutation: proposal_only`

`refine-preview` planning does not execute models, run shell commands, mutate
candidate files, call package managers, run tests, run build tools, contact
model providers, or perform network fetches. It is a deterministic local planning step.

## Rejection Conditions

Reject the plan if required artifacts are missing, artifact paths are absolute
or outside the workspace, paths are symlinked, digests do not match,
`harvest.json` is not a `SpecHarvesterEvidenceSnapshot`, required
`compactModelInput` sections are missing, excluded content appears, authority
policy is weaker than `none` or `proposal_only`, prompt budget fields are
missing, or truncation would remove candidate identity, source revision, or
validation status.

## References

- `docs/SPECNODE_REFINE_PREVIEW_CONTRACT.md`
- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeProviderAdapterContract>
- <doc:SpecNodePatchProposalContract>
- <doc:SpecNodeProviderSmokeCoverage>
- <doc:Workflow>
- <doc:TrustBoundary>
