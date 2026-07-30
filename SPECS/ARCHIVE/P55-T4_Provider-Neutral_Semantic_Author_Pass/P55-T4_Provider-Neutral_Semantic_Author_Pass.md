# P55-T4 Provider-Neutral Semantic Author Pass

## Objective

Run one bounded P55-T3 semantic-author input pack through either Codex 5.3
Spark or an LM Studio OpenAI-compatible endpoint, then retain only a
schema-valid P55-T2 semantic proposal and a proposal-only execution receipt.
Both providers must have identical semantic authority and produce the same
proposal contract.

## Dependencies

- P55-T1 AI Semantic-Author Product and Authority Contract.
- P55-T2 AI Semantic-Author Schemas.
- P55-T3 Semantic Author Input Pack.
- Existing bounded local-provider JSON repair and Codex Spark process patterns.

## Deliverables

- A provider-neutral semantic-author pass API with explicit execution budgets.
- Codex 5.3 Spark and LM Studio adapters behind the same provider interface.
- Strict P55-T2 proposal validation against the input pack's request evidence
  and observed-intent catalog before a proposal can be returned.
- A compact receipt that records provider identity, bounded execution outcome,
  normalized proposal digest, and raw-data non-persistence assertions.
- Deterministic fixtures and tests for both adapters, invalid/stale proposals,
  provider errors, bounded retries, and proposal-only authority.
- GitHub Markdown and DocC documentation.

## Provider And Data Boundary

The pass consumes an already-built `SpecHarvesterAISemanticAuthorInputPack`; it
does not read repository paths, clone/fetch, execute harvested code, or invoke
a package manager. The prompt payload is derived solely from that pack and its
evidence remains untrusted data.

Codex is invoked through a bounded `codex exec` adapter using model
`gpt-5.3-codex-spark`. LM Studio is invoked only through a normalized local
OpenAI-compatible `/v1/chat/completions` endpoint. Both use the P55-T2 proposal
schema as the response contract. Provider transport details cannot alter
proposal authority, evidence requirements, identifier policy, reviewer
authority, or SpecPM ownership.

Raw prompts, raw provider responses, hidden reasoning, credentials, and local
machine paths are never persisted. A pass receipt may retain only normalized
provider metadata, outcome counts, bounded timing, repair metadata, and
cryptographic digests.

## Acceptance Criteria

- The same input pack yields a single provider-neutral proposal record shape
  for Codex 5.3 Spark and LM Studio.
- A returned proposal is schema-valid, binds to the exact candidate and source
  bundle, cites only request allowlisted evidence, and reuses only catalogued
  observed intents.
- Provider failure, malformed output, stale bindings, unknown evidence,
  unknown observed intents, excess output, or exhausted retries fail closed.
- Output is explicitly proposal-only and does not include reviewer edits,
  materialization decisions, candidate mutations, SpecPM mutation, canonical
  intent creation, or publication.
- Tests demonstrate bounded retry behavior and prove neither raw prompt nor raw
  response is written into portable reports.

## Non-Goals

- Quality scoring and semantic diagnostics (P55-T5).
- Portable handoff integration or Workbench rendering (P55-T6 and P55-T7).
- Live 100-candidate calibration, review, acceptance, intent governance,
  registry mutation, or public publication.
