# P37-T7 Validation Report

## Task

`P37-T7` Real Repository Profile Auto-Selection Run.

## Result

Verdict: `PASS_WITH_FOLLOW_UP`.

The real FastMCP run completed successfully and produced durable comparison
evidence. The product result is intentionally not recorded as auto-selection
success: repository-wide auto-selection explained the generic fallback, while
manual `fastmcp_slim` targeting produced a materially narrower public interface
index.

## Real Run Evidence

Source:

- repository: `https://github.com/jlowin/fastmcp`;
- local checkout: `/Users/egor/Development/GitHub/fastmcp`;
- revision: `3b8538e2422a1c43fdb69661c610de7985b785f2`;
- run root: `/tmp/specharvester-p37-t7-fastmcp-20260618T223329Z`;
- AI mode: disabled with `--skip-ai`;
- network: not required.

Auto-selection command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch "$RUN_ROOT/auto-inputs" \
  --out "$RUN_ROOT/auto-output" \
  --skip-ai \
  --repository-profile-selection auto
```

Manual targeting command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch "$RUN_ROOT/manual-inputs" \
  --out "$RUN_ROOT/manual-output" \
  --skip-ai \
  --repository-profile-selection none
```

Both batch reports completed with `status: passed`.

Durable fixture:

```text
tests/fixtures/repository_profile_real_runs/p37-t7-fastmcp-auto-selection-comparison.example.json
```

Key comparison:

| Metric | Auto root | Manual `fastmcp_slim` |
| --- | ---: | ---: |
| Profile decision | `fallback` | `disabled` |
| Selected profile | `null` | `null` |
| Fallback profile | `generic.repository.v0` | `generic.repository.v0` |
| Confidence | `low` | `blocked` |
| Public interface entrypoints | 772 | 260 |
| Public interface symbols | 9199 | 1563 |
| Author-ready status | `author_ready_draft` | `author_ready_draft` |

## Finding

The reusable gap is manifest evidence routing:

- auto `harvest.json` records `packageManifestCount: 1` and
  `packageManifestPaths: ["pyproject.toml"]`;
- auto `workspace-inventory.json` records `packageManifestCount: 0`;
- profile detection therefore lacks high-confidence manifest evidence and falls
  back to `generic.repository.v0`.

The next bounded task is P37-T8: make repository profile detection consume
harvested package manifest evidence when workspace inventory has no manifest
records.

## Documentation

Added:

- `docs/REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`;
- `Sources/SpecHarvester/Documentation.docc/RepositoryProfileRealRunFastMCP.md`.

Updated:

- documentation index;
- DocC root;
- capabilities map;
- repository profile selection contract;
- roadmap;
- workplan.

## Validation Commands

```bash
python -m json.tool tests/fixtures/repository_profile_real_runs/p37-t7-fastmcp-auto-selection-comparison.example.json >/tmp/p37t7-fixture.pretty.json
PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile'
```

Observed results:

```text
15 passed in 0.08s
6 passed, 101 deselected in 0.03s
```

Full repository gates are run after archive/review artifacts are added, before
the pull request is opened.

## Boundary

This task records producer-side evidence only. It does not implement an
ecosystem-specific profile, change profile scoring, accept packages, accept
relations, publish registry metadata, remove `preview_only`, treat profile
decisions or hints as registry truth, treat manual targeting as registry truth,
or treat AI output as registry truth.
