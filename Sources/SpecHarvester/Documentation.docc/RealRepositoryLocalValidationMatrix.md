# Real Repository Local Validation Matrix

This DocC page mirrors `docs/REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md` and
records the compact P15-T4 local validation matrix.

## Scope

The run used operator-managed local checkouts under `~/Development/GitHub` and
kept generated manifests, candidates, run reports, quality reports, and triage
JSON under ignored `.smoke/` paths.

## Command Pattern

```bash
PYTHONPATH=src python scripts/run_real_repository_validation.py \
  --inputs .smoke/p15-t4-inputs \
  --out .smoke/output/p15-t4-local-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p15-t4-analyzer-cache \
  --skip-specpm-validation
```

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p15-t4-local-validation/run-report.json \
  --output .smoke/output/p15-t4-local-validation/quality-report.json
```

## Matrix

| Repository | Shape | Runner | Public index | Quality verdict | Manual SpecPM | Failure class |
|---|---|---|---|---|---|---|
| `cupertino` | Swift/SPM + Xcode workspace | `ok` | no (`manifest_only`) | `pass` | pass | Broad documentation/API intent duplication |
| `navigation-split-view` | Swift/SPM + Xcode project | `ok` | no (`manifest_only`) | `pass` | pass | Package id normalization created `navigation_split_view` namespace/upstream mismatch |
| `xyflow` | JavaScript/TypeScript npm/pnpm monorepo | `ok` | yes | `pass` | pass | none |
| `flask` | Python `pyproject.toml` web framework | `ok` | yes | `pass` | pass | `LICENSE.txt` ambiguous; quality-report analyzer coverage undercounts generated public index |
| `gin` | Go module web framework | `ok` | yes | `pass` | pass | quality-report analyzer coverage undercounts generated public index |
| `docc2context` | Swift/SPM documentation-first CLI | `ok` | no (`manifest_only`) | `pass` | pass | Broad documentation/API intent duplication |

## Aggregate Outcome

- Runner status: `ok`
- Packages attempted: 6
- Packages drafted: 6
- Quality report summary: 6 pass, 0 review, 0 fail, 0 unscored
- Manual SpecPM validation: 6 pass
- Smoke triage status: `attention_required`
- Smoke triage counts: 9 duplicate intent claims, 2 license/provenance issues,
  1 namespace issue, 12 total advisory issues

## Failure Classes

- Broad intent duplication: generic documentation/API/tooling intents are shared
  across unrelated candidates.
- Analyzer coverage undercount: `flask` and `gin` generated public interface
  indexes, but quality-report analyzer coverage undercounts those artifacts.
- License filename classification: `LICENSE.txt` was treated as ambiguous for
  `flask`.
- Package ID normalization: `navigation-split-view.core` became
  `navigation_split_view.core`, producing a namespace/upstream mismatch.

## Safety Notes

No harvested package scripts, dependency installers, tests, builds, package
registry calls, or SpecNode provider execution were run.  Generated `.smoke/`
inputs and outputs were intentionally left uncommitted.
