# Batch Validation Reports

Status: Bootstrap batch review artifact

Batch validation reports summarize `collect-batch` output for human review.
They record confidence, policy notes, warning codes, collected evidence counts,
and skipped records before any drafting or promotion step.

The report step does not clone repositories, call networks, install
dependencies, run package managers, run package scripts, execute repository
content, run public interface analyzers, draft SpecPM packages, or promote
candidates.

## Command

Write a report while collecting batch snapshots:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

The command still prints the batch summary to stdout. The `--report` path writes
a deterministic JSON review artifact.

## Report Contents

The report includes:

- `schemaVersion`
- `kind: SpecHarvesterBatchValidationReport`
- batch input and output root
- selected repository IDs
- summary counts for collected, skipped, confidence, and warnings
- collected records with evidence counts and policy notes
- skipped records with stable reasons
- trust-boundary statements

Each collected record includes:

- repository id and source URL
- `revision` or `ref`
- source manifest path and entry index
- output `harvest.json` path
- evidence counts
- `confidence`
- `confidenceReasons`
- `policyNotes`
- `warnings`

## Confidence

Confidence is advisory review metadata:

- `high`: snapshot policy matches safe static collection, files were collected,
  at least one package manifest was observed, and no warnings were emitted.
- `medium`: snapshot is usable but has review warnings, such as a source `ref`
  instead of a pinned `revision`, skipped files, or no package manifests.
- `low`: snapshot has a policy mismatch or no collected files.

Confidence does not accept or reject a package. It only helps prioritize human
review.

## Stable Warning Codes

Current warning codes:

- `collector_policy_mismatch`
- `source_ref_not_pinned_revision`
- `no_files_collected`
- `files_skipped`
- `no_package_manifests`

These codes are intended to be stable enough for later automation and reviewer
dashboards.

## Trust Boundary

Report generation only summarizes already prepared in-memory snapshots from
`collect-batch`.

It must not:

- clone or fetch repositories;
- install dependencies;
- run package managers;
- run package scripts;
- execute checkout files;
- run public interface analyzers;
- draft or promote SpecPM packages.
