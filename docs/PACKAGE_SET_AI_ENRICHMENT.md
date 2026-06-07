# Package-Set AI Enrichment

Status: Proposal-only local refinement artifact

`package-set-ai-enrichment-proposal` builds an evidence-grounded AI enrichment
proposal for a generated package set. It consumes the deterministic
`draft-package-set` output and optional allowlisted files from a local public
checkout, then records model suggestions as review evidence.

The command does not mutate `specpm.yaml`, does not rewrite
`specs/*.spec.yaml`, does not accept packages, does not accept relations, and
does not publish registry metadata.

## Command

Prepare compact model input without calling a provider:

```bash
python3 -m spec_harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --request-output .smoke/xyflow-package-set/ai/requests.json
```

Run an operator-opt-in local OpenAI-compatible provider such as LM Studio:

```bash
python3 -m spec_harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --provider-base-url http://127.0.0.1:1234 \
  --model openai/gpt-oss-20b \
  --request-output .smoke/xyflow-package-set/ai/requests.json \
  --output .smoke/xyflow-package-set/ai/ai-enrichment-proposals.json
```

Wrap externally produced model output instead of calling a provider:

```bash
python3 -m spec_harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --source-checkout ../../xyflow \
  --model-output .smoke/xyflow-package-set/ai/model-output.json \
  --output .smoke/xyflow-package-set/ai/ai-enrichment-proposals.json
```

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.package-set-ai-enrichment/v0",
  "kind": "SpecHarvesterPackageSetAIEnrichmentProposal",
  "schemaVersion": 1
}
```

## Evidence Inputs

The compact model request may include:

- member candidate `specpm.yaml`;
- member `specs/*.spec.yaml`;
- member `harvest.json`;
- source checkout `package.json`;
- source checkout `README.md`;
- source checkout public export entrypoints such as `src/index.ts`,
  `src/lib/index.ts`, `src/types/index.ts`, and `src/utils/index.ts`.

The source checkout is operator-provided local evidence. The command reads
allowlisted text files only. It does not install dependencies, run package
scripts, execute package managers, run builds, run tests, or browse the
network.

## Model Output Contract

Each model proposal must use this shape:

```json
{
  "packageId": "xyflow.react",
  "refinedSummary": "one sentence",
  "capabilities": [
    {
      "id": "xyflow.react.flow_canvas",
      "summary": "Render and control an interactive React flow canvas.",
      "intentIds": ["intent.javascript.react_library"],
      "evidencePaths": ["packages/react/README.md", "packages/react/src/index.ts"],
      "confidence": "high"
    }
  ],
  "interfaces": [
    {
      "id": "react.component.ReactFlow",
      "kind": "component",
      "summary": "Primary React component export.",
      "evidencePaths": ["packages/react/src/index.ts"],
      "confidence": "high"
    }
  ],
  "evidenceGaps": [],
  "overallConfidence": "high"
}
```

`evidencePaths` must refer to paths supplied in the compact model request. The
proposal report emits `model_evidence_path_unsupported` diagnostics when the
model cites unknown paths.

## Trust Boundary

AI enrichment is proposal evidence only:

- model output cannot accept packages or relations;
- SpecPM remains the validation, acceptance, relation, and registry authority;
- raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted;
- provider execution is local and operator-opt-in;
- CI must not require a running local model provider.

The intended flow is:

```text
workspace inventory
  -> draft-package-set
  -> preflight-bundle-set
  -> package-set-ai-enrichment-proposal
  -> human review
  -> SpecPM-side validation and acceptance decision
```
