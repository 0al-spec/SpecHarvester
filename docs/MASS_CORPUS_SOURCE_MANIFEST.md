# Mass Corpus Source Manifest

P53-T3 freezes the input boundary for the Phase 53 mass campaign. The two
files in `inputs/p53-mass-corpus/` identify exactly 100 new public GitHub
repositories, assign them to four sequential waves of 25, and record their
full default-branch commit pins as observed from public GitHub metadata on
2026-07-27.

`repositories.yml` is the machine-readable source manifest. Its checkout paths
are expectations under `../../../../P53Sources/`; they are not evidence that a
checkout already exists. `selection-metadata.json` records public popularity,
language, declared license metadata, repository-shape classification, size
ceilings, and the reasons each source was selected. The set is distinct from
the P52 reference corpus.

This is selection evidence only. It did not create, restore, clone, or fetch
checkouts; run static harvesting; invoke `codex exec`, Codex Spark, LM Studio,
or adapters; execute package managers or harvested code; accept packages or
relations; publish registry metadata; remove `preview_only`; or treat a source
selection as registry truth. Raw prompts, provider responses, secrets, session
state, stdout/stderr, and chain-of-thought are not persisted.

P53-T4 must verify every operator-provided checkout is present, clean,
revision-matched, within its size budget, and backed by resolved local license
and provenance evidence. Until that gate passes, every checkout-dependent
metadata field remains explicitly pending and P53-T5 through P53-T15 stay
locked.
