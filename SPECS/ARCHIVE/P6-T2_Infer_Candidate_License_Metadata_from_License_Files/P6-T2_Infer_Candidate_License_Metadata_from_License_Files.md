# P6-T2 — Infer Candidate License Metadata from Allowlisted LICENSE Files

**Status:** PASS  
**Owner:** SpecHarvester Team  
**Updated:** 2026-05-18  

## What Changed

- Collector now emits `licenseHint` on allowlisted license-like files (`LICENSE*`, `COPYING`)
  when the text matches conservative, deterministic patterns.
- Drafter now consumes package manifest licenses first, then falls back to deterministic
  license hints when manifests do not provide license metadata.
- Existing manifest license metadata remains authoritative.
- Added tests in `tests/test_collector.py` for manifest-preferred licenses, MIT-style
  inference, and ambiguous fallback to `UNKNOWN`.

## Acceptance Check

- `P6-T2` is implemented with deterministic behavior and no repository execution.
- Unknown license files remain conservative (`UNKNOWN`) when inference is ambiguous.
- Candidate draft generation now avoids unnecessary `unknown_license` signals for common
  static-licensed cases.
