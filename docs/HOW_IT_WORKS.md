# How SpecHarvester Works

Status: Bootstrap runbook

SpecHarvester turns public repository metadata into reviewable SpecPM candidate
packages.

It is not a replacement for SpecPM. It is a producer pipeline that prepares
candidate `SpecPackage` and `BoundarySpec` files so SpecPM can validate them and
so maintainers can decide whether they belong in a public registry.

## One-Screen Summary

```text
public repository URL
        |
        v
local checkout at a pinned revision
        |
        v
collect-local or collect-batch
        |
        v
harvest.json
        |
        v
draft
        |
        v
specpm.yaml + specs/*.spec.yaml
        |
        v
specpm validate
        |
        v
human review
        |
        v
promote
        |
        v
accepted package source
        |
        v
SpecPM public index, future
```

The current bootstrap supports the first controlled candidate loop:

```text
checkout -> harvest.json -> generated SpecPackage -> SpecPM validation -> promotion copy
```

Publication into a registry is intentionally still a SpecPM maintainer PR.

## Terms

### Harvest Snapshot

`harvest.json` is a static evidence snapshot. It records allowlisted file paths,
checksums, bounded metadata, source repository information, collection policy,
and analyzer trust policy.

It is evidence, not a spec.

The `analyzerPolicy` record declares which analyzer artifacts later pipeline
steps may consider compatible with the snapshot. The bootstrap default requires
analyzers to declare:

- `execution: none`
- `networkAccess: none`
- `packageScripts: not_run`
- analyzer id and version metadata
- source revision metadata
- source digest evidence

The policy is declarative. `collect-local` does not run analyzers.

### Analyzer Cache

Deterministic public interface analyzers may use an optional local cache to
avoid reparsing unchanged source files. Cache entries are keyed by analyzer id,
analyzer version, and file SHA-256 digest, and include a cache schema version.

The cache is only an optimization. Analyzer output remains untrusted evidence:
malformed entries, metadata mismatches, digest mismatches, and path/evidence
mismatches are ignored and recomputed.

### Candidate SpecPackage

`specpm.yaml` plus `specs/*.spec.yaml` is a generated SpecPM candidate package.
It is intended for review and validation.

It is not accepted registry truth until maintainers review it.

### Observed Intent

Generated `intent.*` IDs are observed metadata inferred from static repository
signals such as package names and descriptions.

Observed intent IDs are useful for search, duplicate detection, and future
authoring assistance, but they are not canonical semantic authority by
themselves.

For manifest-poor repositories, observed intent can also come from bounded
language-neutral documentation hints. `collect-local` may record compact
`semanticHints` from allowlisted README, API contract, OpenAPI, schema
validation, workflow automation, developer tooling, web framework, or
documentation knowledge base Markdown. `draft` may convert those hints into
`semantic_intent_static_evidence` clusters such as
`intent.web.framework_surface`, `intent.web.http_routing`,
`intent.api.contract_surface`, `intent.metadata.schema_validation`,
`intent.workflow.automation_pipeline`, and
`intent.developer.tooling_surface`.

`draft` also normalizes `PublicInterfaceIndex` symbols into compact semantic
tokens. This lets static names such as `RouterGroup`, `HandlerFunc`,
`RequestContext`, or `Blueprint` support web framework intent claims without
reading raw source bodies during drafting.

Semantic evidence `supports` entries are constrained to declared SpecPM support
targets: `intent.summary`, `provides.capabilities`, and
`provides.capabilities.<capability_id>`. The drafter does not emit
`provides.capabilities.intentIds` because nested `intentIds` is not part of the
current SpecPM BoundarySpec support-target grammar.

This path stores terms and evidence paths only. It does not store raw
documentation bodies, execute repository code, install dependencies, run package
scripts, or contact networks.

raw documentation bodies remain excluded from generated evidence artifacts.

### Accepted Package

An accepted package is a reviewed candidate that maintainers choose to publish
through a SpecPM registry source.

That acceptance step is not automated in the current bootstrap.

### Accepted Package Update Lifecycle

Accepted package versions are immutable once accepted:

- do not overwrite the accepted manifest package path for
  `<packageId>/<packageVersion>`.
- new upstream reality or corrections always create a new accepted version
  publication path.
- if a candidate reuses an already accepted `packageId@version`, the update must
  pass an explicit correction flow.

When upstream evidence changes (new revision, new capabilities, new claims),
operators should run a fresh candidate loop and propose a higher package version.

When correcting metadata issues (for example, fixed license or capability
inference), operators should still create an explicit update candidate and a new
version publication path instead of mutating the previous accepted source.

