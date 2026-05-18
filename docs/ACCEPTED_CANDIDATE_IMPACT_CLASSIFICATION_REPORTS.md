# Accepted/Candidate Impact Classification Reports

Status: Bootstrap governance triage

Accepted/candidate impact classification reports convert diff output into fixed buckets
for review prioritization before accepted-package update proposals.

## Report Command

Build the report from accepted and candidate roots:

```bash
python3 -m spec_harvester accepted-candidate-impact-classification-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-impact-classification.json
```

The command:

- reuses the deterministic accepted-vs-candidate comparison output;
- separates metadata, interface, license, provenance, capability, and intent impact;
- preserves new/unchanged/changed package statuses;
- includes candidate claims that changed and a deterministic summary; and
- writes stable JSON to stdout or `--output`.

## Report Structure

The report contains:

- `schemaVersion`
- `kind: SpecHarvesterAcceptedCandidateImpactClassificationReport`
- `status`: `ok` or `partial` if malformed manifests were skipped;
- `summary` with record counts by status and impact bucket;
- `comparisons`, one entry per candidate package; and
- `issues` for skipped manifests.

Each comparison has:

- `packageId`, old/new package versions, and status;
- candidate and accepted path/version provenance;
- `impact` buckets: `metadata`, `interface`, `license`, `provenance`,
  `capability`, and `intent`;
- `changedClaims` for changed capability/intent/interface claim IDs.

`interface` uses claim IDs with stable prefixes:

- `capability:<claim>`
- `intent:<claim>`

## Trust Boundary

- reads local `specpm.yaml` files only;
- no SpecPM validation;
- no analyzer execution;
- no package installation;
- no dependency installation;
- no network access; and
- no candidate or accepted package mutation.

## Contract Notes

- `metadata.items` contains sorted changed metadata keys.
- `license.items` contains changed metadata keys whose names indicate licensing
  (`license*` fields).
- `provenance` returns full removed/added artifact objects with stable ordering.
