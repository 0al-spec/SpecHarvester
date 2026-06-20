# P46-T2 Validation Report

## Task

P46-T2 Bounded Popular-Library Pilot Static-Only Run

## Verdict

PASS

## Summary

P46-T2 ran the bounded P46 popular-library pilot in static-only mode over the
six pinned local checkouts from P46-T1. The batch passed with no failed
repositories, no preflight warnings, no AI proposals, and no adapter sidecars.
All generated candidates and relations remain producer-side preview evidence.

## Run Root

```text
/tmp/specharvester-p46-t2-bounded-popular-library-static-only-20260620T200603Z
```

## Runtime Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/p46-bounded-popular-library-pilot

PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p46-bounded-popular-library-pilot \
  --out /tmp/specharvester-p46-t2-bounded-popular-library-static-only-20260620T200603Z/output \
  --skip-ai \
  --repository-profile-selection auto
```

## Durable Artifacts

- `tests/fixtures/bounded_popular_library_pilot_static_only_run/p46-t2-bounded-popular-library-pilot-static-only-run.example.json`
- `docs/BOUNDED_POPULAR_LIBRARY_PILOT_STATIC_ONLY_RUN.md`
- `Sources/SpecHarvester/Documentation.docc/BoundedPopularLibraryPilotStaticOnlyRun.md`

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | passed |
| Processed repositories | 6 |
| Failed repositories | 0 |
| Passed preflights | 6 |
| Candidate packages | 9 |
| Relation proposals | 3 |
| Preflight warnings | 0 |
| Repository profile detections | 6 |
| Repository profile selected | 4 |
| Repository profile fallback | 2 |
| AI draft proposals | 0 |
| AI enrichment proposals | 0 |
| Trusted local adapter sidecars | 0 |

Batch report digest:

```text
sha256:01a47a4ceb6d787a11a0059dfca805c35ea51625943bb1873fef5284e271a9b7
```

## Repository Results

| Repository | Status | Candidates | Relations | Profile decision | Interface status |
| --- | --- | ---: | ---: | --- | --- |
| Flask | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Gin | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| xyflow | passed | 4 | 3 | selected `generic.package_set.v0` | partial, 29 diagnostics |
| Cupertino | passed | 1 | 0 | fallback | complete |
| NavigationSplitView | passed | 1 | 0 | fallback | complete |
| docc2context | passed | 1 | 0 | selected `generic.single_package.v0` | complete |

## Boundary Verification

P46-T2 did not run AI, enable trusted local adapter execution, run adapter
code, clone or fetch repositories, install dependencies, invoke package
managers, execute harvested code, accept packages or relations, publish
registry metadata, seed baselines, remove `preview_only`, persist raw prompts,
persist raw provider responses, persist secrets, or persist chain-of-thought.

Static output is not registry truth. AI output and adapter output were not
produced and were not treated as registry truth.

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p46-bounded-popular-library-pilot` | PASS, `repositoryCount: 6` |
| `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p46-bounded-popular-library-pilot --out /tmp/specharvester-p46-t2-bounded-popular-library-static-only-20260620T200603Z/output --skip-ai --repository-profile-selection auto` | PASS, batch status `passed` |
| `python3 -m json.tool tests/fixtures/bounded_popular_library_pilot_static_only_run/p46-t2-bounded-popular-library-pilot-static-only-run.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'bounded_popular_library_pilot_static_only_run'` | PASS, `1 passed, 162 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Remaining Gap

P46-T2 only proves the deterministic static-only gate. P46-T3 must run the same
pinned manifest through the local OpenAI-compatible provider while preserving
proposal-only output and no raw prompt, raw response, secret, or
chain-of-thought persistence.
