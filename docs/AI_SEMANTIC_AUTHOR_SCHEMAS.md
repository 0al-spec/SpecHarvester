# AI Semantic-Author Schemas

P55-T2 defines `schemas/ai-semantic-author-v0.schema.json`, a JSON Schema
Draft 2020-12 bundle for bounded, provider-neutral semantic authoring.

The schema does not describe a provider transport or a prompt. It describes
portable evidence records that Codex 5.3 Spark, LM Studio, or a later provider
must all produce and that a reviewer can inspect without granting the provider
authority.

## Records

The bundle accepts standalone records as well as the all-record fixture:

| Record | Purpose |
| --- | --- |
| `SpecHarvesterAISemanticAuthorRequest` | A candidate ID, source-bundle digest, and bounded allowlisted evidence. |
| `SpecHarvesterAISemanticProposal` | Proposal-only semantic claims, provider receipt digest, and intent decisions. |
| `SpecHarvesterAISemanticIntentReuse` | A recommendation to reuse an observed `intent.*` declaration. |
| `SpecHarvesterAISemanticExperimentalIntent` | A visibly non-canonical `intent.experimental.*` proposal with user need, nearby intents, and non-goals. |
| `SpecHarvesterAISemanticNearbyIntentAnalysis` | Claim-backed differences from nearby observed intents. |
| `SpecHarvesterAISemanticReviewerEdit` | An explicit reviewer decision and accepted or edited claim set. |
| `SpecHarvesterAISemanticMaterializationDecision` | The future maintainer-controlled evidence needed to materialize a new `preview_only` revision. |

Every semantic claim carries one or more evidence bindings. Each binding has a
permitted evidence class, repository-relative path, file digest, and
source-bundle digest. The schema rejects unknown fields, malformed digests,
absolute or traversal paths, unsupported evidence classes, and invalid
experimental intent namespaces.

## Cross-Record Checks

`validate_semantic_author_fixture` adds deterministic checks JSON Schema cannot
express by itself:

- proposal, claim evidence, reviewer edit, and materialization decision must
  share the request source-bundle digest;
- reviewer edit and materialization decision must bind the proposal digest;
- materialization decision must bind the reviewer-edit digest;
- duplicate proposed experimental intent IDs are rejected.

The fixture also binds the P55-T1 authority contract by repository-relative
path and SHA-256. A schema record is evidence only, not a live instruction.

## Authority And Privacy

The materialization record deliberately has no execution effect in P55-T2. It
requires an `accepted` or `edited` reviewer decision, retains `previewOnly:
true`, and fixes `isRegistryTruth: false`. P55-T8 will implement controlled
materialization only after its own review boundary is complete.

No field retains raw prompts, raw provider responses, hidden reasoning,
credentials, or private machine paths. No schema record can accept a package,
create a canonical intent, mutate SpecPM accepted sources or registry truth, or
publish an index.

P55-T2 does not invoke Codex 5.3 Spark, LM Studio, a package manager, adapter,
or harvested repository content. P55-T3 will build the bounded input pack that
can later populate the request record.
