# P30-T5 Validation Report

Task: P30-T5 Selected Candidate Handoff Dry Run

## Summary

P30-T5 records selected SpecPM handoff dry-run evidence for:

- `flask.core`;
- `gin.core`;
- `docc2context.core`.

The dry run keeps all output as `producer_preview_evidence_only` and
`preview_only`. It records producer preflight reports, static viewer digests,
required bundle file digests, deferred candidates, and
`registryAcceptanceDecision.status: external_required` without creating a
SpecPM pull request or treating producer output as accepted registry truth.

## Artifacts

- Fixture:
  `tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json`
- GitHub docs:
  `docs/LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`
- DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/LimitedPopularLibrarySelectedHandoffDryRun.md`
- Linked docs:
  - `docs/README.md`
  - `docs/ROADMAP.md`
  - `docs/SPECPM_HANDOFF.md`
  - `docs/LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`
  - `docs/LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`
  - `docs/LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`
  - DocC mirrors for the same pages
- Regression tests:
  `tests/test_docs_contracts.py`

## Recorded Dry-Run Evidence

Source candidate root:

```text
/tmp/specharvester-p30-t3.f7iGn0/live-lm-studio/package-sets
```

P30-T5 dry-run root:

```text
/tmp/specharvester-p30-t5-selected-handoff
```

Selected candidates:

| Candidate | Preflight | Warnings | Errors | Viewer |
| --- | --- | ---: | ---: | --- |
| `flask.core` | `passed` | `0` | `0` | `ok` |
| `gin.core` | `passed` | `0` | `0` | `ok` |
| `docc2context.core` | `passed` | `0` | `0` | `ok` |

Deferred candidates:

- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`;
- `cupertino.core`;
- `navigation_split_view.core`.

## Validation Commands

Fixture JSON:

```bash
python -m json.tool \
  tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json \
  >/tmp/p30-t5-fixture.json
```

Result: passed.

Docs contract regression:

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `65 passed`.

Full test suite:

```bash
PYTHONPATH=src pytest -q
```

Result: `633 passed, 1 skipped`.

Coverage gate:

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `633 passed, 1 skipped`, total coverage `90.58%`.

Lint:

```bash
PYTHONPATH=src ruff check .
```

Result: passed.

Format check:

```bash
PYTHONPATH=src ruff format --check src tests
```

Result: passed.

Whitespace check:

```bash
git diff --check
```

Result: passed.

Swift package manifest:

```bash
swift package dump-package >/tmp/specharvester-p30-t5-package.json
```

Result: passed.

Swift docs target:

```bash
swift build --target SpecHarvesterDocs
```

Result: passed.

Static DocC generation:

```bash
rm -rf /tmp/specharvester-p30-t5-docc-build-spec
swift package \
  --allow-writing-to-directory /tmp/specharvester-p30-t5-docc-build-spec \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-p30-t5-docc-build-spec \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Result: passed. Existing unrelated DocC warnings remain for
`AcceptedPackageUpdateProposals` and inline command references in
`RealRepositoryQualityReport`.

## Verdict

PASS.

P30-T5 satisfies the PRD: selected candidates have digest-backed producer
preflight and static viewer dry-run evidence, all deferred candidates remain
explicitly excluded, and no SpecPM acceptance, relation acceptance, baseline
seeding, registry publication, or pull request creation is implied.
