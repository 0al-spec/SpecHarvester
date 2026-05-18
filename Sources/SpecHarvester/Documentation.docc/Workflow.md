# Workflow

SpecHarvester turns public repository metadata into reviewable SpecPM candidate
packages through a controlled, review-first pipeline.

## End-to-End Flow

```text
public repository URL
        |
        v
local checkout at a pinned revision
        |
        v
collect-local
        |
        v
harvest.json
        |
        v
draft
        |
        v
specpm validate
        |
        v
human review
        |
        v
prepare-accepted-entry
        |
        v
promote
        |
        v
accepted package source
```

The current bootstrap supports the first controlled candidate loop:

```text
checkout -> harvest.json -> generated SpecPackage -> SpecPM validation -> promotion copy
```

## Current Commands

Collect static evidence:

```bash
python3 -m spec_harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/github.com/example/project
```

Validate batch repository source manifests without collecting snapshots:

```bash
python3 -m spec_harvester source-manifests inputs
```

See <doc:RepositorySourceManifests> for the supported `inputs/*.yml` schema.

Collect snapshots for all enabled manifest records with local checkouts:

```bash
python3 -m spec_harvester collect-batch inputs --out candidates
```

Collect selected repository IDs:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --select xyflow
```

This writes deterministic `candidates/<repository-id>/harvest.json` paths. See
<doc:BatchCollection>.

Write a batch validation report:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

The report records confidence, policy notes, warning codes, and skipped records.
See <doc:BatchValidationReports>.

Draft a reviewable candidate package:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --out candidates/github.com/example/project
```

If a static analyzer has already emitted a `PublicInterfaceIndex`, pass it to
the drafter to enrich `interfaces.inbound` with package, entrypoint, and symbol
summaries:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --interface-index candidates/github.com/example/project/public-interface-index.json \
  --out candidates/github.com/example/project
```

The drafter validates the index, writes a normalized
`public-interface-index.json` artifact into the candidate directory, and records
it as BoundarySpec evidence. It does not run analyzers during drafting.

`PublicInterfaceIndex.summary.status` is preserved as review metadata:
`complete` means no diagnostics were emitted, `partial` means diagnostics were
emitted while package evidence remains available, and `failed` means diagnostics
were emitted without any package record.

Prepare a deterministic manifest entry for a reviewed candidate:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest accepted/accepted-packages.yml
```

This command:

- derives `packageId` and `packageVersion` from `specpm.yaml`;
- infers `public-index/generated/<packageId>/<version>` as the default entry path;
- updates the accepted manifest deterministically.

Follow the immutability policy before proposing any accepted update:

- never mutate an accepted `<packageId>/<packageVersion>` path directly;
- publish updates as new accepted version paths, including metadata-only
  corrections.

Required audit fields for each proposal include source revision, evidence digests,
old/new package version, changed claims, validation status, and reviewer notes.
See <doc:AcceptedPackageUpdateLifecycle>.

Compare accepted and candidate metadata before update proposal work:

```bash
python3 -m spec_harvester accepted-candidate-diff-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-diff.json
```

See <doc:AcceptedCandidateDiffReports>.

Classify update impact before proposal triage:

```bash
python3 -m spec_harvester accepted-candidate-impact-classification-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/accepted-candidate-impact-classification.json
```

See <doc:AcceptedCandidateImpactClassificationReports>.

Build a PR-ready accepted-package update artifact:

```bash
python3 -m spec_harvester accepted-package-update-proposal \
  candidates/github.com/example/project \
  --accepted-root accepted \
  --output candidates/accepted-package-update-proposal.json \
  --proposal-body candidates/accepted-package-update-proposal.md
```

See <doc:AcceptedPackageUpdateProposals>.

Promote a reviewed candidate into accepted-source staging:

```bash
python3 -m spec_harvester promote candidates/github.com/example/project \
  --accepted-root accepted \
  --manifest accepted/accepted-packages.yml
```

Build a duplicate governance claim report for accepted and candidate metadata:

```bash
python3 -m spec_harvester governance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/governance-claims.json
```

The report summarizes overlapping `intent.*` and `capability` claims for review
prioritization before proposal and promotion.

Build a namespace/upstream relationship review report:

```bash
python3 -m spec_harvester governance-upstream-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/namespace-upstream.json
```

This report highlights namespace collisions, missing `upstream_repository`
artifacts, and namespace-vs-upstream-owner mismatches.

Build a license and provenance risk review report:

```bash
python3 -m spec_harvester governance-license-provenance-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output candidates/license-provenance-risk.json
```

The report highlights missing/standardized license metadata and upstream
provenance risks.

## Review Gates

Every generated candidate should be checked for:

- exact source provenance and pinned revision;
- bounded metadata extraction only;
- conservative package naming and inferred intent/capability language;
- successful `specpm validate` output;
- explicit maintainer review before promotion.

## References

- `docs/HOW_IT_WORKS.md`
- `README.md`
- <doc:TrustBoundary>
- <doc:RepositorySourceManifests>
- <doc:BatchCollection>
- <doc:BatchValidationReports>
- <doc:AcceptedManifestEntries>
- <doc:AcceptedPackageUpdateLifecycle>
- <doc:AcceptedCandidateDiffReports>
- <doc:AcceptedCandidateImpactClassificationReports>
- <doc:AcceptedPackageUpdateProposals>
- <doc:ProposalAutomation>
