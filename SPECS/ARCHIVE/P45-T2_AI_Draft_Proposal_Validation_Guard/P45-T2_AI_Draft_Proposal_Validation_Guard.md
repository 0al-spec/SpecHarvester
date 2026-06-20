# P45-T2 AI Draft Proposal Validation Guard

## Status

Archived as PASS on 2026-06-20.

## Motivation

P45-T1 normalized safe AI draft subject identity cases, but the boundary between
safe normalization and genuinely ambiguous provider output should be explicit.
Later P45 reruns need deterministic evidence that provider output was checked
before it was accepted as proposal evidence.

## Goal

Add a deterministic AI draft proposal validation guard that reports missing
package-set subject identity and unknown excluded-package references before
provider output is accepted as proposal evidence.

## Deliverables

- Deterministic pre-normalization validation guard for package-set AI draft
  provider output.
- Machine-readable guard summary in proposal artifacts.
- Regression coverage for valid, safely normalized, and ambiguous model output.
- Documentation updates for the proposal-only validation boundary.
- Validation report for the task.

## Acceptance Criteria

- Proposal artifacts include a validation guard record with status and
  diagnostic counts.
- Missing package-set subject identity is reported when neither the provider
  output nor deterministic request context can identify the package set.
- Unknown excluded-package references are reported for multi-package
  inventories before proposal evidence is accepted.
- Safe P45-T1 normalization cases remain clean: request-backed missing
  `packageSet.packageId` and single-package model-side exclusions must not
  become warnings.
- Existing hard failures remain hard failures: package-set id mismatch,
  selected-member unknown, unsupported relation type, and invalid relation
  endpoints still fail closed.
- The guard remains producer-side evidence only and does not accept packages,
  accept relations, publish registry metadata, seed baselines, remove
  `preview_only`, or treat AI output as registry truth.

## Validation Plan

- Run focused package-set AI draft proposal tests.
- Run focused docs-contract tests for the updated contract text and current
  next task.
- Run lint, format, and whitespace checks for touched files.

## Non-Goals

- Do not rerun the bounded operational MVP corpus; that belongs to `P45-T3`.
- Do not broaden the corpus.
- Do not add Workplan tasks.
- Do not call hosted AI services.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
