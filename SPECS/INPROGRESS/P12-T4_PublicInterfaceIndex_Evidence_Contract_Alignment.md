# P12-T4 PublicInterfaceIndex Evidence Contract Alignment

Status: In Progress
Created: 2026-05-21
Task: `P12-T4` Align `PublicInterfaceIndex` evidence with the SpecPM
validation contract.

## Problem

Generated candidates can include a `public_interface_index` evidence record:

```yaml
evidence:
  - id: public_interface_index
    kind: public_interface_index
    path: public-interface-index.json
```

Current SpecPM validation does not recognize `public_interface_index` as an
accepted evidence kind, so candidate validation emits an avoidable advisory
warning even when the interface index itself is deterministic and valid.

Until SpecPM's vocabulary is updated, SpecHarvester should emit a contract-safe
evidence kind while preserving enough metadata for reviewers to recognize the
artifact as a generated `PublicInterfaceIndex`.

## Goals

- Eliminate the avoidable SpecPM warning caused by
  `kind: public_interface_index`.
- Preserve generated interface index provenance, media type, path, analyzer
  summary, and supported BoundarySpec targets.
- Keep the emitted candidate compatible with the current SpecPM validation
  contract.
- Document the transitional mapping so reviewers understand that the artifact is
  still a `PublicInterfaceIndex`.

## Non-Goals

- Do not change SpecPM's canonical evidence-kind vocabulary in this repository.
- Do not remove `public-interface-index.json` from generated candidate output.
- Do not solve the separate `provides.capabilities.intentIds` support-target
  warning; that remains `P12-T5`.
- Do not execute harvested repository code, package managers, tests, builds,
  package scripts, or network probes.

## Design

- Keep `id: public_interface_index` stable for review tooling and generated
  candidate readability.
- Change the emitted evidence `kind` to a currently accepted generic artifact
  kind if the current SpecPM contract supports one.
- Add explicit metadata fields to preserve the original generated artifact type,
  media type, and schema identity.
- Add tests that prove generated specs no longer contain
  `kind: public_interface_index` while still emitting `public-interface-index.json`
  and interface support links.
- Run SpecPM validation on a candidate with interface evidence to confirm the
  evidence-kind warning is gone.

## Deliverables

- Drafter evidence emission update.
- Unit/regression tests for interface evidence shape.
- Documentation and DocC mirror updates explaining the transitional mapping.
- Flow validation report with SpecPM validation smoke result.

## Acceptance Criteria

- Generated candidates with `PublicInterfaceIndex` evidence do not emit
  `kind: public_interface_index` in BoundarySpec evidence records.
- The evidence record still identifies the artifact as a generated
  `PublicInterfaceIndex` through explicit metadata.
- SpecPM validation no longer warns about an unknown evidence kind for
  `public-interface-index.json`.
- P12-T5 remains tracked for the separate support-target warning.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- Local Flask/Gin or synthetic candidate validation with interface evidence.
