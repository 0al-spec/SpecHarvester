# SpecPM Shared Fixture Policy

SpecHarvester generated fixtures and SpecPM contract fixtures must not silently
drift.

SpecPM owns the producer bundle intake contract. SpecHarvester owns generated
producer output. Shared fixtures connect those sides for review, but they do not
make generated content accepted registry authority.

## Boundary

The intended fixture boundary is:

```text
SpecPM contract fixture -> SpecHarvester generated fixture -> reviewable drift check
```

not:

```text
SpecHarvester generated fixture -> automatic SpecPM contract update
```

## Shared Fixture Set

The shared fixture set covers `specpm.yaml`, referenced `specs/*.spec.yaml`,
`producer-receipt.json`, `validation-report.json`, `diagnostics.json`,
producer preflight report, static viewer evidence, and proposal body evidence
links.

## Locking

A shared fixture lock should name the SpecPM repository, human-readable ref,
exact SpecPM commit SHA, SpecHarvester generator commit SHA, fixture profile
such as `generated_spec_package_v0`, and the generated files covered by the
comparison.

The exact commit SHA is the root of trust. A tag or branch name is only a label.

## Drift

Drift exists when a generated fixture no longer satisfies the SpecPM contract it
claims to follow: missing required files, unsupported receipt identity, changed
review semantics, missing proposal evidence links, or mutable refs without an
expected commit SHA.

Expected drift should be handled by a coordinated refresh: update SpecPM
contract examples, record the exact SpecPM commit SHA, refresh SpecHarvester
fixture expectations, rerun producer preflight and proposal evidence checks,
and record the refresh in the pull request.

Future SpecPM CI preflight fixtures should follow
<doc:SpecPMCiPreflightGateSupport>: cover stable producer evidence roles,
proposal evidence links, and exact commit SHA locks without making generated
output registry authority.

## Non-Goals

This policy does not make SpecPM execute SpecHarvester, does not make generated
fixtures registry authority, does not change `public-index/accepted-packages.yml`,
and does not require live network access in ordinary CI.

## Source

The canonical GitHub-facing source is `docs/SPECPM_SHARED_FIXTURE_POLICY.md`.
