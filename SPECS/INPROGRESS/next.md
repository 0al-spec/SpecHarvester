# Next Task: P46-T4 Bounded Popular-Library Pilot Output Triage

**Status:** Selected
**Branch:** `feature/P46-T4-bounded-popular-library-pilot-output-triage`
**Phase:** Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
**Task:** `P46-T4`
**Depends On:** `P46-T3` Bounded Popular-Library Pilot AI-Enabled Run

## Goal

Triage the bounded pilot candidate layer and AI proposal sidecars, classifying
valid, reviewable, noisy, unsupported, evidence-gap, and do-not-promote outputs
per repository and per package-set member.

## Context

P46-T2 static-only gate passed: six repositories processed, nine preview
candidates, three relation proposals, zero preflight warnings, zero AI
proposals, zero adapter sidecars, and no registry authority.

P46-T3 AI-enabled batch ended `failed`: six repositories processed, two failed
repositories, four AI draft proposals, six AI enrichment proposals, and
110,186 AI enrichment provider tokens. Gin and docc2context AI draft outputs
failed with `ai_json_repair_exhausted` and
`package_set_subject_metadata_missing`. xyflow AI enrichment retained
`model_evidence_path_unsupported`.

## Expected Deliverables

- A triage fixture/report classifying static candidates, relation proposals,
  AI draft sidecars, AI enrichment sidecars, warnings, blockers, and
  do-not-promote outputs.
- Per-repository and per-member classification for Flask, Gin, xyflow,
  Cupertino, NavigationSplitView, and docc2context.
- Documentation explaining what is valid/reviewable, what is noisy, what is
  unsupported, what has an evidence gap, and what must not be promoted.
- Docs-contract coverage for triage identity, P46-T2/P46-T3 source artifact
  linkage, blocker classifications, no-authority boundaries, and current
  next-task pointer.
- Validation report and archive artifacts for P46-T4.

## Boundaries

- Do not rerun the pilot.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat adapter output as registry truth.

## Recently Archived

- `P46-T3` Bounded Popular-Library Pilot AI-Enabled Run: PASS as evidence
  capture on 2026-06-20.
- `P46-T2` Bounded Popular-Library Pilot Static-Only Run: PASS on 2026-06-20.
- `P46-T1` Bounded Popular-Library Pilot Manifest: PASS on 2026-06-20.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P46-T4 triage and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
