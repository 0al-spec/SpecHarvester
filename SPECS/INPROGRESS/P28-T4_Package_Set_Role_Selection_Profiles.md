# P28-T4 — Package-Set Role Selection Profiles

## Objective

Add a named package-set role selection profile for generic monorepos so
operators can request useful workspace/member package-set output without
remembering raw role flags such as `--role workspace --role member_package`.

## Motivation

P28-T3 showed that the default `draft-package-set` behavior is conservative:
for real `TanStack/query`, it selected only `tanstack_query.workspace`. The
useful package-set required explicit member-package role selection and produced
`39` candidates, `38` `contains` relation proposals, and `78` fresh contract
files.

That operator knowledge should become declarative CLI vocabulary. The goal is
not to make every possible monorepo decision automatically; it is to provide a
stable named profile that expresses the common "workspace plus primary member
packages" intent.

## Scope

In scope:

- Add a role selection profile or preset to `draft-package-set`.
- Keep the existing explicit `--role` behavior available.
- Define deterministic behavior when a profile and explicit roles are both
  provided.
- Cover the profile with regression tests using package-set fixture data.
- Update CLI help, GitHub docs, DocC, roadmap, workplan, and Flow artifacts.

Out of scope:

- SpecPM baseline comparison changes.
- First-submission or seeded-baseline workflow for repositories without current
  SpecPM generated artifacts.
- Publishing or proposing TanStack/query packages.
- Running package managers, upstream builds, package scripts, or harvested
  repository tests.

## Acceptance Criteria

- `draft-package-set` exposes a named profile for generic monorepos.
- The profile selects `workspace` and `member_package` roles while continuing
  to exclude examples/tooling/test-like roles by default.
- Explicit `--role` selections remain supported and have documented precedence
  when combined with a profile.
- Tests prove the profile selects the same workspace/member shape that P28-T3
  previously required through explicit `--role workspace --role member_package`.
- Documentation explains when to use the profile and that it is producer-side
  evidence selection, not SpecPM registry acceptance.

## Dependencies

- P25 package-set drafting.
- P28-T3 second real repository refresh compare observation.

## Validation Plan

- Targeted package-set drafting tests.
- Full Python test suite.
- Ruff lint and format checks.
- Diff whitespace check.
- Swift docs build and DocC static generation.
