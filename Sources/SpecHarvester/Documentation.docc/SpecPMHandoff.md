# SpecPM Handoff

This page mirrors `docs/SPECPM_HANDOFF.md` and explains how to hand a generated
SpecHarvester candidate bundle to SpecPM review without treating generated
output as accepted registry truth.

SpecHarvester produces an evidence-rich candidate. SpecPM validates package
shape and registry policy. A maintainer approves acceptance. The public index
publishes only reviewed sources.

It is not:

```text
SpecHarvester generates package -> SpecPM accepts automatically
```

## Required Bundle

A generated candidate intended for public SpecPM review must contain:

```text
candidate/
  specpm.yaml
  specs/*.spec.yaml
  producer-receipt.json
  validation-report.json
  diagnostics.json
```

`producer-receipt.json` records producer identity, source inputs,
configuration digest, output file hashes, validation status, diagnostics
status, privacy/security caveats, and human review status. The separate
`validation-report.json` and `diagnostics.json` artifacts remain
machine-readable evidence for reviewers and future verification tools.

## Operator Flow

Collect deterministic evidence from a pinned checkout:

```bash
spec-harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out .specharvester/snapshots/project
```

Draft a candidate bundle:

```bash
spec-harvester draft .specharvester/snapshots/project \
  --out .specharvester/candidates/example.project \
  --package-id example.project
```

Run producer-side handoff preflight:

```bash
spec-harvester preflight-candidate-bundle \
  .specharvester/candidates/example.project
```

Render a static review site:

```bash
spec-harvester render-spec-site \
  --candidate .specharvester/candidates/example.project \
  --output .specharvester/previews/example.project
```

Review `producer-receipt.json`, `validation-report.json`, `diagnostics.json`,
and the static viewer before any SpecPM proposal. The reviewer decides whether
the candidate should be accepted, rejected, corrected, or regenerated.

When proposal automation opens a SpecPM pull request, the PR body should link
the same evidence: accepted source bundle path, `specpm.yaml`,
`producer-receipt.json`, `validation-report.json`, `diagnostics.json`,
producer preflight report artifact or command output, static viewer artifact
when available, and the accepted-source diff. These links are review evidence;
they do not replace SpecPM validation or maintainer acceptance.

If SpecPM adds an optional CI preflight gate for producer bundles, it should
consume the same evidence layout and stable roles described in
<doc:SpecPMCiPreflightGateSupport>. The CI result can support review, but
acceptance still requires maintainer approval or an explicit override outside
generated receipts.

Registry acceptance decision records are described in
<doc:SpecPMRegistryAcceptanceDecision>. SpecHarvester handoff artifacts may
reference the external record, but must not write maintainer approval into
`producer-receipt.json`.

## Package-Set Handoff

For generated package-set bundles, create a package-set handoff proposal before
any future SpecPM PR:

```bash
spec-harvester package-set-handoff-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --viewer .smoke/xyflow-package-set/viewer \
  --output .smoke/xyflow-package-set/handoff/proposal.json \
  --proposal-body .smoke/xyflow-package-set/handoff/proposal.md
```

The proposal links `package-set-draft.json`,
`package-relation-proposals.json`, `bundle-set-preflight.json`, package-set
viewer output, member candidate bundles, and relation summary evidence. It
uses `registryAcceptanceDecision.status: external_required` for both
`public_index_acceptance` and `package_relation_acceptance`.

This package-set proposal is review evidence. It does not accept packages,
accept relations, publish registry metadata, or replace SpecPM maintainer
review. See <doc:PackageSetHandoffProposal>.

## Receipt Example

```json
{
  "apiVersion": "specpm.receipts/v0",
  "kind": "SpecPMProducerReceipt",
  "schemaVersion": 1,
  "receiptProfile": "generated_spec_package_v0",
  "producer": {
    "name": "SpecHarvester",
    "version": "0.1.0"
  },
  "subject": {
    "packageId": "example.project",
    "packageVersion": "0.1.0",
    "boundarySpecs": ["specs/example_project.spec.yaml"]
  },
  "outputs": [
    {
      "path": "specpm.yaml",
      "role": "manifest",
      "digest": {
        "algorithm": "sha256",
        "value": "<64 lowercase hex characters>"
      }
    }
  ],
  "validation": {
    "status": "passed",
    "reportPath": "validation-report.json",
    "reportDigest": {
      "algorithm": "sha256",
      "value": "<64 lowercase hex characters>"
    }
  },
  "diagnostics": {
    "status": "clean",
    "path": "diagnostics.json",
    "digest": {
      "algorithm": "sha256",
      "value": "<64 lowercase hex characters>"
    }
  },
  "humanReview": {
    "status": "required",
    "requiredFor": ["public_index_acceptance"]
  }
}
```

`producer-receipt.json` must not appear in `outputs[]`; receipt self-hashing is
handled outside the receipt body.

## Report Examples

`validation-report.json` records producer-side shape evidence:

```json
{
  "kind": "SpecHarvesterProducerValidationReport",
  "schemaVersion": 1,
  "status": "valid",
  "summary": {
    "errorCount": 0,
    "warningCount": 0
  },
  "authority": "producer_side_shape_check"
}
```

`diagnostics.json` records privacy, security, and review caveats:

```json
{
  "kind": "SpecHarvesterProducerDiagnosticsReport",
  "schemaVersion": 1,
  "status": "clean",
  "entries": [],
  "privacy": {
    "privatePromptsIncluded": false,
    "rawSourceIncluded": false,
    "secretsIncluded": false
  },
  "security": {
    "caveat": "Generated diagnostics are review evidence only."
  },
  "review": {
    "acceptanceAuthority": "maintainer_review",
    "requiredFor": ["public_index_acceptance"]
  }
}
```

## Rejection Signals

Reject or regenerate the candidate when preflight or review finds missing
required bundle files, unsupported receipt identity fields, output hash
mismatch, `producer-receipt.json` in `outputs[]`, validation or diagnostics
digest mismatch, missing input evidence, bundle-local input path escapes,
unstable generated IDs, generated claims without evidence, privacy-sensitive
content, or namespace and `packageId@version` overlap without maintainer review.

## Acceptance Boundary

For public index handoff, `humanReview.status` should remain `required` or
`pending` until a maintainer reviews the candidate. Public index acceptance
requires `humanReview.status: approved` or an explicit maintainer override
recorded outside the generated bundle, normally in the accepted-source pull
request.

SpecHarvester evidence can support the decision. It cannot make the decision.

The external decision record is the handoff boundary for maintainer approval or
override. SpecHarvester proposal artifacts should use
`registryAcceptanceDecision.status: external_required` until SpecPM review
creates or records a `SpecPMRegistryAcceptanceDecision`.

## Shared Fixture Policy

When examples or tests demonstrate the SpecPM producer bundle contract, keep
them aligned through <doc:SpecPMSharedFixturePolicy>. The fixture policy
requires exact SpecPM commit SHAs, generated fixture provenance, and explicit
drift handling instead of relying on mutable refs or silent example updates.

Future optional SpecPM CI preflight support should consume the same evidence
layout and stable roles described in <doc:SpecPMCiPreflightGateSupport>.
