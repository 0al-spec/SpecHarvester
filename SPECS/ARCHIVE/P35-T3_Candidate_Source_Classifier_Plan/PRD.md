# P35-T3 Candidate Source Classifier Plan

## Summary

Document the candidate source classifier plan for Phase 35.

P35-T2 defined `SpecHarvesterCorpusPlan`, but the plan still needs a stable
classification vocabulary for package-like source units before drafting.
P35-T3 defines how future tooling should distinguish package-set roots,
primary packages, plugins, examples, tooling, type-only packages, generated
artifacts, internal utilities, deprecated sources, and evidence-only units.

## Motivation

- Corpus plans can select repositories and package families, but repository
  internals still contain package-like units that should not all become primary
  SpecPM candidates.
- Without a classifier plan, autonomous drafting can accidentally promote
  examples, internal utilities, generated artifacts, or type-only packages.
- The classifier needs explicit reason codes so later corpus reports can
  explain why a source was selected, deferred, excluded, or evidence-only.

## Deliverables

1. Add a GitHub docs page for the candidate source classifier plan.
2. Add a DocC mirror.
3. Define source classes, allowed actions, classifier inputs, output shape,
   reason codes, override policy, and non-authority boundary.
4. Add a machine-readable example fixture showing classification decisions.
5. Link the plan from corpus plan docs, capabilities, roadmap, and DocC root.
6. Add regression coverage for fixture shape and doc links.

## Classifier Scope

The plan should define:

- source classes:
  - `package_set_root`;
  - `primary_package`;
  - `plugin_package`;
  - `example_package`;
  - `tooling_package`;
  - `types_only_package`;
  - `generated_artifact`;
  - `internal_utility`;
  - `deprecated_source`;
  - `evidence_only`;
- actions:
  - `select_primary`;
  - `select_member`;
  - `defer`;
  - `exclude`;
  - `include_as_evidence_only`;
- inputs:
  - corpus plan source entries;
  - repository source manifests;
  - workspace inventory;
  - package manifests;
  - static evidence paths;
  - explicit operator overrides;
- output:
  - source id;
  - package-like unit id;
  - class;
  - action;
  - reason codes;
  - evidence paths;
  - confidence;
  - stop conditions.

## Acceptance Criteria

- The plan explains which classes may become primary candidates and which must
  remain deferred, excluded, or evidence-only.
- The plan is ecosystem-neutral and works for monorepos and single-package
  repositories.
- The fixture includes at least one primary package, package-set root, plugin,
  example, tooling, type-only, generated, internal, deprecated, and evidence-only
  decision.
- The classifier plan remains a producer review artifact and does not accept
  packages, accept relations, remove `preview_only`, publish registry metadata,
  or execute harvested code.
- `P35-T4` remains the next planned task.

## Non-Goals

- No classifier implementation in this task.
- No autonomous batch run.
- No repository clone/fetch.
- No dependency installation.
- No harvested code execution.
- No SpecPM acceptance or registry publication.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- DocC static generation command from `.github/workflows/docs.yml`
