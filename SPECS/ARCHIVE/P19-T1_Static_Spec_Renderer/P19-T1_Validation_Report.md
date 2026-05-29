# P19-T1 Validation Report

Task: `P19-T1` Static Spec Renderer
Date: 2026-05-29
Branch: `feature/P19-T1-static-spec-renderer`

## Summary

Verdict: PASS

The static renderer implementation, CLI command, docs, DocC mirror, tests, and
CI smoke integration were validated locally.

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_static_spec_renderer.py -q
```

Result: PASS, `7 passed`.

```bash
PYTHONPATH=src python -m pytest tests/test_static_spec_renderer.py tests/test_docs_contracts.py -q
```

Result: PASS, `33 passed`.

```bash
ruff check src tests
```

Result: PASS, `All checks passed!`.

```bash
ruff format --check src tests
```

Result: PASS, `75 files already formatted`.

```bash
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester \
  --output /tmp/spec-harvester-architecture-lint-p19.json
```

Result: PASS command exit. Report status remains `attention` due to the
pre-existing advisory `manifest_parser_pattern` finding in
`src/spec_harvester/license_provenance_reports.py`; no new renderer-specific
architecture lint finding was reported.

```bash
PYTHONPATH=src python -m spec_harvester code-duplication-report \
  --backend pylint \
  --path src/spec_harvester \
  --min-lines 8 \
  --output /tmp/spec-harvester-pylint-duplicates-p19.json
```

Result: PASS, `duplicateBlockCount: 0`.

```bash
swift package dump-package >/dev/null
```

Result: PASS.

```bash
swift build --target SpecHarvesterDocs
```

Result: PASS.

```bash
PYTHONPATH=src python -m pytest
```

Result: PASS, `446 passed, 1 skipped`.

```bash
PYTHONPATH=src python -m pytest \
  --cov=spec_harvester \
  --cov-report=term-missing \
  --cov-fail-under=90
```

Result: PASS, `446 passed, 1 skipped`, total coverage `91.76%`.

```bash
tmp=$(mktemp -d)
fixture="$tmp/fixture"
candidate="$tmp/candidate"
preview="$tmp/preview"
mkdir -p "$fixture"
cat > "$fixture/README.md" <<'EOF'
# Demo

## API Contract

Render SpecPM package previews.
EOF
cat > "$fixture/LICENSE" <<'EOF'
MIT
EOF
cat > "$fixture/package.json" <<'EOF'
{"name":"@example/demo","version":"0.1.0","description":"Demo package","license":"MIT"}
EOF
PYTHONPATH=src python -m spec_harvester collect-local "$fixture" \
  --repository https://github.com/example/demo \
  --revision 0000000000000000000000000000000000000000 \
  --out "$candidate" >/dev/null
PYTHONPATH=src python -m spec_harvester draft "$candidate" \
  --package-id demo.core \
  --name Demo \
  --out "$candidate" >/dev/null
PYTHONPATH=src python -m spec_harvester render-spec-site \
  --candidate "$candidate" \
  --output "$preview" >/tmp/spec-renderer-smoke.json
test -f "$preview/index.html"
test -f "$preview/assets/spec-renderer.js"
test -f "$preview/assets/spec-renderer.css"
test -f "$preview/spec-package.json"
cat /tmp/spec-renderer-smoke.json
```

Result: PASS, renderer returned `status: ok`, `packageId: demo.core`,
`specCount: 1`, and wrote all expected static files.

## Notes

- The renderer embeds escaped JSON in `index.html` for local `file://` preview
  and also writes `spec-package.json` for static hosting and review tooling.
- The browser renderer reads normalized JSON only; YAML parsing remains in
  trusted local Python code.
- The implementation adds `PyYAML>=6.0` as a direct runtime dependency because
  candidate packages use real SpecPM YAML, not only the limited repository
  source manifest subset parsed elsewhere in SpecHarvester.
