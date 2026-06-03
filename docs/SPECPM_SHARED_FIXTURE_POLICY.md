# SpecPM Shared Fixture Policy

Status: Producer/consumer fixture policy

This policy defines how SpecHarvester keeps generated candidate bundle examples
aligned with SpecPM producer bundle contract examples.

SpecHarvester generates candidate bundles. SpecPM defines the registry intake
contract. Shared fixtures must make that boundary reviewable without turning
SpecHarvester output into SpecPM registry authority.

## Boundary

SpecPM owns:

- producer receipt contract examples;
- public-index producer bundle intake checklist examples;
- accepted-source review vocabulary;
- registry authority and maintainer acceptance policy.

SpecHarvester owns:

- generated candidate bundle examples;
- producer-side preflight examples;
- static viewer examples;
- handoff documentation and proposal evidence links.

The shared fixture boundary is:

```text
SpecPM contract fixture -> SpecHarvester generated fixture -> reviewable drift check
```

not:

```text
SpecHarvester generated fixture -> automatic SpecPM contract update
```

## Shared Fixture Set

The shared fixture set covers producer bundle handoff artifacts:

- `specpm.yaml`;
- `specs/*.spec.yaml`;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- producer preflight report;
- static viewer payload or rendered preview evidence;
- proposal body evidence links.

Fixtures outside this set may remain repository-local smoke fixtures unless a
SpecPM contract references them directly.

## Source Of Truth

SpecPM is the source of truth for the producer bundle intake contract.
SpecHarvester is the source of truth for generated producer output.

When these are compared, the fixture lock must name both sides:

- SpecPM repository URL;
- SpecPM human-readable ref or release label;
- exact SpecPM commit SHA;
- SpecHarvester generator commit SHA;
- fixture profile, such as `generated_spec_package_v0`;
- list of generated files covered by the comparison.

Human-readable refs are labels only. The exact commit SHA is the root of trust.

## Fixture Manifest

A shared fixture or future verifier should use a small manifest shape:

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterSharedSpecPMFixture",
  "fixtureProfile": "generated_spec_package_v0",
  "specpm": {
    "repository": "https://github.com/0al-spec/SpecPM",
    "ref": "main",
    "revision": "<40-char-sha>",
    "contract": "specs/PRODUCER_BUNDLE_PROPOSAL_POLICY.md"
  },
  "specHarvester": {
    "repository": "https://github.com/0al-spec/SpecHarvester",
    "revision": "<40-char-sha>",
    "generator": "spec-harvester draft"
  },
  "fixtures": [
    "specpm.yaml",
    "producer-receipt.json",
    "validation-report.json",
    "diagnostics.json"
  ]
}
```

This manifest is review metadata. It does not make generated content accepted.

## Drift Policy

Drift exists when a SpecHarvester generated fixture no longer satisfies the
SpecPM contract it claims to follow. Examples:

- missing required producer bundle files;
- unsupported receipt `apiVersion`, `kind`, or `receiptProfile`;
- receipt output roles that disagree with SpecPM intake vocabulary;
- changed `humanReview.requiredFor` semantics;
- missing proposal evidence links required by SpecPM intake;
- fixture docs naming a mutable SpecPM ref without an expected commit SHA.

Expected drift must be handled as a coordinated contract update:

1. Update SpecPM contract policy or examples.
2. Record the exact SpecPM commit SHA.
3. Update SpecHarvester generated fixture expectations.
4. Re-run producer preflight and proposal evidence checks.
5. Record the fixture refresh in the SpecHarvester pull request.

Silent drift is not acceptable, even when both repositories still pass their
local test suites.

## Refresh Rules

Fixture refresh pull requests should include:

- reason for refresh;
- old and new SpecPM contract commit SHAs;
- affected fixture profile;
- generated files changed;
- validation commands run in SpecHarvester;
- any SpecPM validation or public-index smoke evidence used for review.

Refreshes should not rewrite historical accepted packages or public registry
state. They update examples, tests, and proposal evidence only.

## Verifier Follow-Up

This policy does not add an automated cross-repository verifier yet. A future
verifier may:

- check out SpecPM at the locked commit SHA;
- read the SpecPM fixture contract or manifest;
- generate a SpecHarvester bundle from a deterministic local fixture;
- compare required file presence, receipt identity, report digests, preflight
  status, static viewer payload, and proposal body evidence links;
- report drift without publishing or accepting a package.

That verifier should stay advisory until SpecPM and SpecHarvester have stable
fixture manifests on both sides.

## Non-Goals

This policy does not:

- make SpecPM execute SpecHarvester;
- make SpecHarvester update SpecPM contracts automatically;
- make generated fixtures registry authority;
- change `public-index/accepted-packages.yml`;
- require live network access in ordinary CI;
- require package script execution or dependency installation.
