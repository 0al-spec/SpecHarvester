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

Opt in to repository profile detection evidence:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-profile-selection auto
```

`--repository-profile-selection` accepts `none`, `auto`, or an explicit profile
id. The default is `none`.

Attach repository plugin applicability sidecar evidence:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-plugin-applicability reports/repository-plugin-applicability-report.json
```

`--repository-plugin-applicability` accepts a local
`SpecHarvesterRepositoryPluginApplicabilityReport` JSON file. The batch
validates the report identity, copies it to
`reports/repository-plugin-applicability/repository-plugin-applicability-report.json`,
and records a `repositoryPluginApplicability` sidecar summary with path, digest,
authority, selected/rejected/fallback/blocked counts, and diagnostic codes.
The sidecar records `appliedToDrafting: false` and `registryAuthority: false`.

Generate repository plugin applicability sidecar evidence from the deterministic
static evaluator:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-plugin-registry tests/fixtures/repository_plugins/generic-registry.example.json \
  --repository-plugin-static-evidence-envelope tests/fixtures/repository_plugins/static-evidence-envelope.example.json
```

`--repository-plugin-registry` and
`--repository-plugin-static-evidence-envelope` must be provided together. When
both are present and no explicit `--repository-plugin-applicability` sidecar is
provided, the batch evaluates the registry against the static evidence envelope
and writes
`reports/repository-plugin-applicability/repository-plugin-applicability-report.json`.
The generated report remains sidecar producer evidence with
`sourceMode: auto_static_evaluator`, `appliedToDrafting: false`, and
`registryAuthority: false`.

If both modes are provided, the explicit `--repository-plugin-applicability`
sidecar wins. This preserves operator control and prevents a generated report
from silently overriding a reviewed sidecar.

Attach repository plugin adapter manifest and preflight evidence:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-plugin-adapter-manifest tests/fixtures/repository_plugins/adapter-manifest.example.json \
  --repository-plugin-adapter-preflight tests/fixtures/repository_plugins/adapter-preflight-report.example.json
```

`--repository-plugin-adapter-manifest` and
`--repository-plugin-adapter-preflight` must be provided together. The batch
validates the artifact identities, verifies that the preflight
`manifest.digest` matches the supplied manifest, copies both files under
`reports/repository-plugin-adapter-evidence/`, and records
`repositoryPluginAdapterEvidence` with copied paths, source paths, SHA-256
digests, adapter counts, allowed/rejected/fallback/blocked counts, diagnostic
codes, `appliedToDrafting: false`, `registryAuthority: false`, and
`adapterExecution: not_run`.

Adapter evidence remains explicit operator-supplied producer evidence. The
batch does not auto-generate it, load adapters, execute adapters, install
dependencies, invoke package managers, run AI, change static plugin
applicability defaults, accept packages, accept relations, remove
`preview_only`, publish registry metadata, or treat adapter output as registry
truth.

In `auto` mode, repository profile detection first uses
`workspace-inventory.json` workspace and member manifest records. If workspace
inventory has no manifest records, the batch falls back to already-collected
static manifest paths from `harvest.json`. This keeps detection
language-neutral while allowing root manifests such as `pyproject.toml`,
`package.json`, `Cargo.toml`, `go.mod`, and `Package.swift` to drive
single-package profile evidence without executing package managers.

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
  -> optional repository profile detection evidence
  -> optional repository plugin applicability sidecar evidence
  -> optional repository plugin adapter evidence sidecar
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

The report records `repositoryProfileSelection` and per-repository
`repositoryProfileDetection` summaries. The JSON artifact is written under
`reports/repository-profile-detections/<repository-id>/repository-profile-detection.json`.

When `--repository-plugin-applicability` is provided, the report records
`repositoryPluginApplicability` with the copied sidecar path, digest, authority,
summary counts, and diagnostic codes. The copied JSON artifact is written under
`reports/repository-plugin-applicability/repository-plugin-applicability-report.json`.
When `--repository-plugin-registry` and
`--repository-plugin-static-evidence-envelope` are provided without an explicit
sidecar, the report records the same `repositoryPluginApplicability` section
with `sourceMode: auto_static_evaluator`, generated report path, digest,
authority, selected/rejected/fallback/blocked counts, and diagnostic codes.

When `--repository-plugin-adapter-manifest` and
`--repository-plugin-adapter-preflight` are provided, the report records
`repositoryPluginAdapterEvidence` with copied manifest/preflight paths, source
paths, SHA-256 digests, authority, adapter counts, allowed/rejected/fallback/
blocked counts, diagnostic codes, `appliedToDrafting: false`,
`registryAuthority: false`, and `adapterExecution: not_run`. The copied JSON
artifacts are written as
`reports/repository-plugin-adapter-evidence/adapter-manifest.json` and
`reports/repository-plugin-adapter-evidence/adapter-preflight-report.json`.

Repository profile detection remains producer evidence only. The batch records
`advisoryHintsAppliedToDrafting: false`; it does not apply hints to candidate
drafting, accept packages, accept relations, remove `preview_only`, publish
registry metadata, or treat plugin decisions, harvested manifest evidence, or
profile hints as registry truth.

Repository plugin applicability evidence remains sidecar producer evidence.
It remains producer-side sidecar evidence
only. The batch records `appliedToDrafting: false`; it does not execute
plugins, load third-party plugin code, read repository source files, change
parser profile behavior, change repository profile scoring, accept packages,
accept relations, remove `preview_only`, publish registry metadata, or treat
plugin decisions as registry truth.

Repository plugin adapter evidence also remains sidecar producer evidence only.
The batch records `appliedToDrafting: false`, `registryAuthority: false`, and
`adapterExecution: not_run`; it does not load adapter code, execute adapters,
install dependencies, invoke package managers, execute harvested code, run AI,
change static plugin applicability behavior, accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata, or
treat adapter output as registry truth.

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
