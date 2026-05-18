# P6-T3 — Make Namespace and Upstream Owner Comparison Case-Insensitive

**Status:** PASS  
**Owner:** SpecHarvester Team  
**Updated:** 2026-05-18  

## What Changed

- `src/spec_harvester/namespace_reports.py` now compares manifest namespace and
  parsed upstream owner using case-insensitive matching.
- Only namespace/upstream mismatch detection was adjusted; handling of missing
  upstream info and duplicate upstream artifacts remains unchanged.
- Added a dedicated test in `tests/test_namespace_upstream_reports.py` covering
  `SoundBlaster` versus `soundblaster` case-only owner differences.

## Acceptance Check

- `src/spec_harvester/namespace_reports.py` comparison is case-insensitive for
  namespace and upstream owner values.
- False positives from casing-only mismatches are eliminated.
- Existing mismatches and missing upstream behaviors are preserved.
- Coverage remains stable and deterministic.
