# P39-T6 Real Multi-Repository Static Evaluator Validation

## Context

P39-T5 connected the deterministic repository plugin applicability evaluator to
`autonomous-candidate-batch` as explicit sidecar evidence. The integration is
covered by fixtures, but it still needs a real multi-repository validation pass
across representative local checkouts.

The validation should compare different repository shapes without expanding
authority:

- FastMCP-style documentation-heavy Python repository;
- FastAPI-style Python web framework repository;
- xyflow-style JavaScript/TypeScript workspace/package-set repository.

## Goal

Record a durable real-run comparison showing that the static evaluator and the
batch opt-in sidecar path behave consistently across real local repositories.

## Deliverables

- Reuse existing local checkouts when present; do not clone or fetch source.
- Run deterministic collection and static evaluator paths over representative
  repositories when the local checkout is available.
- Exercise both:
  - `repository-plugin-applicability-detect`;
  - `autonomous-candidate-batch --repository-plugin-registry
    --repository-plugin-static-evidence-envelope`.
- Add a machine-readable real-run fixture under
  `tests/fixtures/repository_plugins/real_runs/`.
- Add GitHub docs and DocC docs summarizing:
  - repositories checked;
  - revisions;
  - command surfaces exercised;
  - selected/fallback/blocked plugin decisions;
  - batch sidecar status and trust boundary;
  - any unavailable local checkout.
- Add docs-contract regression coverage for the fixture and docs.
- Archive the task through Flow and update `next.md`.

## Acceptance Criteria

- The fixture uses a stable identity and schema version.
- Each repository case records local checkout availability, revision if
  available, command surfaces exercised, evaluator summary, batch sidecar
  summary, and boundary statements.
- At least one available real checkout runs through both the standalone
  evaluator CLI and batch auto sidecar path.
- If a target checkout is unavailable, the fixture records that as
  `not_available` rather than cloning or fetching it.
- The generated batch sidecar keeps `sourceMode: auto_static_evaluator`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- Regression tests validate fixture shape, counts, and non-authority boundary.
- Existing Python, lint, format, coverage, Swift docs build, and DocC static
  generation gates pass.

## Non-Goals

- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not run package managers.
- Do not execute harvested code.
- Do not invoke AI.
- Do not change parser/profile behavior.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P39-T3 deterministic evaluator helper.
- P39-T4 `repository-plugin-applicability-detect` CLI.
- P39-T5 autonomous batch opt-in sidecar integration.
- Existing local checkouts for at least one representative repository.
