# Repository Plugin Multi-Repository Static Evaluator Validation

Status: Phase 39 real multi-repository validation.

P39-T6 runs the deterministic repository plugin applicability evaluator across
three existing local checkouts and verifies the P39-T5
`autonomous-candidate-batch` auto sidecar path.

The durable fixture lives at:

```text
tests/fixtures/repository_plugins/real_runs/p39-t6-multi-repository-static-evaluator-validation.example.json
```

It declares `apiVersion: spec-harvester.repository-plugin-real-run/v0`,
`kind: SpecHarvesterRepositoryPluginMultiRepositoryStaticEvaluatorValidation`,
and `schemaVersion: 1`.

## Corpus

| Repository | Shape | Revision | Profile result |
| --- | --- | --- | --- |
| `fastmcp` (FastMCP) | documentation-heavy Python single package | `3b8538e2422a1c43fdb69661c610de7985b785f2` | `generic.single_package.v0` |
| `fastapi` (FastAPI) | Python web framework single package | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | `generic.single_package.v0` |
| `xyflow` | JavaScript/TypeScript workspace package set | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | `generic.package_set.v0` |

All three local checkouts were available and clean. The run did not clone or
fetch repositories.

## Commands

P39-T6 exercised:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/<repo>/inputs" \
  --out "$RUN_ROOT/<repo>/baseline-output" \
  --skip-ai \
  --repository-profile-selection auto
```

```bash
PYTHONPATH=src python -m spec_harvester repository-plugin-applicability-detect \
  --registry tests/fixtures/repository_plugins/generic-registry.example.json \
  --static-evidence-envelope "$RUN_ROOT/<repo>/evidence/static-evidence-envelope.json" \
  --out "$RUN_ROOT/<repo>/detect/repository-plugin-applicability-report.json"
```

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/<repo>/inputs" \
  --out "$RUN_ROOT/<repo>/auto-output" \
  --skip-ai \
  --repository-profile-selection auto \
  --repository-plugin-registry tests/fixtures/repository_plugins/generic-registry.example.json \
  --repository-plugin-static-evidence-envelope "$RUN_ROOT/<repo>/evidence/static-evidence-envelope.json"
```

## Results

All three cases passed. Each standalone evaluator report and each batch
auto-sidecar report selected `4` plugin roles, blocked `1`, and recorded
`sourceMode: auto_static_evaluator`.

The single-package and workspace repositories produce different repository
profile decisions, but the generic plugin evaluator remains language- and
framework-agnostic. In each case it selected static parser/profile/manifest
evidence roles plus the topology helper, and left the review surface blocked
until a `package_topology_hint` is available as explicit evidence.

The batch sidecar matched the standalone evaluator summary and recorded
`appliedToDrafting: false` and `registryAuthority: false`.
In plain text, every batch sidecar records
`sourceMode: auto_static_evaluator`, `appliedToDrafting: false`, and
`registryAuthority: false`.

## Verdict

```text
passed
```

P39-T6 proves that the P39 static evaluator and P39-T5 batch auto-sidecar path
work on representative real local repositories without making plugin
applicability automatic by default or treating plugin decisions as registry
truth.

## Boundary

This validation is producer-side evidence only. It does not load third-party
plugin code, execute plugins, run plugin code, clone or fetch repositories,
install dependencies, execute harvested code, invoke package managers, run AI,
change parser profile behavior, change repository profile scoring, accept
packages, accept relations, publish registry metadata, remove `preview_only`,
treat plugin decisions as registry truth, or treat AI output as registry truth.
