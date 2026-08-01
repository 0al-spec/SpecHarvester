# P55-T10E Repository and Package Semantic Product Profile

## Objective

Build a deterministic, source-bound semantic product profile that tells the AI
author what the repository and selected package are for before intent selection.

## Dependencies

- P55-T3 semantic author input-pack budgets and evidence model.
- P55-T10/P55-T10C pinned campaign source and candidate bindings.
- P55-T10D context-preserving JSON repair.

## Deliverables

- A versioned semantic product profile containing:
  - explicit repository ID, URL, revision, owner, and name when derivable;
  - candidate ID and repository-relative package target path;
  - package name, description, role, manifest path, and bounded keywords;
  - detected languages, ecosystems, package managers, and analyzer signals;
  - root and nearest package-local documentation bindings;
  - exact source digests and deterministic profile digest.
- Pinned git-object readers for nearest package documentation and projected
  package manifest metadata without using the working tree as authority.
- Campaign workspace integration that emits the profile and package-local
  documentation as allowlisted semantic-author evidence.
- Input-pack validation and budget accounting for the generated profile.
- Focused fixtures for a single package and a nested monorepo package.

## Acceptance Criteria

- Repository identity is explicit and no longer inferred only from a synthetic
  candidate ID or README title.
- A nested package records its own target path, manifest metadata, and nearest
  package README independently from the repository root README.
- All values are deterministically projected from candidate YAML, harvest
  metadata, or pinned git objects and carry source paths plus SHA-256 bindings.
- Root and package documentation remain untrusted content; no documentation is
  interpreted as host instruction.
- Evidence and profile budgets fail closed on unsafe paths, malformed metadata,
  stale digests, or oversized content.
- No repository code, package script, package manager, network fetch, adapter,
  materialization, SpecPM mutation, registry mutation, or publication occurs.
- Python tests pass with at least 90% coverage; Ruff lint and format, diff
  integrity, Swift manifest, and Swift documentation checks pass.

## Non-Goals

- Retrieving relevant SpecPM intents or changing generic reuse diagnostics;
  that is P55-T10F.
- Invoking an AI provider or rerunning repositories; that is P55-T10G.
- Accepting, canonicalizing, materializing, or publishing a proposed intent.

---
**Archived:** 2026-08-01
**Verdict:** PASS
