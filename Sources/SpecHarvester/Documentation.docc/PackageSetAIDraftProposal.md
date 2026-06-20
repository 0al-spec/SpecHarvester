# Package-Set AI Draft Proposal

`package-set-ai-draft-proposal` is the LLM-first package-set drafting surface.
It consumes deterministic `workspace-inventory.json`, prepares compact
repository topology, and records model-selected package members, exclusions,
and `contains` relations as proposal-only review evidence.

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

The artifact identity is:

```json
{
  "apiVersion": "spec-harvester.package-set-ai-draft/v0",
  "kind": "SpecHarvesterPackageSetAIDraftProposal",
  "schemaVersion": 1
}
```

The model output proposes:

- aggregate package-set summary and evidence;
- selected member packages with generic roles such as `primary_package`,
  `cli_package`, `plugin_package`, or `platform_binary_package`;
- excluded inventory packages with reasons such as fixture, test, example, or
  private tooling;
- proposed `contains` relations from the aggregate package-set to selected
  members;
- confidence and evidence gaps.

SpecHarvester normalizes this output and emits diagnostics. Unsupported
evidence paths produce `model_evidence_path_unsupported`; relations fail closed
when they target packages that were not selected.

If model output omits `packageSet.packageId`, SpecHarvester uses the
deterministic request package-set id instead of recording a warning. For
single-package inventories, unknown `excludedPackages` entries are ignored as
model-side noise when deterministic package identity is stable. Unknown
exclusions for multi-package inventories still produce
`excluded_package_unknown` diagnostics.

## Bounded JSON Repair

Live local provider output is parsed as one JSON object. If the initial LM
Studio/OpenAI-compatible response is malformed, SpecHarvester can send a bounded
number of repair prompts through `--json-repair-max-attempts`.

Repair is recorded as proposal evidence only:

- `ai_json_repair_needed` marks malformed initial output;
- `providerReceipt.jsonRepairAttemptCount` and `jsonRepairStatus` expose the
  machine-readable repair outcome;
- exhausted repair emits `ai_json_repair_exhausted` and a failed proposal
  artifact when possible;
- raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.

This keeps the original `LLM + schema` model while avoiding a hardcoded
framework encyclopedia. Deterministic inventory is evidence, the model proposes
structure, and SpecPM plus maintainers remain the validation and registry
authority. The command does not mutate generated specs, execute package code,
install dependencies, run package managers, browse the network, or treat model
output as registry truth.

## Author-Ready Draft Boundary

The AI draft proposal can help produce an author-ready valid starter package,
but it is not the final specification. The generated package-set bundle must
still pass the valid starter package hard gates in
<doc:AuthorReadyDraftQualityBar>.

Passing AI draft diagnostics should stop additional model iteration only when
the remaining issues are author-reviewable, such as wording, domain nuance,
missing author intent, or capability choices that require upstream judgment. It
should not stop when validation fails, inventory-derived paths drift, evidence
paths are unsupported, or relation endpoints are inconsistent.

Proposal outputs include `stopPolicySummary` with `stop_for_author_review`,
`continue_generation`, or `blocked_until_inputs_change`. This is a model-loop
signal only; generated package bundles still need author-ready quality reports
and downstream validation.
