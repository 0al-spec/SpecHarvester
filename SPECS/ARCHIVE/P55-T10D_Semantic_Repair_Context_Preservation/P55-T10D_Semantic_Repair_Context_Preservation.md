# P55-T10D Semantic Repair Context Preservation

## Objective

Preserve the complete evidence-grounded semantic-author context across bounded
JSON repair so formal output correction cannot discard product understanding or
bias a specific proposal toward a generic observed intent.

## Dependencies

- P55-T3 bounded semantic author input-pack contract.
- P55-T4 provider-neutral semantic author pass.
- P55-T5 frozen quality and privacy policy.
- P55-T10C immutable follow-up evidence and PARTIAL maintainer disposition.

## Root-Cause Evidence

- P55-T10C completed 32 Spark records; 23 required JSON repair.
- All 23 repaired completions retained a generic intent.
- All four Spark experimental intents came from the nine direct completions.
- The current repair request includes schema and digest bindings but omits the
  original evidence contents and replaces the semantic system instructions with
  a formatting-only repair instruction.

## Deliverables

- Make every repair attempt continue the original message context:
  - retain the original semantic system instructions;
  - retain the complete original provider request and evidence contents;
  - identify the previous invalid output as assistant output;
  - append a bounded repair instruction with the deterministic validation error.
- Keep invalid model output truncated to the existing in-memory repair limit.
- Preserve provider-neutral behavior for Codex exec, LM Studio, AI draft, and AI
  enrichment callers of the shared repair helper.
- Add regression tests proving README/evidence content, observed intents,
  policies, and schema remain visible during repair while raw prompts and raw
  responses remain non-persistent.
- Record full repository quality gates and archive/review artifacts through FLOW.

## Acceptance Criteria

- Repair messages contain the unchanged original system prompt and original
  request object, including evidence content, at their original roles.
- Invalid output is represented as a bounded assistant message and the final
  user message contains the repair attempt number and validation error.
- Repair does not create another provider attempt, change the configured repair
  count, weaken schema or evidence validation, or synthesize missing evidence.
- Existing provider receipts continue to report repair status without storing
  prompts, responses, hidden reasoning, credentials, or machine-local paths.
- Tests cover direct completion, successful repair, exhausted repair, context
  preservation, truncation, and provider integration.
- Python tests pass with at least 90% coverage; Ruff lint and format, diff
  integrity, Swift manifest, and Swift documentation checks pass.

## Non-Goals

- Building the repository/package semantic product profile; that is P55-T10E.
- Changing intent retrieval or generic-reuse quality disposition; that is
  P55-T10F.
- Rerunning repositories or invoking Spark/LM Studio; calibration begins in
  P55-T10G.
- Accepting, materializing, canonicalizing, writing, or publishing any proposal.
