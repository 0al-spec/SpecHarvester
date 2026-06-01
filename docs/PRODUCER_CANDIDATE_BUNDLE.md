# Producer Candidate Bundle Output Plan

SpecHarvester produces reviewable SpecPM candidate packages. It must not imply
that generated candidates are accepted, published, trusted, or upstream
endorsed.

This document aligns SpecHarvester output planning with the SpecPM Producer
Candidate Bundle Contract documented in the adjacent SpecPM repository under
`specs/PRODUCER_RECEIPTS.md` and DocC `ProducerReceipts`.

## Boundary

The candidate bundle is a machine-verifiable handoff:

```text
SpecHarvester generates evidence-rich candidate
        -> SpecPM validates package shape
        -> maintainer reviews acceptance
        -> public index publishes only reviewed sources
```

It is not:

```text
SpecHarvester generates candidate -> SpecPM accepts automatically
```

Producer receipts are evidence, not authority. SpecPM may validate package
shape, hashes, and receipt fields, but public index acceptance still requires
`humanReview.status: approved` or an explicit maintainer override recorded
outside the generated bundle, normally in the accepted-manifest pull request.

## Minimum Bundle Layout

Generated candidates intended for SpecPM review should use this layout:

```text
candidate/
  specpm.yaml
  specs/*.spec.yaml
  producer-receipt.json
  validation-report.json
  diagnostics.json
```

The files have distinct roles:

- `specpm.yaml`: generated package manifest candidate.
- `specs/*.spec.yaml`: generated BoundarySpec candidates.
- `producer-receipt.json`: machine-readable producer handoff receipt.
- `validation-report.json`: machine-readable validation result from producer or
  handoff validation.
- `diagnostics.json`: compact warnings, errors, policy notes, privacy notes,
  unstable-ID warnings, evidence gaps, and overlap diagnostics.

## Receipt Profile

`producer-receipt.json` should follow the SpecPM
`generated_spec_package_v0` profile:

```yaml
apiVersion: specpm.receipts/v0
kind: SpecPMProducerReceipt
schemaVersion: 1
receiptProfile: generated_spec_package_v0
receiptId: example.package@0.1.0:producer:sha256:<digest-prefix>
issuedAt: "2026-06-02T00:00:00Z"
subject: {}
producer: {}
inputs: []
configuration: {}
outputs: []
validation: {}
diagnostics: []
humanReview: {}
privacy: {}
audit: {}
```

SpecHarvester implementation tasks should populate:

- `subject.packageId`, `subject.packageVersion`,
  `subject.packageApiVersion`, and `subject.packageRoot`.
- `producer.name`, `producer.version`, and exact source `producer.revision`
  when available.
- `inputs[]` for source snapshots, harvested evidence, public interface indexes,
  analyzer outputs, templates, prompts, configuration, and previous specs when
  those inputs affected generated output.
- `configuration.digest` for the normalized generation configuration or stable
  configuration summary.
- `outputs[]` for generated files and SHA-256 digests.
- `validation.status`, validation report path, and validation report digest.
- `diagnostics.status`, diagnostics path, diagnostics digest, and compact
  diagnostic entries.
- `humanReview.status` and `humanReview.requiredFor:
  public_index_acceptance`.
- `privacy.secretsIncluded: false` for public handoff receipts.
- `audit.evidence[]` references that let reviewers explain why output changed.

## Output Digest Rules

Every generated output listed in `outputs[]` should include:

```yaml
path: specs/example.spec.yaml
role: boundary_spec
digest:
  algorithm: sha256
  value: <64 lowercase hex characters>
```

Expected output roles include:

- `manifest`
- `boundary_spec`
- `validation_report`
- `diagnostics`
- `evidence`
- `foreign_artifact`

`producer-receipt.json` must not appear in `outputs[]`. Including the receipt
inside its own digest list creates a self-hash problem. Receipt byte
verification belongs in an external envelope, pull request artifact digest, or
review-system digest outside the receipt body.

## Validation And Diagnostics

`validation-report.json` should make validation status machine-readable. Future
implementation should record at least:

- validation status: `not_run`, `valid`, `warning`, or `invalid`;
- validator identity and version when validation ran;
- validation timestamp;
- warning and error counts;
- digest of the validation report when referenced by the receipt.

`diagnostics.json` should summarize producer-side limitations and rejection
risks without embedding raw private source text, private prompts, tokens, or
credentials. Future implementation should record at least:

- diagnostics status: `clean`, `warnings`, or `failed`;
- compact diagnostic entries with `severity`, `code`, and `message`;
- privacy and security caveats;
- unstable generated ID warnings;
- missing or weak evidence links;
- namespace and version overlap warnings;
- skipped files, unsupported languages, or model uncertainty.

## Review Boundary

Generated candidate bundles are review inputs. They do not publish anything.

For public SpecPM index handoff:

- pre-review generated bundles should normally use `humanReview.status:
  required` or `pending`;
- accepted handoff requires `humanReview.status: approved` or explicit
  maintainer override recorded outside the generated bundle;
- `humanReview.status: not_applicable` is only appropriate for local/private
  workflows that do not request public index acceptance.

## Preflight Rejection Diagnostics

Future SpecHarvester preflight should fail or block handoff when:

- required bundle files are missing;
- `producer-receipt.json` is missing or malformed;
- receipt `apiVersion`, `kind`, `schemaVersion`, or `receiptProfile` is
  unsupported;
- subject package ID, version, API version, or package root differ from the
  generated candidate metadata;
- an `outputs[]` digest does not match generated bytes;
- `producer-receipt.json` appears in `outputs[]`;
- `configuration.digest` is missing;
- validation status references a missing or mismatched
  `validation-report.json`;
- diagnostics status references a missing or mismatched `diagnostics.json`;
- `diagnostics.status` is `failed`;
- generated IDs are unstable or invalid;
- generated claims lack evidence references;
- `privacy.secretsIncluded` is `true` for public handoff;
- private prompts, raw confidential source text, tokens, credentials, or local
  machine paths leak into public handoff artifacts;
- generated `packageId@version` overlaps an accepted namespace or version
  without maintainer review evidence.

## Implementation Sequence

This planning document is intentionally non-runtime. Follow-up P21 tasks should
land in order:

1. Emit `producer-receipt.json` using the `generated_spec_package_v0` profile.
2. Emit `validation-report.json` and `diagnostics.json`.
3. Add local candidate bundle preflight verification.
4. Extend the static candidate viewer with receipt, provenance, validation,
   diagnostics, privacy, and review-boundary panels.
5. Add SpecPM handoff examples and operator documentation.
