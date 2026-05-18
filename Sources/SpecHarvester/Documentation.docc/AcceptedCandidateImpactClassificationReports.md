# AcceptedCandidateImpactClassificationReports

Accepted/candidate impact classification reports convert accepted-vs-candidate diffs
into stable review buckets before update proposal work.

```shell
python3 -m spec_harvester accepted-candidate-impact-classification-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-impact-classification.json
```

## Detection Behavior

- Input roots are read recursively for `specpm.yaml`.
- Pairs are matched to the latest accepted package version by `metadata.id`.
- Each package comparison is classified into:
  - metadata
  - interface
  - license
  - provenance
  - capability
  - intent.
- Changes are emitted as structured buckets with `changed`, `added`, and `removed`
  details where applicable.

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
- `kind: SpecHarvesterAcceptedCandidateImpactClassificationReport`
- `status`
- `summary`
- `comparisons`
- `issues`
- `trustBoundary`
