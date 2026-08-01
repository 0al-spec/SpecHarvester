# P55-T10E Validation Report

**Task:** P55-T10E Repository and Package Semantic Product Profile

**Date:** 2026-08-01

**Verdict:** PASS

## Implementation Result

- The retained-corpus campaign now builds a deterministic semantic product
  profile before invoking an AI provider.
- The profile explicitly identifies the repository and selected package,
  including the candidate ID, target path, package role, manifest metadata,
  detected languages, ecosystems, package managers, and analyzer signals.
- Root and nearest package-local documentation are read from the pinned git
  revision. Their original repository paths, projected evidence paths, byte
  counts, and SHA-256 bindings are retained.
- Package metadata is projected from JSON and TOML manifests, with harvested
  package metadata retained as the deterministic fallback.
- The semantic-author input pack validates and includes the profile as bounded,
  untrusted evidence under the provider-neutral request contract.

## Safety and Authority

- Profile identity, full-profile digest, source bindings, document bindings,
  manifest bindings, relative paths, item counts, and byte budgets fail closed.
- Repository documentation and projected product metadata remain untrusted data
  and cannot become host instructions.
- All source reads use pinned git objects; repository code, package scripts,
  package managers, adapters, and networks are not invoked.
- No proposal was accepted, materialized, canonicalized, written to SpecPM or
  registry truth, or published.

## Validation Commands

- `PYTHONPATH=src .venv/bin/python -m pytest -q`: 1353 passed, 1 skipped before
  the final validator branch tests; the coverage run below includes all 1359
  passing tests.
- `PYTHONPATH=src .venv/bin/python -m pytest -q --cov=spec_harvester
  --cov-report=term --cov-fail-under=90`: 1359 passed, 1 skipped; total coverage
  90.02%.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed with the existing unhandled
  DocC catalog warning.
- `git diff --check`: passed.

## Follow-Up Boundary

P55-T10F remains responsible for relevant observed-intent retrieval and the
generic-intent contradiction gate. No provider run or repository calibration
was performed in this task.

## Review Follow-Up

- The input-pack builder now cross-checks profile bindings against the current
  `harvest.json`, `README.md`, and optional `PACKAGE_README.md` bytes before a
  provider request can be built.
- The GitHub and DocC authority contract descriptions now include deterministic
  semantic product profiles as untrusted evidence.
