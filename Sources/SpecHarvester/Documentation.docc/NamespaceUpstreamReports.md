# NamespaceUpstreamReports

A review report for package namespace and upstream relationship metadata.

Use this report during manual review when candidates must be checked against
accepted metadata.

```shell
python3 -m spec_harvester governance-upstream-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/namespace-upstream.json
```

## Detection Behavior

- Reads package `metadata.id` and `metadata.version` to derive namespace.
- Reads `foreignArtifacts` records and focuses on `id: upstream_repository`.
- Emits duplicate namespace groups across scanned packages.
- Emits issues for:
  - missing upstream relationships;
  - duplicate upstream relationship artifacts;
  - invalid upstream URI parsing;
  - namespace owner mismatch against parsed upstream URI owner.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No analyzer execution.
- No mutation of candidate or accepted content.

## Report Format

- `schemaVersion`
- `kind: SpecHarvesterNamespaceUpstreamReviewReport`
- `status`
- `summary`
- `records`
- `duplicates.namespace`
- `issues`
- `trustBoundary`
