# P29-T5 LM Studio JSON Repair and Retry

## Objective

Add bounded JSON repair/retry for live LM Studio/OpenAI-compatible package-set
AI proposal generation so malformed local model output becomes reviewable,
diagnostic evidence instead of an uncaught provider failure or silent success.

This task applies to live provider execution for:

- `package-set-ai-draft-proposal`;
- `package-set-ai-enrichment-proposal`;
- `autonomous-candidate-batch` when live AI mode is enabled.

It does not change deterministic collection, deterministic package-set
drafting, external `--model-output` wrapping, SpecPM acceptance, or registry
publication.

## Background

`P29-T3` showed that local LM Studio output can fail strict JSON parsing under
real corpus load. `P29-T4` fixed the deterministic single-package candidate
fallback for Flask/Gin-style repositories, but live AI proposal generation can
still stop the autonomous batch when the model returns prose, partial JSON, or
malformed JSON.

The product target remains a valid author-ready starter package, not automatic
semantic truth. A local model failure should therefore preserve deterministic
evidence, record why AI proposal generation was unreliable, and give the
operator a bounded retry path without persisting raw prompts, raw provider
responses, secrets, or chain-of-thought.

## Deliverables

- Add a shared bounded JSON repair helper for local OpenAI-compatible provider
  responses.
- Use the helper from live package-set AI draft and enrichment providers.
- Record safe provider receipt metadata for repair behavior:
  - `jsonRepairAttemptCount`;
  - `jsonRepairStatus`;
  - `jsonRepairNeeded`;
  - response digest for the accepted final response only;
  - raw prompt/response persistence flags remaining `false`.
- Add structured diagnostics when repair is needed or exhausted:
  - `ai_json_repair_needed` for malformed initial output;
  - `ai_json_repair_exhausted` when bounded repair attempts do not produce a
    JSON object.
- Preserve failure semantics:
  - successful repair can continue to normal schema/proposal validation;
  - exhausted repair returns a `failed` AI proposal artifact when possible;
  - autonomous batch keeps deterministic artifacts and reports the AI failure
    through repository status and AI proposal records.
- Add CLI/operator controls for the bounded attempt count, with a conservative
  default and validation against negative values.
- Update docs, DocC, workplan, next task, validation/archive/review artifacts.

## Acceptance Criteria

- A live provider response with malformed JSON followed by repairable JSON
  yields `status: completed` or `warning` according to normal proposal
  validation, records one repair attempt, and persists no raw prompt or raw
  response text.
- A live provider response that remains malformed after bounded repair yields a
  `failed` proposal with `ai_json_repair_needed` and
  `ai_json_repair_exhausted` diagnostics.
- The provider receives no more repair prompts than the configured bound.
- Draft and enrichment proposal reports expose repair metadata in machine
  readable form.
- `autonomous-candidate-batch` forwards the repair bound and surfaces failed AI
  proposal status without deleting deterministic harvest, package-set draft,
  preflight, or author-ready summary artifacts.
- Request artifacts continue to contain compact evidence only; no raw prompts,
  raw provider responses, secrets, or chain-of-thought are written.

## Implementation Plan

1. Introduce a small shared module for model JSON parsing/repair orchestration
   and safe receipt diagnostics.
2. Refactor the package-set AI draft provider to use the shared repair helper
   for live execution.
3. Refactor the package-set AI enrichment provider to use the same helper for
   each member request.
4. Add CLI options and autonomous batch option plumbing for
   `json_repair_max_attempts`.
5. Add regression tests for successful repair, exhausted repair, privacy
   boundaries, CLI option propagation, and autonomous batch status surface.
6. Update documentation and Flow validation artifacts.

## Non-Goals

- No raw model output artifact persistence.
- No automatic semantic acceptance of repaired model output.
- No broad corpus rerun or readiness decision; that remains `P29-T6`.
- No SpecPM registry acceptance, baseline seeding, or public index mutation.
- No network scraping, dependency installation, package execution, or provider
  calls in CI tests.
