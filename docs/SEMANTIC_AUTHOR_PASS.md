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
The provider payload includes the bounded evidence content and observed-intent
records as well as their request bindings, so semantic claims can be grounded
without additional filesystem reads.

Codex uses bounded `codex exec` with a read-only sandbox and a temporary,
deleted last-message file. LM Studio uses only a credential-free local
OpenAI-compatible `/v1/chat/completions` endpoint with `json_schema` response
format. Raw prompts, raw responses, hidden reasoning, credentials, and local
paths are not persisted.

Both adapters read at most the configured output byte limit plus one overflow
byte and support a finite JSON-repair budget. Portable receipts are rebuilt
from a fixed metadata allowlist; provider-supplied prompt, response, credential,
or private-path fields are discarded.

The output remains a proposal. It has no candidate materialization, reviewer
decision, canonical-intent, registry-mutation, or publication path. Malformed
output, stale bindings, unknown evidence, unknown observed intents, remote LM
Studio URLs, and exhausted output budgets fail closed.
