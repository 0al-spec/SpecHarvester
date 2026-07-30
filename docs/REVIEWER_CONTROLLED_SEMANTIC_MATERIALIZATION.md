# Reviewer-Controlled Semantic Materialization

P55-T8 creates a new preview candidate revision from one complete semantic
proposal and one explicit P55-T7 reviewer decision:

```bash
spec-harvester materialize-semantic-candidate \
  --candidate review-input/candidate \
  --semantic-record semantic-proposal-record.json \
  --review-decision current-review-decision.json \
  --output review-output/materialized \
  --specpm-command specpm
```

The decision must contain a digest-valid `semanticReview` with decision
`accepted` or `edited`, a non-empty reviewer identity, and explicit selected
claim IDs. Edited text is accepted only for its matching selected claim.
Rejected or deferred decisions cannot materialize output.

## Field Mapping

| Selected semantic input | Preview revision field |
| --- | --- |
| Purpose | `metadata.summary` and BoundarySpec `intent.summary` |
| Capability | Existing capability `summary` values |
| Interface | BoundarySpec `scope.includes` |
| Nearby-intent difference and non-goal | BoundarySpec `scope.excludes` |
| Bound observed or experimental intent decision | Manifest intents and existing capability `intentIds` |

Experimental IDs remain visibly `intent.experimental.*` proposal metadata.
Materialization does not make them canonical.

Only `specpm.yaml` and direct `specs/*.spec.yaml` files are copied. Symlinks,
oversized inputs, stale bindings, unknown claims, malformed scope or capability
shapes, and failed validation stop before publishing an output revision. The
source directory is rehashed after materialization and must remain unchanged.

The output contains `candidate/` and `materialization-report.json`. The report
binds packet, portable record, proposal, source, reviewer edit, before/after
file digests, applied claims and intents, and both validation results. The new
manifest remains `preview_only: true`; `isRegistryTruth` is false and
`registryMutationCount` is zero.

SpecHarvester parses the resulting manifest before invoking bounded, read-only
`specpm validate`. Neither accepted package sources nor the public index are
modified.
