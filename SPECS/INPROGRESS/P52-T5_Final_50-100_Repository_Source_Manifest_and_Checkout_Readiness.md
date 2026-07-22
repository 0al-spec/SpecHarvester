# P52-T5 Final 50-100 Repository Source Manifest and Checkout Readiness

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T5`
**Depends On:** `P52-T4` Twenty-Repository Controlled Pilot

## Goal

Create the final operator-curated 50-100 repository source manifest and prove
that every selected source is an existing, clean, pinned local checkout before
any larger-corpus static or model gate can run.

## Deliverables

- Add a `read_repository_source_manifests` compatible manifest with 50-100
  unique repository ids, public repository URLs, exact revisions, checkout
  paths, package ids, and labels.
- Add companion selection metadata with provenance, license evidence, size
  budgets, ecosystem and repository-shape coverage, importance signals, and
  explicit inclusion/exclusion rationale.
- Add a deterministic readiness command and report fixture that rejects missing,
  dirty, mismatched, private, unlicensed, oversized, or unsupported sources.
- Record the selected corpus size, coverage distribution, stop-policy outcome,
  and proposal-only/no-authority boundary.
- Document the manifest, readiness result, and P52-T6 decision in Markdown and
  DocC with focused regression coverage.

## Acceptance Criteria

- The corpus contains at least 50 and at most 100 existing clean local Git
  checkouts. No source is cloned, fetched, restored, or modified.
- Each source uses an immutable revision, has a matching checkout HEAD, and has
  no staged, unstaged, or untracked content.
- Repository URLs are public, provenance and license evidence are explicit, and
  every source fits its recorded size budget.
- The readiness report records multiple ecosystems and repository shapes and
  rejects unresolved provenance, generated/vendor-only layouts, and sources
  that exceed stop-policy limits.
- Passing readiness unlocks P52-T6 only. It does not run static collection,
  LM Studio, Codex, adapters, package managers, or harvested code.
- No output accepts packages or relations, publishes registry metadata, seeds
  baselines, removes `preview_only`, or becomes registry truth.
- No raw prompts, raw provider responses, secrets, session state, or
  chain-of-thought are persisted.

## Non-Goals

- Do not run P52-T6 static collection, P52-T7 Codex Spark, output triage, or a
  Phase 52 exit decision.
- Do not obtain additional repositories automatically.

## Validation Plan

- Run focused source-manifest/readiness and documentation-contract tests.
- Validate durable JSON artifacts with `python -m json.tool`.
- Run Flow gates from `.flow/params.yaml`, including full pytest with coverage
  >=90%, Ruff, Swift package/DocC build, and `git diff --check`.
