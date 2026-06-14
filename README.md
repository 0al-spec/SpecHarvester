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

SpecHarvester is currently a **developer/operator tool**. The supported
distribution mode is source checkout plus local Python install. It is not yet a
PyPI/Homebrew/Docker-distributed end-user package.

```bash
git clone https://github.com/0al-spec/SpecHarvester.git
cd SpecHarvester
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
spec-harvester --help
```

SpecHarvester now supports the current author-ready producer loop:

```text
local repository checkout
      |
      v
bounded evidence collection
      |
      v
single-package or package-set candidate draft
      |
      v
optional local LM Studio/OpenAI-compatible proposal
      |
      v
optional copied AI-enriched preview candidate
      |
      v
validation, quality report, and static viewer
      |
      v
selected/deferred handoff evidence for SpecPM review
```

The product target is a valid starter package, not a final accepted spec.
Generated candidates remain review evidence until a maintainer accepts them
through SpecPM.

See [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md) for the current capability
map and maturity boundary.

## Bootstrap Example: Single Candidate

Run the current single-candidate loop after the local install above:

```bash
spec-harvester collect-local /path/to/repo \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/github.com/example/project

spec-harvester draft candidates/github.com/example/project \
  --package-id project.core \
  --out candidates/github.com/example/project

spec-harvester render-spec-site \
  --candidate candidates/github.com/example/project \
  --output previews/github.com/example/project
```

For monorepos, the source can be scoped to a folder or file target while still
preserving repository provenance:

```bash
spec-harvester collect-local /path/to/monorepo \
  --target Modules/Player \
  --repository https://github.com/example/project \
  --revision <commit-sha> \
  --out candidates/player
```

This produces:

```text
candidates/github.com/example/project/harvest.json
candidates/github.com/example/project/specpm.yaml
candidates/github.com/example/project/specs/project.spec.yaml
previews/github.com/example/project/index.html
previews/github.com/example/project/spec-package.json
```

Drafted specs are deterministic preview candidates. They must pass SpecPM
validation and maintainer review before they are treated as accepted registry
source. `promote` and `prepare-accepted-entry` are maintainer staging helpers;
they are not public registry publication by themselves.

## Autonomous Batch Example

Run a deterministic local batch without model calls:

```bash
spec-harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --skip-ai
```

Run an AI-enabled local batch through LM Studio or another local
OpenAI-compatible endpoint:

```bash
spec-harvester autonomous-candidate-batch \
  inputs/popular-libraries \
  --out .smoke/autonomous-popular-batch \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --apply-ai-enrichment
```

`--apply-ai-enrichment` is an explicit second opt-in. Clean AI enrichment
proposals are applied into copied preview candidates under:

```text
package-sets/<repository-id>/enriched/<package-id>/
```

The original generated candidates are not mutated, `preview_only` stays true,
and the batch output remains review evidence for SpecPM maintainers.

## Documentation Map

- [`docs/README.md`](docs/README.md): documentation index and operator path
- [`docs/CAPABILITIES.md`](docs/CAPABILITIES.md): current capability map,
  maturity boundary, and non-goals
- [`docs/HOW_IT_WORKS.md`](docs/HOW_IT_WORKS.md): end-to-end workflow
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): component model and boundaries
- [`docs/TRUST_BOUNDARY.md`](docs/TRUST_BOUNDARY.md): zero-trust handling rules
- [`docs/SPECPM_PROPOSAL_AUTOMATION.md`](docs/SPECPM_PROPOSAL_AUTOMATION.md):
  trusted cross-repository proposal flow
- [`docs/ACCEPTED_CANDIDATE_DIFF_REPORTS.md`](docs/ACCEPTED_CANDIDATE_DIFF_REPORTS.md):
  accepted-vs-candidate update review reports
- [`docs/ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md`](docs/ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md):
  build PR-ready accepted package update proposal artifacts
- [`docs/STATIC_SPEC_RENDERER.md`](docs/STATIC_SPEC_RENDERER.md): static
  HTML/JS preview for generated SpecPM candidate packages
- [`docs/LOCAL_SMOKE_FIXTURES.md`](docs/LOCAL_SMOKE_FIXTURES.md): reproducible
  local smoke fixtures for adjacent repository checkouts
- [`docs/ROADMAP.md`](docs/ROADMAP.md): planned delivery phases
- [`SPECS/README.md`](SPECS/README.md): Flow task workflow, PRD, and workplan

## Current Workflow

```text
local repository checkout or source manifest
      |
      v
safe evidence collector
      |
      v
harvest.json + workspace-inventory.json where relevant
      |
      v
deterministic candidate or package-set drafter
      |
      v
specpm.yaml + specs/*.spec.yaml + relation proposals
      |
      v
SpecPM validation, producer preflight, and quality report
      |
      v
static viewer and author/maintainer review
      |
      v
selected/deferred handoff evidence
      |
      v
SpecPM-side preflight and explicit acceptance flow
```

The current repository supports both single-package and package-set preview
loops. It intentionally stops before registry acceptance.

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
.smoke/                   ignored local smoke inputs, candidates, and reports
candidates/               generated candidate evidence and specs
accepted/                 reviewed generated specs and accepted-source staging
generated/                transient generated artifacts, future
```

## Development

Install locally for development:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

For a non-editable pinned Git install, use an exact commit or tag:

```bash
python -m pip install \
  "git+https://github.com/0al-spec/SpecHarvester.git@<commit-or-tag>"
```

The installed console script is:

```bash
spec-harvester --help
```

During source-tree debugging without installing, use:

```bash
PYTHONPATH=src python -m spec_harvester --help
```

Quality gates:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
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
