# Autonomous Candidate Batch

Status: MVP operator runner for local popular-library scraping

`autonomous-candidate-batch` runs the safe producer pipeline over repository
source manifests and writes `SpecHarvesterAutonomousCandidateBatchReport`.

Run with local LM Studio:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b
```

Run without model calls for CI or offline smoke:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai
```

The command expects existing local public checkouts from repository source
manifests. It does not clone repositories, execute harvested code, install
dependencies, publish registry metadata, or accept packages.
In short, it does not clone repositories, execute harvested code, or install
dependencies.

Pipeline:

```text
source manifest
  -> collect-batch
  -> workspace inventory
  -> draft-package-set
  -> preflight-bundle-set
  -> optional local LM Studio AI draft/enrichment proposals
  -> autonomous-candidate-batch-report.json
```

The default `autonomous_popular_mvp` role profile selects workspace,
`core_runtime`, React/Svelte binding, and generic member package roles while
excluding examples, tests, fixtures, and private tooling from primary candidate
output.

Report identity:

```json
{
  "apiVersion": "spec-harvester.autonomous-candidate-batch/v0",
  "kind": "SpecHarvesterAutonomousCandidateBatchReport",
  "schemaVersion": 1
}
```

Generated package files remain `preview_only` producer evidence. SpecPM remains
the validation, acceptance, relation, and registry authority.
