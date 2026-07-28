# P53-T10 Validation Report

**Verdict:** PASS

## Live Wave-3 Run

- Worker: `gpt-5.3-codex-spark` through `codex exec`; no LM Studio or alternate
  worker was used.
- Scope: exactly 25 frozen `wave-3` identities at positions 51-75, from
  `infiniflow-ragflow` through `ladybirdbrowser-ladybird`.
- Static revision gate: passed for all 25 selected checkouts.
- Codex proposals: 25 completed, schema-valid, repository-specific proposals;
  0 unsupported claims and 0 terminal failures.
- Aggregate receipt duration: `467593 ms`; maximum single receipt: `52366 ms`.
- Checkpoint stop: `wave_budget_limit` after the 25th completed repository. This
  is the configured per-wave boundary and is treated as a successful bounded
  completion, not a quality or execution failure.

## Quality Metrics

| Metric | Observed |
| --- | ---: |
| Static completion | 100% |
| Codex completion | 100% |
| Schema valid | 100% |
| Repository specific | 100% |
| Unsupported claim rate | 0% |

## Durable Local Evidence

| Artifact | SHA-256 |
| --- | --- |
| Wave report | `bf0a32afa8c964af5d0447b00cf2e68f16a7c72e30ac6e45ecf8bb44a0d9a7a0` |
| Campaign checkpoint | `b24e8bc5f46753633c14019a53d5470ff47932b86c037523b01c58975e70a696` |
| Static batch report | `d63b480d72fc692f089c5d7ccd9ca57ae923e5786e11a9153fd9f9c3aa7babc9` |

Evidence root: `/tmp/p53-t10-wave-3/`. Outputs remain sanitized proposal-only
evidence: raw prompts, provider responses, and chain-of-thought were not
persisted. This task does not unlock wave 4.
