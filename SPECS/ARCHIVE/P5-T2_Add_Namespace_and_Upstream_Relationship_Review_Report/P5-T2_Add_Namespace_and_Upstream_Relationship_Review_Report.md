# P5-T2 Add Namespace and Upstream Relationship Review Report

Status: Planned
Selected: 2026-05-18
Branch: `feature/P5-T2-add-namespace-and-upstream-relationship-review-report`
Review subject: `p5_t2_namespace_upstream_review_report`

## Objective

Add an additional governance review report for package-level namespace usage and
upstream-relationship metadata across accepted and candidate `specpm.yaml` files.

The report must help maintainers quickly spot namespace collisions and verify
that reported upstream provenance is present and plausibly aligned with package
IDs.

## Deliverables

- Add parser utilities for namespace and `foreignArtifacts` extraction from
  `specpm.yaml` metadata.
- Add CLI command:
  - `governance-upstream-report`
  - inputs: `--accepted-root`, `--candidates-root`, optional `--output`
  - output: deterministic JSON report with namespace and upstream sections.
- Implement duplicate namespace aggregation and upstream relationship issues:
  - missing `upstream_repository` artifact
  - invalid/malformed `upstream_repository.uri`
  - namespace mismatch against inferred upstream owner from URI when detectable.
- Add regression tests for parsing, duplicate aggregation, and CLI execution.
- Document the report command in operator docs and mirror in DocC.

## Acceptance Criteria

- The report is derived only from local `specpm.yaml` files and does not execute
  analyzers, package scripts, network calls, or package managers.
- Running the command with valid roots returns a deterministic JSON report.
- Namespace duplicates include all claimant packages and provenance.
- Upstream checks include at least one issue classification for each manifest
  with missing or malformed upstream metadata.
- New behavior is covered by tests and keeps repository coverage above 90%.
