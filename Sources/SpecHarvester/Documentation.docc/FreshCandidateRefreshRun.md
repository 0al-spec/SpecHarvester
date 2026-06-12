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
