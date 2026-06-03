# SpecPM CI Preflight Gate Support

Status: Producer-side consumer contract

This document defines the SpecHarvester side of a future optional SpecPM CI
preflight gate for producer candidate bundles.

SpecHarvester produces candidate bundle evidence. SpecPM may later consume that
evidence in CI to make review faster and safer. The gate must remain advisory
or policy-driven on the SpecPM side; it must not turn producer evidence into
registry authority.

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

SpecHarvester owns the producer evidence shape. SpecPM owns the CI policy,
registry intake checks, accepted-source diff validation, and maintainer
acceptance decision.

## Gate Inputs

A future SpecPM CI preflight can expect proposal evidence from the trusted
SpecHarvester proposal workflow:

- accepted source bundle path in the SpecPM pull request diff;
- `specpm.yaml`;
- referenced `specs/*.spec.yaml`;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- `producer-preflight-report.json`;
- static viewer artifact when available;
- accepted-source diff in the pull request;
- proposal body `producerEvidenceLinks`.

These inputs are review evidence. They are not signatures, attestations, or
maintainer approvals.

## Stable Evidence Roles

`producerEvidenceLinks` should continue to use stable machine-readable roles so
SpecPM CI does not need to infer meaning from prose:

```json
[
  {
    "role": "accepted_source_bundle",
    "path": "public-index/generated/example.package/0.1.0"
  },
  {
    "role": "manifest",
    "path": "public-index/generated/example.package/0.1.0/specpm.yaml"
  },
  {
    "role": "producer_receipt",
    "path": "public-index/generated/example.package/0.1.0/producer-receipt.json"
  },
  {
    "role": "validation_report",
    "path": "public-index/generated/example.package/0.1.0/validation-report.json"
  },
  {
    "role": "diagnostics",
    "path": "public-index/generated/example.package/0.1.0/diagnostics.json"
  },
  {
    "role": "producer_preflight",
    "artifact": "specpm-proposal-evidence-example.package-0.1.0"
  },
  {
    "role": "static_viewer",
    "artifact": "specpm-proposal-evidence-example.package-0.1.0"
  },
  {
    "role": "accepted_source_diff",
    "url": "https://github.com/0al-spec/SpecPM/pull/<number>/files"
  }
]
```

If a role is renamed or removed, update the SpecPM intake policy and
SpecHarvester proposal automation in the same reviewed change sequence.

## Expected SpecPM CI Checks

A future SpecPM CI gate may check:

- all required evidence paths or artifacts are present;
- `producer-receipt.json` uses a supported `apiVersion`, `kind`,
  `schemaVersion`, and `receiptProfile`;
- receipt `subject.packageId` and `subject.packageVersion` match the accepted
  source path and package manifest;
- receipt `outputs[]` digests match generated files and do not include
  `producer-receipt.json`;
- `validation.reportPath` and `diagnostics.path` point to the expected reports;
- validation and diagnostics digests match report bytes;
- diagnostics status is not `failed`;
- privacy flags do not indicate public handoff leaks;
- `humanReview.requiredFor` includes `public_index_acceptance`;
- `humanReview.status` is not treated as acceptance unless SpecPM has an
  external maintainer approval or override record;
- proposal body `producerEvidenceLinks` include the stable roles listed above.

The gate should report precise rejection diagnostics, but the producer-side
contract does not require SpecPM to publish or accept anything after a pass.

## Workflow Contract

The trusted SpecHarvester proposal workflow should preserve these properties:

- run only from trusted contexts before using cross-repository write
  credentials;
- validate the candidate with SpecPM before promotion;
- run `preflight-candidate-bundle` and store
  `producer-preflight-report.json`;
- run `render-spec-site` and upload static viewer evidence;
- promote into the expected accepted-source path only;
- generate the SpecPM public index as a smoke check;
- reject unexpected SpecPM diff paths before pull request creation;
- include evidence links in the SpecPM pull request body.

Manual dry runs should exercise the same evidence creation and diff preflight
steps without pushing a branch or creating a pull request.

## Shared Fixture Alignment

This gate support depends on the shared fixture policy in
[`SPECPM_SHARED_FIXTURE_POLICY.md`](SPECPM_SHARED_FIXTURE_POLICY.md). Any
fixture claiming to represent SpecPM CI preflight inputs should name:

- exact SpecPM contract commit SHA;
- SpecHarvester generator commit SHA;
- fixture profile, such as `generated_spec_package_v0`;
- generated bundle path;
- producer evidence artifact name;
- evidence roles covered by the fixture.

Exact commit SHAs are the root of trust. Mutable refs are labels only.

## Non-Goals

This support contract does not:

- implement the SpecPM CI gate;
- make SpecPM execute SpecHarvester in ordinary public-index CI;
- make producer evidence accepted registry truth;
- replace maintainer review;
- require live network access for ordinary SpecHarvester tests;
- introduce signing, transparency logs, or external attestations.

Those may be separate future tasks after both repositories agree on the stable
fixture and intake policy.
