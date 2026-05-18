# ``AcceptedPackageUpdateProposals``

`accepted-package-update-proposal` builds a PR-ready artifact for a reviewed
candidate when updating an accepted package version.

The command is used after a reviewable candidate has been compared to the current
accepted version and before cross-repository proposal operations.

## Summary

- Generates a deterministic JSON payload with comparison summary and validation state.
- Detects changed claims from `intent` and `capability` deltas.
- Includes evidence digests from `specpm.yaml` and optional `harvest.json`.
- Optionally renders a deterministic markdown body for operator review.
- Does not mutate candidate or accepted directories.

## Command

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  --accepted-root accepted \
  CANDIDATE_DIR
```

Required:

- `CANDIDATE_DIR` as the reviewed candidate directory.
- `--accepted-root` for latest accepted comparison.

Optional:

- `--output` for JSON proposal file.
- `--proposal-body` for markdown proposal body.
- `--skip-validation` for offline runs.
- `--update-kind` override (`upstream_revision`, `metadata_errata`, `correction`).
- `--reviewer-notes` repeatable.

## Output

The payload includes:

- `packageId`, `packageSubdir`, `manifestEntryPath`
- `oldPackageVersion`, `newPackageVersion`
- `updateKind`, `sourceRevision`
- `evidenceDigests` map
- `changedClaims` list
- `validationStatus`
- `reviewerNotes`
- `comparison`, `candidate`, `accepted`, `issues`, `trustBoundary`

`--skip-validation` is explicit and should be used only for CI smoke fixtures or
operator-specific deterministic flows.

## References

- <doc:AcceptedCandidateDiffReports>
- <doc:AcceptedCandidateImpactClassificationReports>
- <doc:AcceptedPackageUpdateLifecycle>
- <doc:ProposalAutomation>
