# P15-T5 Validation Report

Task: `P15-T5`
Date: 2026-05-24
Branch: `feature/P15-T5-validation-follow-up-workplan`

## Failure Mapping

| P15-T4 failure class | Existing coverage check | Follow-up outcome |
|---|---|---|
| Quality-report analyzer coverage undercounts generated public indexes for `flask` and `gin` | P15-T3 defined quality-report format; P15-T6 aligned runner output shape, but neither fixed colocated `public-interface-index.json` coverage derivation | New `P16-T1` |
| Flask `LICENSE.txt` appears as ambiguous unknown license evidence in governance reports | P12-T1/P12-T6 cover strict source manifest acceptance of common license filenames, not governance license text classification quality | New `P16-T2` |
| `navigation-split-view` hyphen/underscore package identity mismatch creates namespace advisory noise | P6-T3 and P7-T1 cover case-insensitive owner/repository comparisons, not generated package ID separator normalization | New `P16-T3` |
| Broad duplicate documentation/API/tooling semantic intents across unrelated candidates | P9-T1/P9-T2 introduced deterministic semantic intent/evidence generation; P5-T1 detects duplicates, but no task hardens generic intent thresholds from real matrix feedback | New `P16-T4` |
| Need to prove improvements after targeted fixes | P15-T4 captured baseline matrix only | New `P16-T5` |

## Workplan Changes

- Added Phase 16: Real Repository Signal Quality Hardening.
- Added `P16-T1` through `P16-T5` as focused follow-up tasks.
- Updated `SPECS/INPROGRESS/next.md` to suggest `P16-T1`.

## Safety

- No generated `.smoke/` artifacts were committed.
- No harvested repository code, package scripts, dependency installers, tests,
  builds, package managers, registry calls, SpecNode providers, or model calls
  were run for this planning-only task.

## Quality Gates

The following gates passed before the EXECUTE checkpoint:

- `PYTHONPATH=src python -m pytest`: 349 passed, 1 skipped
- `ruff check src tests`: passed
- `ruff format --check src tests`: passed
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  349 passed, 1 skipped; total coverage 90.64%
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
