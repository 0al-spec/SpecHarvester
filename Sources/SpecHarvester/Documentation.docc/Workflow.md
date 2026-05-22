# Workflow

SpecHarvester turns public repository metadata into reviewable SpecPM candidate
packages through a controlled, review-first pipeline.

## End-to-End Flow

```text
public repository URL
        |
        v
local checkout at a pinned revision
        |
        v
collect-local
        |
        v
harvest.json
        |
        v
draft
        |
        v
specpm validate
        |
        v
human review
        |
        v
prepare-accepted-entry
        |
        v
promote
        |
        v
accepted package source
```

The current bootstrap supports the first controlled candidate loop:

```text
checkout -> harvest.json -> generated SpecPackage -> SpecPM validation -> promotion copy
```

## Current Commands

Collect static evidence:

```bash
python3 -m spec_harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/github.com/example/project
```

Validate batch repository source manifests without collecting snapshots:

```bash
python3 -m spec_harvester source-manifests inputs
```

See <doc:RepositorySourceManifests> for the supported `inputs/*.yml` schema.

Collect snapshots for all enabled manifest records with local checkouts:

```bash
python3 -m spec_harvester collect-batch inputs --out candidates
```

Collect selected repository IDs:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --select xyflow
```

This writes deterministic `candidates/<repository-id>/harvest.json` paths. See
<doc:BatchCollection>.

Write a batch validation report:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

The report records confidence, policy notes, warning codes, and skipped records.
See <doc:BatchValidationReports>.

Optionally emit built-in static public interface indexes before drafting:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --emit-interface-indexes \
  --analyzer-cache-dir candidates/.analyzer-cache
```

This consumes `ProjectProfile.analyzerPlan` from each `harvest.json` and writes
`candidates/<repository-id>/public-interface-index.json` when a supported
built-in analyzer is recommended. Supported analyzer plan ids are
`spec_harvester.python_public_api`, `spec_harvester.js_ts_public_api`, and
`spec_harvester.go_public_api`.
Analyzer orchestration still does not install dependencies, run package
managers, run package scripts, execute checkout files, or contact networks.

Draft a reviewable candidate package:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --out candidates/github.com/example/project
```

If a static analyzer has already emitted a `PublicInterfaceIndex`, either rely
on auto-detection beside `harvest.json` or pass it to the drafter to enrich
`interfaces.inbound` with package, entrypoint, and symbol summaries:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --interface-index candidates/github.com/example/project/public-interface-index.json \
  --out candidates/github.com/example/project
```

The drafter validates the index, writes a normalized
`public-interface-index.json` artifact into the candidate directory, and records
it as BoundarySpec evidence. It does not run analyzers during drafting.

The BoundarySpec evidence record for this artifact uses
`kind: public_interface_index`, which is recognized by SpecPM `0.2.0+`, and
includes `artifactKind: SpecHarvesterPublicInterfaceIndex`, `mediaType`,
`schemaVersion`, and `summary` so reviewers can identify the deterministic
artifact contract without opening the JSON first.

`PublicInterfaceIndex.summary.status` is preserved as review metadata:
`complete` means no diagnostics were emitted, `partial` means diagnostics were
emitted while package evidence remains available, and `failed` means diagnostics
were emitted without any package record.

For manifest-poor repositories, `collect-local` may also record compact
`semanticHints` from allowlisted README, API contract, OpenAPI, schema
validation, workflow automation, developer tooling, web framework, or
documentation knowledge base Markdown. `draft` can use those hints as
`semantic_intent_static_evidence` for reviewable intent IDs such as
`intent.web.framework_surface`, `intent.web.http_routing`,
`intent.api.contract_surface`, `intent.metadata.schema_validation`,
`intent.workflow.automation_pipeline`, and
`intent.developer.tooling_surface`. This does not store raw documentation
bodies, run package scripts, execute checkout files, or contact networks.

`draft` can also normalize `PublicInterfaceIndex` symbols such as
`RouterGroup`, `HandlerFunc`, `RequestContext`, and `Blueprint` into compact
semantic tokens for web framework intent evidence without reading raw source
bodies.

Semantic evidence `supports` entries are constrained to declared SpecPM support
targets: `intent.summary`, `provides.capabilities`, and
`provides.capabilities.<capability_id>`. The drafter does not emit
`provides.capabilities.intentIds` because nested `intentIds` is not part of the
current SpecPM BoundarySpec support-target grammar.

raw documentation bodies remain excluded from generated evidence artifacts.

See <doc:LanguageNeutralSemanticExtraction>.

Prepare a deterministic manifest entry for a reviewed candidate:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest accepted/accepted-packages.yml
```

This command:

- derives `packageId` and `packageVersion` from `specpm.yaml`;
- infers `public-index/generated/<packageId>/<version>` as the default entry path;
- updates the accepted manifest deterministically.

Follow the immutability policy before proposing any accepted update:

- never mutate an accepted `<packageId>/<packageVersion>` path directly;
- publish updates as new accepted version paths, including metadata-only
  corrections.

Required audit fields for each proposal include source revision, evidence digests,
old/new package version, changed claims, validation status, and reviewer notes.
See <doc:AcceptedPackageUpdateLifecycle>.

Compare accepted and candidate metadata before update proposal work:

```bash
python3 -m spec_harvester accepted-candidate-diff-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-diff.json
```

See <doc:AcceptedCandidateDiffReports>.

Classify update impact before proposal triage:

```bash
python3 -m spec_harvester accepted-candidate-impact-classification-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-impact-classification.json
```

See <doc:AcceptedCandidateImpactClassificationReports>.

Build a PR-ready accepted-package update artifact:

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  candidates/github.com/example/project \
  --accepted-root accepted \
  --output candidates/accepted-package-update-proposal.json \
  --proposal-body candidates/accepted-package-update-proposal.md
```

