# Single-Package Candidate Fallback

Status: Implemented producer fallback for Phase 29.

The single-package candidate fallback lets `autonomous-candidate-batch` produce
one reviewable preview candidate when deterministic collection succeeds but
`workspace-inventory.json` has no package-set member records.

This covers the Flask/Gin mixed-corpus gap:

- Flask produces `flask.core`.
- Gin produces `gin.core`.
- Both produce `0` relation proposals.

## Activation

The fallback runs only when `draft-package-set` finds no selected package
records, `workspace-inventory.json` has no package records at all, source
metadata has a package id or repository-derived fallback id, and repository-level
`harvest.json` is colocated with `workspace-inventory.json`.

It does not run for monorepos that contain only examples, tooling, tests, or
roles excluded by the selected profile.

## Output Shape

The fallback writes:

- `specpm.yaml`;
- `specs/*.spec.yaml`;
- `harvest.json`;
- `public-interface-index.json` when a colocated index exists;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- `author-ready-draft-quality-report.json`.

`package-set-draft.json` records:

```json
{
  "selectionReason": "single_package_source_manifest_fallback",
  "role": "single_package"
}
```

`package-relation-proposals.json` remains present with an empty `relations[]`
list and `relationCount: 0`. The fallback does not invent `contains` relations.

In review terms, the fallback produces 0 relation proposals.

## Trust Boundary

The fallback is still `producer_preview_evidence_only`. It keeps `preview_only`,
does not execute packages, does not install dependencies, does not mutate the
registry, does not imply SpecPM acceptance, and does not accept relations.
The operational boundary is no SpecPM acceptance.

SpecPM remains the validation, acceptance, relation, and registry authority.

## Follow-Up

`P29-T5` handles bounded LM Studio/OpenAI-compatible JSON repair/retry. `P29-T6`
re-runs the mixed Flask/Gin/xyflow corpus after fallback and repair support.

See also <doc:AutonomousCandidateCorpusBaseline> and
<doc:AutonomousCandidateTechDebtPlan>.
