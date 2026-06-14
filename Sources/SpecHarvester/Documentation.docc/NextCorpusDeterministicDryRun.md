# Next-Corpus Deterministic Dry Run

Status: P33-T3 deterministic producer evidence.

P33-T3 records `SpecHarvesterNextCorpusDeterministicDryRun` with
`apiVersion: spec-harvester.next-corpus-deterministic-dry-run/v0`.

The source manifest is `inputs/p33-next-corpus/repositories.yml`, and the
companion fixture is
`tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json`.

## Deterministic Result

The deterministic `--skip-ai` batch processed all five repositories from the
P33 next bounded corpus:

- `serena` produced `serena.core`;
- `transmission` produced `transmission.core`;
- `mcpm-sh` produced `mcpm.system`;
- `specgraph` produced `specgraph.system`;
- `specpm` produced `specpm.core`.

All five repositories were collected, drafted, preflighted, and classified as
`author_ready_draft` with `stop_for_author_review`. The batch produced five
preview candidates, zero relation proposals, five bundle-set preflights, zero
preflight errors, zero preflight warnings, and zero blocker classes. Every
repository can proceed to P33-T4 live local-model review.

In short, the deterministic result is ready for P33-T4 live local-model review.
The live local-model result is recorded in
<doc:NextCorpusLiveLocalModelBatch>.

## Review Signals

Two package-id review signals remain:

- `mcpm-sh` was hinted as `mcpm.core`, while deterministic package-set drafting
  produced `mcpm.system`;
- `specgraph` was hinted as `specgraph.core`, while deterministic package-set
  drafting produced `specgraph.system`.

These are candidate-layer review findings, not P33-T3 blockers. P33-T5 should
decide whether to accept, defer, regenerate, or adjust package identity policy
for those candidates. The recorded finding id is
`package_id_hint_changed_by_package_set_selection`.

## Non-Authority Boundary

P33-T3 did not clone repositories, fetch remote state, install dependencies,
execute harvested repository code, run package scripts, call a live local-model
provider, accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, create a SpecPM pull request, or
treat AI output as registry truth.

See `docs/NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md` for the full GitHub-facing
record and digest list.
