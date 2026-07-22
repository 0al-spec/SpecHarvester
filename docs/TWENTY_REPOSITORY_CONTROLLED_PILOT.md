# Twenty-Repository Controlled Pilot

Status: P52-T4 completed on 2026-07-22.

P52-T4 ran the Phase 52 controlled pilot over twenty clean, operator-provided,
pinned public local checkouts. It used a static-only baseline first, followed
by proposal-only LM Studio `openai/gpt-oss-20b` and schema-validated Codex
Spark `gpt-5.3-codex-spark` controls. All work was sequential (`concurrency: 1`)
to keep the local provider and external agent receipts deterministic.

The durable sanitized report is:

```text
tests/fixtures/twenty_repository_controlled_pilot/
  p52-t4-twenty-repository-controlled-pilot.example.json
```

Report digest:

```text
sha256:b91f1914150e337cf3a1729bbd23bef0526f159d31d10c087dd1034fc66d326b
```

## Result

| Measure | Result |
| --- | ---: |
| Static completion | 100% (20/20) |
| LM Studio proposal controls | 20/20 completed |
| Codex Spark completion | 100% (20/20) |
| Codex JSON Schema validity | 100% (20/20) |
| Repository specificity | 100% (20/20) |
| Unsupported claim rate | 0% (0/20) |
| Author-reviewed candidates | 10 supported, 0 unsupported |

LM Studio enrichment receipts recorded 221,037 prompt tokens, 7,082 completion
tokens, and 228,119 total tokens. Its proposals retain review diagnostics such
as selected/excluded member overlap, unknown roles, missing refined summaries,
and three unsupported evidence-path warnings; those sidecars remain
proposal-only and did not alter the Codex quality gate or registry state.

Codex Spark used `codex-cli 0.145.0`. All 20 calls returned exit code `0`,
produced schema-valid final messages, and completed in a combined 454,171 ms.
The runner persisted only proposal artifacts and bounded receipts. It did not
persist raw prompts, raw model responses, Codex stdout/stderr, session state,
secrets, or chain-of-thought.

Before the live run, the operator set LM Studio `logSensitiveData` to `false`.
Provider logging remains operator-managed; the report's durable privacy claim
is limited to SpecHarvester artifacts.

## Decision

The static, Codex completion, schema-validity, repository-specificity, and
unsupported-claim thresholds passed. A digest-bound author review sampled ten
Codex proposals and found each supported by its static inventory and
allowlisted evidence. P52-T4 therefore unlocks P52-T5, the final 50-100 source
manifest and checkout-readiness gate.

This is not package acceptance, relation acceptance, registry publication,
baseline seeding, or removal of `preview_only`. No repository was cloned,
fetched, restored, or modified, and no dependencies, package managers,
harvested code, or adapters were executed.
