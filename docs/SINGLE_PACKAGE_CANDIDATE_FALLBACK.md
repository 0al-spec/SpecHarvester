# Single-Package Candidate Fallback

Status: Implemented producer fallback for Phase 29.

The single-package candidate fallback lets `autonomous-candidate-batch` produce
one reviewable preview candidate when deterministic collection succeeds but
`workspace-inventory.json` has no package-set member records.

This is the Flask/Gin case from the mixed corpus baseline:

- Flask should produce `flask.core`.
- Gin should produce `gin.core`.
- Both should produce `0` relation proposals.

## Activation

The fallback is intentionally narrow. It runs only when:

- `draft-package-set` finds no selected package records;
- `workspace-inventory.json` has no package records at all;
- the inventory source metadata has a source manifest `packageId` or a
  repository-derived fallback id;
- repository-level `harvest.json` is colocated with `workspace-inventory.json`.

It does not run for monorepos that contain only examples, tooling, tests, or
roles excluded by the selected profile. Those repositories remain reviewable
gaps rather than being silently converted into a core package.

## Output Shape

The fallback writes the same candidate bundle shape as other preview candidates:

- `specpm.yaml`;
- `specs/*.spec.yaml`;
- `harvest.json`;
- `public-interface-index.json` when a colocated index exists;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- `author-ready-draft-quality-report.json`.

`package-set-draft.json` records candidate metadata with:

```json
{
  "selectionReason": "single_package_source_manifest_fallback",
  "role": "single_package"
}
```

`package-relation-proposals.json` remains present, but its `relations[]` list is
empty and `relationCount` is `0`. The fallback does not invent `contains`
relations.

In review terms, the fallback produces 0 relation proposals.

## Trust Boundary

The fallback is still `producer_preview_evidence_only`.

It keeps:

- `preview_only`;
- no package execution;
- no dependency installation;
- no registry mutation;
- no SpecPM acceptance;
- no relation acceptance;
- no namespace ownership claim.

SpecPM remains the validation, acceptance, relation, and registry authority.

## Follow-Up

`P29-T5` handles bounded LM Studio/OpenAI-compatible JSON repair/retry. `P29-T6`
re-runs the mixed Flask/Gin/xyflow corpus after fallback and repair support.

See also
[`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md)
and
[`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md).
