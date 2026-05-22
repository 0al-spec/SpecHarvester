# SpecHarvester Architecture

Status: Bootstrap

SpecHarvester is a producer pipeline for candidate SpecPM packages.

```text
repository source list
        |
        v
safe evidence collector
        |
        v
evidence snapshot
        |
        v
deterministic candidate drafter
        |
        v
AI-assisted refinement, future
        |
        v
SpecPM validation
        |
        v
candidate review
        |
        v
controlled promotion
        |
        v
accepted registry source
```

## Components

### Safe Evidence Collector

Reads allowlisted static files from a public repository checkout and writes an
evidence snapshot. It does not execute package content.

Current command:

```bash
spec-harvester collect-local <repo> --out <candidate-dir>
```

For allowlisted Markdown, the collector can add bounded `semanticHints` for
language-neutral README, API contract, OpenAPI, schema validation, workflow
automation, developer tooling, and documentation knowledge base evidence. It
stores compact terms and file digests, not raw documentation bodies.

### Repository Source Manifest Reader

Reads operator-authored `inputs/*.yml` files and prints normalized repository
source records for later batch harvesting. It validates repository IDs, source
URLs, and pinned `revision` or `ref` metadata, but it does not clone
repositories or collect snapshots.

Current command:

```bash
spec-harvester source-manifests inputs
```

### Batch Snapshot Collector

Reads validated repository source records and collects `harvest.json` snapshots
from operator-managed local checkouts into deterministic candidate directories.
It uses the same allowlisted static file collector as `collect-local`.

Current command:

```bash
spec-harvester collect-batch inputs --out candidates
```

Outputs are written as:

```text
candidates/<repository-id>/harvest.json
```

The batch collector does not clone repositories, contact networks, install
dependencies, run package managers, run package scripts, execute checkout files,
or derive output paths from repository content.

### Batch Validation Reporter

Builds advisory `SpecHarvesterBatchValidationReport` JSON for `collect-batch`
output. Reports summarize confidence, policy notes, warning codes, evidence
counts, and skipped records for reviewer inspection.

Current command:

