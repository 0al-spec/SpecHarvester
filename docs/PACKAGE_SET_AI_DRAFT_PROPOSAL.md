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
  --json-repair-max-attempts 1 \
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
diagnostics. Relations fail closed when the target is not selected. Common
relation endpoint aliases such as `source`, `target`, `sourcePackage`, and
`targetPackage` are normalized to `sourcePackageId` and `targetPackageId`
before validation. Endpoint aliases may be direct package-id strings or nested
objects with `packageId` or `id`. A missing target can be recovered only when a
single selected member package id is unambiguously present in the relation id or
in a single-item target list.

When model output omits `packageSet.packageId`, SpecHarvester uses the
deterministic request package-set id instead of recording a warning. For
single-package inventories, unknown `excludedPackages` entries are treated as
model-side noise and ignored when the deterministic package identity is stable.
Unknown exclusions for multi-package inventories still produce
`excluded_package_unknown` diagnostics.

When workspace inventory contains no package manifest records but the source
manifest declares a stable `packageId`, the AI draft request carries that
source-backed package identity as one fallback package. This keeps
single-package repositories reviewable without inventing registry acceptance.

Before normalizing proposal evidence, SpecHarvester records a deterministic
`validationGuard` summary with `status`, `diagnosticCount`, `errorCount`,
`warningCount`, and guard diagnostics. The guard reports
`package_set_subject_identity_missing` only when both the model output and the
deterministic request omit package-set identity. It also reports
`excluded_package_unknown` for multi-package inventories before those unknown
exclusions can become proposal evidence. Request-backed missing
`packageSet.packageId` and single-package inventories with model-side unknown
exclusions remain clean guard passes.

## LM Studio Structured Output

For the default `lm_studio` provider name, each live request includes
`response_format.type: json_schema` with the minimal
`spec_harvester_json_object` JSON-object schema. This request-side constraint
ensures the local `gpt-oss` control path returns one JSON object rather than a
Harmony control-token stream that the OpenAI-compatible endpoint cannot expose.

This schema is sent by SpecHarvester. Do not paste it into LM Studio's Chat
Template field. It guarantees JSON-object syntax only; the existing deterministic
inventory, evidence-path, relation, and semantic validation remains authoritative
after the response is received. `providerReceipt.responseFormat` records the
request-side mode. Other OpenAI-compatible provider names keep their existing
payload shape.

## Bounded JSON Repair

Live local provider output is parsed as one JSON object. When the first LM
Studio/OpenAI-compatible response is malformed, SpecHarvester can send a small
bounded number of repair prompts through `--json-repair-max-attempts`.

Repair is diagnostic evidence, not model trust:

- `ai_json_repair_needed` records that the initial response was malformed;
- `providerReceipt.jsonRepairNeeded`, `jsonRepairAttemptCount`, and
  `jsonRepairStatus` record machine-readable repair metadata;
- successful repair continues through the normal proposal normalizer and may
  return `warning` because repair was needed;
- exhausted repair attempts produce `ai_json_repair_exhausted` and a `failed`
  proposal artifact when possible;
- raw prompts, raw provider responses, secrets, and chain-of-thought remain
  unpersisted.

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

Proposal outputs include `stopPolicySummary` with `stop_for_author_review`,
`continue_generation`, or `blocked_until_inputs_change`. This is a model-loop
signal only; generated package bundles still need author-ready quality reports
and downstream validation.

## Single-Package Zero-Subject Policy

`no_proposal_subjects` remains blocking for package sets that need selected
members. A diagnostic-clean zero-subject draft is accepted as non-blocking only
when all of these are true:

- deterministic inventory contains exactly one package, including the
  source-backed package identity fallback when no package manifests were found;
- `validationGuard.status` is `passed`;
- the proposal has no blocking diagnostics; a warning-level
  `ai_json_repair_needed` diagnostic is non-blocking only when bounded JSON
  repair succeeded with `jsonRepairStatus: repaired`;
- the package-set identity is stable after request-backed normalization.

In that bounded case, `stopPolicySummary.decision` is
`stop_for_author_review`, `reason` is
`single_package_no_proposal_subjects_non_blocking`, and
`zeroSubjectPolicy.status` is `accepted_non_blocking`. This means additional
model iteration is not required for a single-package repository because the
deterministic inventory already supplies the only package subject.

For multi-package inventories, warning/failed proposals, or missing identity,
zero-subject output still reports `no_proposal_subjects` and
`zeroSubjectPolicy.status: requires_regeneration`.

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

Before writing proposal evidence, SpecHarvester normalizes role labels by
lowercasing them and treating spaces, hyphens, and punctuation as underscores.
It accepts the canonical role names above plus narrow aliases from adjacent
producer vocabularies. Important aliases include:

- inventory/profile roles: `core_runtime` -> `primary_package`,
  `react_binding` / `svelte_binding` / `library_package` -> `published_package`,
  `tooling_package` -> `private_tooling_package`;
- profile hints: `package_set_root` -> `workspace`, `bridge_package` ->
  `plugin_package`;
- common model labels: `primary` -> `primary_package`, `cli` -> `cli_package`,
  `fixture` -> `fixture_package`, `test` -> `test_package`, `package` ->
  `member_package`.

Unknown role labels still produce `selected_member_role_unknown`. The selected
member record falls back to `member_package`, and the diagnostic records the
original `modelRole` plus `normalizedFallbackRole` so author review can decide
whether the taxonomy needs a future extension.

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
