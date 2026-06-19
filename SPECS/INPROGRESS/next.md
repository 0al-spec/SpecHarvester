# Next Task: P43-T1 Operational MVP Validation Plan

**Status:** Selected
**Branch:** `feature/P43-T1-operational-mvp-validation-plan`
**Phase:** Phase 43. Operational MVP Validation
**Task:** `P43-T1` Document the operational MVP validation plan and add the
next-task scaffold for proving SpecHarvester on a small pinned real-repository
corpus before adding new execution features.

## Motivation

- Phases 37 through 42 built the profile/plugin/adapter safety boundary, but the
  next product question is whether the current pipeline is already useful as an
  author-ready starter package generator.
- Operational validation should measure real repository output quality before
  starting broader autonomous scraping or enabling real adapter execution.
- The validation phase needs a written plan before adding machine-readable
  fixtures, commands, or real corpus run artifacts.

## Goal

Document the operational MVP validation loop: corpus requirements, run modes,
quality dimensions, stop policy, evidence boundaries, and follow-up tasks.

## Scope

- Add the Phase 43 plan to GitHub docs and DocC.
- Define a bounded pinned local corpus strategy for JS/TS, Python, Go, and at
  least one additional ecosystem when available.
- Define static-only and AI-enabled run modes.
- Define author-ready quality dimensions and SpecPM handoff readiness signals.
- Preserve the no-execution and non-authority boundaries established in P40-P42.
- Advance `SPECS/INPROGRESS/next.md` to `P43-T2` during archive.

## Non-Goals

- Do not run the real corpus in P43-T1.
- Do not enable trusted local adapter execution.
- Do not clone or fetch repositories implicitly.
- Do not publish registry metadata, accept packages, accept relations, seed
  baselines, remove `preview_only`, or treat AI output as registry truth.