See <doc:AcceptedPackageUpdateProposals>.

Promote a reviewed candidate into accepted-source staging:

```bash
python3 -m spec_harvester promote candidates/github.com/example/project \
  --accepted-root accepted \
  --manifest accepted/accepted-packages.yml
```

Build a duplicate governance claim report for accepted and candidate metadata:

```bash
python3 -m spec_harvester governance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/governance-claims.json
```

The report summarizes overlapping `intent.*` and `capability` claims for review
prioritization before proposal and promotion.

Build a namespace/upstream relationship review report:

```bash
python3 -m spec_harvester governance-upstream-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/namespace-upstream.json
```

This report highlights namespace collisions, missing `upstream_repository`
artifacts, and namespace-vs-upstream-owner mismatches.

Build a license and provenance risk review report:

```bash
python3 -m spec_harvester governance-license-provenance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/license-provenance-risk.json
```

The report highlights missing/standardized license metadata and upstream
provenance risks.

## Review Gates

Every generated candidate should be checked for:

- exact source provenance and pinned revision;
- bounded metadata extraction only;
- conservative package naming and inferred intent/capability language;
- successful `specpm validate` output;
- explicit maintainer review before promotion.

## Future SpecNode Refinement

Future model-assisted refinement must use <doc:SpecNodeIntegrationContract>.
SpecHarvester prepares a `SpecHarvesterSpecNodeArtifactBundle` and sends it in
a typed `SpecNodeRefinementJob`. The job policy keeps
`modelFilesystemAccess: none`, `modelShellAccess: none`, and
`candidateMutation: proposal_only`.

Before that handoff, `refine-preview` planning must follow
<doc:SpecNodeRefinePreviewContract>. It produces a
`SpecHarvesterRefinePreviewPlan` with `compactModelInput` derived from
`harvest.json`, `ProjectProfile`, optional `PublicInterfaceIndex`,
`semanticEvidenceIndex`, validation summaries, and draft candidate metadata.
It excludes raw repository source and raw documentation bodies.

Prompt rendering must follow <doc:SpecNodeRefinementPromptContract>. The
`SpecNodeRefinementPromptContract` keeps prompt text versioned, requires
target-package intent inference instead of task self-description, and rejects
unknown evidence references, unsupported negative claims, and overconfident
claims without deterministic evidence.

Clean-context semantic review must follow <doc:SpecNodeSemanticReviewContract>.
After structural `SpecNodeRefinementResult` validation, a second model may see
only deterministic evidence, the generated candidate or patch proposal, and a
fixed `SpecNodeSemanticReviewRubric`. It emits `approve`, `needs_revision`, or
`reject` with typed `SpecNodeSemanticReviewFinding` records for issues such as
`wrong_package_intent`, `unsupported_capability_claim`,
`missing_evidence_reference`, `overconfident_confidence_score`,
`unsafe_negative_claim`, `schema_policy_mismatch`, and
`authority_boundary_violation`. The semantic review pass cannot emit patch
operations, retry directives, shell commands, network fetches, provider calls,
or direct file writes.

Provider execution must follow <doc:SpecNodeProviderAdapterContract>. SpecNode
may use `SpecNodeOpenAICompatibleProviderAdapter` for LM Studio or other
OpenAI-compatible local providers, but only through explicit or
`localhost_only` discovery, `/v1/models`, `/v1/chat/completions`,
`timeoutPolicy`, `retryPolicy`, `temperature`, `maxOutputTokens`, and
`promptBudget`. SpecHarvester does not contact providers.

SpecNode output is proposal metadata such as `candidatePatchProposal`,
`reviewNotes`, `rejectionReason`, and `usageReceipt`. SpecHarvester validates
the proposal and reruns SpecPM validation after any accepted edit.

Patch proposal output must follow <doc:SpecNodePatchProposalContract>. SpecNode
may return `SpecNodeCandidatePatchProposal` with structured operations or
`SpecNodeRejectionReason` when no safe proposal can be produced. SpecHarvester
rejects raw diffs, direct file writes, shell commands, provider calls, missing
`usageReceipt`, and proposals without provenance or digest binding.

Executable smoke coverage follows <doc:SpecNodeProviderSmokeCoverage>. The
`SpecNodeProviderSmokeRun` harness builds compact weak-model drafting input
from deterministic artifacts, validates `SpecNodeRefinementResult`, and uses a
deterministic `provider_unavailable` fallback when no local
SpecNode-compatible provider is configured. The smoke path does not contact LM
Studio, execute a model, apply patches, or mutate candidate files.

## References

- `docs/HOW_IT_WORKS.md`
- `README.md`
- <doc:TrustBoundary>
- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeRefinePreviewContract>
- <doc:SpecNodeProviderAdapterContract>
- <doc:SpecNodePatchProposalContract>
- <doc:SpecNodeProviderSmokeCoverage>
- <doc:RepositorySourceManifests>
- <doc:BatchCollection>
- <doc:BatchValidationReports>
- <doc:AcceptedManifestEntries>
- <doc:AcceptedPackageUpdateLifecycle>
- <doc:AcceptedCandidateDiffReports>
- <doc:AcceptedCandidateImpactClassificationReports>
- <doc:AcceptedPackageUpdateProposals>
- <doc:ProposalAutomation>
