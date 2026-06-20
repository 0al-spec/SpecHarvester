# Bounded Popular-Library Pilot Output Triage

Status: P46-T4 triage report.

P46-T4 classifies the P46 bounded popular-library pilot outputs from the
P46-T2 static-only run and the P46-T3 AI-enabled run. It does not rerun the
pilot or change registry truth.

The durable fixture is:

```text
tests/fixtures/bounded_popular_library_pilot_output_triage/p46-t4-bounded-popular-library-pilot-output-triage.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.bounded-popular-library-pilot-output-triage/v0
kind: SpecHarvesterBoundedPopularLibraryPilotOutputTriage
authority: producer_triage_evidence_only
```

## Classification Vocabulary

P46-T4 uses these classifications: valid, reviewable, noisy, unsupported,
evidence-gap, and do-not-promote.

Static output is reviewable producer evidence. AI output is proposal-only
review evidence.

## Summary

| Metric | Count |
| --- | ---: |
| Repositories triaged | 6 |
| Reviewable static repositories | 6 |
| Static candidates | 9 |
| Static relations | 3 |
| AI draft completed repositories | 1 |
| AI draft warning repositories | 3 |
| AI draft do-not-promote repositories | 2 |
| AI enrichment completed repositories | 4 |
| AI enrichment warning repositories | 2 |
| Registry-promotion blockers | 4 |

## Repository Triage

| Repository | Static layer | AI draft | AI enrichment | Handoff class |
| --- | --- | --- | --- | --- |
| Flask | reviewable | noisy | noisy | reviewable static with noisy AI |
| Gin | reviewable | do-not-promote | reviewable | reviewable static, AI draft blocked |
| xyflow | evidence-gap | valid | unsupported | reviewable package-set with evidence gaps |
| Cupertino | reviewable | noisy | reviewable | reviewable static with noisy AI |
| NavigationSplitView | reviewable | noisy | reviewable | reviewable static with noisy AI |
| docc2context | reviewable | do-not-promote | reviewable | reviewable static, AI draft blocked |

The reviewable static members are `flask.core`, `gin.core`, `xyflow.react`,
`xyflow.svelte`, `xyflow.system`, `xyflow.workspace`, `cupertino.core`,
`navigation_split_view.core`, and `docc2context.core`.

## Do-Not-Promote Sidecars

Do not promote these AI sidecars:

- `gin.aiDraft`: `ai_json_repair_exhausted`,
  `package_set_subject_metadata_missing`.
- `docc2context.aiDraft`: `ai_json_repair_exhausted`,
  `package_set_subject_metadata_missing`.

These failures do not invalidate the static candidates. They block use of the
affected AI draft sidecars until regenerated or manually corrected.

## Evidence Gaps and Unsupported Output

xyflow has static evidence gaps:

- `partial_public_interface_index`
- `operator_checkout_origin_fork_mismatch`

xyflow AI enrichment is unsupported for registry promotion because it carries
`model_evidence_path_unsupported`.

Gin also carries forward the P45-T8 AI enrichment blocker
`model_evidence_path_unsupported`. It was not observed again in P46-T3, but it
must remain visible for P46-T5 and remains a registry-promotion blocker until
triaged.

Flask, Cupertino, and NavigationSplitView AI draft sidecars are noisy because
of `selected_member_role_unknown`; Flask also carries
`excluded_package_also_selected` and `refined_summary_missing`.

## Boundary

P46-T4 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The triage does not treat AI output as registry truth, does not treat static
output as registry truth, and does not treat adapter output as registry truth.

## Follow-Up

P46-T5 should produce author-facing handoff summaries that separate reviewable
static evidence from noisy, unsupported, evidence-gap, and do-not-promote AI
sidecars.
