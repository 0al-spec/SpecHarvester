# P29-T3 Corpus Baseline and Gap Report

## Objective

Record the first mixed local corpus run for `autonomous-candidate-batch` as a
durable baseline. The baseline should cover Flask, Gin, and xyflow, preserve
the observed deterministic and live LM Studio outcomes, and classify the
concrete gaps that drive P29-T4 and P29-T5.

This task does not implement the fallback or model repair logic. It records
the evidence and expected next decisions.

## Deliverables

- Machine-readable example baseline artifact for the Flask/Gin/xyflow corpus.
- GitHub docs page explaining the baseline, outcomes, and product verdict.
- DocC mirror and navigation links.
- Workplan/next-task updates that keep the Phase 29 stack moving.
- Regression docs-contract coverage.
- Validation report and Flow archive/review artifacts.

## Acceptance Criteria

- The baseline records deterministic `--skip-ai` results:
  - Flask: `0` candidates, `0` relations, preflight `passed`,
    `single_package_fallback_needed`.
  - Gin: `0` candidates, `0` relations, preflight `passed`,
    `single_package_fallback_needed`.
  - xyflow: `4` candidates, `3` relations, preflight `passed`,
    `stop_for_author_review`.
- The baseline records live LM Studio status:
  - Flask/Gin AI draft and enrichment completed but produced no proposal
    subjects.
  - xyflow observed malformed model JSON and is classified as
    `ai_json_repair_needed`.
- The report states that no generated preview candidate is promoted to SpecPM
  acceptance.
- The product verdict separates pipeline health from candidate quality.
- The report points to P29-T4 and P29-T5 as implementation follow-ups.

## Test-First Plan

1. Add docs-contract assertions for the new baseline page, DocC mirror,
   machine-readable fixture, and next-task state.
2. Add fixture-shape assertions for repository ids, candidate counts, gap
   codes, and non-authority boundary fields.
3. Implement the fixture and docs until targeted tests pass.
4. Run the broader Flow validation gates.

## Execution Plan

### Phase 1 — Baseline Artifact

Inputs:

- Local corpus run results from Flask, Gin, and xyflow.
- `AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`.
- `AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`.

Outputs:

- `tests/fixtures/autonomous_candidate_corpus_baseline/flask-gin-xyflow.example.json`

Verification:

- Fixture test checks identity, repository summaries, gap codes, and
  non-authority boundary.

### Phase 2 — Human-Readable Baseline

Inputs:

- Baseline fixture.
- Existing docs and DocC navigation.

Outputs:

- `docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`
- `Sources/SpecHarvester/Documentation.docc/AutonomousCandidateCorpusBaseline.md`
- Links from docs index, roadmap, autonomous batch, intake policy, and tech debt
  plan.

Verification:

- Docs-contract tests cover required vocabulary and links.

### Phase 3 — Flow Closure

Inputs:

- Completed docs, fixture, and tests.

Outputs:

- `SPECS/INPROGRESS/P29-T3_Validation_Report.md`
- Archived P29-T3 folder.
- Review report and archived review report.

Verification:

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

## Notes

The next implementation tasks remain:

- `P29-T4` single-package candidate fallback.
- `P29-T5` LM Studio JSON repair/retry.
- `P29-T6` corpus quality gate after fallback and retry support.
