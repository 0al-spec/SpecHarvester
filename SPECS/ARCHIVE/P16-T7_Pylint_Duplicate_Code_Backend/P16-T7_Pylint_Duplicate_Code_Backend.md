# P16-T7 — Pylint Duplicate-Code Backend

Branch: `feature/P16-T7-pylint-duplicate-code-checks`
Review subject: `p16_t7_pylint_duplicate_code_backend`

## Context

P16-T6 introduced a dependency-free duplicate-code report contract and a
lightweight built-in detector. That was useful as a safe first step, but the
primary detector should be an established tool where possible.

For Python, `pylint` provides the widely used `duplicate-code` / `R0801`
similarity checker. This task integrates that checker behind the existing
`SpecHarvesterCodeDuplicationReport` contract.

## Goal

Add a `pylint` backend for `code-duplication-report` so operators and CI can
collect a standard duplicate-code baseline without replacing the stable report
contract.

## Deliverables

- Add `pylint` to development dependencies.
- Add `--backend builtin|pylint` to `code-duplication-report`.
- Convert `pylint --enable=duplicate-code --output-format=json` output into
  `SpecHarvesterCodeDuplicationReport`.
- Add regression tests for parsing `R0801` output, missing tool handling, and
  CLI behavior.
- Add a non-blocking CI baseline command using the `pylint` backend.
- Update GitHub docs and DocC mirror.

## Non-Goals

- Do not make duplicate-code detection blocking in CI yet.
- Do not add `jscpd` in this task; that should be a separate multi-language
  backend task because it introduces npm supply-chain and report-shape choices.
- Do not remove the built-in detector yet; keep it as a lightweight fallback.

## Acceptance Criteria

- `code-duplication-report --backend pylint` emits the same report kind as the
  built-in backend.
- Missing `pylint` returns a clear validation error.
- CI runs the `pylint` backend as advisory baseline collection without failing
  on the current duplicate baseline.
- Configured tests, lint, format, coverage, and Swift docs checks pass.
