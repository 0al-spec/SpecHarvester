# SpecPM Registry Acceptance Decision Record

Status: External decision handoff contract

This document defines how SpecHarvester handoff outputs may reference a future
external SpecPM registry acceptance decision record without writing maintainer
decisions into generated producer receipts.

SpecHarvester generates candidate bundle evidence. SpecPM validates registry
policy and maintainers decide acceptance. The acceptance decision is therefore
an external record owned by SpecPM review, not generated producer output.

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

`producer-receipt.json` may state that human review is required for
`public_index_acceptance`. It must not be the root of trust for approval.

## Decision Record Shape

A future SpecPM-owned decision record should be machine-readable:

```json
{
  "schemaVersion": 1,
  "kind": "SpecPMRegistryAcceptanceDecision",
  "decisionId": "example.package@0.1.0:registry-acceptance:<review-id>",
  "subject": {
    "packageId": "example.package",
    "packageVersion": "0.1.0",
    "acceptedSourcePath": "public-index/generated/example.package/0.1.0"
  },
  "decision": {
    "status": "approved",
    "authority": "maintainer_review",
    "requiredFor": ["public_index_acceptance"]
  },
  "evidence": {
    "specpmPullRequest": "https://github.com/0al-spec/SpecPM/pull/<number>",
    "producerEvidenceLinks": "pull-request-body",
    "producerReceipt": "public-index/generated/example.package/0.1.0/producer-receipt.json",
    "validationReport": "public-index/generated/example.package/0.1.0/validation-report.json",
    "diagnostics": "public-index/generated/example.package/0.1.0/diagnostics.json"
  },
  "review": {
    "reviewer": "<maintainer-login-or-team>",
    "reviewedAt": "<iso-8601-timestamp>",
    "notes": "Maintainer reviewed source provenance, evidence, namespace, and policy."
  }
}
```

Valid `decision.status` values are:

- `pending`: review is open and no acceptance decision exists yet;
- `approved`: maintainer approved public index acceptance;
- `rejected`: maintainer rejected public index acceptance;
- `override`: maintainer explicitly overrode a producer or CI warning;
- `withdrawn`: proposal was closed or withdrawn before acceptance.

Only SpecPM review or an explicitly trusted SpecPM-side workflow should create
or finalize this record.

## SpecHarvester Handoff Reference

SpecHarvester proposal artifacts may include a pending reference:

```json
{
  "registryAcceptanceDecision": {
    "status": "external_required",
    "requiredFor": ["public_index_acceptance"],
    "authority": "SpecPM maintainer review",
    "recordKind": "SpecPMRegistryAcceptanceDecision",
    "recordLocation": "SpecPM pull request or accepted-source review record",
    "producerReceiptAuthority": "evidence_only"
  }
}
```

This reference is a consumer hint. It is not approval, and it does not mutate
the generated bundle.

## Relationship To Human Review

Generated receipts should keep public handoff review state conservative:

```json
{
  "humanReview": {
    "status": "required",
    "requiredFor": ["public_index_acceptance"]
  }
}
```

If a package is accepted, the acceptance record should point to the reviewed
producer evidence. The producer receipt should not be edited from `required` to
`approved` by SpecHarvester after generation.

## Expected Consumer Behavior

A future SpecPM CI or review tool may:

- verify that a proposal requiring public index acceptance has
  `registryAcceptanceDecision.status: external_required`;
- verify that the decision record, when present, references the same package ID,
  package version, and accepted source path;
- reject `approved` status inside producer-generated artifacts unless it is
  backed by an external SpecPM decision record;
- display pending, approved, rejected, override, or withdrawn state in review
  tooling;
- keep public registry publication gated on SpecPM merge policy, not on
  SpecHarvester output.

## Non-Goals

This contract does not:

- implement SpecPM-side approval storage;
- define who may approve in SpecPM;
- create signatures, attestations, transparency log entries, or revocation
  policy;
- let SpecHarvester approve public registry acceptance;
- modify generated producer receipts after review;
- publish packages.

Those are SpecPM governance tasks.
