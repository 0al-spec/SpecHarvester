# Real Repository Quality Report

Status: Phase 15 plan

The quality report is a structured JSON artifact that captures the semantic
quality of SpecHarvester output for a real-repository refinement validation run.
It complements the execution report produced by the P15-T2 runner with
evidence-based quality dimensions for each package.

## Purpose

`python -m spec_harvester quality-report` reads an execution report (produced by
the P15-T2 real-repository validation runner) and per-candidate artifact
directories and emits a quality report covering:

- **Package intent accuracy** — is the drafted intent plausible and backed by
  evidence?
- **Capability/evidence support quality** — do capability claims reference
  deterministic evidence?
- **SpecPM validation status** — did the candidate pass `specpm validate`?
- **Retry effectiveness** — did external SpecNode refinement improve the result?
- **Token usage** — prompt and completion token counts (when available from the
  SpecNode result file).
- **Deterministic analyzer coverage** — how many analyzer types contributed to
  the harvest snapshot?
- **Human-review notes** — free-text annotations supplied by the operator.

## Schema

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterRealRepositoryQualityReport",
  "runReport": "<execution report path when supplied>",
  "inputs": "<inputs path from run report>",
  "candidatesRoot": "<path>",
  "dryRun": false,
  "packageCount": 2,
  "summary": {
    "passCount": 1,
    "reviewCount": 1,
    "failCount": 0,
    "unscoredCount": 0
  },
  "packages": [
    {
      "id": "my-package",
      "packageId": "com.example.my-package",
      "intentAccuracy": "strong",
      "intentNotes": "intent present with 2 evidence source(s)",
      "capabilityEvidenceQuality": "partial",
      "capabilityNotes": "2/3 capabilities have evidence sources",
      "specpmStatus": "passed",
      "specpmNotes": "specpm validation passed",
      "retryOutcome": "not_attempted",
      "retryNotes": "no specnode step in run report",
      "tokenUsage": { "prompt": null, "completion": null },
      "analyzerCoverage": "strong",
      "analyzerCoverageNotes": "2 analyzer type(s) found: pythonPublicApi, semanticEvidence",
      "analyzersUsed": ["pythonPublicApi", "semanticEvidence"],
      "humanReviewNotes": "intent matches README; capability evidence is thin",
      "overallVerdict": "review"
    }
  ],
  "trustBoundary": ["..."]
}
```

### Rating Scales

| Dimension | Values |
|---|---|
| `intentAccuracy` | `strong`, `partial`, `weak`, `unscored` |
| `capabilityEvidenceQuality` | `strong`, `partial`, `weak`, `unscored` |
| `analyzerCoverage` | `strong`, `partial`, `weak`, `unscored` |
| `specpmStatus` | `passed`, `failed`, `skipped`, `not_run` |
| `retryOutcome` | `improved`, `unchanged`, `degraded`, `not_attempted` |
| `overallVerdict` | `pass`, `review`, `fail`, `unscored` |

### Derivation Rules

**`intentAccuracy`**:
- `strong` — draft step succeeded and `draft.json` has a non-empty `intent`
  field with ≥1 `evidenceSources` reference.
- `partial` — draft step succeeded and intent is present but no evidence
  references.
- `weak` — draft step failed, intent is missing, or `draft.json` is absent.
- `unscored` — dry_run mode.

**`capabilityEvidenceQuality`**:
- `strong` — all capabilities have ≥1 evidence source.
- `partial` — some capabilities have evidence sources.
- `weak` — draft step failed, `draft.json` is absent, no capabilities are
  present, or none have evidence sources.
- `unscored` — dry_run mode.

**`specpmStatus`**: derived directly from the `specpm` step outcome in the
execution report.

**`retryOutcome`**: derived from the `specnode` step outcome and, when
available, the `specnode-refinement-result.json` `retryCount` and `improved`
fields.

**`analyzerCoverage`**:
- `strong` — ≥2 distinct analyzer types found in `harvest.json`.
- `partial` — 1 analyzer type found.
- `weak` — harvest present but no analyzer output.
- `unscored` — harvest absent or dry_run.

**`overallVerdict`**:
- `pass` — SpecPM passed (or not run/skipped) **and** intent is strong/partial
  **and** capabilities are strong/partial.
- `fail` — SpecPM failed **or** intent is weak.
- `review` — anything else that is not `unscored`.
- `unscored` — dry_run or all dimensions unscored.

## CLI Usage

```bash
# Minimal: derive from run report only
python -m spec_harvester quality-report \
  --run-report .smoke/output/real-repository-validation/run-report.json

# With custom candidates root and notes
python -m spec_harvester quality-report \
  --run-report run-report.json \
  --candidates-root .smoke/output/real-repository-validation \
  --notes "id=my-package,notes=intent looks good" \
  --output quality-report.json

# Notes from a JSON file
python -m spec_harvester quality-report \
  --run-report run-report.json \
  --notes @notes.json \
  --output quality-report.json
```

### Notes File Format

`--notes @<path>` reads a JSON object mapping package ids to notes text:

```json
{
  "my-package": "Intent is plausible; capability evidence is thin.",
  "other-package": "Needs review: SpecPM reported a namespace conflict."
}
```

## Relationship to Execution Report

The execution report (from the P15-T2 real-repository validation runner)
captures **what ran** and whether each step succeeded.  The quality report
captures **how good** the output is.  Both are local-only advisory artifacts
and must not be committed to the repository.

## Safety Rules

- Reads only existing local JSON artifact files. Never executes repository
  code, installs packages, or contacts external services.
- Does not embed raw repository source, prompts, provider transcripts,
  chain-of-thought, or secrets.
- Generated quality report files are advisory and must not be committed.
- The report does not implement SpecNode runtime, provider discovery, model
  execution, scheduling, or lifecycle management.
