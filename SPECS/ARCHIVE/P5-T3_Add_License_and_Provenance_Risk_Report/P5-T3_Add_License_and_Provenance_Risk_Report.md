# P5-T3 Add License and Provenance Risk Report

## Scope

- Add `governance-license-provenance-report` command.
- Build deterministic advisory issues for license and upstream-provenance signals.
- Generate consistent report summary including dynamic `issuesByCode` counts.
- Add focused tests for SPDX parsing and report counting behavior.
- Update DocC/ docs navigation and workflow references.

## Branch

- `feature/p5-t3-add-license-and-provenance-risk-report`.

## Merge

- Merged to `main` via PR #20.

## Result

- New CLI command: `governance-license-provenance-report`.
- New module: `src/spec_harvester/license_provenance_reports.py`.
- New tests: `tests/test_license_provenance_risk_reports.py`.
- Updated docs: `docs/LICENSE_PROVENANCE_RISK_REPORTS.md`, `Sources/SpecHarvester/Documentation.docc/LicenseProvenanceRiskReports.md`, workflow references.

