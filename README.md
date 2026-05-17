# SpecHarvester

AI-assisted harvesting pipeline for turning public repository metadata into
reviewable SpecPM candidate packages.

SpecHarvester is intentionally not SpecPM core. SpecPM validates, indexes, and
serves `SpecPackage` bundles. SpecHarvester discovers public repositories,
collects bounded evidence, drafts deterministic candidate specs, and prepares
them for review and promotion.

License: MIT. See [`LICENSE`](LICENSE).

Live DocC documentation:
[https://0al-spec.github.io/SpecHarvester/](https://0al-spec.github.io/SpecHarvester/).

## TL;DR

Run the current bootstrap loop:

```bash
python3 -m spec_harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/github.com/example/project

python3 -m spec_harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --out candidates/github.com/example/project

python3 -m spec_harvester promote candidates/github.com/example/project \
  --accepted-root accepted \
  --manifest accepted/accepted-packages.yml
```

This produces:

```text
candidates/github.com/example/project/harvest.json
candidates/github.com/example/project/specpm.yaml
candidates/github.com/example/project/specs/project.spec.yaml
accepted/<package_id>/<version>/
```

Drafted specs are deterministic candidates. They must pass `specpm validate`
and maintainer review before they are treated as accepted registry source.

## Documentation Map

- [`docs/README.md`](docs/README.md): documentation index and operator path
- [`docs/HOW_IT_WORKS.md`](docs/HOW_IT_WORKS.md): end-to-end workflow
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): component model and boundaries
- [`docs/TRUST_BOUNDARY.md`](docs/TRUST_BOUNDARY.md): zero-trust handling rules
- [`docs/SPECPM_PROPOSAL_AUTOMATION.md`](docs/SPECPM_PROPOSAL_AUTOMATION.md):
  trusted cross-repository proposal flow
- [`docs/ROADMAP.md`](docs/ROADMAP.md): planned delivery phases
- [`SPECS/README.md`](SPECS/README.md): Flow task workflow, PRD, and workplan

## Current Workflow

```text
repository list
      |
      v
safe evidence collector
      |
      v
harvest.json
      |
      v
deterministic candidate drafter
      |
      v
specpm.yaml + specs/*.spec.yaml
      |
      v
specpm validate
      |
      v
candidate review
      |
      v
controlled promotion
      |
      v
accepted public registry source
```

The current repository supports the first controlled candidate loop:

```text
checkout -> harvest.json -> generated candidate -> SpecPM validation -> promotion copy
```

## Scope and Boundary

SpecHarvester:

- reads public repository metadata from allowlisted static files;
- records provenance and file digests;
- extracts bounded metadata such as package names, descriptions, exports,
  dependency names, script names, and Markdown headings;
- drafts candidate specs from harvested metadata;
- validates candidates with SpecPM before promotion.

SpecHarvester does not:

- execute repository scripts;
- install dependencies;
- run harvested repository tests;
- access secrets or private credentials;
- treat generated specs as upstream-endorsed truth;
- publish candidates directly into a public registry.

Generated specs are community-observed candidate metadata until reviewed.

## GitHub Workflow Surface

This repository uses GitHub as an operational surface similar to SpecPM:

- pull requests use [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)
  to capture motivation, goals, validation, and explicit boundaries;
- issue forms under [`.github/ISSUE_TEMPLATE`](.github/ISSUE_TEMPLATE) capture
  repository intake, candidate promotion requests, and trust-boundary concerns;
- CI in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) validates the
  local Python code and the SpecPM integration loop;
- trusted maintainers can use
  [`.github/workflows/propose-to-specpm.yml`](.github/workflows/propose-to-specpm.yml)
  to propose accepted-source diffs into `0al-spec/SpecPM`.

## Repository Layout

```text
src/spec_harvester/       CLI, collector, drafter, promoter
tests/                    unit tests
docs/                     operator docs, architecture, trust boundary, roadmap
SPECS/                    Flow PRD, workplan, commands, and task archives
inputs/                   example repository lists
candidates/               generated candidate evidence and specs
accepted/                 reviewed generated specs and accepted-source staging
generated/                transient generated artifacts, future
```

## Development

Install locally:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Quality gates:

```bash
pytest
ruff check src tests
ruff format --check src tests
```

## CI and Promotion

Pull requests run [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

- `Python tests` installs `.[dev]`, runs Ruff lint, Ruff format check, and pytest.
- `SpecPM integration` checks out SpecPM, collects and drafts a fixture
  candidate, validates it with SpecPM, promotes it into a temporary accepted
  source root, and verifies that `specpm public-index generate` emits `/v0`
  metadata.

Trusted maintainers can use
[`.github/workflows/propose-to-specpm.yml`](.github/workflows/propose-to-specpm.yml)
to turn a validated candidate into a PR against `0al-spec/SpecPM`. The proposal
workflow requires `SPECPM_PROPOSAL_TOKEN` for cross-repository writes and does
not run with write credentials on ordinary pull requests.

## Relationship to SpecPM

SpecHarvester is a producer of candidate package data. SpecPM remains the
package substrate and validation/indexing layer.

Package content can describe desired outputs. Package content cannot command
the host.
