# P55-T10A Validation Report

**Task:** P55-T10A Experimental-Intent Decision Policy

**Date:** 2026-07-31

**Verdict:** PASS

## Policy Contract

- Added a versioned JSON decision policy with canonical SHA-256 binding
  `0c8a92c0a782d501659021f75c644b03cb2156cd51151e6bbe322ed20845031c`.
- Preserved the three P55 generic observed intent IDs and the P55-T5 frozen
  numerical quality policy without changing thresholds.
- Bound the same policy into Codex 5.3 Spark and LM Studio provider requests and
  into retained semantic-pass evidence.

## Decision Validation

- Existing observed intents remain reusable when semantically sufficient.
- Generic reuse requires an evidence-bound `nearby_intent_difference` claim.
- At most one experimental intent may be proposed, and it cannot retain generic
  observed-intent reuse in the same decision.
- Experimental identifiers require two to six package-neutral semantic terms
  and the first eight characters of the source bundle digest.
- Experimental user need, observed nearby intents, non-goals, and differentiation
  claim kinds are validated before a proposal is retained.
- Experimental overlap with an observed intent is reported as false novelty and
  is a calibration failure rather than a threshold change.

## Authority and Safety

- Semantic output remains `semantic_author_proposal_only`.
- The policy grants no reviewer, materialization, canonicalization, SpecPM,
  registry, or publication authority.
- Provider evidence remains allowlisted and no harvested repository code or
  package manager is executed.
- Raw prompts, raw responses, hidden reasoning, credentials, and local paths are
  not persisted.

## Validation Commands

- `uv run pytest tests/test_experimental_intent_policy.py
  tests/test_semantic_author_pass.py tests/test_semantic_proposal_quality.py -q`:
  `61 passed`.
- `uv run pytest --cov=spec_harvester --cov-report=term-missing
  --cov-fail-under=90`: `1305 passed, 1 skipped`; total coverage `90.03%`.
- `uv run ruff check src tests`: passed.
- `uv run ruff format --check src tests`: passed.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed with the existing warning
  that the DocC catalog is unhandled by the executable target.
- `git diff --check`: passed.
