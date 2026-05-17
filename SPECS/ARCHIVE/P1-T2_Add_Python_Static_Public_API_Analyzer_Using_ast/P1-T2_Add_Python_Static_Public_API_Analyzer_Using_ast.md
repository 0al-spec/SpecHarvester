# P1-T2 Add Python Static Public API Analyzer Using `ast`

Status: Planned
Selected: 2026-05-17
Branch: `feature/P1-T2-python-static-public-api-analyzer`
Review subject: `p1_t2_python_static_public_api_analyzer`

## Objective

Implement the first language-specific public interface analyzer for
SpecHarvester. The analyzer must inspect Python source files with the
standard-library `ast` module and emit a `PublicInterfaceIndex` without
executing repository code, importing harvested modules, installing
dependencies, or making network calls.

This task creates a standalone analyzer surface for future integration. It does
not wire the analyzer into `collect-local`, `draft`, or CLI commands.

## Deliverables

- Add `src/spec_harvester/python_public_api.py`.
- Add tests in `tests/test_python_public_api.py`.
- Emit a `SpecHarvesterPublicInterfaceIndex` with analyzer policy metadata.
- Walk Python source files deterministically while skipping common generated,
  virtual environment, cache, and VCS directories.
- Extract public module-level functions, classes, constants, variables, and
  explicit `__all__` exports.
- Record parse errors as diagnostics instead of failing the whole analysis.
- Attach file evidence with relative path and SHA-256 digest.
- Create `SPECS/INPROGRESS/P1-T2_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- Analyzer output validates with `validate_public_interface_index`.
- Output is deterministic for the same source tree.
- Public names skip leading-underscore declarations unless exported by
  `__all__`.
- Function signatures are derived from AST argument structure without importing
  modules.
- Class symbols are emitted as public symbols; public class methods are emitted
  with `ClassName.method_name` names.
- Syntax errors produce `diagnostics[]` with level `error`, path, message, and
  evidence.
- Analyzer metadata declares `execution: none`, `networkAccess: none`,
  `packageScripts: not_run`, and `confidence: high`.

## Trust Boundary

The analyzer may read source bytes and parse them with `ast.parse`. It must not
execute files, import harvested modules, evaluate annotations, run package
managers, or inspect runtime objects.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Analyzer tests | Small temp Python package fixtures | Failing tests for public symbol extraction and diagnostics | `PYTHONPATH=src python -m pytest tests/test_python_public_api.py` |
| Implementation | Test expectations and `interface_index.py` | `python_public_api.py` | Targeted tests pass |
| Full validation | Repository gates | Validation report | Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add tests for deterministic extraction of functions, classes, methods,
   constants, variables, `__all__`, evidence, and summary counts.
2. Add tests for ignored private names and parse diagnostics.
3. Implement deterministic file discovery and AST symbol extraction.
4. Validate analyzer output through `validate_public_interface_index`.
5. Run Flow quality gates and record results.

## Non-Goals

- No CLI command or `collect-local` integration.
- No JavaScript, TypeScript, Swift, Rust, Go, or Tree-sitter analyzers.
- No type resolution beyond AST shape.
- No runtime imports or execution.

---
**Archived:** 2026-05-17
**Verdict:** PASS
