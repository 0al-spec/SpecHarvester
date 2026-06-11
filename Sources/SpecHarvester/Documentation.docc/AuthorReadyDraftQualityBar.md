# Author-Ready Draft Quality Bar

SpecHarvester's product goal is to create a **valid starter package** for the
repository author, not a 100% correct final specification.

```text
SpecHarvester -> valid author-ready draft
author + agent -> semantic completion and curation
SpecPM -> validation, registry acceptance, and public index authority
```

## Quality Target

An author-ready draft should be valid under SpecPM, repository-specific,
evidence-backed, conservative about claims, and explicit about unresolved
author action items. For monorepos, it should keep package-set boundaries,
selected members, exclusions, and `contains` relations visible.

The draft remains proposal-only. It must not claim upstream author acceptance,
SpecPM acceptance, relation acceptance, or registry publication authority.

## Valid Starter Package Hard Gate

A generated draft is not author-ready unless:

- `specpm validate` has no errors for every generated candidate package;
- required candidate files exist: `specpm.yaml`, `specs/*.spec.yaml`,
  `producer-receipt.json`, `validation-report.json`, and `diagnostics.json`;
- producer receipt hashes match generated files;
- diagnostics contain no critical producer-side errors;
- evidence paths are safe and do not escape the candidate root;
- generated content stays preview/review lifecycle data until maintainer review
  explicitly accepts it.

These gates prove shape, provenance, and safety. They do not prove semantic
perfection.

## Stop Policy

SpecHarvester should stop the drafting loop when the draft is valid and the
remaining work is author-reviewable rather than generator-fixable.

Stop when validation passes, topology is internally consistent, evidence
coverage explains major claims, generic wording is limited and visible, and
unresolved issues are recorded as evidence gaps or author action items.

Continue or fail when validation fails, required files or digests are missing,
inventory-derived paths drift, relation endpoints are inconsistent, unsupported
evidence paths are used, authority boundaries are violated, or the draft is too
generic for an author to review.

The informal "80%" threshold means "valid and useful enough for author review",
not a numeric guarantee of correctness.

## Review Dimensions

Future machine-readable quality reports should expose:

- `validation`;
- `evidenceCoverage`;
- `repositorySpecificity`;
- `packageTopology`;
- `claimConservatism`;
- `authorActionability`;
- `authorityBoundary`.

The first implementation can derive these from existing validation reports,
bundle preflight reports, AI draft diagnostics, AI enrichment diagnostics, and
viewer metadata before adding a dedicated schema.

## Author Handoff

An author-ready handoff should include the generated candidate bundle,
validation and diagnostics reports, producer receipt, source revision, evidence
links, package-set relation evidence when relevant, optional AI draft or
enrichment proposal evidence, and an author checklist describing what to keep,
edit, reject, or investigate.

The handoff is successful when it gives the author a strong starting point that
is cheaper to edit than to write from scratch.

## Non-Goals

SpecHarvester does not produce final accepted package truth, guarantee
domain-complete capabilities, replace upstream maintainer review, remove the
need for curated accepted artifacts, publish to SpecPM, decide registry
acceptance, or become a framework encyclopedia for every ecosystem.
