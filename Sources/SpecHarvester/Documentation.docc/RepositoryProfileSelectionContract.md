# Repository Profile Selection Contract

Status: Phase 37 contract plan.

SpecHarvester can use explicit parser profiles such as
`python.web_framework.v0`, but the operator still has to know when a profile
should apply. Real repositories also expose higher-level shapes before path
classification starts: single packages, workspaces, nested package roots, meta
packages, CLI bridges, examples, generated sources, and mixed layouts.

This contract defines a language- and framework-agnostic selection layer for
repository profile plugins. It is not a detector implementation and it is not a
FastMCP, FastAPI, Python, JavaScript, Rust, Go, Swift, or JVM special case.

## Selection Model

All repository profile selection follows:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

The model is ecosystem-neutral. Future Python, npm, Cargo, Go, SwiftPM, Maven,
Gradle, Bazel, or custom profiles may provide different evidence signals, but
the core policy exposes the same decision structure.

## Contract Shape

Future machine-readable output should use:

```json
{
  "apiVersion": "spec-harvester.repository-profile-detection/v0",
  "kind": "SpecHarvesterRepositoryProfileDetection",
  "schemaVersion": 1,
  "authority": "producer_profile_selection_only"
}
```

The artifact is producer review evidence. It explains why a profile was or was
not selected. It does not make generated package claims authoritative and it
does not accept any package, relation, or registry update.

## Static Inputs

Selection may inspect only local, bounded, static evidence:

- repository source manifest metadata;
- resolved local checkout path and pinned revision/ref;
- operator-provided package family hints and labels;
- root and nested package manifests;
- workspace files and lock/workspace metadata;
- allowlisted README or project metadata;
- directory layout and package-root candidates;
- existing workspace inventory when available;
- explicit CLI or manifest profile overrides.

Selection must not perform network discovery, dependency installation,
package-manager execution, code execution, registry lookups, AI calls, or
candidate drafting.

## Selection Modes

| Mode | Meaning |
| --- | --- |
| `none` | Disable profile selection and use generic behavior. |
| `auto` | Select only when evidence is high-confidence and conflict-free. |
| `<profile-id>` | Apply an explicit profile id from CLI or manifest override. |

Precedence is deterministic:

1. explicit CLI profile override;
2. source manifest `repositoryProfile` override;
3. high-confidence auto-detected profile;
4. generic fallback profile;
5. blocked decision when even generic behavior would be misleading.

## Confidence

| Confidence | Meaning | Auto-select eligible |
| --- | --- | --- |
| `high` | Strong static evidence and no conflicts. | yes |
| `medium` | Useful evidence exists but needs review. | no |
| `low` | Weak hint only. | no |
| `blocked` | Evidence is inconsistent or unsafe. | no |

Auto-selection requires `high` confidence and no unresolved conflict. Medium,
low, missing, unsupported, and conflicting signals fall back to generic
behavior with diagnostics unless an explicit override is present.

## Candidate Profile Record

Each detected candidate profile should record:

- `profileId`;
- `confidence`;
- `evidencePaths`;
- `reasonCodes`;
- `conflicts`;
- `recommendedAction`: `select`, `fallback`, `require_override`, or `block`.

## Decision Artifact Fields

`SpecHarvesterRepositoryProfileDetection` should include:

- repository id, repository URL, revision/ref, and source manifest entry;
- selection mode and override source;
- selected profile id or `null`;
- fallback profile id;
- candidate profile records;
- rejected profile records and reason codes;
- diagnostics with severity, code, message, and evidence paths;
- non-authority statements;
- downstream hints produced by the selected profile, if any.

## Machine-Readable Fixture

P37-T2 provides the first concrete fixture:

```text
tests/fixtures/repository_profile_detection/generic-package-set.example.json
```

The fixture records a high-confidence auto-selection for a generic package-set
repository. It includes:

