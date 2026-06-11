# Package-Set AI Draft Proposal

Status: Proposal-only LLM drafting contract

`package-set-ai-draft-proposal` is the LLM-first package-set drafting surface.
It consumes deterministic `workspace-inventory.json`, prepares a compact
repository topology request, and records model-selected package members,
exclusions, and `contains` relations as review evidence.

The command does not generate `specpm.yaml`, does not mutate
`specs/*.spec.yaml`, does not accept packages, does not accept relations, and
does not publish registry metadata.

## Command

Prepare compact model input without calling a provider:

```bash
python3 -m spec_harvester package-set-ai-draft-proposal \
  candidates/vite/workspace-inventory.json \
  --source-checkout ../../vite \
  --request-output candidates/vite/ai-draft/request.json
```

Wrap externally produced model output:

```bash
python3 -m spec_harvester package-set-ai-draft-proposal \
  candidates/vite/workspace-inventory.json \
  --model-output candidates/vite/ai-draft/model-output.json \
  --output candidates/vite/ai-draft/package-set-ai-draft-proposal.json
```

Run an operator-opt-in local OpenAI-compatible provider such as LM Studio:

```bash
python3 -m spec_harvester package-set-ai-draft-proposal \
  candidates/vite/workspace-inventory.json \
  --source-checkout ../../vite \
  --provider-base-url http://127.0.0.1:1234 \
  --model openai/gpt-oss-20b \
  --request-output candidates/vite/ai-draft/request.json \
  --output candidates/vite/ai-draft/package-set-ai-draft-proposal.json
```

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.package-set-ai-draft/v0",
  "kind": "SpecHarvesterPackageSetAIDraftProposal",
  "schemaVersion": 1
}
```

## Model Output Contract

The model returns one JSON object:

```json
{
  "packageSet": {
    "packageId": "vite.workspace",
    "summary": "Vite workspace package-set entrypoint.",
    "evidencePaths": ["workspace-inventory.json"],
    "confidence": "high"
  },
  "selectedMembers": [
    {
      "packageId": "vite.system",
      "role": "primary_package",
      "sourceTargetPath": "packages/vite",
      "reason": "Primary published Vite package.",
      "evidencePaths": ["workspace-inventory.json", "packages/vite/package.json"],
      "confidence": "high"
    }
  ],
  "excludedPackages": [
    {
      "packageId": "vite.test_cli",
      "category": "test",
      "reason": "Test fixture package, not a public package-set member.",
      "evidencePaths": ["workspace-inventory.json"],
      "confidence": "high"
    }
  ],
  "relations": [
    {
      "id": "vite.workspace.contains.vite.system",
      "type": "contains",
      "sourcePackageId": "vite.workspace",
      "targetPackageId": "vite.system",
      "evidencePaths": ["workspace-inventory.json"],
      "confidence": "high"
    }
  ],
  "evidenceGaps": [],
  "overallConfidence": "high"
}
```

`packageId`, `sourceTargetPath`, and relation endpoints must come from the
supplied inventory. `evidencePaths` must refer to supplied compact evidence.
Unsupported evidence paths produce `model_evidence_path_unsupported`
diagnostics. Relations fail closed when the target is not selected.

## Relationship to Author-Ready Drafts

The AI draft proposal is an input to the author-ready draft workflow, not a
final package specification. It can help select members, exclusions, and
`contains` relations, but the generated package-set bundle must still pass the
valid starter package hard gates documented in
[`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md).

Passing AI draft diagnostics should stop additional model iteration only when
the remaining issues are author-reviewable: wording, domain nuance, missing
author intent, or capability choices that need upstream judgment. It should not
stop when validation fails, inventory-derived paths drift, evidence paths are
unsupported, or relation endpoints are inconsistent.

## Role Taxonomy

The model may propose generic roles:

- `primary_package`
- `published_package`
- `plugin_package`
- `cli_package`
- `platform_binary_package`
- `example_package`
- `fixture_package`
- `test_package`
- `private_tooling_package`
- `member_package`

These roles are proposal labels. They do not replace maintainer review and do
not become SpecPM registry truth by themselves.

## Trust Boundary

This contract keeps the original `LLM + schema` idea while avoiding a
framework-specific rule database:

```text
workspace inventory
  -> compact topology request
  -> LLM package-set draft proposal
  -> schema normalization and diagnostics
  -> human review
  -> SpecPM validation and acceptance decision
```

SpecHarvester constrains and verifies model output. It does not need to know
every framework in the ecosystem. The model proposes structure from supplied
evidence; SpecPM and maintainers remain the acceptance authority.

The command must not:

- execute package code;
- install dependencies;
- run package managers;
- run builds or tests;
- browse the network;
- persist raw prompts, raw model responses, secrets, or chain-of-thought;
- treat model output as accepted registry metadata.
