# GovernanceReports

A governance report to detect duplicate intent and capability claims.

Use this report for review planning when multiple candidates or accepted packages
share the same observed `intent.*` or capability claim IDs.

```shell
python3 -m spec_harvester governance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/governance-claims.json
```

## Detection Behavior

- Reported items include both `intent` and `provides.capabilities` IDs.
- Each duplicate entry lists all claimants with package ID, version, kind, and
  source path.
- Broad language-neutral semantic intents, including API contract, metadata
  schema validation, workflow automation, developer tooling, documentation
  knowledge base, and public repository metadata claims, remain in `records` but
  are not duplicate findings.
- Input roots are read recursively for `specpm.yaml`.
- Errors while reading malformed manifests are reported in `issues` and
  the report `status` is `partial`.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No analyzer execution.
- No candidate or accepted content mutation.

## Report Format

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterGovernanceDuplicateClaimReport`
- `status`
- `summary`
- `records`
- `duplicates.intent`
- `duplicates.capability`
- `issues`
- `trustBoundary`