```bash
spec-harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

Report confidence is not an acceptance decision. It is review metadata that
helps maintainers decide what to inspect before drafting, validation, or
promotion.

### Deterministic Public Interface Analyzers

Extract compact `PublicInterfaceIndex` JSON from local source bytes without
executing package code. Python uses the standard-library `ast` module, and
JavaScript/TypeScript uses package manifest entrypoints plus static export
scanning.

Analyzers can use an optional per-file cache keyed by analyzer id, analyzer
version, and file SHA-256 digest. The cache is treated as derived untrusted
metadata and is ignored when metadata or path/evidence validation fails.

`PublicInterfaceIndex.summary.status` records static analysis coverage:
`complete` means no diagnostics were emitted, `partial` means diagnostics were
emitted while package evidence remains available for review, and `failed` means
diagnostics were emitted without any package record.

Analyzers that require metadata-only build tools are future optional
components. They must meet
[`ANALYZER_SANDBOX_REQUIREMENTS.md`](ANALYZER_SANDBOX_REQUIREMENTS.md) before
use.

`collect-batch --emit-interface-indexes` can opt in to analyzer orchestration
driven by `ProjectProfile.analyzerPlan`. The orchestrator runs only built-in
static analyzers with `recommended` plan status, currently Python `ast` and
JavaScript/TypeScript static export analysis, and deterministic Go source
public API analysis, then writes
`public-interface-index.json` beside `harvest.json`. Plans that are
`manifest_only` or unsupported are recorded as skipped. Supported plan ids are
`spec_harvester.python_public_api`, `spec_harvester.js_ts_public_api`, and
`spec_harvester.go_public_api`; their output remains advisory review evidence.

### Deterministic Candidate Drafter

Consumes evidence snapshots and drafts `specpm.yaml` plus
`specs/*.spec.yaml`. It can also consume a precomputed
`PublicInterfaceIndex` JSON artifact and copy it into the candidate output as
`public-interface-index.json`.

The deterministic draft is intentionally conservative. It records observed
package metadata, inferred capability IDs, inferred `intent.*` IDs, provenance,
review constraints, and analyzer-backed inbound interface summaries when a
valid public interface index is provided. It does not claim upstream
endorsement.

When a `PublicInterfaceIndex` is present, BoundarySpec evidence keeps
`kind: public_interface_index`, which is recognized by SpecPM `0.2.0+`, and
adds explicit artifact metadata: `artifactKind: SpecHarvesterPublicInterfaceIndex`,
`mediaType`, `schemaVersion`, and
`summary`. Older SpecPM validators may warn on that evidence kind; current
public-interface candidates should be checked with SpecPM `0.2.0+`.

When no supported package manifest exists, the drafter may use documentation
`semanticHints` as advisory `semantic_intent_static_evidence`. Language-neutral
clusters such as `web.framework_surface`, `web.http_routing`,
`api.contract_surface`, `metadata.schema_validation`,
`workflow.automation_pipeline`, and `developer.tooling_surface` can replace the
generic metadata fallback while remaining review evidence, not registry truth.
For supported package manifests, only stronger domain clusters such as Swift/iOS
or web framework clusters replace generic manifest intent IDs; broad API or
tooling clusters remain advisory evidence.

Current command:

```bash
spec-harvester draft <harvest-dir-or-json> \
  --interface-index <public-interface-index.json> \
  --out <candidate-dir>
```

If no explicit index path is provided, the drafter only auto-detects
`public-interface-index.json` or `public_interface_index.json` beside
`harvest.json`. It does not run analyzers or inspect raw repository source
during drafting.

### AI Draft Generator

Future component. It may refine deterministic candidates using a bounded
SpecNode job. The handoff contract is
[`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md).
The compact planning contract is
[`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md).
The versioned prompt contract is
[`SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`](SPECNODE_REFINEMENT_PROMPT_CONTRACT.md).
The clean-context semantic review contract is
[`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md).
The provider adapter contract is
[`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md).
The patch proposal output contract is
[`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md).
Executable smoke coverage is described in
[`SPECNODE_PROVIDER_SMOKE_COVERAGE.md`](SPECNODE_PROVIDER_SMOKE_COVERAGE.md).

SpecHarvester must send only a `SpecHarvesterSpecNodeArtifactBundle` inside a
typed `SpecNodeRefinementJob`. The job policy keeps
`modelFilesystemAccess: none`, `modelShellAccess: none`, and
`candidateMutation: proposal_only`. SpecNode may return
`candidatePatchProposal`, `reviewNotes`, `rejectionReason`, and `usageReceipt`
metadata. Model output remains untrusted candidate metadata and must be
validated and reviewed before acceptance.

Before any model provider is contacted, `refine-preview` planning may produce a
`SpecHarvesterRefinePreviewPlan` with `compactModelInput` sections such as
`harvestSummary`, `projectProfile`, `publicInterfaceSummary`,
`semanticEvidenceIndex`, `validationSummaries`, and
`draftCandidateMetadata`. That plan excludes raw repository source and raw
documentation bodies.

When provider execution is added, SpecNode must use
`SpecNodeOpenAICompatibleProviderAdapter` policy for LM Studio or other
OpenAI-compatible local endpoints. Provider execution is `localhost_only` by
default, limited to `/v1/models` and `/v1/chat/completions`, and recorded in
`SpecNodeProviderUsageReceipt`. SpecHarvester does not contact providers.

Model output must conform to `SpecNodeCandidatePatchProposal` or
`SpecNodeRejectionReason`. Candidate changes are structured operations against
`specpm.yaml` and `specs/*.spec.yaml`, not raw diffs, shell commands, provider
calls, or direct file writes.

After structural `SpecNodeRefinementResult` validation, SpecHarvester can build
a `SpecNodeSemanticReviewJob` from the same deterministic artifacts, the
reviewed result, and a fixed `SpecNodeSemanticReviewRubric`. The semantic
reviewer emits only a `SpecNodeSemanticReviewResult` with `approve`,
`needs_revision`, or `reject` plus typed `SpecNodeSemanticReviewFinding`
records. It cannot emit `candidatePatchProposal`, `operations`,
`retryDirective`, shell commands, network fetches, provider calls, package
manager commands, test runner commands, build tool commands, or direct file
writes.

The local `SpecNodeProviderSmokeRun` harness exercises this bridge with an
in-process SpecNode-compatible provider stub. It validates a
`SpecNodeRefinementResult` and returns a deterministic
`provider_unavailable` `SpecNodeRejectionReason` when no provider is
configured. The smoke path still uses compact `SpecHarvesterRefinePreviewPlan`
input and keeps `rawRepositorySource: excluded`, `documentationBodies:
excluded`, `providerLogs: excluded`, `secrets: excluded`, and
`arbitraryPrompts: excluded`.

### SpecPM Validation Gate

Every generated candidate must pass:

```bash
specpm validate <candidate-dir> --json
```

### Review Gate

Generated packages should not be accepted into a public registry without a
review gate. Reviewers should check scope, evidence, provenance, package IDs,
intent IDs, upstream relationship, and licensing statements.

For accepted-source PR review, `prepare-accepted-entry` can deterministically add
an accepted manifest path before running `promote`.

Build an accepted-vs-candidate diff report before proposal prep:

```bash
python3 -m spec_harvester accepted-candidate-diff-report \
  --accepted-root <accepted-root> \
  --candidates-root <candidates-root>
```

Then classify impact by contract bucket:

```bash
python3 -m spec_harvester accepted-candidate-impact-classification-report \
  --accepted-root <accepted-root> \
  --candidates-root <candidates-root>
```

Governance reports can also be generated after drafting:

```bash
spec-harvester governance-report --accepted-root <accepted-root> --candidates-root <candidates-root>
```

The report summarizes duplicate `intent.*` and `provides.capabilities` claims
across accepted and candidate metadata to support human review before proposal.

Build a namespace and upstream relationship review report:

```bash
spec-harvester governance-upstream-report \
  --accepted-root <accepted-root> \
  --candidates-root <candidates-root>
```

The report lists namespace collisions, packages missing upstream relationship
links, and namespace-vs-upstream owner mismatches.

Build a license and provenance risk review report:

```bash
python3 -m spec_harvester governance-license-provenance-report \
  --accepted-root <accepted-root> \
  --candidates-root <candidates-root>
```

The report flags missing or suspicious licenses and upstream provenance signals
that should be reviewed before proposal.

### PR-Ready Update Proposal Builder

After review and promotion preparation, SpecHarvester can produce a review artifact
for the accepted-package mutation:

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  CANDIDATE_DIR \
  --accepted-root <accepted-root> \
  --output report/accepted-package-update-proposal.json \
  --proposal-body report/accepted-package-update-proposal.md
```

The builder compares candidate metadata against the latest accepted record for the
same package ID and includes:

- `oldPackageVersion` / `newPackageVersion`
- `sourceRevision`
- evidence digests for `specpm.yaml` and optional `harvest.json`
- changed capability and intent claims
- validation status
- reviewer notes and issues

This command is deterministic and reads only local files plus optional SpecPM
validation.

### Promotion Gate

Copies a reviewed candidate into an accepted source root and optionally appends
a local `path` entry to an accepted package manifest. Promotion does not publish
to a remote registry by itself.

Current command:

```bash
spec-harvester promote <candidate-dir> --accepted-root <accepted-root>
```

### Accepted Package Immutability

Accepted package versions are immutable evidence snapshots in accepted-source form.
When upstream revision or reviewed metadata changes require an update, SpecHarvester
does not mutate existing `<packageId>/<version>` trees in place.

Update flow is:

1. generate and validate a new candidate,
2. promote into a new accepted version location,
3. prepare the corresponding manifest path update,
4. deliver through SpecPM review and merge.

## Non-Goals

SpecHarvester does not replace SpecPM.

SpecHarvester does not define the remote registry API.

SpecHarvester does not make generated specs canonical.

SpecHarvester does not imply upstream maintainer endorsement.
