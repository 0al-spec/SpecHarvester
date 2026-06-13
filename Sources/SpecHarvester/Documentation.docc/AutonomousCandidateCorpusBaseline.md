# Autonomous Candidate Corpus Baseline

Status: Producer baseline evidence for Phase 29.

This page mirrors
`docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`. It records the first mixed
local corpus run for `autonomous-candidate-batch` as a durable baseline before
implementing fallback or model repair behavior.

The machine-readable fixture is
`tests/fixtures/autonomous_candidate_corpus_baseline/flask-gin-xyflow.example.json`
with:

- `apiVersion: spec-harvester.autonomous-candidate-corpus-baseline/v0`
- `kind: SpecHarvesterAutonomousCandidateCorpusBaseline`
- `schemaVersion: 1`
- `authority: producer_preview_evidence_only`

## Corpus

Corpus id: `local-flask-gin-xyflow`.

| Repository | Package id hint | Revision |
| --- | --- | --- |
| Flask | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |

SpecHarvester did not clone repositories, execute harvested code, install
dependencies, publish registry metadata, or remove `preview_only`.

## Deterministic Results

The deterministic `--skip-ai` path passed for all repositories:

| Repository | Candidates | Relations | Preflight | Author-ready decision |
| --- | ---: | ---: | --- | --- |
| Flask | `0` | `0` | `passed` | `blocked_until_inputs_change` |
| Gin | `0` | `0` | `passed` | `blocked_until_inputs_change` |
| xyflow | `4` | `3` | `passed` | `stop_for_author_review` |

Flask and Gin are classified as `single_package_fallback_needed`. xyflow remains
the package-set-friendly reference case with one aggregate workspace candidate,
three primary member candidates, and three `contains` relation proposals.

## Live LM Studio Results

The live LM Studio path used `openai/gpt-oss-20b`.

| Repository | AI draft | AI enrichment | Status | Gap |
| --- | --- | --- | --- | --- |
| Flask | `completed` | `completed` | `needs_regeneration` | `single_package_fallback_needed` |
| Gin | `completed` | `completed` | `needs_regeneration` | `single_package_fallback_needed` |
| xyflow | `failed` | `not_run_after_ai_draft_failure` | `needs_regeneration` | `ai_json_repair_needed` |

The xyflow diagnostic is `model_output_invalid_json`: `Model output must be
valid JSON`.

## Product Verdict

The baseline records:

- `pipelineHealth: deterministic_pipeline_passed`
- `candidateQuality: needs_follow_up`

This means the runner works as plumbing for the mixed corpus, but broad
popular-library scraping should wait for:

- `P29-T4`: single-package candidate fallback;
- `P29-T5`: bounded LM Studio JSON repair/retry;
- `P29-T6`: corpus quality gate after those fixes.

no generated preview candidate is promoted to SpecPM acceptance. This baseline
cannot accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, or replace maintainer review.

See also <doc:AutonomousCandidateTechDebtPlan> and
<doc:AutonomousCandidateIntakePolicy>.
