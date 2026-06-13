# P31-T2 Validation Report

Task: `P31-T2 Selected Candidate Handoff Proposal Helper`
Branch: `codex/p31-t2-selected-candidate-handoff-proposal-helper`
Verdict: PASS

## Summary

Implemented the producer-side `selected-candidate-handoff-proposal` helper.
The helper reads a P30 selected handoff dry-run artifact and optional local
candidate, preflight, and viewer roots, then emits
`SpecHarvesterSelectedCandidateHandoffProposal` JSON and Markdown review
artifacts.

The implementation preserves the producer boundary:

- output authority remains `producer_preview_evidence_only`;
- selected candidates must remain `previewOnly: true`;
- selected candidates must have zero-warning, zero-error producer preflight;
- static viewer status must be `ok`;
- registry acceptance remains `external_required` with
  `producerAuthority: evidence_only`;
- the helper does not create a SpecPM PR, mutate candidates, accept packages,
  accept relations, seed baselines, remove `preview_only`, or publish registry
  metadata.

## Implemented

- Added `src/spec_harvester/selected_candidate_handoff_proposal.py`.
- Added CLI command:

  ```bash
  python -m spec_harvester selected-candidate-handoff-proposal \
    --selected-handoff-dry-run <p30-t5-json> \
    --candidate-root <selected-candidate-root> \
    --preflight-root <preflight-root> \
    --viewer-root <viewer-root> \
    --output <proposal.json> \
    --proposal-body <proposal.md>
  ```

- Added regression tests in
  `tests/test_selected_candidate_handoff_proposal.py`.
- Updated selected candidate handoff, SpecPM handoff, roadmap, docs index, and
  DocC documentation.
- Updated docs-contract assertions so the helper command and non-authority
  boundary stay documented.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_selected_candidate_handoff_proposal.py tests/test_docs_contracts.py -q` | PASS, `73 passed` |
| `PYTHONPATH=src pytest -q` | PASS, `641 passed, 1 skipped` |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90` | PASS, `641 passed, 1 skipped`, total coverage `90.55%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS, `107 files already formatted` |
| `git diff --check` | PASS |
| `swift package dump-package >/tmp/specharvester-p31-t2-package.json && swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory /tmp/specharvester-p31-t2-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p31-t2-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing unrelated DocC warnings |
| `PYTHONPATH=src python -m spec_harvester selected-candidate-handoff-proposal --selected-handoff-dry-run tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json --output /tmp/specharvester-p31-t2-selected-candidate-handoff-proposal.json --proposal-body /tmp/specharvester-p31-t2-selected-candidate-handoff-proposal.md` | PASS |
| `python -m json.tool /tmp/specharvester-p31-t2-selected-candidate-handoff-proposal.json >/tmp/specharvester-p31-t2-cli-formatted.json` | PASS |

DocC generation still reports unrelated pre-existing warnings for
`AcceptedPackageUpdateProposals` and inline command references in
`RealRepositoryQualityReport`. No P31-T2 documentation warning was observed.

## CLI Smoke Output

The CLI smoke output contained:

- `kind: SpecHarvesterSelectedCandidateHandoffProposal`;
- `authority: producer_preview_evidence_only`;
- `registryAcceptanceDecision.status: external_required`;
- Markdown title `SpecPM Selected Candidate Handoff Proposal`;
- selected candidate row for `flask.core`;
- non-authority language stating that the proposal does not accept packages.

## Follow-Up

Continue with `P31-T3`: run the helper on the real P30 selected candidate
artifacts and record the resulting dry-run handoff proposal fixture.
