# P19-T1 — Static Spec Renderer

Status: Planned
Suggested: 2026-05-29

Branch: `feature/P19-T1-static-spec-renderer`
Review subject: `p19_t1_static_spec_renderer`

## Context

SpecHarvester generates reviewable SpecPM candidate packages under local output
directories. Today reviewers inspect `specpm.yaml`, referenced
`specs/*.spec.yaml` files, validation output, and raw auxiliary artifacts
directly. That is precise, but it is slow and not friendly for GitHub Pages,
local browser review, or future public preview workflows.

SpecPM already has a static registry viewer for generated `/v0` JSON endpoints,
but not a local candidate-package renderer that reads `specpm.yaml` plus
BoundarySpec YAML files and renders them as human-oriented static HTML.

## Scope

- Add a deterministic static renderer module for local SpecPM candidate
  directories.
- Add a CLI command that accepts an input candidate directory and output site
  directory.
- Parse `specpm.yaml` and referenced `specs/*.spec.yaml` files as untrusted
  data through local Python YAML loading only.
- Emit a small static site: `index.html`, browser JavaScript, browser CSS, and
  normalized `spec-package.json`.
- Render package identity, license, capabilities, intents, BoundarySpec cards,
  interfaces, evidence, effects, constraints, validation summary, and raw JSON.
- Keep the renderer data contract self-contained so the implementation can be
  extracted into a standalone repository later.
- Document trust boundary and usage.

## Non-Goals

- Do not execute harvested repository code, package scripts, dependency
  installers, build tools, tests, or network operations.
- Do not publish to GitHub Pages in this task.
- Do not replace SpecPM validation, registry generation, package acceptance, or
  compatibility policy.
- Do not depend on private SpecPM internals at runtime. SpecPM may remain a
  validation authority, but this renderer should have a small local contract.
- Do not implement semantic search, model-assisted review, editing, package
  signing, or public registry browsing.

## Design

- Introduce a behavior-rich renderer object that owns input loading,
  normalization, and static site writing.
- Keep browser-side code pure JavaScript with no npm build step, no runtime
  dependency fetching, and no YAML parsing in the browser.
- Normalize YAML into JSON-compatible records on the Python side:
  package metadata, manifest paths, referenced specs, validation issues, and
  selected reviewer-friendly summaries.
- Use safe HTML escaping in the client renderer and keep raw JSON rendering as
  text content rather than injected markup.
- Treat missing or malformed files as renderer diagnostics instead of executing
  fallback tooling.
- Keep assets under repository-controlled source files so tests can assert
  output shape and future extraction can move a small module plus static assets.

## Acceptance Criteria

- `spec-harvester render-spec-site --candidate <dir> --output <dir>` writes a
  deterministic static site for a valid generated candidate package.
- The site includes `index.html`, `assets/spec-renderer.js`,
  `assets/spec-renderer.css`, and `spec-package.json`.
- The normalized JSON contains package identity, manifest path, specs, selected
  BoundarySpec sections, diagnostics, and renderer metadata.
- Malformed or incomplete candidate input returns a non-zero CLI result with a
  structured diagnostic and does not execute package content.
- Tests cover valid rendering, missing manifest, missing referenced spec,
  browser asset inclusion, and escaping of untrusted text.
- Documentation explains local usage, trust boundary, relation to SpecPM, and
  future extraction into a separate repository.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_static_spec_renderer.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
