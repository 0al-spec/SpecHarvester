# REVIEW — P16-T7 Pylint Duplicate-Code Backend

Subject: `p16_t7_pylint_duplicate_code_backend`
Date: 2026-05-25
Verdict: PASS

## Findings

No actionable findings.

## Review Notes

- The PR moves duplicate-code detection toward an established Python tool
  (`pylint` `R0801`) while preserving the stable
  `SpecHarvesterCodeDuplicationReport` contract.
- CI runs the new backend as advisory baseline collection only. This is the
  correct boundary because current source has `7` Pylint duplicate-code blocks.
- Missing `pylint` and malformed backend output fail closed with validation
  errors instead of false clean reports.
- The built-in detector remains available as a dependency-free fallback.
- `jscpd` is correctly deferred into a separate multi-language follow-up because
  it introduces npm dependency, licensing, output-shape, and CI policy decisions.

## Validation Reviewed

- Targeted tests: PASS, 35 passed.
- Full tests: PASS, 370 passed, 1 skipped.
- Coverage: PASS, 90.70%.
- Ruff lint and format: PASS.
- Swift manifest and docs target build: PASS.
- Pylint backend baseline: PASS, `7` duplicate blocks and `14` occurrences
  reported as advisory signals.

## Residual Risk

The CI baseline step currently prints and writes the report but does not persist
it as a workflow artifact. That is acceptable for P16-T7 because the task goal
is advisory integration; a later baseline-enforcement task should decide how to
persist and compare reports.
