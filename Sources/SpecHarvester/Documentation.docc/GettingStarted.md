# Getting Started

Install SpecHarvester locally from a checkout:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the bootstrap harvesting loop:

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

The typical outputs are:

```text
candidates/github.com/example/project/harvest.json
candidates/github.com/example/project/specpm.yaml
candidates/github.com/example/project/specs/project.spec.yaml
accepted/<package_id>/<version>/
```

Use the repository quality gates before opening or merging changes:

```bash
pytest
ruff check src tests
ruff format --check src tests
```

## Useful Paths

- Runtime implementation: `src/spec_harvester/`
- Tests: `tests/test_collector.py`
- Operator docs: `docs/`
- Example inputs: `inputs/repositories.example.yml`
- Generated candidates: `candidates/`
- Accepted-source staging: `accepted/`

## Next Topics

- <doc:Workflow>
- <doc:Architecture>
- <doc:TrustBoundary>
- <doc:ProposalAutomation>
