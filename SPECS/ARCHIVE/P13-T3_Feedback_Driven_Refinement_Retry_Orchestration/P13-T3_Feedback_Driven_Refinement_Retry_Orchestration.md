# P13-T3 Feedback-Driven Refinement Retry Orchestration

Status: Archived
Task: `P13-T3`
Phase: Phase 13. Prompted Refinement Quality Loop
Priority: P1
Effort: 8 hours
Dependencies: `P13-T2`
Archived: 2026-05-22
Verdict: PASS

## Problem

SpecHarvester now has first-pass `SpecNodeRefinementResult` validation and a
clean-context `SpecNodeSemanticReviewResult` quality gate. The remaining loop
gap is orchestration: semantic findings are review metadata, but there is no
deterministic controller that can turn those findings into bounded retry input,
preserve attempt linkage, cap retries, and record an audit trail.

Without this controller, a future retry implementation risks feeding ad-hoc
model context back into SpecNode, changing deterministic evidence between
attempts, retrying indefinitely, or letting review findings become unbounded
instructions.

## Goals

- Add a deterministic `SpecNodeRefinementRetryRun` controller for the prompted
  refinement quality loop.
- Convert `SpecNodeSemanticReviewFinding` records into bounded
  `SpecNodeRetryDirective` data.
- Reuse the original `SpecHarvesterSpecNodeArtifactBundle` and
  `SpecHarvesterRefinePreviewPlan` for every retry attempt.
- Cap retry attempts with an explicit retry policy.
- Preserve attempt linkage from initial refinement through semantic review and
  retry directives.
- Record an audit trail that can be validated without provider execution.
- Mirror the retry orchestration contract in GitHub docs and DocC.
- Add unit and docs tests for retry policy, directive generation, cap behavior,
  artifact immutability, and audit linkage.

## Non-Goals

- Do not call LM Studio, OpenAI, or any live SpecNode provider in tests.
- Do not apply generated patch proposals automatically.
- Do not let the semantic reviewer request retry directly; it emits findings
  only.
- Do not mutate deterministic evidence between attempts.
- Do not implement accepted-package promotion or SpecPM registry publication.

## Deliverables

- `docs/SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md`
- `Sources/SpecHarvester/Documentation.docc/SpecNodeRefinementRetryOrchestration.md`
- Cross-links from existing SpecNode contracts, architecture, workflow, and DocC
  root.
- `build_specnode_retry_directives(...)`.
- `run_specnode_refinement_retry_orchestration(...)`.
- `validate_specnode_refinement_retry_run(...)`.
- Tests for approval-without-retry, retry directive mapping, capped retry
  attempts, immutable artifact digests, audit trail linkage, and invalid retry
  run rejection.
- Docs contract tests for GitHub docs and DocC mirror coverage.

## Acceptance Criteria

- `approve` semantic review verdict terminates the run without retry.
- `needs_revision` and `reject` semantic review verdicts create bounded retry
  directives only from known finding codes.
- Retry directives cannot contain arbitrary prompt text, raw source, provider
  logs, shell commands, network fetches, package manager commands, test runner
  commands, build tool commands, or direct file writes.
- Every retry attempt references the same source bundle digest and preview plan
  digest unless the caller starts a new orchestration run.
- Retry attempts are capped by explicit `maxAttempts`.
- The audit trail records attempt index, refinement result digest, semantic
  review result digest, retry directive digest, verdict, and status.
- Validation rejects runs with digest drift, missing attempt linkage,
  unsupported directive codes, or attempts beyond the retry cap.
- Python tests, docs tests, lint, format, coverage, Swift package manifest, and
  Swift DocC target build pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_specnode_refinement_smoke.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
