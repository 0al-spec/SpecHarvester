# P38-T6 Validation Report

## Task

P38-T6 Real Repository Plugin Evidence Run.

## Summary

PASS. Ran the pinned local FastMCP checkout through the repository plugin
evidence path and recorded a durable
`SpecHarvesterRepositoryPluginRealRunComparison` fixture.

Source:

- local checkout: `/Users/egor/Development/GitHub/fastmcp`;
- revision: `3b8538e2422a1c43fdb69661c610de7985b785f2`;
- run root: `/tmp/specharvester-p38-t6-fastmcp-20260619T005454Z`;
- AI: disabled with `--skip-ai`;
- network: not required.

Key result:

- current repository profile selection chose `generic.single_package.v0` with
  `confidence: high`;
- this improves over the P37-T7 FastMCP baseline, which fell back to
  `generic.repository.v0`;
- autonomous candidate batch recorded the plugin applicability report as
  `repositoryPluginApplicability.status: recorded`;
- sidecar evidence remained `appliedToDrafting: false` and
  `registryAuthority: false`;
- candidate preflight passed with `0` errors and `0` warnings.

## Real Run Commands

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/auto-inputs" \
  --out "$RUN_ROOT/auto-output" \
  --skip-ai \
  --repository-profile-selection auto
```

Result: `status: passed`.

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/sidecar-inputs" \
  --out "$RUN_ROOT/sidecar-output" \
  --skip-ai \
  --repository-profile-selection auto \
  --repository-plugin-applicability "$RUN_ROOT/repository-plugin-applicability-report.json"
```

Result: `status: passed`.

## Artifacts

- Fixture:
  `tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`
- GitHub docs:
  `docs/REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`
- DocC docs:
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginRealRunFastMCP.md`

## Validation

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json >/tmp/p38-t6-plugin-real-run.pretty.json` | PASS |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin_real_run or repository_plugin_cross_ecosystem or current_next_task'` | PASS, `2 passed, 110 deselected` |
| `PYTHONPATH=src pytest -q` | PASS, `766 passed, 1 skipped` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `766 passed, 1 skipped`, total coverage `91.16%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS, `120 files already formatted` |
| `git diff --check` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Review Notes

- Regression coverage verifies fixture identity, P37 baseline comparison,
  current profile selection, plugin applicability sidecar discovery, selected
  plugin input consistency against the registry fixture, docs links, DocC
  links, and non-authority statements.
- The run remains producer-side evidence only. It does not implement plugin
  execution, load third-party plugin code, clone or fetch repositories, install
  dependencies, run package managers, execute harvested code, run AI, accept
  packages or relations, publish registry metadata, remove `preview_only`, or
  treat plugin decisions as registry truth.
