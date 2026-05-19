# Accepted Package Update Lifecycle

Status: Bootstrap policy

Accepted packages are reviewed artifacts in the SpecPM public-index flow. In the
current bootstrap, accepted package versions are immutable once published:

- an accepted manifest package path for `<packageId>/<packageVersion>` is treated
  as immutable registry evidence;
- operators should not mutate that path in place;
- a new accepted package version should be introduced for any update that changes
  accepted package source content or accepted metadata.
- Same-version mutations are blocked unless the update is explicitly emitted as a
  correction with rationale.

## Why immutability

Immutability protects reproducibility and review traceability. Reviewers and
automation can then verify:

- what upstream source revision was used;
- which evidence artifacts were present;
- which claims changed;
- what passed validation gates;
- what reviewer approved the change and why.

## Update Triggers and Required Paths

### 1) Upstream changes

When the upstream source revision used by a package changes in a way that affects
generated package metadata or claims, treat this as a new candidate and a new
accepted version.

Required behavior:

- collect or draft from a pinned revision;
- generate a reviewed candidate for that revision;
- produce a new accepted source version path (for example
  `.../<packageId>/<newVersion>`);
- keep the previous version path unchanged.

### 2) Metadata corrections and errata

When corrections are required without upstream content changes (for example
typo fixes in comments, evidence interpretation, or deterministic drafting
improvements), keep source revision and evidence provenance explicit, but still
do not rewrite the previous accepted version path.

Required behavior:

- create a new candidate from the same or updated evidence set as appropriate;
- generate a new accepted version for the correction path;
- update accepted sources only through the normal acceptance gate.
- use `accepted-package-update-proposal` with:
  - `--allow-correction`
  - one or more `--correction-note` entries.

The boundary is that a metadata correction is still a revision event for the
accepted registry snapshot and must not be silently applied to an existing
version path.

For correction events, proposal artifacts include `updateKind: correction` and an
explicit `correction` block with `enabled`, `source: manual_review`, and
`reason` details.

## Required Audit Trail Fields

For each accepted update proposal, collect at least these fields:

- `sourceRevision` — pinned upstream SHA (or equivalent source revision marker)
- `evidenceDigests` — digests for principal artifacts, at minimum `harvest.json`
  and any promoted evidence attachments
- `oldPackageVersion` / `newPackageVersion`
- `changedClaims` — list of materially changed `intent.*` / capability / scope
  fields
- `validationStatus` — specpm/spec-harvester validation outcomes
- `reviewerNotes` — structured rationale and risk assessment

Suggested shape:

The example below uses `upstream_revision`; use `metadata_errata` for correction
proposals that do not represent upstream content changes.

```json
{
  "packageId": "xyflow.core",
  "updateKind": "upstream_revision",
  "sourceRevision": "0123456789abcdef",
  "evidenceDigests": {
    "harvestJson": "sha256:...",
    "specpmYaml": "sha256:..."
  },
  "oldPackageVersion": "0.1.0",
  "newPackageVersion": "0.2.0",
  "changedClaims": [
    "provides.capabilities.ui",
    "intent.ui.graph_editor"
  ],
  "validationStatus": {
    "specpm": "warning_only",
    "smokeTriage": "attention_required"
  },
  "reviewerNotes": [
    "Upstream commit added new public-facing symbol exports."
  ]
}
```

## Acceptance Boundary

The update lifecycle is bounded by SpecPM review and merge:

- `promote` can only prepare the local accepted-source staging diff;
- proposal automation can open a cross-repository PR against `0al-spec/SpecPM`;
- a package becomes registry input only after SpecPM review and merge.

This avoids bypassing maintainers when content or metadata changes.

## Operational Checklist

- decide if the change is upstream-driven or metadata correction;
- create a fresh candidate context with pinned revision and reviewable command output;
- compare accepted and candidate metadata with `accepted-candidate-diff-report`;
- build the proposal artifact with `accepted-package-update-proposal`;
- include the audit fields above in the change record or PR body;
- submit through SpecPM proposal path, not direct registry mutation.
