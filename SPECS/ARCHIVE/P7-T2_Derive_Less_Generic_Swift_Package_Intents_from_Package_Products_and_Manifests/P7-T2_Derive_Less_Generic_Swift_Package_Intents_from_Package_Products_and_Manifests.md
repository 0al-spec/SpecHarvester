# P7-T2 - Derive Less Generic Swift Package Intents from Package Products and Manifests

Branch: `feature/P7-T2-swift-package-product-intents`
Review subject: `p7_t2_swift_package_product_intents`

## Problem

Local smoke governance still reports duplicate generic
`intent.package.public_repository_metadata` claims across Swift candidates.
Swift `Package.swift` manifests are collected as package evidence, but their
package names and products are not parsed into metadata that the drafter can
use for deterministic intent IDs.

## Goals

- Extract basic Swift package metadata from `Package.swift` files without
  executing SwiftPM or package code.
- Use Swift package product names to derive deterministic, less generic intent
  IDs.
- Preserve existing JavaScript/TypeScript intent derivation behavior.
- Keep generated intents sorted and reviewable.

## Non-Goals

- No SwiftPM invocation.
- No dependency resolution or build graph analysis.
- No broad Swift parser implementation.
- No canonical intent registry changes.

## Deliverables

- Add a bounded static Swift package manifest parser for package name and
  products.
- Record Swift manifest metadata in harvest snapshots.
- Use Swift package metadata in draft capability and intent generation.
- Add regression tests for Swift manifest extraction and Swift-specific intents.
- Add validation report and archive artifacts.

## Acceptance Criteria

- Swift package candidates avoid duplicate generic metadata intents when product
  evidence supports a product-specific deterministic intent.
- Intent derivation remains static and does not execute SwiftPM or package code.
- Existing JavaScript/TypeScript intent behavior remains unchanged.
- Generated intent IDs stay deterministic and sorted.
- Quality gates from `.flow/params.yaml` pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
