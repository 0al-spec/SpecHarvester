# P37-T8 Harvest Manifest Evidence for Repository Profile Detection

## Motivation

P37-T7 showed a real FastMCP gap in the generic repository profile selection
layer: `harvest.json` recorded `pyproject.toml` as a package manifest, but
`workspace-inventory.json` recorded no package manifests. Because autonomous
batch profile detection only used workspace inventory evidence, auto-selection
fell back to `generic.repository.v0` despite available static manifest
evidence.

The fix should improve generic evidence routing, not create a FastMCP,
Python, or framework-specific profile.

## Goal

Make repository profile detection consume harvested package manifest evidence
when workspace inventory has no manifest records.

The detector should still use the same language- and framework-agnostic model:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

## Deliverables

- Update autonomous candidate batch repository profile detection input
  construction so harvested package manifest paths can supplement empty
  workspace inventory manifest evidence.
- Preserve existing high-confidence workspace and single-package behavior.
- Preserve fallback behavior for ambiguous, nested-only, low-confidence, and
  disabled profile selection scenarios.
- Add regression tests proving a root harvested manifest can drive
  `generic.single_package.v0` selection when workspace inventory is empty.
- Update GitHub docs and DocC to describe the harvested-manifest fallback
  path.
- Record validation and archive the task through Flow.

## Acceptance Criteria

- A repository with empty workspace inventory but harvested root package
  manifest evidence can auto-select `generic.single_package.v0` with high
  confidence.
- The generated `repository-profile-detection.json` records the harvested
  manifest path as evidence.
- Disabled profile selection remains `decision: disabled`.
- Ambiguous or nested-only manifest evidence still falls back when it cannot
  identify one high-confidence repository profile.
- The implementation does not hardcode FastMCP, Python, `pyproject.toml`, or
  any framework as normative.
- Documentation states that harvested manifest evidence remains producer-side
  evidence and is not registry truth.

## Non-Goals

- Do not implement ecosystem-specific repository profiles.
- Do not change package-set drafting semantics.
- Do not execute package managers, install dependencies, run repository code,
  perform network discovery, invoke AI, or clone/fetch repositories.
- Do not accept packages, accept relations, publish registry metadata, remove
  `preview_only`, or promote generated candidates into SpecPM.

## Dependencies

- P37-T4 autonomous candidate batch sidecar integration.
- P37-T7 real FastMCP comparison and `follow_up_required` finding.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