- `apiVersion: spec-harvester.repository-profile-detection/v0`;
- `kind: SpecHarvesterRepositoryProfileDetection`;
- `schemaVersion: 1`;
- `authority: producer_profile_selection_only`;
- repository identity and source manifest metadata;
- `selection.mode: auto`;
- `selection.overrideSource: none`;
- `selection.selectedProfileId: generic.package_set.v0`;
- `selection.fallbackProfileId: generic.repository.v0`;
- candidate profiles with confidence, score, evidence paths, reason codes,
  conflicts, and recommended actions;
- rejected profiles with reason codes;
- diagnostics with severity, code, message, and evidence paths;
- advisory downstream hints such as `package_set_root`, `member_package`, and
  `documentation_source`;
- non-authority statements proving the artifact does not clone/fetch
  repositories, run AI, draft packages, publish registry metadata, accept
  packages or relations, remove `preview_only`, or treat plugin decisions as
  registry truth.

This fixture is intentionally generic. It proves the profile selection artifact
shape without making Python, JavaScript, FastMCP, FastAPI, or any other
ecosystem normative.

## CLI Report Surface

P37-T3 adds an opt-in CLI surface:

```bash
spec-harvester repository-profile-detect \
  --repository-id example.generic-package-set \
  --repository-url https://example.invalid/generic-package-set \
  --revision 0000000000000000000000000000000000000000 \
  --selection auto \
  --evidence-path workspace.yaml \
  --evidence-path packages/core/package.json \
  --evidence-path packages/adapter/package.json \
  --output repository-profile-detection.json
```

The command can also read repository identity from an existing source manifest
directory:

```bash
spec-harvester repository-profile-detect \
  --source-manifest inputs \
  --source-id example.generic-package-set \
  --selection auto \
  --evidence-path workspace.yaml
```

The command accepts `--selection auto`, `--selection none`, or an explicit
profile id such as `--selection custom.vendor_profile.v0`.

This CLI only emits `SpecHarvesterRepositoryProfileDetection`. It reads static
metadata supplied by the operator, writes JSON to stdout, and optionally writes
the same payload to `--output`. It does not collect source files, run analyzers,
invoke package managers, run AI, or draft packages.

## Autonomous Candidate Batch Integration

