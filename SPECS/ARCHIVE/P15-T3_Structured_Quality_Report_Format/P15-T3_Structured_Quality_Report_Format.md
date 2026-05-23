# P15-T3 Structured Quality Report Format

Status: Archived
Archived: 2026-05-23
Verdict: PASS
Task: `P15-T3`
Phase: Phase 15. Real Repository Refinement Validation
Priority: P1
Effort: 3-5 hours
Dependencies: `P15-T2`

## Problem

The P15-T2 runner (`scripts/run_real_repository_validation.py`) produces a
step-execution JSON report that tracks which commands ran and whether they
succeeded.  That report does not capture the semantic quality of SpecHarvester
output: it cannot answer questions like "was the package intent plausible?",
"did the capability list have good evidence coverage?", or "how wide was the
deterministic analyzer coverage for this language?".

Operators need a distinct, structured quality report that captures those
dimensions for every package in a validation run, includes human-review notes,
and stays composable with the existing execution report.

## Goals

- Define a typed quality report schema for real-repository refinement runs.
- Cover all dimensions listed in the Workplan:
  - package intent accuracy
  - capability/evidence support quality
  - SpecPM validation status
  - retry effectiveness
  - token usage (when available)
  - deterministic analyzer coverage
  - human-review notes
- Derive as much as possible automatically from the run report + existing
  per-candidate JSON artifacts; leave human-review notes as explicit optional
  annotations.
- Add a `quality-report` CLI command that reads an execution report (from the
  P15-T2 runner) and optional per-package notes files and emits the quality
  report.
- Keep the report local-only and never commit generated outputs.
- Keep it composable: a quality report JSON is a standalone artifact that
  references, but does not embed, raw harvested source.

## Non-Goals

- Do not implement SpecNode runtime, provider model execution, or provider
  lifecycle management.
- Do not read or embed raw repository source, prompts, provider transcripts,
  chain-of-thought, or secrets.
- Do not commit generated quality report outputs to the repository.
- Do not add a new external dependency; use only Python standard library and
  existing `spec_harvester` modules.
- Do not define "intent accuracy" as an automated ML metric; it is an
  evidence-based rating derived from deterministic artifact presence.

## Deliverables

1. `src/spec_harvester/real_repo_quality_report.py` — new module with:
   - Schema constants: `QUALITY_REPORT_KIND`, `QUALITY_REPORT_SCHEMA_VERSION`
   - Rating literals: `QualityRating` (`strong`, `partial`, `weak`, `unscored`)
   - Status literals: `SpecPMStatus` (`passed`, `failed`, `skipped`, `not_run`)
   - Retry outcome literals: `RetryOutcome` (`improved`, `unchanged`,
     `degraded`, `not_attempted`)
   - Verdict literals: `OverallVerdict` (`pass`, `review`, `fail`, `unscored`)
   - `build_quality_report(run_report, candidates_root, human_notes)` →
     `dict[str, Any]`: derive a quality report from the execution report and
     candidate directories
   - `build_package_quality_record(package_record, candidate_dir, notes)` →
     `dict[str, Any]`: derive quality dimensions for one package
   - `write_quality_report(path, report)` helper
   - `_derive_intent_rating`, `_derive_capability_rating`,
     `_derive_analyzer_coverage`, `_extract_token_usage`,
     `_derive_retry_outcome` private helpers

2. CLI command `quality-report` in `src/spec_harvester/cli.py`:
   - `--run-report PATH` (required): the execution report JSON from the runner
   - `--candidates-root PATH` (optional): override candidate output root
   - `--notes FILE` (optional, repeatable): `id=<pkg_id>,notes=<text>` or
     a JSON file with per-package notes keyed by package id
   - `--output PATH`: write quality report JSON to file
   - Prints quality report JSON to stdout

3. `tests/test_real_repo_quality_report.py` — unit tests covering:
   - Schema version and kind
   - Rating derivation from step outcomes
   - SpecPM status derivation
   - Retry outcome derivation
   - Analyzer coverage derivation
   - Token usage extraction (present and absent)
   - Overall verdict assignment
   - `build_quality_report` with minimal fixture run report
   - `write_quality_report` roundtrip

