# SpecHarvester Documentation

This directory is the operator and design entrypoint for SpecHarvester.

Use it the same way the SpecPM repository uses GitHub-facing documentation:
start from the workflow, then drill into architecture, trust boundaries, and
automation details.

Published DocC site:
[https://0al-spec.github.io/SpecHarvester/](https://0al-spec.github.io/SpecHarvester/).

## Read This First

1. [`../README.md`](../README.md): repository overview and GitHub workflow surface
2. [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md): end-to-end operator flow
3. [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md): non-negotiable execution rules
4. [`../SPECS/README.md`](../SPECS/README.md): Flow workflow for planning,
   implementing, validating, and archiving tasks

## Design References

- [`ARCHITECTURE.md`](ARCHITECTURE.md): component model and non-goals
- [`ROADMAP.md`](ROADMAP.md): implementation phases and future tracks
- [`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md): trusted
  automation for proposing accepted-source diffs into SpecPM

## GitHub Process Surface

- Pull requests: [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md)
- Issue forms: [`.github/ISSUE_TEMPLATE`](../.github/ISSUE_TEMPLATE)
- CI: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Cross-repository proposal automation:
  [`.github/workflows/propose-to-specpm.yml`](../.github/workflows/propose-to-specpm.yml)

## Operator Checklist

- Start from a public repository checkout pinned to a revision.
- Collect bounded static evidence into `harvest.json`.
- Draft deterministic candidate SpecPM files.
- Validate the candidate with SpecPM.
- Review provenance, scope, and inferred metadata.
- Promote only reviewed candidates into accepted-source staging.
