# P3-T1 Read Repository Source Manifests from inputs/*.yml

Status: Planned
Selected: 2026-05-17
Branch: `feature/P3-T1-read-repository-source-manifests-from-inputs-yml`
Review subject: `p3_t1_repository_source_manifests`

## Objective

Add the first batch-harvesting input surface by reading repository source
manifests from `inputs/*.yml`. The reader must validate deterministic source
metadata and expose it as JSON without cloning repositories, collecting
snapshots, running package managers, executing package scripts, or calling the
network.

This task prepares P3-T2. It does not implement batch collection.

## Deliverables

- Add a repository source manifest parser and validator.
- Support deterministic discovery of `*.yml` files under an input directory.
- Define a minimal schema with top-level `repositories` list entries.
- Normalize repository source records into deterministic dictionaries.
- Add a CLI preview command that reads manifests and prints JSON.
- Add tests for valid manifests, deterministic ordering, malformed YAML subset,
  duplicate IDs, missing required fields, unsupported schemes, and CLI output.
- Update GitHub docs with the manifest schema and trust boundary.
- Create `SPECS/INPROGRESS/P3-T1_Validation_Report.md` during EXECUTE.

## Manifest Schema

The supported YAML subset is intentionally small:

```yaml
repositories:
  - id: xyflow
    repository: https://github.com/xyflow/xyflow
    revision: 0123456789abcdef
    checkout: ../checkouts/xyflow
    packageId: xyflow.core
    enabled: true
```

Required fields:

- `id`
- `repository`
- one of `revision` or `ref`

Optional fields:

- `checkout`
- `packageId`
- `enabled`
- `labels`

## Acceptance Criteria

- Manifests are read from `inputs/*.yml` in deterministic path order.
- Disabled entries are skipped by default but can be included by API option.
- Repository URLs are accepted only for `https://` and `git@github.com:` forms.
- Each normalized record includes source manifest path and entry index.
- Duplicate repository IDs across all manifests are rejected.
- Malformed or unsupported manifest shapes fail with clear `ValueError`
  messages.
- The CLI command prints deterministic JSON and does not perform network,
  package-manager, package-script, or repository-code execution.
- Coverage must not decline from the P2-T4 baseline of 90.62%.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

Repository source manifests are operator-authored configuration files, but they
are still treated as data. Reading them must not trigger network access, clone
repositories, inspect package content, install dependencies, or execute package
scripts.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Parser tests | Temp `inputs/*.yml` fixtures | Failing tests for schema, ordering, disabled filtering, duplicate IDs, unsupported URLs, and malformed shapes | `PYTHONPATH=src python -m pytest tests/test_source_manifest.py` |
| CLI tests | Temp inputs directory | Failing test for JSON preview command | `PYTHONPATH=src python -m pytest tests/test_collector.py -k source_manifest` |
| Implementation | Test expectations | `source_manifest.py` and CLI command | Targeted tests pass |
| Documentation | Manifest schema and trust boundary | Docs updated | Review diff |
| Full validation | Repository gates | Validation report with coverage result >= 90.62% | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add parser and CLI tests first.
2. Implement a minimal dependency-free YAML subset parser for this schema.
3. Add `source-manifests` CLI command that prints normalized JSON.
4. Update docs with schema, examples, and non-goals.
5. Run targeted and full quality gates, explicitly comparing coverage to the
   P2-T4 90.62% baseline.

## Non-Goals

- No repository cloning.
- No batch `collect-local` orchestration.
- No network access.
- No package-manager access.
- No package script execution.
- No `*.yaml` support unless added intentionally in a later task.
- No remote manifest fetching.
