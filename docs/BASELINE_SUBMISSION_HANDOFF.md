# Baseline Submission Handoff

Status: producer review evidence

`baseline-submission-handoff` records the boundary for repositories that do not
yet have current SpecPM generated artifacts. It is used after
`fresh-candidate-refresh-run` and, when available, a SpecPM
`prepare-report.json` containing
`refresh_decision_prepare_current_contract_files_missing`.

The artifact is not a refresh decision. It is a handoff that says a maintainer
must choose first submission, seeded baseline, or rejection before future
refresh comparison can produce a normal decision file.

## Command

```bash
python3 -m spec_harvester baseline-submission-handoff \
  --fresh-candidate-refresh-run .smoke/tanstack-query/fresh-candidate-refresh-run.json \
  --specpm-prepare-report .smoke/tanstack-query/prepare-report.json \
  --output .smoke/tanstack-query/baseline-submission-handoff.json
```

`--specpm-prepare-report` is optional. When provided, it must contain
`refresh_decision_prepare_current_contract_files_missing`; otherwise the
command exits with an error instead of producing a misleading first-submission
artifact.

## JSON Identity

```json
{
  "apiVersion": "spec-harvester.baseline-submission-handoff/v0",
  "kind": "SpecHarvesterBaselineSubmissionHandoff",
  "schemaVersion": 1
}
```

The artifact records:

- digest-backed `freshCandidateRefreshRun` input;
- optional digest-backed SpecPM `prepare-report.json` input;
- source repository and revision;
- package-set id, member package ids, candidate count, and contract file count;
- missing-baseline diagnostic count and sample diagnostics;
- maintainer actions: `first_submission_review`, `seed_baseline`, and
  `reject_or_request_regeneration`;
- authority boundaries including `producerEvidenceAuthority: evidence_only`,
  `noRegistryMutation: true`, and `notRefreshDecision: true`.

## Status Values

- `first_submission_required`: a SpecPM prepare report confirmed missing
  generated baseline diagnostics.
- `baseline_review_required`: no SpecPM prepare report was supplied, so the
  handoff is review evidence but the missing-baseline diagnostic is not
  confirmed in the artifact.

## Boundary

Generated candidates remain producer evidence. This command does not:

- mutate SpecPM accepted sources;
- seed SpecPM automatically;
- emit `refresh-decision.json`;
- accept packages or relations;
- publish public registry metadata;
- execute source repository code;
- run package managers.

SpecPM maintainers still own registry acceptance and baseline seeding.
