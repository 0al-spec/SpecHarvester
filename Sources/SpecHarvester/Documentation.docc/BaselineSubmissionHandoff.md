# Baseline Submission Handoff

`baseline-submission-handoff` records the producer-side boundary for
repositories that do not yet have current SpecPM generated artifacts.

Use it after `fresh-candidate-refresh-run` and, when available, a SpecPM
`prepare-report.json` containing
`refresh_decision_prepare_current_contract_files_missing`:

```bash
python3 -m spec_harvester baseline-submission-handoff \
  --fresh-candidate-refresh-run .smoke/tanstack-query/fresh-candidate-refresh-run.json \
  --specpm-prepare-report .smoke/tanstack-query/prepare-report.json \
  --output .smoke/tanstack-query/baseline-submission-handoff.json
```

The output uses:

```json
{
  "apiVersion": "spec-harvester.baseline-submission-handoff/v0",
  "kind": "SpecHarvesterBaselineSubmissionHandoff",
  "schemaVersion": 1
}
```

When the SpecPM prepare report contains missing-baseline diagnostics, the
artifact status is `first_submission_required`. Without a prepare report, the
status is `baseline_review_required`.

The artifact records source revision, package-set member ids, candidate count,
contract file count, sample missing-baseline diagnostics, and maintainer action
options: `first_submission_review`, `seed_baseline`, and
`reject_or_request_regeneration`.

It is not a refresh decision. The authority boundary remains
`producerEvidenceAuthority: evidence_only`, `noRegistryMutation: true`, and
`notRefreshDecision: true`. It does not mutate baselines automatically. SpecPM
maintainers still own registry acceptance and baseline seeding.
