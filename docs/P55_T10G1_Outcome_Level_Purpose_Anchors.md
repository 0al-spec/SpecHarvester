# P55-T10G1 Outcome-Level Purpose Anchors

P55-T10G1 adds a deterministic bridge between bounded repository evidence and
semantic purpose authoring. The bridge does not decide what a package is and
does not grant an AI provider authority. It projects source-bound phrases and
non-mechanical outcome terms that a provider proposal and an independent quality
gate can compare.

## Record

`SpecHarvesterOutcomePurposeAnchors` binds:

- the candidate, source bundle, and semantic product profile digests;
- at most eight bounded phrases from the package description and pinned source
  documentation;
- the source path and SHA-256 digest for every phrase;
- outcome terms after deterministic removal of package identity, repository
  identity, technology, import, discovery, and implementation mechanics;
- an `anchorsSha256` digest over the complete record.

All projected phrases remain `untrusted`. The input-pack builder performs no
provider, repository-code, package-manager, materialization, registry, or
publication action.

## Provider and Quality Behavior

The semantic author receives the anchor record with two explicit constraints:
the purpose must match a source-bound outcome and must not only restate package
mechanics. Provider transport validation applies the same deterministic check.

Independent quality diagnostics classify proposals as follows:

| Condition | Diagnostic | Result |
| --- | --- | --- |
| Purpose overlaps a supported outcome term | none | unchanged |
| Purpose has meaningful terms but no anchor overlap | `purpose_outcome_anchor_missing` | review required |
| Purpose contains only identity or mechanics | `purpose_restates_package_mechanics` | rejected |
| Anchor record or evidence binding is stale | `outcome_purpose_anchors_invalid` | rejected |

The frozen P55-T5 thresholds and proposal-only authority remain unchanged.

## Follow-Up Boundary

P55-T10G2 may make repair messages aware of these and existing semantic
violations while retaining the current provider-attempt and repair budgets.
P55-T10G3, not this task, repeats the frozen ten-repository calibration.
