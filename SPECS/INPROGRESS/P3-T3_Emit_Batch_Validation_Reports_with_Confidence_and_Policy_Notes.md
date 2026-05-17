# P3-T3 Emit Batch Validation Reports with Confidence and Policy Notes

Status: Planned
Selected: 2026-05-17
Branch: `feature/P3-T3-emit-batch-validation-reports-with-confidence-and-policy-notes`
Review subject: `p3_t3_batch_validation_reports`

## Objective

Add deterministic batch validation reports for `collect-batch` output. The
report must summarize collected snapshots, skipped records, confidence levels,
policy notes, and trust-boundary warnings so maintainers can inspect batch
results before drafting or promotion.

This task reports on already collected static evidence. It does not clone
repositories, access networks, run package managers, execute package scripts,
run analyzers, draft SpecPM packages, or promote candidates.

## Deliverables

- Add a deterministic batch validation report builder.
- Add confidence classification for each collected repository.
- Add policy notes derived from each `harvest.json` snapshot policy.
- Add warnings for review-relevant batch conditions such as non-pinned refs,
  skipped files, empty snapshots, missing package manifests, and policy
  mismatches.
- Include skipped manifest records in the report.
- Add a `collect-batch --report <path>` CLI option.
- Add tests for report structure, confidence levels, policy notes, skipped
  records, and CLI report writing.
- Update GitHub docs and DocC with report usage and trust boundary.
- Create `SPECS/INPROGRESS/P3-T3_Validation_Report.md` during EXECUTE.

## Proposed CLI

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

The command still prints the batch summary to stdout. When `--report` is
provided, it also writes a deterministic JSON report.

## Report Shape

The report should include:

- `schemaVersion`
- `kind`
- batch `input`, `outputRoot`, and `selectedIds`
- summary counts for collected, skipped, confidence, and warnings
- `records` for collected repository snapshots
- `skippedRecords` from batch selection
- static `trustBoundary` statements

Each record should include:

- repository id and output path
- source manifest provenance
- evidence counts
- `confidence`
- `confidenceReasons`
- `policyNotes`
- `warnings`

## Acceptance Criteria

- Report JSON is deterministic for the same batch output.
- Report records preserve deterministic collection order.
- Skipped records are included with reasons.
- Confidence is one of `high`, `medium`, or `low`.
- Policy notes explicitly reflect collector policy values from `harvest.json`.
- Warning codes are stable strings suitable for future automation.
- The report does not execute code, run analyzers, call networks, or inspect
  files beyond already prepared in-memory snapshots from `collect-batch`.
- Existing `collect-batch` behavior remains compatible when `--report` is not
  provided.
- Coverage must not decline from the P3-T2 result of 91.85%.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Report builder tests | Synthetic batch records and snapshots | Failing tests for confidence, policy notes, warnings, and skipped records | `PYTHONPATH=src python -m pytest tests/test_batch_validation_report.py` |
| CLI tests | Temp `inputs/*.yml`, local checkout fixtures, `--report` path | Failing test for report file creation through `collect-batch` | `PYTHONPATH=src python -m pytest tests/test_batch_collection.py -k report` |
| Implementation | Test expectations | `batch_validation.py`, CLI wiring, report path support | Targeted tests pass |
| Documentation | Report usage and trust boundary | Docs and DocC updated | Review diff |
| Full validation | Repository gates | Validation report with coverage result >= 91.85% | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add focused tests for deterministic report generation.
2. Implement batch validation report builder with stable warning codes.
3. Wire `collect-batch --report` through the CLI and batch API.
4. Update docs and DocC.
5. Run targeted and full quality gates, explicitly comparing coverage to the
   P3-T2 91.85% baseline.

## Non-Goals

- No repository cloning.
- No network access.
- No package-manager access.
- No package script execution.
- No public interface analyzer execution.
- No deterministic SpecPM drafting.
- No accepted package promotion.
- No standalone validator for arbitrary existing directories in this task.
