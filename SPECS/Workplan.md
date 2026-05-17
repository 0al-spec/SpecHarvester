# SpecHarvester Workplan

Status: Draft
Created: 2026-05-17
Updated: 2026-05-17
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
- [ ] `P1-T3` Add JavaScript and TypeScript manifest/export analyzer.
- [ ] `P1-T4` Evaluate Tree-sitter as the shared syntax indexing layer.
- [ ] `P1-T5` Integrate public interface evidence into deterministic drafting.

Acceptance:

- Interface extraction runs without executing harvested repository code.
- Analyzer outputs include provenance, analyzer version, and source digests.
- `draft` can build richer `interfaces.inbound` entries from public interface
  evidence.
- LLM refinement can consume a compact public interface summary instead of raw
  source files.

## Phase 2. Analyzer Policy and Cache

- [ ] `P2-T1` Add analyzer trust policy fields to harvest snapshots.
- [ ] `P2-T2` Add per-file analyzer cache keyed by file digest and analyzer
  version.
- [ ] `P2-T3` Add parse diagnostics and partial-index behavior.
- [ ] `P2-T4` Document sandbox requirements for analyzers that need build
  tools.

Acceptance:

- Static analyzers fail closed and record diagnostics.
- Re-running harvest on unchanged files reuses cached analyzer results.
- Any analyzer requiring build tools is explicitly marked and sandboxed.

## Phase 3. Batch Harvesting

- [ ] `P3-T1` Read repository source manifests from `inputs/*.yml`.
- [ ] `P3-T2` Collect snapshots for selected repositories into deterministic
  candidate paths.
- [ ] `P3-T3` Emit batch validation reports with confidence and policy notes.

Acceptance:

- Batch mode never executes package content.
- Batch outputs are deterministic for the same source revision and config.

## Phase 4. SpecPM Proposal Integration

- [ ] `P4-T1` Prepare PR-ready accepted package manifest entries.
- [ ] `P4-T2` Add proposal preflight checks for accepted-source diffs.
- [ ] `P4-T3` Extend GitHub proposal automation documentation and validation.

Acceptance:

- Trusted maintainers can propose reviewed accepted-source changes into SpecPM.
- Ordinary pull requests cannot use write credentials for cross-repository
  mutation.

## Phase 5. Governance Reports

- [ ] `P5-T1` Add duplicate intent and capability claim report.
- [ ] `P5-T2` Add namespace and upstream relationship review report.
- [ ] `P5-T3` Add license and provenance risk report.

Acceptance:

- Generated reports remain advisory review artifacts.
- Reports do not accept, reject, publish, install, or execute package content.
