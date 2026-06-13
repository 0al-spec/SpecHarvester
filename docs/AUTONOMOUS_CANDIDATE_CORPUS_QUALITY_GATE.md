# Autonomous Candidate Corpus Quality Gate

Status: Post-mitigation producer evidence for Phase 29.

This page records the mixed local Flask/Gin/xyflow corpus run after:

- `P29-T4` deterministic single-package candidate fallback;
- `P29-T5` bounded LM Studio/OpenAI-compatible JSON repair/retry.

The machine-readable companion fixture is:

```text
tests/fixtures/autonomous_candidate_corpus_quality_gate/flask-gin-xyflow-post-fallbacks.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.autonomous-candidate-corpus-quality-gate/v0",
  "kind": "SpecHarvesterAutonomousCandidateCorpusQualityGate",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Corpus

Corpus id: `local-flask-gin-xyflow-post-fallbacks`.

| Repository | Package id hint | Revision |
| --- | --- | --- |
| Flask | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |

SpecHarvester did not clone repositories, execute harvested code, install
dependencies, publish registry metadata, accept packages, accept relations,
seed baselines, or remove `preview_only`.

## Deterministic Results

The deterministic `--skip-ai` path passed for all three repositories:

| Repository | Candidates | Candidate ids | Relations | Preflight | Author-ready decision |
| --- | ---: | --- | ---: | --- | --- |
| Flask | `1` | `flask.core` | `0` | `passed` | `stop_for_author_review` |
| Gin | `1` | `gin.core` | `0` | `passed` | `stop_for_author_review` |
| xyflow | `4` | `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system` | `3` | `passed` | `stop_for_author_review` |

Product reading:

- Flask and Gin now produce reviewable single-package preview candidates.
- xyflow still produces the expected aggregate workspace/member package-set
  shape with three `contains` relation proposals.
- Every repository has at least one reviewable preview candidate and passing
  bundle-set preflight.

## Live LM Studio Results

The live run used `openai/gpt-oss-20b` through local LM Studio at
`http://127.0.0.1:1234` with `jsonRepairMaxAttempts: 1`.

| Repository | AI draft | AI draft diagnostics | AI enrichment | JSON repair | Repository status |
| --- | --- | --- | --- | --- | --- |
| Flask | `warning` | `excluded_package_unknown` | `completed` | `not_needed` | `passed` |
| Gin | `warning` | `excluded_package_unknown` | `completed` | `not_needed` | `passed` |
| xyflow | `warning` | `package_set_id_missing` | `completed` | `not_needed` | `passed` |

The warning-level AI draft diagnostics are candidate-layer review evidence, not
registry acceptance blockers. AI enrichment completed for every repository.
This run did not need JSON repair and did not exhaust repair attempts.

## Product Verdict

Verdict: `ready_for_limited_popular_library_scraping`.

After P29-T4 and P29-T5, the mixed corpus produces reviewable preview
candidates for Flask, Gin, and xyflow with passing deterministic preflight. The
MVP is ready for a limited larger popular-library scraping batch under
candidate-layer review, not automatic SpecPM acceptance.

This is not a claim that generated specs are final or accepted. The generated
candidate packages remain valid starter packages for author and maintainer
review. SpecPM remains the validation, acceptance, relation, and registry
authority.

## Commands

Deterministic gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  /tmp/spec-harvester-p29-t6.edfHiE/inputs \
  --out /tmp/spec-harvester-p29-t6.edfHiE/deterministic \
  --skip-ai
```

Live LM Studio gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  /tmp/spec-harvester-p29-t6.edfHiE/inputs \
  --out /tmp/spec-harvester-p29-t6.edfHiE/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

## Non-Authority Boundary

The quality gate cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- replace author or SpecPM maintainer review.

See also:

- [`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md)
- [`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md)
- [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
