# Architecture

SpecHarvester is a producer pipeline for candidate SpecPM packages.

## Pipeline Shape

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

### Batch Validation Reporter

Builds advisory `SpecHarvesterBatchValidationReport` JSON for `collect-batch`
output. Reports summarize confidence, policy notes, warning codes, evidence
counts, and skipped records for reviewer inspection.

Report confidence is not an acceptance decision. It is review metadata.

### Deterministic Public Interface Analyzers

Extract compact `PublicInterfaceIndex` artifacts from local source bytes
without executing package code. Python uses the standard-library `ast` module,
and JavaScript/TypeScript uses package manifest entrypoints plus static export
scanning.

Analyzers can use an optional per-file cache keyed by analyzer id, analyzer
version, and file SHA-256 digest. The cache is derived untrusted metadata and
is ignored when metadata or path/evidence validation fails.

`PublicInterfaceIndex.summary.status` records static analysis coverage:
`complete` means no diagnostics were emitted, `partial` means diagnostics were
emitted while package evidence remains available for review, and `failed` means
diagnostics were emitted without any package record.

Analyzers that require metadata-only build tools are future optional
components. They must satisfy <doc:AnalyzerSandboxRequirements> before use.

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
`PublicInterfaceIndex` artifact and copy it into the candidate as
`public-interface-index.json`.

The draft is intentionally conservative. It records observed package metadata,
inferred capability IDs, inferred `intent.*` IDs, provenance, review
constraints, and analyzer-backed inbound interface summaries when a valid index
is provided. It does not claim upstream endorsement.

When a `PublicInterfaceIndex` is present, BoundarySpec evidence keeps
`kind: public_interface_index`, which is recognized by SpecPM `0.2.0+`, and
adds explicit artifact metadata: `artifactKind: SpecHarvesterPublicInterfaceIndex`,
`mediaType`, `schemaVersion`, and
`summary`. Older SpecPM validators may warn on that evidence kind; current
public-interface candidates should be checked with SpecPM `0.2.0+`.

When no supported package manifest exists, the drafter may use documentation
`semanticHints` as advisory `semantic_intent_static_evidence`. Language-neutral
clusters such as `api.contract_surface`, `metadata.schema_validation`,
`workflow.automation_pipeline`, and `developer.tooling_surface` can replace the
generic metadata fallback while remaining review evidence, not registry truth.

The drafter validates compact analyzer output; it does not run analyzers or
inspect raw repository source during candidate drafting.

### AI Draft Generator

Future component. It may refine deterministic candidates through a bounded
SpecNode job. The handoff contract is <doc:SpecNodeIntegrationContract>.

SpecHarvester must send only a `SpecHarvesterSpecNodeArtifactBundle` inside a
typed `SpecNodeRefinementJob`. The job policy keeps
`modelFilesystemAccess: none`, `modelShellAccess: none`, and
`candidateMutation: proposal_only`. SpecNode may return
`candidatePatchProposal`, `reviewNotes`, `rejectionReason`, and `usageReceipt`
metadata. Model output remains untrusted candidate metadata and must be
validated and reviewed before acceptance.

### SpecPM Validation Gate

Every generated candidate must pass:

```bash
specpm validate <candidate-dir> --json
```

### Promotion Gate

Promotion copies a reviewed candidate into an accepted source root and can
append a local path entry to an accepted package manifest. It is not direct
publication.

Before promotion, `prepare-accepted-entry` can generate and append a PR-ready
manifest entry from reviewed candidate metadata without mutating accepted-source
directories. The command supports deterministic `packageId/version` inference and
explicit `manifest-entry-path` overrides.

## Non-Goals

SpecHarvester does not replace SpecPM, define the remote registry API, or make
generated specs canonical by itself.

## References

- `docs/ARCHITECTURE.md`
- <doc:TrustBoundary>
- <doc:SpecNodeIntegrationContract>
- <doc:BatchValidationReports>
- <doc:Roadmap>
