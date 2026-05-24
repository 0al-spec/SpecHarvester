# P15-T5 Convert Validation Failures into Follow-Up Workplan Tasks

Status: Planned
Task: `P15-T5`
Phase: Phase 15. Real Repository Refinement Validation
Priority: P1
Effort: 2-4 hours
Dependencies: `P15-T4`

## Problem

P15-T4 ran the current SpecHarvester implementation against six real public
repository checkouts and found repeated advisory failure classes.  Those
failures should not be fixed by one-off prompt edits or hidden manual
corrections.  They need to become explicit, reviewable Workplan tasks with
clear scope, acceptance criteria, and boundaries.

## Observed Failure Classes

- Broad duplicate semantic intents across unrelated candidates, especially
  generic documentation/API/tooling claims.
- Quality report analyzer coverage undercount for candidates that generated
  `public-interface-index.json`.
- Governance license provenance classification gap where Flask's `LICENSE.txt`
  was collected but still surfaced as ambiguous unknown license evidence.
- Package identity normalization mismatch where hyphen/underscore differences
  produced low-signal namespace/upstream advisory noise.

## Goals

- Convert the repeated P15-T4 failure classes into focused Workplan follow-up
  tasks.
- Avoid duplicating already-completed tasks such as P12-T1 strict license
  filename compatibility or P7 namespace owner/repository matching.
- Define each follow-up with enough acceptance criteria that future PRs can be
  implemented and reviewed independently.
- Keep the source of truth in `SPECS/Workplan.md` and update `next.md` to the
  first actionable follow-up after P15-T5.

## Non-Goals

- Do not implement analyzer, quality-report, license, namespace, or semantic
  extraction fixes in this task.
- Do not rerun the full P15-T4 real-repository matrix unless needed to clarify
  task wording.
- Do not commit generated `.smoke/` outputs.
- Do not change SpecPM contracts or SpecNode boundaries.

## Deliverables

1. New Workplan follow-up tasks for the actionable P15-T4 failure classes.
2. Updated `SPECS/INPROGRESS/next.md` pointing at the first follow-up task.
3. A validation report documenting duplicate checks, task mapping, and quality
   gate results.

## Acceptance Criteria

- Every P15-T4 failure class is either mapped to a new Workplan task or
  explicitly marked as already covered by an existing task.
- New tasks distinguish deterministic analyzer/reporting/policy fixes from
  model prompt tuning.
- The first follow-up task is suggested in `next.md`.
- Markdown quality checks pass through the configured Flow gates or equivalent
  scoped validation.
