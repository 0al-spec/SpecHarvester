# P55-T10F Validation Report

**Task:** P55-T10F Relevant Intent Routing and Generic Contradiction Gate

**Date:** 2026-08-01

**Verdict:** PASS

## Implementation Result

- The semantic campaign now uses a versioned, digest-bound snapshot of 26
  observed SpecPM intents from pinned SpecPM revision
  `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.
- Each candidate receives its current observed generic intents plus at most 16
  nearby observed intents selected from deterministic product-profile terms.
- Nearby selection requires at least two distinct product-term matches. This
  prevents ambiguous words such as `node` or `agent` from routing Axios, n8n,
  or Codex to unrelated observed intents.
- The provider request retains the routing query, matched terms, relevance
  scores, selection reasons, source-record digests, snapshot digest, and routing
  digest inside the semantic-author input pack.
- Provider validation and independent quality diagnostics reject a specific
  evidence-grounded purpose when every intent decision is only generic reuse.
  A missing sufficient observed intent remains eligible for one proposal-only
  `intent.experimental.*` decision under the existing false-novelty policy.

## Representative Static Smoke

The pinned retained-corpus inputs were prepared locally without invoking a
provider for `axios/axios`, `n8n-io/n8n`, `firecrawl/firecrawl`,
`bitcoin/bitcoin`, `excalidraw/excalidraw`, and `openai/codex`.

- All six retained their current generic observed intent as comparison evidence.
- None received an unrelated nearby intent after the two-term relevance gate.
- Before the gate, Axios incorrectly matched node-identity and node-editor
  intents from the single word `node`; n8n and Codex incorrectly matched the
  passport-alignment intent from the single word `agent`. Regression tests now
  prohibit those cases.
- The positive-control xyflow fixture still selects diagramming, flow
  diagramming, and node-editor intents through multiple product-term matches.
- The smoke only read pinned git objects and portable handoff candidates. It did
  not execute repository code, invoke package managers, call an AI provider, or
  persist generated campaign output.

## Safety and Authority

- The SpecPM snapshot is explicitly observed-only, non-canonical metadata. It
  does not define or approve taxonomy truth.
- Snapshot identity, source revision and digest, item identity, duplicate IDs,
  routing budget, selected IDs, source intent digests, and routing digest fail
  closed on mutation.
- Repository content remains bounded untrusted evidence and cannot become host
  instructions.
- No proposal was accepted, materialized, canonicalized, written to SpecPM or
  registry truth, or published.

## Validation Commands

- `PYTHONPATH=src .venv/bin/python -m pytest`: 1374 passed, 1 skipped.
- `PYTHONPATH=src .venv/bin/python -m pytest --cov=spec_harvester
  --cov-report=term-missing --cov-fail-under=90`: 1374 passed, 1 skipped; total
  coverage 90.01%.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed; 197 files formatted.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed with the existing unhandled
  DocC catalog warning.
- `git diff --check`: passed before the validation report was created.

## Follow-Up Boundary

P55-T10G remains responsible for invoking Codex 5.3 Spark on the frozen ten
repository calibration and measuring whether the repaired pipeline improves
generic-intent reduction and reviewer edit burden without increasing false
novelty or provider failures.
