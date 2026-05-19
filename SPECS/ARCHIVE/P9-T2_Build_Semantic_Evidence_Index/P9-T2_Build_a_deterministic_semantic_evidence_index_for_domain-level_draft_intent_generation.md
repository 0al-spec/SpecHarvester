# P9-T2 Build a Deterministic Semantic Evidence Index for Domain-Level Draft Intent Generation

## Status

Planned

## Problem

`P9-T1` improved drafts when a repository matches explicit iOS screen-composition
signals, but smoke testing `SpecificationKit` showed the next gap: the collector
harvests rich README and DocC evidence, yet the drafter receives it mostly as a
flat heading corpus. That is insufficient for weak-model or deterministic
generation of domain-level claims such as specification pattern, predicate
composition, context-driven decisioning, feature gating, reactive evaluation,
and tracing.

## Goals

- Build a deterministic `SemanticEvidenceIndex` from allowlisted static evidence.
- Normalize repository terms into ranked domain clusters with evidence paths.
- Feed the drafter compact domain clusters rather than raw heading bags.
- Generate better SpecificationKit-like intent claims without LLM inference.
- Preserve preview-only and no-execution trust boundaries.

## Non-Goals

- Do not execute harvested repository code, package scripts, dependency
  installers, tests, or network probes.
- Do not call LLMs for intent inference.
- Do not design an open-ended taxonomy for all programming domains.
- Do not automatically promote generated candidates.

## Deliverables

- Deterministic semantic evidence indexing utilities.
- Drafter integration that prefers ranked domain clusters when available.
- SpecificationKit-like tests covering specification pattern, predicate
  composition, context-driven decisioning, feature gating, reactive evaluation,
  and tracing.
- Validation report with configured quality gates and local smoke evidence.

## Acceptance Criteria

- A SpecificationKit-like fixture produces domain-level intents instead of only
  `intent.swift.macro_developer_experience`.
- Domain clusters include stable IDs, scores/counts, matched terms, and evidence
  paths.
- Existing Puzzle/iOS screen intent behavior remains intact.
- Plain Swift packages without rich semantic evidence still fall back to Swift
  product intents.
- Generated evidence remains reviewable and does not execute untrusted content.

## Review Subject

`p9_t2_semantic_evidence_index`
