# P55-T3 Semantic Author Input Pack

## Objective

Build a deterministic, size-bounded semantic-author input pack from a local
validated candidate workspace and explicitly supplied evidence. The result must
conform to P55-T2 request and observed-intent schema records without invoking a
provider or executing repository content.

## Dependencies

- P55-T1 AI Semantic-Author Product and Authority Contract.
- P55-T2 AI Semantic-Author Schemas and deterministic cross-record validator.
- Existing candidate artifact conventions: `specpm.yaml`, `specs/*.spec.yaml`,
  `harvest.json`, and optional `public-interface-index.json`.

## Deliverables

- A deterministic builder and options object for `SpecHarvesterAISemanticAuthorInputPack`.
- Packaged request and observed-intent records validated against the P55-T2
  schema bundle.
- Fixed evidence classes for candidate YAML, harvest metadata, public interface
  evidence, explicitly allowlisted documentation, and a supplied observed-intent
  catalog.
- Exact repository-relative paths and SHA-256 bindings, a source-bundle digest,
  byte/item budgets, and explicit truncation records.
- Valid, hostile-path, oversized-document, stale-catalog, and malformed-input
  tests plus GitHub Markdown and DocC documentation.

## Input And Read Boundary

The builder may read only files inside the explicitly supplied candidate
workspace:

- required `specpm.yaml` and `harvest.json`;
- `specs/*.spec.yaml` discovered under the workspace;
- optional `public-interface-index.json` after its existing deterministic
  validation;
- caller-supplied relative documentation paths after safe-path and containment
  checks.

The observed-intent catalog is a caller-supplied normalized record with a
logical repository-relative source path, SHA-256, and observed intent IDs. The
builder does not fetch, clone, invoke SpecPM, or read arbitrary external paths.

Documentation content is preserved only as bounded, inert untrusted evidence;
it cannot become host instructions. Symlinks, absolute paths, traversal, unknown
files, malformed YAML/JSON, invalid public-interface indexes, invalid observed
intent IDs, duplicate IDs, and exhausted byte or item budgets fail closed.

## Output Boundary

The pack includes a P55-T2 schema-valid request, standalone observed intent
records, bounded evidence excerpts, and source/budget metadata. Its digest is
computed from stable evidence bindings, not filesystem timestamps or provider
state. The output contains no raw prompts, responses, hidden reasoning,
credentials, private paths, reviewer decisions, or materialized candidate
content.

## Acceptance Criteria

- Repeated builds from the same artifacts produce byte-identical packs.
- Every evidence record has an allowlisted relative path, SHA-256, class, and
  common source-bundle digest.
- Candidate YAML, harvest metadata, optional interface evidence, supplied docs,
  and observed intent catalog are represented when present and within budget.
- P55-T2 request/observed schema validation passes for a valid pack.
- Hostile paths, symlinks, malformed records, stale catalog digest, duplicate
  observed intent IDs, oversized inputs, and budget exhaustion are rejected.
- No provider, package manager, harvested code, adapter, materializer, registry,
  or publication path executes.

## Non-Goals

- Provider invocation, prompting, output parsing, or proposal validation.
- Workbench rendering, reviewer decisions, or candidate materialization.
- Intent canonicalization, package acceptance, SpecPM mutation, or publication.
