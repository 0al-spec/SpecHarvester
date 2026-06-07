# P25-T5 — Bundle-Set Preflight

## Objective

Add a producer-side preflight verifier for generated package-set bundles. The
verifier should validate the whole output directory written by
`draft-package-set`, not only each individual candidate bundle.

## Scope

In scope:

- Add a deterministic `preflight-bundle-set` command that consumes a
  package-set output directory.
- Validate `package-set-draft.json` and `package-relation-proposals.json`
  identity, digest references, and summary counts.
- Validate candidate package IDs are unique and each candidate directory has a
  passing candidate bundle preflight report.
- Validate relation source and target package IDs point to generated
  candidates.
- Validate relation proposal inputs match the current package-set draft and
  workspace inventory digest references.
- Emit a machine-readable report with stable identity fields and sorted
  diagnostics.
- Document the producer/review boundary.

Out of scope:

- SpecPM acceptance, package publication, relation acceptance, or registry
  mutation.
- Executing package scripts, package managers, build systems, or generated
  prompts.
- Static viewer package-set panels. P25-T6 owns viewer work.
- End-to-end `xyflow` smoke scenario. P25-T7 owns the smoke scenario.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Passing package set | Draft an `xyflow`-like package set and run bundle-set preflight. | Report status is `passed`, candidates and relations are counted, and per-candidate reports pass. |
| Dangling relation | Modify a relation target to reference a missing package. | Report status is `failed` with `relation_target_missing`. |
| Digest mismatch | Modify `package-set-draft.json` after relation output is written. | Report status is `failed` with an input digest mismatch diagnostic. |
| Duplicate package ID | Add a duplicate package ID to the draft summary. | Report status is `failed` with `candidate_package_id_duplicate`. |
| CLI coverage | Run `preflight-bundle-set <dir>`. | CLI prints report JSON and exits non-zero on failed preflight. |
| Docs contract | Keep GitHub docs and DocC visible. | Docs name the command, report identity, checked fields, and non-goals. |

## Implementation Plan

1. Add a `bundle_set_preflight` module with report constants, options, and a
   verifier object.
2. Reuse existing candidate bundle preflight for each candidate directory.
3. Cross-check package-set draft candidates, relation proposals, input digests,
   summary counts, review status, and relation endpoints.
4. Wire the verifier into the CLI as `preflight-bundle-set`.
5. Add tests, docs, DocC, validation report, archive, and review artifacts.

## Acceptance Criteria

- `python -m spec_harvester preflight-bundle-set <package-set-dir>` prints a
  deterministic JSON report.
- The report has stable identity:
  `apiVersion: spec-harvester.bundle-set-preflight/v0` and
  `kind: SpecHarvesterBundleSetPreflightReport`.
- A generated `xyflow`-like package set passes bundle-set preflight.
- Missing candidate bundles, duplicate package IDs, dangling relations, digest
  mismatches, and non-passing candidate preflight reports fail the bundle-set
  preflight.
- The verifier does not execute package code, package managers, build tools, or
  generated prompts.
- The verifier remains producer-side evidence and does not accept packages or
  relations automatically.

