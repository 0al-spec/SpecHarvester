# P26-T2 — Trusted Package-Set Proposal Workflow Inputs

## Objective

Extend the trusted SpecPM proposal workflow so operators can generate and
upload package-set handoff proposal artifacts as dry-run review evidence
without granting cross-repository write credentials to untrusted pull request
events.

## Scope

In scope:

- Add workflow inputs that select single-package or package-set proposal mode.
- Add package-set bundle/viewer input paths for trusted workflow dispatch or
  trusted `workflow_run` configuration.
- Generate `package-set-handoff-proposal.json` and
  `package-set-handoff-proposal.md` inside the proposal evidence artifact.
- Upload package-set handoff evidence as a GitHub Actions artifact.
- Keep package-set mode dry-run only; it must not push to SpecPM or open a
  cross-repository PR in this task.
- Document the credential boundary and operator flow.

Out of scope:

- SpecPM-side package-set intake checklist. P26-T3 owns that.
- Opening package-set SpecPM PRs with write credentials.
- Accepting packages, accepting relations, or publishing registry metadata.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Workflow contract | Inspect `propose-to-specpm.yml`. | Package-set inputs, dry-run evidence step, artifact upload, and single-package gated write steps are present. |
| Docs contract | Inspect GitHub docs and DocC. | Docs describe trusted package-set dry-run, artifact names, and credential boundary. |
| Existing proposal docs | Ensure single-package proposal automation docs remain linked. | Existing single-package proposal evidence terms still pass. |

## Implementation Plan

1. Extend `.github/workflows/propose-to-specpm.yml` configuration outputs with
   `proposal_kind`, `package_set_bundle_dir`, and `package_set_viewer_dir`.
2. Gate existing single-package materialization, promotion, diff, and PR steps
   behind `proposal_kind == single_package`.
3. Add package-set dry-run evidence generation and upload steps behind
   `proposal_kind == package_set`.
4. Update docs, DocC, tests, validation report, archive, and review artifacts.

## Acceptance Criteria

- Trusted workflow dispatch can select `proposal_kind: package_set`.
- Package-set mode generates and uploads `package-set-handoff-proposal.json`
  and `package-set-handoff-proposal.md`.
- Package-set mode cannot create a SpecPM PR in P26-T2.
- Single-package proposal behavior remains available and gated separately.
- Documentation clearly states that cross-repository write credentials are not
  available to untrusted pull request events and are not used for package-set
  dry-runs.
