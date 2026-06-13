# Autonomous Candidate Corpus Quality Gate

This page records the post-mitigation Flask/Gin/xyflow corpus quality gate
after deterministic single-package fallback and bounded LM Studio JSON
repair/retry.

The companion fixture is:

```text
tests/fixtures/autonomous_candidate_corpus_quality_gate/flask-gin-xyflow-post-fallbacks.example.json
```

Artifact identity:

```json
{
  "apiVersion": "spec-harvester.autonomous-candidate-corpus-quality-gate/v0",
  "kind": "SpecHarvesterAutonomousCandidateCorpusQualityGate",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Corpus

The corpus id is `local-flask-gin-xyflow-post-fallbacks`.

| Repository | Package id hint | Revision |
| --- | --- | --- |
| Flask | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |

## Results

The deterministic `--skip-ai` path passed for every repository:

| Repository | Candidates | Relations | Preflight | Author-ready decision |
| --- | ---: | ---: | --- | --- |
| Flask | `1` | `0` | `passed` | `stop_for_author_review` |
| Gin | `1` | `0` | `passed` | `stop_for_author_review` |
| xyflow | `4` | `3` | `passed` | `stop_for_author_review` |

The live LM Studio run used `openai/gpt-oss-20b` with
`jsonRepairMaxAttempts: 1`:

| Repository | AI draft | AI draft diagnostics | AI enrichment | JSON repair | Repository status |
| --- | --- | --- | --- | --- | --- |
| Flask | `warning` | `excluded_package_unknown` | `completed` | `not_needed` | `passed` |
| Gin | `warning` | `excluded_package_unknown` | `completed` | `not_needed` | `passed` |
| xyflow | `warning` | `package_set_id_missing` | `completed` | `not_needed` | `passed` |

The AI draft warnings are candidate-layer review evidence. They do not accept
packages or relations and do not block the producer-side quality gate.

## Verdict

Verdict: `ready_for_limited_popular_library_scraping`.

The mixed corpus now produces reviewable preview candidates for Flask, Gin, and
xyflow with passing deterministic preflight. SpecHarvester can run a limited
larger popular-library scraping batch under candidate-layer review.

This remains producer preview evidence. It does not publish registry metadata,
seed baselines, remove `preview_only`, or replace author and SpecPM maintainer
review.

See also <doc:AutonomousCandidateCorpusBaseline>,
<doc:SinglePackageCandidateFallback>, <doc:AutonomousCandidateTechDebtPlan>,
and <doc:AutonomousCandidateIntakePolicy>.
