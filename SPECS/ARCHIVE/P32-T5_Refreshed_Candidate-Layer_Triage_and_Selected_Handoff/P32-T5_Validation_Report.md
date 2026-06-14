# P32-T5 Validation Report

Task: `P32-T5 Refreshed Candidate-Layer Triage and Selected Handoff`
Date: 2026-06-13
Verdict: PASS

## Scope

P32-T5 records refreshed selected handoff evidence by combining committed
P30-T5, P32-T3, and P32-T4 fixtures. No new repository harvest, no LM Studio
run, no generated candidate mutation, and no SpecPM mutation were performed.

The recorded result selects eight preview candidates:

- `flask.core`
- `gin.core`
- `docc2context.core`
- `xyflow.workspace`
- `xyflow.react`
- `xyflow.svelte`
- `xyflow.system`
- `navigation_split_view.core`

`cupertino.core` remains deferred because `refined_summary_missing` is still
unresolved.

## Artifacts

- `tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json`
- `docs/REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`
- `Sources/SpecHarvester/Documentation.docc/RefreshedCandidateLayerSelectedHandoff.md`

## Validation

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `75 passed`

```bash
PYTHONPATH=src pytest -q
```

Result before final format pass: `651 passed, 1 skipped`

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90
```

Result: `651 passed, 1 skipped`; coverage `90.56%`

```bash
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed

```bash
swift build --target SpecHarvesterDocs
```

Result: passed

```bash
rm -rf /tmp/specharvester-p32-t5-docc-build-spec
swift package --allow-writing-to-directory /tmp/specharvester-p32-t5-docc-build-spec \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-p32-t5-docc-build-spec \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Result: passed. The command emitted pre-existing unrelated DocC warnings for
`AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

## Boundary

- No new harvest was run.
- No LM Studio or AI provider call was run.
- No generated candidate bundle was mutated.
- No SpecPM repository file was changed.
- No package or relation was accepted.
- No baseline was seeded.
- No `preview_only` marker was removed.
- No registry metadata was published.
- No SpecPM pull request was created.

