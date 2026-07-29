# AI Semantic-Author Schemas

P55-T2 defines the provider-neutral JSON Schema 2020-12 records required
before a semantic author can run. The schema bundle is
`schemas/ai-semantic-author-v0.schema.json`.

## Records

The bundle covers a bounded request, complete proposal, distinct observed
catalog intent, observed-intent reuse, experimental intent proposal,
nearby-intent analysis, reviewer edit, and future materialization decision.
Every semantic claim must carry allowlisted path-and-digest evidence.

`intent.experimental.*` remains visibly non-canonical. A materialization
decision requires an explicit `accepted` or `edited` reviewer decision, retains
`previewOnly: true`, and fixes `isRegistryTruth: false`.

## Deterministic Checks

JSON Schema validates record shape. The deterministic fixture validator also
rejects stale source-bundle or proposal bindings, claim evidence outside the
request allowlist, duplicate experimental intent IDs, and materialized claims
that the reviewer did not accept or edit. It binds the P55-T1 authority contract
by SHA-256.

The schema stores no raw prompt, raw provider response, hidden reasoning,
credential, or private machine path. It neither invokes Codex 5.3 Spark or LM
Studio nor materializes, canonicalizes, accepts, or publishes anything.

<doc:AISemanticAuthorContract> defines the preceding product and authority
boundary. P55-T3 will create bounded input packs for the request record.
