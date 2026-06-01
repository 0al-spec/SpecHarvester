# Producer Candidate Bundle

SpecHarvester produces reviewable SpecPM candidate packages. It must not imply
that generated candidates are accepted, published, trusted, or upstream
endorsed.

This page mirrors the GitHub-facing
`docs/PRODUCER_CANDIDATE_BUNDLE.md` contract and aligns SpecHarvester output
planning with the SpecPM Producer Candidate Bundle Contract documented in
SpecPM `ProducerReceipts`.

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

SpecHarvester implementation tasks should populate `subject`, `producer`,
`inputs`, `configuration`, `outputs`, `validation`, `diagnostics`,
`humanReview`, `privacy`, and `audit` with enough evidence for maintainers to
review candidate provenance.

## Output Digest Rules

Generated outputs listed in `outputs[]` should include `path`, `role`, and a
SHA-256 digest:

```yaml
path: specs/example.spec.yaml
role: boundary_spec
digest:
  algorithm: sha256
  value: <64 lowercase hex characters>
```

Expected output roles include `manifest`, `boundary_spec`,
`validation_report`, `diagnostics`, `evidence`, and `foreign_artifact`.

`producer-receipt.json` must not appear in `outputs[]`. Including the receipt
inside its own digest list creates a self-hash problem. Receipt byte
verification belongs in an external envelope, pull request artifact digest, or
review-system digest outside the receipt body.

## Validation And Diagnostics

`validation-report.json` should make validation status machine-readable.
`diagnostics.json` should summarize producer-side limitations and rejection
risks without embedding raw private source text, private prompts, tokens, or
credentials.

Future implementation should record validation status, validator identity,
warning and error counts, diagnostics status, privacy and security caveats,
unstable generated ID warnings, missing evidence links, namespace/version
overlap warnings, skipped files, unsupported languages, and model uncertainty.

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

Future SpecHarvester preflight should fail or block handoff when required files
are missing, `producer-receipt.json` is missing or malformed, receipt identity
fields are unsupported, subject metadata differs from candidate metadata, output
digests mismatch, `producer-receipt.json` appears in `outputs[]`,
`configuration.digest` is missing, validation or diagnostics files are missing
or mismatched, `diagnostics.status` is `failed`, generated IDs are unstable,
claims lack evidence references, `privacy.secretsIncluded` is `true`, private
data leaks into public artifacts, or `packageId@version` overlaps an accepted
namespace without maintainer review evidence.

## Implementation Sequence

This planning page is intentionally non-runtime. Follow-up P21 tasks should
emit `producer-receipt.json`, emit `validation-report.json` and
`diagnostics.json`, add local candidate bundle preflight verification, extend
the static candidate viewer, and add SpecPM handoff examples.
