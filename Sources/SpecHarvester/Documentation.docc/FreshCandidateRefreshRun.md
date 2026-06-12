# Fresh Candidate Refresh Run

`fresh-candidate-refresh-run` exports a generated package-set bundle into the
fresh generated-root layout consumed by SpecPM's
`producer-bundle prepare-refresh-decision` helper.

It bridges producer evidence and consumer-side refresh comparison:

```text
SpecHarvester package-set output
  -> SpecHarvesterFreshCandidateRefreshRun
  -> specpm producer-bundle prepare-refresh-decision
  -> SpecPMGeneratedCandidateRefreshDecision
```

The command does not publish packages, mutate SpecPM sources, or decide
registry acceptance.

## Command

```bash
python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --fresh-generated-root .smoke/xyflow-package-set/fresh-generated \
  --output .smoke/xyflow-package-set/fresh-candidate-refresh-run.json
```

The payload identity is:

```json
{
  "apiVersion": "spec-harvester.fresh-candidate-refresh-run/v0",
  "kind": "SpecHarvesterFreshCandidateRefreshRun",
  "schemaVersion": 1
}
```

## Layout

The normalized root uses the
`specpm-public-index-generated-root/v0` layout:

```text
<package_id>/<version>/specpm.yaml
<package_id>/<version>/specs/*.spec.yaml
```

The manifest records SHA-256 digests for contract-bearing files only:
`specpm.yaml` and `specs/*.spec.yaml`.

## SpecPM Consumer

The `specpmConsumer` section records the command
`specpm producer-bundle prepare-refresh-decision`, package IDs, package-set
subject, version, source repository, source revision, and expected artifacts:

- `refresh-decision.json`
- `prepare-report.json`
- `preflight-report.json`

SpecPM compares the fresh generated root with its current
`public-index/generated` and curated evidence. Passing comparison is review
evidence, not registry acceptance.

## Authority Boundary

The report records `producerEvidenceAuthority: evidence_only`,
`registryAuthority: SpecPM maintainer review`, and `noRegistryMutation: true`.

The command does not accept packages, publish registry metadata, edit curated
artifacts, execute source repository code, run package managers, or replace
SpecPM maintainer review.

## Observed `xyflow` Refresh Compare

P28-T2 ran real `xyflow` revision
`a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` through:

```text
collect-batch --emit-workspace-inventory
  -> draft-package-set
  -> preflight-bundle-set
  -> render-package-set-site
  -> fresh-candidate-refresh-run
  -> SpecPM prepare-refresh-decision
  -> SpecPM preflight-refresh-decision
```

SpecPM prepared `status: no_update_required`, `updateNeeded: false`, and
`reason: no_contract_delta`, then verified 8 generated contract-file digests
with `preflight-refresh-decision`.

This confirms the current generator can reproduce the accepted `xyflow`
generated contract surface. Producer receipt and report changes remain useful
evidence, but they are not enough to justify a registry update when
`specpm.yaml` and `specs/*.spec.yaml` are unchanged.

## Observed `TanStack/query` Refresh Compare

P28-T3 repeated the path on `https://github.com/TanStack/query` at revision
`feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`.

The workspace inventory found 100 package manifests and no workspace
diagnostics. Default draft roles selected only `tanstack_query.workspace`,
skipped 99 package manifests, and produced no relations. An explicit
`--role workspace --role member_package` run selected 39 candidates, excluded
61 example packages, produced 38 `contains` relation proposals, passed
bundle-set preflight, rendered the package-set viewer, and prepared 78
contract files in the fresh generated root.

SpecPM compare against the current registry root returned a structured
missing-baseline result: prepare report `failed`, refresh decision summary
`status: manual_review_required`, `updateNeeded: true`,
`reason: refresh_prepare_requires_review`, package count 39, and digest
verified count 0. The first blocker was
`refresh_decision_prepare_current_contract_files_missing`, and no
`refresh-decision.json` was written.

This confirms the producer-side package-set handoff is not `xyflow`-specific,
while also clarifying that `prepare-refresh-decision` is a refresh compare
helper, not a first-submission bootstrap helper. New repositories need a
separate first-submission or seeded-baseline workflow before refresh comparison
can emit a preflightable decision file. Use
`baseline-submission-handoff` and <doc:BaselineSubmissionHandoff> to record
that boundary as review evidence.
