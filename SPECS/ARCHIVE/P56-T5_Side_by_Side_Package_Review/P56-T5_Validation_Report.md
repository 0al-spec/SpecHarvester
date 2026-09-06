# P56-T5 Validation Report

Date: 2026-09-06
Verdict: PASS for comparison preparation; human utility review pending.

## Artifact Checks

Five new candidates, five pinned README files and five separate semantic
records are reachable. Retained package counts are 4 / 1 / 1 / 1 / 77.
All 38 new files and all 603 retained candidate-set files preserve T4 bytes.
Archive/member, report/preparation and source identity checks passed.
Known quality defects and historical mismatches remain visible; originals and
historical v1 were not modified. No provider or publication path ran.

## Commands

- `.venv/bin/python -m spec_harvester.exploratory_comparison --output <new-outside-repo-directory>`:
  generated local site and comparison/empty-human-review JSON successfully.
- `.venv/bin/python -m pytest tests/test_exploratory_comparison.py -q --cov=spec_harvester.exploratory_comparison --cov-report=term-missing`:
  22 passed; module coverage 98%.
- `.venv/bin/python -m pytest -q --tb=short --cov=spec_harvester --cov-report=term --cov-fail-under=90`:
  1475 passed, 7 skipped; coverage 90.12%.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed, existing unhandled DocC warning.
- `.venv/bin/python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p56-t5-architecture.json`:
  one existing advisory in license_provenance_reports.py, none in the new module.

## Bounded Browser Check

Playwright, 15 tool invocations including three failures, four screenshots
visually inspected. No maintainer data mutation or scoring. Checks:

- Codex reference switches to retained packages (4 links) and semantic proposal.
- Existing viewer JavaScript renders the n8n candidate in the sandboxed frame.
- Final offline-specific check renders Codex overview with zero external requests;
  derived viewer CSS removes Google Fonts and viewer HTML adds local-resource CSP.
- n8n retained selector exposes all 77 package links.
- Final complete-spec route exposes Purpose first at 1440x1000 and 390x844.
- DOM scroll width equals viewport width (1440/1440 and 390/390); no horizontal
  page overflow. Earlier mobile frame measurements confirm vertical stacking.
- Final desktop screenshot shows both populated columns; final mobile screenshot
  shows the first candidate column, with reference below the fold.

The file URL was blocked by the automation browser, so local HTTP was used.
One screenshot-path introspection used unavailable require; navigation/layout
actions before that error succeeded and measurements were separately confirmed.
No repeated tool troubleshooting. Local screenshots are not committed.
A single connection-refused response occurred during the local server restart;
the server became available and the one retry confirmed offline rendering.

## Limits

README intentionally remains escaped source text; external images/HTML do not
render. This presentation limitation must not be mistaken for missing README
content in T6. Download flows and exhaustive per-file UI navigation were not
browser-tested; byte preservation and file coverage are tested in Python.
The worksheet starts empty, stores no human decision by itself, and grants no
acceptance authority. A generated bundle is not a human usefulness verdict.
