# P9-T1 Derive Semantic Intent Claims From Trusted Static Documentation and Public API Evidence

## Status

Planned

## Problem

Generated drafts currently produce technically valid but low-signal intent claims
such as `intent.swift.product.puzzlecore`. For repositories such as Puzzle and
SpecificationKit, static repository evidence contains a clearer purpose in DocC,
PRD, README, and public API names, but the draft generator does not use that
evidence when choosing capability intent IDs or summaries.

The collector can also include nested package manifests from generated
dependency checkouts, build products, test fixtures, and historical draft folders
as package interface evidence. Those files are useful as untrusted harvested data
only when explicitly reviewed, but they should not drive primary package intent
claims.

## Goals

- Prefer deterministic semantic intent IDs when static documentation or public
  API clusters provide clear domain signals.
- Keep Swift package product intent IDs as fallback claims for packages without
  stronger evidence.
- Filter generated/dependency/fixture/historical manifests out of primary
  package interface and intent derivation.
- Preserve local-first, no-execution, no-network trust boundaries.

## Non-Goals

- Do not call LLMs to infer repository intent.
- Do not execute SwiftPM, package scripts, dependency installers, or tests in
  harvested repositories.
- Do not promote generated candidates automatically.
- Do not attempt full natural-language understanding of arbitrary docs.

## Deliverables

- Deterministic semantic intent derivation in `draft` from allowlisted evidence.
- Primary package manifest filtering that ignores generated dependency checkout,
  build, fixture, and archived draft paths for capability/interface claims.
- Tests covering a Puzzle-like Swift package with PRD/DocC/public API evidence.
- Validation report with configured quality gate results.

## Acceptance Criteria

- A Puzzle-like fixture produces meaningful intent IDs such as screen
  composition, UIKit/SwiftUI migration, collection layout composition, or state
  binding instead of only `intent.swift.product.*`.
- A plain Swift package without richer semantic evidence still falls back to
  Swift product intents.
- Nested manifests under dependency/build/fixture/historical paths do not appear
  as primary inbound package interfaces.
- Existing governance and accepted-update tests continue to pass.

## Review Subject

`p9_t1_semantic_intent_drafting`
