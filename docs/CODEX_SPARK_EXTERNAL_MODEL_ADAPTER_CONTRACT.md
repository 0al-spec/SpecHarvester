# Codex Spark External-Model Adapter Contract

Status: P52-T2 contract; no live Codex invocation.

P52-T2 defines the narrow boundary for a future `gpt-5.3-codex-spark`
proposal worker. It is a contract and fixture, not a subprocess adapter, a
repository run, or an approval to process a corpus.

The durable contract is:

```text
tests/fixtures/codex_spark_external_model_adapter_contract/
  p52-t2-codex-spark-external-model-adapter-contract.example.json
```

Its final-message JSON Schema is:

```text
tests/fixtures/codex_spark_external_model_adapter_contract/
  package-set-ai-draft-final-message.schema.json
```

## Boundary

The adapter is `codex_exec_external_model_output`, not an OpenAI-compatible
HTTP provider. It does not replace the LM Studio path. A future
operator-opt-in execution may use only this profile:

```text
codex exec \
  --model gpt-5.3-codex-spark \
  --sandbox read-only \
  --ephemeral \
  --ignore-user-config \
  --cd <generated-read-only-evidence-stage> \
  --output-schema <package-set-ai-draft-final-message.schema.json> \
  --output-last-message <ephemeral-final-message.json> \
  <bounded-instruction-text>
```

The generated evidence stage contains the deterministic compact
`SpecHarvesterPackageSetAIDraftRequest` and allowlisted evidence copies only.
It must not expose an original checkout, writable agent workspace,
`--add-dir`, dependency installation, a package manager, harvested code,
adapter code, or a network/provider endpoint. The profile also forbids
`--dangerously-bypass-approvals-and-sandbox`, `--full-auto`, and `--json`;
therefore event-stream transcripts are not retained.

## Structured Handoff

Codex must emit exactly one final JSON message that validates against the
P52-T2 schema. The schema requires a top-level `proposal` envelope containing
the existing package-set draft shape: `packageSet`, selected members,
exclusions, `contains` relations, evidence gaps, and overall confidence.

Only after JSON Schema validation may the adapter unwrap `proposal` and invoke
the existing external handoff:

```text
package-set-ai-draft-proposal --model-output <validated-final-message.json>
```

The established `--model-output` seam already marks the provider record as an
externally produced model output. The future adapter must not send the output
through LM Studio, substitute an HTTP provider, repair malformed JSON, or
retain the raw model session.

## Receipts And Failure Policy

A future receipt may retain only the model id, Codex CLI version, sandbox,
schema digest, evidence digest, duration, exit code, and final-output digest.
It must not retain raw prompts, raw provider responses, secrets, session state,
and chain-of-thought.

The final proposal-only output is rejected, without repair or automatic retry,
when Codex is unavailable or version-incompatible, the model is unauthorized,
the command has a non-zero exit, its 300-second timeout expires, the final
message is missing or schema-invalid, the invocation policy drifts, the receipt
does not match, or the `--model-output` handoff fails.

## Authority

This contract records `execution: not_run`. It does not run Codex or AI; create,
restore, clone, or fetch a checkout; install dependencies; invoke package
managers; execute harvested code or adapters; accept packages or relations;
publish registry metadata; seed baselines; remove `preview_only`; or establish
registry truth. It unlocks planning of P52-T3 only after normal Flow review and
merge; P52-T3 remains the first five-repository calibration.

See also [the Phase 52 corpus plan](CONTROLLED_REPOSITORY_CORPUS_PLAN.md) and
[the package-set AI draft proposal contract](PACKAGE_SET_AI_DRAFT_PROPOSAL.md).
