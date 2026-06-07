# SpecPM Package Set Alignment

Status: Producer implementation alignment

This document maps the SpecPM package-set contracts to SpecHarvester
implementation work. It is a planning and review contract for monorepo
discovery. It does not add runtime behavior by itself.

SpecPM owns package validation, public registry indexing, accepted-source
review, and maintainer acceptance. SpecHarvester owns producer-side discovery,
candidate generation, preflight evidence, and static review previews.

## SpecPM Contract Inputs

SpecHarvester package-set work should align with these SpecPM contracts:

- Package Sets: aggregate discovery entrypoints, not inheritance.
- Package Relations: explicit relation claims such as `contains`, `composes`,
  `refines`, `satisfies`, `supersedes`, and `related`.
- Package Set Search: exact lookup remains index-based and returns explicit
  result scope rather than requiring root-to-leaf traversal.
- Package Set Registry Metadata: future `/v0` metadata uses additive fields and
  keeps existing `package_id` conventions for registry payloads.
- SpecHarvester Monorepo Discovery: producer output should include workspace
  inventory, stable package ID proposals, package-set candidates, scoped member
  candidates, relation proposals, and bundle-set review evidence.
- Multi-Package Producer Intake: maintainers may accept, reject, or defer each
  generated package and relation independently.
- Xyflow Package Set Reference: the reference monorepo scenario should produce
  `xyflow.workspace`, `xyflow.system`, `xyflow.react`, and `xyflow.svelte` as
  separate candidate subjects with explicit `contains` relations.

## Producer Mapping

SpecHarvester should map the contracts into producer-side artifacts as follows.

### Workspace Inventory

P25-T2 should emit a deterministic workspace inventory before candidate
drafting. The inventory should include:

- repository URL and exact revision;
- workspace manifests such as `pnpm-workspace.yaml`, root `package.json`, or
  ecosystem equivalents;
- all workspace include patterns observed in the pinned manifest;
- package manifest paths;
- package ecosystem, name, and version metadata when available;
- source target paths;
- proposed stable SpecPM package IDs;
- package roles such as `workspace`, `core_runtime`, `react_binding`, or
  `svelte_binding`;
- privacy-safe evidence references.

The inventory is producer evidence. It is not a SpecPM registry payload.

### Package-Set Candidates

P25-T3 should draft aggregate package-set candidates alongside scoped member
package candidates. For a monorepo such as `xyflow`, the aggregate package-set
candidate should preserve broad repository discovery intent while member
packages keep scoped evidence and capabilities precise.

The producer should not collapse all observed intent into one package when
workspace manifests show independently reviewable package subjects.

### Scoped Member Candidates

Member candidates should remain ordinary SpecPM candidate packages. They should
carry only the capabilities, intents, interfaces, compatibility hints, and
evidence supported by their scoped source target.

Membership in a package set must not imply:

- inherited capabilities;
- inherited constraints;
- inherited lifecycle state;
- inherited namespace ownership;
- trust propagation;
- automatic package selection.

### Relation Proposals

P25-T4 should emit relation proposal output as producer-observed review
evidence. Initial monorepo support should start with `contains` relations from
the aggregate workspace package to scoped member packages.

Relation proposals should record:

- relation `type`;
- `source` package ID;
- `target` package ID;
- evidence paths such as workspace manifests and package manifests;
- `reviewStatus: producer_observed`.

SpecHarvester must not mark relations as accepted. Maintainers decide relation
acceptance in SpecPM review.

### Bundle-Set Preflight

P25-T5 should extend candidate bundle preflight for multi-package bundle sets.
The preflight should check:

- unique package IDs;
- per-package required files;
- receipt, validation report, and diagnostics digests;
- relation source and target existence;
- workspace inventory consistency;
- privacy and raw-source boundaries;
- human review status and public-index acceptance boundaries.

The preflight remains producer-side evidence. It must not publish, accept, sign,
install, or execute generated packages.

### Static Viewer

P25-T6 should show package-set review previews without hiding scoped packages
under the aggregate package. The viewer should render:

- aggregate package-set summary;
- scoped member package cards;
- relation proposal badges;
- evidence links and review status;
- exact search result scope examples;
- producer-observed caveats.

### Xyflow Smoke Scenario

P25-T7 adds `xyflow-package-set-smoke`, a deterministic local fixture that
exercises the reference scenario. The smoke shows:

- workspace inventory with `packages/*`, `examples/*`, `tooling/*`, and
  `tests/*` patterns from the pinned `xyflow` snapshot;
- `xyflow.workspace`;
- `xyflow.system`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.workspace contains xyflow.system`;
- `xyflow.workspace contains xyflow.react`;
- `xyflow.workspace contains xyflow.svelte`;
- `bundle-set-preflight.json`;
- `viewer/package-set.json`;
- `xyflow-package-set-smoke.json`.
- `contains` relation proposals from the workspace package to each scoped
  member package;
- bundle-set preflight evidence;
- static viewer output matching the SpecPM reference scenario.

## Identifier Policy

SpecHarvester should propose stable SpecPM package IDs, but it should not claim
namespace authority. Proposed IDs are review inputs.

For package-set work:

- aggregate workspace IDs should use a stable repository or workspace subject,
  such as `xyflow.workspace`;
- scoped package IDs should name the member package boundary, such as
  `xyflow.react`;
- relation source and target IDs must match generated candidate subjects;
- generated IDs should be deterministic for the same repository revision and
  configuration.

## Search and Registry Boundary

SpecHarvester can preview search expectations, but SpecPM owns registry search
semantics. Producer output may include examples such as:

```json
{
  "intent": "intent.ui.node_based_editor",
  "results": [
    {
      "package": "xyflow.workspace",
      "scope": "aggregate",
      "match": "direct"
    },
    {
      "package": "xyflow.react",
      "scope": "package",
      "match": "direct",
      "relations": [
        {
          "type": "contains",
          "source": "xyflow.workspace",
          "target": "xyflow.react"
        }
      ]
    }
  ]
}
```

Those examples are review previews. They are not generated `/v0` registry
payloads unless SpecPM later accepts and indexes the package data.

## Implementation Sequence

The implementation order should be:

1. P25-T2: deterministic workspace inventory.
2. P25-T3: package-set and scoped member candidate drafting.
3. P25-T4: relation proposal output.
4. P25-T5: bundle-set preflight.
5. P25-T6: static viewer package-set preview.
6. P25-T7: `xyflow` monorepo smoke.

This order keeps discovery evidence ahead of candidate generation and keeps
review tooling ahead of public-index proposal automation.

## Non-Goals

This alignment does not add:

- SpecPM registry mutation;
- automatic maintainer acceptance;
- relation acceptance authority;
- semantic resolver behavior;
- dependency solving;
- package execution;
- package script execution;
- harvested dependency installation;
- trust inheritance across package-set members.
