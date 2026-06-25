# P51-T4 Validation Report

**Task:** `P51-T4` Larger Curated Corpus Static-Only Gate
**Date:** 2026-06-25
**Verdict:** PASS

## Summary

P51-T4 ran the larger curated corpus static-only gate over the 12 selected
P51 sources. The batch passed with no failed repositories, no preflight
warnings, no AI proposals, and no adapter sidecars. All generated candidates
and relations remain producer-side preview evidence only.

P51-T5 AI-enabled proposal-only execution is allowed.

## Run Root

```text
/tmp/specharvester-p51-t4-larger-curated-corpus-static-only-20260625T103322Z
```

## Runtime Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/p51-larger-curated-corpus

PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p51-larger-curated-corpus \
  --out /tmp/specharvester-p51-t4-larger-curated-corpus-static-only-20260625T103322Z/output \
  --skip-ai \
  --repository-profile-selection auto
```

## Durable Artifacts

- `tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json`
- `docs/LARGER_CURATED_CORPUS_STATIC_ONLY_GATE.md`
- `Sources/SpecHarvester/Documentation.docc/LargerCuratedCorpusStaticOnlyGate.md`

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | passed |
| Processed repositories | 12 |
| Failed repositories | 0 |
| Passed preflights | 12 |
| Candidate packages | 15 |
| Relation proposals | 3 |
| Preflight warnings | 0 |
| Repository profile detections | 12 |
| Repository profile selected | 10 |
| Repository profile fallback | 2 |
| Author-ready drafts | 15 |
| AI draft proposals | 0 |
| AI enrichment proposals | 0 |
| Trusted local adapter sidecars | 0 |

Batch report digest:

```text
sha256:2f6bd4e6f8762463d1698be5bfa3369e7fbdae8214d3cbb8b552a15855e73823
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
| FastAPI | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| FastMCP | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| SpecPM | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Hypercode | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| SpecNode | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Hyperprompt | passed | 1 | 0 | selected `generic.single_package.v0` | complete |

## Caveats Carried Forward

- `xyflow.operator_checkout_origin_fork_mismatch`
- `docc2context.source_checkout_had_untracked_doccarchive`

These are non-blocking for P51-T4 and remain review evidence for P51-T6 triage.

## Boundary Verification

P51-T4 did not run AI, enable trusted local adapter execution, run adapter
code, clone or fetch repositories, install dependencies, invoke package
managers, execute harvested code, accept packages or relations, publish
registry metadata, seed baselines, remove `preview_only`, persist raw prompts,
persist raw provider responses, persist secrets, or persist chain-of-thought.

Static output is not registry truth. AI output and adapter output were not
produced and were not treated as registry truth.

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p51-larger-curated-corpus` | PASS, `repositoryCount: 12` |
| `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p51-larger-curated-corpus --out /tmp/specharvester-p51-t4-larger-curated-corpus-static-only-20260625T103322Z/output --skip-ai --repository-profile-selection auto` | PASS, batch status `passed` |
| `python3 -m json.tool tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_static_only_gate or larger_curated_corpus_checkout_readiness or larger_curated_corpus_source_plan or larger_curated_corpus_planning_phase"` | PASS, `4 passed, 180 deselected` |
| `python3 -m ruff format tests/test_docs_contracts.py` | PASS, `1 file reformatted` |
| `git diff --check` | PASS |
| `python3 -m ruff format --check src tests` | PASS, `131 files already formatted` |
| `python3 -m ruff check src tests` | PASS, `All checks passed!` |
| `PYTHONPATH=src python3 -m pytest` | PASS, `915 passed, 1 skipped` |
| `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `915 passed, 1 skipped`; total coverage `90.48%` |
| `swift package dump-package` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package describe` | PASS |
| `swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs` | PASS |

## Next Step

P51-T5 should run the larger curated corpus AI-enabled proposal-only gate using
the same P51 manifest, preserving all no-registry-authority and no raw
prompt/response persistence boundaries.
