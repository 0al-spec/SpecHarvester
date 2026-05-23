# Real Repository Refinement Validation

Status: Phase 15 plan

This document defines a reproducible, local-only validation plan for exercising
SpecHarvester on real public repository checkouts while keeping SpecNode,
Platform, SpecPM, and `.0al` ownership boundaries intact.

The plan validates the SpecHarvester-side pipeline:

```text
operator-supplied checkout paths
  -> source manifest
  -> collect-batch
  -> deterministic evidence artifacts
  -> draft
  -> SpecPM validation and governance reports
  -> optional external SpecNode contract boundary
  -> compact quality report and follow-up routing
```

SpecHarvester owns deterministic evidence, draft candidates, artifact bundle
construction, validation, and reporting. It does not implement SpecNode runtime,
provider discovery, model execution, scheduling, provider lifecycle, or
provider-specific orchestration.

## Local Input Manifest

Use a local, untracked manifest under `.smoke/inputs`. The manifest points at
already-cloned public repository checkouts and pinned revisions.

```yaml
repositories:
  - id: flask
    repository: https://github.com/pallets/flask
    checkout: ../../flask
    revision: "<commit-sha>"
    packageId: flask.core

  - id: gin
    repository: https://github.com/gin-gonic/gin
    checkout: ../../gin
    revision: "<commit-sha>"
    packageId: gin.core
```

The checkout path is local operator input. The path is not a stable contract and
must not be committed with machine-specific values.
Strict public mode is the `collect-batch` default; use `--relaxed-private` only
when intentionally validating private-code spec coverage.

## Command Sequence

Validate manifest shape:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests .smoke/inputs
```

Collect deterministic evidence and analyzer summaries:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/real-repository-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/.analyzer-cache \
  --report .smoke/output/real-repository-validation/batch-validation.json
```

Draft one candidate at a time:

```bash
PYTHONPATH=src python -m spec_harvester draft \
  .smoke/output/real-repository-validation/flask \
  --package-id flask.core \
  --out .smoke/output/real-repository-validation/flask
```

Generate advisory governance reports when enough candidate output exists:

```bash
PYTHONPATH=src python -m spec_harvester governance-report \
  --candidates-root .smoke/output/real-repository-validation \
  --output .smoke/output/real-repository-validation/governance-claims.json

PYTHONPATH=src python -m spec_harvester governance-upstream-report \
  --candidates-root .smoke/output/real-repository-validation \
  --output .smoke/output/real-repository-validation/namespace-upstream.json

PYTHONPATH=src python -m spec_harvester governance-license-provenance-report \
  --candidates-root .smoke/output/real-repository-validation \
  --output .smoke/output/real-repository-validation/license-provenance.json
```

Build a compact local triage summary:

```bash
PYTHONPATH=src python -m spec_harvester smoke-triage-summary \
  --batch-validation .smoke/output/real-repository-validation/batch-validation.json \
  --governance-claims .smoke/output/real-repository-validation/governance-claims.json \
  --namespace-upstream .smoke/output/real-repository-validation/namespace-upstream.json \
  --license-provenance .smoke/output/real-repository-validation/license-provenance.json \
  --output .smoke/output/real-repository-validation/smoke-triage.json
```

Optional external refinement may consume
`SpecHarvesterSpecNodeArtifactBundle`, `SpecHarvesterRefinePreviewPlan`, and
`SpecNodeRefinementRetryRun` shaped artifacts when an external
SpecNode-compatible implementation exists. SpecHarvester records and validates
the contract-facing artifacts; SpecNode owns provider execution and usage
receipt production.

## Expected Local Outputs

All generated outputs remain under `.smoke/output` and are not committed:

- `harvest.json`
- `ProjectProfile` evidence inside `harvest.json`
- `public-interface-index.json`
- `semanticEvidenceIndex` evidence inside drafted specs when available
- `specpm.yaml`
- `specs/*.spec.yaml`
- `batch-validation.json`
- `governance-claims.json`
- `namespace-upstream.json`
- `license-provenance.json`
- `smoke-triage.json`
- optional external refinement result, retry audit, and usage receipt summaries

## Quality Rubric

Record compact, reviewable scores or notes for each repository:

| Category | Question |
| --- | --- |
| intent accuracy | Does the draft describe the target package behavior instead of SpecHarvester or SpecPM mechanics? |
| capability/evidence support | Are capability claims backed by known deterministic evidence references? |
| SpecPM validation | Does `specpm.yaml` plus `specs/*.spec.yaml` validate, and are warnings actionable? |
| analyzer coverage | Did `ProjectProfile`, `PublicInterfaceIndex`, and semantic evidence cover the dominant package surface? |
| retry effectiveness | Did semantic review findings improve the next proposal without changing source artifacts? |
| token usage | Are provider/model usage receipts present when external refinement ran? |
| boundary compliance | Were raw source, prompts, provider logs, secrets, and chain-of-thought excluded? |

## Routing Findings

Use the owner table before creating follow-up work:

| Finding class | Owner |
| --- | --- |
| Missing deterministic analyzer evidence, weak draft intent, incorrect support target, or report gap | SpecHarvester |
| Job protocol, provider discovery, model execution, usage receipt, runtime policy, or provider lifecycle issue | SpecNode |
| workspace catalog, local path wiring, launch profile, service topology, or provider wiring issue | Platform |
| SpecPackage validation semantics, evidence vocabulary, registry compatibility, or accepted-source contract issue | SpecPM |
| Cross-repo observation, unresolved ownership question, or temporary handoff | `.0al` |

Write `.0al` handoffs through the local logging CLI when the finding is
cross-repository but not yet canonical behavior:

```bash
../.0al/scripts/0al-log.py --project specharvester --kind handoff \
  --owner specnode \
  --title "Provider usage receipt contract needed" \
  --text "Real-repository validation needs a stable external SpecNode usage receipt field."
```

## Safety Rules

- Do not install harvested dependencies.
- Do not run harvested package scripts.
- Do not execute harvested repository code.
- Do not run harvested tests or build commands.
- Do not contact package registries while harvesting.
- Do not commit generated candidates, `.smoke/` output, raw prompts, provider
  transcripts, secrets, or model chain-of-thought.
- Do not treat generated candidates as accepted registry truth.

Repeated failures become Workplan tasks. Single-run prompt tweaks are not a
durable fix unless they are promoted into a versioned prompt contract, analyzer,
schema, or validation policy.
