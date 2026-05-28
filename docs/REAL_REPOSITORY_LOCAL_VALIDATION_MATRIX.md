# Real Repository Local Validation Matrix

Status: Phase 16 rerun summary

This page records the compact real-repository validation matrix.  The original
P15-T4 run established the baseline; P16-T5 reran the same six checkout shapes
after the P16-T1 through P16-T4 signal-quality fixes.  Both runs used
operator-managed local checkouts under `~/Development/GitHub` and kept all
generated manifests, candidates, run reports, quality reports, and triage JSON
under ignored `.smoke/` paths.

## Command Pattern

The P16-T5 local manifest was staged only under ignored `.smoke/p16-t5-inputs`.

```bash
PYTHONPATH=src python scripts/run_real_repository_validation.py \
  --inputs .smoke/p16-t5-inputs \
  --out .smoke/output/p16-t5-local-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p16-t5-analyzer-cache \
  --skip-specpm-validation
```

The matrix then built the structured quality report from the generated run
report:

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p16-t5-local-validation/run-report.json \
  --candidates-root .smoke/output/p16-t5-local-validation \
  --output .smoke/output/p16-t5-local-validation/quality-report.json
```

Manual per-candidate SpecPM validation was run separately with the adjacent
local SpecPM checkout:

```bash
PYTHONPATH=../SpecPM/src python -m specpm.cli validate \
  .smoke/output/p16-t5-local-validation/<candidate> --json
```

## P16-T5 Matrix Rerun

| Repository | Shape | Runner | Public index | Quality verdict | Manual SpecPM | Failure class |
|---|---|---|---|---|---|---|
| `cupertino` | Swift/SPM + Xcode workspace | `ok` | no (`manifest_only`) | `pass` (`strong` intent, `strong` capabilities, `partial` analyzer coverage) | warning-only (`preview_only_package`) | residual specific web intent overlap |
| `navigation-split-view` | Swift/SPM + Xcode project | `ok` | no (`manifest_only`) | `pass` (`strong`, `strong`, `partial`) | warning-only (`preview_only_package`) | none; namespace/upstream mismatch cleared |
| `xyflow` | JavaScript/TypeScript npm/pnpm monorepo | `ok` | yes | `pass` (`strong`, `strong`, `strong`; `public-interface-index.json` counted) | warning-only (`preview_only_package`) | none |
| `flask` | Python `pyproject.toml` web framework | `ok` | yes | `pass` (`strong`, `strong`, `partial`; `public-interface-index.json` counted) | warning-only (`preview_only_package`) | low `collected_unknown_license_evidence` |
| `gin` | Go module web framework | `ok` | yes | `pass` (`strong`, `strong`, `partial`; `public-interface-index.json` counted) | warning-only (`preview_only_package`) | none |
| `docc2context` | Swift/SPM documentation-first CLI | `ok` | no (`manifest_only`) | `pass` (`strong`, `strong`, `partial`) | warning-only (`preview_only_package`) | residual specific web intent overlap |

## P16-T5 Aggregate Outcome

- Runner status: `ok`
- Packages attempted: 6
- Packages drafted: 6
- Quality report summary: 6 pass, 0 review, 0 fail, 0 unscored
- Manual SpecPM validation: 6 warning-only, each with the expected
  `preview_only_package` warning and no errors
- Smoke triage status: `attention_required`
- Smoke triage counts: 0 batch errors, 0 batch warnings, 4 duplicate intent
  claims, 0 duplicate claim issues, 1 license/provenance issue, 0 namespace
  issues, 5 total advisory issues

## Delta from P15-T4

| Signal | P15-T4 baseline | P16-T5 rerun | Result |
|---|---:|---:|---|
| Total advisory issues | 12 | 5 | improved |
| Duplicate intent claims | 9 | 4 | improved |
| License/provenance issues | 2 | 1 | improved |
| Namespace/upstream issues | 1 | 0 | cleared |
| Quality pass count | 6 | 6 | preserved |

The broad language-neutral duplicate intent noise from P15-T4 is gone from
`duplicates.intent`.  Remaining duplicate intent findings are specific web
claims: `intent.web.framework_surface`, `intent.web.http_routing`,
`intent.web.middleware_pipeline`, and `intent.web.request_response_context`.

## Remaining Review Signals

### Specific Web Intent Overlap

The governance report still finds four specific duplicate web intent claims.
Three are expected overlap between `flask` and `gin`.  The fourth,
`intent.web.request_response_context`, also appears on `cupertino` and
`docc2context`, so it remains a candidate for later semantic intent tightening
if this signal proves noisy in future matrices.

### Analyzer Coverage

The P16-T1 fix is visible.  `xyflow`, `flask`, and `gin` all report
`public-interface-index.json counted`; `xyflow` reaches `strong` analyzer
coverage, while `flask` and `gin` move from misleading `weak` classification to
`partial` single-analyzer coverage.

### License Provenance

`flask` now reports low-severity `collected_unknown_license_evidence` for
`LICENSE.txt` instead of the noisier P15-T4 ambiguous license classification.
This is the expected P16-T2 behavior: the report recognizes standard collected
license-file evidence but does not parse full license text or infer SPDX
identifiers.

### Namespace Normalization

The P16-T3 normalization fix cleared the previous
`navigation_split_view.core` namespace/upstream mismatch.  P16-T5 reports
`namespaceIssueCount=0`.

## Safety Notes

- No harvested package scripts, dependency installers, tests, or builds were
  run.
- No package registry calls were made.
- SpecNode runtime/provider execution was not invoked.
- Generated `.smoke/` inputs and outputs were intentionally left uncommitted.
