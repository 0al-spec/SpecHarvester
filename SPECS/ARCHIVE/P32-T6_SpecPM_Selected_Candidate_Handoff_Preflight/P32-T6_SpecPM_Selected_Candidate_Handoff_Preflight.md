# P32-T6 SpecPM Selected Candidate Handoff Preflight

Status: Archived
Phase: Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness
Owner: SpecHarvester coordination, SpecPM consumer gate

## Motivation

P32-T5 produced a refreshed selected handoff artifact for the limited popular
library corpus. The artifact is intentionally producer preview evidence: it
selects eight reviewable candidates and keeps `cupertino.core` deferred, but it
does not have SpecPM registry authority.

Before P32-T7 can record an intake readiness decision, SpecPM needs to prove it
can consume and validate the handoff shape independently.

## Goal

Record the completed SpecPM-side consumer gate for selected candidate handoff
evidence and verify it against the committed P32-T5 fixture.

## Deliverables

- Link the merged SpecPM implementation PR:
  [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140).
- Run `specpm producer-bundle preflight-selected-candidate-handoff` against
  the committed P32-T5 refreshed selected handoff fixture.
- Record the selected/deferred candidate counts and digest verification result.
- Mark P32-T6 complete in `SPECS/Workplan.md`.
- Advance `SPECS/INPROGRESS/next.md` to P32-T7.

## Acceptance Criteria

- SpecPM PR #140 is merged.
- The P32-T5 fixture passes SpecPM selected candidate handoff preflight.
- The preflight report remains non-authoritative review evidence:
  it does not accept packages, accept relations, seed baselines, remove
  `preview_only`, publish registry metadata, or create a SpecPM PR.
- P32-T7 is the next selected task.

## Non-Goals

- Do not regenerate any candidate.
- Do not edit candidate bundles or fixtures.
- Do not submit accepted packages to SpecPM.
- Do not resolve the deferred `cupertino.core` blocker.

## Archive

Archived: 2026-06-13
Verdict: PASS

SpecPM PR [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140)
was merged at revision `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.

The committed P32-T5 refreshed selected handoff fixture passed
`specpm producer-bundle preflight-selected-candidate-handoff` with eight
selected candidates, one deferred candidate (`cupertino.core`), zero warnings,
zero errors, and three source digests verified.

The next selected task is P32-T7: record the limited corpus intake readiness
decision using the P32-T5 producer evidence and P32-T6 SpecPM consumer preflight
result.
