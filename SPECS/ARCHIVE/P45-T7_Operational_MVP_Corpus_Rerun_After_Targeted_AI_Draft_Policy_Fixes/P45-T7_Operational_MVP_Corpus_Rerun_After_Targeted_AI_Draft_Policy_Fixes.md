# P45-T7 Operational MVP Corpus Rerun After Targeted AI Draft Policy Fixes

Status: Planned
Phase: Phase 45. Operational MVP AI Draft Shape Hardening
Task: P45-T7
Branch: `feature/P45-T7-operational-mvp-rerun-after-targeted-ai-draft-policy-fixes`
Depends on: P45-T6 Single-Package no_proposal_subjects Policy

## Problem

P45-T5 and P45-T6 changed package-set AI draft normalization and stop-policy
behavior. The code-level tests prove the targeted cases, but Phase 45 still
needs bounded corpus evidence over the same xyflow, FastAPI, and Gin checkouts
used by P45-T3 before P45-T8 can make a final readiness decision.

## Goal

Re-run the bounded operational MVP corpus after P45-T5/P45-T6 and record
whether the remaining P45-T3 blockers are resolved:

- xyflow should no longer report `selected_member_role_unknown` for known role
  aliases;
- FastAPI and Gin should no longer block solely on `no_proposal_subjects` when
  single-package inventory evidence is diagnostic-clean;
- AI output should remain proposal-only with no raw prompt/response or
  chain-of-thought persistence.

## Deliverables

- P45-T7 rerun fixture under
  `tests/fixtures/operational_mvp_quality_hardening/`.
- GitHub Markdown and DocC documentation for the rerun result.
- Docs-contract coverage for fixture identity, source artifact digests,
  comparison fields, warning/stop-policy changes, and authority boundaries.
- Validation report and archive artifacts for P45-T7.

## Acceptance Criteria

- Use the same pinned local checkouts as P45-T3:
  - xyflow `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`;
  - FastAPI `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`;
  - Gin `5f4f9643258dc2a65e684b63f12c8d543c936c67`.
- Static-only and AI-enabled runs complete with zero repository failures.
- Fixture records processed counts, candidate counts, relation counts,
  proposal counts, token totals, warning codes, stop-policy reasons and
  decisions, validation guard status, privacy persistence flags, and
  proposal-only authority.
- Fixture compares P45-T7 to P45-T3 on warning codes, diagnostic counts, and
  stop-policy reasons.
- P45-T7 does not make the final Phase 46 readiness decision; P45-T8 owns that
  decision.

## Boundaries

- Do not broaden the corpus beyond xyflow, FastAPI, and Gin.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not install dependencies, invoke package managers, or execute harvested
  package code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.

## Validation Plan

- Verify local checkout revisions.
- Probe LM Studio at `http://127.0.0.1:1234/v1/models`.
- Run `source-manifests` for the generated P45-T7 manifest.
- Run static-only `autonomous-candidate-batch`.
- Run AI-enabled `autonomous-candidate-batch` with `openai/gpt-oss-20b`.
- Validate the P45-T7 fixture with `python3 -m json.tool`.
- Run focused docs-contract tests.
- Run lint, format, and whitespace checks for touched files.
