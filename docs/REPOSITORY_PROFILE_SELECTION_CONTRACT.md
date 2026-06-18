# Repository Profile Selection Contract

Status: Phase 37 contract plan.

SpecHarvester can use explicit parser profiles such as
`python.web_framework.v0`, but the operator still has to know when a profile
should apply. Real repositories also expose higher-level shapes before path
classification starts: single packages, workspaces, nested package roots,
meta packages, CLI bridges, examples, generated sources, and mixed layouts.

This contract defines a language- and framework-agnostic selection layer for
repository profile plugins. It is not a detector implementation and it is not
a FastMCP, FastAPI, Python, JavaScript, Rust, Go, Swift, or JVM special case.

## Problem

Profile selection has to be explicit and reviewable:

- hidden heuristics make generated package topology hard to audit;
- repository-wide collection may over-include docs, examples, tests, or demo
  apps as public interface evidence;
- manual target selection can improve quality but does not scale to curated
  multi-ecosystem corpus runs;
- language/framework plugins can provide evidence, but the core pipeline needs
  a common way to choose, reject, fall back, and record the decision.

The selection subsystem must answer:

```text
Which repository profile should apply, why, and what happens if confidence is
too weak or conflicting?
```

## Selection Model

All repository profile selection follows the same deterministic model:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

This model is intentionally ecosystem-neutral. A future Python, npm, Cargo, Go,
SwiftPM, Maven, Gradle, Bazel, or custom profile may provide different evidence
signals, but the core policy must expose the same decision structure.

## Contract Shape

A future machine-readable decision artifact should use a versioned shape:

```json
{
  "apiVersion": "spec-harvester.repository-profile-detection/v0",
  "kind": "SpecHarvesterRepositoryProfileDetection",
  "schemaVersion": 1,
  "authority": "producer_profile_selection_only",
  "repositoryId": "example",
  "selection": {
    "mode": "auto",
    "selectedProfileId": "example.workspace.v0",
    "confidence": "high",
    "reasonCodes": ["workspace_manifest_present", "member_manifests_present"]
  }
}
```

The artifact is producer review evidence. It explains why a profile was or was
not selected. It does not make generated package claims authoritative and it
does not accept any package, relation, or registry update.

## Static Inputs

Profile selection may inspect only local, bounded, static evidence:

- repository source manifest metadata;
- resolved local checkout path and pinned revision/ref;
- operator-provided package family hints and labels;
- root and nested package manifests;
- workspace files and lock/workspace metadata;
- allowlisted README or project metadata;
- directory layout and package-root candidates;
- existing workspace inventory when available;
- explicit CLI or manifest profile overrides.

Profile selection must not perform network discovery, dependency installation,
package-manager execution, code execution, registry lookups, AI calls, or
candidate drafting.

## Selection Modes

The operator-facing mode space is:

| Mode | Meaning |
| --- | --- |
| `none` | Disable profile selection and use generic behavior. |
| `auto` | Detect candidate profiles and select only when evidence is high-confidence and conflict-free. |
| `<profile-id>` | Apply an explicit profile id from CLI or source manifest override. |

Default behavior should remain conservative. If no mode is implemented yet,
existing generic behavior continues.

## Precedence

Selection precedence is deterministic:

1. explicit CLI profile override;
2. source manifest `repositoryProfile` override;
3. high-confidence auto-detected profile;
4. generic fallback profile;
5. blocked decision when even generic behavior would be misleading.

Explicit overrides must still be recorded. They are operator intent, not proof
that the selected profile is semantically correct.

## Confidence

Candidate profile confidence is one of:

| Confidence | Meaning | Auto-select eligible |
| --- | --- | --- |
| `high` | Strong static evidence and no conflicting profile signals. | yes |
| `medium` | Useful evidence exists but needs operator review. | no |
| `low` | Weak hint only. | no |
| `blocked` | Evidence is inconsistent or unsafe to interpret. | no |

Auto-selection requires `high` confidence and no unresolved conflict. Medium,
low, missing, unsupported, and conflicting signals must fall back to generic
behavior with diagnostics unless an explicit override is present.

