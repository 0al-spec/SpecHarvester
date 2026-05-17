# P1-T4 Evaluate Tree-sitter as the Shared Syntax Indexing Layer

Status: Planned
Selected: 2026-05-17
Branch: `feature/P1-T4-evaluate-tree-sitter-syntax-indexing-layer`
Review subject: `p1_t4_tree_sitter_syntax_indexing_layer`

## Objective

Evaluate whether Tree-sitter should become SpecHarvester's shared syntax
indexing layer for future public interface analyzers. The output must be a
reviewable engineering decision artifact that covers trust boundary, parser
packaging, deterministic output, source provenance, diagnostics, and whether
Tree-sitter should replace or complement the existing Python AST and
JavaScript/TypeScript manifest/export analyzers.

This task does not add Tree-sitter as a runtime dependency and does not
implement a Tree-sitter analyzer.

## Deliverables

- Add `docs/TREE_SITTER_EVALUATION.md`.
- Add a DocC mirror page under `Sources/SpecHarvester/Documentation.docc/`.
- Link the evaluation from `docs/README.md` and the DocC topic index.
- Record primary-source references with a verification date.
- Define a recommendation for P1-T5 and later analyzer/cache tasks.
- Create `SPECS/INPROGRESS/P1-T4_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- The evaluation explicitly states whether Tree-sitter should replace or
  complement current language-specific analyzers.
- The evaluation covers:
  - trust boundary and sandbox expectations;
  - parser/runtime packaging options;
  - deterministic output requirements;
  - query design and language grammar drift;
  - diagnostics for syntax errors and parser failures;
  - cache implications for P2 tasks;
  - licensing/provenance notes.
- The recommendation is actionable for P1-T5 and does not require running
  untrusted package code.
- DocC build succeeds after adding the mirror page.
- Flow quality gates from `.flow/params.yaml` pass.

## Source Review Scope

Use primary sources only for Tree-sitter facts:

- Tree-sitter repository and official documentation.
- py-tree-sitter documentation.
- Official Tree-sitter language grammar repositories for Python,
  JavaScript, and TypeScript.

## Trust Boundary

The evaluation may inspect public documentation and local repository files. It
must not install Tree-sitter packages, compile grammars, execute harvested
repository code, run package managers, or add network-dependent validation.

## Execution Plan

1. Summarize current analyzers and constraints from P1-T2/P1-T3.
2. Verify Tree-sitter facts from primary sources.
3. Author the GitHub-facing evaluation document.
4. Add the DocC mirror page and index link.
5. Run all configured quality gates.

## Non-Goals

- No Tree-sitter dependency in `pyproject.toml`.
- No generated parser artifacts.
- No Tree-sitter query implementation.
- No analyzer cache implementation.
- No replacement of existing Python or JavaScript/TypeScript analyzers.
