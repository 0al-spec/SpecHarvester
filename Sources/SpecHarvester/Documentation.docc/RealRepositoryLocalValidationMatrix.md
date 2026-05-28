# Real Repository Local Validation Matrix

This DocC page mirrors `docs/REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md` and
records the compact local validation matrix.  P15-T4 established the baseline;
P16-T5 reran the same six repositories after P16-T1 through P16-T4.

## Scope

The runs used operator-managed local checkouts under `~/Development/GitHub` and
kept generated manifests, candidates, run reports, quality reports, and triage
JSON under ignored `.smoke/` paths.

## Command Pattern

```bash
PYTHONPATH=src python scripts/run_real_repository_validation.py \
  --inputs .smoke/p16-t5-inputs \
  --out .smoke/output/p16-t5-local-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p16-t5-analyzer-cache \
  --skip-specpm-validation
```

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p16-t5-local-validation/run-report.json \
  --candidates-root .smoke/output/p16-t5-local-validation \
  --output .smoke/output/p16-t5-local-validation/quality-report.json
```

## P16-T5 Matrix Rerun

| Repository | Shape | Runner | Public index | Quality verdict | Manual SpecPM | Failure class |
|---|---|---|---|---|---|---|
| `cupertino` | Swift/SPM + Xcode workspace | `ok` | no (`manifest_only`) | `pass` | warning-only (`preview_only_package`) | residual specific web intent overlap |
| `navigation-split-view` | Swift/SPM + Xcode project | `ok` | no (`manifest_only`) | `pass` | warning-only (`preview_only_package`) | none; namespace/upstream mismatch cleared |
| `xyflow` | JavaScript/TypeScript npm/pnpm monorepo | `ok` | yes | `pass` (`strong` analyzer coverage; `public-interface-index.json` counted) | warning-only (`preview_only_package`) | none |
| `flask` | Python `pyproject.toml` web framework | `ok` | yes | `pass` (`partial` analyzer coverage; `public-interface-index.json` counted) | warning-only (`preview_only_package`) | low `collected_unknown_license_evidence` |
| `gin` | Go module web framework | `ok` | yes | `pass` (`partial` analyzer coverage; `public-interface-index.json` counted) | warning-only (`preview_only_package`) | none |
| `docc2context` | Swift/SPM documentation-first CLI | `ok` | no (`manifest_only`) | `pass` | warning-only (`preview_only_package`) | residual specific web intent overlap |

## P16-T5 Aggregate Outcome

- Runner status: `ok`
- Packages attempted: 6
- Packages drafted: 6
- Quality report summary: 6 pass, 0 review, 0 fail, 0 unscored
- Manual SpecPM validation: 6 warning-only, each with expected
  `preview_only_package` and no errors
- Smoke triage status: `attention_required`
- Smoke triage counts: 4 duplicate intent claims, 1 license/provenance issue,
  0 namespace issues, 5 total advisory issues

## Delta from P15-T4

| Signal | P15-T4 baseline | P16-T5 rerun | Result |
|---|---:|---:|---|
| Total advisory issues | 12 | 5 | improved |
| Duplicate intent claims | 9 | 4 | improved |
| License/provenance issues | 2 | 1 | improved |
| Namespace/upstream issues | 1 | 0 | cleared |
| Quality pass count | 6 | 6 | preserved |

Broad language-neutral duplicate intent noise is gone from `duplicates.intent`.
Remaining duplicate findings are specific web claims:
`intent.web.framework_surface`, `intent.web.http_routing`,
`intent.web.middleware_pipeline`, and `intent.web.request_response_context`.

## Remaining Review Signals

- Specific web intent overlap remains advisory-only.  Three duplicate claims
  are expected overlap between `flask` and `gin`; `intent.web.request_response_context`
  also appears on `cupertino` and `docc2context`.
- Analyzer coverage now counts `public-interface-index.json`: `xyflow` is
  `strong`, while `flask` and `gin` are `partial` single-analyzer cases.
  The quality report explicitly records `public-interface-index.json counted`.
- Flask now reports low-severity `collected_unknown_license_evidence` for
  `LICENSE.txt` instead of an ambiguous license classification.  Full SPDX
  inference remains out of scope.
- `navigation_split_view.core` no longer creates a namespace/upstream issue;
  `namespaceIssueCount=0`.

## Safety Notes

No harvested package scripts, dependency installers, tests, builds, package
registry calls, or SpecNode provider execution were run.  Generated `.smoke/`
inputs and outputs were intentionally left uncommitted.
