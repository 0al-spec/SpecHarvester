# License and Provenance Risk Reports

Status: Governance review

License and provenance risk reports summarize candidate and accepted package
metadata for reviewers before proposal and promotion.

## Report Command

Build the report from one or more metadata roots:

```bash
python3 -m spec_harvester governance-license-provenance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/license-provenance-risk.json
```

The command:

- scans every `specpm.yaml` under both roots;
- extracts `metadata.id`, `metadata.version`, `metadata.license`, and
  `foreignArtifacts` upstream declarations;
- flags license and provenance risk signals;
- returns deterministic JSON on stdout.

At least one of `--accepted-root` or `--candidates-root` must be provided.

## Report Structure

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterLicenseProvenanceRiskReport`
- `status`: `ok` or `partial` when issues were found
- `summary` with counts and issue buckets:
  - `records`
  - `riskScore`
  - `issueCount`
  - `riskCounts` (high/medium/low)
  - `issuesByCode`
- `records` with package and upstream artifact context;
- `issues` list of review risk codes with severities; and
- `trustBoundary` advisory notes.

## Current Warnings / Checks

- `missing_license`: package metadata has no `license` field.
- `unknown_license`: license uses placeholder values (`unknown`, `n/a`, etc.).
- `non_standard_license`: license is not recognized as a common SPDX-like identifier.
- `missing_upstream_repository`: no `id: upstream_repository` in `foreignArtifacts`.
- `duplicate_upstream_repository_entries`: more than one upstream artifact present.
- `invalid_upstream_repository_uri`: upstream URI is malformed.
- `upstream_namespace_mismatch`: namespace does not match inferred upstream owner.
- `non_github_upstream_repository`: upstream URI is not a GitHub source.

## Trust Boundary

- no repository code execution;
- no package installation;
- no network calls;
- no analyzer execution;
- no mutation of candidate or accepted content.

