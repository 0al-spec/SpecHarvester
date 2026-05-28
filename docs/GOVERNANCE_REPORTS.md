# Governance Duplicate Claim Reports

Status: Governance reporting

Duplicate claim reports summarize overlapping `intent.*` and capability
claims across package `specpm.yaml` files before acceptance. The report helps
reviewers detect conflicting or duplicate governance assertions in generated
candidates and accepted package metadata.

## Report Command

Build the report from one or more metadata roots:

```bash
python3 -m spec_harvester governance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/governance-claims.json
```

The command:

- scans every `specpm.yaml` under `--accepted-root` and `--candidates-root`;
- extracts package `metadata.id`, `metadata.version`, `index.intents`, and
  `index.provides.capabilities`;
- aggregates duplicate claim IDs and emits claimant provenance;
- treats broad language-neutral semantic intents such as API contracts,
  metadata schema validation, workflow automation, developer tooling,
  documentation knowledge bases, and public repository metadata as record-only
  signals rather than duplicate findings;
- returns deterministic JSON on stdout.

If `--output` is provided, the report is written as stable JSON to that path.

At least one of `--accepted-root` or `--candidates-root` must be provided.

## Report Structure

The report contains:

- `schemaVersion`
- `kind: SpecHarvesterGovernanceDuplicateClaimReport`
- `status`: `ok` or `partial` if malformed manifests were skipped;
- `summary` with counts (total records, duplicate counts, issue count);
- `records` for all parsed claims;
- `duplicates.intent` for overlapping comparable intent IDs;
- `duplicates.capability` for overlapping capabilities;
- `issues` when manifests could not be parsed; and
- `trustBoundary` advisory notes.

Broad language-neutral semantic intents remain visible in `records`. They are
not counted in `duplicates.intent` because they are valid evidence but weak
cross-package duplicate signals.

## Trust Boundary

The report command reads local `specpm.yaml` files only and performs no external
execution.

It does not:

- execute package scripts;
- install dependencies;
- run analyzers;
- clone repositories;
- write candidate or accepted package content.

## Example

```json
{
  "kind": "SpecHarvesterGovernanceDuplicateClaimReport",
  "summary": {
    "records": 12,
    "duplicateIntentCount": 2,
    "duplicateCapabilityCount": 1,
    "issueCount": 0
  }
}
```
