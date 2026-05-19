# Next Task: P9-T2 Build a deterministic semantic evidence index for domain-level draft intent generation

**Status:** READY

**Updated:** 2026-05-19

## Description

`P9-T1` proved the semantic drafting path with Puzzle, but SpecificationKit
showed the next gap: collected README/DocC evidence is still served to the
drafter as mostly flat headings. Build a deterministic semantic evidence index
that extracts compact, ranked domain clusters from static materials before draft
intent generation.

## Acceptance

- Extract domain terms from allowlisted README, DocC, PRD, package manifests, and
  public interface symbols.
- Normalize and rank domain clusters with evidence paths, without executing
  harvested code or using LLM inference.
- Feed the drafter a compact `SemanticEvidenceIndex` suitable for weak-model or
  deterministic intent generation.
- Cover SpecificationKit-like evidence with clusters for specification pattern,
  predicate composition, context-driven decisioning, feature gating, reactive
  evaluation, and tracing.
- Preserve generated candidates as `preview_only` and keep SpecPM acceptance as a
  review boundary.
