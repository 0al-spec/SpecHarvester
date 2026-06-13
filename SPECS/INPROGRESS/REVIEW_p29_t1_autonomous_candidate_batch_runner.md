# REVIEW: P29-T1 Autonomous Candidate Batch Runner

**Status:** PASS
**Reviewed:** 2026-06-13

## Scope

Reviewed the P29-T1 implementation for an MVP autonomous candidate batch runner:

- `autonomous-candidate-batch` CLI command.
- `SpecHarvesterAutonomousCandidateBatchReport` output.
- deterministic package-set collection/draft/preflight orchestration.
- optional local LM Studio AI draft/enrichment proposals.
- `autonomous_popular_mvp` role selection profile.
- docs, DocC, Workplan, archive, and contract tests.

## Findings

No blocking findings.

## Residual Risks

- The runner produces reviewable preview evidence only. It does not define the
  SpecPM intake/acceptance policy for autonomous batch output.
- AI semantic quality remains proposal-only and depends on maintainer or author
  review before any registry authority is granted.
- Repository acquisition is intentionally out of scope: the runner consumes
  local public checkouts and source manifests, but does not clone repositories.

## Follow-Up

Proceed with `P29-T2 SpecPM Candidate-Layer Intake Policy` so SpecPM can define
how autonomous preview batches, AI proposals, author-ready summaries, and
package-set bundles enter maintainer review without becoming accepted truth.

## Validation Reviewed

- `PYTHONPATH=src python -m pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py tests/test_autonomous_candidate_batch.py tests/test_package_set_drafter.py -q`
- `ruff check src tests`
- `ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- DocC static generation
- local LM Studio smoke with `openai/gpt-oss-20b`
- real `xyflow` smoke over local checkout
