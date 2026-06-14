# Next Task: P36-T4 FastAPI AI-Enabled Parser Profile Rerun

**Status:** In Progress
**Phase:** Phase 36. Repository Parsing Plugin System
**Task:** `P36-T4` Re-run the FastAPI AI-enabled candidate batch with the Python parser profile
**Branch:** `feature/P36-T4-fastapi-ai-enabled-parser-profile-rerun`
**Last Archived:** P36-T3 Plugin-Aware Source Classification Hook

## Recently Archived

- `P36-T3` added an opt-in parser profile hook for static analyzer path
  classification.
- `collect-batch` and `autonomous-candidate-batch` now accept
  `--parser-profile python.web_framework.v0`.
- The Python public API analyzer now proves default analyzer behavior remains
  unchanged when no parser profile is selected.
- When `python.web_framework.v0` is selected, paths classified with
  `publicInterfaceEligible: false` are excluded from public interface
  entrypoints.
- Public interface package records include `repositoryParsingProfile` and
  `pathClassification` review metadata.
- Unknown parser profile ids fail closed.
- The hook remains producer-side path classification evidence only: it does
  not publish registry metadata, accept packages or relations, remove
  `preview_only`, or treat AI output as registry truth.
- In plain terms, it does not treat AI output as registry truth.

## Context

P36-T1 documented the repository parsing plugin contract. P36-T2 added the
Python web-framework profile fixture. P36-T3 made that profile executable in
the analyzer path.

P36-T4 should now run the practical FastAPI comparison that motivated the
phase: an AI-enabled candidate batch using `python.web_framework.v0`, compared
against the earlier FastAPI run that over-captured `docs_src/*` tutorial code
as public API evidence.

## Motivation

- Verify that the new parser profile improves real FastAPI evidence selection.
- Measure evidence volume and claim quality after excluding tutorial files
  from `public-interface-index.json`.
- Decide whether the new output is closer to registry-review quality.

## Goal

Re-run FastAPI through the AI-enabled autonomous candidate pipeline with the
Python web-framework parser profile and record the comparison result.

## Proposed Scope

- Locate or create a bounded local FastAPI source manifest using an existing
  checkout when available.
- Run autonomous candidate batch with:
  - `--parser-profile python.web_framework.v0`
  - live LM Studio/OpenAI-compatible model when available;
  - deterministic fallback documentation if the local model endpoint is not
    reachable.
- Compare public interface evidence volume before/after parser profile use.
- Inspect generated candidate quality, author-ready verdicts, and AI
  proposal status.
- Record a durable fixture or report summarizing whether FastAPI output is
  closer to registry-review quality.

## Acceptance

- The run proves that `docs_src/*` no longer appears as public interface
  entrypoints when the parser profile is selected.
- The run records public interface entrypoint/symbol counts and candidate
  quality verdicts.
- The run records whether live AI was used and which provider/model was used.
- The report explicitly states that output remains producer-side evidence only
  and is not registry acceptance.
