# Final 50-Repository Static-Only Gate

P52-T6 runs the approved P52-T5 corpus through the existing deterministic
`autonomous-candidate-batch` pipeline with `skip_ai: true` and automatic static
repository-profile selection. The readiness input is bound to SHA-256 digest
`49b31573ea40eeb1396b0dea67164264d4e7effa1fbc5fc0996b5d0210d5c9af`.

## Result

| Measure | Result |
| --- | ---: |
| Manifest sources | 50 |
| Processed source outcomes | 50 |
| Strict static completion | 48 |
| Static completion rate | 96% |
| Required minimum | 95% |
| Candidate preflights passed | 50 |
| AI draft or enrichment proposals | 0 |
| Adapter executions | 0 |
| P52-T7 | Unlocked |

`uv` and `actix-web` are the two explicit static failures. Both repositories
use root `LICENSE-APACHE` and `LICENSE-MIT` files, while the current strict
collector allowlist reports `missing_license_file` for those names. Their
deterministic drafts and preflights completed, but P52-T6 conservatively counts
the collection validation errors as failures. No source was omitted.

The durable sanitized report is
`tests/fixtures/final_corpus_static_only_gate/p52-t6-final-corpus-static-only-gate.example.json`
with digest
`sha256:64a142093fec3587437702fa4845c1bcddfeaab0c578f7f8c0d9ce3caec805cf`.
It binds the disposable autonomous batch report digest
`sha256:e660723a9006088cbce979100df9a63ec3a9d6aa4f6106f6d0e6c772f6ad5cb3`
and collection validation report digest
`sha256:29ee43d6eb7d98982fda3f52b7fa65ddf8d56491437f4b188532c7a742b16f73`.

## Boundary

The gate wrote deterministic preview candidates only. LM Studio, Codex Spark,
AI draft, AI enrichment, adapters, package managers, builds, repository tests,
and harvested code were not run. The result does not accept packages or
relations, publish registry metadata, seed baselines, remove `preview_only`, or
change registry truth.
The report has no registry authority.
