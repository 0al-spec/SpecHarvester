# P52-T10 Dual-License Collector Follow-Up

P52-T10 corrects a strict collector filename allowlist gap found in the P52-T6
historical static-only gate. The collector now recognizes the canonical root
no-extension filenames `LICENSE-APACHE` and `LICENSE-MIT`, in addition to its
existing `LICENSE` and `COPYING` names with allowed text extensions.

## Targeted Static Validation

The follow-up used existing operator-provided pinned local checkouts only:

| Repository | Pinned revision | License files | `missing_license_file` | Result |
| --- | --- | ---: | --- | --- |
| `uv` | `25ada4d695c8d05232a3b22cef69bcf9858e274a` | 2 | no | passed |
| `actix-web` | `eee23e2326d1f063c2959a71fa642e1b7c3b1dc9` | 2 | no | passed |

The sanitized durable summary is
`tests/fixtures/final_corpus_dual_license_follow_up/p52-t10-dual-license-follow-up.example.json`.
It records the historical P52-T6 48/50 outcome as preserved evidence, rather
than changing an already recorded run.

## Boundary

This follow-up ran static collection and validation only. It did not clone or
fetch repositories, install dependencies, invoke package managers, execute
harvested code, run AI or adapters, accept packages or relations, publish
registry metadata, or change registry truth. No raw prompts, provider
responses, or chain-of-thought were created or persisted.

## Effect on P52 Triage

The two dual-license filename findings have been resolved for the pinned source
revisions. P52-T8's historical triage remains evidence of its original run;
P52-T9 consumes this follow-up when recording the Phase 52 exit decision.
