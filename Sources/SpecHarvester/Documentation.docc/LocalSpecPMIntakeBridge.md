# Local SpecPM Intake Bridge

Use `build-local-specpm-intake-proposal` to run P54-T8 read-only SpecPM
validation for current Workbench decisions whose disposition is
`accept_for_intake` and reason is `evidence_verified`.

The bridge revalidates the portable archive, packet, catalog, immutable
decision history, and current decision digest. It reconstructs only declared
and digest-verified regular candidate files beneath a temporary root, confirms
that package manifests remain `preview_only`, and invokes only
`specpm validate <package> --json`.

SpecPM output and diagnostics are size-bounded and time-bounded. The normalized
portable result preserves package identity, checked files, capabilities,
intents, intent mappings, warnings, errors, and a report digest without
machine-local temporary paths.

The emitted `SpecHarvesterLocalSpecPMIntakeProposal` is proposal evidence only.
It records zero registry mutations and does not access repository checkouts,
execute harvested code, invoke package managers or AI providers, edit SpecPM
accepted sources, update the public index, remove `preview_only`, create a
SpecPM pull request, or replace maintainer review.
