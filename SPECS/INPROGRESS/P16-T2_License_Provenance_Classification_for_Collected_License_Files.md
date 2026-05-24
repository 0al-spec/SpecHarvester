# P16-T2 License Provenance Classification for Collected License Files

Status: Planned
Task: `P16-T2`
Phase: Phase 16. Real Repository Signal Quality Hardening
Priority: P1
Effort: 2-4 hours
Dependencies: `P15-T4`, `P15-T5`, `P12-T1`, `P12-T6`

## Problem

P12-T1 and P12-T6 already made strict public collection accept common license
filenames such as `LICENSE.txt`.  P15-T4 found a different gap: the governance
license provenance report still treats some collected license-file evidence as
`ambiguous_unknown_license` when the candidate license remains `UNKNOWN`, even
when the evidence path is a standard collected license filename.

For public SpecPM.dev workflows, absence of license evidence remains an error in
strict collection.  Once evidence exists, governance should distinguish
recognizable collected license-file evidence from genuinely ambiguous unknown
license evidence.

## Goals

- Preserve strict missing-license behavior from P12-T1/P12-T6.
- Reduce false-positive `ambiguous_unknown_license` issues when
  `licenseEvidence.paths` contains standard collected license filenames such as
  `LICENSE.txt`.
- Keep truly ambiguous license-like evidence reviewable.
- Document the governance distinction between absent, collected license-file,
  and ambiguous license-file evidence.

## Non-Goals

- Do not implement full license text parsing or ScanCode integration.
- Do not infer SPDX identifiers from arbitrary license body text in this task.
- Do not change batch validation strict/relaxed policy.
- Do not change SpecPM contracts.

## Deliverables

1. Governance license provenance logic that classifies collected standard
   license-file evidence separately from ambiguous unknown license evidence.
2. Regression tests for `UNKNOWN` + `ambiguous_license_file` +
   `paths: [LICENSE.txt]`.
3. Documentation updates for the license provenance report issue classes.
4. Validation report with quality gate results.

## Acceptance Criteria

- `UNKNOWN` with `source: absent` still reports `absent_license_evidence`.
- `UNKNOWN` with truly ambiguous license-like file evidence still reports
  `ambiguous_unknown_license`.
- `UNKNOWN` with a standard collected license filename such as `LICENSE.txt`
  does not report `ambiguous_unknown_license`; it reports a lower-noise
  collected-license-evidence advisory instead.
- Existing known-license records remain issue-free.
- Full Flow quality gates pass.
