# P12-T3 Domain Intent Inference

Status: In Progress
Created: 2026-05-21
Task: `P12-T3` Improve domain intent inference from public interface indexes,
package metadata, README headings, and documentation evidence.

## Problem

Popular framework repositories such as Flask and Gin currently produce valid
candidate specs, but their generated intent claims can collapse to generic
`intent.api.contract_surface` or `intent.developer.tooling_surface` labels even
when deterministic evidence clearly describes web framework behavior.

Weak-model drafting should receive compact, ranked domain signals from static
evidence rather than having to infer domain semantics from raw source or broad
metadata.

## Goals

- Add deterministic domain intent signals for common web framework and HTTP
  server surfaces.
- Use existing harvested evidence: public interface indexes, package metadata,
  README headings, documentation snippets, and semantic evidence clusters.
- Preserve evidence provenance so generated intent claims can be audited.
- Improve Flask and Gin smoke output so generated candidates include meaningful
  web-framework/API-server intent claims when supported by static evidence.
- Keep behavior local-only and deterministic.

## Non-Goals

- Do not execute package code, package managers, test suites, build scripts, or
  network probes in harvested repositories.
- Do not add broad model-assisted refinement or SpecNode integration; that
  remains Phase 11 work.
- Do not change the SpecPM evidence-kind vocabulary or support-target grammar;
  those remain `P12-T4` and `P12-T5`.
- Do not claim accepted registry truth. Generated candidates remain preview-only
  until reviewed and accepted through SpecPM.

## Design

- Inspect current deterministic intent generation and semantic evidence flow.
- Add a small domain taxonomy layer for static signals that are strong enough to
  support specific intent IDs.
- Start with framework/API-server semantics that are observable from exported
  APIs and documentation terms:
  - route/router/routing;
  - middleware;
  - handler/request/response/context;
  - HTTP/server/web framework;
  - templating or JSON/API helpers when present.
- Rank specific domain intents ahead of generic fallback intents only when
  evidence support crosses a deterministic threshold.
- Keep fallback behavior unchanged when domain evidence is absent.

## Deliverables

- Updated deterministic intent inference implementation.
- Unit tests for Flask-like and Gin-like static evidence inputs.
- Regression tests proving generic fallback remains available for weak evidence.
- Documentation and DocC mirror updates for domain intent inference.
- Flask/Gin smoke rerun evidence in the validation report.

## Acceptance Criteria

- Flask-like evidence produces a specific web-framework/API-server intent rather
  than only generic API/tooling intents.
- Gin-like public interface evidence produces a specific web-framework/API-server
  intent from exported router, middleware, handler, and HTTP symbols.
- Generic repositories without domain evidence continue to produce conservative
  fallback intents.
- Intent support records cite deterministic evidence paths or analyzer outputs.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_semantic_evidence.py tests/test_draft.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- Local Flask/Gin smoke rerun if the `.smoke/inputs` entries and repository
  checkouts are available.
