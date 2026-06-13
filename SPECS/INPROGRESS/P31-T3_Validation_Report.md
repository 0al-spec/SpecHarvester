# P31-T3 Validation Report

Task: `P31-T3 Real Selected Candidate Handoff Proposal Dry Run`
Branch: `codex/p31-t3-real-selected-candidate-handoff-proposal-dry-run`
Verdict: PASS

## Summary

Ran `selected-candidate-handoff-proposal` against the recorded P30-T5 selected
candidate handoff evidence and committed the generated JSON and Markdown
handoff artifacts.

The generated JSON fixture records:

- `apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0`;
- `kind: SpecHarvesterSelectedCandidateHandoffProposal`;
- `schemaVersion: 1`;
- `authority: producer_preview_evidence_only`;
- selected candidates: `flask.core`, `gin.core`, `docc2context.core`;
- deferred candidates: `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`,
  `xyflow.system`, `cupertino.core`, `navigation_split_view.core`;
- `registryAcceptanceDecision.status: external_required`;
- no SpecPM PR creation, package acceptance, relation acceptance, baseline
  seeding, `preview_only` removal, or registry publication.

The original P30 local candidate, preflight, and viewer artifact roots were
present during the run, so the helper recorded `local_file` digest sources for
the real selected candidate artifacts. It also preserves a relative path to the
P30-T5 selected handoff dry-run fixture for portability.

## Artifacts

- JSON fixture:
  `tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`
- Markdown companion:
  `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`
- DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/SelectedCandidateHandoffProposalP31T3.md`

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_selected_candidate_handoff_proposal.py tests/test_docs_contracts.py -q` | PASS, `76 passed` |
| `PYTHONPATH=src pytest -q` | PASS, `644 passed, 1 skipped` |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90` | PASS, `644 passed, 1 skipped`, total coverage `90.56%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS, `107 files already formatted` |
| `git diff --check` | PASS |
| `swift package dump-package >/tmp/specharvester-p31-t3-package.json && swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory /tmp/specharvester-p31-t3-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p31-t3-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing unrelated DocC warnings |
| `PYTHONPATH=src python -m spec_harvester selected-candidate-handoff-proposal --selected-handoff-dry-run tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json --output /tmp/specharvester-p31-t3-selected-candidate-handoff-proposal.json --proposal-body /tmp/specharvester-p31-t3-selected-candidate-handoff-proposal.md` | PASS |
| `python -m json.tool /tmp/specharvester-p31-t3-selected-candidate-handoff-proposal.json >/tmp/specharvester-p31-t3-cli-formatted.json` | PASS |
| `cmp -s /tmp/specharvester-p31-t3-selected-candidate-handoff-proposal.json tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json` | PASS |

DocC generation still reports unrelated pre-existing warnings for
`AcceptedPackageUpdateProposals` and inline command references in
`RealRepositoryQualityReport`. No P31-T3 documentation warning was observed.

## Follow-Up

Continue with `P31-T4`: define downstream SpecPM-side preflight expectations
for `SpecHarvesterSelectedCandidateHandoffProposal` evidence.