P37-T4 connects the same decision artifact to `autonomous-candidate-batch` as
producer-side evidence:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-profile-selection auto
```

The option accepts `none`, `auto`, or an explicit profile id. The default is
`none`, which emits a disabled artifact and preserves generic behavior. `auto`
reads already-collected `workspace-inventory.json` evidence and selects only
high-confidence, conflict-free generic profiles. Explicit profile ids are
recorded as CLI overrides.

Each processed repository gets a `repositoryProfileDetection` summary in the
batch report and a JSON artifact under:

```text
reports/repository-profile-detections/<repository-id>/repository-profile-detection.json
```

The report records `repositoryProfileSelection` with
`authority: producer_profile_selection_only` and
`advisoryHintsAppliedToDrafting: false`.

This is not drafting authority. The batch does not apply advisory hints to
candidate drafting, accept packages, accept relations, remove `preview_only`,
publish registry metadata, or treat plugin decisions as registry truth.

## Generic Hints

P37-T5 defines the generic hint vocabulary in
<doc:RepositoryProfileDiscoveryHints> and the fixture:

```text
tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json
```

The vocabulary artifact uses
`apiVersion: spec-harvester.repository-profile-hints/v0`,
`kind: SpecHarvesterRepositoryProfileHintVocabulary`, and
`authority: producer_profile_hint_vocabulary_only`.

Profiles may propose ecosystem-neutral hints:

- `package_set_root`;
- `member_package`;
- `meta_package`;
- `primary_package`;
- `cli_package`;
- `bridge_package`;
- `plugin_package`;
- `example_package`;
- `test_package`;
- `documentation_source`;
- `generated_artifact`;
- `internal_utility`;
- `evidence_only`.

Hints are advisory. They may guide workspace inventory, source classification,
candidate drafting, and reviewer UI, but the hint boundary does not accept
packages, does not accept relations, does not remove `preview_only`, does not
publish registry metadata, and does not treat profile hints as registry truth.

## Cross-Ecosystem Fixtures

P37-T6 records cross-ecosystem fixture coverage in
<doc:RepositoryProfileCrossEcosystemFixtures>.
The GitHub source document is
`docs/REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`.

The fixture set includes:

- `cross-ecosystem-workspace.example.json` selects `generic.package_set.v0`;
- `cross-ecosystem-single-package.example.json` selects
  `generic.single_package.v0`;
- `cross-ecosystem-nested-package.example.json` falls back to
  `generic.repository.v0`;
- `cross-ecosystem-ambiguous-multi-signal.example.json` falls back to
  `generic.repository.v0`.

These fixtures prove the profile selection contract against workspace-shaped,
single-package, nested-package, and ambiguous multi-signal repositories without
making any language or framework normative.

They do not implement ecosystem-specific plugins, accept packages, accept
relations, publish registry metadata, remove `preview_only`, treat profile
decisions as registry truth, or treat profile hints as registry truth.

## Real FastMCP Comparison

P37-T7 records a real FastMCP comparison in:

```text
tests/fixtures/repository_profile_real_runs/p37-t7-fastmcp-auto-selection-comparison.example.json
```

The DocC report is <doc:RepositoryProfileRealRunFastMCP>.

The run shows that repository-wide auto-selection currently falls back to
`generic.repository.v0` with `confidence: low`, while explicit manual targeting
of `fastmcp_slim` produces a narrower public interface index. The fixture
records `follow_up_required` and recommends P37-T8.

The reusable finding is not FastMCP-specific: `harvest.json` can see a package
manifest while `workspace-inventory.json` has no manifest records, leaving
profile detection without enough high-confidence evidence. P37-T8 should make
repository profile detection consume harvested package manifest evidence when
workspace inventory is empty.

## Fallback Behavior

Fallback must be explicit:

- `generic.repository.v0` continues with current generic behavior;
- `none` means the operator disabled profile selection;
- `blocked` means generic behavior would produce misleading evidence and the
  run should require operator review.

## Non-Authority Boundary

Repository profile selection is producer-side evidence only.

It does not clone or fetch repositories.
It does not treat plugin decisions as registry truth.
It does not treat AI output as registry truth.

It does not clone or fetch repositories, install dependencies, execute
harvested code, invoke package managers, call package registries, run AI,
draft packages, publish registry metadata, accept packages or relations, seed
baselines, remove `preview_only`, treat plugin decisions as registry truth, or
treat AI output as registry truth.

## Relationship to Parser Profiles

```text
source manifest
  -> repository profile detection
  -> selected repository profile / generic fallback
  -> workspace/member hints
  -> parser profile path classification
  -> analyzer path selection
  -> public_interface_index
  -> candidate drafting
```

Repository profiles answer "which repository shape is this?" Parser profiles
answer "which paths are public interface, semantic usage, docs, tests,
generated, tooling, internal, or ignored?"

## Motivating Validation Cases

FastMCP and FastAPI are validation cases, not normative profile rules. FastMCP
demonstrates why workspace/member shape and package-root targeting should be
detected before drafting. FastAPI demonstrates why path-level parser profiles
should keep tutorials out of public interface evidence.

## Planned Follow-Ups

- `P37-T2`: add the machine-readable
  `SpecHarvesterRepositoryProfileDetection` fixture format.
- `P37-T3`: implement an opt-in detection CLI/report surface.
- `P37-T4`: connect profile selection to autonomous candidate batch.
- `P37-T5`: define generic workspace/member discovery hints.
- `P37-T6`: add cross-ecosystem profile fixtures.
- `P37-T7`: rerun a real repository with profile auto-selection and compare
  against manual targeting.
