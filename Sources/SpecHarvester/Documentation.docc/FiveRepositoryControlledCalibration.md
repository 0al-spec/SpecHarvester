# Five-Repository Controlled Calibration

P52-T3 is the first live Phase 52 calibration over five operator-provided,
pinned local checkouts: Flask, Gin, xyflow, FastAPI, and FastMCP. It compares
static-only evidence, an LM Studio control, and the schema-validated Codex
Spark external-model handoff. All resulting artifacts remain proposal-only.

The compact durable report is
`tests/fixtures/controlled_calibration/p52-t3-five-repository-controlled-calibration.example.json`.
Its report digest is
`sha256:9d33c7fec360f131eb564d83815ee6c2ba628fec9a16e1801ea6f990250b85bf`.

## Result

All five static preflights passed. LM Studio used `openai/gpt-oss-20b` with
request-side `response_format.type: json_schema`, completed 13 proposal calls,
and recorded 127,360 total tokens. Its Flask, Gin, and FastAPI proposal
sidecars retain warning diagnostics for author review; they did not fail the
control or change registry truth.

Codex used `gpt-5.3-codex-spark` through `codex-cli 0.145.0`. All five calls
had exit code `0`, schema-valid final messages, repository-specific proposals,
and zero unsupported claims. The quality thresholds all passed:

| Metric | Result |
| --- | ---: |
| Static completion | 100% (5/5) |
| Codex completion | 100% (5/5) |
| Schema validity | 100% (5/5) |
| Repository specificity | 100% (5/5) |
| Unsupported claim rate | 0% (0/5) |

The first bounded Codex attempt exposed a valid but empty member selection for
Flask and Gin. The runner now requires a selected package whenever the P52
inventory is non-empty; the final full calibration passed with that rule.

## Boundary

The runner verifies revisions, runs static-only collection first, and gives
Codex only a temporary compact evidence stage. Its Codex invocation is
`read-only`, `ephemeral`, `ignore-user-config`, and
`skip-git-repo-check`; it validates the final JSON Schema before using the
existing `--model-output` handoff.

SpecHarvester durable artifacts do not retain raw prompts, raw model responses,
Codex stdout/stderr, session state, secrets, or chain-of-thought. LM Studio
server logging is operator-managed and outside this artifact guarantee; it must
be disabled separately before a provider-log-clean live run.

P52-T3 does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code or adapters, accept packages or
relations, publish registry metadata, seed baselines, remove `preview_only`,
or treat model output as registry truth.

The passed quality gate unlocks P52-T4, the twenty-repository controlled
pilot. It does not approve the 50-100 corpus or registry promotion.

## See Also

- <doc:ControlledRepositoryCorpusPlan>
- <doc:CodexSparkExternalModelAdapterContract>
- <doc:PackageSetAIDraftProposal>
- <doc:PackageSetAIEnrichment>
