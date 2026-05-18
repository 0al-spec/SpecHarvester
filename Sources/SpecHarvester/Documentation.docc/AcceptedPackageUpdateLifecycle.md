# Accepted Package Update Lifecycle

Accepted packages are reviewed SpecPM metadata snapshots.

In the current bootstrap, accepted package versions are immutable once published:

- do not mutate the accepted manifest package path for
  `<packageId>/<packageVersion>` in place,
- create a new package version for any upstream-driven change or metadata correction.

## Update Kinds

### Upstream-driven update

When a pinned upstream revision changes and affects candidate output, operators
should run the full candidate flow again and promote a candidate with a new package
version path.

### Metadata correction (errata)

When validation, inference, or documentation corrections are needed without an
upstream content change, operators should still create an explicit update proposal
for a new package version path.

## Required Audit Fields

For each update, capture:

- `sourceRevision`
- `evidenceDigests`
- `oldPackageVersion`, `newPackageVersion`
- `changedClaims`
- `validationStatus`
- `reviewerNotes`

## Trust Boundary

`promote` prepares local staging content.
Cross-repository proposal automation opens a SpecPM PR.
Registry publication remains bound to SpecPM review and merge.
