# P12-T5 Evidence Support Target Contract Alignment

Status: In Progress
Created: 2026-05-21
Task: `P12-T5` Remove or remap generated evidence support targets that SpecPM
does not currently declare.

## Problem

Generated candidates can include semantic evidence like:

```yaml
evidence:
  - id: semantic_intent_static_evidence
    kind: documentation
    supports:
      - intent.summary
      - provides.capabilities.intentIds
```

Current SpecPM validation derives allowed evidence support targets from
BoundarySpec structural fields and declared document IDs. It does not declare
`provides.capabilities.intentIds`, so otherwise valid generated candidates can
emit an avoidable `evidence_support_target_unknown` warning.

## Goals

- Remove generated `provides.capabilities.intentIds` support targets.
- Preserve semantic evidence provenance for generated intent and capability
  claims by targeting declared BoundarySpec fields.
- Ensure candidates with `semantic_intent_static_evidence` validate without
  avoidable support-target warnings under SpecPM `0.2.0`.
- Extend tests and CI so the warning cannot regress silently.

## Non-Goals

- Do not change SpecPM's support-target grammar in this repository.
- Do not remove `semantic_intent_static_evidence` or `semanticEvidenceIndex`.
- Do not change deterministic intent inference rules.
- Do not execute harvested repository code, package managers, tests, builds,
  package scripts, or network probes.

## Design

- Keep `intent.summary` because it is a declared SpecPM support target.
- Replace `provides.capabilities.intentIds` with declared targets:
  `provides.capabilities` and `provides.capabilities.<capability_id>` for each
  generated capability.
- Add regression tests that generated specs no longer contain
  `provides.capabilities.intentIds` and that semantic evidence points to known
  capability targets.
- Extend SpecPM integration coverage so CI validates a candidate that includes
  `semantic_intent_static_evidence` and fails on
  `evidence_support_target_unknown`.
- Update GitHub docs and DocC mirrors to describe the declared-target contract.

## Deliverables

- Drafter evidence support-target update.
- Unit/regression tests for semantic evidence support targets.
- CI SpecPM integration fixture exercising `semantic_intent_static_evidence`.
- Documentation and DocC mirror updates.
- Flow validation report with SpecPM validation smoke result.

## Acceptance Criteria

- Generated candidates do not emit `provides.capabilities.intentIds`.
- Semantic evidence keeps provenance by supporting declared capability targets.
- Local SpecPM validation on a semantic-evidence candidate has no
  `evidence_support_target_unknown` warning.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- Local SpecPM validation of a generated candidate containing
  `semantic_intent_static_evidence`.
