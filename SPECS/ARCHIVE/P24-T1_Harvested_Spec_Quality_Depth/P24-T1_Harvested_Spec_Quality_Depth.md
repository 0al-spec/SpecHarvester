# P24-T1 — Harvested Spec Quality Depth

## Objective

Upgrade generated SpecPM candidate packages from safe metadata previews to more
subject-focused preview contracts. The task improves deterministic draft output
for packages such as `xyflow.core` without changing the trust boundary:
generated candidates remain `preview_only`, maintainer-reviewed, and based on
public harvested evidence rather than package execution or model-authored direct
mutation.

## Scope

In scope:

- Make generated manifest and BoundarySpec summaries describe the target package
  boundary more directly when deterministic package metadata is available.
- Add finer-grained evidence `supports` mappings for generated interfaces and
  compatibility claims.
- Prefer deterministic evidence such as package manifests, exports, public
  interface indexes, analyzer output, and digests.
- Keep model output as bounded review evidence only.

Out of scope:

- Running package scripts, dependency installation, or repository runtime code.
- Accepting packages into SpecPM automatically.
- Treating LM Studio or any model output as registry authority.
- Adding a new SpecPM schema version or registry acceptance decision format.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| `tests/test_collector.py` or drafter-focused tests | Cover subject-focused summary generation from package manifests and exports. | Generated summaries no longer default to producer-centric wording when subject metadata exists. |
| Drafter evidence tests | Verify interface and compatibility evidence targets. | Evidence supports include generated interface IDs and compatibility targets. |
| Candidate bundle or SpecPM integration fixture tests | Validate a generated preview package still passes SpecPM validation. | Candidate remains `preview_only` and validates. |
| Docs contract tests | Keep P24 documentation visible in Flow artifacts. | P24-T1 acceptance stays documented. |

## Implementation Plan

### Phase 1. Current Output Audit

Inputs: current drafter, collector outputs, candidate fixtures, and existing
`xyflow.core` review notes.

Actions:

- Locate the functions that build `specpm.yaml`, BoundarySpec summaries,
  interfaces, compatibility, and evidence.
- Identify current evidence target names for `interfaces.*` and
  `compatibility.*`.
- Capture the smallest test fixture that reproduces shallow producer-centric
  output.

Outputs: failing tests that describe desired P24 behavior.

Verification: targeted tests fail before implementation for the intended reason.

### Phase 2. Deterministic Draft Improvements

Inputs: package manifests, public interface indexes, analyzer reports, and
existing harvested metadata.

Actions:

- Generate subject-focused summaries from package description/name/export
  evidence before falling back to producer-centric text.
- Add deterministic interface evidence support targets for generated
  `interfaces.inbound` entries.
- Add compatibility evidence support targets or downgrade unsupported
  compatibility to explicit ecosystem hints.
- Preserve `preview_only` and all producer receipt/review boundaries.

Outputs: updated drafter behavior and focused tests.

Verification: targeted tests pass and generated candidate output remains valid.

### Phase 3. Validation and Documentation

Inputs: implemented behavior and Flow quality gates.

Actions:

- Update docs only where the new behavior changes author/operator expectations.
- Run configured gates from `.flow/params.yaml`.
- Record exact command results in `P24-T1_Validation_Report.md`.

Outputs: validation report and archived task artifacts.

Verification: full local gates pass with coverage at or above 90%.

## Acceptance Criteria

- A generated package such as `xyflow.core` can still validate as a SpecPM
  preview package.
- Manifest and BoundarySpec summaries describe the target package boundary
  rather than primarily describing SpecHarvester.
- Generated `interfaces.inbound` entries have deterministic evidence support
  targets.
- Compatibility claims are evidence-backed or explicitly represented as
  ecosystem hints instead of unsupported guarantees.
- BoundarySpec evidence `supports` entries cover capabilities, interfaces, and
  compatibility at useful granularity.
- No package scripts, dependency installation, runtime behavior claims, or
  model-authored direct file mutation is introduced.

## Notes

- If implementation reveals that compatibility target names need a stable
  vocabulary, keep the initial change local and add a follow-up task rather than
  expanding this task into a schema redesign.
- Any model review output must remain review evidence only and must not be used
  to directly rewrite generated files.
