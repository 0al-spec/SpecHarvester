# P16-T8 — Evaluate Multi-Language Duplicate-Code Detector

Branch: `feature/P16-T8-multilanguage-duplicate-code-detector`
Review subject: `p16_t8_multilanguage_duplicate_code_detector`

## Context

SpecHarvester already has `SpecHarvesterCodeDuplicationReport` with a
dependency-free `builtin` backend and a Python-focused `pylint` backend.
P16-T6 and P16-T7 intentionally kept duplicate-code checking advisory and
non-blocking.  P16-T8 evaluates whether a multi-language detector such as
`jscpd` can fit the same report contract without turning CI into a networked
npm install path.

Current package metadata observed from the npm registry:

- `jscpd` version: `4.2.4`
- license: `MIT`
- package description: `detector of copy/paste in files`
- repository: `git+ssh://git@github.com/kucherenko/jscpd.git`
- CLI bin: `jscpd`
- direct dependency footprint includes `@jscpd/core`, `@jscpd/finder`,
  `@jscpd/tokenizer`, reporter packages, `commander`, `colors`, and `fs-extra`

Registry access produced intermittent `ECONNRESET` during evaluation, so the
integration must not require live npm registry access for ordinary CI.

## Scope

- Add an optional `jscpd` backend behind the existing
  `SpecHarvesterCodeDuplicationReport` JSON contract.
- Keep `builtin` and `pylint` behavior unchanged.
- Convert deterministic `jscpd` JSON output into existing duplicate block
  fields: fingerprint, line count, normalized preview, and occurrences.
- Add CLI wiring for selecting the backend and supplying the command path or
  command words.
- Document licensing, supply-chain, trust-boundary, output-shape, and CI
  ergonomics.
- Add tests using mocked subprocess output rather than installing `jscpd` in
  the test suite.

## Non-Goals

- Do not add `jscpd` to Python package dependencies.
- Do not add npm install or `npx` to default CI.
- Do not make multi-language duplicate detection blocking.
- Do not change the report schema version.
- Do not run scanned repository code, imports, package scripts, or builds.
- Do not vendor npm packages or generated detector output.

## Acceptance Criteria

- `--backend jscpd` is accepted by the CLI and emits
  `SpecHarvesterCodeDuplicationReport`.
- Missing or invalid `jscpd` output fails closed with a clear error.
- Converted duplicates are sorted deterministically and preserve source paths
  and line ranges.
- Documentation states that `jscpd` is optional, MIT-licensed, npm-supplied,
  and not installed by SpecHarvester.
- Tests cover conversion, missing tool behavior, invalid JSON behavior, and CLI
  backend selection.
- Full Flow quality gates pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_code_duplication_report.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend builtin --path src/spec_harvester --output /tmp/p16t8-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend pylint --path src/spec_harvester --output /tmp/p16t8-dup-pylint.json`
- Optional local smoke if `jscpd` or `npx jscpd@4.2.4` is available:
  `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend jscpd --path <fixture> --min-lines 3 --jscpd-command <command> --output /tmp/p16t8-dup-jscpd.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
