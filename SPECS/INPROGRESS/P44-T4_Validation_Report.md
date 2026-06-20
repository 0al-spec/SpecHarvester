# P44-T4 Validation Report

## Status

Passed.

## Scope

P44-T4 reran the bounded operational MVP corpus after P44-T1 through P44-T3:
xyflow, FastAPI, and Gin. It records static-only and AI-enabled rerun evidence
and compares it against the P43 baseline.

## Runtime Note

During P44-T4 command probing, Homebrew Python 3.10 process startup temporarily
hung. The actual rerun commands were executed with `uv run python` in the
project environment. Subsequent docs-contract validation used the normal
`python` interpreter after it recovered.

## Run Root

```text
/tmp/specharvester-p44-t4-quality-hardened-rerun-20260620T000000Z
```

## Validation Commands

```bash
PYTHONPATH=src uv run python -m spec_harvester source-manifests /tmp/specharvester-p44-t4-quality-hardened-rerun-20260620T000000Z/inputs
PYTHONPATH=src uv run python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p44-t4-quality-hardened-rerun-20260620T000000Z/inputs --out /tmp/specharvester-p44-t4-quality-hardened-rerun-20260620T000000Z/output-static --skip-ai --repository-profile-selection auto
curl --silent --show-error --max-time 5 http://127.0.0.1:1234/v1/models
PYTHONPATH=src uv run python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p44-t4-quality-hardened-rerun-20260620T000000Z/inputs --out /tmp/specharvester-p44-t4-quality-hardened-rerun-20260620T000000Z/output-ai --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1
python3 -m json.tool tests/fixtures/operational_mvp_quality_hardening/p44-t4-operational-mvp-quality-hardened-rerun.example.json >/dev/null
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_quality_hardened_rerun or current_next_task'
```

## Results

- Source manifest parse: passed, `repositoryCount: 3`.
- Static-only rerun: passed.
- LM Studio provider probe: passed, `openai/gpt-oss-20b` available.
- AI-enabled rerun: passed.
- JSON fixture parse: passed.
- Focused docs-contract coverage: `1 passed, 155 deselected`.

## Rerun Summary

| Mode | Processed | Failed | Preflight passed | AI draft proposals | AI enrichment proposals |
| --- | --- | --- | --- | --- | --- |
| static-only | 3 | 0 | 3 | 0 | 0 |
| AI-enabled | 3 | 0 | 3 | 3 | 3 |

AI-enabled enrichment proposal members: 6.

Provider total tokens: 81,003.

## Comparison Summary

- Static-only rerun matches the P43-T4 baseline: 6 candidates, 3 relations,
  xyflow partial interface index, FastAPI/Gin complete interface indexes.
- AI-enabled rerun remains proposal-only and does not apply AI enrichment into
  preview candidates.
- xyflow and FastAPI still report `package_set_id_missing` AI draft warnings.
- Gin now reports `excluded_package_unknown` rather than
  `package_set_id_missing`.
- Resolved warning count: 0.
- Quality-hardening outcome:
  `rerun_passed_but_warning_ambiguity_not_fully_resolved`.

## Authority Boundary

P44-T4 is producer-side review evidence only. It does not accept packages or
relations, publish registry metadata, seed baselines, remove `preview_only`,
enable trusted local adapter execution, apply AI enrichment, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, persist raw prompts, persist raw provider responses, persist
chain-of-thought, or treat quality-hardened rerun output as registry truth.
