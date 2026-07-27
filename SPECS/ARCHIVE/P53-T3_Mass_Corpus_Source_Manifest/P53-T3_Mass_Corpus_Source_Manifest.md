# P53-T3 Mass Corpus Source Manifest

**Status:** Planned
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Task:** `P53-T3`
**Depends On:** `P53-T1` Mass Corpus Operating Plan and `P53-T2` Resumable
Mass-Run Orchestration

## Objective

Create the immutable operator-curated source boundary for the Phase 53 campaign:
exactly 100 public GitHub repositories, assigned in a fixed order to four waves
of 25. The output is a repository manifest plus companion selection metadata.
It will let P53-T4 validate operator-provided checkouts without choosing,
substituting, or expanding sources at run time.

## Acceptance Criteria

- A dedicated `inputs/p53-mass-corpus/` directory contains a 100-entry source
  manifest and matching 100-entry selection metadata; no P52 identity is reused.
- Every entry records canonical HTTPS origin, full pinned revision, expected
  checkout under `../../../../P53Sources/`, package id, fixed wave, ecosystem,
  repository shape, importance signal, size ceiling, and discovery evidence for
  license and provenance.
- The metadata records selection timestamp and public GitHub metadata source,
  but labels checkout-dependent license and size facts as pending P53-T4
  verification rather than asserting a live readiness result.
- Contract tests prove exact cardinality, IDs and revisions, four 25-item waves,
  P52 separation, coverage quotas, required metadata, and no authority change.
- Documentation defines the handoff to P53-T4 and explicitly prohibits source
  acquisition, static collection, Codex invocation, and registry mutation.

## Test-First Plan

1. Add focused tests that load the planned manifest and metadata and reject a
   duplicate P52 source, missing pin, invalid wave, or collapsed coverage.
2. Capture public repository discovery metadata and generate the static,
   reviewable manifest and companion metadata from the selected records.
3. Add only the validator necessary to make the contract reusable by P53-T4;
   then update operator documentation and the validation report.

## Implementation Plan

1. Select a balanced, operator-curated public corpus with quotas for Python,
   TypeScript/JavaScript, Go, Rust, Java, C/C++, Swift, and multi-package or
   documentation-heavy repository shapes. Assign each selected identity to one
   immutable wave of 25.
2. Store the source pins and selection evidence. Set every checkout path to its
   expected P53 location, and retain only sanitized public metadata.
3. Implement tests and the small validation helper. Run focused and configured
   quality gates; record only sanitized results in the task validation report.

## Constraints And Non-Goals

- Do not create, restore, clone, fetch, or modify source checkouts. P53-T4 is
  the sole readiness decision for operator-provided checkouts.
- Do not run static harvesting, `codex exec`, LM Studio, adapters, package
  managers, or harvested code. Do not persist prompts, model responses,
  secrets, session state, stdout/stderr, or chain-of-thought.
- This task is proposal-only infrastructure. It cannot accept packages or
  relations, publish registry metadata, remove `preview_only`, or make P53-T5
  through P53-T15 pass.

## Notes

Update the Workplan, next-task pointer, archive index, and operator-facing
campaign documentation when the manifest has passed review.

---
**Archived:** 2026-07-27
**Verdict:** PASS
