# LicenseProvenanceRiskReports

A review report for package license and upstream provenance signals.

Use this report during manual review when candidates should be prioritized by
license and supply-chain risk signals.

```shell
python3 -m spec_harvester governance-license-provenance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/license-provenance-risk.json
```

## Detection Behavior

- Reads package `metadata.id`, `metadata.version`, `metadata.license`.
- Reads `foreignArtifacts` and focuses on `id: upstream_repository` records.
- Emits risk issues for missing or unknown license metadata.
- Emits risk issues for invalid, missing, or out-of-policy upstream provenance.
- Produces deterministic JSON with package provenance context and issue severity.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No analyzer execution.
- No mutation of candidate or accepted content.

## Report Format

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterLicenseProvenanceRiskReport`
- `status`
- `summary`
- `records`
- `issues`
- `trustBoundary`
