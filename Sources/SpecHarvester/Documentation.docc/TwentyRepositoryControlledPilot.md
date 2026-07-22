# Twenty-Repository Controlled Pilot

P52-T4 scales the Phase 52 calibration to twenty clean pinned public local
checkouts. It runs static collection first, then proposal-only LM Studio and
read-only schema-validated Codex Spark controls with deterministic concurrency
of one.

## Result

All 20 static baselines, LM Studio controls, and Codex Spark calls completed.
Codex output was 100% schema-valid and repository-specific with zero unsupported
claims. Ten digest-bound author reviews found the sampled proposals supported.
The complete sanitized result is recorded in
`tests/fixtures/twenty_repository_controlled_pilot/p52-t4-twenty-repository-controlled-pilot.example.json`.

LM Studio sensitive logging was disabled by the operator before the live run.
SpecHarvester stores no raw prompts, raw responses, Codex stdout/stderr, session
state, secrets, or chain-of-thought.

## Decision

The pilot unlocks P52-T5, the final 50-100 source manifest and checkout
readiness gate. It does not grant package, relation, baseline, publication, or
registry authority to static or model output.

## See Also

- <doc:FiveRepositoryControlledCalibration>
- <doc:ControlledRepositoryCorpusPlan>
- <doc:CodexSparkExternalModelAdapterContract>
