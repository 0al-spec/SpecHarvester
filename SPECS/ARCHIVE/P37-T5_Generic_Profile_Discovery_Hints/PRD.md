# P37-T5 Generic Profile Discovery Hints

## Motivation

P37-T4 records repository profile selection as producer-side evidence, but the
hint vocabulary is still informal. Future profiles need a stable way to say
"this path looks like an example package" or "this path looks like the primary
package" without turning that hint into package acceptance or registry truth.

This task defines the generic hint vocabulary before adding ecosystem-specific
profiles or changing drafting behavior.

## Goal

Define a versioned, language- and framework-agnostic vocabulary for repository
profile discovery hints.

The vocabulary must cover:

- package-set root;
- member package;
- meta package;
- primary package;
- CLI package;
- bridge package;
- plugin package;
- example package;
- test package;
- documentation source;
- generated artifact;
- internal utility;
- evidence-only source.

## Deliverables

- Add a small domain module for generic repository profile discovery hints.
- Add a machine-readable fixture for the vocabulary.
- Make existing repository profile detection hints use canonical hint ids.
- Reject accidental unknown built-in hint ids in current hint emission code.
- Document the vocabulary in GitHub docs and DocC.
- Link the vocabulary from docs index, DocC root, capabilities, roadmap, and
  repository profile selection docs.
- Add regression tests for the fixture, vocabulary shape, existing detection
  output, and documentation links.
- Archive the task through Flow.

## Acceptance Criteria

- A fixture exists at:
  `tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json`.
- The fixture uses:
  - `apiVersion: spec-harvester.repository-profile-hints/v0`;
  - `kind: SpecHarvesterRepositoryProfileHintVocabulary`;
  - `schemaVersion: 1`;
  - `authority: producer_profile_hint_vocabulary_only`.
- The fixture contains exactly the 13 generic hint ids listed in the goal.
- Each hint records:
  - stable `hint`;
  - `title`;
  - `pathSubject`;
  - `summary`;
  - `consumerAction`;
  - `nonAuthorityStatements`.
- Current detection output still emits existing hints:
  `package_set_root`, `member_package`, and `documentation_source`.
- Unknown current hint ids are rejected by the hint construction path.
- Documentation explicitly states that hints are advisory producer evidence
  only and do not accept packages, accept relations, remove `preview_only`, or
  publish registry metadata.

## Non-Goals

- Do not implement ecosystem-specific profile plugins.
- Do not change package-set drafting semantics.
- Do not apply hints to candidate selection, relation acceptance, or registry
  publication.
- Do not clone/fetch repositories, install dependencies, execute harvested
  code, invoke package managers, or run AI.
- Do not treat profile hints as registry truth.

## Dependencies

- P37-T1 repository profile selection contract.
- P37-T2 detection fixture format.
- P37-T3 detection CLI/report surface.
- P37-T4 autonomous batch sidecar evidence integration.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift build --target SpecHarvesterDocs`
