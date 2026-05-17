# P4-T1 Prepare PR-ready Accepted Package Manifest Entries

Status: Planned
Selected: 2026-05-17
Branch: `feature/P4-T1-prepare-pr-ready-accepted-package-manifest-entries`
Review subject: `p4_t1_pr_ready_accepted_manifest_entries`

## Objective

Add a deterministic and review-safe way to prepare accepted-package manifest entries
for reviewed candidate packages before any cross-repository proposal write operation.

The new workflow path must let operators generate and apply the exact manifest
`path` line that SpecPM proposal automation consumes, while keeping candidate
content movement and candidate copying outside of this new step.

This task enables deterministic PR-ready manifest prep with existing `candidate
-- manifest` flow, and preserves current `promote` behavior for full accepted-source
staging copy operations.

## Deliverables

- Add a new CLI command that prepares and appends a local manifest entry
  for a reviewed candidate without copying the candidate.
- Derive PR-ready manifest paths deterministically from candidate metadata
  (`metadata.id` and `metadata.version`) and optional custom prefix/subdir.
- Reuse safe manifest-entry path validation and deterministic insertion behavior.
- Support explicit manifest-entry overrides when automation paths differ from
  defaults.
- Update docs to describe the new command and recommended order in the workflow.
- Add unit and CLI tests for manifest path inference, explicit path override,
  duplicate handling, and manifest update output.
- Add a validation report artifact in the current task branch.

## Proposed CLI

Prepare a manifest entry for a reviewed candidate:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest /path/to/SPECPM/public-index/accepted-packages.yml
``

Optionally pass a custom path prefix:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest /path/to/SPECPM/public-index/accepted-packages.yml \
  --manifest-entry-prefix public-index/generated
```

If needed, override both prefix-derived path with an explicit entry:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest .../accepted-packages.yml \
  --manifest-entry-path public-index/generated/example.core/0.1.0
```

## Acceptance Criteria

- The command reads candidate metadata from `<candidate>/specpm.yaml` and derives a
  deterministic `packageId` and `version` when no explicit override is supplied.
- The command appends the local manifest entry using the existing deterministic
  insertion rules and keeps duplicate entries idempotent.
- By default the entry path follows `public-index/generated/<packageId>/<version>`.
- `--manifest-entry-prefix` must be merged with the package subdir when
  `--manifest-entry-path` is not provided.
- `--manifest-entry-path` overrides the prefix-based inference.
- Unsafe paths or invalid manifest structure raise explicit validation errors.
- Candidate copy, validation, and file promotion remain unchanged in this task.
- Tests and docs for the new command are added.
- No cross-repository write operations and no dependency installation are added.
- The new command output and behavior are stable for review workflows.

## Trust Boundary

Candidate manifests are generated artifacts and are trusted for local review only.
No untrusted repository source content should be executed by this task.

The new command must not:

- run package managers;
- fetch remotes;
- copy or mutate accepted package directories;
- invoke `specpm validate`;
- execute candidate files.

## Test-First Plan

1. Add focused tests for:
   - inferred default manifest entry (`id`/`version` -> `public-index/generated/...`);
   - explicit manifest-entry-path override;
   - optional subdir override;
   - duplicate manifest entries (idempotent update).
2. Implement deterministic entry preparation function and CLI command in
   `spec_harvester.promoter` and `spec_harvester.cli`.
3. Update docs and workflow references.
4. Add one task validation artifact: execution plan and coverage baseline before
   review.
*** End Patch