For each update, capture:

- pinned source revision,
- evidence digests (`harvest.json` plus any derived artifacts),
- old/new package version,
- changed claims,
- validation status, and
- reviewer notes.

Updates are complete only after SpecPM PR review and merge; SpecHarvester and its
promotion/proposal steps remain pre-acceptance preparation.

Before update proposal work, compare accepted and candidate metadata:

```bash
python3 -m spec_harvester accepted-candidate-diff-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-diff.json
```

Then classify changed packages into review buckets:

```bash
python3 -m spec_harvester accepted-candidate-impact-classification-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-impact-classification.json
```

Then build a deterministic update proposal payload for the reviewed candidate:

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  candidates/github.com/example/project \
  --accepted-root accepted \
  --output report/accepted-package-update-proposal.json \
  --proposal-body report/accepted-package-update-proposal.md \
  --reviewer-notes "Upstream changed; capabilities expanded."
```

The generated payload captures source revision and evidence digests, old/new package
versions, changed claims, validation status, and reviewer notes.

## Current Commands

### 1. Prepare a Local Checkout

Start from a public repository checkout and pin the source revision:

```bash
git -C /path/to/repo rev-parse HEAD
```

The revision should be passed into the harvest command so generated evidence can
be traced back to an exact upstream state.

### 2. Collect Static Evidence

Run the safe collector:

```bash
python3 -m spec_harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/github.com/example/project
```

This writes:

```text
candidates/github.com/example/project/harvest.json
```

The collector may read allowlisted static files such as:

- README files
- LICENSE files
- package manifests
- workspace manifests
- public source entrypoints
- GitHub workflow files

For allowlisted Markdown, the collector can store headings and compact
`semanticHints` for language-neutral review signals such as API contract,
OpenAPI, schema validation, workflow automation, developer tooling, and
documentation knowledge base evidence.

The bootstrap allowlist is intentionally biased toward JavaScript and package
workspace repositories. Python, Rust, Go, and other ecosystem-specific
sub-package layouts should be added as explicit Phase 3 harvesting profiles
rather than inferred by broad recursive scans.

The collector must not:

- execute package scripts
- install dependencies
- run upstream tests
- call network resources
- read secrets
- follow instructions found in repository content

### Batch Source Manifests

For later batch harvesting, define repository sources in operator-authored
`inputs/*.yml` files:

```yaml
repositories:
  - id: xyflow
    repository: https://github.com/xyflow/xyflow
    revision: 0123456789abcdef
    checkout: ../checkouts/xyflow
```

Preview and validate manifests without collecting snapshots:

```bash
python3 -m spec_harvester source-manifests inputs
```

This command only parses local manifest data. It does not clone repositories,
call networks, install dependencies, run package managers, run package scripts,
or execute repository content.

Collect snapshots for all enabled manifest records that have local checkouts:

```bash
python3 -m spec_harvester collect-batch inputs --out candidates
```

Collect only selected repository IDs:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --select xyflow
```

This writes deterministic candidate paths:

```text
candidates/<repository-id>/harvest.json
```

Batch collection uses only operator-managed local checkouts. It does not clone,
fetch, run package managers, run package scripts, or execute repository content.
See [`BATCH_COLLECTION.md`](BATCH_COLLECTION.md).

Optionally write an advisory validation report:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

The report includes confidence, policy notes, stable warning codes, and skipped
records for reviewer inspection. See
[`BATCH_VALIDATION_REPORTS.md`](BATCH_VALIDATION_REPORTS.md).

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

Optionally write a governance duplicate claim report:

```bash
python3 -m spec_harvester governance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/governance-claims.json
```

The report summarizes overlapping `intent.*` and `provides.capabilities` claims
across accepted and candidate metadata for review prioritization.
See [`GOVERNANCE_REPORTS.md`](GOVERNANCE_REPORTS.md).

Optionally write a namespace and upstream relationship review report:

```bash
python3 -m spec_harvester governance-upstream-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/namespace-upstream.json
```

This report highlights namespace collisions, missing upstream repository
provenance, and namespace-vs-upstream-owner mismatches for maintainer review.
See [`NAMESPACE_UPSTREAM_REPORTS.md`](NAMESPACE_UPSTREAM_REPORTS.md).

### 3. Draft a Candidate SpecPackage

Run the deterministic drafter:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --name project \
  --out candidates/github.com/example/project
```

If a deterministic analyzer has already produced a compact
`PublicInterfaceIndex`, either rely on auto-detection beside `harvest.json` or
pass it explicitly:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --name project \
  --interface-index candidates/github.com/example/project/public-interface-index.json \
  --out candidates/github.com/example/project
```

When no `--interface-index` value is provided, the drafter auto-detects a
`public-interface-index.json` file beside `harvest.json`.

This writes:

```text
candidates/github.com/example/project/specpm.yaml
candidates/github.com/example/project/specs/project.spec.yaml
```

When public interface evidence is supplied or auto-detected, the drafter also
writes a normalized copy:

```text
candidates/github.com/example/project/public-interface-index.json
```

The drafter currently derives conservative metadata from `harvest.json`:

- package identity
- package capabilities
- observed `intent.*` IDs
- compatibility hints
- analyzer-backed `interfaces.inbound` summaries when a valid
  `PublicInterfaceIndex` is present
- source repository provenance
- evidence links back to `harvest.json`
- evidence links back to `public-interface-index.json` when present
- review constraints
- `preview_only: true`

Intent inference is a deterministic bootstrap heuristic over package manifest
names and descriptions. It is useful as reviewable seed metadata, but it is not
semantic authority and it can produce false positives. Other harvested files,
including GitHub workflow files, are preserved as evidence and are not used for
intent inference.

The draft step does not run analyzers. It only reads and validates the supplied
`PublicInterfaceIndex`, copies the normalized JSON into the candidate directory,
and uses its package, entrypoint, symbol, analyzer, and diagnostic summary as
reviewable metadata.

The BoundarySpec evidence record for this artifact uses
`kind: public_interface_index`, which is recognized by SpecPM `0.2.0+`, and
includes `artifactKind: SpecHarvesterPublicInterfaceIndex`, `mediaType`,
`schemaVersion`, and `summary` so reviewers can identify the deterministic
artifact contract without opening the JSON first.

`PublicInterfaceIndex.summary.status` makes partial analysis explicit:

- `complete` means no diagnostics were emitted.
- `partial` means diagnostics were emitted while package evidence remains
  available for review.
- `failed` means diagnostics were emitted without any package record.

The generated package must be treated as untrusted candidate metadata.

### 4. Validate with SpecPM

Run SpecPM validation against the generated candidate directory:

```bash
specpm validate candidates/github.com/example/project --json
```

When running from this development checkout without installing SpecPM globally,
use the local SpecPM source path:

```bash
PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src \
  python -m specpm.cli validate \
  /Users/egor/Development/GitHub/0AL/SpecHarvester/candidates/github.com/example/project \
  --json
```

Expected bootstrap result:

```text
status: warning_only
```

The expected warning is usually:

```text
preview_only_package
```

That warning is intentional. Generated packages are candidates until reviewed.

### 5. Review the Candidate

Reviewers should check:

- package ID naming
- capability IDs
- observed intent IDs
- scope includes and excludes
- evidence support targets
- source repository and revision
- upstream endorsement wording
- license metadata
- whether generated claims are too broad
- whether the package should remain rejected, stay candidate, or become accepted

The review should be stricter than ordinary YAML validation. A candidate can be
valid YAML and still be semantically wrong.

### 6. Accept or Reject

Current bootstrap behavior:

```text
validated candidate -> human decision
```

The current repository does not publish directly into an accepted registry.

### 7. Prepare PR-Ready Manifest Entry

After review, prepare an accepted package manifest entry without copying the
candidate:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest /Users/egor/Development/GitHub/0AL/SpecPM/public-index/accepted-packages.yml
```

This command reads `<candidate>/specpm.yaml` metadata, derives
`<packageId>/<packageVersion>`, and writes:

```text
public-index/generated/<packageId>/<packageVersion>
```

as an accepted-packages manifest path when no explicit `--manifest-entry-path` is
provided.

### 8. Promote a Reviewed Candidate

After review, copy the candidate into an accepted source root:

```bash
python3 -m spec_harvester promote candidates/github.com/example/project \
  --accepted-root accepted \
  --manifest accepted/accepted-packages.yml
```

Promotion does three controlled things:

- validates the candidate with SpecPM unless `--skip-validation` is passed;
- copies the candidate into `<accepted-root>/<package_id>/<version>`;
- optionally appends a local `path` entry to an accepted package manifest.

For a SpecPM public-index PR, point promotion at a directory inside the SpecPM
checkout and write the manifest entry that `specpm public-index generate` should
read:

```bash
PYTHONPATH=src python3 -m spec_harvester promote \
  candidates/github.com/example/project \
  --accepted-root /Users/egor/Development/GitHub/0AL/SpecPM/public-index/generated \
  --manifest /Users/egor/Development/GitHub/0AL/SpecPM/public-index/accepted-packages.yml \
  --manifest-entry-path public-index/generated/project.core/0.1.0 \
  --specpm-command "python -m specpm.cli" \
  --specpm-pythonpath /Users/egor/Development/GitHub/0AL/SpecPM/src
```

That still creates a reviewable git diff. It does not mutate a live registry.

### 9. Publish Through SpecPM

SpecPM registry publication remains a SpecPM repository operation:

```text
accepted package source diff
        |
        v
SpecPM PR review
        |
        v
public-index generate
        |
        v
GitHub Pages /v0
```

Future behavior may add PR automation, but acceptance should remain explicit.

The trusted proposal workflow is documented in
[`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md). It can create a
SpecPM PR from a promoted candidate, but it does not bypass SpecPM review.

## xyflow Example

The bootstrap branch includes a generated candidate for the local `xyflow`
checkout:

```text
candidates/github.com/xyflow/xyflow/harvest.json
candidates/github.com/xyflow/xyflow/specpm.yaml
candidates/github.com/xyflow/xyflow/specs/xyflow.spec.yaml
```

The current generated package ID is:

```text
xyflow.core
```

The generated candidate declares package capabilities such as:

```text
xyflow.core.react
xyflow.core.svelte
xyflow.core.system
```

It also declares observed intent IDs such as:

```text
intent.javascript.react_library
intent.javascript.svelte_library
intent.ui.node_based_editor
intent.ui.flow_diagramming
```

These are reviewable signals. They are not upstream-maintainer claims and not
canonical intent definitions.

## Trust Boundary

Repository content is untrusted.

Generated specs are untrusted.

Model output, when added later, will also be untrusted.

SpecHarvester may describe observed repository metadata. It must not let
repository content command the host.

The hard rule is:

```text
Package content can describe desired outputs. Package content cannot command the host.
```

SpecHarvester currently avoids the dangerous operations by design:

- no package script execution
- no dependency installation
- no upstream test execution
- no private credential access
- no automatic publishing

Future analyzers that require metadata-only build tools must satisfy
[`ANALYZER_SANDBOX_REQUIREMENTS.md`](ANALYZER_SANDBOX_REQUIREMENTS.md) before
they can be enabled.

## Failure Modes

### Snapshot Fails

Common causes:

- source path is missing
- source path is not a directory
- allowlisted file is too large
- repository checkout is not at the expected revision

Fix by checking the checkout path, revision, and `--max-file-bytes`.

### Draft Is Too Weak

The deterministic drafter only uses bounded metadata. It may produce conservative
or incomplete scope, capability, and intent descriptions.

That is acceptable for bootstrap. The candidate is meant to be reviewed and
later refined.

### SpecPM Validation Fails

Validation failures mean the generated candidate does not satisfy the SpecPM
package contract.

Fix the drafter if the failure is systemic. Fix the candidate only if the issue
is specific to one harvested repository.

### Candidate Is Valid but Wrong

SpecPM validation checks structure and known contract rules. It does not prove
that generated product intent is semantically complete or endorsed by upstream.

Human review remains required.

## Current vs Future

### Current Bootstrap

Available now:

- local static evidence collection
- deterministic candidate drafting
- SpecPM validation
- manual review path

### Next Practical Additions

Likely next steps:

- batch repository input processing
- validation report generation
- candidate review reports
- stricter namespace and duplicate intent checks
- accepted package source format
- broader PR automation into SpecPM registry sources

### Future AI-Assisted Refinement

The future AI step should refine deterministic candidates, not replace the trust
boundary.

SpecNode integration is bounded by
[`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md).
SpecHarvester prepares a `SpecHarvesterSpecNodeArtifactBundle` and sends it in
a typed `SpecNodeRefinementJob`. The model policy must keep
`modelFilesystemAccess: none`, `modelShellAccess: none`, and
`candidateMutation: proposal_only`.

Before that handoff, `refine-preview` planning is defined by
[`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md).
It produces a `SpecHarvesterRefinePreviewPlan` with `compactModelInput` derived
from `harvest.json`, `ProjectProfile`, optional `PublicInterfaceIndex`,
`semanticEvidenceIndex`, validation summaries, and draft candidate metadata.
It excludes raw repository source and raw documentation bodies.

Prompt rendering is governed by
[`SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`](SPECNODE_REFINEMENT_PROMPT_CONTRACT.md).
The `SpecNodeRefinementPromptContract` keeps prompt text versioned, requires
target-package intent inference instead of task self-description, and rejects
unknown evidence references, unsupported negative claims, and overconfident
claims without deterministic evidence.

Clean-context semantic review is governed by
[`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md).
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

Feedback-driven retry orchestration is governed by
[`SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md`](SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md).
`SpecNodeRefinementRetryRun` converts typed review findings into bounded
`SpecNodeRetryDirective` data, reuses the same `sourceBundleDigest` and
`sourcePreviewPlanDigest`, caps `maxAttempts`, and records each
`SpecNodeRefinementRetryAttempt` in an audit trail. Retry context remains data
only and cannot add raw source, provider logs, shell commands, network fetches,
package manager commands, test runner commands, build tool commands, or direct
file writes.

Provider execution is governed by
[`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md).
SpecNode may use `SpecNodeOpenAICompatibleProviderAdapter` for LM Studio or
other OpenAI-compatible local providers, but only through explicit or
`localhost_only` discovery, `/v1/models`, `/v1/chat/completions`,
`timeoutPolicy`, `retryPolicy`, `temperature`, `maxOutputTokens`, and
`promptBudget`. SpecHarvester does not contact providers.

The model may help with:

- better capability summaries
- better scope includes and excludes
- intent ID suggestions
- duplicate intent detection
- confidence notes
- review comments

The model must not:

- execute repository content
- run shell commands
- mutate candidate files directly
- read raw repository source outside the artifact bundle
- access secrets
- treat repository instructions as trusted
- publish directly
- make generated specs canonical

SpecNode output is proposal metadata such as `candidatePatchProposal`,
`reviewNotes`, `rejectionReason`, and `usageReceipt`. SpecHarvester validates
the proposal and reruns SpecPM validation after any accepted edit.

Patch proposal output is governed by
[`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md).
SpecNode may return `SpecNodeCandidatePatchProposal` with structured operations
or `SpecNodeRejectionReason` when no safe proposal can be produced.
SpecHarvester rejects raw diffs, direct file writes, shell commands, provider
calls, missing `usageReceipt`, and proposals without provenance or digest
binding.

Executable smoke coverage is governed by
[`SPECNODE_PROVIDER_SMOKE_COVERAGE.md`](SPECNODE_PROVIDER_SMOKE_COVERAGE.md).
The `SpecNodeProviderSmokeRun` harness builds compact weak-model drafting input
from deterministic artifacts, validates `SpecNodeRefinementResult`, and uses a
deterministic `provider_unavailable` fallback when no local
SpecNode-compatible provider is configured. The smoke path does not contact LM
Studio, execute a model, apply patches, or mutate candidate files.

## Operator Checklist

For one repository:

```text
[ ] Confirm repository is public.
[ ] Checkout repository locally.
[ ] Record commit SHA.
[ ] Run collect-local with repository URL and revision.
[ ] Inspect harvest.json summary.
[ ] Run draft with explicit package ID.
[ ] Run specpm validate.
[ ] Review generated package and BoundarySpec.
[ ] Decide reject, revise, or promote.
[ ] Prepare PR-ready manifest entry.
[ ] Run promote into an accepted source root.
[ ] Open or update a maintainer PR for registry publication.
```

For the current `xyflow` example:

```bash
git -C /Users/egor/Development/GitHub/xyflow rev-parse HEAD

PYTHONPATH=src python3 -m spec_harvester collect-local \
  /Users/egor/Development/GitHub/xyflow \
  --repository https://github.com/xyflow/xyflow \
  --revision <commit-sha> \
  --out candidates/github.com/xyflow/xyflow

PYTHONPATH=src python3 -m spec_harvester draft \
  candidates/github.com/xyflow/xyflow \
  --package-id xyflow.core \
  --name xyflow \
  --out candidates/github.com/xyflow/xyflow

PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src \
  python -m specpm.cli validate \
  /Users/egor/Development/GitHub/0AL/SpecHarvester/candidates/github.com/xyflow/xyflow \
  --json

PYTHONPATH=src python3 -m spec_harvester promote \
  candidates/github.com/xyflow/xyflow \
  --accepted-root accepted \
  --manifest accepted/accepted-packages.yml \
  --skip-validation

python3 -m spec_harvester prepare-accepted-entry \
  candidates/github.com/xyflow/xyflow \
  --manifest /Users/egor/Development/GitHub/0AL/SpecPM/public-index/accepted-packages.yml
```

## Relationship to SpecPM and SpecGraph

SpecHarvester produces candidates.

SpecPM validates, packages, indexes, and serves accepted SpecPackage data.

SpecGraph and downstream governance may later curate meaning, relationships, and
canonical intent vocabulary.

SpecHarvester should remain a harvesting and candidate-production tool. It
should not become the canonical reasoning layer.
