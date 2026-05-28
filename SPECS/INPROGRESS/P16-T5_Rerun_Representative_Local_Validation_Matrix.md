# P16-T5 — Rerun Representative Local Validation Matrix

Branch: `feature/P16-T5-rerun-local-validation-matrix`
Review subject: `p16_t5_rerun_local_validation_matrix`

## Context

P15-T4 established a compact local real-repository validation matrix over six
operator-managed checkout paths under `~/Development/GitHub`. P16-T1 through
P16-T4 addressed several issues observed in that baseline:

- analyzer coverage undercount for generated `public-interface-index.json`;
- license provenance classification for collected license files;
- package identity and namespace/upstream normalization;
- broad language-neutral semantic intents counted as duplicate findings.

The matrix should now be rerun to measure whether advisory counts, analyzer
coverage, and failure classes improved without committing generated `.smoke/`
artifacts.

## Scope

- Reuse the representative P15-T4 repository set:
  `cupertino`, `navigation-split-view`, `xyflow`, `flask`, `gin`, and
  `docc2context`.
- Create ignored `.smoke/` inputs and outputs for the rerun.
- Run the local validation runner with interface-index emission and analyzer
  cache enabled.
- Build the structured quality report and smoke triage summary.
- Compare results against the P15-T4 baseline.
- Update the GitHub documentation page and DocC mirror with P16-T5 rerun
  outcomes.
- Commit only compact documentation, Flow artifacts, and validation summaries.

## Non-Goals

- Do not commit `.smoke/` inputs, generated candidates, raw harvested outputs,
  run reports, quality reports, or triage JSON.
- Do not clone new repositories.
- Do not run harvested repository tests, builds, package scripts, dependency
  installers, or package manager network operations.
- Do not invoke SpecNode, a model provider, or live LM Studio.
- Do not accept generated candidates into SpecPM.

## Acceptance Criteria

- At least the six P15-T4 repositories are attempted, or the validation report
  explains any unavailable checkout.
- The rerun records runner status, quality verdicts, analyzer coverage, SpecPM
  validation status, and advisory/failure-class deltas.
- Generated `.smoke/` artifacts remain ignored and uncommitted.
- GitHub docs and DocC mirror describe the P16-T5 rerun and the P15-T4
  comparison.
- Docs contract coverage is updated if needed.
- Full Flow quality gates pass.

## Validation Plan

- Strict public preflight: staged changes are absent in all selected checkout
  repositories.
- `PYTHONPATH=src python -m spec_harvester source-manifests .smoke/p16-t5-inputs`
- `PYTHONPATH=src python scripts/run_real_repository_validation.py --inputs .smoke/p16-t5-inputs --out .smoke/output/p16-t5-local-validation --emit-interface-indexes --analyzer-cache-dir .smoke/output/p16-t5-analyzer-cache --skip-specpm-validation`
- `PYTHONPATH=src python -m spec_harvester quality-report --run-report .smoke/output/p16-t5-local-validation/run-report.json --candidates-root .smoke/output/p16-t5-local-validation --output .smoke/output/p16-t5-local-validation/quality-report.json`
- Local SpecPM validation against the adjacent SpecPM checkout when available.
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
