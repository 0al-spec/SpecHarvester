# Portable Semantic Proposal Records

P55-T6 carries complete P55 semantic-author results into portable author
handoff packets. It replaces a summary-only review signal with an inert,
digest-bound record while retaining proposal-only authority.

## Input Layout

Pass `--semantic-record-root <path>` to `p53-portable-author-handoff`. A
candidate directory may contain:

```text
<path>/<candidate_id>/
  input-pack.json
  semantic-pass.json
  quality-report.json
```

The files must be the matching P55-T3, P55-T4, and P55-T5 records. Missing
candidate directories remain explicitly `not_available` for compatibility with
existing P53 archives. Partial or malformed directories fail closed.

## Portable Record

The handoff writes `semantic-proposal-record.json` beside `packet.json`. It
contains:

- the complete normalized semantic proposal;
- the deterministic quality report and diagnostics;
- the allowlisted provider receipt;
- candidate, source-bundle, proposal, receipt, quality-report, and record
  SHA-256 bindings.

The record is revalidated before writing. Proposal and receipt digests are
recomputed, the P55-T5 evaluator is rerun, and its output must exactly match the
supplied quality report. Rejected quality reports cannot become portable.

P54 detail generation verifies the packet member digest and every embedded
binding again. It presents the complete record as inert JSON and exposes only
digest/status metadata in the static-versus-AI comparison. Interactive reviewer
controls remain a P55-T7 concern.

## Privacy and Authority

Raw prompts, raw provider responses, hidden reasoning, credentials, and
provider-local paths are not retained. Unknown receipt fields or enabled raw
data persistence flags are rejected.

Portable records cannot apply proposals, materialize candidates, mutate
SpecPM, accept canonical intents, mutate registry truth, or publish packages.
They carry no publication authority.
