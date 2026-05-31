# Next Task: P20-T2 — Tuist Manifest Parsing

**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Effort:** 4-8 hours
**Dependencies:** P20-T1
**Status:** In Progress
**Suggested:** 2026-05-31

## Description

Add deterministic Tuist manifest parsing for `Project.swift`, `Workspace.swift`,
and `Tuist.swift`, extracting project names, targets, product/platform hints, and
source globs without executing Tuist, Swift code, package scripts, or build
tools.

## Recently Archived

- P20-T1: Scoped Source Target Harvesting (PASS, 2026-05-31)
- P17-T1: Procedural Style Metrics Report (PASS, 2026-05-29)
- P19-T1: Static Spec Renderer (PASS, 2026-05-29)
- P18-T1: Swift Public API Analyzer (PASS, 2026-05-29)
- P16-T8: Evaluate Multi-Language Duplicate-Code Detector (PASS, 2026-05-28)

## Rationale

P20-T1 makes folder and file targets first-class, which unblocks monorepo
modules that are not standalone SwiftPM packages. Tuist-managed modules still
need better deterministic manifest evidence so generated specs can describe
project/target boundaries without invoking Tuist.

## Next Step

Run SELECT for `P20-T2`, characterize common Tuist manifest shapes, and add a
small static parser with fixtures before expanding generated spec intent rules.
