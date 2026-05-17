# Next Task: P1-T2 — Add Python Static Public API Analyzer Using `ast`

**Priority:** P1
**Phase:** Public Interface Indexing
**Effort:** Medium
**Dependencies:** P1-T1
**Status:** Selected
**Selected:** 2026-05-17
**Branch:** `feature/P1-T2-python-static-public-api-analyzer`

## Description

Implement the first language-specific analyzer that emits
`PublicInterfaceIndex` package, entrypoint, symbol, diagnostic, and evidence
records from Python source files using the standard-library `ast` module.

## Expected Artifacts

- `src/spec_harvester/python_public_api.py`
- Tests covering deterministic Python public API extraction and diagnostics
- `SPECS/INPROGRESS/P1-T2_Add_Python_Static_Public_API_Analyzer_Using_ast.md`
- `SPECS/INPROGRESS/P1-T2_Validation_Report.md`

## Next Step

Run the PLAN command to generate the implementation-ready PRD.
