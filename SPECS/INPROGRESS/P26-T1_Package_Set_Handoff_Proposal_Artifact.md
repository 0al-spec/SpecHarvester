# P26-T1 — Package-Set Handoff Proposal Artifact

## Objective

Add a reviewable package-set handoff proposal artifact that turns a generated
package-set bundle into structured SpecPM proposal evidence.

## Scope

In scope:

- Add a deterministic `package-set-handoff-proposal` command.
- Read `package-set-draft.json`, `package-relation-proposals.json`,
  optional `bundle-set-preflight.json`, and optional package-set viewer output.
- Emit a machine-readable JSON proposal with member package evidence links,
  relation evidence links, preflight status, viewer links, and external
  registry acceptance decision boundary.
- Emit a Markdown proposal body suitable for a future SpecPM PR or issue.
- Document that the proposal is review evidence only and does not accept
  packages, accept relations, publish registry metadata, or replace maintainer
  review.

Out of scope:

- Opening the cross-repository SpecPM PR.
- Mutating SpecPM accepted sources.
- Defining SpecPM-side package-set acceptance records.
- Uploading viewer artifacts from CI.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Generated package-set proposal | Build from an `xyflow`-like bundle-set output. | Proposal lists aggregate/member packages, 3 `contains` relations, preflight status, and viewer link. |
| Markdown proposal body | Render human-readable handoff body. | Body includes package-set summary, members, relation proposals, evidence links, and review boundary. |
| Missing relation artifact | Run against incomplete bundle-set output. | Command fails with clear diagnostics and does not produce a misleading proposal. |
| CLI coverage | Run `package-set-handoff-proposal --bundle-set ... --output ... --proposal-body ...`. | JSON and Markdown files are written deterministically. |
| Docs contract | Keep GitHub docs and DocC visible. | Docs name the command, JSON kind, evidence roles, and non-goals. |

## Implementation Plan

1. Add a `package_set_handoff_proposal` module with JSON and Markdown builders.
2. Reuse package-set draft/preflight constants instead of duplicating schema
   strings.
3. Wire CLI output and Markdown body writing.
4. Add tests, docs, validation report, archive, and review artifacts.

## Acceptance Criteria

- `python -m spec_harvester package-set-handoff-proposal --bundle-set <dir>`
  prints deterministic JSON.
- The JSON has stable identity:
  `apiVersion: spec-harvester.package-set-handoff-proposal/v0` and
  `kind: SpecHarvesterPackageSetHandoffProposal`.
- The proposal includes member package evidence links, relation proposal
  evidence links, bundle-set preflight status, optional viewer artifact link,
  and `registryAcceptanceDecision.status: external_required`.
- The Markdown body is suitable as review text for a future SpecPM PR.
- The command does not mutate SpecPM, accept packages, accept relations, publish
  registry metadata, execute package code, or run package managers.
