# P55-T1 AI Semantic-Author Product and Authority Contract

## Objective

Define the product, authority, evidence, provider, reviewer, and trust contract
for evidence-grounded AI semantic authoring before schemas, input packs,
provider execution, validation, portable proposals, Workbench comparison, or
materialization are implemented.

## Dependencies

- P54-T10 exit decision authorizing the bounded proposal-only Phase 55
  follow-up.
- P54 Workbench inert-content, decision, and read-only SpecPM boundaries.
- Existing SpecPM observed intent metadata and author freedom to submit
  well-formed non-canonical intent declarations.

## Deliverables

- A machine-readable product and authority contract bound to P54-T10 by SHA-256.
- GitHub Markdown and DocC contract documentation.
- Contract tests covering roles, semantic-author responsibilities, provider
  interchangeability, evidence classes, intent states, reviewer lifecycle,
  materialization boundary, threats, privacy, and non-authority.
- Documentation navigation and capability references.

## Product Boundary

The semantic author converts validated candidate evidence into complete,
reviewable proposals for purpose, package-owned capabilities, intents,
interfaces, and evidence bindings. It may recommend reuse of observed intents
or propose visibly experimental `intent.experimental.*` identifiers. It is not
an intent registry, canonicalization authority, autonomous maintainer,
publication engine, or source-of-truth editor.

## Provider Contract

Codex 5.3 Spark is the primary Phase 55 worker and LM Studio is a comparison
provider. Both consume the same bounded semantic request and produce the same
provider-neutral proposal contract. Provider identity, transport, cost, or
reasoning capability cannot alter evidence requirements, review semantics, or
authority.

## Intent States

- `observed`: existing SpecPM intent metadata available for comparison or reuse.
- `proposed_reuse`: a model recommendation to reuse an observed intent.
- `proposed_experimental`: a new evidence-grounded
  `intent.experimental.*` proposal.
- `reviewer_accepted` or `reviewer_edited`: fields approved for a new candidate
  revision, still not canonical registry truth.
- `canonical`: outside Phase 55 and possible only through separate SpecPM
  governance.

## Reviewer Authority

The model may propose but cannot accept, edit, reject, defer, materialize, or
publish its own output. A maintainer must explicitly accept, edit, reject, or
defer each proposal. Only accepted or edited fields may reach bounded
materialization into a new candidate revision with before/after provenance and
read-only SpecPM validation.

## Acceptance Criteria

- The contract binds the completed P54-T10 decision by repository-relative path
  and SHA-256.
- Model responsibilities include purpose refinement, concrete package-owned
  capability proposals, observed-intent reuse, experimental-intent proposals,
  interface claims, evidence selection, nearby-intent analysis, and non-goals.
- Every semantic claim requires an allowlisted source path and digest.
- Documentation is untrusted evidence, never host instructions.
- Codex 5.3 Spark and LM Studio share one provider-neutral authority contract.
- Experimental intents remain visibly non-canonical.
- Reviewer decisions and any materialized candidate revision remain
  proposal-only with respect to SpecPM accepted sources and registry truth.
- Raw prompts, raw responses, hidden reasoning, credentials, private machine
  paths, and unsupported quantitative claims are not persisted.
- No provider, materialization, package manager, harvested code, adapter,
  registry mutation, or publication path executes in P55-T1.

## Non-Goals

- Defining schemas or validation thresholds.
- Building semantic input packs or invoking a provider.
- Extending the Workbench UI.
- Materializing candidate revisions.
- Canonicalizing intents or publishing packages.

## Validation

- Focused documentation contract tests.
- Full pytest and coverage threshold.
- Ruff check and format check.
- `git diff --check`.
- Swift package manifest and documentation target checks.
