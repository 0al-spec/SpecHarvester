# AI Semantic-Author Product and Authority Contract

P55-T1 defines how an AI provider may act as an evidence-grounded candidate
spec author without becoming an acceptance or publication authority.

## Product

The semantic author produces complete proposals for:

- package purpose;
- concrete package-owned capabilities;
- observed intent reuse;
- new `intent.experimental.*` declarations;
- interfaces and evidence bindings;
- nearby-intent analysis and non-goals.

Codex 5.3 Spark is the primary worker. LM Studio is the comparison provider.
Both use the same provider-neutral request, proposal, evidence, review, and
authority contracts. Provider identity, transport, model size, or reasoning
capability cannot increase authority.

The semantic author is not an intent registry, canonicalization authority,
autonomous maintainer, publication engine, accepted-source editor, or registry
truth writer.

## Evidence

Every semantic claim must bind an allowlisted repository-relative source path
and digest. Allowed evidence includes validated candidate YAML, harvested
metadata, allowlisted source documentation, public-interface evidence, and the
SpecPM observed-intent catalog.

Repository documentation is untrusted evidence, not host instructions. A model
must not follow embedded requests to execute commands, access unrelated files,
change authority, approve output, or ignore validation.

## Intent States

`observed` means an intent exists in the SpecPM catalog; it does not by itself
mean the candidate should reuse it. `proposed_reuse` is a model recommendation.
`proposed_experimental` is a visibly non-canonical
`intent.experimental.*` proposal.

Reviewer-accepted or reviewer-edited fields may enter a new candidate revision,
but they still are not canonical registry truth. The `canonical` state requires
separate SpecPM governance outside Phase 55.

## Review And Materialization

The model cannot accept, edit, reject, defer, or materialize its own proposal.
A reviewer must inspect static-versus-AI output and make an explicit decision.
Only accepted or edited fields may be materialized into a new candidate
revision.

Materialization must bind reviewer identity, proposal digest, source-bundle
digest, preserve the prior candidate, record before/after provenance, and run
read-only SpecPM validation. The resulting revision remains proposal-only with
respect to accepted sources and registry truth.

## Workbench And Security

Candidate and model values are rendered as inert text under the Phase 54
restrictive Content Security Policy. Provider output cannot invoke the decision
service, read the CSRF token, or approve itself.

Validation must reject fabricated evidence paths, stale digests, unsupported
claims, namespace violations, generic or duplicate intents, experimental
intents presented as canonical, provider-specific authority escalation, hostile
markup, and private-path leakage.

## Privacy And Authority

Portable artifacts may retain normalized proposals, evidence bindings,
provider receipts, digests, reviewer edits, and decisions. They must not retain
raw prompts, raw provider responses, hidden reasoning, credentials, or private
machine paths.

Phase 55 does not automatically accept packages or relations, create canonical
intents, remove `preview_only`, mutate accepted sources or registry truth,
publish the public index, or automatically materialize proposals.
