# Author-Ready Draft Quality Bar

Status: Phase 27 policy

SpecHarvester's product goal is not to create a 100% correct specification.
Its goal is to give the repository author a **valid starter package** that is
personalized to the repository, evidence-backed, and ready for author review.

```text
SpecHarvester -> valid author-ready draft
author + agent -> semantic completion and curation
SpecPM -> validation, registry acceptance, and public index authority
```

## Quality Target

The target is an **author-ready draft**, not an accepted package.

An author-ready draft should be:

- valid under the current SpecPM schema and authoring rules;
- repository-specific rather than generic framework text;
- grounded in deterministic evidence such as manifests, README files, public
  interface indexes, workspace inventory, and package-set relation proposals;
- explicit about aggregate package-set boundaries, selected members, exclusions,
  and `contains` relations when the source repository is a monorepo;
- conservative about claims and capabilities;
- clear about unresolved evidence gaps and author action items;
- safe for a repository author to edit with their own agent without trusting
  model output as registry truth.

The draft should not claim that the upstream author has accepted it, that SpecPM
has accepted it, or that model output is authoritative.

## Valid Starter Package Hard Gate

A generated draft is not author-ready unless the hard gates pass:

- `specpm validate` has no errors for every generated candidate package;
- required candidate bundle files exist:
  - `specpm.yaml`;
  - `specs/*.spec.yaml`;
  - `producer-receipt.json`;
  - `validation-report.json`;
  - `diagnostics.json`;
- producer receipt output hashes match generated files;
- diagnostics contain no critical producer-side errors;
- evidence paths are safe, repo-relative or bundle-relative as documented, and
  do not escape the candidate root;
- generated content keeps `preview_only` or equivalent non-accepted lifecycle
  markers until maintainer review removes them;
- no generated artifact claims registry acceptance, relation acceptance, or
  maintainer approval.

These gates are about shape, provenance, and safety. They do not prove semantic
perfection.

## Author-Ready Stop Policy

SpecHarvester should stop the drafting loop when the draft is valid and the
remaining work is author-reviewable rather than generator-fixable.

Stop when:

- all valid starter package hard gates pass;
- package-set/member topology is internally consistent;
- evidence coverage is sufficient to explain why each major claim exists;
- generic wording is limited and visible;
- unresolved issues are recorded as author action items or evidence gaps;
- additional model iterations would mostly rewrite wording or guess domain
  semantics.

Continue or fail when:

- `specpm validate` fails;
- required bundle files, digests, or receipts are missing;
- package IDs, `sourceTargetPath` values, or relation endpoints drift from
  deterministic inventory;
- the draft relies on unsupported evidence paths;
- the model invents acceptance authority, hidden package members, or
  non-evidenced public capabilities;
- summaries and capabilities are so generic that an author cannot identify what
  should be reviewed.

The informal "80%" threshold means "valid and useful enough for author review",
not a numeric guarantee of correctness.

## Review Dimensions

Machine-readable `author-ready-draft-quality-report.json` reports score the
draft along these dimensions:

| Dimension | Question |
|---|---|
| `validation` | Does every generated package validate with SpecPM? |
| `evidenceCoverage` | Do claims cite deterministic evidence? |
| `repositorySpecificity` | Does the draft reflect this repository rather than a generic ecosystem template? |
| `packageTopology` | Are package-set members, exclusions, and relations internally consistent? |
| `claimConservatism` | Does the draft avoid claims beyond evidence? |
| `authorActionability` | Can the author see what to keep, edit, reject, or investigate? |
| `authorityBoundary` | Does every artifact remain proposal-only and review-gated? |

The report contract is documented in
[`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md).
It maps these dimensions onto bundle-local validation, diagnostics, receipt
planning, evidence outputs, package-set handoff links, and static viewer
metadata where available.

## Author Handoff

An author-ready handoff should include:

- the generated candidate bundle;
- validation and diagnostics reports;
- producer receipt and source revision;
- `author-ready-draft-quality-report.json`;
- evidence links for the main claims;
- package-set draft and relation proposal evidence when relevant;
- AI draft or enrichment proposal evidence when available;
- an author checklist with:
  - summaries to review;
  - capabilities to confirm or reject;
  - weak evidence claims;
  - package members to rename, split, or exclude;
  - missing public interfaces or documentation evidence.

The handoff is successful when it gives the author a strong starting point that
is cheaper to edit than to write from scratch.

## Non-Goals

SpecHarvester does not:

- produce the final accepted package truth;
- guarantee that generated capabilities are domain-complete;
- replace upstream maintainer review;
- remove the need for curated accepted artifacts;
- publish to SpecPM;
- decide registry acceptance;
- become a framework encyclopedia for every ecosystem.

## Next Implementation Tasks

1. Add a stop-policy summary to draft, package-set draft, AI draft, and AI
   enrichment runs.
2. Show author action items and unresolved gaps in the static viewer.
3. Run a real-repository calibration matrix and record how many author edits are
   needed to move drafts from valid starter packages to curated specs.
