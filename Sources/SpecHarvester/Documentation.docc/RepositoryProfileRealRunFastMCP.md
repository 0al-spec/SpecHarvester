# Repository Profile Real Run: FastMCP

P37-T7 reran a pinned local FastMCP checkout through repository profile
auto-selection and compared it with explicit manual targeting. The run validates
the generic profile selection subsystem on a real repository without adding a
FastMCP-specific, Python-specific, or framework-specific rule.

## Source

| Field | Value |
| --- | --- |
| Repository | `https://github.com/jlowin/fastmcp` |
| Local checkout | `/Users/egor/Development/GitHub/fastmcp` |
| Revision | `3b8538e2422a1c43fdb69661c610de7985b785f2` |
| Run root | `/tmp/specharvester-p37-t7-fastmcp-20260618T223329Z` |
| AI mode | disabled through `--skip-ai` |
| Network | not required |

The durable fixture is:

```text
tests/fixtures/repository_profile_real_runs/p37-t7-fastmcp-auto-selection-comparison.example.json
```

It uses `apiVersion:
spec-harvester.repository-profile-real-run/v0`,
`kind: SpecHarvesterRepositoryProfileRealRunComparison`, and `schemaVersion:
1`.

## Commands

The auto-selection run enabled automatic profile selection:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/auto-inputs" \
  --out "$RUN_ROOT/auto-output" \
  --skip-ai \
  --repository-profile-selection auto
```

The comparison run disabled profile selection and used explicit operator
targeting:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/manual-inputs" \
  --out "$RUN_ROOT/manual-output" \
  --skip-ai \
  --repository-profile-selection none
```

Both batch reports completed with `status: passed`.

## Result

The auto-selection run recorded `decision: fallback`,
`selectedProfileId: null`, `fallbackProfileId: generic.repository.v0`,
`confidence: low`, and
`insufficient_high_confidence_profile_evidence`.

The manual `fastmcp_slim` target produced a materially narrower public
interface index:

| Metric | Auto root | Manual `fastmcp_slim` | Delta |
| --- | ---: | ---: | ---: |
| Public interface entrypoints | 772 | 260 | 512 fewer |
| Public interface symbols | 9199 | 1563 | 7636 fewer |
| Author-ready status | `author_ready_draft` | `author_ready_draft` | none |
| Author action items | 3 | 3 | none |

The finding is a profile-evidence mismatch: `harvest.json` saw
`pyproject.toml`, but `workspace-inventory.json` reported
`packageManifestCount: 0`, so auto-selection lacked high-confidence manifest
evidence and fell back.

## Verdict

The verdict is `follow_up_required`.

P37-T8 should make repository profile detection consume harvested package
manifest evidence when workspace inventory has no manifest records.

## Boundary

This real run is producer-side evidence only. It does not implement
ecosystem-specific profiles, change profile scoring, clone/fetch repositories,
install dependencies, execute harvested code, invoke package managers, run AI,
accept packages, accept relations, publish registry metadata, remove
`preview_only`, treat profile decisions or hints as registry truth, treat manual
targeting as registry truth, or treat AI output as registry truth.
