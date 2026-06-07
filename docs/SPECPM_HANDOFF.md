# SpecPM Handoff Guide

This guide explains how to hand a generated SpecHarvester candidate bundle to
SpecPM review without treating generated output as accepted registry truth.

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

The bundle is machine-verifiable evidence. `producer-receipt.json` records
producer identity, source inputs, configuration digest, output file hashes,
validation status, diagnostics status, privacy/security caveats, and human
review status. `validation-report.json` and `diagnostics.json` remain separate
artifacts so future tools can verify their hashes and inspect them without
trusting receipt prose.

## Operator Flow

1. Collect deterministic evidence from a pinned checkout:

   ```bash
   spec-harvester collect-local /path/to/repo \
     --repository https://github.com/example/project \
     --revision <commit-sha> \
     --out .specharvester/snapshots/project
   ```

2. Draft a candidate bundle:

   ```bash
   spec-harvester draft .specharvester/snapshots/project \
     --out .specharvester/candidates/example.project \
     --package-id example.project
   ```

3. Run producer-side handoff preflight:

   ```bash
   spec-harvester preflight-candidate-bundle \
     .specharvester/candidates/example.project
   ```

4. Render a static review site:

   ```bash
   spec-harvester render-spec-site \
     --candidate .specharvester/candidates/example.project \
     --output .specharvester/previews/example.project
   ```

5. Review the generated bundle before any SpecPM proposal:

   - inspect `producer-receipt.json` for producer identity, input provenance,
     configuration digest, `outputs[]` SHA-256 digests, validation references,
     diagnostics references, privacy notes, and `humanReview.status`;
   - inspect `validation-report.json` for validation status and error/warning
     counts;
   - inspect `diagnostics.json` for warnings, evidence gaps, unstable generated
     IDs, namespace/version overlap signals, privacy caveats, and security
     caveats;
   - inspect the static viewer for a human-readable summary of the same
     evidence;
   - decide whether the candidate should be accepted, rejected, corrected, or
     regenerated.

6. When using SpecPM proposal automation, verify that the generated pull
   request body links the same evidence:

   - accepted source bundle path in the SpecPM diff;
   - `specpm.yaml`;
   - `producer-receipt.json`;
   - `validation-report.json`;
   - `diagnostics.json`;
   - producer preflight report artifact or command output;
   - static viewer artifact, when available;
   - accepted-source diff in the pull request.

   The links are review evidence. They do not replace SpecPM validation or the
   maintainer acceptance decision.

   If SpecPM adds an optional CI preflight gate for producer bundles, it should
   consume the same evidence layout and stable roles described in
   [`SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md`](SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md).
   The CI result can support review, but acceptance still requires maintainer
   approval or an explicit override outside generated receipts.

  Registry acceptance decision records are described in
  [`SPECPM_REGISTRY_ACCEPTANCE_DECISION.md`](SPECPM_REGISTRY_ACCEPTANCE_DECISION.md).
  SpecHarvester handoff artifacts may reference the external record, but must
  not write maintainer approval into `producer-receipt.json`.

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

This package-set proposal is still review evidence. It does not accept
packages, accept relations, publish registry metadata, or replace SpecPM
maintainer review. See
[`PACKAGE_SET_HANDOFF_PROPOSAL.md`](PACKAGE_SET_HANDOFF_PROPOSAL.md).

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

## Validation Report Example

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

This report is producer-side evidence. It does not replace SpecPM validation.

## Diagnostics Example

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

Reject or regenerate the candidate when preflight or review finds:

- missing `specpm.yaml`, `specs/*.spec.yaml`, `producer-receipt.json`,
  `validation-report.json`, or `diagnostics.json`;
- unsupported receipt `apiVersion`, `kind`, `schemaVersion`, or
  `receiptProfile`;
- output hash mismatch;
- `producer-receipt.json` listed in `outputs[]`;
- validation or diagnostics report digest mismatch;
- missing source input evidence or bundle-local input path escapes;
- unstable generated IDs;
- generated claims without backing evidence;
- privacy-sensitive content, secrets, private prompts, or confidential raw
  source in public handoff artifacts;
- namespace or `packageId@version` overlap without explicit maintainer review.

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

## Package-Set AI Enrichment

After `draft-package-set` and `preflight-bundle-set`, operators may prepare
proposal-only semantic enrichment for generated package-set candidates:

```bash
spec-harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --provider-base-url http://127.0.0.1:1234 \
  --model openai/gpt-oss-20b \
  --request-output .smoke/xyflow-package-set/ai/requests.json \
  --output .smoke/xyflow-package-set/ai/ai-enrichment-proposals.json
```

The output is `SpecHarvesterPackageSetAIEnrichmentProposal` with
`apiVersion: spec-harvester.package-set-ai-enrichment/v0`. It records
`refinedSummary`, `capabilities`, `interfaces`, `evidencePaths`, confidence,
provider usage metadata, and diagnostics such as
`model_evidence_path_unsupported`.

The artifact is still review evidence. It does not mutate generated specs,
accept packages, accept relations, publish registry metadata, or replace
SpecPM maintainer review. See
[`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md).

## Shared Fixture Policy

When examples or tests are intended to demonstrate the SpecPM producer bundle
contract, keep them aligned through
[`SPECPM_SHARED_FIXTURE_POLICY.md`](SPECPM_SHARED_FIXTURE_POLICY.md). The
fixture policy requires exact SpecPM commit SHAs, generated fixture provenance,
and explicit drift handling instead of relying on mutable refs or silent
example updates.
