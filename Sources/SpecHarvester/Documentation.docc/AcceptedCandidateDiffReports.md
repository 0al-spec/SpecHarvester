# AcceptedCandidateDiffReports

Accepted/candidate diff reports compare candidate `specpm.yaml` metadata against
the latest accepted package metadata for the same `metadata.id`.

```shell
python3 -m spec_harvester accepted-candidate-diff-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-diff.json
```

## Detection Behavior

- Input roots are read recursively for `specpm.yaml`.
- Candidates are matched to accepted packages by `metadata.id`.
- The accepted comparison point is the latest accepted version by SemVer ordering.
- Reported changes include package metadata, intents, capabilities, and upstream
  artifact references.
- Errors while reading malformed manifests are reported in `issues` and the
  report `status` is `partial`.

## Trust Boundary

- No SpecPM validation.
- No repository code execution.
- No package installation.
- No network calls.
- No analyzer execution.
- No candidate or accepted content mutation.

## Report Format

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterAcceptedCandidateDiffReport`
- `status`
- `summary`
- `comparisons`
- `issues`
- `trustBoundary`
