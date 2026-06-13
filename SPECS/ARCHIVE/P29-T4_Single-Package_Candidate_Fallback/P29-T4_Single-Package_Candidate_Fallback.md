# P29-T4 Single-Package Candidate Fallback

## Objective

Add a deterministic fallback for repositories that collect useful public
evidence but do not expose package-set workspace topology. The fallback should
let `autonomous-candidate-batch` produce one reviewable preview candidate for
single-package repositories such as Flask and Gin instead of returning `0`
candidates.

This task implements the deterministic producer fallback only. It does not
change SpecPM acceptance, AI repair, registry publishing, or curated package
quality.

## Background

`P29-T3` recorded the mixed Flask/Gin/xyflow baseline:

- Flask and Gin: deterministic collection and preflight were healthy, but
  `draft-package-set` produced `0` candidates and `0` relations.
- xyflow: package-set drafting remained healthy with `4` candidates and `3`
  relations.

The gap exists because `package_set_drafter` currently selects from
`workspace-inventory.json` package records. Python and Go single-package
repositories may have no `package.json` workspace/member records even when
`harvest.json`, README/license evidence, and `public-interface-index.json` are
present.

## Deliverables

- Preserve source manifest `packageId` in `workspace-inventory.json` source
  metadata.
- Add a package-set drafter fallback when selected package records are empty:
  - use the source manifest package id as the fallback candidate id;
  - use the repository-level `harvest.json` beside `workspace-inventory.json`;
  - use colocated `public-interface-index.json` when present;
  - write one candidate bundle with `specpm.yaml`, `specs/*.spec.yaml`,
    `producer-receipt.json`, `validation-report.json`, `diagnostics.json`, and
    `author-ready-draft-quality-report.json`;
  - write `package-set-draft.json` and empty `package-relation-proposals.json`.
- Surface the fallback in autonomous batch output through existing
  `packageSetDraft`, `preflight`, and `authorReadyDraftSummary` fields.
- Add regression tests for:
  - direct package-set drafter fallback;
  - autonomous batch offline fallback on a Python-style single-package repo;
  - workspace inventory source `packageId` preservation;
  - no invented `contains` relations.
- Update docs, DocC, workplan, next task, and validation/archive/review
  artifacts.

## Acceptance Criteria

- A single-package fixture with repository package id `flask.core` produces one
  preview candidate `flask.core`.
- A single-package fixture with repository package id `gin.core` produces one
  preview candidate `gin.core`.
- The fallback candidate includes the colocated `public-interface-index.json`
  when it exists.
- The fallback emits producer receipt, validation report, diagnostics, and
  author-ready quality report artifacts like other preview candidates.
- The fallback writes `0` relation proposals and does not invent `contains`
  relations.
- Bundle-set preflight passes for fallback output.
- The fallback keeps `preview_only`, `producer_preview_evidence_only`, and no
  registry mutation boundaries intact.

## Implementation Plan

1. Extend workspace inventory source metadata with `packageId` from the source
   manifest.
2. Extend `PackageSetDrafter.write_candidates()` with a fallback path when
   `selected_package_records()` returns empty and a source package id is
   available.
3. Build the fallback candidate by calling `draft_spec_package()` over the
   repository-level `harvest.json` colocated with `workspace-inventory.json`,
   optionally passing the colocated `public-interface-index.json`.
4. Record fallback selection metadata in `package-set-draft.json` so reviewers
   can distinguish it from workspace/member selection.
5. Add focused regression tests, then run the Flow gates.

## Non-Goals

- No LM Studio JSON repair/retry. That remains `P29-T5`.
- No broad corpus rerun or readiness decision. That remains `P29-T6`.
- No SpecPM registry acceptance or public index mutation.
- No relation acceptance and no synthetic package-set relation inference.
