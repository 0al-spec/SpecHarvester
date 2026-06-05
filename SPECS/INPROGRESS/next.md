# Next Task: P24-T1 Harvested Spec Quality Depth

**Phase:** Phase 24. Harvested Spec Quality Depth
**Status:** Planned
**Updated:** 2026-06-05

## Context

The first real SpecHarvester-backed SpecPM proposal for `xyflow.core` is safe,
reviewable, and suitable as a `preview_only` package. Review also showed that
the generated candidate is still mostly an observed public package metadata
contract:

- manifest and BoundarySpec summaries are producer-centric;
- `interfaces.inbound` entries are useful but shallow;
- `compatibility.languages` and `compatibility.platforms` are not explicitly
  tied to fine-grained evidence;
- evidence `supports` mappings cover broad intent/scope/capability claims, but
  not interfaces and compatibility at the same level;
- bounded LM Studio review is useful as review evidence, but must not become
  registry authority or direct file mutation.

## Motivation

Downstream consumers need generated package candidates to become more useful as
package contracts without weakening the trust boundary. The next quality step is
to enrich deterministic evidence and drafting so generated specs describe the
target package boundary more directly while staying `preview_only` and
maintainer-reviewed.

## Goal

Upgrade generated package specs from safe metadata previews to subject-focused
preview contracts.

P24-T1 should:

- use deterministic public evidence first: package manifests, package exports,
  public interface indexes, analyzer outputs, and digests;
- make `interfaces`, `compatibility`, and capability summaries traceable to
  specific evidence;
- reduce producer-centric wording in summaries and scope;
- keep model output as bounded review evidence only, never as authoritative
  registry content.

## Acceptance Sketch

- A generated package such as `xyflow.core` still validates as a SpecPM preview
  package.
- Summary and scope describe the target package boundary, not primarily the
  producer process.
- `interfaces.inbound` entries cite deterministic evidence such as package
  exports or `public-interface-index.json`.
- `compatibility.languages` and `compatibility.platforms` are evidence-backed
  or downgraded to clearly named ecosystem hints.
- BoundarySpec evidence `supports` entries cover capabilities, interfaces, and
  compatibility claims at useful granularity.
- No package scripts, dependency installation, repository runtime behavior, or
  model-authored direct file mutation is introduced.
