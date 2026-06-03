# Proposal Automation

SpecHarvester can prepare proposal pull requests in the SpecPM repository after
a candidate has been generated, validated, and promoted into a SpecPM
accepted-source diff.

This automation is intentionally a proposal mechanism. It does not publish
directly to the public registry.

## Flow

```text
SpecHarvester candidate
        |
        v
SpecHarvester validation and promotion
        |
        v
trusted proposal workflow
        |
        v
PR in 0al-spec/SpecPM
        |
        v
SpecPM CI and maintainer review
        |
        v
merge to SpecPM main
        |
        v
GitHub Pages /v0 publication
```

## Workflow Entry Point

The trusted automation lives in:

```text
.github/workflows/propose-to-specpm.yml
```

It can run in two trusted modes:

- manual `workflow_dispatch`;
- `workflow_run` after `CI` succeeds on `main`, only when explicitly enabled
  through repository variables.

It must not run with write credentials on ordinary `pull_request` events.

## Preflight Validation

Before writing proposal diffs, the workflow validates the candidate and expected
proposal identity:

- candidate directory presence
- `specpm` candidate validation (`specpm.cli validate`)
- producer bundle preflight (`preflight-candidate-bundle`)
- static viewer rendering (`render-spec-site`)
- candidate metadata identity:
  - `metadata.id` matches workflow `package_id`
  - `metadata.version` matches workflow `package_version`
- symlink rejection for candidate manifest reads

The workflow uploads the producer preflight report and static viewer as a
workflow artifact. Pull request bodies opened against SpecPM link the accepted
source bundle path, `specpm.yaml`, `producer-receipt.json`,
`validation-report.json`, `diagnostics.json`, the preflight artifact, the
static viewer artifact, and the accepted-source diff. These links are review evidence
only; SpecPM maintainers still own acceptance.

The stable evidence roles and expected inputs for a future optional SpecPM CI
preflight gate are covered by <doc:SpecPMCiPreflightGateSupport>. Such a gate
may consume proposal evidence, but it must not replace maintainer review.

After promotion and `public-index generate`, proposal diff scope is validated.
Allowed changed files are:

- `public-index/generated/<packageId>/<packageVersion>/*`
- `public-index/accepted-packages.yml`

Any unexpected changed file fails the workflow before PR creation.

## Required Secret

To create a pull request in SpecPM, configure:

```text
SPECPM_PROPOSAL_TOKEN
```

The token should be a GitHub App installation token or a narrowly scoped token
with write access to `0al-spec/SpecPM`.

## References

- `docs/SPECPM_PROPOSAL_AUTOMATION.md`
- <doc:Workflow>
- <doc:TrustBoundary>
