# P2-T2 Add Per-File Analyzer Cache Keyed by File Digest and Analyzer Version

Status: Planned
Selected: 2026-05-17
Branch: `feature/P2-T2-add-per-file-analyzer-cache-keyed-by-file-digest-and-analyzer-version`
Review subject: `p2_t2_per_file_analyzer_cache`

## Objective

Add a deterministic per-file analyzer cache so static analyzers can reuse
unchanged file analysis results when the file SHA-256 digest and analyzer
identity/version match.

The cache must remain local, optional, and safe. It must not execute package
content, install dependencies, call networks, trust repository instructions, or
make analyzer output authoritative registry truth.

## Deliverables

- Add a reusable analyzer cache helper module.
- Key cache entries by analyzer id, analyzer version, and source file digest.
- Store deterministic JSON entries with schema version, analyzer metadata, file
  digest, and cached payload.
- Add optional `cache_dir` arguments to Python and JavaScript/TypeScript public
  API analyzers.
- Cache per-file Python entrypoint results, including parse diagnostics.
- Cache per-file JavaScript/TypeScript source entrypoint symbol extraction.
- Add focused tests proving cache hits avoid reparsing unchanged files and cache
  misses occur when analyzer version or file digest changes.
- Update docs and DocC pages for the optional cache behavior.
- Create `SPECS/INPROGRESS/P2-T2_Validation_Report.md` during EXECUTE.

## Acceptance Criteria

- Existing analyzer behavior is unchanged when no cache directory is provided.
- Cache entry paths are deterministic and filesystem-safe.
- Cache hits require matching analyzer id, analyzer version, and file digest.
- Cache entries are ignored if malformed or if metadata does not match.
- Re-running an analyzer over unchanged files can reuse cached per-file results.
- Modifying a file digest or analyzer version produces a cache miss.
- No package code, package scripts, dependency installs, build tools, or network
  calls are introduced.
- Local quality gates from `.flow/params.yaml` pass and are recorded.

## Trust Boundary

The analyzer cache stores derived metadata only. It is untrusted until validated
through the analyzer output schema. Cache data must not grant permission to run
repository code or skip policy checks. Cache writes must be deterministic JSON
records under the operator-supplied cache directory.

## Test-First Plan

| Phase | Input | Output | Verification |
|-------|-------|--------|--------------|
| Cache helper tests | Analyzer id/version/digest/payload fixtures | Failing tests for deterministic keying, metadata matching, malformed entry ignore, and version/digest miss | `PYTHONPATH=src python -m pytest tests/test_analyzer_cache.py` |
| Python analyzer tests | Temp `.py` file and cache dir | Failing test proving unchanged file cache hit avoids `ast.parse` | `PYTHONPATH=src python -m pytest tests/test_python_public_api.py` |
| JS/TS analyzer tests | Temp package and cache dir | Failing test proving unchanged entrypoint cache hit avoids source scanning | `PYTHONPATH=src python -m pytest tests/test_js_ts_public_api.py` |
| Implementation | Test expectations | `analyzer_cache.py`, analyzer cache wiring | Targeted tests pass |
| Full validation | Repository gates | Validation report | Pytest, Ruff, coverage, Swift gates pass |

## TODO Plan

1. Add focused cache helper tests.
2. Add analyzer cache module with deterministic read/write helpers.
3. Add Python analyzer cache wiring for per-file entrypoint/diagnostic payloads.
4. Add JS/TS analyzer cache wiring for source entrypoint symbol payloads.
5. Update docs and DocC cache notes.
6. Run targeted and full quality gates.
7. Record validation results in `P2-T2_Validation_Report.md`.

## Non-Goals

- No cache eviction policy.
- No shared remote cache.
- No analyzer orchestration command.
- No Tree-sitter parser integration.
- No sandbox implementation.
- No cache use in `collect-local`.