## Candidate Profile Record

Each detected candidate profile should record:

```json
{
  "profileId": "example.workspace.v0",
  "confidence": "high",
  "evidencePaths": ["workspace.yaml", "packages/core/package.json"],
  "reasonCodes": ["workspace_manifest_present"],
  "conflicts": [],
  "recommendedAction": "select"
}
```

Required review fields:

- `profileId`: stable profile id;
- `confidence`: confidence bucket;
- `evidencePaths`: repository-relative evidence paths;
- `reasonCodes`: machine-readable rationale;
- `conflicts`: other profile ids or evidence conflicts;
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

The artifact should be hashable and referenceable from producer receipts,
quality reports, and handoff artifacts.

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
an explicit producer-side evidence layer:

```bash
python3 -m spec_harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai \
  --repository-profile-selection auto
```

The option accepts:

- `none`: default, emits a disabled decision artifact and preserves generic
  behavior;
- `auto`: reads already-collected `workspace-inventory.json` evidence and
  selects only high-confidence, conflict-free generic profiles;
- `<profile-id>`: records an explicit operator override with
  `overrideSource: cli`.

For each processed repository, the batch report attaches a
`repositoryProfileDetection` summary and writes:

```text
reports/repository-profile-detections/<repository-id>/repository-profile-detection.json
```

The batch report also records `repositoryProfileSelection` with
`authority: producer_profile_selection_only` and
`advisoryHintsAppliedToDrafting: false`.

This is intentionally not a drafting authority. The batch uses detection output
as inspectable evidence only; it does not apply advisory hints to candidate
drafting, accept packages, accept relations, remove `preview_only`, publish
registry metadata, or treat plugin decisions as registry truth.

## Generic Hints

P37-T5 defines the generic hint vocabulary in
[`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md)
and the fixture:

```text
tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json
```

The vocabulary artifact uses
`apiVersion: spec-harvester.repository-profile-hints/v0`,
`kind: SpecHarvesterRepositoryProfileHintVocabulary`, and
`authority: producer_profile_hint_vocabulary_only`.

Profiles may propose hints in this ecosystem-neutral vocabulary:

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

## Fallback Behavior

Fallback must be explicit:

- `generic.repository.v0` means continue with current generic behavior;
- `none` means the operator disabled profile selection;
- `blocked` means even generic behavior would produce misleading evidence and
  the run should require operator review.

Fallback diagnostics should tell the operator what evidence was missing,
ambiguous, unsupported, or conflicting.

## Non-Authority Boundary

Repository profile selection is producer-side evidence only.

It does not clone or fetch repositories.
It does not treat plugin decisions as registry truth.
It does not treat AI output as registry truth.

It does not:

- clone or fetch repositories;
- install dependencies;
- execute harvested code, tests, package scripts, or build tools;
- invoke package managers;
- call package registries;
- run AI;
- draft packages;
- publish registry metadata;
- accept packages or relations;
- seed baselines;
- remove `preview_only`;
- treat plugin decisions as registry truth;
- treat AI output as registry truth.

## Relationship to Parser Profiles

Repository profile selection happens before parser profile path
classification:

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

FastMCP and FastAPI are validation cases, not normative profile rules:

- FastMCP demonstrates why workspace/member shape and package-root targeting
  should be detected before drafting.
- FastAPI demonstrates why path-level parser profiles should keep tutorials
  out of public interface evidence.

Future fixtures may use these repositories, but the contract remains reusable
for other ecosystems and repository shapes.

## Planned Follow-Ups

- `P37-T2`: add the machine-readable
  `SpecHarvesterRepositoryProfileDetection` fixture format.
- `P37-T3`: implement an opt-in detection CLI/report surface.
- `P37-T4`: connect profile selection to autonomous candidate batch.
- `P37-T5`: define generic workspace/member discovery hints.
- `P37-T6`: add cross-ecosystem profile fixtures.
- `P37-T7`: rerun a real repository with profile auto-selection and compare
  against manual targeting.
