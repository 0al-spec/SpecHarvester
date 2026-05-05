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
