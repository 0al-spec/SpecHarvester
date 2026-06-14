# Autonomous Candidate Corpus Baseline

Status: Producer baseline evidence for Phase 29.

This page records the first mixed local corpus run for
`autonomous-candidate-batch` after the SpecPM candidate-layer intake policy.
It is a durable baseline for implementation follow-ups, not a registry
acceptance record.

The machine-readable companion fixture is:

```text
tests/fixtures/autonomous_candidate_corpus_baseline/flask-gin-xyflow.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.autonomous-candidate-corpus-baseline/v0",
  "kind": "SpecHarvesterAutonomousCandidateCorpusBaseline",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Corpus

Corpus id: `local-flask-gin-xyflow`.

The baseline covers local public checkouts:

| Repository | Package id hint | Revision |
| --- | --- | --- |
| Flask | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |

SpecHarvester did not clone repositories, execute harvested code, install
dependencies, publish registry metadata, or remove `preview_only`.

## Deterministic Results

The deterministic `--skip-ai` path passed for all three repositories:

| Repository | Candidates | Relations | Preflight | Author-ready decision |
| --- | ---: | ---: | --- | --- |
| Flask | `0` | `0` | `passed` | `blocked_until_inputs_change` |
| Gin | `0` | `0` | `passed` | `blocked_until_inputs_change` |
| xyflow | `4` | `3` | `passed` | `stop_for_author_review` |

Product reading:

- Flask and Gin gathered useful deterministic evidence but produced no package
  candidates because the current package-set drafter expects workspace topology.
- xyflow remains the package-set-friendly reference case: one aggregate
  workspace candidate, three primary member candidates, and three `contains`
  relation proposals.

## Live LM Studio Results

The live LM Studio run used `openai/gpt-oss-20b` through the local
OpenAI-compatible provider path.

| Repository | AI draft | AI enrichment | Status | Gap |
| --- | --- | --- | --- | --- |
| Flask | `completed` | `completed` | `needs_regeneration` | `single_package_fallback_needed` |
| Gin | `completed` | `completed` | `needs_regeneration` | `single_package_fallback_needed` |
| xyflow | `failed` | `not_run_after_ai_draft_failure` | `needs_regeneration` | `ai_json_repair_needed` |

For Flask and Gin the model calls completed, but there were no proposal subjects
because deterministic drafting produced `0` candidates. For xyflow, the observed
diagnostic was `model_output_invalid_json` with message
`Model output must be valid JSON`.

## Product Verdict

The baseline separates pipeline health from candidate quality:

- `pipelineHealth: deterministic_pipeline_passed`
- `candidateQuality: needs_follow_up`

The practical conclusion is that the autonomous runner works as plumbing for
the mixed corpus, but it is not ready for broad popular-library scraping until
two concrete gaps are addressed:

- `single_package_fallback_needed`: single-package repositories need a preview
  candidate fallback.
- `ai_json_repair_needed`: local LM Studio/OpenAI-compatible output needs
  bounded JSON repair/retry handling.

no generated preview candidate is promoted to SpecPM acceptance by this
baseline. It cannot accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, or replace maintainer review.

## Follow-Up Tasks

The next planned tasks are:

- `P29-T4`: implement single-package candidate fallback for repositories such
  as Flask and Gin.
- `P29-T5`: implement bounded LM Studio JSON repair/retry.
- `P29-T6`: re-run the mixed corpus after those fixes and decide whether the
  MVP is ready for larger autonomous scraping.

See also
[`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md)
and
[`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md).
