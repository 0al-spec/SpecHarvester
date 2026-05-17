# P1-T1 Define PublicInterfaceIndex Snapshot Schema

Status: Planned
Selected: 2026-05-17
Branch: `feature/P1-T1-public-interface-index-schema`
Review subject: `p1_t1_public_interface_index_schema`

## Objective

Define the first deterministic `PublicInterfaceIndex` schema for
SpecHarvester. The schema must describe public package, entrypoint, symbol,
diagnostic, and analyzer metadata in a compact form that future static analyzers
can emit without executing repository content.

This task does not implement language analyzers. It creates the typed schema
builder and validation surface that later tasks can populate from Python AST,
JavaScript/TypeScript exports, Tree-sitter syntax indexes, or sandboxed
language-specific tools.

## Deliverables

- Add `src/spec_harvester/interface_index.py`.
- Provide deterministic constructors for an empty index and analyzer entries.
- Provide validation for index shape, schema version, kind, source revision,
  analyzer records, package records, entrypoints, symbols, and diagnostics.
- Add focused tests for valid shape, deterministic JSON serialization, and
  invalid records.
- Create `SPECS/INPROGRESS/P1-T1_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- The index kind is `SpecHarvesterPublicInterfaceIndex`.
- The schema version is stable and recorded as an integer.
- Analyzer metadata records `id`, `version`, `execution`, `networkAccess`,
  `packageScripts`, and `confidence`.
- Symbols can represent at least `function`, `class`, `struct`, `enum`,
  `interface`, `type`, `constant`, `variable`, and `unknown`.
- Every source evidence reference includes `path` and `sha256`.
- Validation rejects unsupported execution/network/script modes and malformed
  evidence records.
- JSON output is deterministic with sorted keys when produced by tests.

## Trust Boundary

The schema is evidence metadata only. It must not execute harvested repository
code, install dependencies, import modules from the harvested repository, run
package scripts, or make network calls. Analyzer execution mode must be explicit
so future non-static tools can be reviewed separately.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Schema tests | Expected minimal index fields | Failing tests for constructors and validators | `PYTHONPATH=src python -m pytest tests/test_interface_index.py` |
| Implementation | Test expectations | `interface_index.py` | Targeted test passes |
| Full validation | Repository gates | Validation report | Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add tests for `new_public_interface_index`, `analyzer_record`, and
   deterministic JSON serialization.
2. Add tests for validation failures on bad kind, schema version, analyzer
   execution policy, and malformed evidence references.
3. Implement schema constants, allowed vocabularies, constructors, and
   validation helpers.
4. Run targeted tests, then full Flow quality gates from `.flow/params.yaml`.
5. Record validation results in `P1-T1_Validation_Report.md`.

## Non-Goals

- No Python AST analyzer.
- No JavaScript, TypeScript, Swift, Rust, Go, or Tree-sitter parser.
- No integration into `collect-local` or `draft`.
- No changes to candidate SpecPM generation.

## Notes

Future tasks should consume this schema rather than introducing analyzer-specific
output formats.

---
**Archived:** 2026-05-17
**Verdict:** PASS
