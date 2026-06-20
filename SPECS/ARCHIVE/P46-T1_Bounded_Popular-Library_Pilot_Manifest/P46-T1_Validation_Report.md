# P46-T1 Validation Report

## Task

P46-T1 Bounded Popular-Library Pilot Manifest

## Verdict

PASS

## Summary

P46-T1 defines the first bounded Phase 46 pilot input contract without running
the pilot. The task adds a pinned, local-first source manifest for six
repositories and a durable fixture documenting selection rationale, local
checkout requirements, stop conditions, authority boundaries, and carry-forward
triage context from P45-T8.

## Durable Artifacts

- `inputs/p46-bounded-popular-library-pilot/repositories.yml`
- `tests/fixtures/bounded_popular_library_pilot_manifest/p46-t1-bounded-popular-library-pilot-manifest.example.json`
- `docs/BOUNDED_POPULAR_LIBRARY_PILOT_MANIFEST.md`
- `Sources/SpecHarvester/Documentation.docc/BoundedPopularLibraryPilotManifest.md`

## Pilot Manifest

Manifest digest:

```text
sha256:fe5786e7b905bef12bbda53ff1f3fe01a03dcd2051826bdca599e46e99f01f26
```

Selected pinned repositories:

| Repository | Revision | Package id | Notes |
| --- | --- | --- | --- |
| Flask | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` | `flask.core` | Python/PyPI single-package web framework |
| Gin | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | `gin.core` | Go single-package web framework; carries `model_evidence_path_unsupported` triage |
| xyflow | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | `xyflow.workspace` | TypeScript/npm workspace; carries fork-origin caveat |
| Cupertino | `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b` | `cupertino.core` | Swift Package Manager UI library |
| NavigationSplitView | `2c88df50b8f587560b91f6027e9ea275aee17060` | `navigation_split_view.core` | Swift Package Manager UI library |
| docc2context | `a2babcc4910c87bbd1b65f9a4221097f5ae4b753` | `docc2context.core` | Swift documentation CLI |

## Boundary Verification

P46-T1 did not run `autonomous-candidate-batch`, run AI, run adapters, clone or
fetch repositories, install dependencies, invoke package managers, execute
harvested code, accept packages, accept relations, publish registry metadata,
seed baselines, remove `preview_only`, persist raw prompts or raw responses, or
treat manifest, AI, adapter, or readiness output as registry truth.

The manifest requires existing local checkouts. Missing checkouts or revision
mismatches are explicit blockers for P46-T2 instead of triggers for network
repair.

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p46-bounded-popular-library-pilot` | PASS, `repositoryCount: 6` |
| `python3 -m json.tool tests/fixtures/bounded_popular_library_pilot_manifest/p46-t1-bounded-popular-library-pilot-manifest.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'bounded_popular_library_pilot_manifest or current_next_task'` | PASS, `1 passed, 161 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Remaining Gap

P46-T1 only establishes the bounded pilot input contract. P46-T2 must run the
manifest in static-only mode before any AI-enabled pilot, trusted local adapter
execution, registry publication, or baseline seeding can be considered.
