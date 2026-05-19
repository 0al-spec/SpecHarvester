# P10-T3 Trusted Classifier Evaluation

Status: In Progress
Created: 2026-05-19
Task: `P10-T3` Evaluate and integrate trusted language classification and
vendored/generated-file filtering from established tools such as GitHub
Linguist-compatible classifiers, `go-enry`, `Syft`, `ScanCode`, and Universal
Ctags where licensing and deterministic operation are acceptable.

## Problem

SpecHarvester now has a manifest-first `ProjectProfile`, but source-language
classification, vendored/generated filtering, package cataloging, license
scanning, and symbol extraction should not be reinvented wholesale. The project
needs a documented, deterministic integration boundary for trusted external
tools before any optional classifier is wired into harvest workflows.

## Goals

- Evaluate candidate tools for license compatibility, deterministic operation,
  trust boundary, output usefulness, and local-only execution.
- Add a machine-readable classifier registry that records approved, deferred,
  and rejected integration candidates.
- Define an adapter contract for optional classifier output that can enrich
  `ProjectProfile` without becoming registry authority.
- Keep default harvest behavior dependency-free and deterministic when external
  tools are unavailable.
- Add tests for registry shape, supported tool decisions, and fallback behavior.

## Non-Goals

- Do not require installing external tools in CI.
- Do not execute package managers, build systems, dependency installers, or
  harvested repository code.
- Do not make external classifier output authoritative over manifest evidence.
- Do not implement full Tree-sitter AST ingestion in this task.
- Do not change drafting behavior except through documented evidence contracts.

## Candidate Tools

- GitHub Linguist / `go-enry`: language classification plus vendored/generated
  filtering semantics.
- `Syft`: package/SBOM cataloging when local deterministic cataloging is useful.
- `ScanCode Toolkit`: license, package, and provenance metadata scanning.
- Universal Ctags: broad symbol extraction where tags output is deterministic.
- Tree-sitter: future parser substrate for deeper syntax indexing, not a direct
  P10-T3 runtime dependency.

## Acceptance Criteria

- Repository includes a reviewed classifier registry with license, trust,
  determinism, execution, network, and fallback notes for each candidate tool.
- `ProjectProfile` or analyzer policy exposes the registry/adapter contract
  without requiring external tools to exist.
- Manifest-first evidence remains primary when external classifier evidence is
  absent or lower confidence.
- Tests verify registry validity, approved/deferred status values, and that
  default harvest still succeeds without invoking external tools.
- Documentation clearly states that external classifier output is advisory
  untrusted metadata.

## Validation Plan

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
