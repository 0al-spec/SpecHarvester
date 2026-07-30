# P55-T9 Validation Report

## Result

PASS

P55-T9 successfully executed the frozen targeted calibration and produced a
complete provider-separated decision record. The calibration result does not
unblock P55-T10 because neither provider met the frozen quality gates.

## Calibration Result

| Provider | Completed | Failed | Purpose accuracy | Evidence support | Schema validity | Edit burden |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex 5.3 Spark | 2/4 | 2/4 | 0.25 | 0.50 | 0.50 | 0.125 |
| LM Studio `openai/gpt-oss-20b` | 0/4 | 4/4 | 0.00 | 0.00 | 0.00 | 0.00 |

- Codex produced one purpose-accurate `openai/codex` proposal and one
  schema-valid but purpose-inaccurate `rtk-ai/rtk` proposal. The latter also
  violated the candidate capability namespace.
- Codex outputs for `ripgrep` and `claude-mem` failed proposal-schema
  validation.
- All four LM Studio outputs failed proposal-schema validation because schema
  references or pointer-like objects appeared where proposal values were
  required.
- Failed records remain in the gate denominator. LM Studio's zero edit burden
  therefore is not a quality pass.

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
`f470de471e8957f06c8f5df0c6b9d765b37fbb2a4c8a7e8f45ec36e5fcf728bc`.
It excludes raw prompts, raw responses, hidden reasoning, credentials, and
machine-local paths.

## Validation

- Real provider-separated calibration:
  - completed with eight accounted target/provider records;
  - recorded Codex 5.3 Spark `2/4` complete and LM Studio `0/4` complete;
  - recorded P55-T10 as blocked without changing thresholds.
- `uv run pytest -q tests/test_targeted_semantic_calibration.py tests/test_portable_semantic_proposal.py tests/test_docs_contracts.py`
  - `232 passed`
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

The run used retained pinned P53 sources and P53-T14 candidates. It did not
clone or fetch repositories, execute harvested code, install dependencies,
invoke package managers for harvested repositories, mutate SpecPM accepted
sources, change registry truth, publish packages, or grant either provider
review or materialization authority.
