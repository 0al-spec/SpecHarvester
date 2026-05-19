# Next Task: P9-T1 Derive semantic intent claims from trusted static documentation and public API evidence

**Status:** SELECTED

**Updated:** 2026-05-19

## Description

Generated SpecPM drafts currently infer Swift package product intents such as
`intent.swift.product.puzzlecore` even when repositories include deterministic
DocC, PRD, README, or public API evidence that describes a clearer domain-level
purpose. This task improves draft intent quality without using runtime execution
or LLM inference.

## Acceptance

- Drafts prefer meaningful domain-level intent claims when deterministic static
  documentation or public interface evidence supports them.
- Swift package product intents remain fallback evidence for packages without
  richer intent signals.
- Primary package interface claims ignore generated dependency checkouts,
  fixture manifests, build directories, and historical drafts.
- Quality gates pass and validation includes a Puzzle-like fixture.
