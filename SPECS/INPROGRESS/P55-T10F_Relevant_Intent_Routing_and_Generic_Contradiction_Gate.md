# P55-T10F Relevant Intent Routing and Generic Contradiction Gate

## Objective

Give the semantic author a bounded set of semantically nearby observed SpecPM
intents and reject a proposal that demonstrates a specific product purpose but
maps it only to a generic implementation-shape intent.

## Dependencies

- P55-T10A experimental-intent decision policy and false-novelty protections.
- P55-T10D context-preserving JSON repair.
- P55-T10E deterministic repository and package semantic product profile.
- The observed-only SpecPM intent index at pinned SpecPM revision
  `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.

## Deliverables

- A versioned, digest-bound local snapshot of the observed SpecPM intent index,
  preserving observed-only and non-canonical authority.
- Deterministic relevant-intent routing that:
  - derives bounded product terms from the P55-T10E profile;
  - always retains current generic observed intents when present in SpecPM;
  - ranks positive lexical matches across intent IDs, capabilities, and package
    IDs;
  - excludes zero-score unrelated intents and caps the selected catalog;
  - records matched terms, score, source intent digest, and routing digest.
- Semantic-author input-pack and provider-request integration for the selected
  relevant catalog and routing explanation.
- A provider-neutral generic contradiction gate that rejects, including during
  bounded JSON repair, a proposal whose evidence-grounded purpose contains
  multiple specific product terms while every intent decision is generic reuse.
- Matching deterministic quality diagnostics for proposal records evaluated
  outside the live provider path.
- Focused fixtures for relevant observed reuse, justified experimental novelty,
  generic-only contradiction, stale snapshot data, and bounded selection.

## Acceptance Criteria

- The author receives current generic observations plus only positively matched
  nearby SpecPM intents, with at most 16 observed intents total.
- Existing observed intent digests come from the pinned SpecPM snapshot rather
  than hashes synthesized from candidate IDs.
- A specific purpose mapped only to `intent.package.javascript_library`,
  `intent.package.public_repository_metadata`, or
  `intent.repository.package_workspace` fails provider validation and appears
  as an error in deterministic quality diagnostics.
- A genuinely generic package description may still reuse a generic intent; a
  sufficient specific observed intent may be reused; a missing sufficient
  observed intent may still produce one proposal-only experimental intent.
- Snapshot, routing, catalog, candidate, and source digests fail closed on
  mutation, duplicate IDs, unsafe paths, or budget overflow.
- No network access, repository code, package manager, adapter, materialization,
  SpecPM mutation, registry mutation, canonicalization, or publication occurs.
- Python tests pass with at least 90% coverage; Ruff lint and format, diff
  integrity, Swift manifest, and Swift documentation checks pass.

## Non-Goals

- Invoking Codex 5.3 Spark or calibrating repositories; that is P55-T10G.
- Adding new canonical SpecPM intents or treating observed metadata as
  canonical taxonomy.
- Semantic embedding infrastructure, remote search, or an unbounded registry
  crawl.
- Accepting, materializing, canonicalizing, or publishing any proposal.
