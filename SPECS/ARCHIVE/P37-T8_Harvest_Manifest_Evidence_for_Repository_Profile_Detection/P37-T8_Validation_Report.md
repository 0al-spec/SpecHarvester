# P37-T8 Validation Report

## Task

`P37-T8` Harvest Manifest Evidence for Repository Profile Detection.

## Result

Verdict: `PASS`.

Autonomous batch repository profile detection now supplements empty workspace
inventory evidence with already-collected static manifest paths from
`harvest.json`. This closes the generic evidence-routing gap found by P37-T7
without introducing a FastMCP-specific, Python-specific, or framework-specific
profile.

## Implementation Summary

- `repository_profile_evidence_paths()` still prefers
  `workspace-inventory.json` workspace and package manifest records.
- When workspace inventory provides no profile evidence, it reads
  `harvest.json` and uses files with `kind: package_manifest` or
  `kind: workspace_manifest` as static evidence paths.
- The autonomous batch `repositoryProfileDetection` sidecar now passes the
  collected `harvest.json` path into evidence construction.
- Existing package-set and disabled-selection behavior remains unchanged.

## Behavioral Proof

New regression coverage creates a single-package Go checkout where:

- `workspace-inventory.json` has `packageManifestCount: 0`;
- `harvest.json` has `packageManifestCount: 1`;
- the harvested manifest path is `go.mod`;
- `--repository-profile-selection auto` selects
  `generic.single_package.v0` with `confidence: high`;
- the detection payload records `go.mod` as evidence.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q
PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile or autonomous_candidate_batch'
PYTHONPATH=src ruff check src/spec_harvester/autonomous_candidate_batch.py tests/test_autonomous_candidate_batch.py tests/test_docs_contracts.py
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Observed results:

```text
14 passed in 0.57s
15 passed in 0.08s
7 passed, 100 deselected in 0.83s
All checks passed!
120 files already formatted
```

Full repository gates are run after archive/review artifacts are added, before
the pull request is opened.

## Boundary

Harvested manifest paths remain producer-side evidence. They do not accept
packages, accept relations, publish registry metadata, remove `preview_only`,
treat manifests as registry truth, or replace maintainer review.
