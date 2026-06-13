# Package-Set AI Enrichment

`package-set-ai-enrichment-proposal` builds proposal evidence only for
generated package-set candidates.

```bash
python3 -m spec_harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --provider-base-url http://127.0.0.1:1234 \
  --model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --request-output .smoke/xyflow-package-set/ai/requests.json \
  --output .smoke/xyflow-package-set/ai/ai-enrichment-proposals.json
```

The artifact identity is:

```json
{
  "apiVersion": "spec-harvester.package-set-ai-enrichment/v0",
  "kind": "SpecHarvesterPackageSetAIEnrichmentProposal",
  "schemaVersion": 1
}
```

The compact request includes deterministic candidate evidence plus optional
allowlisted source checkout evidence such as `package.json`, `README.md`,
`src/index.ts`, `src/lib/index.ts`, `src/types/index.ts`, and
`src/utils/index.ts`.

The model output is constrained to `refinedSummary`, `capabilities`,
`interfaces`, `evidencePaths`, `confidence`, and `evidenceGaps`. Unsupported
evidence paths produce `model_evidence_path_unsupported` diagnostics.

For package-local generated artifacts, the normalizer accepts paths relative to
the proposal package. For example, `harvest.json` in the `xyflow.react`
proposal is normalized to `xyflow.react/harvest.json` when that package-local
artifact was supplied in the compact request.

## Bounded JSON Repair

Live local provider output is parsed separately for each package member. When a
member response is malformed, SpecHarvester can send bounded repair prompts
through `--json-repair-max-attempts`.

Repair metadata is recorded in the affected member `providerReceipt` through
`jsonRepairNeeded`, `jsonRepairAttemptCount`, and `jsonRepairStatus`.
Exhausted repair attempts emit `ai_json_repair_exhausted` and produce a failed
proposal artifact when possible. Raw prompts, raw provider responses, secrets,
and chain-of-thought are not persisted.

Proposal outputs include `stopPolicySummary` with `stop_for_author_review`,
`continue_generation`, or `blocked_until_inputs_change`. This summary tells
operators whether another model iteration is useful; it does not mutate
generated specs and does not make AI enrichment registry truth.

This command does not mutate `specpm.yaml` or `specs/*.spec.yaml`. It does not
accept packages, accept relations, publish registry metadata, install
dependencies, run package scripts, execute package managers, run builds, run
tests, or browse the network. Provider execution is local and operator-opt-in;
CI must not require a running model provider.

SpecPM remains the validation, acceptance, relation, and registry authority.
