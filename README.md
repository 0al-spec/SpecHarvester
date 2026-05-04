# SpecHarvester

SpecHarvester is an AI-assisted pipeline for producing reviewable SpecPM
candidate packages from public repository metadata.

It is intentionally not SpecPM core. SpecPM validates, packs, indexes, and
serves specification packages. SpecHarvester discovers public repositories,
collects safe evidence, drafts candidate `SpecPackage` / `BoundarySpec` files,
and sends them through validation and review.

## Current Bootstrap

This repository currently provides a small safe collector and deterministic
candidate drafter:

```bash
python3 -m spec_harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/github.com/example/project
```

The command writes:

```text
candidates/github.com/example/project/harvest.json
```

The snapshot contains checksums and metadata from allowlisted static files such
as `README.md`, `LICENSE`, `package.json`, `pyproject.toml`, `pnpm-workspace.yaml`,
package manifests, public source entrypoints, and workflow files.

Then draft a reviewable SpecPM candidate from the snapshot:

```bash
python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --out candidates/github.com/example/project
```

The command writes:

```text
candidates/github.com/example/project/specpm.yaml
candidates/github.com/example/project/specs/project.spec.yaml
```

Drafted specs are deterministic candidates. They must pass `specpm validate`
and maintainer review before acceptance.

## Boundary

SpecHarvester:

- reads public repository metadata;
- records provenance and file digests;
- extracts bounded metadata such as package names, descriptions, exports,
  dependency names, script names, and Markdown headings;
- drafts candidate specs from harvested metadata;
- validates candidates with SpecPM.

SpecHarvester does not:

- execute repository scripts;
- install dependencies;
- run package tests;
- access secrets or private credentials;
- treat generated specs as upstream-endorsed truth;
- publish candidates directly into the accepted registry.

Generated specs are candidate, community-observed metadata until reviewed.

## Intended Pipeline

```text
repository list
      |
      v
safe evidence collector
      |
      v
deterministic draft generator
      |
      v
AI-assisted refinement, future
      |
      v
specpm validate
      |
      v
candidate review
      |
      v
accepted public registry source
```

## Repository Layout

```text
src/spec_harvester/       CLI and collector implementation
tests/                    unit tests
docs/                     architecture, boundary, roadmap
inputs/                   example repository lists
candidates/               generated candidate evidence/specs
accepted/                 reviewed generated specs, future
generated/                transient generated artifacts, future
```

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check src tests
ruff format --check src tests
```

## Relationship to SpecPM

SpecHarvester is a producer of candidate package data. SpecPM remains the
package substrate and validation/indexing layer.

Package content can describe desired outputs. Package content cannot command
the host.
