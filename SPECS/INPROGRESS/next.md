# Next Task: P36-T1 Repository Parsing Plugin Contract

**Status:** In Progress
**Phase:** Phase 36. Repository Parsing Plugin System
**Task:** `P36-T1` Document repository parsing plugin contract
**Branch:** `feature/P36-T1-repository-parsing-plugin-plan`
**Last Archived:** P35-T6 Selected Corpus Dry-Run Readiness

## Recently Archived

- `P35-T6` added
  [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](../../docs/SELECTED_CORPUS_DRY_RUN_READINESS.md)
  and the DocC mirror `SelectedCorpusDryRunReadiness`.
- The readiness fixture
  `tests/fixtures/selected_corpus_readiness/p35-t6-readiness.example.json`
  defines `SpecHarvesterSelectedCorpusReadinessReport` with `apiVersion:
  spec-harvester.selected-corpus-readiness/v0`, `schemaVersion: 1`, and
  `authority: producer_readiness_report_only`.
- Phase 35 completed the bounded curated corpus selection foundation and
  stopped before autonomous collection until selected repositories have
  verified pinned local checkouts.
- The readiness verdict was `blocked_pending_local_checkouts`, with selected
  sources blocked by `local_checkout_not_verified` until the downstream
  `autonomous-candidate-batch` gate can be rerun safely.

## Context

The FastAPI rerun with live local AI now produces a valid
`author_ready_draft`, but the Python public API analyzer over-captures
documentation tutorial files such as `docs_src/*` as public interface
evidence. Those files are valuable for intent and usage semantics, but they
should not inflate the package public API boundary.

This is not just a FastAPI detail. Repository layouts vary by language,
framework, and ecosystem. SpecHarvester needs a plugin-shaped parsing policy
layer so technology-specific rules can classify repository paths without
hardcoding every repository in the core analyzer.

## Motivation

- Keep documentation, tutorials, examples, and tests useful as semantic usage
  evidence for LLM enrichment and reviewer context.
- Keep `public_interface_index` focused on package surfaces intended for
  consumers.
- Avoid repository-specific one-off exceptions by defining a reusable
  language/framework parsing plugin contract.
- Preserve the SpecHarvester boundary: parser decisions are producer review
  evidence only, not registry acceptance.

## Goal

Document the repository parsing plugin contract before implementation.

The contract should define:

- plugin inputs: source manifest metadata, repository checkout path, detected
  ecosystem/package layout, candidate package id, and analyzer plans;
- plugin outputs: path classifications and evidence roles such as
  `public_interface`, `semantic_usage`, `documentation`, `example`, `test`,
  `generated`, `tooling`, `internal`, and `ignored`;
- rule precedence and fallback behavior when no plugin matches;
- how plugin decisions are recorded as review evidence;
- safety/non-authority boundaries.

## Proposed Scope

- Add GitHub Markdown and DocC documentation for the parsing plugin contract.
- Use FastAPI `docs_src` over-capture as the motivating example.
- Define a future Python web-framework parser profile as the first intended
  implementation target.
- Update capabilities/roadmap/workplan references.
- Add docs-contract regression coverage.

## Acceptance

- The contract clearly separates public API evidence from semantic
  usage/documentation evidence.
- The FastAPI case is framed as a Python web-framework profile, not a
  repository-specific special case.
- The contract explains how future plugins can support language and technology
  rules without broad crawler behavior.
- The non-authority boundary is explicit: plugin decisions do not publish
  registry metadata. The task does not publish registry metadata, does not
  accept packages or relations, does not remove `preview_only`, and does not
  treat AI output as registry truth.
