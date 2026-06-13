# P30-T5 Selected Candidate Handoff Dry Run

## Objective

Prepare SpecPM handoff dry-run evidence for the P30 selected candidates only:

- `flask.core`;
- `gin.core`;
- `docc2context.core`.

The dry run must prove that selected candidate bundles have reviewable producer
evidence, producer-side preflight reports, and static viewer artifacts without
creating a SpecPM pull request or treating producer output as accepted registry
truth.

## Background

P30-T4 recorded the candidate-layer triage report:

```text
tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json
```

The triage selected three candidates for dry-run handoff and deferred six
candidates:

```text
selected: flask.core, gin.core, docc2context.core
deferred: xyflow.workspace, xyflow.react, xyflow.svelte, xyflow.system,
          cupertino.core, navigation_split_view.core
```

P30-T5 must not override those triage decisions. It should package evidence
only for selected candidates and make every omitted candidate explicit.

## Deliverables

- Add a machine-readable selected-candidate handoff dry-run fixture that
  records:
  - corpus identity and source fixture links;
  - selected candidate ids;
  - excluded/deferred candidate ids with reasons;
  - candidate bundle paths from the recorded P30-T3 run;
  - required candidate files and SHA-256 digests;
  - producer preflight report paths/digests/statuses;
  - static viewer artifact paths/digests/statuses;
  - registry acceptance boundary.
- Add GitHub docs and DocC coverage for the dry run.
- Link the dry-run report from README, roadmap, SpecPM handoff docs, corpus
  plan, live LM Studio batch docs, and candidate-layer triage docs.
- Add regression tests covering selected candidates, deferred candidates,
  digests, preflight status, viewer status, and non-authority boundaries.
- Archive Flow artifacts and mark Phase 30 complete unless new P30 follow-up
  tasks are discovered during review.

## Dry-Run Boundary

P30-T5 can:

- verify candidate bundles with `preflight-candidate-bundle`;
- render static review sites with `render-spec-site`;
- record evidence links and digests;
- recommend selected candidates for future SpecPM review.

P30-T5 cannot:

- run another scrape;
- call LM Studio;
- create a SpecPM pull request;
- run `prepare-accepted-entry`;
- run `accepted-package-update-proposal`;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- treat producer output as accepted SpecPM truth.

## Acceptance Criteria

- The fixture includes exactly three selected candidates:
  `flask.core`, `gin.core`, and `docc2context.core`.
- The fixture excludes all six P30-T4 deferred candidates and records why.
- Each selected candidate records required handoff files:
  - `specpm.yaml`;
  - `specs/*.spec.yaml`;
  - `producer-receipt.json`;
  - `validation-report.json`;
  - `diagnostics.json`;
  - `author-ready-draft-quality-report.json`.
- Each selected candidate records producer preflight status `passed` with zero
  warnings/errors.
- Each selected candidate records static viewer output status `ok`.
- The dry-run product verdict is explicit and does not imply SpecPM registry
  acceptance.
- Tests verify the docs and fixture contract.

## Non-Goals

- No broad P30 corpus rerun.
- No package-set handoff for xyflow.
- No curation of selected package semantics.
- No SpecPM repository mutation or PR creation.
- No registry publication, accepted-source update, relation acceptance, or
  baseline seeding.
