# Mass Corpus Checkout Readiness

`mass-corpus-checkout-readiness` is the P53-T4 gate for the immutable
100-source corpus. It reads `inputs/p53-mass-corpus/repositories.yml` and its
selection metadata, then examines only each expected local checkout.

```bash
PYTHONPATH=src python -m spec_harvester mass-corpus-checkout-readiness \
  inputs/p53-mass-corpus \
  --metadata inputs/p53-mass-corpus/selection-metadata.json \
  --out /tmp/p53-t4-readiness.json
```

All 100 operator-provided checkouts are expected under
`../../../../P53Sources/` relative to the source-manifest directory. A passing
report requires every checkout to exist, be clean, have the pinned revision and
canonical `origin`, remain within its size budget, and contain a root-level
static license, copying, or notice file. The report then sets
`decision.p53T5Unlocked` to `true`.

The command is intentionally fail-closed. Missing checkout, revision or origin
drift, dirty state, unavailable tracked size, size overflow, and absent license
evidence block P53-T5. It does not create, restore, clone, or fetch checkouts;
run package managers or harvested code; invoke Codex, LM Studio, or adapters;
accept packages or relations; publish registry metadata; or persist raw model
input or output.
