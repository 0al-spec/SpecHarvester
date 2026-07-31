# Provider-Neutral Semantic Author Pass

P55-T4 executes a bounded P55-T3 evidence pack with either Codex 5.3 Spark or
the local LM Studio comparison provider. Both providers emit the same P55-T2
proposal-only contract.

Evidence is untrusted data, raw prompts and responses are not persisted, and
the result cannot materialize a candidate, change SpecPM, create canonical
intents, or publish registry data. The pass validates candidate and bundle
digests, evidence bindings, observed-intent reuse, and claim references before
returning output. Both providers receive the same bounded evidence content,
use finite JSON repair, enforce output byte limits while reading, and retain
only allowlisted receipt metadata.

The P55-T10A experimental-intent decision policy is supplied to both providers.
It requires explicit semantic comparison for generic reuse and permits at most
one source-digest-bound experimental intent when observed intents are
insufficient. Novelty remains proposal-only and non-canonical.
