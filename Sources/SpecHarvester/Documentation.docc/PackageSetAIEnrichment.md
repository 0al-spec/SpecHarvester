# Package-Set AI Enrichment

`package-set-ai-enrichment-proposal` builds proposal evidence only for
generated package-set candidates.

```bash
python3 -m spec_harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --provider-base-url http://127.0.0.1:1234 \
  --model openai/gpt-oss-20b \
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

This command does not mutate `specpm.yaml` or `specs/*.spec.yaml`. It does not
accept packages, accept relations, publish registry metadata, install
dependencies, run package scripts, execute package managers, run builds, run
tests, or browse the network. Provider execution is local and operator-opt-in;
CI must not require a running model provider.

SpecPM remains the validation, acceptance, relation, and registry authority.
