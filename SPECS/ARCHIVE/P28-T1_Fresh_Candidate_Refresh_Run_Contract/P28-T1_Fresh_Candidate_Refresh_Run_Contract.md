# P28-T1 — Fresh Candidate Refresh Run Contract

## Objective

Add a producer-side contract that exports generated package-set bundles into
the fresh generated-root layout expected by SpecPM's
`producer-bundle prepare-refresh-decision` helper.

The task closes the practical gap between:

```text
SpecHarvester package-set bundle
SpecPM generated candidate refresh decision helper
```

without letting SpecHarvester publish registry metadata or decide acceptance.

## Scope

In scope:

- Add a `SpecHarvesterFreshCandidateRefreshRun` JSON artifact.
- Add a CLI command that copies member candidates into
  `<package_id>/<version>/specpm.yaml` and `specs/*.spec.yaml`.
- Record source revision, package-set members, contract-file digests, and
  downstream SpecPM command metadata.
- Document the authority boundary and `noRegistryMutation: true`.
- Update GitHub docs, DocC, roadmap, workplan, and tests.

Out of scope:

- Running SpecPM from SpecHarvester.
- Opening or updating SpecPM pull requests.
- Publishing accepted packages, accepted relations, or registry metadata.
- Mutating curated SpecPM artifacts.
- Executing harvested repository code or package managers.

## Test-First Plan

| Test | Purpose | Expected Result |
| --- | --- | --- |
| Builder test | Verify export from package-set bundle to SpecPM fresh root. | `xyflow.*` candidates appear under `<package_id>/0.1.0` with manifest and spec digests. |
| CLI test | Verify operator command writes JSON and normalized files. | Command returns `0`, writes report, and creates fresh generated root. |
| Safety test | Verify escaped candidate paths are rejected. | Builder raises before copying files outside the package-set root. |
| Docs contract | Verify public docs expose the contract. | GitHub docs, DocC, roadmap, workplan, and root docs mention the new artifact and boundary. |

## Acceptance Criteria

- `fresh-candidate-refresh-run` emits
  `apiVersion: spec-harvester.fresh-candidate-refresh-run/v0`.
- The artifact kind is `SpecHarvesterFreshCandidateRefreshRun`.
- The fresh root layout is `specpm-public-index-generated-root/v0`.
- Package outputs are copied into `<package_id>/<version>` directories.
- Contract-file digests cover `specpm.yaml` and `specs/*.spec.yaml`.
- The report records `specpm producer-bundle prepare-refresh-decision`
  metadata and expected `refresh-decision.json`, `prepare-report.json`, and
  `preflight-report.json` artifacts.
- Authority remains producer evidence only:
  `producerEvidenceAuthority: evidence_only`, `registryAuthority: SpecPM
  maintainer review`, and `noRegistryMutation: true`.
