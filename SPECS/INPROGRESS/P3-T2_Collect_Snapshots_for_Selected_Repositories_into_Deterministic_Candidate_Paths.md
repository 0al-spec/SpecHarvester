# P3-T2 Collect Snapshots for Selected Repositories into Deterministic Candidate Paths

Status: Planned
Selected: 2026-05-17
Branch: `feature/P3-T2-collect-snapshots-for-selected-repositories-into-deterministic-candidate-paths`
Review subject: `p3_t2_batch_snapshot_collection`

## Objective

Add deterministic batch snapshot collection for selected repository records from
validated `inputs/*.yml` source manifests. The collector must use only
operator-managed local checkouts and write each snapshot into a stable candidate
directory without cloning repositories, accessing the network, running package
managers, running package scripts, or executing repository content.

This task connects P3-T1 manifest records to the existing safe
`collect_local_repository` collector. It does not draft SpecPM packages or run
public interface analyzers.

## Deliverables

- Add a batch collection API that reads source manifests and collects snapshots
  for enabled selected repositories.
- Require every collected repository record to provide a local `checkout` path.
- Resolve relative checkout paths deterministically from the input manifest
  directory.
- Write snapshots under deterministic candidate directories based on repository
  IDs.
- Add a CLI command for batch collection with optional repeated selection by
  repository ID.
- Return deterministic JSON summary output for collected and skipped records.
- Add tests for deterministic output paths, selection filtering, missing
  checkout handling, missing checkout directory handling, and CLI output.
- Update GitHub docs and DocC with batch collection usage and trust boundary.
- Create `SPECS/INPROGRESS/P3-T2_Validation_Report.md` during EXECUTE.

## Proposed CLI

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --select xyflow \
  --select another-repo
```

If no `--select` values are provided, all enabled manifest records are collected.

Each collected repository writes:

```text
candidates/<repository-id>/harvest.json
```

The command prints deterministic JSON containing status, output root, collected
records, and skipped records.

## Acceptance Criteria

- Batch collection reads enabled repository records through the P3-T1 manifest
  reader.
- Batch collection never clones repositories, contacts networks, installs
  dependencies, runs package managers, runs package scripts, or executes
  repository code.
- Each collected record must have a non-empty `checkout` path that resolves to
  an existing local directory.
- Relative checkout paths are resolved relative to the input directory.
- Output paths are deterministic and derived from repository IDs, not from
  checkout paths or wall-clock time.
- Selected repository IDs are collected in deterministic manifest order.
- Unknown selected IDs fail with a clear `ValueError`.
- The CLI writes `harvest.json` snapshots and prints deterministic JSON.
- Coverage must not decline from the P3-T1 result of 91.48%.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

Repository source manifests are operator-authored data. Local checkouts contain
untrusted repository content. Batch collection may read only the same
allowlisted static files already handled by `collect_local_repository`.

The batch command must not:

- run `git clone`, `git fetch`, or other network operations;
- install dependencies;
- run build tools;
- run package managers;
- run package scripts;
- execute files from the checkout;
- infer output locations from untrusted repository content.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Batch API tests | Temp `inputs/*.yml` and local checkout fixtures | Failing tests for deterministic paths, selection, and validation errors | `PYTHONPATH=src python -m pytest tests/test_batch_collection.py` |
| CLI tests | Temp input and output directories | Failing test for `collect-batch` JSON output and `harvest.json` creation | `PYTHONPATH=src python -m pytest tests/test_batch_collection.py -k cli` |
| Implementation | Test expectations | Batch API and CLI command | Targeted tests pass |
| Documentation | Batch usage and trust boundary | Docs and DocC updated | Review diff |
| Full validation | Repository gates | Validation report with coverage result >= 91.48% | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add `tests/test_batch_collection.py` with deterministic fixtures.
2. Implement a small `batch_collection.py` module that orchestrates manifest
   reading and `collect_local_repository`.
3. Add `collect-batch` CLI command.
4. Update docs and DocC with examples, output layout, and non-goals.
5. Run targeted and full quality gates, explicitly comparing coverage to the
   P3-T1 91.48% baseline.

## Non-Goals

- No repository cloning.
- No network access.
- No package-manager access.
- No package script execution.
- No public interface analyzer execution.
- No deterministic drafting of SpecPM packages.
- No accepted package promotion.
