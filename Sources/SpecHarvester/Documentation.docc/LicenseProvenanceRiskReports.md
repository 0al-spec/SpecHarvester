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

- Reads package `metadata.id`, `metadata.version`, `metadata.license`, and
  `metadata.licenseEvidence`.
- Reads `foreignArtifacts` and focuses on `id: upstream_repository` records.
- Emits distinct risk issues for absent license evidence, collected standard
  license-file evidence, and ambiguous unclassified license-like evidence.
- Emits risk issues for invalid, missing, or out-of-policy upstream provenance.
- Produces deterministic JSON with package provenance context and issue severity.

## License Evidence

Generated candidates can include `metadata.licenseEvidence`:

- `manifest`: package manifest provided the license string.
- `license_file_hint`: an allowlisted license file produced a known static hint.
- `ambiguous_license_file`: a license-like file existed but was not classifiable.
- `absent`: no manifest license or license-like file evidence was found.

When `metadata.license` is still `UNKNOWN`, standard collected license
filenames such as `LICENSE`, `LICENSE.txt`, `LICENSE.md`, `COPYING`, and
`COPYING.rst` produce `collected_unknown_license_evidence`.  This remains a
review advisory, but it is lower severity than `ambiguous_unknown_license`
because deterministic collection found an allowlisted public license file.

Issue classes include:

- `absent_license_evidence`
- `ambiguous_unknown_license`
- `collected_unknown_license_evidence`

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
