# Codex Spark External-Model Adapter Contract

Status: P52-T2 contract; no live Codex invocation.

P52-T2 records the bounded future integration of `gpt-5.3-codex-spark` as an
external proposal-only worker. The durable contract fixture is:

```text
tests/fixtures/codex_spark_external_model_adapter_contract/
  p52-t2-codex-spark-external-model-adapter-contract.example.json
```

The final-message JSON Schema is stored beside it:

```text
tests/fixtures/codex_spark_external_model_adapter_contract/
  package-set-ai-draft-final-message.schema.json
```

## Invocation Boundary

The contract identifies the adapter as `codex_exec_external_model_output`, not
an OpenAI-compatible HTTP provider, and it does not replace the LM Studio
path. A future operator-opt-in invocation is constrained to:

```text
codex exec --model gpt-5.3-codex-spark --sandbox read-only --ephemeral \
  --ignore-user-config --skip-git-repo-check --cd <generated-read-only-evidence-stage> \
  --output-schema <package-set-ai-draft-final-message.schema.json> \
  --output-last-message <ephemeral-final-message.json> <bounded-instruction-text>
```

The read-only stage contains a deterministic
`SpecHarvesterPackageSetAIDraftRequest` and allowlisted evidence copies only.
No original checkout, writable agent workspace, `--add-dir`, dependency
installation, package manager, harvested code, adapter code, or network/provider
endpoint is allowed. `--dangerously-bypass-approvals-and-sandbox`, `--full-auto`,
and `--json` are forbidden.
`--skip-git-repo-check` is limited to the deliberately non-Git evidence stage;
it does not relax the read-only sandbox.

## Handoff And Rejection

The only accepted model artifact is a final JSON message that passes the P52-T2
schema. Its required `proposal` envelope carries the existing package-set draft
shape. After validation, the adapter unwraps the envelope and invokes
`package-set-ai-draft-proposal <generated-workspace-inventory.json> --model-output
<validated-final-message.json>`. The generated inventory remains the required
positional input used to rebuild the deterministic request before the external
output is read. There is no malformed JSON repair and no raw session persistence.

A receipt may keep model, CLI version, sandbox, schema/evidence/output digests,
duration, and exit code. It excludes raw prompts, raw provider responses,
secrets, session state, and chain-of-thought. Non-zero exit, timeout, missing or
schema-invalid final output, policy drift, receipt mismatch, and handoff failure
all reject the proposal-only output without automatic retry.

This is `execution: not_run`: it grants no registry authority and does not
accept packages or relations, publish registry metadata, seed baselines, or
remove `preview_only`. Flow review and merge unlock P52-T3, the separate
five-repository calibration.

## Topics

### Related Documentation

- <doc:ControlledRepositoryCorpusPlan>
- <doc:PackageSetAIDraftProposal>
- <doc:PackageSetAIEnrichment>
