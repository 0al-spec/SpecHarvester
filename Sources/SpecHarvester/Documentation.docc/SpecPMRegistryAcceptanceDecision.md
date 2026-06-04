# SpecPM Registry Acceptance Decision Record

SpecHarvester may reference a future external SpecPM registry acceptance
decision record without writing maintainer decisions into generated producer
receipts.

## Boundary

The intended boundary is:

```text
SpecHarvester candidate evidence
        -> SpecPM CI and maintainer review
        -> external registry acceptance decision record
        -> public registry source merge
```

It is not:

```text
SpecHarvester receipt says approved -> package is accepted
```

`producer-receipt.json` can say human review is required for
`public_index_acceptance`, but it must not be the root of trust for approval.

## Decision Record

A SpecPM-owned decision record should use kind
`SpecPMRegistryAcceptanceDecision`, name the package ID, package version,
accepted source path, decision status, review authority, and producer evidence
reviewed by the maintainer.

Valid decision statuses include `pending`, `approved`, `rejected`, `override`,
and `withdrawn`.

## SpecHarvester Reference

SpecHarvester proposal artifacts may include:

```json
{
  "registryAcceptanceDecision": {
    "status": "external_required",
    "requiredFor": ["public_index_acceptance"],
    "authority": "SpecPM maintainer review",
    "recordKind": "SpecPMRegistryAcceptanceDecision",
    "producerReceiptAuthority": "evidence_only"
  }
}
```

This is a consumer hint, not approval.

## Human Review

Generated receipts should keep `humanReview.status` conservative, normally
`required` or `pending`. If a package is accepted, the external decision record
should point to the reviewed producer evidence. SpecHarvester should not edit a
generated receipt from `required` to `approved` after generation.

## Source

The canonical GitHub-facing source is
`docs/SPECPM_REGISTRY_ACCEPTANCE_DECISION.md`.
