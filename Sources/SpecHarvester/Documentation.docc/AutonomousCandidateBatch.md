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
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Opt in to copied AI-enriched preview candidates:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --apply-ai-enrichment
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
  -> optional copied AI-enriched preview candidates
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

When `--apply-ai-enrichment` is set, clean
`SpecHarvesterPackageSetAIEnrichmentProposal` artifacts can be applied through
the deterministic `apply-ai-enrichment-proposal` helper into
`package-sets/<repository-id>/enriched/<package-id>/`. Each copied candidate
keeps `preview_only` and receives `ai-enrichment-candidate-patch.json`.

The `aiEnrichedPreview` report section records applied, skipped, and failed
counts. Warning-bearing, failed, missing, or package-misaligned AI enrichment
proposals remain sidecar-only and are counted as skipped.

This mode does not accept packages, does not accept relations, does not remove
`preview_only`, does not mutate source candidates, does not publish registry
metadata, does not create a SpecPM pull request, and does not treat AI output
as upstream project endorsement.

Live AI mode uses bounded JSON repair for malformed local provider output.
`--json-repair-max-attempts` limits repair prompts per model call. Batch AI
records expose `diagnosticCodes` such as `ai_json_repair_needed` and
`ai_json_repair_exhausted`, plus a `jsonRepair` summary. Exhausted repair marks
the AI layer failed while preserving deterministic harvest, package-set draft,
preflight, and author-ready summary artifacts.

For single-package repositories with no workspace package records, the runner
uses the deterministic <doc:SinglePackageCandidateFallback> path to produce one
preview candidate with `0` relation proposals.

For the SpecPM-facing review boundary for these batch artifacts, see
<doc:AutonomousCandidateIntakePolicy>.
