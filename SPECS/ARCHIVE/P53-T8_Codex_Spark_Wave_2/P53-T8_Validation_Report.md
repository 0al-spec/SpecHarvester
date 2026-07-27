# P53-T8 Validation Report

**Verdict:** PASS (execution evidence recorded; does not unlock P53-T10)

## Clean Wave-2 Run

- Worker: `gpt-5.3-codex-spark` through `codex exec`; LM Studio and alternate
  workers were not used.
- Scope: exactly 25 frozen `wave-2` source identities at positions 26-50.
- Static revision gate: `passed`, 25 collected and preflighted; 75 sources
  skipped; no static failures.
- Codex proposals: 25 completed, 25 schema-valid, 24 repository-specific,
  1 unsupported claim, 0 terminal failures.
- Checkpoint: 25 completed, 0 terminal failures, `stop: null`; concurrency was
  two and all outputs remained proposal-only.
- Aggregate Codex receipt duration: `432895 ms`; maximum single receipt:
  `27375 ms`.

## Initial Quality Boundary for P53-T9

`bitcoin-bitcoin` is the sole quality exception. Its proposal is schema-valid
but has `repositorySpecific: false` and `unsupportedClaimCount: 1`. This makes
the unsupported-claim rate `1 / 25` (4%), above the Phase 53 scale-out limit of
2%.

## Targeted Corrective Rerun

The producer now omits `contains` relations for selected members whose
deterministic inventory has an empty `manifestPath`. The member remains in the
proposal, but the producer does not retain a relation claim without manifest
evidence. The Codex instruction records the same boundary.

A revision-verified rerun of only `bitcoin-bitcoin` completed with:

- schema-valid: `true`;
- repository-specific: `true`;
- unsupported claims: `0`;
- selected members: `1`;
- relations: `0`;
- warnings and errors: `0`.

Replacing only the original `bitcoin-bitcoin` record with this bounded rerun
gives effective wave-2 metrics of 25/25 completed, 25/25 schema-valid, 25/25
repository-specific, and 0/25 unsupported claims. P53-T9 must still manually
review at least three proposals and record the scale-out decision; this
corrective evidence does not itself unlock wave 3.

## Durable Local Evidence

| Artifact | SHA-256 |
| --- | --- |
| Wave report | `b859cb6accc440d46735756ffd741b4a6b7649c6cb2638aa574ee50f61bf3fce` |
| Campaign checkpoint | `efa7f9dde5664d80c8bcfa5c134d27961a16d29844ec3f8f142505e785648edf` |
| Static batch report | `60eea051b8a968d3b77c7a960f5d18261944b9cfe746e4dbdf0f953a836c3dae` |

Evidence root: `/tmp/p53-t8-wave-2-rerun/`. Durable artifacts persist no raw
prompts, raw model responses, or chain-of-thought.

| Targeted follow-up artifact | SHA-256 |
| --- | --- |
| Follow-up report | `7ecfc66ecbb48a377acd2b01f22b53ae8aafdf8b700e8a2abb1a7050418f4ddd` |
| Corrected proposal | `4818f764de36046994d4de1b37b3644f53adcc8a966fd9635af54af5c3297803` |
| Targeted static report | `b9a4d591b3cf32328a9518f48ab8bd403b917507a2d8afae6792155f87816074` |

Targeted evidence root:
`/tmp/p53-t8-bitcoin-follow-up.mDtiaB/`.

## Corrected Preflight Invocation

The first local invocation exposed that the new CLI `--wave` value was not
propagated into runner options. It was terminated before producing a final
report after four unintended wave-1 proposals. The propagation defect was
corrected and the clean rerun above is the only T8 result used for this report.
