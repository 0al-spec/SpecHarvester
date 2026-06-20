# Operational MVP Static-Only Baseline

Status: P43-T4 real local static-only baseline.

P43-T4 runs the Phase 43 operational MVP validation over an
operator-provided pinned local corpus without AI, adapter execution, package
manager invocation, dependency installation, clone/fetch, package acceptance,
or registry publishing.

The durable fixture is:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
```

## What Was Run

The run used existing local checkouts and the deterministic autonomous batch
path:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/inputs \
  --out /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/output \
  --skip-ai \
  --repository-profile-selection auto
```

The source manifest is intentionally kept outside the repository because it
contains machine-local checkout paths. The fixture records the input manifest
digest, batch report digest, local checkout paths, exact revisions, and per-run
artifact digests.

## Corpus

| Repository | Ecosystem | Shape | Revision | Static-only result |
| --- | --- | --- | --- | --- |
| `xyflow` | JavaScript/TypeScript | package-set monorepo | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | passed, 4 candidates, 3 relations |
| `fastapi` | Python | framework/library package | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | passed, 1 candidate |
| `gin` | Go | single-package framework | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | passed, 1 candidate |

All three checkouts were clean and pinned at run time.

The `xyflow` local checkout origin was `git@github.com:SoundBlaster/xyflow.git`
while the Phase 43 plan uses `https://github.com/xyflow/xyflow` as the example
candidate. The baseline records that fork/origin difference explicitly instead
of rewriting it.

## Result Summary

The static-only run produced:

- `3` processed repositories;
- `3` passed static-only repository results;
- `6` preview candidate packages;
- `6` candidate preflight passes;
- `3` package relation proposals;
- `3` repository profile selections;
- `0` AI draft proposals;
- `0` AI enrichment proposals;
- `0` adapter sidecars;
- `3` SpecPM handoff-ready preview results that still require author review.

The baseline report digest is:

```text
sha256:735cc878bc3dc19325c269adf2f2e5e12798373527b37979a92ce6f950062499
```

## Quality Baseline

Each repository result records the P43 quality dimensions:

- `validity`: passed bundle-set preflight.
- `repositorySpecificity`: reviewable static repository evidence is present.
- `evidencePrecision`: complete static public-interface index for FastAPI and
  Gin; reviewable with a partial public-interface index caveat for xyflow.
- `packageTopology`: reviewable package-set topology for xyflow and
  reviewable single-package topology for FastAPI and Gin.
- `claimConservatism`: reviewable, with author confirmation still required.
- `authorActionability`: strong, because the generated quality reports include
  explicit author action items.
- `SpecPMHandoffReadiness`: reviewable handoff-ready preview candidates, not
  registry-accepted packages.

The only observed caveat is `partial_public_interface_index` for xyflow. It is
not a blocking stop condition for P43-T4, but it should remain visible for the
AI-enabled comparison and exit decision.

## Non-Authority Boundary

This baseline is producer-side evidence only. It does not:

- clone or fetch repositories;
- accept mutable repository state;
- execute harvested code;
- install dependencies;
- invoke package managers;
- enable trusted local adapter execution;
- run adapter code;
- run AI;
- accept packages or relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth;
- treat adapter output as registry truth.

Generated candidates remain preview review material until explicit SpecPM
maintainer review and acceptance.

## Follow-Up

- `P43-T5`: recorded
  [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
  over the same pinned corpus with local LM Studio `openai/gpt-oss-20b`;
  AI draft/enrichment sidecars are proposal-only and do not change static
  handoff truth.
- `P43-T6`: add author handoff summaries.
- `P43-T7`: record the operational MVP exit decision.

## References

- [`OPERATIONAL_MVP_VALIDATION_PLAN.md`](OPERATIONAL_MVP_VALIDATION_PLAN.md)
- [`OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md)
- [`OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md)
- [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
- [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md)
