# Limited Popular-Library Selected Handoff Dry Run

This page records the P30-T5 selected candidate handoff dry run for
`flask.core`, `gin.core`, and `docc2context.core`.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json
```

Its identity is
`SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun` with
`apiVersion: spec-harvester.limited-popular-library-selected-handoff-dry-run/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Inputs

The dry run consumes P30-T2 deterministic evidence, P30-T3 live LM Studio
evidence, and the P30-T4 candidate-layer triage fixture. It does not run
another scrape, call LM Studio, clone repositories, install dependencies,
generate accepted-source content, or create a SpecPM pull request.

## Selected Candidates

| Candidate | Producer preflight | Viewer | Registry acceptance |
| --- | --- | --- | --- |
| `flask.core` | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |
| `gin.core` | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |
| `docc2context.core` | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |

Each selected candidate records SHA-256 digests for `specpm.yaml`,
`specs/*.spec.yaml`, `producer-receipt.json`, `validation-report.json`,
`diagnostics.json`, `author-ready-draft-quality-report.json`, producer
preflight JSON, static viewer `index.html`, and static viewer
`spec-package.json`.

## Deferred Candidates

P30-T5 intentionally excludes `xyflow.workspace`, `xyflow.react`,
`xyflow.svelte`, `xyflow.system`, `cupertino.core`, and
`navigation_split_view.core`. All six remain `needs_regeneration` before any
selected handoff dry run.

## Product Verdict

Verdict: `selected_handoff_dry_run_ready`.

The selected candidates have reviewable producer evidence, passing
producer-side preflight reports, and static viewer artifacts for future SpecPM
review. They remain producer preview evidence only. The dry run does not remove
`preview_only`, run `prepare-accepted-entry`, run
`accepted-package-update-proposal`, publish registry metadata, create a SpecPM
pull request, or replace maintainer review.

The dry run cannot accept packages, accept relations, seed baselines, publish
registry metadata, or treat producer output as accepted SpecPM truth.

See also <doc:LimitedPopularLibraryCandidateLayerTriage>,
<doc:LimitedPopularLibraryLiveLMStudioBatch>,
<doc:LimitedPopularLibraryDeterministicBatch>,
<doc:LimitedPopularLibraryCorpusPlan>, and <doc:SpecPMHandoff>.
