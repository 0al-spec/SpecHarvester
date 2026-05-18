# P7-T3 - Distinguish Absent License Evidence from Ambiguous Unknown License Evidence

Branch: `feature/P7-T3-license-evidence-classification`
Review subject: `p7_t3_license_evidence_classification`

## Problem

The license/provenance governance report currently treats `metadata.license:
UNKNOWN` as one generic `unknown_license` issue. That hides whether the draft
candidate had no license evidence at all or had license-like evidence that could
not be classified deterministically.

This matters for local smoke triage: absent evidence usually means upstream
metadata is missing from the harvested allowlist, while ambiguous evidence means
a human should inspect a license-like file before accepting or correcting the
candidate.

## Goals

- Preserve deterministic license evidence classification when drafting
  `specpm.yaml`.
- Let the license/provenance report distinguish absent license evidence from
  ambiguous license-like evidence.
- Keep known manifest licenses and known license file hints unchanged.
- Keep report records and issues deterministic and sorted.
- Preserve compatibility with existing manifests that do not yet contain license
  evidence classification metadata.

## Non-Goals

- No full license text classifier.
- No external SPDX database lookup.
- No repository code execution, dependency installation, or network access.
- No changes to accepted package policy or registry promotion behavior.

## Design

- Draft generation will compute both `license` and `licenseEvidence`:
  - `manifest`: package manifest provided a license string.
  - `license_file_hint`: allowlisted license file produced a known static hint.
  - `ambiguous_license_file`: allowlisted license-like file exists but no known
    hint could be inferred.
  - `absent`: no manifest license and no license-like file evidence.
- The generated `specpm.yaml` will include this classification under
  `metadata.licenseEvidence` so governance reports can read it without needing
  access to harvest snapshots.
- The license/provenance report will include the classification in each record
  and split `UNKNOWN` issues:
  - `absent_license_evidence`
  - `ambiguous_unknown_license`
- Existing manifests without `metadata.licenseEvidence` will retain the legacy
  `unknown_license` issue to avoid inventing evidence.

## Deliverables

- Add a small deterministic license evidence classifier to draft generation.
- Parse and emit `metadata.licenseEvidence` in license/provenance records.
- Update license risk evaluation to emit distinct issue codes for absent versus
  ambiguous unknown evidence.
- Add regression tests for:
  - absent license evidence,
  - ambiguous license-like file evidence,
  - known SPDX-like license behavior unchanged,
  - legacy `UNKNOWN` manifests without classification metadata.
- Update documentation and DocC pages for the new report fields and issue codes.
- Add validation report and archive artifacts.

## Acceptance Criteria

- License provenance records include enough evidence classification to separate
  absent license metadata from ambiguous license evidence.
- `UNKNOWN` generated from no manifest license and no license file hint is
  reported differently from unrecognized license-like evidence.
- Existing SPDX-like known license handling remains unchanged.
- Report output remains deterministic and sorted.
- Coverage remains above the configured project threshold.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_license_provenance_risk_reports.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
