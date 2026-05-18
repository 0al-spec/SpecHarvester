# SpecHarvester Workplan

Status: Draft
Created: 2026-05-17
Updated: 2026-05-18
Input: `PRD.md`, `docs/ROADMAP.md`, current repository implementation

## Working Rules

- Keep harvesting local-first and deterministic.
- Treat every harvested repository file as untrusted data.
- Prefer static metadata, AST, and parser output over LLM discovery.
- Do not execute package scripts, install harvested dependencies, or access
  secrets.
- Preserve evidence paths, file digests, analyzer versions, and policy notes.
- Use SpecPM validation before promotion.
- Keep generated candidates preview-only until reviewed.
- Keep Flow artifacts small enough to be useful in code review.

## Phase 0. Flow Operating Baseline

- [x] `P0-T1` Configure Flow operating scaffold.

Acceptance:

- `SPECS/COMMANDS/FLOW.md` exists.
- `SPECS/PRD.md` and `SPECS/Workplan.md` exist.
- `SPECS/INPROGRESS/next.md` identifies the next recommended task.
- `SPECS/ARCHIVE/INDEX.md` exists.
- Required quality gates are documented and locally runnable.

## Phase 1. Public Interface Indexing

- [x] `P1-T1` Define `PublicInterfaceIndex` snapshot schema.
- [x] `P1-T2` Add Python static public API analyzer using `ast`.
- [x] `P1-T3` Add JavaScript and TypeScript manifest/export analyzer.
- [x] `P1-T4` Evaluate Tree-sitter as the shared syntax indexing layer.
- [x] `P1-T5` Integrate public interface evidence into deterministic drafting.

Acceptance:

- Interface extraction runs without executing harvested repository code.
- Analyzer outputs include provenance, analyzer version, and source digests.
- `draft` can build richer `interfaces.inbound` entries from public interface
  evidence.
- LLM refinement can consume a compact public interface summary instead of raw
  source files.

## Phase 2. Analyzer Policy and Cache

- [x] `P2-T1` Add analyzer trust policy fields to harvest snapshots.
- [x] `P2-T2` Add per-file analyzer cache keyed by file digest and analyzer
  version.
- [x] `P2-T3` Add parse diagnostics and partial-index behavior.
- [x] `P2-T4` Document sandbox requirements for analyzers that need build
  tools.

Acceptance:

- Static analyzers fail closed and record diagnostics.
- Re-running harvest on unchanged files reuses cached analyzer results.
- Any analyzer requiring build tools is explicitly marked and sandboxed.

## Phase 3. Batch Harvesting

- [x] `P3-T1` Read repository source manifests from `inputs/*.yml`.
- [x] `P3-T2` Collect snapshots for selected repositories into deterministic
  candidate paths.
- [x] `P3-T3` Emit batch validation reports with confidence and policy notes.

Acceptance:

- Batch mode never executes package content.
- Batch outputs are deterministic for the same source revision and config.

## Phase 4. SpecPM Proposal Integration

- [x] `P4-T1` Prepare PR-ready accepted package manifest entries.
- [x] `P4-T2` Add proposal preflight checks for accepted-source diffs.
- [x] `P4-T3` Extend GitHub proposal automation documentation and validation.

Acceptance:

- Trusted maintainers can propose reviewed accepted-source changes into SpecPM.
- Ordinary pull requests cannot use write credentials for cross-repository
  mutation.

## Phase 5. Governance Reports

- [x] `P5-T1` Add duplicate intent and capability claim report.
- [x] `P5-T2` Add namespace and upstream relationship review report.
- [x] `P5-T3` Add license and provenance risk report.

Acceptance:

- Generated reports remain advisory review artifacts.
- Reports do not accept, reject, publish, install, or execute package content.

## Phase 6. Smoke-Test Feedback

- [x] `P6-T1` Discover nested Swift package manifests during static harvest.
- [x] `P6-T2` Infer candidate license metadata from allowlisted LICENSE files.
- [x] `P6-T3` Make namespace and upstream owner comparison case-insensitive.
- [x] `P6-T4` Add reproducible local smoke-test fixture documentation.

Acceptance:

- Swift repositories with nested `Package.swift` files are collected with useful
  package-manifest evidence without executing SwiftPM or package code.
- Generated candidates can infer common license identifiers from static LICENSE
  files when package manifests do not provide license metadata.
- Governance namespace/upstream reports do not flag casing-only GitHub owner
  differences as mismatches.
- Smoke testing remains local-only, deterministic, and clearly separated from
  committed generated candidate outputs.

## Phase 7. Smoke-Test Signal Quality

- [x] `P7-T1` Treat package namespace matches against upstream repository names
  as valid namespace evidence.
- [ ] `P7-T2` Derive less generic Swift package intents from package products
  and manifests.
- [ ] `P7-T3` Distinguish absent license evidence from ambiguous unknown license
  evidence.
- [ ] `P7-T4` Add a compact local smoke triage summary for batch and governance
  report output.

Acceptance:

- Governance namespace/upstream reports avoid false positives when a package
  namespace matches the upstream repository name but not the GitHub owner.
- Swift-only candidates avoid duplicate generic metadata intents when static
  product or manifest evidence can support a more specific claim.
- License provenance reports explain whether `UNKNOWN` means no license evidence
  was found or license-like evidence was present but not classifiable.
- Local smoke output can be summarized into a stable review artifact without
  committing generated candidates.

## Phase 8. Accepted Specification Update Lifecycle

- [ ] `P8-T1` Document accepted package update lifecycle and immutability policy.
- [ ] `P8-T2` Add accepted-vs-candidate package diff report.
- [ ] `P8-T3` Classify update proposals by metadata, interface, license,
  provenance, capability, and intent impact.
- [ ] `P8-T4` Add PR-ready SpecPM update proposal flow for new accepted package
  versions.
- [ ] `P8-T5` Add correction and errata path for fixing accepted metadata
  without treating upstream content as changed.

Acceptance:

- Accepted SpecPM package versions are treated as immutable registry evidence
  unless a correction path explicitly records the reason for metadata repair.
- Noticeable upstream module changes produce a new reviewed candidate from a
  pinned source revision and a reviewable diff against the currently accepted
  package version.
- Update proposals preserve audit trail: source revision, evidence digests,
  old/new package version, changed claims, validation status, and reviewer
  notes.
- SpecHarvester can propose update PRs to SpecPM, but SpecPM review and merge
  remain the acceptance boundary.
