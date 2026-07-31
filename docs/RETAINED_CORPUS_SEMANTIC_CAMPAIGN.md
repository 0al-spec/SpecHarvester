# Retained-Corpus Semantic Campaign

P55-T10 runs the validated semantic-author flow through Codex 5.3 Spark over
the complete retained P53 corpus. The campaign is resumable, digest-bound, and
proposal-only: it creates review material without changing candidate packages,
SpecPM, registry truth, or publication output.

## Observed Result

| Measure | Result |
| --- | ---: |
| Retained repositories | 100 |
| Completed records | 100 |
| Terminal provider failures | 0 |
| Portable proposals | 42 |
| Eligible for calibration | 4 |
| Requires reviewer attention | 38 |
| Rejected by deterministic quality checks | 58 |
| Provider attempts | 103 |
| Failed provider attempts recovered within budget | 3 |
| Records requiring bounded JSON repair | 8 |
| Recorded provider runtime | 1,307,042 ms |

Every completed proposal was schema-valid and evidence-supported, and the
campaign recorded purpose-claim coverage of 1.00. The main quality limitation
was not transport reliability: 58 proposals inherited or
created capability identifiers outside the accepted candidate namespace, 48
retained a generic static intent, and one contained an unsupported quantitative
claim. No duplicate experimental intent IDs were observed.

The campaign did not reduce the 48 generic static intent references. This is a
negative semantic-quality result: Codex Spark can execute the full corpus
reliably, but the current author/rubric combination does not yet replace generic
intent descriptions consistently enough for automatic downstream use.

## Review State

No human reviewer decisions were supplied to the campaign. All 100 records are
therefore reported as `unreviewed`; none are inferred to be accepted, edited,
rejected, or deferred, and reviewer edit burden is explicitly unavailable. The
42 portable proposals can be loaded into the Phase
54 Workbench for explicit review.

## Reproduction

Run one wave at a time against the pinned local corpus:

```bash
uv run python scripts/run_p55_t10_retained_corpus.py \
  --source-manifest-dir inputs/p53-mass-corpus \
  --source-root /path/to/P53Sources \
  --handoff-root /path/to/P53HandoffT14PortableV3 \
  --readiness-evidence SPECS/EVIDENCE/P55-T9A/P55-T9A_Semantic_Provider_Output_Conformance_Follow-Up.json \
  --work-root /path/to/P55T10SemanticCampaign \
  --wave wave-1
```

Repeat with `wave-2`, `wave-3`, and `wave-4`, then use `--finalize` with
`--output` and `--archive`. Completed digest-valid records are reused. Provider
attempts are capped at two per repository and JSON repair at one attempt per
provider attempt.

## Trust Boundary

The runner reads pinned Git documentation and candidate evidence only. It does
not execute repository code, invoke package managers, persist raw prompts or
responses, retain hidden reasoning or credentials, materialize proposals,
create reviewer decisions, mutate SpecPM, change registry truth, or publish
packages.
