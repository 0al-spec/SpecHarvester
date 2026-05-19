# Accepted Package Update Proposals

Status: Bootstrap workflow support

`accepted-package-update-proposal` builds a PR-ready artifact for a reviewed
candidate when creating a new accepted package version.

Use this command after running:

- `accepted-candidate-diff-report`
- `accepted-candidate-impact-classification-report`
- `prepare-accepted-entry` (optional) and `promote`

to convert an updated candidate into a review artifact for accepted package version
updates.

## Command

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  candidates/github.com/example/project \
  --accepted-root accepted \
  --output report/accepted-package-update-proposal.json \
  --proposal-body report/accepted-package-update-proposal.md \
  [--skip-validation] \
  [--update-kind upstream_revision|metadata_errata|correction] \
  [--allow-correction] \
  [--correction-note "metadata typo fix"] \
  [--reviewer-notes "upstream revision changed"]
```

Required input:

- `candidate` positional argument: reviewed candidate directory.
- `--accepted-root` path to staging accepted package root used for the latest
  version comparison.

Output:

- `--output` path: writes the JSON proposal payload.
- `--proposal-body` path: writes a deterministic Markdown body.

If no output options are given, payload is printed to stdout as JSON.

## Proposal Shape

Required fields:

- `schemaVersion`: current proposal schema version.
- `kind: SpecHarvesterAcceptedPackageUpdateProposal`.
- `status`: `ok` if no validation/issues, else `partial`.
- `packageId`, `packageSubdir`, `manifestEntryPath`.
- `oldPackageVersion` and `newPackageVersion` from comparison.
- `updateKind`: `upstream_revision`, `metadata_errata`, or `correction`.
- `sourceRevision`: upstream repository revision from `specpm.yaml` `foreignArtifacts`.
- `evidenceDigests` for `harvestJson` (when present) and `specpmYaml`.
- `changedClaims` list of added/removed `intent:` and `capability:` claims.
- `validationStatus` from SpecPM validation.
- `reviewerNotes`: optional list of human-supplied notes.
- `comparison` for changed capabilities/intents.
- `candidate` and `accepted` reference objects.
- `issues`: validation and parsing issues collected during report generation.
- `trustBoundary` notes.
- `correction` block with manual correction evidence when correction mode is enabled.

`validationStatus` is at least:

- `{"specpm": "ok"}` when validation passes.
- `{"specpm": "skipped"}` when `--skip-validation` is used.
- `{"specpm": "failed", "error": "<details>"}` on validation failure.

`updateKind` inference:

- `upstream_revision` by default for new candidates or changed upstream revision
  when the package version is also new.
- `metadata_errata` for unchanged source revision (when revision is extractable).
- `correction` as an explicit manual override only.

For any proposal that targets an already accepted `packageId@version`, the
command requires `--allow-correction` and at least one `--correction-note`:

- `updateKind` is `correction`.
- `comparison.status` is `correction`.
- `correction` block is included with:
  - `enabled: true`
  - `source: manual_review`
  - `reason: [...]`.

## Trust Boundary

The command is advisory/read-only:

- Reads local `specpm.yaml` from `candidate` and `accepted-root`.
- Reads optional `harvest.json` only for digesting evidence.
- Optionally runs `specpm validate` when not skipped.
- Does not write candidate or accepted package directories.

It is intended to produce a deterministic artifact for later trusted review and
SpecPM proposal operations.
