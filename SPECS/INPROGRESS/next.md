# Next Task: P55-T4 Provider-Neutral Semantic Author Pass

**Priority:** P0
**Phase:** Phase 55. Evidence-Grounded AI Semantic Authoring
**Dependencies:** `P55-T3` Semantic Author Input Pack
**Status:** Selected
**Branch:** `feature/P55-T4-provider-neutral-semantic-author-pass`

## Objective

Implement the provider-neutral semantic author pass with Codex 5.3 Spark as the
primary worker and LM Studio as a comparison provider.

## Required Scope

Consume only P55-T3 bounded packs and emit the P55-T2 proposal contract. Let a
provider refine purpose, propose package-owned capabilities, reuse observed
intents, or propose visibly experimental intents with evidence, nearby intents,
and non-goals. Preserve provider-neutral authority, bounded budgets, and
proposal-only output; do not materialize candidates or mutate SpecPM.

## Recently Archived

- `P55-T3` Semantic Author Input Pack: PASS. Deterministic bounded packs now
  bind allowlisted candidate YAML, harvest metadata, optional public-interface
  evidence, documentation as untrusted data, and observed intents without any
  provider execution.
- `P55-T2` AI Semantic-Author Schemas: PASS. Provider-neutral JSON Schema and
  deterministic cross-record checks now define evidence-bound requests,
  proposals, observed-intent reuse, experimental intents, reviewer edits, and
  future proposal-only materialization decisions without provider execution.
- `P55-T1` AI Semantic-Author Product and Authority Contract: PASS. Codex 5.3
  Spark and LM Studio now share one evidence-grounded proposal contract; models
  may propose observed-intent reuse or visibly experimental intents, while
  explicit reviewer decisions and separate SpecPM governance retain acceptance,
  canonicalization, materialization, and publication authority.
- `P54-T10` Phase 54 Exit Decision: PASS. Local maintainer Workbench use and the
  bounded proposal-only Phase 55 semantic-authoring follow-up are authorized;
  automatic acceptance, canonical intent creation, registry mutation,
  publication, remote multi-user deployment, and broader-corpus execution
  remain unapproved.
- `P54-T9` Workbench End-to-End Validation: PASS. The full 100-candidate corpus
  and all four 25-candidate waves were accounted for; representative decisions,
  restart and portable exchange, fail-closed integrity scenarios, hostile
  content containment, desktop/mobile usability, and one read-only SpecPM
  preflight passed with zero registry mutations.
- `P54-T8` SpecPM Intake Bridge: PASS. Current reviewer-approved candidates now
  pass archive, catalog, packet, decision-history, and decision-digest
  revalidation before bounded read-only SpecPM validation; proposal evidence
  remains `preview_only`, non-authoritative, and records zero registry
  mutations.
- `P54-T7` Reviewer Actions and Portable Decision Exchange: PASS. The local
  Workbench now records four reason-validated reviewer dispositions, preserves
  immutable replacement history, reconciles corpus progress after restart, and
  imports or exports digest-bound evidence with zero registry mutations.
- `P54-T6` Local Review-Decision Service and Storage Contract: PASS. Catalog-bound
  decisions now use atomic current-state writes, immutable digest history,
  optimistic replacement checks, restart validation, and a loopback
  Origin/CSRF-protected service boundary.
- `P54-T5` Candidate Detail Review Surface: PASS. The local browser now opens
  schema-valid, digest-bound provenance, generated-file, diagnostics, and
  proposal-only static-versus-Codex Spark detail evidence for all 100 candidates.
- `P54-T4` Local Candidate Browser: PASS. A local static candidate-only browser
  now provides corpus summary, facets, search, sorting, and a resumable queue.
- `P54-T3` Deterministic Local Candidate Review Catalog: PASS. The bounded
  generator verified all 100 portable packets and emitted a stable,
  schema-valid catalog with digest bindings and six review facets.
- `P54-T2` Local Candidate Review Workbench Schemas: PASS. Six versioned
  Workbench records now bind candidate state and decisions to P53-T14 packet
  digests while preserving portable evidence-only authority.
- `P54-T1` Local Candidate Review Workbench Product Contract: PASS. Product
  scope, roles, trust zones, portable input, decision lifecycle, hostile-content
  controls, and read-only SpecPM boundary are fixed before implementation.
- `P53-T15` Phase 53 Exit Decision: PASS. Phase 53 is complete and all 100
  portable candidates are available for maintainer disposition; larger-corpus,
  higher-concurrency, automatic-acceptance, and registry-promotion paths remain
  unapproved.
- `P53-T14` Portable Author Handoff and SpecPM Intake Preflight: PASS. All 100
  selected repositories have portable preview candidates and digest-bound
  packets; SpecPM consumer preflight passed with zero errors and warnings.
- `P53-T13` Campaign Quality Triage: PASS. Exactly 100 frozen repositories were
  accounted for once; all effective outcomes met quality thresholds and were
  selected for author review. Two bounded corrections remain explicit in the
  audit trail.
