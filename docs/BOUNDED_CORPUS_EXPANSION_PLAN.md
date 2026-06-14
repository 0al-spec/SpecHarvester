# Bounded Corpus Expansion Plan

Status: Current plan for Phase 33 after the Phase 32 intake readiness decision.

This plan keeps the next autonomous candidate expansion bounded. The goal is
not to collect every popular framework into SpecPM. The goal is to run one
small, operator-selected local source manifest through the existing
SpecHarvester evidence pipeline and stop at reviewable producer evidence.

## Decision

`P33-T1` records the next expansion policy as
`SpecHarvesterBoundedCorpusExpansionPlan` with
`apiVersion: spec-harvester.bounded-corpus-expansion-plan/v0`.

The next expansion is allowed only after a source manifest exists. That
manifest must be local-only, pinned, reviewable, and small enough to inspect.

## Corpus Limit

The next corpus is capped at five repositories.

The count is intentionally small:

- it is larger than the original Flask/Gin/xyflow smoke corpus;
- it is still small enough for author-ready review and handoff inspection;
- it prevents the runner from becoming a broad framework crawler;
- it gives one batch enough diversity to include monorepo, single-package,
  documentation-heavy, and language-diverse repository shapes.

## Source Manifest Requirements

`P33-T2` must add the next-corpus source manifest fixture before any scrape
runs.

The manifest must define:

- repository identifiers;
- local checkout paths;
- pinned revisions;
- repository selection rationale;
- expected package shape, such as single package, package-set, scoped source
  unit, or documentation-heavy package;
- excluded repositories or duplicate shapes when relevant;
- no network discovery behavior.

The manifest must not allow clone, fetch, dependency installation, harvested
code execution, package scripts, or remote registry mutation.

## Gate Sequence

The next expansion has four gates:

1. Deterministic collection and draft gate.
2. Live local-model draft/enrichment gate with bounded JSON repair.
3. Candidate-layer triage gate.
4. SpecPM-side selected handoff preflight gate.

Each gate produces review evidence only. Passing a gate does not accept a
package, accept a relation, seed a baseline, remove `preview_only`, or publish
registry metadata.

## Stop Conditions

The run must stop when any of these conditions occur:

- the source manifest is missing or does not match the expected schema;
- a repository count exceeds five;
- a checkout path is missing, unpinned, remote, or outside the operator-approved
  local corpus;
- deterministic preflight fails;
- source digests drift between collection and handoff;
- package identity or package-set topology drifts;
- the local model provider is unavailable and no deterministic fallback policy
  applies;
- JSON repair exceeds its bounded retry policy;
- candidate-layer triage cannot classify a candidate as selected, deferred,
  blocked, or not-for-intake;
- SpecPM-side preflight reports errors or authority ambiguity.

## Author and Maintainer Handoff

The next-corpus result should stop at author/maintainer review evidence.

Author review answers whether the generated starter package accurately
describes the upstream repository. SpecPM maintainer review answers whether any
candidate can enter accepted registry sources. SpecHarvester does not make
either decision.

## Phase 33 Work Plan

### P33-T1 Bounded Corpus Expansion Plan

Owner: SpecHarvester.

Motivation:

- Phase 32 ended with a review-ready limited corpus and an explicit stop before
  broader autonomous scraping.
- The next expansion needs its own source manifest, repository count, gate
  sequence, stop conditions, and authority boundary.

Goal:

- Record the bounded expansion policy before any new scrape runs.

Acceptance:

- The plan caps the next corpus at five repositories.
- The plan requires a pinned local source manifest before collection.
- The plan defines deterministic, live-model, candidate-layer, and SpecPM
  preflight gates.
- The plan preserves the non-authority boundary.

### P33-T2 Next-Corpus Source Manifest Fixture

Owner: SpecHarvester.

Motivation:

- A bounded plan is not enough without a concrete manifest.
- The selected repositories must be inspectable before any runner touches them.

Goal:

- Add the next-corpus source manifest fixture with repository IDs, local
  checkout expectations, pinned revisions, and selection rationale.

Acceptance:

- The manifest contains no more than five repositories.
- Every entry has a pinned revision and local checkout requirement.
- The manifest has no network discovery, clone, fetch, install, or execute
  behavior.

Artifact:

- [`NEXT_CORPUS_SOURCE_MANIFEST.md`](NEXT_CORPUS_SOURCE_MANIFEST.md) records
  the P33-T2 fixture. The source manifest is
  `inputs/p33-next-corpus/repositories.yml`, and the companion fixture is
  `SpecHarvesterNextCorpusSourceManifestFixture` with
  `apiVersion: spec-harvester.next-corpus-source-manifest/v0`.

### P33-T3 Deterministic Next-Corpus Dry Run

Owner: SpecHarvester.

Motivation:

- Deterministic evidence should fail fast before any local model call is used.

Goal:

- Run collection and draft generation without AI and record candidate counts,
  preflight outcomes, and blocker classes.

Acceptance:

- Deterministic preflight passes or records exact blockers.
- The run records source digests and package shape decisions.
- The run stops before live AI if hard gates fail.

Artifact:

- [`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md)
  records the P33-T3 deterministic `--skip-ai` run. It processed all five
  repositories, produced five preview candidates, produced zero relation
  proposals, passed five bundle-set preflights, recorded package-id review
  signals for `mcpm-sh` and `specgraph`, and is ready for P33-T4 live
  local-model review.

### P33-T4 Live Local-Model Next-Corpus Dry Run

Owner: SpecHarvester.

Motivation:

- The author-ready starter package quality bar depends on bounded local-model
  draft/enrichment behavior, but model output must remain proposal evidence.

Goal:

- Run the next corpus through live local-model draft/enrichment with bounded
  JSON repair and provider receipts.

Acceptance:

- Provider receipts are recorded.
- JSON repair stays within bounded retry policy.
- AI output remains proposal-only and never registry truth.

### P33-T5 Next-Corpus Candidate-Layer Triage

Owner: SpecHarvester.

Motivation:

- The batch is useful only if each candidate receives a review state.

Goal:

- Produce selected, deferred, blocked, and not-for-intake decisions for the
  next corpus.

Acceptance:

- Selected candidates have required evidence roles and passing producer
  preflight.
- Deferred and blocked candidates remain visible with blocker codes.
- Not-for-intake candidates are recorded with rationale.

### P33-T6 Next-Corpus SpecPM Preflight and Intake Decision

Owner: SpecHarvester + SpecPM.

Motivation:

- SpecPM remains the downstream validation and registry authority.

Goal:

- Run or coordinate SpecPM-side preflight for the next-corpus selected handoff
  and record the intake readiness decision.

Acceptance:

- The SpecPM-side preflight result is linked.
- The readiness decision remains review evidence only.
- Any registry acceptance requires a separate SpecPM maintainer flow.

## Non-Authority Boundary

Phase 33 must not:

- clone repositories;
- fetch remote state;
- install dependencies;
- execute harvested repository code;
- run package scripts;
- publish SpecPM registry content;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth;
- create a SpecPM pull request unless a later trusted handoff task explicitly
  requests it.

## Fixture

The example policy fixture is:

`tests/fixtures/bounded_corpus_expansion_plan/p33-t1-bounded-corpus-expansion-plan.example.json`
