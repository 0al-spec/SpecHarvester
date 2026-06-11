# P27-T2 — Author-Ready Draft Quality Report

## Objective

Add a machine-readable quality report that tells operators whether a generated
SpecHarvester draft is a valid starter package that is ready for author review,
needs another generator pass, or is blocked.

The report must implement the P27-T1 product boundary:

```text
SpecHarvester -> valid author-ready draft
author + agent -> semantic completion and curation
SpecPM -> validation, registry acceptance, and public index authority
```

## Scope

In scope:

- Define a stable `SpecHarvesterAuthorReadyDraftQualityReport` JSON contract.
- Add an `authorReadyDraft` verdict with statuses:
  - `author_ready_draft`;
  - `needs_regeneration`;
  - `blocked`.
- Derive hard gates from existing validation, diagnostics, producer receipt,
  bundle preflight, and package-set evidence where available.
- Add advisory quality dimensions for repository specificity, evidence
  coverage, capability usefulness, interface depth, package topology, authority
  boundary, and author edit distance.
- Emit structured `authorActionItems[]` that tell authors what to review or
  edit.
- Include the quality report in generated candidate/bundle evidence and receipt
  outputs where practical.
- Update docs, DocC, workplan, and Flow artifacts.

Out of scope:

- Semantic truth judgment for generated specs.
- Automatic SpecPM acceptance or registry publication.
- Model rerun/stop-loop orchestration.
- Static viewer UI beyond documented report availability.
- Changing the existing package-set AI draft proposal contract.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Author-ready success fixture | Verify valid starter package verdict. | Report status is `author_ready_draft`, hard gates pass, action items are review-oriented. |
| Validation failure fixture | Verify blocked verdict. | Invalid SpecPM validation or critical diagnostics produces `blocked`. |
| Weak/generic fixture | Verify regeneration verdict. | Valid but weak evidence or generic content produces `needs_regeneration`. |
| Receipt integration | Verify evidence chain. | Producer receipt includes `quality_report` output with digest. |
| CLI/output integration | Verify operators can generate/read the report. | Draft/package-set outputs include stable report path or command output. |
| Docs contract | Verify public contract is documented. | GitHub docs, DocC, Workplan, and next task references mention the report shape and statuses. |

## Implementation Plan

1. Inspect current quality report, validation report, diagnostics, producer
   receipt, and package-set bundle generation paths.
2. Add a small author-ready quality model and report renderer with deterministic
   verdict rules.
3. Integrate the report into generated candidate bundles and package-set
   bundles without making it acceptance authority.
4. Add regression fixtures for all three statuses and receipt output inclusion.
5. Update docs, DocC, workplan, and Flow archive artifacts.
6. Run the repository gates and open a PR.

## Acceptance Criteria

- A generated candidate or package-set bundle can emit
  `author-ready-draft-quality-report.json`.
- The report declares `apiVersion:
  spec-harvester.author-ready-draft-quality/v0`, `kind:
  SpecHarvesterAuthorReadyDraftQualityReport`, and `schemaVersion: 1`.
- The report contains `authorReadyDraft.status` as one of
  `author_ready_draft`, `needs_regeneration`, or `blocked`.
- Hard gates include validation status, critical diagnostics, evidence link
  presence, required bundle files, receipt availability, and authority boundary.
- Advisory dimensions are present but explicitly non-authoritative.
- `authorActionItems[]` is structured and useful for repository authors.
- Producer receipts include the quality report output where candidate bundles
  already emit receipts.
- Docs explain that `author_ready_draft` means “valid starter package ready for
  author review,” not “finished accepted spec.”
