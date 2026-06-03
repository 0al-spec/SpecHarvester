# SpecPM CI Preflight Gate Support

SpecHarvester can prepare evidence for a future optional SpecPM CI preflight
gate without making generated producer output registry authority.

## Boundary

The intended boundary is:

```text
SpecHarvester generated bundle
        -> stable producer evidence layout
        -> optional SpecPM CI preflight
        -> SpecPM maintainer review
        -> registry acceptance decision
```

It is not:

```text
SpecHarvester preflight passed -> SpecPM accepts package automatically
```

SpecHarvester owns the producer evidence shape. SpecPM owns CI policy,
registry intake checks, accepted-source diff validation, and maintainer
acceptance.

## Inputs

A future SpecPM CI preflight can consume the accepted source bundle path,
`specpm.yaml`, referenced `specs/*.spec.yaml`, `producer-receipt.json`,
`validation-report.json`, `diagnostics.json`,
`producer-preflight-report.json`, static viewer artifact, accepted-source diff,
and proposal body `producerEvidenceLinks`.

These inputs are review evidence only.

## Stable Roles

`producerEvidenceLinks` should expose stable roles such as
`accepted_source_bundle`, `manifest`, `producer_receipt`,
`validation_report`, `diagnostics`, `producer_preflight`, `static_viewer`, and
`accepted_source_diff`.

SpecPM CI should not infer evidence semantics from prose or artifact names
alone.

## Expected Checks

A future gate may check required evidence presence, receipt identity, subject
package identity, output digests, validation and diagnostics report digests,
diagnostics status, privacy flags, `humanReview.requiredFor:
public_index_acceptance`, and complete proposal evidence links.

A pass is not acceptance. SpecPM still needs maintainer approval or an explicit
override recorded outside generated receipts.

## Source

The canonical GitHub-facing source is
`docs/SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md`.
