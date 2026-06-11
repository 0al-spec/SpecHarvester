# Author-Ready Draft Quality Report

`author-ready-draft-quality-report.json` is a machine-readable producer-side
quality report for generated SpecPM candidate bundles.

It answers one narrow question:

```text
Is this generated output a valid starter package that can be handed to the
repository author for review?
```

It does not answer whether the package is semantically perfect, accepted by
SpecPM, endorsed by the upstream project, or ready for public index publication.

## Contract

The report uses this identity:

```json
{
  "apiVersion": "spec-harvester.author-ready-draft-quality/v0",
  "kind": "SpecHarvesterAuthorReadyDraftQualityReport",
  "schemaVersion": 1
}
```

The main verdict lives under `authorReadyDraft.status` and mirrors the top-level
`status` field:

- `author_ready_draft`: hard gates passed and remaining work is author-review
  work.
- `needs_regeneration`: the draft is structurally usable, but warning-level
  generator or evidence gaps should be reviewed before handoff.
- `blocked`: at least one hard gate failed; do not hand the draft to authors
  until the bundle is regenerated or repaired.

## Inputs

The report is derived from bundle-local producer evidence:

- `validation-report.json`
- `diagnostics.json`
- generated output roles from `producer-receipt.json` planning
- bundled evidence outputs such as `harvest.json` or
  `public-interface-index.json`

For package-set drafts, each member candidate receives its own quality report.
The package-set handoff proposal links those reports as `member_quality_report`
evidence.

## Hard Gates

`hardGates[]` records deterministic producer-side gates:

- `producer_validation`: `validation-report.json` is valid and has no errors.
- `critical_diagnostics`: `diagnostics.json` has no error-level entries.
- `required_bundle_files`: `specpm.yaml`, referenced specs, validation, and
  diagnostics files exist.
- `producer_receipt_planned`: `producer-receipt.json` is not listed in
  `outputs[]`, avoiding a self-hash problem.
- `evidence_links_present`: at least one bundled evidence output is present.
- `authority_boundary`: SpecPM registry acceptance remains external maintainer
  authority.

Failed gates produce `blocked`. Review-required evidence gates produce
`needs_regeneration`.

## Dimensions

`dimensions[]` is advisory and deliberately non-numeric. It exists to guide
author review, not to claim correctness:

- `validation`
- `evidenceCoverage`
- `repositorySpecificity`
- `packageTopology`
- `claimConservatism`
- `authorActionability`
- `authorityBoundary`

These ratings are review hints. They are not a score, benchmark, or acceptance
policy.

## Author Action Items

`authorActionItems[]` is the practical handoff surface. A normal
`author_ready_draft` still includes author tasks such as:

- review package identity, summary, license, keywords, and version;
- review capabilities, intents, constraints, and evidence support;
- run downstream SpecPM validation before public index submission.

When the report is `needs_regeneration` or `blocked`, action items point at the
gate or evidence area that needs correction.

## Receipt Boundary

Generated candidate receipts include the report as:

```json
{
  "path": "author-ready-draft-quality-report.json",
  "role": "quality_report",
  "digest": {
    "algorithm": "sha256",
    "value": "..."
  }
}
```

`producer-receipt.json` must still stay outside `outputs[]`; receipt byte
verification belongs in an external envelope or pull request tooling.

## Non-Authority

The report is review evidence only:

- not SpecPM registry acceptance;
- not maintainer approval;
- not upstream project endorsement;
- not a semantic proof of correctness.

SpecPM and repository authors remain responsible for final semantic curation.
