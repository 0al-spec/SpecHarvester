# P55-T10G4 Outcome Anchor Source-Authority Ranking

P55-T10G4 separates evidence that describes what a repository is for from
generated or structural text that merely describes how SpecHarvester examined
it. The distinction prevents a plausible generated preview from becoming the
evidence for a semantic intent claim.

## Ranked Evidence

Each outcome-purpose anchor carries an explicit `sourceAuthority` under the
versioned `p55-t10g4-outcome-anchor-source-authority/v1` policy. Selection is
ordered by that authority before the bounded anchor limit is applied, so many
weak root-document phrases cannot displace a later strong package-local source.

Strong authority can support a source-bound purpose claim:

- a pinned descriptive `description` field in the package manifest, including
  field-level provenance and a normalized-value digest;
- pinned package-local documentation;
- pinned repository documentation.

Weak authority remains visible as reviewer context but cannot establish
specificity:

- generated candidate preview and preview mechanics;
- member-package boundary, import, discovery, and module mechanics;
- unclassified documentation and legacy version-one anchor records.

The anchor record reports `strong_anchor_available`, `weak_only`, or
`no_outcome_source`. A legacy v1 record is still readable, but is explicitly
classified as `legacy_unclassified`; it is never silently upgraded to strong
evidence.

## Provider and Reviewer Behaviour

The semantic author input pack preserves the anchor assessment, including an
empty result. Only a pack with at least one strong anchor asks a provider to
make its purpose match a source-bound outcome. A weak-only pack instead marks
the proposal for review, avoiding an unsatisfiable provider instruction.

Quality diagnostics distinguish weak, absent, and legacy outcome sources. Such
proposals are `review_required` and cannot become calibration-eligible solely
because their generated wording sounds specific.

## Integrity and Authority Boundaries

Before a provider is called, the input pack is verified against the pinned
candidate, source bundle, evidence content, and request bindings. An embedded
product profile must have the fixed repository-root/package-local document
topology, and every declared document must match an
`allowlisted_source_documentation` evidence item. Anchor validation reconstructs
the expected authority from that pinned profile and source role, so recomputing
only an outer digest cannot upgrade weak text to strong authority.

This work is proposal-only. It does not run a provider, change provider or
repair budgets, materialize a proposal, or mutate SpecPM, registry, or
publication truth.
