# P20-T3 Validation Report

**Date:** 2026-05-31
**Task:** P20-T3 — CodeGraph Adapter Evaluation
**Verdict:** PASS

## Evaluation Commands

- `npm view @colbymchenry/codegraph version license dist.tarball bin --json`
  - PASS: version `0.9.7`, license `MIT`, bin `codegraph: npm-shim.js`
- `npm view @colbymchenry/codegraph dependencies optionalDependencies peerDependencies --json`
  - PASS: platform packages listed as optional dependencies
- `npm view @colbymchenry/codegraph dist.integrity dist.shasum time.modified repository homepage --json`
  - PASS after retry; first attempt hit transient `ECONNRESET`
- `npm view @colbymchenry/codegraph-darwin-arm64@0.9.7 version license dist.tarball dist.integrity dist.shasum --json`
  - PASS: platform package metadata captured
- `curl -L --retry 3 --retry-delay 2 --fail https://registry.npmjs.org/@colbymchenry/codegraph/-/codegraph-0.9.7.tgz -o /tmp/codegraph-0.9.7.tgz`
  - PASS: small npm shim tarball downloaded and inspected
- `npx --yes @colbymchenry/codegraph --help`
  - PARTIAL: failed with transient npm registry `ECONNRESET`
- `npm pack @colbymchenry/codegraph@0.9.7 --pack-destination /tmp`
  - PARTIAL: failed with transient npm registry `ECONNRESET`
- `git clone --depth 1 https://github.com/colbymchenry/codegraph.git /tmp/codegraph-repo`
  - PASS: inspected source at `b026e64b413bb4dca1bc7326d7de0837afe0a899`
- `curl ... codegraph-darwin-arm64-0.9.7.tgz`
  - PARTIAL: platform bundle was approximately `45.5 MB`; interrupted after
    enough progress to confirm binary-bundle size and avoid unnecessary local
    installation for an evaluation-only PR

## Project Quality Gates

- `PYTHONPATH=src python -m pytest`
  - PASS: `473 passed, 1 skipped`
- `ruff check src tests && ruff format --check src tests`
  - PASS: `All checks passed!`, `79 files already formatted`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `473 passed, 1 skipped`; total coverage `91.76%`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Result

The evaluation produced a concrete recommendation and two follow-up tasks. No
production adapter code was added in this PR, so the existing runtime behavior
remains unchanged.
