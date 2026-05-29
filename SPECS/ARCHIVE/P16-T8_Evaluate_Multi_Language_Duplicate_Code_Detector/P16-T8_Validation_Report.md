# P16-T8 Validation Report

Task: `P16-T8 — Evaluate Multi-Language Duplicate-Code Detector`
Date: 2026-05-28
Branch: `feature/P16-T8-multilanguage-duplicate-code-detector`
Verdict: PASS

## Summary

- Added optional `jscpd` backend support behind the existing
  `SpecHarvesterCodeDuplicationReport` schema.
- Kept `builtin` and `pylint` backend behavior unchanged.
- Added CLI support for `--backend jscpd` and `--jscpd-command`.
- Kept `jscpd` out of project dependencies and default CI.
- Documented licensing, npm supply-chain boundary, deterministic JSON
  conversion, and opt-in CI posture in GitHub docs and DocC.
- Added a `jscpd`-specific trust-boundary note so report output does not imply
  that operator-supplied wrapper commands such as `npx` are dependency-free or
  network-free.

## Backend Evaluation

- `npm view jscpd@4.2.4 license version --json`
  - PASS: version `4.2.4`, license `MIT`.
- `npm view jscpd@4.2.4 dependencies --json`
  - PASS: direct dependencies are `@jscpd/core`, `@jscpd/finder`,
    `@jscpd/tokenizer`, reporter packages, `commander`, `colors`, and
    `fs-extra`.
- Direct dependency license spot-check:
  - PASS: `@jscpd/core@4.2.4`, `@jscpd/finder@4.2.4`,
    `@jscpd/tokenizer@4.2.4`, `@jscpd/html-reporter@4.2.4`,
    `@jscpd/badge-reporter@4.2.4`, `jscpd-sarif-reporter@4.2.4`,
    `commander@5`, `colors@1.4.0`, and `fs-extra@11` report MIT licenses.
- `npm pack --offline --silent --pack-destination /tmp jscpd@4.2.4`
  - PASS: cached package tarball available as `jscpd-4.2.4.tgz`.
- `npx --yes jscpd@4.2.4 --help`
  - NOT RUN SUCCESSFULLY: npm registry access failed with `ECONNRESET`.
    This supports keeping `jscpd` optional and out of default CI.

## Behavior Validation

- `PYTHONPATH=src python -m pytest tests/test_code_duplication_report.py tests/test_docs_contracts.py -q`
  - PASS: 45 passed.
- Mocked `jscpd` conversion tests cover:
  - `jscpd-report.json` conversion into the stable report schema;
  - deterministic source occurrence and preview mapping;
  - `summary.fileCount` from documented `statistics.total.sources`;
  - `jscpd`-specific external-tool trust-boundary reporting;
  - missing command failures;
  - empty command failures;
  - invalid JSON failures;
  - malformed duplicate entry failures;
  - CLI backend selection.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend builtin --path src/spec_harvester --output /tmp/p16t8-dup-builtin.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`,
    `fileCount=35`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend pylint --path src/spec_harvester --output /tmp/p16t8-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`,
    `fileCount=35`, `tool.returnCode=0`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend jscpd --path src/spec_harvester --output /tmp/p16t8-dup-jscpd-unavailable.json`
  - PASS as fail-closed unavailable-tool behavior: exit code `2` with
    `Cannot run jscpd duplicate-code backend`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend jscpd --jscpd-command '' --path src/spec_harvester`
  - PASS as fail-closed empty-command behavior: exit code `2`.

## Quality Gates

- `PYTHONPATH=src python -m pytest`
  - PASS: 424 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 424 passed, 1 skipped, total coverage 91.72%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 68 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `git diff --check`
  - PASS.

## Boundaries

- No npm package was added to project dependencies.
- No default CI step installs or runs `jscpd`.
- No scanned source code is executed or imported by SpecHarvester.
- The `jscpd` backend is opt-in and requires an operator-provided trusted local
  command.
- Invalid or missing external tool output fails closed.
