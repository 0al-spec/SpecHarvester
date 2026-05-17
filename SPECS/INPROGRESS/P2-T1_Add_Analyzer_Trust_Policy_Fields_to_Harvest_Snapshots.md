# P2-T1 Add Analyzer Trust Policy Fields to Harvest Snapshots

Status: Planned
Selected: 2026-05-17
Branch: `feature/P2-T1-add-analyzer-trust-policy-fields-to-harvest-snapshots`
Review subject: `p2_t1_analyzer_trust_policy_fields`

## Objective

Add explicit analyzer trust policy fields to `SpecHarvesterEvidenceSnapshot`
output so later analyzer cache, diagnostic, sandbox, and drafting flows can
evaluate analyzer artifacts against the same no-execution trust boundary used
for repository collection.

This task is a policy metadata task. It must not add analyzer execution,
package-manager execution, cache storage, Tree-sitter integration, or broad
source scanning.

## Deliverables

- Add a deterministic `analyzerPolicy` record to harvest snapshots.
- Include allowed analyzer execution modes, network policy, package script
  policy, input/output authority labels, and minimum evidence requirements.
- Add collector tests proving the policy fields are emitted deterministically.
- Add a small helper surface for constructing the default analyzer trust
  policy without duplicating dictionary literals.
- Update GitHub docs and DocC trust-boundary docs to explain the new snapshot
  policy fields.
- Create `SPECS/INPROGRESS/P2-T1_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- `collect-local` snapshots include an `analyzerPolicy` object.
- The default policy allows only analyzers that declare no repository code
  execution, no network access, and no package script execution.
- The policy requires analyzer id, analyzer version, source revision matching,
  and per-symbol/per-diagnostic source digest evidence.
- Existing snapshot fields remain backward-compatible: `policy.execution`,
  `policy.networkAccess`, `policy.packageScripts`, and
  `policy.contentAuthority` stay unchanged.
- Snapshot generation remains deterministic for the same input tree.
- No analyzer is run by `collect-local`.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

Harvested repository content is untrusted input. Analyzer output is also
untrusted evidence until validated and reviewed. The snapshot policy may
describe which analyzer metadata is acceptable, but it must not grant authority
to execute repository-owned scripts, install dependencies, call networks, or
treat analyzer claims as runtime behavior.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Collector tests | Small temp repository fixture | Failing assertions for `analyzerPolicy` shape and determinism | `PYTHONPATH=src python -m pytest tests/test_collector.py` |
| Implementation | Test expectations | `collector.py` helper and snapshot field | Targeted tests pass |
| Documentation | New policy meaning | Updated trust boundary docs and runbook text | Docs are deterministic |
| Full validation | Repository gates | Validation report | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add tests for the default analyzer trust policy emitted by `collect-local`.
2. Add a deterministic policy helper in `collector.py` and wire it into the
   snapshot root.
3. Update docs and DocC with the new policy contract.
4. Run targeted tests, then full Flow quality gates.
5. Record validation results in `P2-T1_Validation_Report.md`.

## Non-Goals

- No analyzer cache implementation.
- No parser sandbox implementation.
- No analyzer execution orchestration.
- No changes to `PublicInterfaceIndex` schema version.
- No promotion or registry policy changes.
