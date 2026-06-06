# SpecPM Package Set Alignment

This page mirrors `docs/SPECPM_PACKAGE_SET_ALIGNMENT.md` and maps the SpecPM
package-set contracts to SpecHarvester implementation work.

SpecPM owns package validation, registry indexing, accepted-source review, and
maintainer acceptance. SpecHarvester owns producer-side discovery, candidate
generation, preflight evidence, and static review previews.

## Contract Inputs

SpecHarvester package-set work aligns with:

- Package Sets: aggregate discovery entrypoints, not inheritance;
- Package Relations: explicit `contains`, `composes`, `refines`, `satisfies`,
  `supersedes`, and `related` claims;
- Package Set Search: exact index-based lookup with explicit result scope;
- Package Set Registry Metadata: additive `/v0` metadata and existing
  `package_id` conventions;
- SpecHarvester Monorepo Discovery: workspace inventory, package-set
  candidates, scoped member candidates, relation proposals, and bundle-set
  review evidence;
- Multi-Package Producer Intake: independent maintainer review of each package
  and relation;
- Xyflow Package Set Reference: `xyflow.workspace`, `xyflow.system`,
  `xyflow.react`, and `xyflow.svelte` as separate candidate subjects.

## Producer Artifacts

P25 implementation should produce:

- P25-T2 deterministic workspace inventory with repository URL, exact revision,
  workspace manifests, all workspace include patterns, package manifest paths,
  package metadata, source target paths, proposed SpecPM package IDs, roles,
  and privacy-safe evidence references;
- P25-T3 package-set candidates alongside scoped member package candidates;
- P25-T4 relation proposals with `type`, `source`, `target`, evidence paths, and
  `reviewStatus: producer_observed`;
- P25-T5 bundle-set preflight evidence for unique IDs, required files, digests,
  relation source/target existence, inventory consistency, privacy status, and
  human review boundaries;
- P25-T6 static viewer previews with aggregate package-set summaries, member package
  cards, relation badges, review status, and result-scope examples;
- P25-T7 an `xyflow` smoke scenario with `packages/*`, `examples/*`,
  `tooling/*`, and `tests/*` workspace patterns.

## Boundary

Membership in a package set does not imply inherited capabilities, constraints,
lifecycle state, namespace ownership, trust propagation, or automatic package
selection.

SpecHarvester can preview search expectations, but SpecPM owns registry search
semantics and `/v0` publication.

## Implementation Sequence

1. Deterministic workspace inventory.
2. Package-set and scoped member candidate drafting.
3. Relation proposal output.
4. Bundle-set preflight.
5. Static viewer package-set preview.
6. `xyflow` monorepo smoke.

## Non-Goals

This alignment does not add SpecPM registry mutation, automatic maintainer
acceptance, relation acceptance authority, semantic resolver behavior,
dependency solving, package execution, package script execution, harvested
dependency installation, or trust inheritance across package-set members.
