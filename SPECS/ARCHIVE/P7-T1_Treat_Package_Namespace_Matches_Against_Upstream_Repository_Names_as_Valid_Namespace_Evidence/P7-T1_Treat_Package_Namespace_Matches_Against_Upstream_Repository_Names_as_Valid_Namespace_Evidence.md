# P7-T1 - Treat Package Namespace Matches Against Upstream Repository Names as Valid Namespace Evidence

Branch: `feature/P7-T1-upstream-repository-name-namespace-evidence`
Review subject: `p7_t1_upstream_repository_name_namespace_evidence`

## Problem

Local smoke reports show false-positive namespace mismatches for candidates
whose package namespace matches the upstream repository name rather than the
GitHub owner. Examples include `xyflow.core`, `docc2context.core`, and
`puzzle.core`.

The current governance checks parse only the upstream owner from
`foreignArtifacts[].uri` and compare that owner with `metadata.id` namespace.
That misses a valid and common package naming pattern:

```text
https://github.com/<owner>/<repository>
package namespace == <repository>
```

## Goals

- Parse GitHub upstream references into owner and repository name.
- Treat namespace matches against either owner or repository name as valid
  namespace evidence.
- Share the behavior between namespace/upstream and license/provenance reports.
- Preserve existing diagnostics for missing, duplicate, malformed, and
  non-GitHub upstream references.

## Non-Goals

- No broad URL support beyond the existing GitHub HTTPS/HTTP and SSH forms.
- No candidate generation changes.
- No change to duplicate namespace detection.
- No acceptance/promotion behavior.

## Deliverables

- Add a deterministic upstream reference parser for GitHub URLs.
- Update namespace/upstream report checks.
- Update license/provenance report checks.
- Add regression tests for repository-name namespace matches.
- Add validation report and archive artifacts.

## Acceptance Criteria

- GitHub HTTPS/HTTP and SSH URLs expose owner and repository names.
- `metadata.id` namespace matches are valid when equal to upstream owner or
  upstream repository name, case-insensitively.
- Malformed and non-GitHub URI behavior is preserved.
- License provenance report no longer emits namespace mismatch when namespace
  matches repository name.
- Quality gates from `.flow/params.yaml` pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
