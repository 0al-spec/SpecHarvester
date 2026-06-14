# Real Repository Quality Report

Status: Phase 15 plan

This page mirrors the GitHub documentation for the structured quality report
format added in P15-T3.  The quality report captures the semantic quality of
SpecHarvester output for a real-repository refinement validation run and
complements the execution report produced by the P15-T2 runner.

## Purpose

`python -m spec_harvester quality-report` reads an execution report and
per-candidate artifact directories and emits a quality report covering:

- **Package intent accuracy** — is the drafted intent plausible and backed by
  evidence?
- **Capability/evidence support quality** — do capability claims reference
  deterministic evidence?
- **SpecPM validation status** — did the candidate pass `specpm validate`?
- **Retry effectiveness** — did external SpecNode refinement improve the result?
- **Token usage** — prompt and completion token counts (when available).
- **Deterministic analyzer coverage** — how many analyzer types contributed to
  the harvest snapshot or colocated public interface index artifact?
- **Human-review notes** — free-text annotations supplied by the operator.

The P15-T2 runner writes per-candidate `draft-summary.json` files from the
generated `specpm.yaml` and `specs/*.spec.yaml` artifacts.  The report uses that
summary for intent and capability evidence scoring.

For analyzer coverage, the report reads `harvest.json` analyzer fields and a
candidate-local `public-interface-index.json` when present.  The public
interface index must validate as `SpecHarvesterPublicInterfaceIndex` before it
contributes coverage.  The report counts analyzer ids declared in the index, or
`publicInterfaceIndex` when no analyzer ids are present; invalid or missing
index artifacts are ignored.

## Rating Scales

| Dimension | Values |
|---|---|
| `intentAccuracy` | `strong`, `partial`, `weak`, `unscored` |
| `capabilityEvidenceQuality` | `strong`, `partial`, `weak`, `unscored` |
| `analyzerCoverage` | `strong`, `partial`, `weak`, `unscored` |
| `specpmStatus` | `passed`, `failed`, `skipped`, `not_run` |
| `retryOutcome` | `improved`, `unchanged`, `degraded`, `not_attempted` |
| `overallVerdict` | `pass`, `review`, `fail`, `unscored` |
| `tokenUsage` | `{ "prompt": <int or null>, "completion": <int or null> }` |
| `humanReviewNotes` | free-text string; empty string when not supplied |

## CLI Usage

```bash
python -m spec_harvester quality-report \
  --run-report .smoke/output/real-repository-validation/run-report.json \
  --candidates-root .smoke/output/real-repository-validation \
  --notes "id=my-package,notes=intent looks good" \
  --output quality-report.json
```

Notes can also be supplied from a JSON file mapping package ids to notes text:

```bash
python -m spec_harvester quality-report \
  --run-report run-report.json \
  --notes @notes.json
```

## Relationship to Execution Report

The execution report captures **what ran** and whether each step succeeded.
The quality report captures **how good** the output is.  Both are local-only
advisory artifacts and must not be committed to the repository.

P27 adds a second layer on top: <doc:AuthorReadyCalibrationMatrix> translates
this quality report into estimated author edits, edit categories, review
priority, and repeated generator gaps.

When `--candidates-root` is not supplied, package artifact lookup uses each
package record's `candidateDir` from `run-report.json`; otherwise it falls back
to `<candidatesRoot>/<package-id>`.

## Safety Rules

- Reads only existing local JSON artifact files.
- Does not execute repository code, install packages, or contact external
  services.
- Does not embed raw source, prompts, provider transcripts, chain-of-thought,
  or secrets.
- Generated quality report files must not be committed.
- Does not implement SpecNode runtime, provider discovery, model execution,
  scheduling, or lifecycle management.
