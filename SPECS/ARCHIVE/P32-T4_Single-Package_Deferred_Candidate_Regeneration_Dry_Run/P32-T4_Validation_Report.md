# P32-T4 Validation Report

Task: `P32-T4 Single-Package Deferred Candidate Regeneration Dry Run`

Date: 2026-06-13

## Summary

P32-T4 ran the bounded deferred single-package regeneration path for
`cupertino` and `navigation-split-view` only.

Result:

- `cupertino.core`: valid preview bundle, clean producer preflight and viewer,
  but still `needs_regeneration` because AI enrichment reports
  `refined_summary_missing`.
- `navigation_split_view.core`: valid preview bundle, canonical underscore id
  confirmed across manifest, generated `specpm.yaml`, validation, candidate
  preflight, bundle-set preflight, and viewer. It is
  `candidate_layer_review_required` with `selectedHandoffEligible: true`.

No package was accepted, no relation was accepted, no baseline was seeded, no
`preview_only` was removed, no registry metadata was published, and no SpecPM
pull request was created.

## Source Inputs

Source manifest:

```text
inputs/limited-popular-libraries/repositories.yml
```

Validation:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests inputs/limited-popular-libraries
```

Result:

```text
status: ok
repositoryCount: 6
```

Pinned checkout verification:

```bash
git -C /Users/egor/Development/GitHub/cupertino rev-parse HEAD
git -C /Users/egor/Development/GitHub/cupertino status --short --branch
git -C /Users/egor/Development/GitHub/NavigationSplitView rev-parse HEAD
git -C /Users/egor/Development/GitHub/NavigationSplitView status --short --branch
```

Result:

```text
cupertino: 65dcae238d30cfbd0d9d15ae10f7b8c67575c19b, clean
NavigationSplitView: 2c88df50b8f587560b91f6027e9ea275aee17060, clean
```

LM Studio provider check:

```bash
curl -sS --max-time 5 http://127.0.0.1:1234/v1/models
```

Result:

```text
openai/gpt-oss-20b available
```

## Dry Run

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --select cupertino \
  --select navigation-split-view \
  --out .smoke/p32-deferred-regeneration/20260613T184534Z/single-package \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Result:

```text
status: passed
processedCount: 2
skippedCount: 4
passedPreflightCount: 2
aiDraftProposalCount: 2
aiEnrichmentProposalCount: 2
```

Candidate paths:

```text
.smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/cupertino/cupertino.core
.smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/navigation-split-view/navigation_split_view.core
```

## Candidate Preflight and Viewer

Commands:

```bash
PYTHONPATH=src python -m spec_harvester render-spec-site \
  --candidate .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/cupertino/cupertino.core \
  --output .smoke/p32-deferred-regeneration/20260613T184534Z/viewer/cupertino.core

PYTHONPATH=src python -m spec_harvester preflight-candidate-bundle \
  .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/cupertino/cupertino.core

PYTHONPATH=src python -m spec_harvester render-spec-site \
  --candidate .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/navigation-split-view/navigation_split_view.core \
  --output .smoke/p32-deferred-regeneration/20260613T184534Z/viewer/navigation_split_view.core

PYTHONPATH=src python -m spec_harvester preflight-candidate-bundle \
  .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/navigation-split-view/navigation_split_view.core
```

Result:

```text
cupertino.core viewer: status ok
cupertino.core candidate preflight: passed, warnings 0, errors 0
navigation_split_view.core viewer: status ok
navigation_split_view.core candidate preflight: passed, warnings 0, errors 0
```

## Recorded Artifacts

- `docs/SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`
- `Sources/SpecHarvester/Documentation.docc/SinglePackageDeferredCandidateRegenerationDryRun.md`
- `tests/fixtures/single_package_deferred_candidate_regeneration/p32-t4-single-package-deferred-candidate-regeneration.example.json`

## Quality Gates

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` | PASS, `74 passed` |
| `PYTHONPATH=src pytest -q` | PASS, `650 passed, 1 skipped` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS, `107 files already formatted` |
| `git diff --check` | PASS |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90` | PASS, `650 passed, 1 skipped`, coverage `90.56%` |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory /tmp/specharvester-p32-t4-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p32-t4-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings for `AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport` inline code references |

## Verdict

PASS.

P32-T4 satisfies the dry-run objective: the current corpus now has recorded
single-package deferred candidate regeneration evidence. `navigation_split_view.core`
can move into P32-T5 refreshed candidate-layer triage, while `cupertino.core`
stays explicitly deferred until its remaining enrichment summary gap is
resolved.
