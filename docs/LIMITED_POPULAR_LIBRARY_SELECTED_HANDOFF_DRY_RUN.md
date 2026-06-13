# Limited Popular-Library Selected Handoff Dry Run

Status: P30-T5 selected candidate dry-run evidence.

This page records the P30-T5 handoff dry run for the selected candidate-layer
review packages from P30-T4:

- `flask.core`;
- `gin.core`;
- `docc2context.core`.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.limited-popular-library-selected-handoff-dry-run/v0",
  "kind": "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P30-T5 consumes already-recorded evidence only:

- P30-T2 deterministic fixture:
  `tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json`;
- P30-T3 live LM Studio fixture:
  `tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json`;
- P30-T4 candidate-layer triage fixture:
  `tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json`.

It does not run another scrape, call LM Studio, clone repositories, install
dependencies, generate accepted-source content, or create a SpecPM pull
request.

## Selected Candidates

| Candidate | Repository | Producer preflight | Viewer | Registry acceptance |
| --- | --- | --- | --- | --- |
| `flask.core` | Flask | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |
| `gin.core` | Gin | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |
| `docc2context.core` | docc2context | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |

Each selected candidate records SHA-256 digests for:

- `specpm.yaml`;
- `specs/*.spec.yaml`;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- `author-ready-draft-quality-report.json`;
- producer preflight report JSON;
- static viewer `index.html`;
- static viewer `spec-package.json`.

The preflight reports have identity
`SpecHarvesterCandidateBundlePreflightReport` and authority
`producer_side_preflight`.

## Deferred Candidates

P30-T5 intentionally excludes the six P30-T4 deferred candidates:

- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`;
- `cupertino.core`;
- `navigation_split_view.core`.

All six remain `needs_regeneration`. They require package-set identity fixes,
AI draft regeneration, enrichment regeneration, author-supplied summary
evidence, or package-id normalization before a selected handoff dry run.

## Product Verdict

Verdict: `selected_handoff_dry_run_ready`.

The selected candidates have reviewable producer evidence, passing
producer-side preflight reports, and static viewer artifacts. This is enough
for a future SpecPM review dry run, but it is not enough for registry
acceptance.

P30-T5 does not remove `preview_only`. It does not run
`prepare-accepted-entry` or `accepted-package-update-proposal`. It does not
publish registry metadata or create a SpecPM pull request.

## Commands

Producer-side preflight:

```bash
PYTHONPATH=src python -m spec_harvester preflight-candidate-bundle \
  /tmp/specharvester-p30-t3.f7iGn0/live-lm-studio/package-sets/flask/flask.core
```

Static viewer render:

```bash
PYTHONPATH=src python -m spec_harvester render-spec-site \
  --candidate /tmp/specharvester-p30-t3.f7iGn0/live-lm-studio/package-sets/flask/flask.core \
  --output /tmp/specharvester-p30-t5-selected-handoff/viewers/flask.core
```

The same commands were run for `gin.core` and `docc2context.core`.

## Non-Authority Boundary

The dry run cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- replace author or SpecPM maintainer review;
- treat producer output as accepted SpecPM truth.

See also:

- [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
- [`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md)
- [`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md)
- [`LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`](LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
