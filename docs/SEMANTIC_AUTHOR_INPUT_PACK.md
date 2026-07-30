# Semantic Author Input Pack

P55-T3 builds a deterministic `SpecHarvesterAISemanticAuthorInputPack` from a
local preview candidate workspace and an explicitly supplied observed-intent
catalog. It does not invoke a model.

The pack reads only `specpm.yaml`, `specs/*.spec.yaml`, `harvest.json`, an
optional validated `public-interface-index.json`, and explicitly allowlisted
relative documentation paths. Every record retains a class, relative path,
SHA-256, and common source-bundle digest. Documentation is included as bounded,
inert untrusted evidence, never host instructions.

The output includes a P55-T2-valid request and standalone observed intent
records. It rejects absolute/traversal paths, symlinks, malformed candidate
artifacts, invalid interface indexes, stale catalogs, duplicate observed
intents, and exhausted item or byte budgets. It does not execute repository
code, package managers, adapters, providers, review decisions, materialization,
SpecPM mutation, or publication.
