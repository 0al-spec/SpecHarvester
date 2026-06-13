# P17-T3 Report Builder Behavior Objects

Status: Planned
Phase: Phase 17. Elegant Objects Refactoring Strategy
Owner: SpecHarvester report-layer refactoring track

## Objective

Refactor one stable report builder behind behavior-rich report objects while
preserving its public output contract. The first P17-T3 slice targets
`accepted_diff.py` and the `SpecHarvesterAcceptedCandidateDiffReport` contract.

The goal is to move mature report-building decisions out of one large
procedural function chain without changing report schemas, issue codes, trust
boundary text, CLI flags, output formatting, or downstream imports.

## Motivation

P17-T2 moved selected CLI report execution bodies into command objects. The
next concentration is the report-builder layer: report modules already expose
stable JSON contracts, so they are a good place to introduce named domain
objects around comparison, summary, issue ordering, and report assembly.

`accepted_diff.py` is the lowest-risk first target because it already has
focused characterization tests and is reused by accepted impact and update
proposal flows. A narrow refactor here proves the object pattern before larger
governance and quality reports are touched.

## Deliverables

- Introduce behavior-rich accepted candidate diff report objects.
- Preserve existing public function names as compatibility wrappers:
  - `build_accepted_candidate_diff_report`;
  - `collect_package_diff_records`;
  - `build_candidate_comparison`;
  - `diff_records`;
  - `latest_accepted_by_package_id`;
  - `write_accepted_candidate_diff_report`.
- Add direct object-level characterization tests for the new report objects.
- Update EO refactoring documentation to record the completed P17-T3 report
  object slice.
- Add Flow validation, archive, and review artifacts.

## Acceptance Criteria

- `SpecHarvesterAcceptedCandidateDiffReport` JSON remains byte-shape stable for
  existing tests:
  - `schemaVersion`;
  - `kind`;
  - `status`;
  - `summary`;
  - `comparisons`;
  - `issues`;
  - `trustBoundary`.
- Existing issue codes remain unchanged:
  - `specpm_symlink`;
  - `invalid_specpm_manifest`.
- Existing comparison statuses remain unchanged:
  - `new_package`;
  - `changed`;
  - `unchanged`.
- Existing metadata, intent, capability, and upstream artifact diff semantics
  remain unchanged.
- CLI `accepted-candidate-diff-report` output behavior remains unchanged.
- Downstream modules that import accepted diff functions keep working without
  import changes.
- Coverage remains at or above 90%.

## Test-First Plan

1. Add tests that instantiate the new accepted diff report objects directly and
   assert the same report summary, comparison status, and issue behavior as the
   public wrapper.
2. Keep existing accepted candidate diff tests unchanged as public contract
   characterization.
3. Run focused accepted diff, accepted impact, accepted update proposal, docs
   contract, and full validation gates.

## Implementation Plan

### Phase 1: Object Seam

Inputs:

- current `build_accepted_candidate_diff_report`;
- current package diff record parsing and collection functions;
- current candidate comparison and diff helpers.

Outputs:

- an accepted candidate diff report object with a deterministic `report()`
  method;
- small collaborator objects for source collection, accepted-version selection,
  candidate comparison, and report writing where they reduce procedural
  concentration.

Verification:

- direct object tests pass;
- existing wrapper tests pass unchanged.

### Phase 2: Compatibility Wrappers

Inputs:

- public functions imported by CLI, accepted impact, and update proposal flows.

Outputs:

- wrappers delegate to objects while preserving function signatures and return
  payloads.

Verification:

- downstream focused tests pass without import changes;
- CLI writes the same JSON fields.

### Phase 3: Flow Validation

Inputs:

- `.flow/params.yaml` quality gates;
- EO refactoring strategy acceptance metrics.

Outputs:

- validation report;
- archived task artifacts;
- review report.

Verification:

- focused tests for accepted diff and downstream accepted reports;
- full pytest;
- ruff check and format check;
- coverage gate;
- Swift docs build when documentation is touched;
- architecture lint smoke for the touched report module.

## Non-Goals

- Do not change accepted candidate diff report schema.
- Do not change CLI parser flags, defaults, exit codes, or output formatting.
- Do not refactor accepted impact, governance reports, real repository quality
  reports, code duplication, architecture lint, or procedural-style reports in
  this PR.
- Do not change SpecPM, SpecNode, package-set, or autonomous batch contracts.
- Do not remove compatibility functions that downstream modules import.
