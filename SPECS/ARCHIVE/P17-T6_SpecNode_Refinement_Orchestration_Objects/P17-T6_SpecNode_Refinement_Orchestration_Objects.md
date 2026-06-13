# P17-T6 SpecNode Refinement Orchestration Objects

Status: Planned
Phase: Phase 17. Elegant Objects Refactoring Strategy
Owner: SpecHarvester SpecNode integration track

## Objective

Refactor one narrow SpecNode refinement orchestration slice behind a
behavior-rich object while preserving provider, validation, retry, and
unavailable-result contracts.

This task starts with the bounded retry orchestration path exposed by
`run_specnode_refinement_retry_orchestration`. It does not change model
provider APIs, semantic review schemas, retry directive schemas, validation
rules, prompt content, or fallback result payloads.

## Motivation

`specnode_refinement.py` remains the final Phase 17 procedural hotspot after
report, analyzer, collector, and drafter seams. The largest current top-level
function is `run_specnode_refinement_retry_orchestration`, which owns bundle
construction, preview plan construction, provider calls, semantic review calls,
retry directive creation, attempt record creation, final digest binding, and
run validation.

Moving that retry loop behind a named behavior object gives future SpecNode
work a stable seam while keeping the external function and JSON contracts
unchanged.

## Deliverables

- Add a small behavior-rich object for retry orchestration run construction.
- Keep `SpecNodeRefinementRetryOptions` and
  `run_specnode_refinement_retry_orchestration(options)` as the public API.
- Preserve:
  - retry run `kind`, `schemaVersion`, status vocabulary, and policy fields;
  - attempt record shape and digest bindings;
  - provider unavailable fallback behavior;
  - semantic review validation behavior;
  - retry directive construction and validation behavior;
  - final refinement and semantic review digest behavior.
- Add direct characterization coverage for the new object seam.
- Update Flow validation, archive, and review artifacts.

## Acceptance Criteria

- Existing SpecNode refinement smoke tests pass without output contract changes.
- The new object constructor performs no filesystem access, provider calls,
  network access, subprocess execution, package installation, or repository
  imports.
- Provider calls and filesystem reads happen through explicit behavior methods.
- `run_specnode_refinement_retry_orchestration(options)` delegates to the new
  object and preserves behavior.
- Coverage remains at or above 90%.

## Test-First Plan

1. Add object-level characterization that compares the new retry sequence
   object output with the existing wrapper output for an approve-without-retry
   path.
2. Keep existing retry orchestration tests unchanged as public API
   characterization.
3. Run focused SpecNode retry tests before full validation.

## Implementation Plan

### Phase 1: Retry Sequence Object

Inputs:

- `SpecNodeRefinementRetryOptions`;
- existing artifact bundle and preview plan builders;
- existing provider, reviewer, validation, directive, and attempt helpers.

Outputs:

- a `SpecNodeRefinementRetryRun` payload identical to the current wrapper
  output.

Verification:

- object-level characterization passes;
- existing retry orchestration tests pass unchanged.

### Phase 2: Compatibility Wrapper

Inputs:

- existing `run_specnode_refinement_retry_orchestration(options)` call sites.

Outputs:

- wrapper delegates to the retry sequence object.

Verification:

- public retry orchestration tests and live-smoke unit tests continue to pass.

### Phase 3: Flow Validation

Inputs:

- Flow quality gates;
- procedural-style and architecture-lint advisory checks for the SpecNode slice.

Outputs:

- validation report;
- archived task artifacts;
- review report.

Verification:

- focused SpecNode tests;
- full pytest;
- ruff check and format check;
- coverage gate;
- Swift docs build and static DocC generation.

## Non-Goals

- Do not change provider interfaces, model payload schemas, retry directive
  schema, semantic review schema, or validation error vocabulary.
- Do not change prompt content, prompt budgets, or excluded content policy.
- Do not change `run_specnode_refinement_smoke` in this task.
- Do not alter package drafting, candidate bundle, package-set, autonomous
  batch, or SpecPM handoff contracts.
