# Next Task: P36-T3 Plugin-Aware Source Classification Hook

**Status:** In Progress
**Phase:** Phase 36. Repository Parsing Plugin System
**Task:** `P36-T3` Implement plugin-aware source classification hook
**Branch:** `feature/P36-T3-plugin-aware-source-classification-hook`
**Last Archived:** P36-T2 Python Web-Framework Parser Profile Fixture

## Recently Archived

- `P36-T2` added
  `tests/fixtures/repository_parsing_profiles/python-web-framework-v0.example.json`.
- The fixture defines `SpecHarvesterRepositoryParsingProfile` with
  `apiVersion: spec-harvester.repository-parsing-profile/v0`,
  `schemaVersion: 1`, and `authority:
  producer_path_classification_profile_only`.
- The profile id is `python.web_framework.v0`.
- It uses the P36-T1 decision contract:
  `SpecHarvesterRepositoryParsingPluginDecision` with `apiVersion:
  spec-harvester.repository-parsing-plugin/v0` and `authority:
  producer_path_classification_only`.
- It records rule precedence:
  `operator_override`, `selected_parser_profile_rule`,
  `language_package_manager_rule`, `generic_repository_classifier_rule`, and
  `conservative_default_fallback`.
- It classifies `fastapi/applications.py` as `public_interface`,
  `docs_src/first_steps/tutorial001.py` as `semantic_usage`, and
  `tests/test_applications.py` as `test`.
- It keeps documentation, tutorials, examples, and tests out of public
  interface evidence by default while preserving semantic usage evidence where
  useful.
- The non-authority boundary remains explicit: the fixture does not publish
  registry metadata, does not accept packages or relations, does not remove
  `preview_only`, and does not treat AI output as registry truth.

## Context

P36-T1 defined the plugin contract and P36-T2 added the first parser profile
fixture. P36-T3 should now add the first plugin-aware source classification
hook so collection/analyzer code can consume parser profile decisions in an
opt-in, backwards-compatible way.

## Motivation

- Make the Python web-framework profile executable by the pipeline.
- Keep default analyzer behavior backwards-compatible when no parser profile
  is selected.
- Avoid hardcoding FastAPI-specific path exclusions in core analyzer code.

## Goal

Implement the first plugin-aware source classification hook.

## Proposed Scope

- Add a small parser profile loader/decision helper for the fixture shape.
- Add deterministic path classification for selected profiles.
- Keep parser profile use opt-in.
- Wire the hook only far enough for tests to prove path role decisions can be
  produced and consumed safely; avoid broad behavior changes.
- Add regression coverage for FastAPI-like paths.

## Acceptance

- No parser profile selected means current behavior remains unchanged.
- Selecting `python.web_framework.v0` can classify FastAPI-like package,
  `docs_src`, docs, examples, tests, generated, tooling, internal, and fallback
  paths.
- Decisions preserve `publicInterfaceEligible` and `semanticUsageEligible`.
- The hook does not clone/fetch repositories, install dependencies, execute
  harvested code, publish registry metadata, accept packages or relations,
  remove `preview_only`, or treat AI output as registry truth.
