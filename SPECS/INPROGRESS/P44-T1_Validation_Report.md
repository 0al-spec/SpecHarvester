# P44-T1 Validation Report

Task: Operational MVP Warning Triage

Status: PASS

## Scope

P44-T1 records a producer-side triage artifact for the P43-T5
`package_set_id_missing` AI draft warnings across xyflow, FastAPI, and Gin.

The triage classifies all three warnings as `ai_proposal_shape` issues in the
AI draft proposal layer. It does not classify them as source checkout identity
drift, missing repository evidence, or registry acceptance blockers.

## Artifacts

- `tests/fixtures/operational_mvp_quality_hardening/p44-t1-operational-mvp-warning-triage.example.json`
- `docs/OPERATIONAL_MVP_WARNING_TRIAGE.md`
- `Sources/SpecHarvester/Documentation.docc/OperationalMVPWarningTriage.md`
- Documentation and DocC navigation links in README, capabilities, and roadmap.
- Contract coverage in `tests/test_docs_contracts.py`.

## Fixture Evidence

- Fixture API: `spec-harvester.operational-mvp-warning-triage/v0`
- Fixture kind: `SpecHarvesterOperationalMVPWarningTriage`
- Fixture authority: `producer_operational_mvp_warning_triage_only`
- Source AI comparison digest:
  `sha256:cd03f8486a7cb9bd1dcf6efde1c7660ce6f63457a082207b1e81ee62ff5e327a`
- Source exit report digest:
  `sha256:28d1dc5d3d8ad24d1050e4a7fbb170a00ffa20043c80fbe2bb8a33c375bf78d7`

## Triage Evidence

- `xyflow`: `package_set_id_missing`, enrichment completed with 4 proposals,
  primary cause `ai_proposal_shape`; partial public-interface and fork-origin
  caveats remain P44-T3 manual-correction context.
- `fastapi`: `package_set_id_missing`, enrichment completed with 1 proposal,
  primary cause `ai_proposal_shape`.
- `gin`: `package_set_id_missing`, enrichment completed with 1 proposal,
  primary cause `ai_proposal_shape`.

## Validation Commands

```bash
python3 -m json.tool tests/fixtures/operational_mvp_quality_hardening/p44-t1-operational-mvp-warning-triage.example.json >/dev/null
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_warning_triage or current_next_task'
ruff check tests/test_docs_contracts.py
ruff format --check tests/test_docs_contracts.py
git diff --check
```

## Validation Outcomes

- JSON fixture validation: PASS
- Focused docs contract: PASS, `1 passed, 152 deselected`
- Ruff lint: PASS
- Ruff format check: PASS
- Whitespace diff check: PASS

## Boundaries

P44-T1 did not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, call hosted AI services, run LM
Studio, persist raw prompts, persist raw provider responses, persist
chain-of-thought, enable trusted local adapter execution, run adapter code,
accept packages or relations, publish registry metadata, seed baselines, remove
`preview_only`, or treat AI output as registry truth.
