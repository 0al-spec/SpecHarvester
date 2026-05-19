# P9-T2 Validation Report

## Result

PASS

## Scope

Validated deterministic semantic evidence indexing for domain-level draft intent
generation, with a SpecificationKit-like regression fixture and a real
SpecificationKit local smoke run.

## Quality Gates

- `ruff check src tests`: PASS.
- `ruff format --check src tests`: PASS.
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`: PASS, 58 passed.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: PASS, 177 passed, total coverage 90.62%.
- `swift package dump-package >/dev/null`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.

## Smoke Evidence

- Ran strict `collect-batch` for local `SpecificationKit`: PASS.
- Drafted `SpecificationKit`: PASS, `capabilityCount: 1`, `intentCount: 7`.
- Generated domain-level intents:
  - `intent.swift.context_driven_decisioning`
  - `intent.swift.feature_gating`
  - `intent.swift.macro_developer_experience`
  - `intent.swift.predicate_composition`
  - `intent.swift.reactive_specification_evaluation`
  - `intent.swift.specification_pattern`
  - `intent.swift.specification_tracing`
- Generated summary:
  `Provide a Swift Specification Pattern toolkit for composing reusable predicates, context-driven decisions, feature gates, reactive evaluation, and diagnostic tracing.`
- Generated `semanticEvidenceIndex` clusters with stable IDs, scores, matched
  terms, and evidence paths.
- Governance, namespace/upstream, license provenance, and smoke triage reports
  for `SpecificationKit` all returned `status: ok`.

## Trust Boundary

- No harvested repository code, package scripts, dependency installers, tests, or
  network probes were executed.
- The semantic evidence index is deterministic and built from allowlisted static
  evidence only.
- Generated candidates remain `preview_only` and require review before registry
  acceptance.
