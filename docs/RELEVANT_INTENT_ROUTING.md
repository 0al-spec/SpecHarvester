# Relevant Intent Routing and Generic Contradiction Gate

P55-T10F fixes the intent-choice context used by the semantic author. Earlier
retained-corpus requests usually exposed only the candidate's existing generic
intent, so the provider could describe a specific product correctly and still
reuse an implementation-shape intent such as
`intent.package.javascript_library`.

## Observed SpecPM Snapshot

SpecHarvester packages a digest-bound snapshot of the 26 observed intents in
the SpecPM index at revision `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.
The snapshot has `observed_metadata_only` authority and `canonical: false`.
An observed intent is non-canonical comparison evidence, not a taxonomy
decision.

The snapshot records each intent ID, associated capabilities, package IDs, the
source index digest, and its pinned deterministic digest. Catalog validation
reconstructs every selected record from that exact snapshot, so replacing a
capability, source-record digest, or routing term and recomputing a self-digest
still fails closed. Campaign scope and every completed record bind and
revalidate the snapshot and routing digests.

## Bounded Routing

The router derives normalized product terms from the deterministic P55-T10E
profile: repository and package identity, package description and keywords,
target label, language, ecosystem, and analyzer signals. It then:

1. Retains current generic observations that actually exist in SpecPM.
2. Scores positive lexical matches across intent IDs, capability IDs, and
   package IDs.
3. Requires at least two distinct product-term matches, preventing ambiguous
   words such as `node` or `agent` from selecting an unrelated intent.
4. Returns at most 16 observed intents with matched terms, scores, selection
   reasons, and source-record digests.

The selected catalog and routing explanation are part of the digest-bound
semantic-author evidence. No network search or embedding service is used.

## Contradiction Gate

When a purpose claim contains at least two specific product terms, a proposal
cannot use only these generic intents:

- `intent.package.javascript_library`;
- `intent.package.public_repository_metadata`;
- `intent.repository.package_workspace`.

The provider validator rejects that contradiction during the normal structured
output path, so bounded JSON repair can reconsider the same full evidence. The
quality evaluator emits `specific_purpose_generic_only_contradiction` for the
same condition in retained or externally evaluated proposal records.

A generic package purpose may still justify generic reuse. A sufficiently close
observed intent should be reused. If the current SpecPM snapshot has no intent
that expresses the documented user outcome, the provider may propose one
evidence-grounded, package-neutral `intent.experimental.*` record under the
unchanged P55-T10A policy.

## Boundary

Routing does not create or canonicalize an intent. It executes no repository
code or package manager, performs no network access, and grants no acceptance,
materialization, registry mutation, or publication authority. P55-T10G performs
the first provider calibration over this corrected input and gate.