4. `docs/REAL_REPOSITORY_QUALITY_REPORT.md` — GitHub docs page describing:
   - Purpose and relationship to the execution report
   - Schema fields and rating scales
   - CLI usage example
   - Safety rules (local-only, no output commits)

5. `Sources/SpecHarvester/Documentation.docc/RealRepositoryQualityReport.md`
   — DocC mirror of the GitHub docs page

6. `SPECS/INPROGRESS/P15-T3_Validation_Report.md` — quality gates run

## Quality Report Schema

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterRealRepositoryQualityReport",
  "runReport": "<path or null>",
  "candidatesRoot": "<path or null>",
  "packageCount": 2,
  "summary": {
    "passCount": 1,
    "reviewCount": 1,
    "failCount": 0,
    "unscoredCount": 0
  },
  "packages": [
    {
      "id": "...",
      "packageId": "...",
      "intentAccuracy": "partial",
      "intentNotes": "...",
      "capabilityEvidenceQuality": "strong",
      "capabilityNotes": "...",
      "specpmStatus": "passed",
      "specpmNotes": "...",
      "retryOutcome": "not_attempted",
      "retryNotes": "...",
      "tokenUsage": { "prompt": null, "completion": null },
      "analyzerCoverage": "strong",
      "analyzerCoverageNotes": "...",
      "analyzersUsed": ["pythonPublicApi", "semanticEvidence"],
      "humanReviewNotes": "...",
      "overallVerdict": "review"
    }
  ]
}
```

## Derivation Rules

**intentAccuracy**:
- `strong` — draft step succeeded and `draft.json` contains a non-empty
  `intent` field with ≥1 evidence reference
- `partial` — draft step succeeded but intent is present without evidence
  references
- `weak` — draft step failed, draft step was not attempted, `draft.json` is
  absent, or intent is missing
- `unscored` — dry_run mode

**capabilityEvidenceQuality**:
- `strong` — `draft.json` has ≥1 capability and all capabilities have
  ≥1 evidence reference
- `partial` — ≥1 capability present but some lack evidence
- `weak` — draft step failed, draft step was not attempted, `draft.json` is
  absent, no capabilities are present, or all capabilities lack evidence
- `unscored` — dry_run mode

**specpmStatus**:
- `passed` — specpm step in run report exited 0
- `failed` — specpm step exited non-zero
- `skipped` — step was skipped via `--skip-specpm-validation`
- `not_run` — step was not attempted

**retryOutcome**:
- `not_attempted` — specnode step absent
- `improved` — specnode step succeeded and result file contains
  `"retryCount": >0` with `"improved": true`
- `unchanged` — specnode step succeeded but no improvement
- `degraded` — specnode step failed after retry

**analyzerCoverage** (derived from `harvest.json` analyzer evidence):
- `strong` — harvest.json present and has ≥2 analyzer types
- `partial` — harvest.json present with 1 analyzer type
- `weak` — harvest.json present but no analyzer output
- `unscored` — harvest.json absent or dry_run

**overallVerdict**:
- `pass` — specpmStatus in (passed, not_run, skipped) AND intentAccuracy in
  (strong, partial) AND capabilityEvidenceQuality in (strong, partial)
- `fail` — specpmStatus==failed OR intentAccuracy==weak
- `review` — everything else non-unscored
- `unscored` — dry_run or all dimensions unscored

## Acceptance Criteria

- `PYTHONPATH=src python -m pytest tests/test_real_repo_quality_report.py`
  passes with no failures.
- `ruff check src tests` passes with no errors.
- `ruff format --check src tests` passes.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-fail-under=90`
  passes.
- `python -m spec_harvester quality-report --help` prints usage without error.
- Quality report schema fields match deliverable spec.
- Documentation files exist and reference the CLI correctly.
- No harvested source, prompts, secrets, or generated output is committed.
