# Accepted Package Update Proposals

`accepted-package-update-proposal` builds a PR-ready artifact for a reviewed
candidate when updating an accepted package version.

The command is used after a reviewable candidate has been compared to the current
accepted version and before cross-repository proposal operations.

## Summary

- Generates a deterministic JSON payload with comparison summary and validation state.
- Detects changed claims from `intent` and `capability` deltas.
- Includes evidence digests from `specpm.yaml` and optional `harvest.json`.
- Includes `producerEvidenceLinks` for the accepted source bundle path,
  `producer-receipt.json`, `validation-report.json`, `diagnostics.json`,
  optional preflight output, optional static viewer output, and the
  accepted-source pull request diff.
- Includes a pending `registryAcceptanceDecision` reference with
  `status: external_required` and
  `recordKind: SpecPMRegistryAcceptanceDecision`.
- Detects same-version changes in copied package evidence before allowing a
  correction proposal.
- Optionally renders a deterministic markdown body for operator review.
- Does not mutate candidate or accepted directories.

## Command

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  --accepted-root accepted \
  CANDIDATE_DIR \
  [--update-kind upstream_revision|metadata_errata|correction] \
  [--allow-correction] \
  [--correction-note "metadata typo fix"] \
  [--reviewer-notes "rationale"]
```

Required:

- `CANDIDATE_DIR` as the reviewed candidate directory.
- `--accepted-root` for latest accepted comparison.

Optional:

- `--output` for JSON proposal file.
- `--proposal-body` for markdown proposal body, including the registry
  acceptance decision boundary.
- `--skip-validation` for offline runs.
- `--update-kind` override (`upstream_revision`, `metadata_errata`, `correction`).
- `--allow-correction` to permit explicit review of updates targeting an already
  accepted package version.
- `--correction-note` repeatable rationale note, required in correction mode.
- `--reviewer-notes` repeatable.

## Output

The payload includes:

- `packageId`, `packageSubdir`, `manifestEntryPath`
- `oldPackageVersion`, `newPackageVersion`
- `updateKind`, `sourceRevision`
- `evidenceDigests` map
- `producerEvidenceLinks`
- `changedClaims` list
- `validationStatus`
- `reviewerNotes`
- `comparison`, `candidate`, `accepted`, `issues`, `trustBoundary`
- optional `correction` object when correction mode is explicitly enabled

`--skip-validation` is explicit and should be used only for CI smoke fixtures or
operator-specific deterministic flows.

## References

- <doc:AcceptedCandidateDiffReports>
- <doc:AcceptedCandidateImpactClassificationReports>
- <doc:AcceptedPackageUpdateLifecycle>
- <doc:ProposalAutomation>
- <doc:SpecPMRegistryAcceptanceDecision>
