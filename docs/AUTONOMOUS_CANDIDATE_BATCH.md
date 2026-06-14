# Autonomous Candidate Batch

Status: MVP operator runner for local popular-library scraping

`autonomous-candidate-batch` runs the existing safe SpecHarvester producer
pipeline over a repository source manifest. It is intended for autonomous
exploration of popular libraries before deciding which candidates deserve
curated SpecPM submission work.

The command produces reviewable `preview_only` candidate artifacts. It does not
publish packages to SpecPM, does not remove `preview_only`, and does not make
AI output registry truth.
SpecPM remains the validation, acceptance, relation, and registry authority.

For single-package repositories with no workspace package records, the runner
uses the deterministic
[`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md)
path to produce one preview candidate with `0` relation proposals.

## Command

Run with local LM Studio:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Opt in to copied AI-enriched preview candidates when clean enrichment proposals
should become reviewable candidate artifacts:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --apply-ai-enrichment
```

Run deterministically without model calls for CI or offline smoke:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai
```

The input is the existing repository source manifest directory documented in
[`REPOSITORY_SOURCE_MANIFESTS.md`](REPOSITORY_SOURCE_MANIFESTS.md). The command
expects local public checkouts; it does not clone, fetch, or browse for
repositories.

In other words, the autonomous runner does not clone repositories; source
acquisition remains an explicit operator responsibility.
It also does not execute harvested code or install dependencies.

## Pipeline

For each selected repository, the runner orchestrates:

```text
repository source manifest
  -> collect-batch with workspace inventory and public interface indexes
  -> draft-package-set using role profile autonomous_popular_mvp by default
  -> preflight-bundle-set
  -> optional local LM Studio package-set AI draft proposal
  -> optional local LM Studio package-set AI enrichment proposal
  -> optional copied AI-enriched preview candidates
  -> autonomous-candidate-batch-report.json
```

Outputs are written under the requested output root:

```text
output/
  collected/<repository-id>/harvest.json
  collected/<repository-id>/workspace-inventory.json
  package-sets/<repository-id>/package-set-draft.json
  package-sets/<repository-id>/bundle-set-preflight.json
  package-sets/<repository-id>/ai/package-set-ai-draft-proposal.json
  package-sets/<repository-id>/ai/package-set-ai-enrichment-proposal.json
  package-sets/<repository-id>/enriched/<package-id>/specpm.yaml
  package-sets/<repository-id>/enriched/<package-id>/ai-enrichment-candidate-patch.json
  reports/batch-validation-report.json
  autonomous-candidate-batch-report.json
```

AI proposal files are present only when live local model execution is enabled.
The `enriched/` subtree is present only when `--apply-ai-enrichment` is set and
the package's `SpecHarvesterPackageSetAIEnrichmentProposal` is clean enough for
the deterministic `apply-ai-enrichment-proposal` helper.

## Report Identity

```json
{
  "apiVersion": "spec-harvester.autonomous-candidate-batch/v0",
  "kind": "SpecHarvesterAutonomousCandidateBatchReport",
  "schemaVersion": 1
}
```

The report records:

- collection status and validation report path;
- processed, skipped, and failed repository counts;
- per-repository harvest, workspace inventory, package-set draft, and preflight
  paths;
- candidate and relation counts;
- author-ready stop-policy summary;
- AI draft and enrichment proposal status when enabled;
- `aiEnrichedPreview` status, applied/skipped/failed counts, copied candidate
  paths, and `ai-enrichment-candidate-patch.json` paths when enabled;
- explicit producer-evidence authority and non-goals.

The default `autonomous_popular_mvp` role profile selects workspace,
`core_runtime`, React/Svelte binding, and generic member package roles while
still excluding examples, tests, fixtures, and private tooling from primary
candidate output.

## LM Studio Boundary

Live AI mode is local and operator-controlled:

- `--lm-studio-base-url` defaults to `http://127.0.0.1:1234`;
- `--lm-studio-model` is required unless `--skip-ai` is set;
- `--json-repair-max-attempts` bounds malformed JSON repair prompts per local
  model call;
- `--apply-ai-enrichment` is an explicit second opt-in that turns clean
  proposal evidence into copied preview candidate artifacts;
- provider execution is recorded as `operator_opt_in_local`;
- compact structured requests can be inspected, but raw prompts, raw provider
  responses, secrets, and chain-of-thought are not persisted;
- CI should use `--skip-ai` or existing external `--model-output` fixtures for
  lower-level AI proposal commands.

`--apply-ai-enrichment` does not change authority. It does not accept packages,
does not accept relations, does not remove `preview_only`, does not mutate
source candidates, does not publish registry metadata, does not create a SpecPM
pull request, and does not treat AI output as upstream project endorsement.
Warning-bearing, failed, missing, or package-misaligned AI enrichment proposals
remain sidecar-only and are counted as skipped.

When local model output is malformed, AI proposal records surface
`diagnosticCodes` such as `ai_json_repair_needed` and
`ai_json_repair_exhausted`, plus a `jsonRepair` summary. Exhausted repair marks
the AI proposal and repository as failed, but deterministic harvest,
package-set draft, bundle-set preflight, and author-ready summary artifacts
remain available for review.

## Trust Boundary

The runner must not:

- clone repositories;
- browse the network for source repositories;
- execute harvested package code;
- install dependencies;
- run package managers, builds, tests, or package scripts;
- publish SpecPM registry metadata;
- accept packages or relations;
- treat AI output as accepted package truth.

The intended MVP loop is:

```text
popular local checkouts
  -> autonomous candidate batch
  -> author-ready valid starter packages
  -> human/author review
  -> SpecPM-side preflight and maintainer acceptance decision
```

This keeps the original `LLM + schema` product idea: the model helps produce a
repository-personalized valid starter package, while final curation remains
with repository authors, their agents, and SpecPM maintainers.

For the SpecPM-facing review boundary for these batch artifacts, see
[`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md).
