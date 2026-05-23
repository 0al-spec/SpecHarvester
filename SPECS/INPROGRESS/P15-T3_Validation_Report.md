# P15-T3 Validation Report

Task: `P15-T3`
Status: PASS

## Quality Gates

| Gate | Command | Result |
|---|---|---|
| Tests | `PYTHONPATH=src python -m pytest` | 324 passed, 1 skipped |
| Lint | `ruff check src tests` | All checks passed |
| Format | `ruff format --check src tests` | 49 files already formatted |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-fail-under=90` | 90.56% (≥90%) |

## Deliverables Verified

- `src/spec_harvester/real_repo_quality_report.py` — 185 lines, 95% test
  coverage. Exports `build_quality_report`, `build_package_quality_record`,
  `write_quality_report`, and all rating/status/verdict constants.
- `src/spec_harvester/cli.py` — `quality-report` subcommand added with
  `--run-report`, `--candidates-root`, `--notes`, `--output` arguments.
- `tests/test_real_repo_quality_report.py` — 55 tests covering all derivation
  helpers, `build_package_quality_record`, `build_quality_report`,
  `write_quality_report`, and CLI integration.
- `tests/test_docs_contracts.py` — new
  `test_real_repository_quality_report_docs_cover_required_fields` test.
- `docs/REAL_REPOSITORY_QUALITY_REPORT.md` — full schema documentation, rating
  scale table, derivation rules, CLI usage, and safety rules.
- `Sources/SpecHarvester/Documentation.docc/RealRepositoryQualityReport.md` —
  DocC mirror.
- `docs/README.md` — entry 29 added.
- `Sources/SpecHarvester/Documentation.docc/SpecHarvester.md` —
  `<doc:RealRepositoryQualityReport>` reference added.

## CLI Smoke

```
python -m spec_harvester quality-report --help  → exit 0, prints usage
```

## Acceptance Criteria

- [x] `PYTHONPATH=src python -m pytest tests/test_real_repo_quality_report.py`
  passes.
- [x] `ruff check src tests` passes.
- [x] `ruff format --check src tests` passes.
- [x] Coverage ≥90%.
- [x] `python -m spec_harvester quality-report --help` prints usage.
- [x] Quality report schema fields match PRD spec.
- [x] Documentation files exist and reference the CLI correctly.
- [x] No harvested source, prompts, secrets, or generated output is committed.
