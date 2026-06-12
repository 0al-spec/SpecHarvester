# Fresh Candidate Refresh Run

Status: Producer-side SpecPM refresh evidence contract

`fresh-candidate-refresh-run` exports a generated package-set bundle into the
fresh generated-root layout expected by SpecPM's
`producer-bundle prepare-refresh-decision` helper.

The command exists for the refresh/no-op workflow:

```text
SpecHarvester package-set output
  -> fresh-candidate-refresh-run
  -> SpecPM prepare-refresh-decision
  -> SpecPM refresh-decision preflight
```

It does not publish packages, mutate SpecPM sources, or decide whether a
generated candidate should replace curated accepted artifacts.

## Command

```bash
python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --fresh-generated-root .smoke/xyflow-package-set/fresh-generated \
  --output .smoke/xyflow-package-set/fresh-candidate-refresh-run.json
```

If `package-set-draft.json` already records `source.exactRevision`, the command
uses it as the source revision. Operators can override source identity when
needed:

```bash
python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --fresh-generated-root .smoke/xyflow-package-set/fresh-generated \
  --source-repository https://github.com/xyflow/xyflow \
  --source-revision a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd \
  --run-label xyflow-refresh-evaluation \
  --output .smoke/xyflow-package-set/fresh-candidate-refresh-run.json
```

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.fresh-candidate-refresh-run/v0",
  "kind": "SpecHarvesterFreshCandidateRefreshRun",
  "schemaVersion": 1
}
```

## Fresh Generated Root Layout

SpecPM expects generated candidates to be addressable by package ID and
version:

```text
<fresh-generated-root>/
  <package_id>/
    <version>/
      specpm.yaml
      specs/*.spec.yaml
```

The report records this as:

```json
{
  "freshGeneratedRoot": {
    "layout": "specpm-public-index-generated-root/v0",
    "packagePathTemplate": "<package_id>/<version>"
  }
}
```

Only contract-bearing files participate in the refresh comparison:

- `<package_id>/<version>/specpm.yaml`
- `<package_id>/<version>/specs/*.spec.yaml`

The command may copy additional producer evidence files beside them, such as
`producer-receipt.json`, `validation-report.json`, `diagnostics.json`, and
`author-ready-draft-quality-report.json`, but SpecPM's refresh helper compares
only the manifest and boundary spec files.

## SpecPM Consumer Contract

The report includes a `specpmConsumer` section so operators can pass the output
to SpecPM without guessing paths:

```json
{
  "specpmConsumer": {
    "command": "specpm producer-bundle prepare-refresh-decision",
    "expectedArtifacts": [
      "refresh-decision.json",
      "prepare-report.json",
      "preflight-report.json"
    ]
  }
}
```

For a package set such as `xyflow`, the equivalent SpecPM command is:

```bash
specpm producer-bundle prepare-refresh-decision \
  --root /path/to/SpecPM \
  --fresh-generated-root .smoke/xyflow-package-set/fresh-generated \
  --package xyflow.workspace \
  --package xyflow.react \
  --package xyflow.svelte \
  --package xyflow.system \
  --package-id xyflow.workspace \
  --version 0.1.0 \
  --source-repository https://github.com/xyflow/xyflow \
  --source-revision a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd \
  --output refresh-decision.json \
  --json
```

SpecPM then writes or prints a
`SpecPMGeneratedCandidateRefreshDecisionPrepareReport` and can emit a
`SpecPMGeneratedCandidateRefreshDecision` for
`preflight-refresh-decision`.

## Authority Boundary

Every `SpecHarvesterFreshCandidateRefreshRun` records:

```json
{
  "authority": {
    "producerEvidenceAuthority": "evidence_only",
    "registryAuthority": "SpecPM maintainer review",
    "noRegistryMutation": true
  }
}
```

This means:

- SpecHarvester prepared review evidence only.
- SpecPM remains the validator and registry authority.
- A no-op refresh decision is still a maintainer-review artifact.
- The compact authority summary is `producerEvidenceAuthority:
  evidence_only` and `noRegistryMutation: true`.
- `noRegistryMutation` must remain true for this producer command.

The command does not accept packages, publish registry metadata, edit curated
artifacts, execute source repository code, run package managers, or replace
SpecPM maintainer review.

## Relation To Package-Set Handoff

`package-set-handoff-proposal` explains what maintainers should review.
`fresh-candidate-refresh-run` prepares a filesystem layout and manifest that
SpecPM can compare mechanically.

Use both when evaluating whether a fresh package-set run changes accepted
registry contract surface:

```text
package-set-handoff-proposal: review context
fresh-candidate-refresh-run: compare input
SpecPM prepare-refresh-decision: consumer-side decision draft
```
