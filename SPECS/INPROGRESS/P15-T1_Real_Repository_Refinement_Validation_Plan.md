# P15-T1 Real-Repository Refinement Validation Plan

Status: Planned
Task: `P15-T1`
Phase: Phase 15. Real Repository Refinement Validation
Priority: P1
Effort: 2-4 hours
Dependencies: `P14-T1`

## Problem

SpecHarvester now has deterministic evidence collection, candidate drafting,
SpecNode refinement contracts, clean semantic review, retry orchestration, and
a manual LM Studio live smoke. The remaining gap is a reproducible operator
plan for exercising that loop on real public repository checkouts without
committing generated outputs or expanding SpecHarvester into SpecNode runtime
territory.

## Goals

- Define a local-only validation plan for operator-supplied repository paths.
- Keep SpecHarvester responsible for collection, drafting, artifact bundles,
  validation reports, and compact quality summaries.
- Treat SpecNode as an external contract boundary for runtime/provider/model
  execution rather than implementing those responsibilities here.
- Define what gets recorded in reviewable summaries and what must remain
  untracked local output.
- Define when findings become SpecHarvester, SpecNode, Platform, SpecPM, or
  `.0al` coordination follow-ups.

## Non-Goals

- Do not implement SpecNode runtime, provider discovery, model execution,
  scheduling, provider lifecycle, or provider-specific orchestration.
- Do not edit `../SpecNode`, `../Platform`, or `../.0al` as part of this task
  except for an optional `.0al` handoff note when coordination is needed.
- Do not run package scripts, dependency installers, tests, build commands,
  registry calls, or arbitrary network probes inside harvested repositories.
- Do not commit generated `.smoke/` outputs, harvested source snapshots, raw
  prompts, provider transcripts, candidate specs, secrets, or model
  chain-of-thought.
- Do not tune ad-hoc prompts from one repository result; repeated failures must
  become explicit Workplan follow-ups.

## Deliverables

- A GitHub/DocC documentation page describing the real-repository validation
  plan.
- A safe input manifest shape for local repository path selection.
- A command sequence for `collect`, `draft`, SpecHarvester-side artifact
  packaging, optional external refinement, semantic review reporting, and
  compact triage.
- A quality rubric covering intent accuracy, capability/evidence support,
  SpecPM validation status, deterministic analyzer coverage, retry outcome, and
  token usage where available.
- Cross-repository ownership rules for routing findings to SpecHarvester,
  SpecNode, Platform, SpecPM, or `.0al`.
- A validation report showing docs/tests/quality gates run for this task.

## Cross-Repository Boundary

SpecHarvester owns:

- Repository source manifests and deterministic harvest snapshots.
- `ProjectProfile`, `PublicInterfaceIndex`, semantic evidence, and draft
  candidate metadata.
- SpecNode artifact bundle construction and contract validation.
- SpecPM validation and compact quality reports.
- Workplan follow-ups for deterministic analyzer, drafting, prompt-contract,
  and reporting gaps.

SpecNode owns:

- Runtime process or daemon behavior.
- Provider discovery, health checks, model execution, and provider lifecycle.
- Job protocol execution semantics and usage receipt production.
- Runtime security policy for local model/provider access.

Platform owns:

- Workspace catalog entries.
- Service topology, launch profiles, local path wiring, and provider wiring.
- Coordinated local environment startup/doctor flows.

`.0al` owns:

- Local coordination notes, cross-repo handoffs, and operator decisions that are
  not yet canonical product behavior.

## Acceptance Criteria

- The validation plan is documented in GitHub docs and mirrored into DocC.
- The documentation clearly rejects harvested code execution and generated
  output commits.
- The documentation identifies SpecNode as an external contract boundary and
  avoids assigning SpecNode runtime/provider responsibilities to SpecHarvester.
- The plan includes concrete local manifest examples, command examples, output
  locations, and quality scoring categories.
- Cross-repo findings have an explicit routing table for SpecHarvester,
  SpecNode, Platform, SpecPM, and `.0al`.
- Existing docs contract tests pass.
- Full Flow validation gates from `.flow/params.yaml` pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
