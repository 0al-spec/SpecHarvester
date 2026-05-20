# P10-T5 Language-Neutral Semantic Extraction

Status: In Progress
Created: 2026-05-20
Task: `P10-T5` Add language-neutral semantic extraction for
documentation-first repositories so README/API-contract evidence can produce
meaningful intent clusters even when no supported package manifest is present.

## Problem

SpecHarvester can already derive stronger semantic intent for some Swift and
iOS repositories, but documentation-first or manifest-poor repositories still
fall back to generic public repository metadata. That is weak for repositories
whose public value is documented through README files, API contracts, schema
references, workflow descriptions, or command/tooling guides.

## Goals

- Extract compact, deterministic language-neutral semantic hints from
  allowlisted Markdown documentation without storing raw document bodies in
  `harvest.json`.
- Add language-neutral semantic cluster rules for API contracts, schema
  validation, workflow automation, developer tooling, and documentation
  knowledge bases.
- Allow `draft` to use semantic evidence as the fallback capability/intent
  source when no supported package manifest exists.
- Preserve evidence paths and semantic cluster details in generated
  BoundarySpec evidence.
- Keep generated intent claims advisory and reviewable.

## Non-Goals

- Do not use LLM inference for semantic extraction.
- Do not fetch remote documentation.
- Do not execute repository code, package managers, package scripts, build
  systems, dependency installers, or network probes.
- Do not store full README/API-document bodies in the harvest snapshot.
- Do not make language-neutral semantic clusters registry authority.

## Proposed Shape

- Extend Markdown collection with bounded `semanticHints`, derived from a
  curated list of language-neutral phrases.
- Feed `semanticHints` into the existing deterministic semantic profile builder.
- Add language-neutral `SemanticDomainRule` entries with no required language
  context.
- Update fallback capability generation so `semantic_profile.intent_ids` are
  used when no package manifest exists.
- Document the evidence contract in GitHub docs and DocC.

## Acceptance Criteria

- A documentation-only repository with README/API-contract evidence produces a
  semantic profile and non-generic intent ids during `draft`.
- The generated BoundarySpec includes `semantic_intent_static_evidence` with
  semantic clusters and evidence paths.
- Existing package-manifest semantic behavior remains compatible.
- `harvest.json` remains bounded and stores compact semantic hints rather than
  raw documentation bodies.
- Tests cover collector hints, docs-only semantic drafting, and docs contracts.

## Validation Plan

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
