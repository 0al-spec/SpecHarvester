# Relevant Intent Routing

P55-T10F gives the semantic author up to 16 positively matched observed SpecPM
intents instead of exposing only a candidate's existing generic intent.

Routing uses deterministic terms from the repository and package semantic
product profile. It preserves current generic observations and ranks positive
matches across observed intent IDs, capabilities, and package IDs. A nearby
selection requires at least two distinct product-term matches, preventing an
ambiguous word such as `node` or `agent` from selecting an unrelated intent.
Every selection binds the non-canonical, observed-only SpecPM snapshot and
source intent digest. Validation pins the exact snapshot digest and
reconstructs selected catalog records from that snapshot, so a semantic
substitution with a recomputed self-digest still fails closed.

A proposal fails the generic contradiction gate when its purpose uses at least
two specific product terms but every intent decision reuses only a generic
package, repository-metadata, or workspace intent. Bounded JSON repair retains
the full product evidence and can replace that answer with a sufficient
observed intent or one proposal-only `intent.experimental.*` declaration.

The router does not execute repository code, query a network service, create a
canonical intent, materialize a proposal, mutate registry truth, or publish.
