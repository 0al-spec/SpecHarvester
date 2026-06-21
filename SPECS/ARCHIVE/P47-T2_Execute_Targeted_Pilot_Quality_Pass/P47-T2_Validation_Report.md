# P47-T2 Validation Report

Task: P47-T2 Execute Targeted Pilot Quality Pass
Date: 2026-06-21
Verdict: PASS

## Summary

P47-T2 records an evidence-only targeted quality pass over the P46 pilot
blockers. The pass explicitly excludes current bad sidecars from bounded-rerun
promotion, records bounded-rerun dispositions for the xyflow caveats, and
selects P47-T3 as the next gate while keeping larger curated corpus approval
blocked until P47-T3 and P47-T4 complete.

No pilot rerun, AI call, adapter run, repository clone/fetch, dependency
install in harvested repositories, package manager invocation against harvested
repositories, registry promotion, baseline seeding, or `preview_only` removal
was performed.

## Artifacts

| Artifact | Result |
| --- | --- |
| `tests/fixtures/targeted_pilot_quality_pass/p47-t2-targeted-pilot-quality-pass.example.json` | Added durable `SpecHarvesterTargetedPilotQualityPass` fixture. |
| `docs/TARGETED_PILOT_QUALITY_PASS.md` | Added GitHub documentation for P47-T2 disposition and boundaries. |
| `Sources/SpecHarvester/Documentation.docc/TargetedPilotQualityPass.md` | Added DocC mirror. |
| `tests/test_docs_contracts.py` | Added contract coverage for fixture identity, source digests, sidecar/caveat dispositions, non-authority boundaries, docs links, and next-task readiness. |

## Validation Commands

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/targeted_pilot_quality_pass/p47-t2-targeted-pilot-quality-pass.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -q -k 'targeted_pilot_quality_pass'` | PASS, `1 passed, 168 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
| `PYTHONPATH=src python3 -m pytest` | PASS, `900 passed, 1 skipped` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `131 files already formatted` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `PYTHONPATH=src uv run --extra dev pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `900 passed, 1 skipped`, total coverage `90.51%` |

## Environment Note

The direct command
`PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
was attempted first and failed before test collection because the system
`/usr/bin/python3` environment did not have `pytest-cov` installed. The project
declares `pytest-cov` in the `dev` extra and CI installs `.[dev]`, so the
coverage gate was rerun through `uv run --extra dev`.
