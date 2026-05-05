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
specpm.yaml + specs/*.spec.yaml
        |
        v
specpm validate
        |
        v
human review
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

Draft a reviewable candidate package:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --out candidates/github.com/example/project
```

Promote a reviewed candidate into accepted-source staging:

```bash
python3 -m spec_harvester promote candidates/github.com/example/project \
  --accepted-root accepted \
  --manifest accepted/accepted-packages.yml
```

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
- <doc:ProposalAutomation>
