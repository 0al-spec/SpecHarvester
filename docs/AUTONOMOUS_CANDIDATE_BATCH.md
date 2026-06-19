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

Opt in to repository profile detection evidence while keeping candidate
drafting generic:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-profile-selection auto
```

`--repository-profile-selection` accepts `none`, `auto`, or an explicit
profile id. The default is `none`.

Attach repository plugin applicability sidecar evidence while keeping candidate
drafting generic:

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
static evaluator while keeping candidate drafting generic:

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
The generated report is still sidecar producer evidence with
`sourceMode: auto_static_evaluator`, `appliedToDrafting: false`, and
`registryAuthority: false`.

If both modes are provided, the explicit `--repository-plugin-applicability`
sidecar wins. This preserves operator control and prevents a generated report
from silently overriding a reviewed sidecar.

Attach repository plugin adapter manifest and preflight evidence while keeping
candidate drafting generic:

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

Attach a disabled trusted local adapter runner report as review-only evidence:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --trusted-local-adapter-run-report /tmp/trusted-local-adapter-run-report.json
```

`--trusted-local-adapter-run-report` accepts a
`SpecHarvesterTrustedLocalAdapterRunReport` emitted by
`trusted-local-adapter-runner-skeleton`. The batch validates the report
identity, disabled runner status, no-execution boundary, and non-authority
statements, copies it under
`reports/trusted-local-adapter-run-evidence/trusted-local-adapter-run-report.json`,
and records `trustedLocalAdapterRunEvidence` with source/copied SHA-256
digests, report identity, diagnostic codes, `adapterExecution: not_run`,
`adapterCodeLoaded: false`, `adapterProcessSpawned: false`,
`executedAdapterCount: 0`, `appliedToDrafting: false`, and
`registryAuthority: false`.

Trusted local adapter run evidence is explicit operator-supplied producer
evidence. The batch does not execute adapters, load adapter code, run adapter
processes, install dependencies, invoke package managers, execute harvested
code, run AI because of this sidecar, change static plugin applicability
behavior, accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, or treat the runner report as
adapter output truth.

In `auto` mode, repository profile detection first uses
`workspace-inventory.json` workspace and member manifest records. If workspace
inventory has no manifest records, the batch falls back to already-collected
static manifest paths from `harvest.json`. This keeps detection
language-neutral while allowing root manifests such as `pyproject.toml`,
`package.json`, `Cargo.toml`, `go.mod`, and `Package.swift` to drive
single-package profile evidence without executing package managers.

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
  -> optional repository profile detection evidence
  -> optional repository plugin applicability sidecar evidence
  -> optional repository plugin adapter evidence sidecar
  -> optional trusted local adapter run evidence sidecar
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
  reports/repository-profile-detections/<repository-id>/repository-profile-detection.json
  reports/repository-plugin-applicability/repository-plugin-applicability-report.json
  reports/repository-plugin-adapter-evidence/adapter-manifest.json
  reports/repository-plugin-adapter-evidence/adapter-preflight-report.json
  reports/trusted-local-adapter-run-evidence/trusted-local-adapter-run-report.json
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
- repository profile selection mode and authority;
- repository plugin applicability sidecar path, digest, authority, summary
  counts, diagnostic codes, and source mode when an explicit
  `--repository-plugin-applicability` sidecar is copied or when
  `--repository-plugin-registry` and
  `--repository-plugin-static-evidence-envelope` generate the sidecar;
- repository plugin adapter evidence sidecar manifest/preflight paths, source
  paths, SHA-256 digests, authority, adapter counts, allowed/rejected/fallback/
  blocked counts, diagnostic codes, `appliedToDrafting: false`,
  `registryAuthority: false`, and `adapterExecution: not_run` when both
  `--repository-plugin-adapter-manifest` and
  `--repository-plugin-adapter-preflight` are supplied;
- trusted local adapter run evidence sidecar path, source path, SHA-256
  digests, authority, runner status, no-execution boundary, diagnostic codes,
  `appliedToDrafting: false`, `registryAuthority: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, and `executedAdapterCount: 0` when
  `--trusted-local-adapter-run-report` is supplied;
- processed, skipped, and failed repository counts;
- per-repository harvest, workspace inventory, package-set draft, and preflight
  paths;
- per-repository `repositoryProfileDetection` path, selected profile id,
  decision, confidence, reason codes, and diagnostic codes;
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

Repository profile detection is producer-side evidence only. Even when
`--repository-profile-selection auto` selects `generic.package_set.v0`, the
batch records `advisoryHintsAppliedToDrafting: false` and preserves the
existing generic drafting path. Detection output does not accept packages,
accept relations, remove `preview_only`, publish registry metadata, or treat
plugin decisions, harvested manifest evidence, or profile hints as registry
truth.

Repository plugin applicability evidence is sidecar producer evidence.
It is producer-side sidecar evidence
only. Even when `--repository-plugin-applicability` records selected plugins,
or when the static evaluator auto-generates selected plugin decisions from
`--repository-plugin-registry` and
`--repository-plugin-static-evidence-envelope`, the batch records
`appliedToDrafting: false`; it does not execute plugins, load third-party
plugin code, read repository source files, change parser profile behavior,
change repository profile scoring, accept packages, accept relations, remove
`preview_only`, publish registry metadata, or treat plugin decisions as
registry truth.

Repository plugin adapter evidence is also sidecar producer evidence only.
Even when `--repository-plugin-adapter-manifest` and
`--repository-plugin-adapter-preflight` are supplied, the batch records
`repositoryPluginAdapterEvidence` with `appliedToDrafting: false`,
`registryAuthority: false`, and `adapterExecution: not_run`. It validates and
copies the sidecars for review, but does not load adapter code, execute
adapters, install dependencies, invoke package managers, execute harvested
code, run AI, change static plugin applicability behavior, accept packages,
accept relations, seed baselines, remove `preview_only`, publish registry
metadata, or treat adapter output as registry truth.

Trusted local adapter run evidence is sidecar producer evidence only. Even
when `--trusted-local-adapter-run-report` is supplied, the batch records
`trustedLocalAdapterRunEvidence` with `appliedToDrafting: false`,
`registryAuthority: false`, `adapterExecution: not_run`,
`adapterCodeLoaded: false`, `adapterProcessSpawned: false`, and
`executedAdapterCount: 0`. It validates and copies the report for review, but
does not run adapters, load third-party adapter code, run adapter processes,
install dependencies, invoke package managers, execute harvested code, run AI,
change static plugin applicability behavior, accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
or treat a runner report as adapter output truth.

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
