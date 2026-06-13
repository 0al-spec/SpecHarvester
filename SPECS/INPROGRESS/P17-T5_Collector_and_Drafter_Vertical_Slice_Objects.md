# P17-T5 Collector and Drafter Vertical Slice Objects

Status: Planned
Phase: Phase 17. Elegant Objects Refactoring Strategy
Owner: SpecHarvester draft generation track

## Objective

Refactor one narrow collector/drafter behavior slice behind a small
behavior-rich object while preserving generated candidate package output.

This task starts with the single-package drafter artifact-writing path. It
does not change repository profiling, license inference, semantic evidence,
intent profile selection, capability assembly, or package-set drafting.

## Motivation

`draft_spec_package` currently builds package metadata, boundary spec content,
evidence references, producer reports, quality reports, and producer receipts
in one procedural body. That makes future changes risky because content
decisions and bundle materialization are interleaved.

The first safe vertical slice is candidate bundle output materialization:
directory creation, bundled harvest snapshot materialization, optional public
interface index output, manifest/spec writing, producer reports, quality report,
receipt emission, and final CLI-compatible result assembly. This behavior is
already covered by mature characterization tests, so it can move behind a named
object without changing the generated contract.

## Deliverables

- Add a small behavior-rich drafter object for single-package candidate bundle
  materialization.
- Keep `DraftOptions` and `draft_spec_package(options)` as the public API.
- Preserve generated files and report paths:
  - `specpm.yaml`;
  - `specs/*.spec.yaml`;
  - `harvest.json`;
  - `public-interface-index.json` when present;
  - `validation-report.json`;
  - `diagnostics.json`;
  - `author-ready-draft-quality-report.json`;
  - `producer-receipt.json`.
- Preserve producer receipt outputs, roles, digests, validation record,
  diagnostics record, author-ready summary, and result payload fields.
- Add direct characterization coverage for the new object seam.
- Update Flow validation, archive, and review artifacts.

## Acceptance Criteria

- Existing `draft_spec_package` tests pass without generated contract changes.
- The new drafter object constructor performs no filesystem access, subprocess
  execution, network access, package installation, or repository imports.
- All filesystem writes happen through explicit behavior methods.
- `producer-receipt.json` remains excluded from receipt `outputs[]`.
- Optional public interface index behavior remains unchanged.
- Coverage remains at or above 90%.

## Test-First Plan

1. Add object-level characterization that writes a minimal draft bundle through
   the new object and asserts the same output roles, report paths, receipt
   exclusion rule, and author-ready summary behavior.
2. Keep existing `draft_spec_package` tests as public API characterization.
3. Run focused drafter tests before full validation.

## Implementation Plan

### Phase 1: Candidate Bundle Output Object

Inputs:

- assembled manifest payload;
- assembled boundary spec payload;
- original harvest snapshot path;
- optional public interface index payload;
- package identity and generation options.

Outputs:

- a deterministic candidate bundle on disk;
- producer validation, diagnostics, author-ready quality report, and receipt;
- the same result payload currently returned by `draft_spec_package`.

Verification:

- object-level characterization passes;
- existing draft tests pass unchanged.

### Phase 2: Compatibility Wrapper

Inputs:

- existing `draft_spec_package(options)` call sites.

Outputs:

- `draft_spec_package` delegates materialization to the object after preserving
  current manifest/spec assembly logic.

Verification:

- public API tests and package-set/autonomous batch tests continue to pass.

### Phase 3: Flow Validation

Inputs:

- Flow quality gates;
- procedural-style and architecture-lint advisory checks for the drafter slice.

Outputs:

- validation report;
- archived task artifacts;
- review report.

Verification:

- focused drafter tests;
- full pytest;
- ruff check and format check;
- coverage gate;
- Swift docs build and static DocC generation.

## Non-Goals

- Do not alter generated package summaries, capabilities, intents, constraints,
  evidence, provenance, compatibility, or keywords.
- Do not refactor collector repository profiling or license inference in this
  task.
- Do not change package-set drafting, handoff, autonomous batch, SpecPM
  preflight, or SpecNode refinement contracts.
- Do not change producer receipt, validation report, diagnostics report, or
  author-ready quality report schemas.
