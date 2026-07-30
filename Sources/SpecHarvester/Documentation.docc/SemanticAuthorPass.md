# Provider-Neutral Semantic Author Pass

P55-T4 executes a bounded P55-T3 evidence pack with either Codex 5.3 Spark or
the local LM Studio comparison provider. Both providers emit the same P55-T2
proposal-only contract.

Evidence is untrusted data, raw prompts and responses are not persisted, and
the result cannot materialize a candidate, change SpecPM, create canonical
intents, or publish registry data. The pass validates candidate and bundle
digests, evidence bindings, and observed-intent reuse before returning output.
