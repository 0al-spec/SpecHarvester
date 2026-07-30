# P55-T7 Workbench Static-versus-AI Semantic Review

## Objective

Extend the local candidate review Workbench so a maintainer can compare static
candidate semantics with a complete portable AI semantic proposal and record an
explicit accept, edit, reject, or defer decision without materializing output.

## Dependencies

- P54-T5 candidate detail and static-versus-AI comparison records.
- P54-T6/T7 loopback decision service, immutable history, and portable exchange.
- P55-T2 reviewer-edit contract.
- P55-T6 complete portable semantic proposal records.

## Deliverables

- A deterministic semantic comparison projection for purpose, capability,
  interface, evidence, observed-intent reuse, and experimental-intent proposals.
- Structured Workbench panels that render static and AI content side by side as
  inert text and keep observed reuse visibly separate from experimental intent
  proposals.
- Reviewer controls for `accepted`, `edited`, `rejected`, and `deferred`
  semantic decisions, including bounded claim selection and optional edited
  claim text.
- A digest-bound `SpecHarvesterAISemanticReviewerEdit` embedded in the existing
  candidate decision history and portable exchange.
- Service-side validation that reviewer identity, claim IDs, edited text,
  proposal digest, source digest, and optimistic prior-decision binding match
  the selected candidate evidence.
- Updated schema, documentation, fixtures, and focused browser, detail, decision
  service, integrity, and hostile-content tests.

## Decision Contract

- The reviewer edit binds the candidate packet, portable semantic record,
  proposal, and source bundle digests.
- `accepted` and `edited` require at least one accepted or edited claim.
- `edited` requires bounded replacement text for at least one selected claim;
  other decisions cannot carry edits.
- Claim IDs and original evidence bindings must come from the complete portable
  proposal. Reviewer edits may replace claim text but cannot add evidence,
  change provider receipts, create canonical intents, or grant publication
  authority.
- The decision service computes the reviewer-edit digest and persists the
  resulting record within the existing immutable candidate decision chain.

## Acceptance Criteria

- A complete portable proposal produces a stable structured comparison for all
  required semantic areas.
- Workbench content uses DOM text nodes only; candidate and provider content is
  never interpreted as HTML, script, URL, or instruction.
- Each semantic action round-trips through loopback Origin/CSRF controls and
  survives export/import with exact digest bindings.
- Unknown or stale proposal, source, record, packet, or claim bindings fail
  closed.
- An AI proposal cannot submit a decision; only an explicit reviewer action with
  a non-empty reviewer identity can create one.
- Existing candidates without complete semantic records remain reviewable and
  cannot record a semantic decision.
- Full tests pass with at least 90% coverage; Ruff, formatting, diff, Swift
  manifest, and DocC checks pass.

## Non-Goals

- Candidate revision materialization, SpecPM mutation, or accepted-source
  changes.
- Canonical intent acceptance, registry mutation, or publication.
- Provider execution or P55-T9 quality calibration.
- Remote multi-user review or authentication beyond the existing loopback
  boundary.
