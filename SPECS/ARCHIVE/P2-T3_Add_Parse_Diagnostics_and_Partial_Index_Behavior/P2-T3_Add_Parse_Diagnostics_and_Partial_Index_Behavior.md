# P2-T3 Add Parse Diagnostics and Partial-Index Behavior

Status: Planned
Selected: 2026-05-17
Branch: `feature/P2-T3-add-parse-diagnostics-and-partial-index-behavior`
Review subject: `p2_t3_parse_diagnostics_partial_index`

## Objective

Make `PublicInterfaceIndex` partial-index state explicit so downstream
drafting and review flows can distinguish complete analysis from analysis that
continued after parser, manifest, or entrypoint diagnostics.

This task strengthens diagnostic semantics without executing repository code,
installing dependencies, running package scripts, calling networks, or treating
analyzer output as authoritative runtime truth.

## Deliverables

- Add deterministic `summary.status` to `PublicInterfaceIndex`.
- Define allowed index statuses:
  - `complete`: no diagnostics were emitted.
  - `partial`: diagnostics were emitted and at least one package record remains
    available for review.
  - `failed`: diagnostics were emitted and no package record is available.
- Validate `summary.status` as part of the existing summary equality check.
- Update Python and JavaScript/TypeScript analyzer tests to assert explicit
  complete/partial/failed status behavior.
- Add focused schema tests for summary status derivation and validation errors.
- Update drafting/docs/DocC references so partial analyzer evidence is visible
  in review context.
- Create `SPECS/INPROGRESS/P2-T3_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- Existing `PublicInterfaceIndex` summaries include `status`.
- No-diagnostic indexes report `complete`.
- Analyzer outputs with diagnostics and retained package records report
  `partial`.
- Analyzer outputs with diagnostics and no package records report `failed`.
- Validation rejects stale or incorrect `summary.status` values through the
  existing summary equality path.
- The drafter preserves the updated summary in public interface provenance.
- No repository code execution, dependency install, build tool execution,
  package script execution, or network access is introduced.
- Coverage must not decline from the P2-T2 baseline of 90.57%; add focused
  tests for new status branches rather than relying only on
  `--cov-fail-under=90`.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

Diagnostics and partial-index state are metadata about static analysis
coverage. They do not grant permission to execute harvested content, infer
runtime behavior, or publish generated specs as accepted registry truth.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Schema tests | Complete, partial, failed index fixtures | Failing tests for `summary.status` derivation and validation | `PYTHONPATH=src python -m pytest tests/test_interface_index.py` |
| Python analyzer tests | Valid and broken Python files | Failing assertions for `complete` and `partial` analyzer summaries | `PYTHONPATH=src python -m pytest tests/test_python_public_api.py` |
| JS/TS analyzer tests | Valid package, malformed root manifest, unreadable/missing entrypoints | Failing assertions for `complete`, `partial`, and `failed` summaries | `PYTHONPATH=src python -m pytest tests/test_js_ts_public_api.py` |
| Documentation | Updated summary semantics | Docs and DocC mention partial-index status | Review diff |
| Full validation | Repository gates | Validation report with coverage result >= 90.57% | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add schema tests for summary status and stale summary validation.
2. Add analyzer tests for complete/partial/failed status.
3. Implement summary status derivation and validation.
4. Update docs, DocC, and validation report.
5. Run targeted and full quality gates, with coverage explicitly compared to
   the P2-T2 90.57% baseline.

## Non-Goals

- No new parser implementation.
- No Tree-sitter integration.
- No sandbox implementation.
- No CLI analyzer orchestration command.
- No change to analyzer cache keying.
- No remote/shared cache.

---
**Archived:** 2026-05-17
**Verdict:** PASS
