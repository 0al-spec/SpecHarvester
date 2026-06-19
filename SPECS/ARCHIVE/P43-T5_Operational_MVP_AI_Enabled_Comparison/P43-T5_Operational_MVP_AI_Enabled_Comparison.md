# P43-T5 Operational MVP AI-Enabled Comparison

## Status

Planned.

## Motivation

P43-T4 records the static-only operational MVP baseline over the pinned local
xyflow, FastAPI, and Gin corpus. P43-T5 needs to compare that baseline with
AI-enabled proposal mode when a local OpenAI-compatible provider is available.

The task must keep AI assistance proposal-only. If a provider is unavailable,
the comparison should record that fact explicitly instead of changing provider
policy, silently falling back to non-local AI, or pretending that AI ran.

## Goal

Record an AI-enabled comparison artifact for the same pinned corpus used by
P43-T4, including either real proposal-mode deltas from a local
OpenAI-compatible provider or an explicit provider-unavailable result.

## Deliverables

- Machine-readable AI-enabled comparison fixture under the operational MVP
  validation fixture layout.
- Linkage to the P43-T4 static-only baseline fixture and the P43-T2/P43-T3
  operational validation contracts.
- Provider availability evidence for the configured local OpenAI-compatible
  endpoint.
- Per-repository comparison records for xyflow, FastAPI, and Gin with
  static-only baseline status, AI-enabled proposal status, deltas or skipped
  reasons, proposal-only warnings, stop-policy outcome, and SpecPM handoff
  implications.
- GitHub documentation describing the comparison artifact, provider gate,
  proposal-only boundary, and no-authority constraints.
- DocC mirror and index/capability/roadmap links.
- Docs-contract regression coverage for fixture identity, baseline linkage,
  provider availability, per-repository comparison status, proposal-only
  authority, and non-authority boundaries.
- Validation report for this task.

## Provider Boundary

The only allowed AI endpoint is a local OpenAI-compatible provider such as LM
Studio. The task must not call hosted AI services, use network discovery,
persist raw prompts or raw provider responses, accept AI output as registry
truth, or mutate accepted SpecPM metadata.

Provider-unavailable is an acceptable result when recorded explicitly with:

- configured base URL;
- configured model policy;
- probe status and failure reason;
- no AI proposal artifacts;
- unchanged static-only baseline and handoff state.

## Acceptance Criteria

- The comparison uses the same pinned corpus as P43-T4.
- The artifact references the P43-T4 baseline fixture with a pinned digest.
- Provider availability or unavailability is machine-readable.
- AI-enabled output, when run, remains proposal-only and review-only.
- If no provider is available, every repository records `status:
  provider_unavailable` or an equivalent explicit skipped state.
- No package acceptance, relation acceptance, baseline seeding, `preview_only`
  removal, registry publishing, adapter execution, package-manager invocation,
  dependency installation, clone/fetch, or harvested-code execution occurs.
- Documentation and tests prove that AI comparison output is not registry
  authority.
- `SPECS/INPROGRESS/next.md` advances to P43-T6 after archive.

## Non-Goals

- Do not enable trusted local adapter execution.
- Do not run adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested repository code.
- Do not call hosted AI services.
- Do not persist raw prompt or response content.
- Do not publish registry metadata.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat AI output as registry truth.

## Validation Plan

- Provider availability probe for the local OpenAI-compatible endpoint.
- `python3 -m json.tool` for the AI comparison fixture.
- Targeted docs-contract regression tests for the comparison fixture.
- Full docs-contract suite.
- `PYTHONPATH=src python -m pytest`.
- `ruff check src tests`.
- `ruff format --check src tests`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`.
- `swift package dump-package`.
- `swift build --target SpecHarvesterDocs`.
- `git diff --check`.

---
**Archived:** 2026-06-20
**Verdict:** PASS
