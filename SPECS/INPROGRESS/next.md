# Next Task: P36-T2 Python Web-Framework Parser Profile Fixture

**Status:** In Progress
**Phase:** Phase 36. Repository Parsing Plugin System
**Task:** `P36-T2` Add Python web-framework parser profile fixture
**Branch:** `feature/P36-T2-python-web-framework-parser-profile`
**Last Archived:** P36-T1 Repository Parsing Plugin Contract

## Recently Archived

- `P36-T1` added
  [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](../../docs/REPOSITORY_PARSING_PLUGIN_CONTRACT.md)
  and the DocC mirror `RepositoryParsingPluginContract`.
- The contract defines `SpecHarvesterRepositoryParsingPluginDecision` with
  `apiVersion: spec-harvester.repository-parsing-plugin/v0`,
  `schemaVersion: 1`, and `authority:
  producer_path_classification_only`.
- It separates `public_interface` evidence from `semantic_usage`,
  `documentation`, `example`, `test`, `generated`, `tooling`, `internal`, and
  `ignored` path roles.
- It uses the FastAPI `docs_src/*` over-capture as the motivating case while
  keeping the future Python web-framework parser profile reusable rather than
  repository-specific.
- The non-authority boundary remains explicit: plugin decisions do not publish
  registry metadata, do not accept packages or relations, do not remove
  `preview_only`, and do not treat AI output as registry truth.

## Context

P36-T1 defined the contract. P36-T2 should now turn that contract into a
machine-readable fixture for Python web frameworks. The fixture should describe
how FastAPI-style repositories classify package code as public interface
evidence while classifying docs, tutorials, examples, and tests as semantic
usage evidence unless a plugin rule explicitly promotes a path.

## Motivation

- Make the plugin contract concrete enough for implementation.
- Prevent future Python analyzer changes from hardcoding FastAPI-specific
  paths in core logic.
- Preserve documentation/tutorial usefulness for LLM enrichment without
  inflating public API symbol counts.

## Goal

Add a machine-readable Python web-framework parser profile fixture.

## Proposed Scope

- Define the fixture shape and example profile id.
- Include path role rules for package roots, docs, `docs_src`, examples,
  tests, generated artifacts, tooling, internal paths, and fallback behavior.
- Include sample decisions for FastAPI-like paths.
- Link the fixture from the plugin contract docs and DocC mirror.
- Add docs-contract regression coverage.

## Acceptance

- The fixture uses the P36-T1 contract vocabulary.
- FastAPI package code is public interface eligible.
- `docs_src`, tutorials, examples, and tests are semantic usage or
  non-public-interface evidence by default.
- The fixture remains producer-side review evidence only and does not publish
  registry metadata, does not accept packages or relations, does not remove
  `preview_only`, and does not treat AI output as registry truth.
