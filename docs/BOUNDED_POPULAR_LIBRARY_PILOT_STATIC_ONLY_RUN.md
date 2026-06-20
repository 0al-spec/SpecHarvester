# Bounded Popular-Library Pilot Static-Only Run

Status: P46-T2 real local static-only run.

P46-T2 runs the P46 bounded popular-library pilot manifest in deterministic
static-only mode. It is the required gate before any local OpenAI-compatible
provider run in P46-T3.

The source manifest is:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

The durable fixture is:

```text
tests/fixtures/bounded_popular_library_pilot_static_only_run/p46-t2-bounded-popular-library-pilot-static-only-run.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.bounded-popular-library-pilot-static-only-run/v0
kind: SpecHarvesterBoundedPopularLibraryPilotStaticOnlyRun
authority: producer_static_preview_evidence_only
```

## What Was Run

Run root:

```text
/tmp/specharvester-p46-t2-bounded-popular-library-static-only-20260620T200603Z
```

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p46-bounded-popular-library-pilot \
  --out /tmp/specharvester-p46-t2-bounded-popular-library-static-only-20260620T200603Z/output \
  --skip-ai \
  --repository-profile-selection auto
```

The source manifest digest was:

```text
sha256:fe5786e7b905bef12bbda53ff1f3fe01a03dcd2051826bdca599e46e99f01f26
```

The batch report digest was:

```text
sha256:01a47a4ceb6d787a11a0059dfca805c35ea51625943bb1873fef5284e271a9b7
```

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | passed |
| Processed repositories | 6 |
| Failed repositories | 0 |
| Passed preflights | 6 |
| Candidate packages | 9 |
| Relation proposals | 3 |
| Preflight warnings | 0 |
| Repository profile detections | 6 |
| Repository profile selected | 4 |
| Repository profile fallback | 2 |
| AI draft proposals | 0 |
| AI enrichment proposals | 0 |
| Trusted local adapter sidecars | 0 |

In prose: six repositories processed, nine preview candidates, three relation
proposals, zero AI proposals, zero adapter sidecars, and no registry authority.

## Repository Results

| Repository | Status | Candidates | Relations | Profile decision | Interface status |
| --- | --- | ---: | ---: | --- | --- |
| Flask | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Gin | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| xyflow | passed | 4 | 3 | selected `generic.package_set.v0` | partial, 29 diagnostics |
| Cupertino | passed | 1 | 0 | fallback | complete |
| NavigationSplitView | passed | 1 | 0 | fallback | complete |
| docc2context | passed | 1 | 0 | selected `generic.single_package.v0` | complete |

xyflow produced the relation proposals:

- `xyflow.workspace.contains.xyflow.react`
- `xyflow.workspace.contains.xyflow.svelte`
- `xyflow.workspace.contains.xyflow.system`

## Carry-Forward Triage

The static-only gate passed, but P46-T4 and P46-T5 must keep these items
visible before any registry promotion:

- Gin `model_evidence_path_unsupported` from P45-T8 remains a
  registry-promotion blocker until triaged, even though it was not observed in
  the static-only run.
- xyflow `partial_public_interface_index` was observed with 29 diagnostics.
  It does not block P46-T3, but it remains review evidence for pilot triage.
- xyflow `operator_checkout_origin_fork_mismatch` from P46-T1 remains visible
  because the local checkout origin differs from the canonical manifest URL.

## Boundary

P46-T2 did not run AI, enable trusted local adapter execution, run adapter
code, clone or fetch repositories, install dependencies, invoke package
managers, execute harvested code, accept packages or relations, publish
registry metadata, seed baselines, remove `preview_only`, persist raw prompts,
persist raw provider responses, persist secrets, or persist chain-of-thought.

The run does not treat static output as registry truth, does not treat AI
output as registry truth, and does not treat adapter output as registry truth.
All generated candidates and relations remain preview review evidence requiring
SpecPM maintainer review.

## Follow-Up

P46-T3 may run the same pinned manifest with the local OpenAI-compatible
provider. The P46-T3 run must preserve proposal-only AI output and must not
persist raw prompts, raw provider responses, secrets, or chain-of-thought.
