# P20-T8 DocC Warning Cleanup

## Motivation

DocC static generation succeeds but emits stale warnings that obscure real
documentation regressions:

- `AcceptedPackageUpdateProposals` is linked as a documentation page, but the
  article heading uses symbol-page syntax.
- `RealRepositoryQualityReport` uses DocC symbol-style double-backtick markup
  for literal CLI commands.

The warnings are not runtime failures, but they make CI output noisy and make
future DocC regressions easier to miss.

## Goal

Make DocC generation warning-clean for the known stale warnings while keeping
runtime code, registry behavior, candidate generation, and SpecPM handoff
contracts unchanged.

## Deliverables

- Convert the `AcceptedPackageUpdateProposals` article into a normal DocC
  documentation page so `<doc:AcceptedPackageUpdateProposals>` resolves.
- Replace literal command double-backtick references in
  `RealRepositoryQualityReport` with code formatting that DocC does not treat
  as symbol links.
- Add or update docs-contract coverage so future edits do not reintroduce the
  stale DocC warning sources.
- Record validation output showing DocC generation no longer emits those
  warnings.

## Acceptance Criteria

- DocC generation completes without warnings for:
  - `AcceptedPackageUpdateProposals`;
  - `python -m spec_harvester quality-report`;
  - `specpm validate`.
- Existing Python tests pass.
- `ruff check`, `ruff format --check`, and `git diff --check` pass.
- No runtime behavior or registry output changes.

## Boundaries

This task does not:

- change SpecPM handoff contracts;
- change candidate bundle schemas;
- change registry publication behavior;
- add new runtime commands;
- broaden autonomous scraping or AI behavior.
