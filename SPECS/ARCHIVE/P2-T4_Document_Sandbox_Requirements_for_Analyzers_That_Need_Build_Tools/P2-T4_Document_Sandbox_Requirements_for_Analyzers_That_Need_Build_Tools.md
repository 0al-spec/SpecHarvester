# P2-T4 Document Sandbox Requirements for Analyzers That Need Build Tools

Status: Planned
Selected: 2026-05-17
Branch: `feature/P2-T4-document-sandbox-requirements-for-analyzers-that-need-build-tools`
Review subject: `p2_t4_analyzer_sandbox_requirements`

## Objective

Document the requirements for future analyzers that cannot remain purely static
and need metadata-only build tools, while preserving SpecHarvester's trust
boundary: no package scripts, no harvested dependency installation, no network
access, no host secret access, and no untrusted repository code execution.

This task is documentation and contract-test work. It must not implement a
sandbox runtime, add build-tool analyzer execution, or loosen current analyzer
policy defaults.

## Deliverables

- Add a GitHub-facing analyzer sandbox requirements document.
- Add a matching DocC page and link it from the DocC architecture topics.
- Update trust-boundary and architecture docs to reference the sandbox
  requirements.
- Add lightweight documentation contract tests that check required sandbox
  invariants remain present.
- Create `SPECS/INPROGRESS/P2-T4_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- The document distinguishes `execution: none`, `metadata_tool_only`, and
  `build_tool_sandboxed`.
- The document defines mandatory controls for sandboxed analyzers:
  no network, no package scripts, no harvested dependency installation, no
  secret access, pinned analyzer/tool identity, bounded filesystem inputs,
  deterministic output, source digest evidence, diagnostics on failure, and
  audit logging.
- The document states that `collect-local` still does not run analyzers.
- The document states that sandboxed analyzer output remains untrusted
  evidence, not runtime truth or registry authority.
- GitHub docs and DocC include links to the sandbox requirements.
- Documentation contract tests pass.
- Coverage must not decline from the P2-T3 baseline of 90.62%.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

Build-tool analyzers are future optional components. They must be explicitly
marked and isolated before use. Repository-owned scripts, tests, package
managers, dependency installs, dynamic imports, and network probes remain
forbidden unless a future task defines a stronger sandbox policy and updates
the analyzer policy intentionally.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Contract tests | Expected doc paths and required terms | Failing tests for missing sandbox requirements | `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py` |
| Documentation | Sandbox requirements | GitHub doc, DocC mirror, navigation links | Contract tests pass |
| Full validation | Repository gates | Validation report with coverage result >= 90.62% | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add documentation contract tests for required sandbox terms.
2. Add `docs/ANALYZER_SANDBOX_REQUIREMENTS.md`.
3. Add `Sources/SpecHarvester/Documentation.docc/AnalyzerSandboxRequirements.md`.
4. Link the new page from trust-boundary, architecture, and DocC topic pages.
5. Run targeted and full quality gates, explicitly comparing coverage to the
   P2-T3 90.62% baseline.

## Non-Goals

- No sandbox runtime implementation.
- No analyzer orchestration command.
- No build-tool analyzer execution.
- No network or package manager integration.
- No dependency installation.
- No changes to default `collect-local` behavior.
- No changes to analyzer cache keying.

---
**Archived:** 2026-05-17
**Verdict:** PASS
