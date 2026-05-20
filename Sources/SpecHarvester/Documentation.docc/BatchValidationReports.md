# Batch Validation Reports

Batch validation reports summarize `collect-batch` output for human review.
They record confidence, policy notes, stable error/warning codes, evidence
counts, and skipped records before drafting or promotion.

The report step does not clone repositories, call networks, install
dependencies, run package managers, run package scripts, execute repository
content, run public interface analyzers, draft SpecPM packages, or promote
candidates.

## Command

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

The command still prints the batch summary to stdout and writes a deterministic
JSON review artifact at the report path.

`collect-batch` defaults to `strict_public` mode for public SpecPM.dev intake.
In this mode staged git changes fail preflight, and missing allowlisted
license-like evidence is reported as `missing_license_file` with
`status: error`. Allowlisted root filenames include `LICENSE`, `LICENSE.txt`,
`LICENSE.md`, `COPYING`, `COPYING.txt`, and `COPYING.md`. Use
`--relaxed-private` for private-code spec coverage.
When a generated report has `status: error`, `collect-batch` exits non-zero.

## Confidence

- `high`: safe static collection policy matches, files were collected, at least
  one package manifest was observed, and no warnings were emitted.
- `medium`: the snapshot is usable but has review warnings, such as a source
  `ref`, skipped files, or no package manifests.
- `low`: the snapshot has a strict public error, policy mismatch, or no collected files.

Confidence is advisory review metadata. It does not accept or reject a package.

## Error Codes

- `missing_license_file`

## Warning Codes

- `collector_policy_mismatch`
- `source_ref_not_pinned_revision`
- `no_files_collected`
- `files_skipped`
- `no_package_manifests`

## References

- `docs/BATCH_VALIDATION_REPORTS.md`
- <doc:BatchCollection>
- <doc:Workflow>
- <doc:TrustBoundary>
