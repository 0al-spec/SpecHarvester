# P55-T9 Validation Report

## Result

PASS

P55-T9 successfully executed the frozen targeted calibration and produced a
complete provider-separated decision record. The calibration result does not
unblock P55-T10 because neither provider met the frozen quality gates.

## Calibration Result

| Provider | Completed | Failed | Purpose accuracy | Evidence support | Schema validity | Edit burden |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex 5.3 Spark | 4/4 | 0/4 | 0.25 | 1.00 | 1.00 | 0.625 |
| LM Studio `openai/gpt-oss-20b` | 0/4 | 4/4 | 0.00 | 0.00 | 0.00 | 1.00 |

- Codex produced four schema-valid, evidence-bound proposals, but only the
  `openai/codex` purpose matched every frozen concept group. Exact token
  matching no longer accepts rubric terms embedded inside identifiers.
- All four LM Studio outputs failed proposal-schema validation because schema
  references or pointer-like objects appeared where proposal values were
  required.
- Failed records contribute maximal edit burden. LM Studio's four failures
  therefore record `1.00` instead of an understated `0.00`.

## Decision

- `p55T10Unblocked: false`
- `thresholdsRedefined: false`
- Frozen policy digest:
  `687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82`
- No proposal was accepted, materialized, promoted, or published.

A bounded provider-output-conformance follow-up and an exact rerun of this
target set are required before P55-T10.

## Durable Artifacts

- Target rubric:
  `tests/fixtures/targeted_semantic_calibration/p55-t9-target-rubric.example.json`
- Repeatable runner: `scripts/run_p55_t9_calibration.py`
- Normalized evidence:
  `SPECS/EVIDENCE/P55-T9/P55-T9_Targeted_Semantic_Quality_Calibration.json`
- GitHub Markdown and DocC result documentation.
- Regression tests for target accounting, frozen-policy binding, failure
  denominators, privacy, and the P55-T10 decision.

The evidence file SHA-256 is
`2c5f74daa4cd30ffd91c2d3e8479285b9e9970f1cede0f7c78726fbf9c1c3834`.
It excludes raw prompts, raw responses, hidden reasoning, credentials, and
machine-local paths.

## Validation

- Real provider-separated calibration:
  - completed with eight accounted target/provider records;
  - recorded Codex 5.3 Spark `4/4` complete and LM Studio `0/4` complete;
  - recorded P55-T10 as blocked without changing thresholds.
- `uv run pytest -q tests/test_targeted_semantic_calibration.py tests/test_portable_semantic_proposal.py tests/test_docs_contracts.py`
  - `237 passed`
- `uv run pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90 -q`
  - `1266 passed, 1 skipped`
  - total coverage: `90.00%`
- `uv run ruff check src tests scripts/run_p55_t9_calibration.py`
  - passed
- `uv run ruff format --check src tests scripts/run_p55_t9_calibration.py`
  - `184 files already formatted`
- `git diff --check`
  - passed
- JSON evidence and fixture parsing
  - passed
- `swift package dump-package`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- DocC static documentation build
  - passed with the repository's existing unhandled-resource warning

## Boundary Verification

The run verified clean retained checkouts at the exact P53 manifest revisions
before using pinned P53 sources and P53-T14 candidates. It did not
clone or fetch repositories, execute harvested code, install dependencies,
invoke package managers for harvested repositories, mutate SpecPM accepted
sources, change registry truth, publish packages, or grant either provider
review or materialization authority.
