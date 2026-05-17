# P1-T5 Integrate Public Interface Evidence into Deterministic Drafting

Status: Planned
Selected: 2026-05-17
Branch: `feature/P1-T5-integrate-public-interface-evidence-into-drafting`
Review subject: `p1_t5_public_interface_evidence_drafting`

## Objective

Integrate deterministic `PublicInterfaceIndex` evidence into the `draft`
pipeline so generated BoundarySpecs can describe richer `interfaces.inbound`
entries from compact analyzer output instead of inspecting raw source during
drafting.

The draft step must continue to treat harvested repositories as untrusted data.
It may read a precomputed analyzer JSON artifact, validate it, and copy it into
the candidate output as evidence. It must not execute package code, run package
scripts, install dependencies, call build tools, or invoke static analyzers
implicitly.

## Deliverables

- Extend `DraftOptions` and the `draft` CLI with an optional public interface
  index input.
- Auto-detect a colocated `public-interface-index.json` beside `harvest.json`
  when no explicit interface index path is provided.
- Validate the supplied artifact with `validate_public_interface_index`.
- Enrich generated `interfaces.inbound` entries with public package,
  entrypoint, symbol, and analyzer-derived metadata.
- Copy the validated index into the candidate output as
  `public-interface-index.json` and reference it from BoundarySpec evidence.
- Add tests for direct API use, CLI use, auto-detection, and malformed index
  rejection.
- Update user-facing documentation for the new draft input.
- Create `SPECS/INPROGRESS/P1-T5_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- `draft` remains deterministic for the same `harvest.json` and
  `PublicInterfaceIndex` inputs.
- `draft` does not run analyzers or inspect repository source paths directly.
- Invalid public interface indexes fail before candidate files are written.
- Generated inbound interfaces include analyzer-backed entrypoint and symbol
  summaries when valid public interface evidence is present.
- Existing manifest-only drafting behavior remains unchanged when no interface
  index is supplied.
- BoundarySpec evidence includes a `public_interface_index` record supporting
  generated inbound interfaces.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

The public interface index is untrusted metadata. The drafter must validate its
shape and preserve it as reviewable evidence, but it must not treat analyzer
claims as accepted registry truth. Analyzer execution policy remains encoded in
the index itself.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Drafter tests | Harvest snapshot plus compact public interface index fixture | Failing tests for enriched interfaces, evidence copy, CLI option, auto-detection, and invalid index rejection | `PYTHONPATH=src python -m pytest tests/test_collector.py` |
| Implementation | Test expectations and `interface_index.py` validators | `drafter.py` and `cli.py` changes | Targeted tests pass |
| Documentation | Updated behavior | Docs mention `--interface-index` and evidence artifact | Docs are deterministic and linked |
| Full validation | Repository gates | Validation report | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add focused tests around `draft` public interface index consumption.
2. Add `DraftOptions.interface_index` and CLI `--interface-index`.
3. Implement validated index loading, auto-discovery, normalized evidence copy,
   and deterministic interface enrichment.
4. Update docs for the analyzer-output-to-draft path.
5. Run Flow quality gates and record the validation report.

## Non-Goals

- No new analyzer command.
- No automatic analyzer execution inside `draft`.
- No Tree-sitter implementation.
- No source tree scanning beyond reading explicitly provided JSON artifacts.
- No promotion or registry acceptance changes.
