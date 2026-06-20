# Next Task: P46-T3 Bounded Popular-Library Pilot AI-Enabled Run

**Status:** Selected
**Branch:** `feature/P46-T3-bounded-popular-library-pilot-ai-enabled-run`
**Phase:** Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
**Task:** `P46-T3`
**Depends On:** `P46-T2` Bounded Popular-Library Pilot Static-Only Run

## Goal

Run the same pinned bounded popular-library pilot with the local
OpenAI-compatible provider after the static-only gate passed.

## Context

P46-T2 proved the deterministic static-only gate for
`inputs/p46-bounded-popular-library-pilot/repositories.yml`: six repositories
processed, nine preview candidates, three relation proposals, zero preflight
warnings, zero AI proposals, zero adapter sidecars, and no registry authority.

P46-T3 may now run the local OpenAI-compatible provider against the same
manifest. The output must remain proposal-only. Static output remains the
baseline for comparison; AI output is advisory review evidence, not registry
truth.

The run must preserve carry-forward triage for:

- Gin `model_evidence_path_unsupported`;
- xyflow `partial_public_interface_index`;
- xyflow `operator_checkout_origin_fork_mismatch`.

## Expected Deliverables

- AI-enabled run output or fixture/report for the same bounded pilot manifest.
- Comparison against the P46-T2 static-only gate covering processed
  repositories, candidates, relations, warnings, AI proposal counts, token
  usage, and quality-gate state.
- Documentation explaining proposal-only AI findings and any blockers for
  P46-T4 triage.
- Docs-contract or fixture coverage for run identity, source manifest digest,
  P46-T2 static baseline linkage, no raw prompt/response persistence, no
  adapter boundary, and no-registry-authority boundary.
- Validation report and archive artifacts for P46-T3.

## Boundaries

- Do not change the source manifest.
- Do not run outside the six pinned local checkouts.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not enable trusted local adapter execution or run adapter code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not persist raw prompts.
- Do not persist raw provider responses.
- Do not persist secrets or chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat adapter output as registry truth.
- Do not treat readiness output as registry truth.

## Recently Archived

- `P46-T2` Bounded Popular-Library Pilot Static-Only Run: PASS on 2026-06-20.
- `P46-T1` Bounded Popular-Library Pilot Manifest: PASS on 2026-06-20.
- `P45-T8` Targeted-Hardening Readiness Decision: PASS on 2026-06-20.

## Validation Expectations

- Run the AI-enabled pilot from
  `inputs/p46-bounded-popular-library-pilot/repositories.yml` against the local
  OpenAI-compatible provider.
- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for the P46-T3 run/comparison and current
  next task.
- Run formatting/lint/whitespace checks scaled to touched files.
