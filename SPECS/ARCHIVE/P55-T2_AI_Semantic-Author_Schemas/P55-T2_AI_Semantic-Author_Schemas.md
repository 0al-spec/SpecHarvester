# P55-T2 AI Semantic-Author Schemas

## Objective

Define versioned, provider-neutral JSON Schema 2020-12 records for bounded AI
semantic authoring. The schemas must make complete proposals reviewable and
portable without giving providers, reviewers, or materialized candidate
revisions canonical SpecPM authority.

## Dependencies

- P55-T1 AI Semantic-Author Product and Authority Contract.
- The P55-T1 contract fixture at
  `tests/fixtures/ai_semantic_author_contract/p55-t1-ai-semantic-author-contract.example.json`,
  bound by SHA-256 `ddde481a6f9cdb8ec051b0d1d8944d217b7f1616174a987db1bb6f1357b9dd32`.
- The P54 local Workbench schema style and its inert, evidence-only decision
  boundary.

## Deliverables

- A packaged JSON Schema 2020-12 bundle for semantic author request, complete
  proposal, observed-intent reuse, experimental intent, nearby-intent analysis,
  claim-level evidence binding, reviewer edit, and materialization decision
  records.
- A small loader module so future P55 stages consume one schema artifact rather
  than duplicated shapes.
- Representative valid, malformed, unsupported-evidence, duplicate-intent, and
  stale-digest fixture cases validated with `Draft202012Validator`.
- GitHub Markdown and DocC documentation, capability navigation, and contract
  tests that bind the P55-T1 source digest.

## Record Boundary

Each standalone record and the fixture envelope uses its own `apiVersion`,
`kind`, and `schemaVersion`. The bundle must require:

- provider-neutral request and proposal identities;
- one allowlisted repository-relative path, SHA-256, and allowed evidence class
  for every semantic claim;
- package-owned capability IDs and explicit evidence-backed purpose, interface,
  nearby-intent, and non-goal claims;
- separate `observed`, `proposed_reuse`, and `proposed_experimental` intent
  records, with the latter constrained to `intent.experimental.*`;
- reviewer identity, proposal/source bundle digests, and accepted-or-edited
  fields before any materialization decision;
- materialized candidate revisions marked `preview_only` and non-canonical.

## Validation Boundary

The schemas reject unknown fields, malformed digests, absolute or traversal
paths, disallowed evidence classes, invalid experimental namespaces, duplicate
proposed intent IDs, unsupported claim bindings, stale source-bundle links, and
materialization attempts without an explicit accepted or edited reviewer
decision.

JSON Schema validates record shape. Deterministic semantic helpers may enforce
cross-record uniqueness and binding consistency; no provider, reviewer service,
candidate materializer, package manager, harvested repository, adapter, SpecPM
accepted source, registry, or publication path executes in P55-T2.

## Acceptance Criteria

- The schema is Draft 2020-12 and packaged with the Python distribution.
- Valid fixture coverage includes all required record kinds and the P55-T1
  authority/source contract binding.
- Invalid fixtures cover malformed shape, unsupported evidence class, duplicate
  intent proposal, and stale digest linkage.
- Raw prompts, raw responses, hidden reasoning, credentials, and private paths
  have no schema field.
- Both Markdown and DocC explain that provider execution and materialization
  are deferred to later tasks.
- Focused schema and documentation tests, full Python tests with coverage at
  least 90%, Ruff checks, `git diff --check`, and Swift documentation build pass.

## Non-Goals

- Building P55-T3 semantic input packs.
- Invoking Codex 5.3 Spark or LM Studio.
- Validating provider output against live repository sources.
- Rendering Workbench comparison UI or recording reviewer decisions.
- Materializing candidate revisions, canonicalizing intents, accepting packages,
  mutating SpecPM, or publishing the registry.
