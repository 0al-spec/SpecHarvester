# P20-T5 Scoped Source-Unit Draft Intent Boundaries

**Status:** Planned
**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Dependencies:** P20-T4, P17-T6

## Problem

Scoped source harvesting can now collect repository roots, folders, and single
files while preserving owning repository provenance. Drafting and refinement
still need an explicit intent boundary so generated specs do not accidentally
upgrade scoped evidence into repository-level or package-manager ownership
claims.

Without that boundary, a folder or file candidate can look like a full package
candidate to downstream reviewers and to SpecNode refinement prompts.

## Goal

Make the generated draft and SpecNode refinement input distinguish:

- repository intent;
- package intent;
- folder/module intent;
- single-file source-unit intent.

The output should remain a valid starter package, but claims must stay scoped to
the evidence that was actually harvested.

## Deliverables

- Add a deterministic source-unit intent boundary representation for draft
  generation.
- Surface that boundary in generated manifest/spec metadata using conservative
  language for folder and single-file targets.
- Pass the same boundary into SpecNode refinement preview/model input so later
  refinement cannot treat scoped evidence as package-manager ownership.
- Add characterization tests for scoped folder and single-file behavior.
- Record validation results in the task validation report.

## Non-Goals

- Do not implement the CodeGraph adapter.
- Do not introduce new source graph evidence shapes.
- Do not change SpecPM registry acceptance policy.
- Do not auto-promote scoped source units into package-set members.

## Acceptance Criteria

- Folder targets generate draft language that identifies the candidate as a
  folder/module source unit and warns against repository/package ownership
  overclaiming.
- Single-file targets generate draft language that identifies the candidate as a
  single-file source unit and warns against repository/package ownership
  overclaiming.
- Repository/package targets keep their current broad behavior unless the new
  boundary can describe them without changing semantics.
- SpecNode refinement preview/model input includes the source-unit boundary for
  the selected candidate.
- Existing draft, refinement, quality-report, and handoff tests pass.

## Validation Plan

- Targeted pytest for scoped-source draft tests.
- Targeted pytest for SpecNode refinement smoke tests.
- Full pytest suite.
- Ruff check and format check.
- Swift docs build and DocC generation if the task changes public docs.
