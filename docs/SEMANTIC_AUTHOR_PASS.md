# Provider-Neutral Semantic Author Pass

P55-T4 runs one bounded P55-T3 input pack through a provider-neutral,
proposal-only semantic-author pass. Codex 5.3 Spark is the primary worker;
LM Studio is an interchangeable local comparison provider. Both return the
same P55-T2 `SpecHarvesterAISemanticProposal` contract.

The pass reads no checkout itself. It consumes only the input pack, treats all
embedded repository evidence as untrusted data, and validates every returned
claim against the request evidence allowlist and observed-intent catalog.
Provider-specific transport metadata is held in a receipt and cannot alter
proposal authority, reviewer authority, or SpecPM validation requirements.

Codex uses bounded `codex exec` with a read-only sandbox and a temporary,
deleted last-message file. LM Studio uses only a credential-free local
OpenAI-compatible `/v1/chat/completions` endpoint with `json_schema` response
format. Raw prompts, raw responses, hidden reasoning, credentials, and local
paths are not persisted.

The output remains a proposal. It has no candidate materialization, reviewer
decision, canonical-intent, registry-mutation, or publication path. Malformed
output, stale bindings, unknown evidence, unknown observed intents, remote LM
Studio URLs, and exhausted output budgets fail closed.
