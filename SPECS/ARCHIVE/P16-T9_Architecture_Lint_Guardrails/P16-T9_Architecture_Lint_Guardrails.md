# P16-T9 — Architecture Lint Guardrails

Branch: `feature/P16-T9-architecture-lint-guardrails`
Review subject: `p16_t9_architecture_lint_guardrails`

## Context

The next structural work may apply the tested Elegant Objects refactoring style
from `../../PromptEval/tools/prompt-eval/prompts/elegant_objects/eo_refactor.md`.
Before changing report-layer structure, SpecHarvester needs small deterministic
guardrails that catch the most likely relapse risks:

- broad `Helper`, `Manager`, `Processor`, `Service`, and `Utils` names;
- I/O or heavy work inside constructors;
- static/class helper methods in domain modules;
- duplicated `specpm.yaml` manifest parser patterns.

## Goal

Add a dependency-free architecture linter that runs locally and in CI as an
advisory baseline. The linter should produce deterministic JSON output and an
optional fail mode, but this task must not make current baseline findings
blocking.

## Deliverables

- Add `architecture-lint` CLI command.
- Add architecture lint report JSON with stable `kind`, `summary`, `issues`,
  and `trustBoundary`.
- Implement initial rules:
  - `helper_name_relapse`
  - `constructor_io`
  - `static_domain_helper`
  - `manifest_parser_pattern`
- Add tests for each rule, missing-path handling, output writing, and
  `--fail-on-issues`.
- Add GitHub docs and DocC mirror.
- Add a non-blocking CI baseline command.

## Non-Goals

- Do not enforce full Elegant Objects semantics with regexes.
- Do not block CI on current architecture findings.
- Do not refactor report modules in this task.
- Do not add new dependencies such as Semgrep or ast-grep yet.

## Acceptance Criteria

- `architecture-lint` produces deterministic output for selected source roots.
- Missing paths fail closed instead of producing false clean reports.
- CI collects an advisory architecture lint baseline.
- Tests, lint, format, coverage, Swift manifest, and Swift docs build pass.
