# Repository Profile Real Run: FastMCP

Status: Phase 37 real-repository validation evidence.

P37-T7 reran a pinned local FastMCP checkout through repository profile
auto-selection and compared it with explicit manual targeting. The goal was to
validate the generic profile selection subsystem on a real repository without
implementing a FastMCP-specific, Python-specific, or framework-specific rule.

## Source

| Field | Value |
| --- | --- |
| Repository | `https://github.com/jlowin/fastmcp` |
| Local checkout | `/Users/egor/Development/GitHub/fastmcp` |
| Revision | `3b8538e2422a1c43fdb69661c610de7985b785f2` |
| Run root | `/tmp/specharvester-p37-t7-fastmcp-20260618T223329Z` |
| AI mode | disabled through `--skip-ai` |
| Network | not required |

The durable summary fixture lives at:

```text
tests/fixtures/repository_profile_real_runs/p37-t7-fastmcp-auto-selection-comparison.example.json
```

It uses:

```json
{
  "apiVersion": "spec-harvester.repository-profile-real-run/v0",
  "kind": "SpecHarvesterRepositoryProfileRealRunComparison",
  "schemaVersion": 1
}
```

## Commands

The auto-selection run used repository-wide input and enabled automatic profile
selection:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/auto-inputs" \
  --out "$RUN_ROOT/auto-output" \
  --skip-ai \
  --repository-profile-selection auto
```

The comparison run used explicit operator targeting and disabled profile
selection:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/manual-inputs" \
  --out "$RUN_ROOT/manual-output" \
  --skip-ai \
  --repository-profile-selection none
```

Both batch reports completed with `status: passed`.

## Result

The auto-selection run did not select a high-confidence profile:

| Field | Value |
| --- | --- |
| Mode | `auto` |
| Decision | `fallback` |
| Selected profile | `null` |
| Fallback profile | `generic.repository.v0` |
| Confidence | `low` |
| Reason | `insufficient_high_confidence_profile_evidence` |

The auto run still explains the output: it records why the generic fallback was
used. It does not improve targeting for this checkout.

The manual target run used `fastmcp_slim` as an explicit folder target and
produced a materially narrower public interface index:

| Metric | Auto root | Manual `fastmcp_slim` | Delta |
| --- | ---: | ---: | ---: |
| Public interface entrypoints | 772 | 260 | 512 fewer |
| Public interface symbols | 9199 | 1563 | 7636 fewer |
| Author-ready status | `author_ready_draft` | `author_ready_draft` | none |
| Author action items | 3 | 3 | none |

## Finding

The important finding is a profile-evidence mismatch:

- `harvest.json` saw a package manifest at `pyproject.toml`;
- `workspace-inventory.json` reported `packageManifestCount: 0`;
- repository profile auto-selection consumed insufficient manifest evidence and
  fell back to `generic.repository.v0`.

This means current auto-selection is useful as review evidence, but it is not
yet good enough to replace manual target selection for this FastMCP shape.

## Verdict

```text
follow_up_required
```

P37-T8 adds a generic harvested-manifest fallback so repository profile
detection can consume package manifest evidence when workspace inventory has no
manifest records. That keeps the profile subsystem language- and
framework-agnostic while closing the real FastMCP evidence gap found by P37-T7.

## Boundary

This real run is producer-side evidence only.

It does not:

- implement an ecosystem-specific profile;
- change profile scoring;
- clone or fetch repositories;
- install dependencies;
- execute harvested code;
- invoke package managers;
- run AI;
- accept packages;
- accept relations;
- publish registry metadata;
- remove `preview_only`;
- treat profile decisions as registry truth;
- treat profile hints as registry truth;
- treat manual targeting as registry truth;
- treat AI output as registry truth.
