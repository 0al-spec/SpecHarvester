# P33-T2 Next-Corpus Source Manifest Fixture

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 33. Bounded Corpus Expansion Planning

## Motivation

P33-T1 records the bounded expansion policy, but no next corpus can run until
the operator-selected source manifest exists and is reviewable. The manifest is
the root of trust for the next batch: it defines which local checkouts may be
read, which revisions are pinned, why each repository is in scope, and which
package shape the later dry runs should expect.

## Goal

Add a committed next-corpus source manifest fixture for five local public
checkout targets and record its selection rationale without running collection,
drafting, or model enrichment.

## Deliverables

- Add `inputs/p33-next-corpus/repositories.yml` using the existing repository
  source manifest schema.
- Add a machine-readable fixture that records source manifest identity,
  selected repository rationale, expected package shapes, local checkout policy,
  and non-authority boundary.
- Add GitHub docs and DocC docs for the P33-T2 manifest fixture.
- Link the fixture from the bounded corpus expansion plan, roadmap, docs index,
  and current `next.md`.
- Add regression tests that parse the YAML source manifest through
  `read_repository_source_manifests`, verify the five entries, verify pinned
  revisions, and verify the companion fixture.
- Archive Flow artifacts and leave `next.md` on P33-T3.

## Candidate Repositories

- `serena`
- `transmission`
- `mcpm.sh`
- `SpecGraph`
- `SpecPM`

## Acceptance Criteria

- The source manifest contains exactly five enabled entries.
- Every entry has a repository URL, local checkout path, exact revision,
  package id hint, and labels.
- The companion fixture records repository selection rationale and expected
  package shape for each entry.
- The fixture does not use `ref`; every entry is pinned by `revision`.
- The fixture remains local-only and forbids clone, fetch, dependency install,
  harvested code execution, package scripts, registry publication, package or
  relation acceptance, baseline seeding, `preview_only` removal, and AI output
  as registry truth.
- Project docs-contract tests pass.

## Non-Goals

- No collection run.
- No deterministic draft run.
- No live local-model run.
- No candidate-layer triage.
- No SpecPM preflight.
- No SpecPM repository change.
- No registry publication or package acceptance.

## Review Subject

`p33_t2_next_corpus_source_manifest_fixture`
