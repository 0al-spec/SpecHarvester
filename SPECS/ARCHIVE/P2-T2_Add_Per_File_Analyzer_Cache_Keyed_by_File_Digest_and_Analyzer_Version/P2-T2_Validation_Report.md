# P2-T2 Validation Report

Task: Add Per-File Analyzer Cache Keyed by File Digest and Analyzer Version
Branch: `feature/P2-T2-add-per-file-analyzer-cache-keyed-by-file-digest-and-analyzer-version`
Date: 2026-05-17
Verdict: PASS

## Implementation Summary

Implemented an optional per-file analyzer cache for deterministic public
interface analyzers:

- Added `spec_harvester.analyzer_cache.AnalyzerCache`.
- Keyed cache entries by analyzer id, analyzer version, and file SHA-256
  digest.
- Stored deterministic JSON cache records with schema version and analyzer
  metadata.
- Added `cache_dir` support to Python and JavaScript/TypeScript public API
  analyzers.
- Cached Python per-file entrypoint payloads and parse diagnostics.
- Cached JavaScript/TypeScript source entrypoint symbol payloads.
- Ignored malformed, metadata-mismatched, digest-mismatched, and path/evidence
  mismatched cache entries.
- Updated GitHub docs and DocC architecture/trust-boundary pages.

## Validation Commands

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_analyzer_cache.py tests/test_python_public_api.py tests/test_js_ts_public_api.py -q` | PASS, 18 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 62 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 15 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 62 passed, total coverage 90.57% |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

## Trust Boundary Validation

- The cache is optional and local to the operator-supplied directory.
- Analyzer output remains untrusted derived metadata.
- Cache hits require matching analyzer id, analyzer version, file digest, and
  cache schema version.
- Cached path/evidence metadata is validated before reuse to avoid reusing a
  digest-matched payload for the wrong repository-relative path.
- No repository code execution, package script execution, dependency
  installation, build tool execution, or network access was introduced.
- `collect-local` still does not run analyzers or use analyzer caches.

## Residual Risks

- There is no cache eviction policy.
- There is no shared or remote cache.
- Analyzer cache use is not yet exposed through a dedicated CLI command.
- Future Tree-sitter or sandboxed analyzers must include parser/query identity
  in their analyzer id/version contract or use a more specific cache key.
