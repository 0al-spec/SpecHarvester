# P12-T6 Popular Repository Smoke Scenario Promotion

Status: Archived
Created: 2026-05-21
Task: `P12-T6` Promote the Flask/Gin popular-repository smoke scenario into
reproducible local smoke documentation or synthetic tests.

## Problem

Recent hardening work validated Flask/Gin-style popular repositories through
manual `.smoke/` runs. Those runs proved important behaviors across strict
license handling, Python/Go analyzer orchestration, web-framework intent
inference, SpecPM validation warnings, and governance triage output.

The evidence currently lives in archived validation reports and local ignored
outputs. That is useful historically, but it is not a durable regression guard
or a convenient operator recipe.

## Goals

- Add committed synthetic coverage for Flask-like and Gin-like repository
  shapes without cloning real repositories or committing generated `.smoke/`
  output.
- Cover Python strict public collection with `LICENSE.txt`.
- Cover Go module collection and static public interface evidence without
  executing `go`, package scripts, tests, builds, or network probes.
- Verify generated web-framework/domain intents for both scenarios.
- Verify current SpecPM warning expectations: generated candidates should no
  longer include the avoidable evidence-kind or support-target warning sources.
- Verify governance report and smoke triage summary production for the
  generated candidates.
- Document the reproducible real-checkout operator workflow in GitHub docs and
  DocC.

## Non-Goals

- Do not commit generated `.smoke/` outputs.
- Do not clone, fetch, install dependencies, run package managers, run package
  scripts, run tests, build harvested projects, or execute harvested code.
- Do not accept or promote generated candidates into a SpecPM registry source.
- Do not require external Flask/Gin checkouts for the committed test suite.

## Design

- Add a dedicated synthetic popular smoke test that creates minimal Flask-like
  and Gin-like local checkouts under `tmp_path`.
- Run `collect-batch` with `--emit-interface-indexes` equivalent options so
  Python and Go public interface indexes are produced through deterministic
  static analyzers.
- Draft both generated candidates and assert web-framework, routing,
  middleware, request/response context, API contract, tooling, workflow, and
  documentation intent claims are present where expected.
- Assert generated specs do not contain `kind: unknown`,
  `provides.capabilities.intentIds`, or other known avoidable warning sources.
- Generate duplicate-claim, namespace/upstream, license/provenance, and smoke
  triage reports from the synthetic candidates.
- Extend `LOCAL_SMOKE_FIXTURES.md` and its DocC mirror with a popular
  Flask/Gin recipe and expected outputs.

## Deliverables

- Synthetic Flask/Gin popular smoke regression test.
- GitHub local smoke documentation update.
- DocC local smoke documentation mirror update.
- Documentation contract updates if needed.
- Flow validation report.

## Acceptance Criteria

- Synthetic Flask/Gin smoke coverage runs under pytest without external
  repositories.
- Flask-like strict public fixture with `LICENSE.txt` collects successfully.
- Gin-like Go module fixture emits deterministic public interface evidence.
- Both generated candidates include meaningful web-framework/domain intents.
- Governance reports and smoke triage summary are generated and validated.
- Docs describe how to reproduce the real-checkout `.smoke/` scenario while
  keeping generated outputs ignored.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_popular_repository_smoke.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

---

**Archived:** 2026-05-21
**Verdict:** PASS
