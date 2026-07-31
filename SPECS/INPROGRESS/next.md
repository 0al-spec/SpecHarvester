# Next Task: P55-T10A Experimental-Intent Decision Policy

**Priority:** P0
**Phase:** Phase 55. Evidence-Grounded AI Semantic Authoring
**Dependencies:** `P55-T10` Retained-Corpus Semantic Author and Review Flow
**Status:** Ready

## Objective

Correct the semantic-author decision policy so Codex 5.3 Spark can propose a
bounded experimental intent when existing generic intents do not express the
evidence-backed user outcome.

## Required Scope

Use the P55-T10 result as the fixed baseline: all 48 generic static intent
references were reused and no `intent.experimental.*` proposal was emitted.
Require explicit nearby-intent comparison and evidence-grounded justification
for reuse versus novelty. Prevent forced novelty, synonyms, taxonomy leakage,
canonicalization, materialization, registry mutation, and publication. Produce
the implementation and fixtures needed to unblock P55-T10B targeted
calibration; P55-T11 remains blocked through P55-T10C.

## Recently Archived

- `P55-T10` Retained-Corpus Semantic Author and Review Flow: PASS. Codex 5.3
  Spark completed all 100 retained repositories without terminal provider
  failures and produced 42 portable proposals. Deterministic quality checks
  rejected 58 records; generic-intent reduction remained 0/48 and all records
  remain explicitly unreviewed, so P55-T11 must choose the bounded next step.
- `P55-T9A` Semantic Provider Output Conformance Follow-Up: PASS. Codex 5.3
  Spark and LM Studio each completed all four frozen targets and passed every
  unchanged gate. Provider outputs now use bounded structured conformance and
  repair while deterministic quality diagnostics and proposal-only authority
  remain intact; P55-T10 is unblocked.
- `P55-T9` Targeted Semantic Quality Calibration: PASS. Eight
  provider/target outcomes were accounted for against the frozen policy.
  Codex completed four schema-valid proposals but failed purpose and edit
  burden gates; LM Studio completed zero of four. Neither provider passed, so
  P55-T10 remains blocked.
- `P55-T8` Reviewer-Controlled Semantic Materialization: PASS. Explicit
  accepted or edited semantic decisions now create separate preview revisions
  with exact before/after provenance and SpecHarvester plus read-only SpecPM
  validation, without changing source candidates or registry truth.
- `P55-T7` Workbench Static-versus-AI Semantic Review: PASS. The Workbench now
  presents inert structured static-versus-AI semantic comparisons and records
  digest-bound accept, edit, reject, or defer evidence in the existing immutable
  reviewer decision history without materialization or publication authority.

- `P55-T6` Complete Portable Semantic Proposal Records: PASS. Complete
  proposals, deterministic quality reports, and allowlisted provider receipts
  now survive P53 handoff and P54 detail generation with candidate, source,
  proposal, receipt, quality, packet, and record digest bindings; raw provider
  data and all application or publication authority remain excluded.
- `P55-T5` Semantic Proposal Validation and Quality Diagnostics: PASS.
  Deterministic provider-neutral reports now distinguish eligible, review, and
  rejected proposals; enforce evidence, namespace, manifest/boundary, intent,
  wording, and quantitative-claim constraints; and bind the frozen P55-T9
  quality thresholds without granting materialization or publication authority.
- `P55-T4` Provider-Neutral Semantic Author Pass: PASS. Codex 5.3 Spark and
  local LM Studio now share a bounded P55-T2 semantic-proposal contract. The
  pass retains normalized proposal and receipt data only, validates evidence
  and observed-intent bindings, and has no materialization, SpecPM mutation,
  registry, or publication path.

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
