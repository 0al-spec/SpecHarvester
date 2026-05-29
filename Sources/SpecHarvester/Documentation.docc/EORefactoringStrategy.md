# EORefactoringStrategy

This strategy turns the current procedural Python modules into small
behavior-rich objects without changing report schemas, CLI behavior, or
SpecPM/SpecNode contracts.

## Current State

The production Python code still has a procedural core:

- 35 production modules under `src/spec_harvester`;
- about 13.6k source lines;
- about 450 top-level functions versus about 59 class methods;
- about 49 classes, with most of them used as dataclass records or exception
  types rather than behavior owners;
- the largest procedural clusters are `specnode_refinement.py`, `drafter.py`,
  `cli.py`, `collector.py`, public API analyzers, report builders, and
  duplicate-code reporting.

The existing EO seams are useful but still local:

- `SpecPackageManifest` and `ManifestParser`;
- report source records;
- public API payload records and analyzer options;
- semantic keyword taxonomy;
- upstream issue and real-repository rating policies.

The next stage should not rewrite everything. It should introduce stable object
seams around one behavior cluster at a time, preserve public output, and keep
coverage above the configured threshold.

## Target Style

New and refactored Python code should follow these local EO rules:

- Behavior belongs to named objects, not broad top-level helper functions.
- Constructors only store validated inputs; filesystem, subprocess, network,
  provider, or repository reads happen in explicit behavior methods.
- Objects expose business actions such as `report()`, `records()`, `proposal()`,
  `verdict()`, or `payload()`, not generic `process()` or `handle()` methods.
- Data records stay small and immutable when useful, but domain decisions should
  move out of passive dataclasses.
- Refactors preserve JSON schemas, issue codes, markdown output, CLI flags, exit
  codes, and trust-boundary text unless a task explicitly changes them.
- Characterization tests are added before moving mature procedural behavior.

## Refactoring Sequence

### 1. Establish Measurable Baselines

Create deterministic metrics for procedural style:

- top-level function count and span by module;
- method count and span by module;
- behavior-rich class count, excluding DTO-only dataclasses and exceptions;
- largest top-level functions;
- modules with no classes and many top-level functions;
- existing `architecture-lint` advisory count;
- duplicate-code report output for `builtin`, `pylint`, and optional external
  backends when available.

The baseline should be stored as a compact report artifact and used to prove
that refactors reduce procedural concentration without creating style theater.

### 2. Split the CLI Shell from Domain Behavior

Keep `argparse` in `cli.py`, but move command execution bodies into small
command objects. Each object should own one command contract:

- argument normalization;
- delegation to one domain object;
- output writing and exit-code policy;
- error-to-JSON conversion where the CLI contract requires it.

This keeps the CLI procedural shell thin without forcing all parser definition
code into objects prematurely.

### 3. Refactor Report Builders by Output Contract

Report modules are good EO candidates because they have stable observable JSON
contracts. Refactor them one report family at a time:

- accepted candidate diff and impact;
- governance reports;
- namespace and license provenance reports;
- real repository quality reports;
- code duplication reports;
- architecture lint reports.

Each report object should own the domain decision and expose a deterministic
`report()` method. Filesystem traversal and parsing should be injected through
existing source record and manifest objects where possible.

### 4. Refactor Public API Analyzer Pipelines

The public API analyzers should become language-specific analyzer objects with
shared payload and option objects:

- Python analyzer object;
- Go analyzer object;
- JS/TS analyzer object;
- language-neutral interface index writer/reader object.

The goal is not to hide language-specific algorithms. The goal is to move parse,
diagnostic, symbol, and evidence decisions behind named analyzer behaviors.

### 5. Refactor Collector and Drafter in Thin Vertical Slices

`collector.py` and `drafter.py` are central and should be changed last, in thin
slices only:

- repository profile detection;
- license inference;
- semantic evidence extraction;
- intent profile generation;
- package draft assembly;
- output artifact writing.

Each slice needs characterization tests around generated artifacts before
moving logic. Do not combine behavior moves with prompt, schema, or policy
changes in the same PR.

### 6. Refactor SpecNode Orchestration Last

`specnode_refinement.py` has the largest procedural cluster and several external
boundary concerns. It should be split only after report, analyzer, collector,
and drafter seams are stable.

Candidate objects:

- provider request/response adapter;
- refinement job;
- schema-bound result validator;
- semantic review job;
- retry directive set;
- retry orchestrator;
- provider-unavailable result builder.

SpecHarvester must still not implement SpecNode runtime ownership; these objects
should model SpecHarvester-side contracts and validation only.

## PR Strategy

Use stacked or sequential PRs, but keep each PR reviewable:

- one behavior cluster per PR;
- no broad rename-only PRs without behavior movement;
- no schema changes unless the task is explicitly a schema task;
- no mixed prompt and refactor changes;
- no broad test rewrites that hide behavior drift;
- run full Python tests, coverage, ruff, Swift manifest, and DocC build when docs
  or DocC are touched.

Recommended PR size:

- small seam introduction: 100-250 changed lines;
- medium report refactor: 250-600 changed lines;
- large module slice: split before exceeding one stable behavior boundary.

## Acceptance Metrics

Progress is practical when:

- top-level function span decreases in targeted modules;
- behavior-rich object method span increases in targeted modules;
- DTO-only dataclasses do not count as EO progress unless behavior moves into or
  next to them;
- architecture-lint advisory count does not increase;
- duplicate-code report remains at the practical minimum baseline;
- coverage stays above 90%;
- public report snapshots and CLI exit behavior remain stable.

Do not chase zero top-level functions. Pure functions are acceptable for tiny
formatting or normalization policies when object ownership would make the code
less clear. The goal is to move domain decisions and orchestration, not to
mechanically wrap every line in a class.

## Stop Conditions

Pause a refactor track when one of these happens:

- characterization tests cannot describe the existing behavior clearly;
- a public schema change is needed;
- the task starts changing SpecPM or SpecNode contracts;
- the module needs a product decision rather than a structural move;
- review diff becomes dominated by unrelated churn.

In these cases, create a planning task or proposal first, then resume
implementation in a narrower PR.
