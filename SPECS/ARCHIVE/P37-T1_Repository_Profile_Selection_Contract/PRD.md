# P37-T1 Repository Profile Selection Contract

## Motivation

Phase 36 proved that explicit parser profiles can improve evidence boundaries,
but operators still have to know which profile to choose. The FastMCP dry run
showed the next gap: a generic repository-wide run can over-include docs and
examples, while manually targeted member packages produce a better
author-ready starter package.

SpecHarvester needs a language- and framework-agnostic contract for deciding
which repository profile plugin, if any, should apply. That selection must be
explainable, reproducible, and reviewable rather than hidden inside ad hoc
heuristics.

## Goal

Document the repository profile selection contract before implementation. The
contract must define the common selection model:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

The contract should describe how ecosystem-specific plugins provide evidence
while the core SpecHarvester policy chooses, rejects, falls back, and records a
decision.

## Deliverables

- Add `docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md`.
- Add the DocC mirror for the same contract.
- Link the contract from the docs index, DocC root, capabilities, roadmap, and
  workplan-facing surfaces.
- Define the future `SpecHarvesterRepositoryProfileDetection` artifact shape
  without implementing it yet.
- Define selection inputs, candidate scoring, confidence levels, selection
  modes, override precedence, fallback behavior, diagnostics, and
  non-authority boundaries.
- Add docs-contract regression coverage for the new contract.

## Acceptance Criteria

- The contract is language- and framework-agnostic and does not make FastMCP,
  FastAPI, Python, or any other ecosystem normative.
- The contract defines explicit `auto`, `none`, and explicit profile-id
  selection modes.
- The contract states that explicit CLI and manifest overrides take precedence
  over auto-detection.
- The contract states that high-confidence, conflict-free evidence can select
  a profile automatically.
- The contract states that ambiguous, low-confidence, unsupported, or
  conflicting signals fall back to generic behavior with diagnostics.
- The contract defines a replayable decision artifact with selected profile,
  candidate profiles, evidence paths, rejected profiles, fallback profile,
  override source, diagnostics, and non-authority statements.
- The contract states that profile selection is producer-side evidence only.
- Docs, DocC, and regression tests reference the contract.

## Non-Goals

- Do not implement repository profile detection.
- Do not add a runtime plugin registry.
- Do not add a language-specific or FastMCP-specific profile.
- Do not modify autonomous candidate batch behavior.
- Do not clone/fetch repositories, install dependencies, execute harvested
  code, invoke package managers, run AI, draft packages, publish registry
  metadata, accept packages or relations, remove `preview_only`, or treat AI
  output or plugin decisions as registry truth.

## Dependencies

- P36-T1 repository parsing plugin contract.
- P36-T3 plugin-aware source classification hook.
- P36-T4 FastAPI parser profile rerun evidence.
- Phase 37 workplan entries from the merged planning PR.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift build --target SpecHarvesterDocs`
