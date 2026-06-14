# REVIEW P35-T4 Seed Corpus Plan

## Scope

Reviewed P35-T4 changes against the PRD and Phase 35 contracts:

- `docs/MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`;
- DocC mirror `MultiEcosystemSeedCorpusPlan`;
- `tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json`;
- docs and DocC navigation links;
- `tests/test_docs_contracts.py`;
- Flow archive and `next.md` transition to P35-T5.

## Findings

No actionable findings.

## Checks Reviewed

- Fixture uses `SpecHarvesterCorpusPlan` identity and references P35-T2/P35-T3
  contracts.
- Selected sources cover npm, PyPI, crates, Go, and Swift.
- Deferred and rejected sources are present and machine-readable.
- Selected sources include local checkout requirements, analyzer expectations,
  classifier expectations, and stop conditions.
- Non-authority statements preserve the no clone/fetch/install/execute,
  no registry publication, no acceptance, no baseline seeding, no
  `preview_only` removal, and no AI-as-registry-truth boundary.
- `next.md` points to P35-T5 explainable corpus selection report.

## Follow-Up

No follow-up task required from review.

## Verdict

APPROVED.
