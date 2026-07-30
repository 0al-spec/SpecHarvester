# Portable Semantic Proposal Records

P55-T6 preserves complete, validated semantic proposals in portable author
handoff packets.

Use `--semantic-record-root` with `p53-portable-author-handoff` to supply
candidate-scoped P55-T3 input packs, P55-T4 semantic passes, and P55-T5 quality
reports. The builder revalidates the triplet and emits a self-digesting
`semantic-proposal-record.json`.

The record retains the complete proposal, quality diagnostics, allowlisted
provider receipt, and candidate/source/proposal/receipt bindings. Candidate
detail generation verifies the record and renders it only as inert JSON.

Raw prompts, raw responses, hidden reasoning, credentials, and provider-local
paths are excluded. The record has no proposal application, materialization,
SpecPM mutation, canonical intent acceptance, registry, or publication
authority.
