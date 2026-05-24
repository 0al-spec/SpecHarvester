# Real Repository Local Validation Matrix

Status: Phase 15 local validation summary

This page records the compact P15-T4 real-repository validation matrix.  The
run used operator-managed local checkouts under `~/Development/GitHub` and kept
all generated manifests, candidates, run reports, quality reports, and triage
JSON under ignored `.smoke/` paths.

## Command Pattern

The local manifest was staged only under ignored `.smoke/p15-t4-inputs`.

```bash
PYTHONPATH=src python scripts/run_real_repository_validation.py \
  --inputs .smoke/p15-t4-inputs \
  --out .smoke/output/p15-t4-local-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p15-t4-analyzer-cache \
  --skip-specpm-validation
```

The matrix then built the structured quality report from the generated run
report:

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p15-t4-local-validation/run-report.json \
  --output .smoke/output/p15-t4-local-validation/quality-report.json
```

Manual per-candidate SpecPM validation was run separately with the adjacent
local SpecPM checkout:

```bash
PYTHONPATH=../SpecPM/src python -m specpm.cli validate \
  .smoke/output/p15-t4-local-validation/<candidate> --json
```

## Matrix

| Repository | Shape | Runner | Public index | Quality verdict | Manual SpecPM | Failure class |
|---|---|---|---|---|---|---|
| `cupertino` | Swift/SPM + Xcode workspace | `ok` | no (`manifest_only`) | `pass` (`strong` intent, `strong` capabilities, `partial` analyzer coverage) | pass | Broad documentation/API intent duplication |
| `navigation-split-view` | Swift/SPM + Xcode project | `ok` | no (`manifest_only`) | `pass` (`strong`, `strong`, `partial`) | pass | Package id normalized from hyphen to underscore, causing namespace/upstream mismatch |
| `xyflow` | JavaScript/TypeScript npm/pnpm monorepo | `ok` | yes | `pass` (`strong`, `strong`, `partial`) | pass | none |
| `flask` | Python `pyproject.toml` web framework | `ok` | yes | `pass` (`strong`, `strong`, `weak`) | pass | `LICENSE.txt` classified as ambiguous unknown license; quality-report analyzer coverage undercounts generated public index |
| `gin` | Go module web framework | `ok` | yes | `pass` (`strong`, `strong`, `weak`) | pass | quality-report analyzer coverage undercounts generated public index |
| `docc2context` | Swift/SPM documentation-first CLI | `ok` | no (`manifest_only`) | `pass` (`strong`, `strong`, `partial`) | pass | Broad documentation/API intent duplication |

## Aggregate Outcome

- Runner status: `ok`
- Packages attempted: 6
- Packages drafted: 6
- Quality report summary: 6 pass, 0 review, 0 fail, 0 unscored
- Manual SpecPM validation: 6 pass
- Smoke triage status: `attention_required`
- Smoke triage counts: 0 batch errors, 0 batch warnings, 9 duplicate intent
  claims, 0 duplicate claim issues, 2 license/provenance issues, 1 namespace
  issue, 12 total advisory issues

## Failure Classes

### Broad Intent Duplication

The governance report found repeated broad intent claims such as
`intent.api.contract_surface`, `intent.developer.tooling_surface`, and
`intent.documentation.knowledge_base` across unrelated candidates.  This points
to a useful follow-up area for making language-neutral semantic extraction less
eager with generic documentation/API/tooling intents.

### Analyzer Coverage Undercount

`flask` and `gin` generated `public-interface-index.json`, and the runner
reported executed Python/Go public API analyzers.  The quality report still
classified analyzer coverage as `weak` for both.  In short, quality-report
analyzer coverage undercounts generated public index artifacts because its
coverage derivation does not yet account for the colocated public interface
index.  The generated candidate quality is stronger than the quality-report
rating suggests.

### License Filename Classification

`flask` uses `LICENSE.txt`; the governance license report classified it as
`ambiguous_unknown_license` even though it is a standard public project license
file shape.  This is a deterministic classifier compatibility gap.

### Package ID Normalization

`navigation-split-view` was supplied as `navigation-split-view.core`, while the
drafter normalized the generated package identity to
`navigation_split_view.core`.  The namespace/upstream report then flagged a
low-severity mismatch against the upstream repository name
`NavigationSplitView`.

## Safety Notes

- No harvested package scripts, dependency installers, tests, or builds were
  run.
- No package registry calls were made.
- SpecNode runtime/provider execution was not invoked.
- Generated `.smoke/` inputs and outputs were intentionally left uncommitted.
