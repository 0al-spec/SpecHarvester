# Accepted/Candidate Diff Reports

Status: Update lifecycle reporting

Accepted/candidate diff reports compare candidate `specpm.yaml` metadata against
the latest accepted package metadata for the same `metadata.id`.

The report is intended for update review. It helps reviewers see whether a
candidate is new, unchanged, or materially different before later tooling
classifies impact or prepares a SpecPM update proposal.

## Report Command

Build the report from accepted and candidate roots:

```bash
python3 -m spec_harvester accepted-candidate-diff-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-diff.json
```

The command:

- scans every `specpm.yaml` under both roots;
- matches candidates to accepted package records by `metadata.id`;
- compares against the latest accepted version by SemVer ordering;
- reports changed package metadata, `intent.*` claims, capability claims, and
  upstream artifact references;
- emits deterministic JSON on stdout.

If `--output` is provided, the report is written as stable JSON to that path.

## Report Structure

The report contains:

- `schemaVersion`
- `kind: SpecHarvesterAcceptedCandidateDiffReport`
- `status`: `ok` or `partial` if malformed manifests were skipped;
- `summary` with accepted/candidate/comparison counts;
- `comparisons` for every parsed candidate package;
- `issues` for skipped manifests; and
- `trustBoundary` advisory notes.

Each comparison has one of these statuses:

- `new_package`: candidate package ID is not present in accepted metadata;
- `unchanged`: candidate matches the latest accepted metadata for compared fields;
- `changed`: candidate differs from the latest accepted metadata.

Impact classification is intentionally separate and belongs to later update
lifecycle tooling.

## Trust Boundary

The report command reads local `specpm.yaml` files only and performs no external
execution.

It does not:

- run SpecPM validation;
- execute package scripts;
- install dependencies;
- run analyzers;
- clone repositories;
- write candidate or accepted package content.
